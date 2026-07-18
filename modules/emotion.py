import joblib
from modules.preprocessing import preprocess_text

model = joblib.load("models/emotion_model.pkl")
vectorizer = joblib.load("models/emotion_vectorizer.pkl")

def predict_emotion(text):
    text = preprocess_text(text)
    text = vectorizer.transform([text])
    prediction = model.predict(text)[0]
    return prediction