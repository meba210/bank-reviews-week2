# src/scrape_reviews.py
from google_play_scraper import reviews_all
import pandas as pd
import os
import time

os.makedirs("data", exist_ok=True)

# Correct app IDs (verified)
apps = {
    "CBE": "com.combanketh.mobilebanking",
    "BOA": "com.boa.boaMobileBanking",
    "Dashen": "com.dashen.dashensuperapp"
}

all_rows = []

for bank, app_id in apps.items():
    print(f"Scraping: {bank} ({app_id})")

    combined_reviews = []

    for lang in ['en', 'am']:  
        try:
            print(f"  -> Fetching lang={lang}")
            reviews = reviews_all(
                app_id,
                lang=lang,
                country='et'   # Ethiopia
            )
            print(f"     Collected {len(reviews)} reviews for lang={lang}")
            combined_reviews.extend(reviews)
            time.sleep(1)

        except Exception as e:
            print("Error:", e)

    print(f"Total reviews for {bank}: {len(combined_reviews)}")

    for r in combined_reviews:
        all_rows.append({
            "review": r.get("content", ""),
            "rating": r.get("score", None),
            "date": r.get("at", None),
            "bank": bank,
            "source": "Google Play"
        })

df = pd.DataFrame(all_rows)
df.to_csv("data/raw_reviews.csv", index=False)
print("FINAL TOTAL REVIEWS:", len(df))
