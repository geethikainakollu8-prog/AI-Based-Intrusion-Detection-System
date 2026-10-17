from flask import Flask, render_template, request, send_file, redirect, url_for
import pandas as pd
import os
import json
import threading
from datetime import datetime

from predict import predict_intrusion

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)

# NSL-KDD Columns
columns = [
    "duration","protocol_type","service","flag","src_bytes",
    "dst_bytes","land","wrong_fragment","urgent","hot",
    "num_failed_logins","logged_in","num_compromised","root_shell",
    "su_attempted","num_root","num_file_creations","num_shells",
    "num_access_files","num_outbound_cmds","is_host_login",
    "is_guest_login","count","srv_count","serror_rate",
    "srv_serror_rate","rerror_rate","srv_rerror_rate",
    "same_srv_rate","diff_srv_rate","srv_diff_host_rate",
    "dst_host_count","dst_host_srv_count",
    "dst_host_same_srv_rate","dst_host_diff_srv_rate",
    "dst_host_same_src_port_rate","dst_host_srv_diff_host_rate",
    "dst_host_serror_rate","dst_host_srv_serror_rate",
    "dst_host_rerror_rate","dst_host_srv_rerror_rate",
    "label","difficulty"
]

# Store latest result for PDF
latest_result = {}

REPORTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
HISTORY_FILE = os.path.join(REPORTS_DIR, "analysis_history.json")
HISTORY_LOCK = threading.Lock()


def ensure_history_file():
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w", encoding="utf-8") as file:
            json.dump([], file)


def load_history():
    ensure_history_file()
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError):
        return []

    return data if isinstance(data, list) else []


def write_history(entries):
    temp_path = HISTORY_FILE + ".tmp"
    with open(temp_path, "w", encoding="utf-8") as file:
        json.dump(entries, file, indent=2)
    os.replace(temp_path, HISTORY_FILE)


def save_history_entry(entry):
    with HISTORY_LOCK:
        entries = load_history()
        entries.insert(0, entry)
        entries = entries[:10]
        write_history(entries)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/history")
def history():
    return render_template("history.html", entries=load_history())


@app.route("/clear-history")
def clear_history():
    with HISTORY_LOCK:
        write_history([])
    return redirect(url_for("home"))


@app.route("/sample-file")
def sample_file():
    return send_file(
        os.path.join(app.root_path, "sample_test.csv"),
        as_attachment=True,
        download_name="sample_test.csv"
    )


@app.route("/predict", methods=["POST"])
def predict():

    global latest_result

    try:

        file = request.files["file"]

        df = pd.read_csv(file, header=None)

        feature_columns = columns[:-2]
        expected_columns = len(feature_columns)

        if len(df.columns) == expected_columns:
            if str(df.iloc[0, 0]).strip().lower() == "duration":
                df = df.iloc[1:].reset_index(drop=True)
            df.columns = feature_columns
        elif len(df.columns) == len(columns):
            if str(df.iloc[0, 0]).strip().lower() == "duration":
                df = df.iloc[1:].reset_index(drop=True)
            df.columns = columns
            df.drop(columns=["label", "difficulty"], inplace=True)
        else:
            raise ValueError(
                f"CSV must contain {expected_columns} feature columns "
                f"or {len(columns)} NSL-KDD columns."
            )

        # Remove label & difficulty columns
        df = df.drop(columns=["label", "difficulty"], errors="ignore")

        result = predict_intrusion(df)

        latest_result = result

        latest_result["date"] = datetime.now().strftime("%d-%m-%Y %I:%M %p")

        save_history_entry({
            "date": latest_result["date"],
            "prediction": result["prediction"],
            "risk": result["risk"],
            "confidence": float(result["confidence"]),
            "total_records": int(result["total_records"]),
            "attack_count": int(result["attack_count"]),
            "normal_count": int(result["normal_count"]),
            "attack_percentage": float(result["attack_percentage"]),
            "normal_percentage": float(result["normal_percentage"]),
            "file_name": getattr(file, "filename", "uploaded.csv")
        })

        return render_template(
            "result.html",
            prediction=result["prediction"],
            confidence=result["confidence"],
            risk=result["risk"],
            total_records=result["total_records"],
            attack_count=result["attack_count"],
            normal_count=result["normal_count"],
            attack_percentage=result["attack_percentage"],
            normal_percentage=result["normal_percentage"],
            analysis_date=latest_result["date"]
        )

    except Exception as e:
        return f"<h2>Error</h2><br>{e}"


@app.route("/download-report")
def download_report():

    reports_dir = os.path.join(app.root_path, "reports")
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)

    filename = os.path.join(reports_dir, "AI_Intrusion_Report.pdf")

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph("AI Intrusion Detection Report", styles["Title"])
    )

    story.append(
        Paragraph("<br/>", styles["BodyText"])
    )

    story.append(
        Paragraph(f"Analysis Time : {latest_result.get('date','')}", styles["BodyText"])
    )

    story.append(
        Paragraph(f"Prediction : {latest_result.get('prediction','')}", styles["BodyText"])
    )

    story.append(
        Paragraph(f"Confidence : {latest_result.get('confidence','')} %", styles["BodyText"])
    )

    story.append(
        Paragraph(f"Risk Level : {latest_result.get('risk','')}", styles["BodyText"])
    )

    story.append(
        Paragraph(f"Total Records : {latest_result.get('total_records','')}", styles["BodyText"])
    )

    story.append(
        Paragraph(f"Attack Records : {latest_result.get('attack_count','')}", styles["BodyText"])
    )

    story.append(
        Paragraph(f"Normal Records : {latest_result.get('normal_count','')}", styles["BodyText"])
    )

    story.append(
        Paragraph(f"Attack Percentage : {latest_result.get('attack_percentage','')} %", styles["BodyText"])
    )

    story.append(
        Paragraph("<br/>Security Recommendations", styles["Heading2"])
    )

    story.append(
        Paragraph("• Enable Firewall", styles["BodyText"])
    )

    story.append(
        Paragraph("• Monitor Suspicious Traffic", styles["BodyText"])
    )

    story.append(
        Paragraph("• Scan for Malware", styles["BodyText"])
    )

    story.append(
        Paragraph("• Block Suspicious IP Addresses", styles["BodyText"])
    )

    doc.build(story)

    return send_file(filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)