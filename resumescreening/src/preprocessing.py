import pandas as pd
import re

# Load Dataset
df = pd.read_csv("resumescreening/data/resume_data.csv")
df.columns = df.columns.str.replace("\ufeff", "", regex=False)
df.columns = df.columns.str.strip()

# Remove extra spaces from column names
#df.columns = df.columns.str.strip()

# Select useful columns
df = df[[
    "career_objective",
    "skills",
    "degree_names",
    "major_field_of_studies",
    "positions",
    "responsibilities",
    "certification_skills",
    "languages",
    "job_position_name",
    "matched_score",
    "skills_required"
]]

# Handle Missing Values
df.fillna("", inplace=True)

# Remove Duplicate Rows
df.drop_duplicates(inplace=True)

# Merge all resume information
df["resume_text"] = (
    df["career_objective"] + " " +
    df["skills"] + " " +
    df["degree_names"] + " " +
    df["major_field_of_studies"] + " " +
    df["positions"] + " " +
    df["responsibilities"] + " " +
    df["certification_skills"] + " " +
    df["languages"]
)

# Text Cleaning Function
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)       # Remove URLs
    text = re.sub(r"[^a-zA-Z ]", " ", text)   # Remove numbers & symbols
    text = re.sub(r"\s+", " ", text)          # Remove extra spaces
    return text.strip()

# Apply Cleaning
df["resume_text"] = df["resume_text"].apply(clean_text)
df["skills_required"] = df["skills_required"].apply(clean_text)

# Keep final columns
df = df[[
    "resume_text",
    "skills_required",
    "job_position_name",
    "matched_score"
]]

# Save Preprocessed Dataset
df.to_csv("preprocessed_resume_data.csv", index=False)

print("Preprocessing Completed Successfully!")
print(df.head())
print(df.shape)
