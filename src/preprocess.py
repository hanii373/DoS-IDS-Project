import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib

column_names = [
    "duration","protocol_type","service","flag","src_bytes","dst_bytes",
    "land","wrong_fragment","urgent","hot","num_failed_logins",
    "logged_in","num_compromised","root_shell","su_attempted","num_root",
    "num_file_creations","num_shells","num_access_files","num_outbound_cmds",
    "is_host_login","is_guest_login","count","srv_count","serror_rate",
    "srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate",
    "diff_srv_rate","srv_diff_host_rate","dst_host_count","dst_host_srv_count",
    "dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate",
    "dst_host_rerror_rate","dst_host_srv_rerror_rate",
    "label","difficulty_level"
]

dos_attacks = [
    "back","land","neptune","pod","smurf","teardrop",
    "apache2","udpstorm","processtable","mailbomb"
]

def preprocess():
    print("📥 Loading dataset...")
    df = pd.read_csv("data/KDDTrain+.txt", names=column_names)

    print("🔄 Mapping labels into {0=Normal, 1=DoS}...")
    df["binary_label"] = df["label"].apply(lambda x: 1 if x in dos_attacks else 0)

    print("🔠 Encoding categorical columns (one-hot)...")
    df = pd.get_dummies(df, columns=["protocol_type", "service", "flag"])

    print("📏 Scaling numeric columns...")
    feature_cols = df.drop(["binary_label", "label", "difficulty_level"], axis=1).columns

    scaler = StandardScaler()
    df[feature_cols] = scaler.fit_transform(df[feature_cols])

    print("💾 Saving processed dataset & scaler...")
    df.to_csv("data/clean_train.csv", index=False)
    joblib.dump(scaler, "models/scaler.pkl")

    print("\n✅ Preprocessing complete!")

try:
    scaler = joblib.load("models/scaler.pkl")
    print("Scaler loaded for runtime preprocessing.")
except:
    scaler = None
    print("⚠ WARNING: Could not load scaler.pkl — realtime packets won't be scaled!")


def preprocess_features(features: dict):
    """
    Convert ONE packet dict into the exact format used during training.
    Ensures:
      - Missing one-hot columns are added
      - Column order matches scaler.feature_names_in_
      - Scaler is applied
    """
    if scaler is None:
        raise RuntimeError("scaler.pkl not loaded — cannot preprocess input packet!")

    df = pd.DataFrame([features])

    required_cols = scaler.feature_names_in_

    for col in required_cols:
        if col not in df.columns:
            df[col] = 0

    df = df[required_cols]

    df_scaled = scaler.transform(df)
    df_scaled = pd.DataFrame(df_scaled, columns=required_cols)

    return df_scaled

if __name__ == "__main__":
    preprocess()
