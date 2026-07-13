import pandas as pd
import re
import nltk

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download NLTK resources (first time only)
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("omw-1.4")

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv("resumescreening/data/train.csv")

# -----------------------------
# Remove Missing Values
# -----------------------------
print("Missing Values Before:")
print(df.isnull().sum())

df.dropna(inplace=True)

print("\nMissing Values After:")
print(df.isnull().sum())

# -----------------------------
# Remove Duplicate Rows
# -----------------------------
print("\nDuplicate Rows Before:", df.duplicated().sum())

df.drop_duplicates(inplace=True)

print("Duplicate Rows After:", df.duplicated().sum())

# Reset Index
df.reset_index(drop=True, inplace=True)

# -----------------------------
# Stopwords & Lemmatizer
# -----------------------------
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

# -----------------------------
# Resume Cleaning Function
# -----------------------------
def clean_resume(text):

    # Convert to lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r'http\S+|www\S+', ' ', text)

    # Remove Emails
    text = re.sub(r'\S+@\S+', ' ', text)

    # Remove Phone Numbers
    text = re.sub(r'\+?\d[\d\s()-]{8,}\d', ' ', text)

    # Remove Numbers
    #text = re.sub(r'\d+', ' ', text)

    # Remove Special Characters
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)

    # Remove Extra Spaces
    text = re.sub(r'\s+', ' ', text).strip()

    # Tokenization
    words = text.split()

    # Remove Stopwords
    words = [word for word in words if word not in stop_words]

    # Lemmatization
    words = [lemmatizer.lemmatize(word) for word in words]

    # Join words
    return " ".join(words)

# -----------------------------
# Apply Cleaning
# -----------------------------
df["Cleaned_Text"] = df["Text"].apply(clean_resume)

# -----------------------------
# Show Sample
# -----------------------------
print("\nOriginal Resume:\n")
print(df["Text"].iloc[0][:1000])

print("\nCleaned Resume:\n")
print(df["Cleaned_Text"].iloc[0][:1000])

# -----------------------------
# Save Cleaned Dataset
# -----------------------------
df.to_csv("resumescreening/data/cleaned_train.csv", index=False)

print("\nCleaned dataset saved as data/cleaned_train.csv")
print("Final Dataset Shape:", df.shape)