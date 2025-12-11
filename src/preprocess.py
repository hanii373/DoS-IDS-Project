import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib

# Full column list (43 columns)
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

# DoS attack names
dos_attacks = [
    "back","land","neptune","pod","smurf","teardrop",
    "apache2","udpstorm","processtable","mailbomb"
]

def preprocess():
    print("Loading dataset...")
    df = pd.read_csv("data/KDDTrain+.txt", names=column_names)

    print("Mapping labels (DoS vs Normal)...")
    df["binary_label"] = df["label"].apply(lambda x: 1 if x in dos_attacks else 0)

    print("Encoding categorical columns...")
    df = pd.get_dummies(df, columns=["protocol_type", "service", "flag"])

    print("Scaling numeric columns...")

    # Drop target columns BEFORE scaling
    feature_cols = df.drop(["binary_label", "label", "difficulty_level"], axis=1).columns

    scaler = StandardScaler()
    df[feature_cols] = scaler.fit_transform(df[feature_cols])

    print("Saving clean dataset...")
    df.to_csv("data/clean_train.csv", index=False)
    joblib.dump(scaler, "models/scaler.pkl")

    print("\n✅ Preprocessing complete!")

if __name__ == "__main__":
    preprocess()
