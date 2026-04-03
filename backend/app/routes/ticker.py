from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import pandas as pd
from ..schemas import TickerInfo
from ..services.ticker_resolver import search_tickers, resolve_ticker
from ..services.market_data import fetch_market_data
import json

router = APIRouter()

@router.get("/search", response_model=List[TickerInfo])
async def search_ticker(q: str = Query(..., min_length=2)):
    """Search for NSE tickers using fuzzy search."""
    return search_tickers(q)

@router.get("/{symbol}", response_model=TickerInfo)
async def get_ticker_info(symbol: str):
    """Retrieve detailed ticker info."""
    info = resolve_ticker(symbol)
    if not info:
        raise HTTPException(status_code=404, detail="Ticker not found.")
    return info

@router.get("/{symbol}/chart")
async def get_ticker_chart_data(symbol: str):
    """Retrieve OHLCV data for Lightweight Charts."""
    df = await fetch_market_data(symbol)
    if df is None or df.empty:
        raise HTTPException(status_code=404, detail="Chart data not found.")
    
    # Flatten MultiIndex columns returned by yfinance (e.g. ('Open', 'RELIANCE.NS') -> 'Open')
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]
    
    df = df.dropna(subset=['Open', 'High', 'Low', 'Close'])
    
    chart_data = []
    for idx, row in df.iterrows():
        time_val = idx[0] if isinstance(idx, tuple) else idx
        chart_data.append({
            "time": time_val.strftime("%Y-%m-%d"),
            "open": round(float(row["Open"]), 2),
            "high": round(float(row["High"]), 2),
            "low": round(float(row["Low"]), 2),
            "close": round(float(row["Close"]), 2),
            "volume": int(row["Volume"]) if not pd.isna(row["Volume"]) else 0
        })
    return chart_data
