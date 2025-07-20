# sentiment_analyzer.py
from transformers import pipeline

# Load Hugging Face sentiment analysis model
sentiment_pipeline = pipeline("sentiment-analysis")

def analyze_sentiment(comments):
    return sentiment_pipeline(comments)
