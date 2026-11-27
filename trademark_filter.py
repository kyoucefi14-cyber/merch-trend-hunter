
"""
Merch Trend Hunter
Trademark warning filter.

IMPORTANT:
This is a preliminary keyword warning tool.
It is NOT a legal trademark search or clearance.
"""

import re
from pathlib import Path


# Starter list only. Expand this list with verified records.
# Do not assume that words absent from this list are safe.
DEFAULT_TRADEMARK_TERMS = [
    "disney",
    "mickey mouse",
    "minnie mouse",
    "marvel",
    "spiderman",
    "spider-man",
    "star wars",
    "harry potter",
    "pokemon",
    "pokémon",
    "nintendo",
    "lego",
    "barbie",
    "hello kitty",
    "minecraft",
    "fortnite",
    "nike",
    "adidas",
    "coca cola",
    "pepsi",
]


def normalize_text(text):
    """Normalize text for basic phrase matching."""
    return " ".join(str(text).lower().split())


def find_trademark_warnings(
    keyword,
    trademark_terms=None,
):
    """
    Find phrases from the supplied warning list.

    Returns matching terms. This is only a preliminary warning.
    """

    if trademark_terms is None:
        trademark_terms = DEFAULT_TRADEMARK_TERMS

    normalized_keyword = normalize_text(keyword)
    matches = []

    for term in trademark_terms:
        normalized_term = normalize_text(term)

        if not normalized_term:
            continue

        pattern = (
            r"(?<!\w)"
            + re.escape(normalized_term)
            + r"(?!\w)"
        )

        if re.search(pattern, normalized_keyword):
            matches.append(term)

    return sorted(set(matches), key=str.lower)


def check_trademark(keyword, trademark_terms=None):
    """
    Check one keyword and return a structured result.
    """

    matches = find_trademark_warnings(
        keyword,
        trademark_terms,
    )

    if matches:
        status = "WARNING"
        message = (
            "Potential trademark term detected. "
            "Review carefully before using this keyword."
        )
    else:
        status = "NO_MATCH"
        message = (
            "No match found in the local warning list. "
            "This does NOT mean the keyword is legally safe."
        )

    return {
        "keyword": keyword,
        "trademark_status": status,
        "matched_terms": matches,
        "message": message,
    }


def check_keywords(keywords, trademark_terms=None):
    """
    Check multiple keywords.

    Accepts a list of strings or keyword dictionaries.
    """

    results = []

    for item in keywords:
        if isinstance(item, dict):
            keyword = item.get("keyword", "")
        else:
            keyword = str(item)

        if not keyword.strip():
            continue

        results.append(
            check_trademark(keyword, trademark_terms)
        )

    return results


if __name__ == "__main__":
    examples = [
        "Funny Dachshund Dog Shirt",
        "Mickey Mouse Christmas Shirt",
        "Vintage Coffee Lover Shirt",
        "Pokemon Trainer Shirt",
    ]

    for result in check_keywords(examples):
        print("-" * 50)
        print("Keyword:", result["keyword"])
        print("Status:", result["trademark_status"])
        print("Matches:", result["matched_terms"])
        print("Message:", result["message"])
