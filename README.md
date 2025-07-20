# 💡 Advanced Mood Analyzer – Social Media Sentiment Dashboard

An advanced, multi-platform tool to analyze public sentiment and mood across **Twitter**, **YouTube**, and **review websites**. Built using `Streamlit`, `transformers`, and web scraping tools for intelligent decision-making and audience understanding.

---

## 📸 Preview

![Sentiment Dashboard Screenshot](screenshots/16e72896-6a2c-45ff-97b1-4c9d6e1a2fda.png)

---

## 🚀 Features

| Feature | Description |
|--------|-------------|
| 🐦 **Twitter Integration** | Analyze latest tweets by keyword or hashtag. |
| 📺 **YouTube Comments** | Paste any YouTube link to analyze video feedback. |
| 🌐 **Website Reviews** | Paste URLs of review sites (e.g., CollegeDekho, Yelp) and analyze sentiment of user opinions. |
| 🧠 **Transformer-Based Sentiment Model** | Uses Hugging Face’s sentiment pipeline. |
| 💬 **Mock Tweet Dataset** | Built-in support to simulate tweets when API fails or token isn’t available. |
| 📈 **Pie Chart Visualization** | Visual sentiment distribution via pie chart. |
| 📑 **Review Breakdown** | Display individual comment sentiment with optional confidence scores. |
| 📥 **CSV Download** | Download the full sentiment report. |
| ⚡ **Dashboard Filters** | Toggle between platforms, adjust number of reviews/comments. |

---

## 📦 Tech Stack

- Python
- Streamlit
- Hugging Face Transformers
- Matplotlib
- YouTube Data API v3
- Twitter API v2
- BeautifulSoup (Web Scraping)

---

## 🧪 Example Use Cases

- 🏫 **College Selection**: Analyze real student reviews from college sites.
- 📦 **Product Hype Check**: See if Twitter buzz around new products is mostly positive or negative.
- 🎥 **Content Feedback**: Use YouTube comments to assess how a video is received by viewers.
- 🏢 **Brand Health**: Track brand sentiment from various sources before launches or campaigns.

---

## 🔐 API Keys Required

| Platform | Type | Where to Get |
|----------|------|---------------|
| Twitter | Bearer Token | [Twitter Developer Portal](https://developer.twitter.com/) |
| YouTube | API Key | [Google Developer Console](https://console.developers.google.com/) |

> ⚠️ If APIs hit rate limits or keys are not provided, the app will use mock tweets/comments to demonstrate.

---

## 🛠 Installation

```bash
git clone https://github.com/your-username/advanced-mood-analyzer.git
cd advanced-mood-analyzer
pip install -r requirements.txt
streamlit run app.py
