import pandas as pd
import joblib

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# ==============================
# NSL-KDD Column Names
# ==============================

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

print("Loading Dataset...")

df = pd.read_csv(
    "dataset/KDDTrain+.txt",
    names=columns
)

print("\nDataset Loaded Successfully")
print(df.head())

print("\nDataset Shape :", df.shape)

# ==============================
# Binary Classification
# ==============================

df["label"] = df["label"].apply(
    lambda x: "normal" if x == "normal" else "attack"
)

# ==============================
# Encode Categorical Columns
# ==============================

encoders = {}

categorical_columns = [
    "protocol_type",
    "service",
    "flag"
]

for col in categorical_columns:

    encoder = LabelEncoder()

    df[col] = encoder.fit_transform(df[col])

    encoders[col] = encoder

joblib.dump(encoders, "encoders.pkl")

print("Encoders Saved")

# ==============================
# Encode Target
# ==============================

target_encoder = LabelEncoder()

df["label"] = target_encoder.fit_transform(df["label"])

joblib.dump(target_encoder, "target_encoder.pkl")

# ==============================
# Features & Target
# ==============================

X = df.drop(
    columns=["label", "difficulty"]
)

y = df["label"]

# ==============================
# Train/Test Split
# ==============================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print("\nTraining Samples :", len(X_train))
print("Testing Samples :", len(X_test))

# ==============================
# Train Model
# ==============================

print("\nTraining Random Forest...")

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(
    X_train,
    y_train
)

print("Training Completed")

# ==============================
# Prediction
# ==============================

prediction = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    prediction
)

print("\nAccuracy :", round(accuracy * 100, 2), "%")

print("\nClassification Report\n")

print(
    classification_report(
        y_test,
        prediction
    )
)

# ==============================
# Save Model
# ==============================

joblib.dump(
    model,
    "model.pkl"
)

print("\nModel Saved Successfully")

print("\nGenerated Files")

print("---------------------------")

print("model.pkl")

print("encoders.pkl")

print("target_encoder.pkl")