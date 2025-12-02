# src/to_postgres.py
import pandas as pd
from sqlalchemy import create_engine, text

# update with your credentials
db_uri = "postgresql+psycopg2://postgres:yourpassword@localhost:5432/bank_reviews"
engine = create_engine(db_uri)

df = pd.read_csv("data/clean_reviews_with_topics.csv")
# map bank name to bank_id
with engine.connect() as conn:
    bank_map = {row['bank_name']: row['bank_id'] for row in conn.execute(text("SELECT bank_id, bank_name FROM banks")).mappings()}
# prepare rows
rows = []
for _, r in df.iterrows():
    rows.append({
        'bank_id': bank_map[r['bank']],
        'review_text': r['review'],
        'rating': int(r['rating']) if not pd.isna(r['rating']) else None,
        'review_date': r['date'] if not pd.isna(r['date']) else None,
        'sentiment_label': r['sentiment_label'],
        'sentiment_score': float(r['sentiment_score']) if not pd.isna(r['sentiment_score']) else None,
        'topic': int(r['topic']) if 'topic' in r and not pd.isna(r['topic']) else None,
        'source': r.get('source','Google Play')
    })
# insert in batches
df_insert = pd.DataFrame(rows)
df_insert.to_sql('reviews', engine, if_exists='append', index=False, method='multi', chunksize=1000)
print("Inserted rows into PostgreSQL")
