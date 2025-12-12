import pandas as pd
import numpy as np

columns = [line.strip() for line in open("data/field_names.txt").readlines()]
columns.append("label") 

train_df = pd.read_csv("data/KDDTrain+.txt", names=columns)
test_df = pd.read_csv("data/KDDTest+.txt", names=columns)

print("Datasets loaded!")
print("Train shape:", train_df.shape)
print("Test shape:", test_df.shape)

dos_numbers = [0, 1, 2, 3, 4, 5]

def label_to_binary(label):
    if label in dos_numbers:
        return 1   # DoS attack
    else:
        return 0   # Normal or non-DoS attack

train_df["binary_label"] = train_df["label"].apply(label_to_binary)
test_df["binary_label"] = test_df["label"].apply(label_to_binary)

print("DoS labeling done!")
print(train_df["binary_label"].value_counts())

train_df.to_csv("data/clean_train.csv", index=False)
test_df.to_csv("data/clean_test.csv", index=False)

print("Saved clean_train.csv and clean_test.csv!")
print("Script is running!")
