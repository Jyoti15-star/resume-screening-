import pandas as pd

# Load the dataset
df = pd.read_csv("resumescreening/data/resume_data.csv")


# 1. Display first 5 rows
# Purpose: Dataset ka starting data dekhne ke liye

print("FIRST 5 ROWS")
print(df.head())


# 2. Display last 5 rows
# Purpose: Dataset ka ending data dekhne ke liye

print("\nLAST 5 ROWS")
print(df.tail())


# 3. Display shape
# Purpose: Total rows aur columns dekhne ke liye

print("\nSHAPE OF DATASET")
print(df.shape)


# 4. Display column names
# Purpose: Dataset me kaun-kaun se columns hain

print("\nCOLUMN NAMES")
print(df.columns)


# 5. Dataset information
# Purpose: Data types, non-null values aur memory usage

print("\nDATASET INFO")
print(df.info())


# 6. Check missing values
# Purpose: Kis column me kitna missing data hai

print("\nMISSING VALUES")
print(df.isnull().sum())


# 7. Check duplicate rows
# Purpose: Duplicate resumes hain ya nahi

print("\nDUPLICATE ROWS")
print(df.duplicated().sum())


# 8. Statistical summary (Text Columns)
# Purpose: Object (text) columns ki summary

print("\nTEXT COLUMN SUMMARY")
print(df.describe(include="object"))


# 9. Unique Categories
# Purpose: Kitni different job categories hain

print("\nUNIQUE CATEGORIES")
print(df["Category"].unique())


# 10. Count of each Category
# Purpose: Har category me kitne resumes hain

print("\nCATEGORY COUNT")
print(df["Category"].value_counts())


# 11. Display one sample resume
# Purpose: Resume ka actual format dekhna

print("\nSAMPLE RESUME")
print(df["Resume"][0])

