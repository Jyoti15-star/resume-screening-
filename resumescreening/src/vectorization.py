import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
# Load preprocessed dataset
df = pd.read_csv(
    "resumescreening/data/preprocessed_resume_data.csv"
)
df.fillna("", inplace=True)
df["combined_text"] = (
    df["resume_text"] + " " +
    df["skills_required"]
)


# Combine resume and required skills
df["combined_text"] = (
    df["resume_text"] + " " +
    df["skills_required"]
)


# Create TF-IDF vectorizer
tfidf = TfidfVectorizer(
    max_features=5000,
    stop_words="english",
    ngram_range=(1,2)
)
print(df["combined_text"].isnull().sum())
print(df["combined_text"].head())

# Convert text into vectors
X = tfidf.fit_transform(df["combined_text"])


print("Vectorization Completed!")
print("Number of resumes:", X.shape[0])
print("Number of features:", X.shape[1])


# Save vectors
with open(
    "resumescreening/data/tfidf_vectors.pkl",
    "wb"
) as file:
    pickle.dump(X, file)


# Save vectorizer
with open(
    "resumescreening/data/tfidf_vectorizer.pkl",
    "wb"
) as file:
    pickle.dump(tfidf, file)