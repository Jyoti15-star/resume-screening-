import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer

# Load Cleaned Dataset
df = pd.read_csv("resumescreening/data/cleaned_train.csv")

# Input Feature
X = df["Cleaned_Text"]

# TF-IDF Vectorizer
tfidf = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1,2)
)

# Convert Text into Numerical Features
X_tfidf = tfidf.fit_transform(X)

# Print Information
print("TF-IDF Matrix Shape:")
print(X_tfidf.shape)

print("\nNumber of Features:")
print(len(tfidf.get_feature_names_out()))

print("\nFirst 20 Features:")
print(tfidf.get_feature_names_out()[:20])

# Save TF-IDF Vectorizer
with open("resumescreening/models/tfidf_vectorizer.pkl", "wb") as file:
    pickle.dump(tfidf, file)

print("\nTF-IDF Vectorizer Saved Successfully!")