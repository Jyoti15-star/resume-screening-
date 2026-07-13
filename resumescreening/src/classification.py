import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score, classification_report

# ==============================
# Load Cleaned Dataset
# ==============================

df = pd.read_csv("resumescreening/data/cleaned_train.csv")

# ==============================
# Features and Target
# ==============================

X = df["Cleaned_Text"]
y = df["Category"]

# ==============================
# Label Encoding
# ==============================

label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

with open("resumescreening/models/label_encoder.pkl", "wb") as file:
    pickle.dump(label_encoder, file)

# ==============================
# TF-IDF Vectorization
# ==============================

tfidf = TfidfVectorizer(stop_words="english")

X = tfidf.fit_transform(X)

with open("resumescreening/models/tfidf_vectorizer.pkl", "wb") as file:
    pickle.dump(tfidf, file)

# ==============================
# Train-Test Split
# ==============================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ==============================
# Machine Learning Models
# ==============================

models = {

    "Logistic Regression": LogisticRegression(max_iter=1000),

    "Naive Bayes": MultinomialNB(),

    "Linear SVM": LinearSVC(),

    "Random Forest": RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

}

best_accuracy = 0
best_model = None
best_model_name = ""

# ==============================
# Training & Evaluation
# ==============================

for name, model in models.items():

    print("\n===================================")
    print("Training :", name)

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)

    print("Accuracy :", round(accuracy * 100, 2), "%")

    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_model = model
        best_model_name = name

# ==============================
# Save Best Model
# ==============================

with open("resumescreening/models/resume_classifier.pkl", "wb") as file:
    pickle.dump(best_model, file)

print("\n===================================")
print("Best Model :", best_model_name)
print("Best Accuracy :", round(best_accuracy * 100, 2), "%")

# ==============================
# Classification Report
# ==============================

y_pred = best_model.predict(X_test)

print("\nClassification Report\n")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=label_encoder.classes_
    )
)