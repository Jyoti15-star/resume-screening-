import pickle

from resume_parser import extract_text

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
# Predict Role Function
# ==============================

def predict_role(text):

    text_tfidf = tfidf.transform([text])

    text_selected = selector.transform(text_tfidf)

    prediction = model.predict(text_selected)

    category = label_encoder.inverse_transform(prediction)

    return category[0]


# ==============================
# Testing
# ==============================

if __name__ == "__main__":

    resume_path = input("Enter Resume PDF Path: ")

    # PDF se text nikalo
    resume_text = extract_text(resume_path)

    # Role predict karo
    role = predict_role(resume_text)

    print("\n==============================")
    print("Predicted Category :", role)
    print("==============================")