import yfinance as yf

stock_ticker = "AAPL"
stock = yf.Ticker(stock_ticker)
news_list = stock.news

clean_headlines = []

print(f"--- NEWS FOR {stock_ticker} ---")

for item in news_list:
    if 'content' in item:
        title = item['content']['title'] 
        clean_headlines.append(title)
        print(f"- {title}")

print("\nDone! We have", len(clean_headlines), "headlines.")