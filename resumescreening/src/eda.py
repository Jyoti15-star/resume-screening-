import pandas as pd
import matplotlib.pyplot as plt

# Load Dataset
df = pd.read_csv("resumescreening/data/train.csv")

# ---------------------------
# Basic Information
# ---------------------------

print("Shape of Dataset:")
print(df.shape)

print("\nColumns:")
print(df.columns)

print("\nData Types:")
print(df.dtypes)

print("\nFirst 5 Rows:")
print(df.head())

print("\nLast 5 Rows:")
print(df.tail())

# ---------------------------
# Missing Values
# ---------------------------

print("\nMissing Values:")
print(df.isnull().sum())

# ---------------------------
# Duplicate Values
# ---------------------------

print("\nDuplicate Rows:")
print(df.duplicated().sum())

# ---------------------------
# Category Distribution
# ---------------------------

print("\nCategory Counts:")
print(df["Category"].value_counts())

# ---------------------------
# Resume Length
# ---------------------------

df["Resume_Length"] = df["Text"].apply(len)

print("\nResume Length Statistics:")
print(df["Resume_Length"].describe())

# ---------------------------
# Sample Resume
# ---------------------------

print("\nSample Resume:")
print(df["Text"].iloc[0])

print("\nSample Category:")
print(df["Category"].iloc[0])

# ---------------------------
# Category Distribution Graph
# ---------------------------

plt.figure(figsize=(12,6))
df["Category"].value_counts().plot(kind="bar")

plt.title("Resume Category Distribution")
plt.xlabel("Job Role")
plt.ylabel("Number of Resumes")

plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# ---------------------------
# Resume Length Distribution
# ---------------------------

plt.figure(figsize=(8,5))
plt.hist(df["Resume_Length"], bins=30)

plt.title("Resume Length Distribution")
plt.xlabel("Resume Length")
plt.ylabel("Frequency")

plt.tight_layout()
plt.show()