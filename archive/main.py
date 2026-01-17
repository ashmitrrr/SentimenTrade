# from transformers import pipeline

# print("Loading AI... (This might take a minute)")
# classifier = pipeline('sentiment-analysis', model='ProsusAI/finbert')

# # headlines
# headlines = [
#     "Apple is hungry for mango.",
#     "Google ceo had sex with a hooker, girl is pregnant, media wants the girl to have twins and die.",
#     "Market is closed today for the holiday."
# ]

# # analysis
# print("\n--- RESULTS ---")
# for text in headlines:
#     result = classifier(text)[0]
#     print(f"News: {text}")
#     print(f"Sentiment: {result['label']} (Score: {result['score']:.2f})\n")

import yfinance as yf
from transformers import pipeline

# 1. SETUP: Load the AI Brain (This takes a few seconds)
print("Loading AI model... (Please wait)")
classifier = pipeline('sentiment-analysis', model='ProsusAI/finbert')

# 2. INPUT: Ask the user which stock to check
ticker = input("\nEnter a Stock Ticker (e.g. AAPL, TSLA, GOOG): ")

# 3. SCRAPING: Connect to Yahoo Finance
print(f"\nFetching news for {ticker}...")
stock = yf.Ticker(ticker)
news_list = stock.news

# 4. PROCESSING: Extract headlines and analyze them
print(f"\n--- SENTIMENT REPORT FOR {ticker} ---\n")

headlines_found = 0

for item in news_list:
    if 'content' in item:
        headline = item['content']['title']
        
        # --- NEW: STRICT FILTER ---
        # Only process if the Ticker (e.g., AAPL) or Company Name (Apple) is in the text
        if ticker in headline or "Apple" in headline: 
            headlines_found += 1
            result = classifier(headline)[0]
            
            print(f"News: {headline}")
            label = result['label']
            score = result['score'] * 100
            print(f"Prediction: {label} (Confidence: {score:.0f}%)")
            print("-" * 50)

if headlines_found == 0:
    print("No news found for this stock today.")