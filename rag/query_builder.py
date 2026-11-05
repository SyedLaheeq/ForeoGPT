
def build_skin_query(zone, features):
    """
    Build a knowledge-retrieval query from measured image features.

    These measurements are not clinical diagnoses.
    """

    terms = [
        f"{zone} facial skin",
        "skin colour measurements",
        "brightness and redness measurements",
        "gentle skincare guidance",
        "FOREO product specifications and device modes",
    ]

    if features.get("hsv_statistics") is not None:
        terms.append("HSV colour statistics")

    if features.get("color_statistics") is not None:
        terms.append("RGB colour statistics")

    return " ".join(terms)