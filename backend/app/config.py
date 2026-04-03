import os
import logging
from dotenv import load_dotenv

load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("signalstack")

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Constants
CACHE_TTL_PRICE = 3600  # 1 hour
CACHE_TTL_NEWS = 3600   # 1 hour
CACHE_TTL_SIGNAL = 3600 # 1 hour

# Scoring weights
WEIGHTS = {
    "technical": 0.30,
    "event": 0.25,
    "news": 0.15,
    "historical": 0.20,
    "behavioral": 0.10
}
