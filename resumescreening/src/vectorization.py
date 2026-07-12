import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

# Load preprocessed dataset
df = pd.read_csv("resumescreening/data/preprocessed_resume_data.csv")
df.fillna("", inplace=True)

# Input feature
X = df["resume_text"]

# Target
y = df["job_position_name"]

# TF-IDF
tfidf = TfidfVectorizer(
    max_features=5000,
    stop_words="english",
    ngram_range=(1,2)
)

X_tfidf = tfidf.fit_transform(X)

print("Vectorization Completed!")
print("Number of resumes:", X_tfidf.shape[0])
print("Number of features:", X_tfidf.shape[1])

# Save TF-IDF Vectorizer
with open("resumescreening/data/tfidf_vectorizer.pkl", "wb") as file:
    pickle.dump(tfidf, file)