# src/thematic_analysis.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
import spacy
nlp = spacy.load("en_core_web_sm")

df = pd.read_csv("data/clean_reviews_with_sentiment.csv")
df['text_processed'] = df['review'].fillna("").str.lower()

# TF-IDF top terms per bank
tfidf = TfidfVectorizer(max_features=2000, ngram_range=(1,2), stop_words='english')
X = tfidf.fit_transform(df['text_processed'])
terms = tfidf.get_feature_names_out()

# NMF topic model (choose n_topics 6)
n_topics = 6
nmf = NMF(n_components=n_topics, random_state=42)
W = nmf.fit_transform(X)
H = nmf.components_

topic_keywords = {}
for topic_idx, topic in enumerate(H):
    topn = [terms[i] for i in topic.argsort()[-15:][::-1]]
    topic_keywords[f"topic_{topic_idx}"] = topn

# Assign dominant topic per review
topic_assignments = W.argmax(axis=1)
df['topic'] = topic_assignments
df.to_csv("data/clean_reviews_with_topics.csv", index=False)

# Save keywords mapping
import json
with open("reports/topic_keywords.json", "w", encoding="utf-8") as f:
    json.dump(topic_keywords, f, ensure_ascii=False, indent=2)

print("Saved topics and keywords")
