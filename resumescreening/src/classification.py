import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

# Load dataset
df = pd.read_csv("resumescreening/data/preprocessed_resume_data.csv")
df.fillna("", inplace=True)


# Features and Target
X = df["resume_text"]
y = df["job_position_name"]

# TF-IDF
tfidf = TfidfVectorizer(stop_words="english")
X = tfidf.fit_transform(X)

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Training Data:", X_train.shape)
print("Testing Data:", X_test.shape)