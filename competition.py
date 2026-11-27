
"""
Merch Trend Hunter
Competition analysis for Amazon USA Merch keywords.

This is a heuristic indicator, not verified sales or competition data.
Amazon result counts can be approximate and fluctuate.
"""

from urllib.parse import quote_plus


def _normalize(value, threshold):
    """Convert a non-negative value to a 0-100 scale."""
    if value is None:
        return None

    value = max(0, float(value))
    return min(100, (value / threshold) * 100)


def calculate_competition_score(
    result_count=None,
    exact_match_count=None,
    average_reviews=None,
):
    """
    Estimate competition from manually observed Amazon indicators.

    Higher score = potentially more competition.

    All inputs are optional. Missing inputs are excluded and
    the remaining weights are recalculated.
    """

    indicators = [
        (_normalize(result_count, 10000), 0.40),
        (_normalize(exact_match_count, 5000), 0.35),
        (_normalize(average_reviews, 1000), 0.25),
    ]

    available = [
        (score, weight)
        for score, weight in indicators
        if score is not None
    ]

    if not available:
        return None

    total_weight = sum(weight for _, weight in available)

    score = sum(
        value * weight
        for value, weight in available
    ) / total_weight

    return round(score, 1)


def get_competition_level(score):
    """Return a readable competition category."""

    if score is None:
        return "Unknown"

    if score < 30:
        return "Low"

    if score < 60:
        return "Medium"

    if score < 80:
        return "High"

    return "Very High"


def build_amazon_shirt_url(keyword):
    """
    Build an Amazon USA search URL focused on the Fashion category.
    """

    query = quote_plus(f"{keyword} shirt")

    return (
        f"https://www.amazon.com/s?k={query}"
        "&i=fashion"
    )


def analyze_competition(
    keyword,
    result_count=None,
    exact_match_count=None,
    average_reviews=None,
):
    """Return a complete competition analysis."""

    score = calculate_competition_score(
        result_count=result_count,
        exact_match_count=exact_match_count,
        average_reviews=average_reviews,
    )

    return {
        "keyword": keyword,
        "competition_score": score,
        "competition_level": get_competition_level(score),
        "amazon_url": build_amazon_shirt_url(keyword),
        "method": "Heuristic estimate from supplied indicators",
        "warning": (
            "Not verified sales data. Amazon result counts "
            "are approximate and should not be treated as "
            "the exact number of competing Merch listings."
        ),
    }


if __name__ == "__main__":
    result = analyze_competition(
        keyword="funny dachshund shirt",
        result_count=2500,
        exact_match_count=800,
        average_reviews=120,
    )

    for key, value in result.items():
        print(f"{key}: {value}")

def filter_low_result_keywords(keywords):
    """
    Keep only keywords with Amazon result counts
    from 0 to 99.
    Missing or invalid counts are excluded.
    """
    filtered = []

    for item in keywords:
        try:
            count = int(item.get("result_count"))
        except (TypeError, ValueError):
            continue

        if 0 <= count <= 99:
            filtered.append(item)

    return filtered
