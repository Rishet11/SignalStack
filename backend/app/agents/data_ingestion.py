import time
from typing import Dict, Any
from .state import SignalState
from ..services.market_data import fetch_market_data, compute_indicators, detect_basic_signals
from ..services.news_service import get_latest_news
from ..services.ticker_resolver import resolve_ticker
from ..schemas import AuditEntry
from ..config import logger

async def data_ingestion_node(state: SignalState) -> Dict[str, Any]:
    """Agent 1: Fetch and normalize market data and news."""
    start_time = time.time()
    ticker = state["ticker"]
    request_id = state["request_id"]
    
    logger.info(f"[{request_id}] Agent 1: Ingesting data for {ticker}")
    
    # 1. Resolve ticker
    ticker_info = resolve_ticker(ticker)
    if not ticker_info:
        error_msg = f"Could not resolve ticker: {ticker}"
        state["errors"].append(error_msg)
        return {**state, "errors": state["errors"], "current_step": "data_ingestion_error"}

    # 2. Fetch market data
    df = await fetch_market_data(ticker_info.symbol)
    price_data = None
    if df is not None and not df.empty:
        df = compute_indicators(df)
        signals_summary = detect_basic_signals(df)
        price_data = signals_summary # Indicators + signals
    else:
        state["errors"].append(f"Failed to fetch market data for {ticker_info.symbol}")

    # 3. Fetch news
    news_items = await get_latest_news(ticker_info.symbol)
    
    # 4. Create Audit Entry
    duration_ms = int((time.time() - start_time) * 1000)
    audit_entry = AuditEntry(
        agent_name="data_ingestion",
        duration_ms=duration_ms,
        status="success" if price_data else "error",
        input_state_summary=f"Ticker: {ticker}",
        output_state_summary=f"Price data: {'Yes' if price_data else 'No'}, News count: {len(news_items)}",
        timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
    )
    
    return {
        "ticker_info": ticker_info,
        "price_data": price_data,
        "news_items": news_items,
        "audit_entries": state["audit_entries"] + [audit_entry],
        "current_step": "data_ingestion_complete"
    }
