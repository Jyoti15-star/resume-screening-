import pickle

# ==============================
# Load Saved Models
# ==============================

with open("resumescreening/models/tfidf_vectorizer.pkl", "rb") as f:
    tfidf = pickle.load(f)

with open("resumescreening/models/feature_selector.pkl", "rb") as f:
    selector = pickle.load(f)

with open("resumescreening/models/resume_classifier.pkl", "rb") as f:
    model = pickle.load(f)

with open("resumescreening/models/label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

# ==============================
# Input Resume Text
# ==============================

resume = """
Python Developer with 3 years of experience.
Skills: Python, Django, Flask, SQL, Machine Learning,
Pandas, NumPy, Scikit-learn, Git, Linux.
Developed REST APIs and machine learning models.
"""

# ==============================
# TF-IDF Transformation
# ==============================

resume_tfidf = tfidf.transform([resume])

# ==============================
# Feature Selection
# ==============================

resume_selected = selector.transform(resume_tfidf)

# ==============================
# Prediction
# ==============================

prediction = model.predict(resume_selected)

category = label_encoder.inverse_transform(prediction)

print("\n==============================")
print("Predicted Category :", category[0])
print("==============================")