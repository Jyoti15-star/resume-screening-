import pandas as pd
import matplotlib.pyplot as plt

# Load Dataset
df = pd.read_csv("resumescreening/data/resume_data.csv")

# Remove BOM and extra spaces
df.columns = df.columns.str.replace("\ufeff", "", regex=False)
df.columns = df.columns.str.strip()

# 1. Dataset Overview
print("Shape:", df.shape)
print("\nColumns:")
print(df.columns)

print("\nInfo:")
df.info()

print("\nFirst 5 Rows:")
print(df.head())

print("\nStatistical Summary:")
print(df.describe())

# 2. Missing Values
print("\nMissing Values:")
print(df.isnull().sum())

plt.figure(figsize=(12,5))
df.isnull().sum().plot(kind="bar")
plt.title("Missing Values")
plt.xticks(rotation=90)
plt.show()

# 3. Duplicate Values
print("\nDuplicate Rows:")
print(df.duplicated().sum())

# 4. Target Variable Analysis
print("\nJob Position Count:")
print(df["job_position_name"].value_counts())

plt.figure(figsize=(12,5))
df["job_position_name"].value_counts().head(10).plot(kind="bar")
plt.title("Top 10 Job Roles")
plt.xticks(rotation=45)
plt.show()

# 5. Matched Score Analysis
print("\nMatched Score Summary:")
print(df["matched_score"].describe())

plt.figure(figsize=(6,4))
plt.hist(df["matched_score"], bins=20)
plt.title("Matched Score Distribution")
plt.show()

plt.figure(figsize=(5,4))
plt.boxplot(df["matched_score"].dropna())
plt.title("Matched Score Boxplot")
plt.show()

# 6. Unique Job Roles
print("\nUnique Job Roles:")
print(df["job_position_name"].nunique())

# 7. Correlation
print("\nCorrelation:")
print(df.corr(numeric_only=True))

# 8. Skewness
print("\nSkewness:")
print(df.skew(numeric_only=True))

# 9. Class Distribution
print("\nClass Percentage:")
print(df["job_position_name"].value_counts(normalize=True) * 100)
print("EDA successful")