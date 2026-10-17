"""Weekly Google Trends export to CSV (Google Sheets ready).

Usage: python example.py "chatgpt" "gemini" --geo US
"""
import argparse
import csv
import datetime
import os
import sys

from apify_client import ApifyClient

ACTOR = "lagenuina_agency/google-trends-scraper"
TOKEN = os.environ.get("APIFY_TOKEN")
if not TOKEN:
    sys.exit("Set APIFY_TOKEN first: https://console.apify.com/settings/integrations")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("terms", nargs="+", help="keywords to track")
    p.add_argument("--geo", default="", help="country/region code, empty = worldwide")
    p.add_argument("--time-range", default="today 3-m")
    a = p.parse_args()

    client = ApifyClient(TOKEN)
    run = client.actor(ACTOR).call(run_input={
        "searchTerms": a.terms,
        "geo": a.geo,
        "timeRange": a.time_range,
        "includeInterestByRegion": False,
        "includeRelated": True,
    })
    items = client.dataset(run["defaultDatasetId"]).list_items().items

    today = datetime.date.today().isoformat()
    with open(f"trends_{today}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["searchTerm", "geo", "date", "value", "isPartial"])
        for it in items:
            for point in it.get("timeline", []):
                w.writerow([it["searchTerm"], it.get("geo", ""), point["date"][:10], point.get("value"), point.get("isPartial", False)])
    with open(f"rising_{today}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["searchTerm", "query", "growth"])
        for it in items:
            for q in it.get("relatedQueries_rising", []):
                w.writerow([it["searchTerm"], q["query"], q.get("formattedValue", q.get("value"))])
    print(f"{len(items)} keywords -> trends_{today}.csv, rising_{today}.csv")


if __name__ == "__main__":
    main()
