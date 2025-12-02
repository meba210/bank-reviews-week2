# src/final_plots.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("data/clean_reviews_with_topics.csv")

# Plot 1: rating distribution
plt.figure(figsize=(8,5))
sns.countplot(data=df, x='rating', hue='bank')
plt.title("Rating distribution by bank")
plt.savefig("reports/plot_rating_distribution.png", dpi=200)
plt.close()

# Plot 2: sentiment distribution per bank
sent_counts = df.groupby(['bank','sentiment_label']).size().unstack(fill_value=0)
sent_counts.plot(kind='bar', stacked=True, figsize=(8,5))
plt.title("Sentiment distribution by bank")
plt.savefig("reports/plot_sentiment_distribution.png", dpi=200)
plt.close()
