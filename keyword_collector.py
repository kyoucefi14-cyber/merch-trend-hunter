
"""
Merch Trend Hunter
Amazon USA keyword suggestion collector.

Note:
Amazon autocomplete suggestions are not verified search-volume,
sales, or competition data.
"""

import json
import time
from datetime import datetime, timezone
from urllib.parse import urlencode
from urllib.request import Request, urlopen


AMAZON_AUTOCOMPLETE_URL = (
    "https://completion.amazon.com/api/2017/suggestions"
)

DEFAULT_SEEDS = [
    "funny shirt",
    "dog shirt",
    "cat shirt",
    "christmas shirt",
    "teacher shirt",
    "bbq shirt",
    "vintage shirt",
    "halloween shirt",
    "coffee shirt",
    "fishing shirt",
    "hunting shirt",
    "camping shirt",
    "bigfoot shirt",
    "mama shirt",
    "dad shirt",
    "retro shirt",
    "birthday shirt",
    "gym shirt",
    "garden shirt",
    "book lover shirt",
]


NICHE_KEYWORDS = {
    "Funny": ["funny", "humor", "joke", "sarcastic", "meme"],
    "Dogs": ["dog", "puppy", "dachshund", "golden retriever", "bulldog"],
    "Cats": ["cat", "kitten", "kitty"],
    "Christmas": ["christmas", "santa", "xmas", "holiday"],
    "Teachers": ["teacher", "teaching", "school", "education"],
    "BBQ": ["bbq", "grill", "barbecue", "smoke", "grilling"],
    "Halloween": ["halloween", "spooky", "ghost", "witch"],
    "Outdoor": ["fishing", "hunting", "camping", "hiking"],
    "Coffee": ["coffee", "espresso", "caffeine"],
    "Fitness": ["gym", "fitness", "workout", "lifting"],
    "Vintage": ["vintage", "retro", "80s", "90s"],
    "Books": ["book", "reading", "reader", "book lover"],
}


def classify_niche(keyword):
    """Assign a basic niche label to a keyword."""

    text = keyword.lower()

    for niche, terms in NICHE_KEYWORDS.items():
        if any(term in text for term in terms):
            return niche

    return "General"


def get_amazon_suggestions(keyword, limit=10, timeout=15):
    """
    Retrieve autocomplete suggestions from Amazon USA.

    Returns a list of suggested keyword strings.
    """

    params = {
        "limit": str(limit),
        "prefix": keyword,
        "suggestion-type": "KEYWORD",
        "page-type": "Search",
        "lop": "en_US",
        "site-variant": "desktop",
        "client-info": "amazon-search-ui",
        "mid": "ATVPDKIKX0DER",
        "alias": "aps",
    }

    url = AMAZON_AUTOCOMPLETE_URL + "?" + urlencode(params)

    request = Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
            ),
            "Accept": "application/json",
        },
    )

    try:
        with urlopen(request, timeout=timeout) as response:
            data = json.loads(response.read().decode("utf-8"))

        suggestions = data.get("suggestions", [])

        results = []

        for item in suggestions:
            if isinstance(item, dict):
                value = item.get("value", "")
            else:
                value = str(item)

            value = value.strip()

            if value:
                results.append(value)

        return results

    except Exception as error:
        print(f"Could not collect '{keyword}': {error}")
        return []


def collect_keywords(
    seed_keywords=None,
    limit_per_seed=10,
    delay_seconds=0.5,
):
    """
    Collect Amazon USA autocomplete suggestions.

    Returns a list of dictionaries.
    """

    if seed_keywords is None:
        seed_keywords = DEFAULT_SEEDS

    collected = {}
    total = len(seed_keywords)

    for index, seed in enumerate(seed_keywords, start=1):
        print(f"[{index}/{total}] Searching: {seed}")

        suggestions = get_amazon_suggestions(
            keyword=seed,
            limit=limit_per_seed,
        )

        # Include the original seed.
        all_keywords = [seed] + suggestions

        for keyword in all_keywords:
            clean_keyword = " ".join(keyword.split())

            if not clean_keyword:
                continue

            key = clean_keyword.lower()

            if key not in collected:
                collected[key] = {
                    "keyword": clean_keyword,
                    "niche": classify_niche(clean_keyword),
                    "source": "Amazon Autocomplete",
                    "market": "US",
                    "collected_at_utc": datetime.now(
                        timezone.utc
                    ).isoformat(),
                }

        time.sleep(max(0, delay_seconds))

    return list(collected.values())


if __name__ == "__main__":
    keywords = collect_keywords()

    print(f"\nCollected {len(keywords)} unique keywords.")

    for item in keywords[:20]:
        print(
            f"{item['keyword']} "
            f"| Niche: {item['niche']}"
        )
