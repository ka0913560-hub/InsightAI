from modules.sentiment import predict_sentiment

ASPECT_KEYWORDS = {
    "Quality": [
        "quality", "durable", "build", "material", "finish"
    ],

    "Delivery": [
        "delivery", "shipping", "courier", "arrived"
    ],

    "Packaging": [
        "package", "packaging", "box", "seal"
    ],

    "Price": [
        "price", "cost", "expensive", "cheap", "value"
    ],

    "Customer Service": [
        "support", "service", "customer", "refund", "replacement"
    ],

    "Battery": [
        "battery", "charging", "charger", "charge", "power"
    ],

    "Performance": [
        "performance", "speed", "lag"
    ]
}


POSITIVE_WORDS = [
    "good",
    "great",
    "excellent",
    "amazing",
    "awesome",
    "perfect",
    "fast",
    "smooth",
    "love",
    "best",
    "durable",
    "recommended",
    "satisfied",
    "worth",
    "works",
    "working",
    "long-lasting",
    "powerful",
    "stable"
]


NEGATIVE_WORDS = [
    "bad",
    "poor",
    "late",
    "damaged",
    "broken",
    "slow",
    "worst",
    "refund",
    "problem",
    "issue",
    "delay",
    "terrible",
    "disappointed",
    "drain",
    "drains",
    "draining",
    "dead",
    "dies",
    "stopped",
    "stopped working",
    "useless",
    "defective",
    "failed",
    "failure",
    "not working",
    "cracked",
    "faulty"
]


def predict_aspect(review):

    review_lower = review.lower()

    results = []

    for aspect, keywords in ASPECT_KEYWORDS.items():

        for keyword in keywords:

            if keyword in review_lower:

                index = review_lower.find(keyword)

                start = max(0, index - 40)
                end = min(len(review_lower), index + 40)

                context = review_lower[start:end]

                status = None

                # Negative words get highest priority
                for word in NEGATIVE_WORDS:
                    if word in context:
                        status = "Negative"
                        break

                # Positive words checked only if no negative found
                if status is None:
                    for word in POSITIVE_WORDS:
                        if word in context:
                            status = "Positive"
                            break

                # Fallback to overall sentiment
                if status is None:
                    status = predict_sentiment(review)

                results.append((aspect, status))
                break

    if not results:
        results.append(("General", predict_sentiment(review)))

    return results