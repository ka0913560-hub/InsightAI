"""
Bulk Review Analysis helpers.

This module ONLY orchestrates calls to the existing, already-trained
models/functions (sentiment, emotion, fake_review, rating, aspect).
No model is created, retrained, or modified here.
"""

import io
import pandas as pd

from modules.sentiment import predict_sentiment
from modules.emotion import predict_emotion
from modules.fake_review import predict_fake_review
from modules.rating_prediction import predict_rating
from modules.aspect_analysis import predict_aspect


# Candidate column names that may contain the review text.
# Matching is done in a normalized form (lowercase, spaces/underscores/
# hyphens stripped) so variants like "Review Text", "review_text",
# "ReviewText", "Customer Review", etc. are all recognized automatically.
# Ordered roughly by priority (most specific/likely first).
REVIEW_COLUMN_CANDIDATES = [
    "reviewtext", "review", "reviewtitle", "reviewbody", "reviewcontent",
    "reviewmessage", "reviewdescription",
    "customerreview", "customerreviews", "customerfeedback",
    "feedback", "comments", "comment",
    "message", "body", "content", "description", "text",
]


def _normalize_column_name(name):
    """Lowercase and strip spaces/underscores/hyphens for fuzzy column matching."""
    return (
        str(name)
        .strip()
        .lower()
        .replace(" ", "")
        .replace("_", "")
        .replace("-", "")
    )


def _read_csv_robust(raw_bytes):
    """
    Attempt to parse CSV bytes using a sequence of increasingly permissive
    strategies, so real-world/malformed CSV files (Windows/Linux line endings,
    multiline quoted reviews, commas inside quoted text, inconsistent column
    counts, stray delimiters, BOM markers, non-UTF-8 encoding, etc.) don't
    crash the app.

    Order of attempts (fastest/strictest first, most tolerant last):
        1. C engine, UTF-8-SIG (handles BOM; falls back to plain UTF-8 content
           since utf-8-sig also correctly decodes files without a BOM).
        2. C engine, Latin-1 (handles UnicodeDecodeError on non-UTF-8 files).
        3. C engine with automatic delimiter sniffing + bad-line skipping
           (handles semicolon/tab separated exports and malformed rows).
        4. Python engine (slower, far more tolerant of quoting/multiline
           edge cases) with delimiter sniffing + bad-line skipping, tried
           for each encoding above.

    Returns the first DataFrame that parses successfully.
    """
    encodings = ["utf-8-sig", "latin-1"]
    last_error = None

    # 1 & 2: fast C engine, default (comma) delimiter — best performance for
    # well-formed large files. quoting/quotechar defaults already handle
    # commas-inside-quotes and multiline quoted fields correctly.
    for encoding in encodings:
        try:
            return pd.read_csv(io.BytesIO(raw_bytes), encoding=encoding, engine="c")
        except UnicodeDecodeError as exc:
            last_error = exc
            continue
        except Exception as exc:
            # Buffer overflow / tokenizing errors / malformed input -> try next strategy.
            last_error = exc
            continue

    # 3: C engine with auto-detected delimiter and tolerant bad-line handling
    # (covers semicolon/tab-separated files and rows with a wrong field count).
    for encoding in encodings:
        try:
            return pd.read_csv(
                io.BytesIO(raw_bytes),
                encoding=encoding,
                engine="c",
                sep=None,
                on_bad_lines="skip",
            )
        except Exception as exc:
            last_error = exc
            continue

    # 4: Python engine — slower but the most tolerant of malformed/irregular
    # CSVs (mismatched quotes, inconsistent column counts, mixed delimiters).
    for encoding in encodings:
        try:
            return pd.read_csv(
                io.BytesIO(raw_bytes),
                encoding=encoding,
                engine="python",
                sep=None,          # auto-detect delimiter
                on_bad_lines="skip",
            )
        except Exception as exc:
            last_error = exc
            continue

    raise ValueError(
        "Could not parse the CSV file even with a lenient parser. "
        "The file appears to be corrupted or is not a valid delimited text file. "
        f"({last_error})"
    )


def read_uploaded_file(uploaded_file):
    """
    Read an uploaded CSV/XLSX/XLS file into a DataFrame.
    Raises ValueError with a user-friendly message on failure.

    Robust against real-world, malformed CSV files: automatically retries
    with different encodings and, if the fast C parser fails, falls back to
    the more tolerant Python engine (skipping unparsable rows) so a single
    bad row doesn't crash the whole upload.
    """
    if uploaded_file is None:
        raise ValueError("No file was uploaded.")

    name = uploaded_file.name.lower()
    raw_bytes = uploaded_file.getvalue()

    if len(raw_bytes) == 0:
        raise ValueError("The uploaded file is empty.")

    try:
        if name.endswith(".csv"):
            df = _read_csv_robust(raw_bytes)
        elif name.endswith(".xlsx") or name.endswith(".xls"):
            df = pd.read_excel(io.BytesIO(raw_bytes))
        else:
            raise ValueError("Unsupported file type. Please upload a CSV or Excel (.xlsx/.xls) file.")
    except ValueError:
        raise
    except Exception as exc:
        raise ValueError(f"Could not read the file. It may be corrupted or in an invalid format. ({exc})")

    if df is None or df.empty:
        raise ValueError("The uploaded file does not contain any data.")

    # Drop fully-empty rows/columns that can result from skipped/malformed lines.
    df = df.dropna(how="all").dropna(axis=1, how="all")

    if df.empty:
        raise ValueError("The uploaded file does not contain any usable data after cleaning.")

    return df


def detect_review_column(df):
    """
    Return the auto-detected review column name, or None if not confidently found.

    Matching is case-insensitive and ignores spaces, underscores, and hyphens,
    so "Review Text", "review_text", "review-text", "REVIEW TEXT",
    "ReviewText", "Customer Review", "customer_review", etc. are all
    recognized as the same candidate.
    """
    print("[BulkAnalysis] Detected dataframe columns:", list(df.columns))

    normalized_map = {_normalize_column_name(c): c for c in df.columns}

    detected = None
    for candidate in REVIEW_COLUMN_CANDIDATES:
        if candidate in normalized_map:
            detected = normalized_map[candidate]
            break

    print("[BulkAnalysis] Detected review column:", detected)
    return detected


def get_text_like_columns(df):
    """
    Return all columns that look like they could contain free text, for use
    when auto-detection fails or is ambiguous.

    A column is considered "text-like" if it has object/string dtype AND at
    least one non-null value is an actual string (not e.g. a stray float/NaN
    column that pandas happened to type as object). This is intentionally
    permissive so real-world columns like "Review Text", "Review Title",
    "Reviewer Name", etc. are never silently excluded.
    """
    text_cols = []

    for c in df.columns:
        series = df[c]

        is_object_or_string = (
            series.dtype == object or pd.api.types.is_string_dtype(series)
        )
        if not is_object_or_string:
            continue

        # At least one real (non-empty) string value must be present.
        sample = series.dropna().astype(str).str.strip()
        if (sample != "").any():
            text_cols.append(c)

    print("[BulkAnalysis] Text-like columns:", text_cols)
    return text_cols


def analyze_reviews_bulk(df, review_column, progress_callback=None, batch_size=25):
    """
    Run all existing (unmodified) models on every review in df[review_column].

    progress_callback: optional callable(done, total) invoked after each batch.

    Returns a new DataFrame with columns:
        Review, Sentiment, Emotion, Authenticity, Rating, Detected Aspects
    Rows with empty/NaN reviews are skipped (not sent to the models).
    """
    reviews = df[review_column].astype(str)

    valid_mask = df[review_column].notna() & (reviews.str.strip() != "") & (reviews.str.lower() != "nan")
    valid_indices = df.index[valid_mask].tolist()
    total = len(valid_indices)

    results = []
    processed = 0

    for start in range(0, total, batch_size):
        batch_indices = valid_indices[start:start + batch_size]

        for idx in batch_indices:
            review_text = str(df.at[idx, review_column]).strip()

            try:
                sentiment = predict_sentiment(review_text)
            except Exception:
                sentiment = "Unknown"

            try:
                emotion = predict_emotion(review_text)
            except Exception:
                emotion = "Unknown"

            try:
                authenticity = predict_fake_review(review_text)
            except Exception:
                authenticity = "Unknown"

            try:
                rating = predict_rating(review_text)
            except Exception:
                rating = None

            try:
                aspects = predict_aspect(review_text)
                aspects_str = ", ".join(f"{name} ({status})" for name, status in aspects) if aspects else ""
            except Exception:
                aspects_str = ""

            results.append({
                "Review": review_text,
                "Sentiment": sentiment,
                "Emotion": emotion,
                "Authenticity": authenticity,
                "Rating": rating,
                "Detected Aspects": aspects_str,
            })

        processed += len(batch_indices)
        if progress_callback:
            progress_callback(processed, total)

    return pd.DataFrame(results, columns=[
        "Review", "Sentiment", "Emotion", "Authenticity", "Rating", "Detected Aspects"
    ])


def build_summary_dashboard(results_df):
    """
    Compute summary/business-dashboard statistics from the processed results.
    Returns a dict of metrics.
    """
    total_reviews = len(results_df)

    if total_reviews == 0:
        return {
            "total_reviews": 0,
            "positive_reviews": 0,
            "negative_reviews": 0,
            "positive_pct": 0.0,
            "negative_pct": 0.0,
            "average_rating": 0.0,
            "fake_pct": 0.0,
            "genuine_pct": 0.0,
            "most_common_emotion": "N/A",
            "most_mentioned_aspect": "N/A",
            "top_positive_aspect": "N/A",
            "top_negative_aspect": "N/A",
        }

    sentiment_counts = results_df["Sentiment"].value_counts()
    positive_reviews = int(sentiment_counts.get("Positive", 0))
    negative_reviews = int(sentiment_counts.get("Negative", 0))

    ratings = pd.to_numeric(results_df["Rating"], errors="coerce").dropna()
    average_rating = round(float(ratings.mean()), 2) if not ratings.empty else 0.0

    auth_counts = results_df["Authenticity"].value_counts()
    fake_count = int(auth_counts.get("Fake", 0))
    genuine_count = int(auth_counts.get("Genuine", 0))
    auth_total = fake_count + genuine_count

    emotion_counts = results_df["Emotion"].value_counts()
    most_common_emotion = emotion_counts.idxmax() if not emotion_counts.empty else "N/A"

    aspect_pos_counts = {}
    aspect_neg_counts = {}
    aspect_total_counts = {}

    for aspects_str in results_df["Detected Aspects"]:
        if not aspects_str:
            continue
        for item in aspects_str.split(", "):
            if "(" not in item:
                continue
            name, status = item.rsplit(" (", 1)
            status = status.rstrip(")")
            aspect_total_counts[name] = aspect_total_counts.get(name, 0) + 1
            if status.lower() == "positive":
                aspect_pos_counts[name] = aspect_pos_counts.get(name, 0) + 1
            elif status.lower() == "negative":
                aspect_neg_counts[name] = aspect_neg_counts.get(name, 0) + 1

    most_mentioned_aspect = max(aspect_total_counts, key=aspect_total_counts.get) if aspect_total_counts else "N/A"
    top_positive_aspect = max(aspect_pos_counts, key=aspect_pos_counts.get) if aspect_pos_counts else "N/A"
    top_negative_aspect = max(aspect_neg_counts, key=aspect_neg_counts.get) if aspect_neg_counts else "N/A"

    return {
        "total_reviews": total_reviews,
        "positive_reviews": positive_reviews,
        "negative_reviews": negative_reviews,
        "positive_pct": round(positive_reviews / total_reviews * 100, 1),
        "negative_pct": round(negative_reviews / total_reviews * 100, 1),
        "average_rating": average_rating,
        "fake_pct": round(fake_count / auth_total * 100, 1) if auth_total else 0.0,
        "genuine_pct": round(genuine_count / auth_total * 100, 1) if auth_total else 0.0,
        "most_common_emotion": most_common_emotion,
        "most_mentioned_aspect": most_mentioned_aspect,
        "top_positive_aspect": top_positive_aspect,
        "top_negative_aspect": top_negative_aspect,
        "aspect_total_counts": aspect_total_counts,
    }


def to_csv_bytes(df):
    return df.to_csv(index=False).encode("utf-8")


def to_excel_bytes(df):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Bulk Analysis")
    return buffer.getvalue()
