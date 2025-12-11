import pandas as pd

path = "data/KDDTrain+.csv"

df = pd.read_csv(path)

print("Dataset loaded successfully!")
print("Shape:", df.shape)
print("Columns:", df.columns)
print("First 5 labels:", df.iloc[:5, -1])
