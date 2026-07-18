import joblib
from modules.preprocessing import preprocess_text

# Load model and vectorizer once
model = joblib.load("models/sentiment_model.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")


def predict_sentiment(review):
    review = preprocess_text(review)
    review = vectorizer.transform([review])
    prediction = model.predict(review)[0]

    return prediction.capitalize()