import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix
import joblib
import torch
import torch.nn as nn
import torch.optim as optim

df = pd.read_csv("data/clean_train.csv")

X_df = df.drop(["binary_label", "label", "difficulty_level"], axis=1)

X_df = X_df.astype("float32")

X = X_df.values
y = df["binary_label"].values

input_size = X.shape[1]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

print("Dataset loaded successfully!")
print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))
print("Number of features:", input_size)
print("\nTraining RandomForest model...")

rf = RandomForestClassifier(n_estimators=150, random_state=42)
rf.fit(X_train, y_train)

joblib.dump(rf, "models/baseline_model.joblib")

y_pred = rf.predict(X_test)

print("\n📊 RandomForest Results:")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall:", recall_score(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

class IDS_MLP(nn.Module):
    def __init__(self, input_dim):
        super(IDS_MLP, self).__init__()
        self.fc1 = nn.Linear(input_dim, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 1)
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.sigmoid(self.fc3(x))
        return x

print("\nTraining PyTorch MLP model...")

model = IDS_MLP(input_size)
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train.reshape(-1,1), dtype=torch.float32)

# Train for 10 epochs
epochs = 10
for epoch in range(epochs):
    optimizer.zero_grad()
    outputs = model(X_train_tensor)
    loss = criterion(outputs, y_train_tensor)
    loss.backward()
    optimizer.step()
    print(f"Epoch {epoch+1}/{epochs} — Loss: {loss.item():.4f}")

# Save neural network model
torch.save(model.state_dict(), "models/ids_model.pt")

print("\n✅ Training complete!")
print("✔ Saved baseline_model.joblib")
print("✔ Saved ids_model.pt")
