
"""
Merch Trend Hunter
Export keyword research results to CSV.
"""

import csv
import io
from datetime import datetime, timezone


CSV_COLUMNS = [
    "keyword",
    "niche",
    "demand_score",
    "competition_score",
    "competition_level",
    "trend_score",
    "buyer_intent_score",
    "design_score",
    "opportunity_score",
    "trademark_status",
    "matched_terms",
    "amazon_url",
    "source",
    "collected_at_utc",
]


def export_to_csv(data, include_bom=True):
    """
    Convert a list of keyword dictionaries into CSV text.

    Returns CSV as a string, suitable for Streamlit download_button.
    """

    output = io.StringIO(newline="")

    writer = csv.DictWriter(
        output,
        fieldnames=CSV_COLUMNS,
        extrasaction="ignore",
    )

    writer.writeheader()

    for item in data:
        row = dict(item)

        # Convert lists to readable text.
        if isinstance(row.get("matched_terms"), list):
            row["matched_terms"] = ", ".join(
                row["matched_terms"]
            )

        writer.writerow(row)

    csv_text = output.getvalue()

    if include_bom:
        return "\ufeff" + csv_text

    return csv_text


def save_csv(data, filename=None):
    """Save keyword data to a local CSV file."""

    if filename is None:
        timestamp = datetime.now(
            timezone.utc
        ).strftime("%Y%m%d_%H%M%S")

        filename = f"merch_keywords_{timestamp}.csv"

    csv_text = export_to_csv(data)

    with open(filename, "w", encoding="utf-8", newline="") as file:
        file.write(csv_text)

    return filename


if __name__ == "__main__":
    sample_data = [
        {
            "keyword": "funny dachshund shirt",
            "niche": "Dogs",
            "demand_score": 75,
            "competition_score": 35,
            "competition_level": "Medium",
            "trend_score": 80,
            "buyer_intent_score": 85,
            "design_score": 90,
            "opportunity_score": 77.8,
            "trademark_status": "NO_MATCH",
            "matched_terms": [],
            "amazon_url": (
                "https://www.amazon.com/s?k="
                "funny+dachshund+shirt&i=fashion"
            ),
            "source": "Amazon Autocomplete",
            "collected_at_utc": datetime.now(
                timezone.utc
            ).isoformat(),
        }
    ]

    filename = save_csv(sample_data)

    print(f"CSV exported successfully: {filename}")
