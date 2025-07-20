import streamlit as st
import requests
from transformers import pipeline
import matplotlib.pyplot as plt

# -----------------------
# Sentiment model (Hugging Face)
# -----------------------
@st.cache_resource
def load_sentiment_model():
    return pipeline("sentiment-analysis")

sentiment_model = load_sentiment_model()

# -----------------------
# Mock tweets (used on API failure)
# -----------------------
def fetch_mock_tweets():
    return [
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
    ]

# -----------------------
# Fetch real tweets via Twitter API
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
        return fetch_mock_tweets()

    else:
        st.error(f"❌ Twitter API Error: {response.status_code}")
        return []

# -----------------------
# Analyze mood
# -----------------------
def analyze_mood(tweets):
    results = sentiment_model(tweets)
    sentiment_counts = {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 0}

    for result in results:
        label = result["label"].upper()
        if label == "POSITIVE":
            sentiment_counts["POSITIVE"] += 1
        elif label == "NEGATIVE":
            sentiment_counts["NEGATIVE"] += 1
        else:
            sentiment_counts["NEUTRAL"] += 1

    return sentiment_counts, results

# -----------------------
# Streamlit UI
# -----------------------
st.set_page_config(page_title="Mood Analyzer - Twitter Sentiment AI", layout="centered")
st.title("📊 Mood Analyzer - Twitter Sentiment AI")

# Input Bearer Token
bearer_token = st.sidebar.text_input("🔐 Enter your Twitter Bearer Token", type="password")

# Input keyword and number of tweets
keyword = st.text_input("🔍 Enter a keyword or hashtag (e.g., #AI, mood)", "#AI")
tweet_count = st.slider("📊 Number of Tweets to Analyze", 10, 100, 20)

if st.button("Analyze Mood"):
    if not bearer_token:
        st.error("Please enter a valid Bearer Token.")
    elif not keyword:
        st.error("Please enter a search keyword.")
    else:
        tweets = fetch_tweets(bearer_token, keyword, tweet_count)

        if tweets:
            sentiment_counts, full_results = analyze_mood(tweets)

            # Pie chart
            st.subheader("🧠 Mood Distribution")

            # ✅ Define sizes, labels, and colors before plotting
            labels = ['POSITIVE', 'NEGATIVE', 'NEUTRAL']
            sizes = [
                sentiment_counts['POSITIVE'],
                sentiment_counts['NEGATIVE'],
                sentiment_counts['NEUTRAL']
            ]
            colors = ['#2ecc71', '#e74c3c', '#f1c40f']  # green, red, yellow

            fig, ax = plt.subplots(figsize=(4, 4))  # 👈 reduced chart size
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
            ax.axis('equal')
            st.pyplot(fig)
    

            # Show results
            st.subheader("📝 Sample Sentiment Results")
            for i, (tweet, result) in enumerate(zip(tweets[:5], full_results[:5])):
                st.markdown(f"**{i+1}.** {tweet}")
                st.markdown(f"Sentiment: `{result['label']}` | Confidence: `{result['score']:.2f}`")
        else:
            st.warning("No tweets found or failed to fetch data.")
