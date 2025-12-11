import pandas as pd

columns = [line.strip() for line in open("data/field_names.txt").readlines()]
columns.append("label")

df = pd.read_csv("data/KDDTrain+.txt", names=columns)

print("Unique labels in dataset:")
print(df["label"].unique())
print("\nNumber of unique labels:", len(df["label"].unique()))
