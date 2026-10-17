import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load model and encoders from the project directory regardless of current working directory
model = joblib.load(os.path.join(BASE_DIR, "model.pkl"))
encoders = joblib.load(os.path.join(BASE_DIR, "encoders.pkl"))

# Categorical columns used during training
categorical_columns = [
    "protocol_type",
    "service",
    "flag"
]


def predict_intrusion(df):

    # Make a copy so original data isn't modified
    df = df.copy()

    # Encode categorical columns
    for col in categorical_columns:

        if col in df.columns:

            encoder = encoders[col]

            # Handle unknown values safely
            df[col] = df[col].apply(
                lambda x: encoder.transform([x])[0]
                if x in encoder.classes_
                else 0
            )

    # Predict every record
    predictions = model.predict(df)

    # Prediction probabilities
    probabilities = model.predict_proba(df)

    # Statistics
    total_records = len(predictions)

    attack_count = (predictions == 0).sum()

    normal_count = (predictions == 1).sum()

    attack_percentage = round(
        (attack_count / total_records) * 100,
        2
    )

    normal_percentage = round(
        (normal_count / total_records) * 100,
        2
    )

    confidence = round(
        probabilities.max(axis=1).mean() * 100,
        2
    )

    # Overall result
    if attack_count > normal_count:
        prediction = "Attack Detected"
        risk = "High"
    else:
        prediction = "Normal Traffic"
        risk = "Low"

    return {
        "prediction": prediction,
        "confidence": confidence,
        "risk": risk,
        "total_records": total_records,
        "attack_count": attack_count,
        "normal_count": normal_count,
        "attack_percentage": attack_percentage,
        "normal_percentage": normal_percentage
    }