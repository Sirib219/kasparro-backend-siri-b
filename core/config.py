import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/crypto"
)

COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")
COINPAPRIKA_API_KEY = os.getenv("COINPAPRIKA_API_KEY")
