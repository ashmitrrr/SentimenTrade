import streamlit as st
from transformers import pipeline
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# --- 1. LOAD AI MODEL (Cached) ---
@st.cache_resource
def load_model():
    return pipeline('sentiment-analysis', model='ProsusAI/finbert')

# --- 2. FETCH DATA FUNCTION (Cached to fix Rate Limit) ---
# This saves the data for 10 minutes (600 seconds) so we don't spam Yahoo
@st.cache_data(ttl=600)
def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
    
    # 1. Fetch History
    history = stock.history(period="1mo")
    
    # 2. Fetch News (Handle errors if missing)
    try:
        news = stock.news
    except Exception:
        news = []
        
    # 3. Fetch Info (Currency, etc.)
    try:
        info = stock.info
    except Exception:
        info = {}
        
    return history, news, info

# --- PAGE CONFIG ---
st.set_page_config(page_title="SentimenTrade", page_icon="📈", layout="wide")
st.title("SentimenTrade Dashboard")

# Load AI 
with st.spinner("Loading AI Brain..."):
    classifier = load_model()

# --- 3. SIDEBAR ---
with st.sidebar:
    st.header("Dashboard")
    ticker = st.text_input("Enter Stock Ticker:", "AAPL")
    st.info("💡 Tip: For India use .NS (e.g. ZOMATO.NS), for Aus use .AX (e.g. CBA.AX)")
    st.markdown("---")
    st.caption("Built with Streamlit")
    st.caption("Built by Ashmit")

# --- 4. MAIN APP ---
if st.button("Analyze Sentiment"):
    st.write(f"Fetching data for **{ticker}**...")
    
    try:
        # --- CALL THE CACHED FUNCTION ---
        # Instead of calling yf directly, we call our "smart" function
        history, news_list, stock_info = fetch_stock_data(ticker)
        
        # if data exists
        if history.empty:
            st.error(f"Could not find data for {ticker}. Please check the ticker symbol.")
        else:
            # latest price & change
            current_price = history['Close'].iloc[-1]
            prev_price = history['Close'].iloc[-2]
            price_change = current_price - prev_price
            
            # --- DETECT CURRENCY ---
            currency_code = stock_info.get('currency', 'USD') 
            symbol_map = {'USD': '$', 'INR': '₹', 'AUD': 'A$', 'EUR': '€', 'GBP': '£'}
            currency_symbol = symbol_map.get(currency_code, currency_code)

            # --- DISPLAY METRICS ---
            col1, col2, col3 = st.columns(3)
            col1.metric(f"Current Price ({currency_code})", 
                        f"{currency_symbol} {current_price:.2f}", 
                        f"{price_change:.2f}")
            
            # --- PLOTLY CHART ---
            fig = go.Figure(data=[go.Candlestick(x=history.index,
                        open=history['Open'],
                        high=history['High'],
                        low=history['Low'],
                        close=history['Close'])])
            
            fig.update_layout(title=f"{ticker} Price Action (Last 30 Days)", height=400)
            st.plotly_chart(fig, use_container_width=True)

            # --- NEWS & ANALYSIS ---
            st.markdown("### AI News Analysis")
            
            headlines = []
            sentiments = []
            scores = []
            links = [] 
            
            # loop through the news list we fetched earlier
            for item in news_list:
                # checks
                if 'content' in item:
                    headline = item['content']['title']
                    
                    click_data = item['content'].get('clickThroughUrl')
                    
                    # if it exists (not None)
                    if click_data:
                        link = click_data.get('url', 'https://finance.yahoo.com')
                    else:
                        link = 'https://finance.yahoo.com'
                    
                    # run ai
                    result = classifier(headline)[0]
                    label = result['label']
                    score = result['score']
                    
                    # store data
                    headlines.append(headline)
                    sentiments.append(label)
                    scores.append(score)
                    links.append(link)

            # --- RESULTS ---
            if len(headlines) > 0:
                # DataFrame
                df = pd.DataFrame({'Headline': headlines, 'Sentiment': sentiments, 'Score': scores})
                sentiment_counts = df['Sentiment'].value_counts()
                
                c1, c2 = st.columns([1, 2])
                
                # bar 
                with c1:
                    st.write("### Sentiment Ratio")
                    st.bar_chart(sentiment_counts)
                
                # expander
                with c2:
                    st.write("### Recent Headlines (Click to Expand)")
                    
                    # display 10 articles
                    for i in range(min(10, len(headlines))): 
                        text = headlines[i]
                        label = sentiments[i]
                        score_pct = scores[i] * 100
                        link = links[i]
                        
                        if label == 'positive':
                            emoji = "🟢"
                        elif label == 'negative':
                            emoji = "🔴"
                        else:
                            emoji = "⚪"
                        
                        with st.expander(f"{emoji} [{score_pct:.0f}%] {text}"):
                            st.write(f"**Sentiment:** {label.title()} ({score_pct:.1f}% Confidence)")
                            st.markdown(f"**🔗 [Read Full Article on Yahoo Finance]({link})**")
            else:
                st.warning("No news found to analyze for this stock.")

    except Exception as e:
        st.error(f"An error occurred: {e}")