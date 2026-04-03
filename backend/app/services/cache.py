import json
import os
from typing import Optional, Dict, Any
import aiosqlite
from ..config import logger, CACHE_TTL_PRICE, CACHE_TTL_NEWS
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "signalstack.db")

async def get_cached_data(key: str, table: str = "signal_cache") -> Optional[Dict[str, Any]]:
    """Retrieve data from SQLite cache if not expired."""
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute(f"SELECT opportunity_card, timestamp FROM {table} WHERE ticker = ?", (key,))
            row = await cursor.fetchone()
            if row:
                data_json, timestamp_str = row
                # Check expiration
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                if datetime.now() - timestamp < timedelta(seconds=CACHE_TTL_PRICE):
                     return json.loads(data_json)
        return None
    except Exception as e:
        logger.error(f"Error reading from cache: {e}")
        return None

async def set_cached_data(key: str, data: Dict[str, Any], table: str = "signal_cache"):
    """Store data in SQLite cache."""
    try:
        data_json = json.dumps(data)
        async with aiosqlite.connect(DB_PATH) as db:
             await db.execute(
                 f"INSERT OR REPLACE INTO {table} (ticker, opportunity_card, timestamp) VALUES (?, ?, ?)",
                 (key, data_json, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
             )
             await db.commit()
    except Exception as e:
        logger.error(f"Error writing to cache: {e}")
