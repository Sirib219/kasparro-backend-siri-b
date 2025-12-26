import requests

URL = "https://api.coinpaprika.com/v1/tickers"


def fetch_coinpaprika_data(limit: int = 10):
    response = requests.get(URL, timeout=10)
    response.raise_for_status()

    data = response.json()
    return data[:limit]
