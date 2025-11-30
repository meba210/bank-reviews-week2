# src/plots_for_interim.py
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib
matplotlib.use('Agg') 
 
import os

os.makedirs("reports", exist_ok=True)
df = pd.read_csv("data/clean_reviews.csv")

# Plot 1: rating distribution
plt.figure(figsize=(6,4))
df.groupby(['bank','rating']).size().unstack(fill_value=0).T.plot(kind='bar')
plt.title("Rating distribution by bank")
plt.xlabel("Rating")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("reports/rating_distribution.png", dpi=150)
plt.close()

# Simple freq words (naive)
stopwords = set(open('/usr/share/dict/words','w')) if False else set([
    "the","and","a","to","is","in","it","you","for","of","this","app","i"
])
def tokenize(text):
    tokens = re.findall(r'\b[a-zA-Z]{2,}\b', str(text).lower())
    return [t for t in tokens if t not in stopwords]

all_words = []
for text in df['review'].dropna():
    all_words += tokenize(text)
most = Counter(all_words).most_common(15)
words, counts = zip(*most)

plt.figure(figsize=(6,4))
plt.barh(words[::-1], counts[::-1])
plt.title("Top 15 words")
plt.tight_layout()
plt.savefig("reports/top_words.png", dpi=150)
plt.close()

# Optional: quick sentiment using VADER (fast)
analyzer = SentimentIntensityAnalyzer()
df['vader_compound'] = df['review'].fillna("").apply(lambda x: analyzer.polarity_scores(x)['compound'])
df['vader_label'] = df['vader_compound'].apply(lambda s: "pos" if s>=0.05 else ("neg" if s<=-0.05 else "neu"))
df.to_csv("data/clean_reviews_with_sentiment.csv", index=False)

print("Plots saved to reports/, sample sentiment saved.")
