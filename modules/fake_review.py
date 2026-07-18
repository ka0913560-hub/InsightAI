import joblib
from modules.preprocessing import preprocess_text

print("✅ fake_review.py loaded")

model = joblib.load("models/fake_review_model.pkl")
vectorizer = joblib.load("models/fake_review_vectorizer.pkl")

def predict_fake_review(review):

    print("✅ predict_fake_review() called")

    cleaned_review = preprocess_text(review)

    review_vector = vectorizer.transform([cleaned_review])

    prediction = model.predict(review_vector)[0]

    print("Prediction:", prediction)
    print("Classes:", model.classes_)
    print("Probability:", model.predict_proba(review_vector)[0])

    return prediction