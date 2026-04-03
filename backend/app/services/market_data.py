import yfinance as yf
import pandas as pd
import pandas_ta as ta
import numpy as np
from typing import Optional, Dict, Any
from ..config import logger

async def fetch_market_data(ticker: str, period: str = "6mo", interval: str = "1d") -> Optional[pd.DataFrame]:
    """Fetch OHLCV data from yfinance for a given NSE ticker."""
    symbol = f"{ticker}.NS" if not ticker.endswith(".NS") else ticker
    try:
        data = yf.download(symbol, period=period, interval=interval, progress=False)
        if data.empty:
            logger.warning(f"No data found for {symbol}")
            return None
        return data
    except Exception as e:
        logger.error(f"Error fetching data for {symbol}: {e}")
        return None

def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Compute technical indicators using pandas-ta."""
    # Ensure columns are named correctly for pandas-ta
    df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]

    # RSI
    df["RSI"] = ta.rsi(df["Close"], length=14)

    # MACD
    macd = ta.macd(df["Close"])
    if macD := macd: # Avoid NameError if macd is None
        df = pd.concat([df, macD], axis=1)

    # Bollinger Bands
    bbands = ta.bbands(df["Close"], length=20, std=2)
    if bb := bbands:
        df = pd.concat([df, bb], axis=1)

    # SMA/EMA
    df["SMA_20"] = ta.sma(df["Close"], length=20)
    df["EMA_20"] = ta.ema(df["Close"], length=20)
    df["SMA_50"] = ta.sma(df["Close"], length=50)

    # ATR for volatility
    df["ATR"] = ta.atr(df["High"], df["Low"], df["Close"], length=14)

    # Volume SMA
    df["Volume_SMA_20"] = ta.sma(df["Volume"], length=20)

    return df

def detect_basic_signals(df: pd.DataFrame) -> Dict[str, Any]:
    """Detect simple technical signals from the indicators."""
    latest = df.iloc[-1]
    prev = df.iloc[-2]

    signals = []

    # RSI Signals
    if latest["RSI"] > 70:
        signals.append({"type": "RSI_Overbought", "value": latest["RSI"], "direction": "bearish"})
    elif latest["RSI"] < 30:
        signals.append({"type": "RSI_Oversold", "value": latest["RSI"], "direction": "bullish"})

    # MACD Crossover
    if prev["MACD_12_26_9"] < prev["MACDs_12_26_9"] and latest["MACD_12_26_9"] > latest["MACDs_12_26_9"]:
        signals.append({"type": "MACD_Bullish_Crossover", "direction": "bullish"})
    elif prev["MACD_12_26_9"] > prev["MACDs_12_26_9"] and latest["MACD_12_26_9"] < latest["MACDs_12_26_9"]:
        signals.append({"type": "MACD_Bearish_Crossover", "direction": "bearish"})

    # Breakout/Breakdown
    recent_high = df["High"].iloc[-21:-1].max()
    if latest["Close"] > recent_high:
        signals.append({"type": "Price_Breakout", "direction": "bullish"})

    # Unusual Volume
    if latest["Volume"] > 2 * latest["Volume_SMA_20"]:
         signals.append({"type": "Unusual_Volume", "value": latest["Volume"] / latest["Volume_SMA_20"]})

    return {
        "latest_price": latest["Close"],
        "signals": signals,
        "indicators": latest.to_dict()
    }
