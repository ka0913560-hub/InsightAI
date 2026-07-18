import re
import string
import pandas as pd

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def _ensure_nltk_resource(resource_path, download_name):
    try:
        nltk.data.find(resource_path)
    except LookupError:
        nltk.download(download_name, quiet=True)


# Download only the NLTK resources that are missing (skipped if already present)
_ensure_nltk_resource("corpora/stopwords", "stopwords")
_ensure_nltk_resource("corpora/wordnet", "wordnet")
_ensure_nltk_resource("corpora/omw-1.4", "omw-1.4")

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