import requests

# Assuming you have stored your API key in a config.py file
from .config import ALPHA_VANTAGE_API_KEY

BASE_URL = "https://www.alphavantage.co/query"

def fetch_from_alpha_vantage(params):
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()

def get_company_overview(symbol):
    params = {
        "function": "OVERVIEW",
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    return fetch_from_alpha_vantage(params)

def get_earnings(symbol):
    params = {
        "function": "EARNINGS",
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    return fetch_from_alpha_vantage(params)


def get_time_series_daily(symbol):
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": symbol,
        "outputsize": "compact", # Or "full" for more historical data
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    return fetch_from_alpha_vantage(params)

def get_news(ticker):
    url = 'https://www.alphavantage.co/query'
    params = {
        "function": "NEWS_SENTIMENT",
        "ticker": ticker,
        "apikey": ALPHA_VANTAGE_API_KEY 
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()['feed'][:5]  # Return the first 5 articles
    else:
        return None

