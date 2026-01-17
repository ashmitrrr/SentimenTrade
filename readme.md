# SentimenTrade: Real-Time Financial Sentiment Analysis Dashboard

## Project Overview
SentimenTrade is a full-stack financial intelligence tool designed to bridge the gap between qualitative news data and quantitative market price action. The application leverages Natural Language Processing (NLP) to perform real-time sentiment analysis on financial news headlines, visualizing the correlation between market sentiment and stock price movements.

This project demonstrates the implementation of an end-to-end data pipeline, integrating live market data scraping, transformer-based machine learning models (BERT), and an interactive frontend interface.

## Key Features

* **Real-Time Data Pipeline:** dynamically scrapes live news and OHLC (Open, High, Low, Close) price data using the Yahoo Finance API.
* **NLP Sentiment Engine:** Implements the `ProsusAI/finbert` model—a BERT-based language model fine-tuned specifically on financial corpus—to classify headlines as Positive, Negative, or Neutral with confidence scores.
* **Interactive Visualization:** Renders professional-grade candlestick charts and sentiment distribution metrics using Plotly.
* **Global Market Support:** Features dynamic currency detection and ticker suffix handling to support global exchanges (e.g., NSE India, ASX Australia, NYSE).
* **Robust Error Handling:** Includes failsafes for missing data points, null API responses, and broken URLs.

## Technical Architecture

### Tech Stack
* **Language:** Python 3.10+
* **Frontend Framework:** Streamlit
* **Machine Learning:** Hugging Face Transformers (PyTorch backend)
* **Data Engineering:** yfinance, Pandas
* **Visualization:** Plotly Graph Objects

### Data Flow
1.  **Input:** User queries a specific stock ticker (e.g., `AAPL`, `ZOMATO.NS`).
2.  **Acquisition:** The application initiates a synchronous request to the Yahoo Finance API to fetch the last 30 days of price history and the latest 10-20 news items.
3.  **Processing:**
    * Price data is cleaned and structured into a Pandas DataFrame.
    * News headlines are tokenized and passed through the FinBERT pipeline.
4.  **Analysis:** The model outputs a sentiment classification and a softmax confidence score for each headline.
5.  **Visualization:** The frontend renders a dashboard combining the price chart with a statistical breakdown of the sentiment data.

## Installation and Usage

To run this project locally, follow the steps below.

### Prerequisites
* Python 3.8 or higher
* pip (Python Package Installer)
* Git

### Setup Instructions

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/SentimenTrade.git](https://github.com/YOUR_USERNAME/SentimenTrade.git)
    cd SentimenTrade
    ```

2.  **Create and Activate Virtual Environment**
    It is recommended to use a virtual environment to manage dependencies.
    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Application**
    ```bash
    python -m streamlit run app.py
    ```

## Project Structure

* `app.py`: The main entry point containing the application logic, UI layout, and data processing functions.
* `requirements.txt`: List of all Python dependencies required to run the application.
* `.gitignore`: Configuration file to ensure local environment files are not tracked by version control.

## Author
**Ashmit Raina**
