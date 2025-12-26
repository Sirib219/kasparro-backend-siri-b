import os
import requests

COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")


def fetch_coingecko_data():
    """
    Fetches market data from CoinGecko
    """
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 50,
        "page": 1
    }

    headers = {
        "x-cg-api-key": COINGECKO_API_KEY
    }

    response = requests.get(url, params=params, headers=headers, timeout=15)
    response.raise_for_status()
    return response.json()
