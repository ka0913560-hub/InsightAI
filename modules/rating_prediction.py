import joblib
from modules.preprocessing import preprocess_text

model = joblib.load("models/rating_model.pkl")
vectorizer = joblib.load("models/rating_vectorizer.pkl")

def predict_rating(review):

    cleaned_review = preprocess_text(review)

    review_vector = vectorizer.transform([cleaned_review])

    prediction = model.predict(review_vector)[0]

    return int(prediction)
    rating = max(1, min(5, rating))

    return rating