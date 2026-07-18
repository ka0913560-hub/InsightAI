import re
import string
import pandas as pd

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Initialize
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))


def remove_html(text):
    return re.sub(r"<.*?>", "", str(text))


def remove_urls(text):
    return re.sub(r"http\S+|www\S+", "", text)


def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))


def remove_numbers(text):
    return re.sub(r"\d+", "", text)


def remove_stopwords(text):
    words = text.split()
    words = [word for word in words if word not in stop_words]
    return " ".join(words)


def lemmatize(text):
    words = text.split()
    words = [lemmatizer.lemmatize(word) for word in words]
    return " ".join(words)


def preprocess_text(text):
    text = str(text).lower()

    text = remove_html(text)
    text = remove_urls(text)
    text = remove_punctuation(text)
    text = remove_numbers(text)

    text = remove_stopwords(text)
    text = lemmatize(text)

    text = re.sub(r"\s+", " ", text).strip()

    return text