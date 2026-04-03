import aiosqlite
import json
import os
from .config import logger

# Correct path for DB_PATH relative to the package
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "signalstack.db")
PRELOADED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "preloaded")

async def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS audit_log (
                request_id TEXT,
                ticker TEXT,
                agent_name TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                duration_ms INTEGER,
                status TEXT,
                input_data TEXT,
                output_data TEXT,
                prompt_snippet TEXT,
                error_msg TEXT
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS signal_cache (
                ticker TEXT PRIMARY KEY,
                opportunity_card TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.commit()
        
        # Prime cache with preloaded data if empty
        cursor = await db.execute("SELECT count(*) FROM signal_cache")
        count = (await cursor.fetchone())[0]
        if count == 0 and os.path.exists(PRELOADED_DIR):
            for filename in os.listdir(PRELOADED_DIR):
                if filename.endswith(".json"):
                    ticker = filename.split(".")[0]
                    with open(os.path.join(PRELOADED_DIR, filename), "r") as f:
                        card_json = f.read()
                        await db.execute(
                            "INSERT OR REPLACE INTO signal_cache (ticker, opportunity_card) VALUES (?, ?)",
                            (ticker, card_json)
                        )
            await db.commit()
            logger.info("Primed database with preloaded demo data.")
            
        logger.info(f"Database initialized at {DB_PATH}")

async def log_audit_entry(request_id: str, ticker: str, entry: dict):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            '''INSERT INTO audit_log 
               (request_id, ticker, agent_name, duration_ms, status, input_data, output_data, prompt_snippet, error_msg)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (request_id, ticker, entry.get("agent_name"), entry.get("duration_ms"), entry.get("status"), 
             entry.get("input_state_summary"), entry.get("output_state_summary"), 
             entry.get("llm_prompt_snippet"), entry.get("error_message"))
        )
        await db.commit()

async def cache_opportunity_card(ticker: str, card_json: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            '''INSERT OR REPLACE INTO signal_cache (ticker, opportunity_card, timestamp) 
               VALUES (?, ?, CURRENT_TIMESTAMP)''',
            (ticker, card_json)
        )
        await db.commit()
