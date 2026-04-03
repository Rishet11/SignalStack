import json
import os
from typing import List, Optional, Dict
from fuzzywuzzy import process
from ..config import logger
from ..schemas import TickerInfo

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "data", "nse_symbols.json")

def load_symbols() -> List[Dict[str, str]]:
    """Load symbols from JSON file."""
    if not os.path.exists(DATA_FILE):
        logger.warning(f"Symbol file {DATA_FILE} not found.")
        return []

    with open(DATA_FILE, "r") as f:
        return json.load(f)

def resolve_ticker(query: str) -> Optional[TickerInfo]:
    """Resolve a common name or symbol to an NSE ticker."""
    symbols = load_symbols()
    if not symbols:
        return None

    # Exact match first
    for s in symbols:
        if s["symbol"].upper() == query.upper():
            return TickerInfo(**s)

    # Fuzzy match next
    names = [s["name"] for s in symbols]
    match, score = process.extractOne(query, names)
    if score > 80:
        for s in symbols:
            if s["name"] == match:
                return TickerInfo(**s)

    return None

def search_tickers(query: str, limit: int = 10) -> List[TickerInfo]:
    """Search for tickers based on query."""
    symbols = load_symbols()
    if not symbols:
        return []

    # Simple search in symbol or name
    matches = []
    for s in symbols:
        if query.upper() in s["symbol"].upper() or query.lower() in s["name"].lower():
             matches.append(TickerInfo(**s))
             if len(matches) >= limit:
                 break
    return matches
