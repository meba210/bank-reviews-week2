# src/preprocess.py
import pandas as pd
import os
from dateutil import parser

os.makedirs("data", exist_ok=True)
df = pd.read_csv("data/raw_reviews.csv")

# Drop duplicates by review text
df = df.drop_duplicates(subset=["review"])

# Drop empty reviews
df = df[df["review"].notnull() & (df["review"].str.strip() != "")]

# Ensure rating is int
df['rating'] = pd.to_numeric(df['rating'], errors='coerce').astype('Int64')

# Normalize date to YYYY-MM-DD if datetime-like; if string, parse
def normalize_date(x):
    try:
        return parser.parse(str(x)).date().isoformat()
    except Exception:
        return None

df['date'] = df['date'].apply(normalize_date)

# Reorder columns
df = df[["review", "rating", "date", "bank", "source"]]

df.to_csv("data/clean_reviews.csv", index=False)
print("Clean reviews saved:", len(df))
print(df['bank'].value_counts())
