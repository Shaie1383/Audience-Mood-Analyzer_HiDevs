# Advanced Mood Analyzer with Multi-Platform and Dashboard Support + Website Review Integration
import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from transformers import pipeline
from googleapiclient.discovery import build
import re
import random
from bs4 import BeautifulSoup
import urllib.request

# -----------------------
# Load Sentiment Model
# -----------------------
@st.cache_resource
def load_sentiment_model():
    return pipeline("sentiment-analysis")

sentiment_model = load_sentiment_model()

# -----------------------
# Mock Dataset (Extended)
# -----------------------
mock_data = pd.DataFrame({
    "text": [
        "AI is transforming the world rapidly!",
        "I’m scared of what AI might do in the future.",
        "AI is neutral – it’s humans that matter.",
        "Amazing AI breakthrough announced by OpenAI!",
        "AI is overhyped in some areas, underused in others.",
        "So excited about the future of artificial intelligence!",
        "AI-generated content is both exciting and scary.",
        "I don't trust AI making decisions for humans.",
        "AI tools helped me become more productive.",
        "Too much hype, not enough real-world use cases."
    ] * 3
})

# -----------------------
# Fetch Tweets Function
# -----------------------
def fetch_tweets(bearer_token, keyword, tweet_count):
    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }
    url = f"https://api.twitter.com/2/tweets/search/recent?query={keyword}&max_results={min(tweet_count, 100)}&tweet.fields=text"

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        tweets_data = response.json()
        return [tweet["text"] for tweet in tweets_data.get("data", [])]
    elif response.status_code == 429:
        st.warning("⚠️ Rate limit hit. Showing mock tweets instead.")
        return mock_data["text"].sample(tweet_count, replace=True).tolist()
    else:
        st.error(f"❌ Twitter API Error: {response.status_code}")
        return []

# -----------------------
# Extract YouTube Video ID
# -----------------------
def extract_video_id(youtube_url):
    regex = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(regex, youtube_url)
    return match.group(1) if match else None

# -----------------------
# Fetch YouTube Comments
# -----------------------
def fetch_youtube_comments(api_key, video_url, max_comments=20):
    video_id = extract_video_id(video_url)
    if not video_id:
        st.error("Invalid YouTube URL.")
        return []

    youtube = build("youtube", "v3", developerKey=api_key)
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=min(max_comments, 100),
        textFormat="plainText"
    )
    try:
        response = request.execute()
        comments = [
            item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            for item in response.get("items", [])
        ]
        return comments
    except Exception as e:
        st.warning("Failed to fetch YouTube comments. Showing mock data.")
        return mock_data["text"].sample(max_comments, replace=True).tolist()

# -----------------------
# Scrape Website Reviews
# -----------------------
def scrape_website_reviews(url, max_reviews=20):
    try:
        req = urllib.request.Request(
            url,
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0'
            }
        )
        page = urllib.request.urlopen(req)
        soup = BeautifulSoup(page, 'html.parser')
        paragraphs = soup.find_all('p')
        texts = [p.get_text().strip() for p in paragraphs if len(p.get_text()) > 40]
        return texts[:max_reviews] if texts else mock_data["text"].sample(max_reviews, replace=True).tolist()
    except Exception as e:
        st.error(f"Error scraping website: {e}")
        return mock_data["text"].sample(max_reviews, replace=True).tolist()

# -----------------------
# Analyze Mood Function
# -----------------------
def analyze_mood(texts):
    results = sentiment_model(texts)
    sentiment_counts = {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 0}
    final_results = []

    for text, result in zip(texts, results):
        label = result["label"].upper()
        if label == "POSITIVE":
            sentiment_counts["POSITIVE"] += 1
        elif label == "NEGATIVE":
            sentiment_counts["NEGATIVE"] += 1
        else:
            sentiment_counts["NEUTRAL"] += 1
        final_results.append({"text": text, "label": label, "score": result["score"]})

    return sentiment_counts, pd.DataFrame(final_results)

# -----------------------
# Streamlit App UI
# -----------------------
st.set_page_config(page_title="Advanced Mood Analyzer", layout="wide")
st.title("📊 Advanced Mood Analyzer - Social Media Sentiment Dashboard")

platform = st.selectbox("Choose Platform", ["Twitter", "YouTube", "Website"])

if platform == "Twitter":
    bearer_token = st.sidebar.text_input("🔐 Twitter Bearer Token", type="password")
    keyword = st.text_input("🔍 Enter keyword or hashtag", "#AI")
elif platform == "YouTube":
    youtube_api_key = st.sidebar.text_input("🔐 YouTube API Key", type="password")
    video_url = st.text_input("📺 Paste YouTube Video URL")
elif platform == "Website":
    site_url = st.text_input("🌐 Paste Website URL for Review Analysis")

comment_count = st.slider("📊 Number of Comments/Reviews", 10, 100, 20)
show_confidence = st.checkbox("🔎 Show Confidence Scores")

# Analyze Button
if st.button("Analyze Mood"):
    if platform == "Twitter":
        if not bearer_token:
            st.error("Enter Twitter Bearer Token.")
        else:
            with st.spinner("Analyzing tweets..."):
                texts = fetch_tweets(bearer_token, keyword, comment_count)
                sentiment_counts, df = analyze_mood(texts)

    elif platform == "YouTube":
        if not youtube_api_key or not video_url:
            st.error("Provide YouTube API Key and video link.")
        else:
            with st.spinner("Analyzing YouTube comments..."):
                texts = fetch_youtube_comments(youtube_api_key, video_url, comment_count)
                sentiment_counts, df = analyze_mood(texts)

    elif platform == "Website":
        if not site_url:
            st.error("Please provide a website URL.")
        else:
            with st.spinner("Scraping website reviews..."):
                texts = scrape_website_reviews(site_url, comment_count)
                sentiment_counts, df = analyze_mood(texts)

    if sentiment_counts:
        col1, col2 = st.columns([1, 2])

        with col1:
            st.subheader("🧠 Sentiment Distribution")
            labels = list(sentiment_counts.keys())
            sizes = list(sentiment_counts.values())
            colors = ["#90ee90", "#ffcccb", "#d3d3d3"]

            fig, ax = plt.subplots(figsize=(4, 4))
            ax.pie(sizes, labels=labels, autopct="%1.1f%%", colors=colors, startangle=90)
            ax.axis('equal')
            st.pyplot(fig)

        with col2:
            st.subheader("📊 Sentiment Breakdown")
            st.dataframe(df if show_confidence else df.drop(columns=["score"]))

        st.subheader("💡 Insight")
        if sentiment_counts["NEGATIVE"] > sentiment_counts["POSITIVE"]:
            st.warning("⚠️ High negative sentiment detected. Consider adjusting your messaging.")
        else:
            st.success("✅ Positive sentiment dominates. Keep up the good engagement!")

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV Report", csv, "sentiment_results.csv", "text/csv")
