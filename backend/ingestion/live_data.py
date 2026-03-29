import yfinance as yf
from datetime import datetime, timezone
import math

def fetch_market_snapshot(ticker_symbol: str) -> dict:
    """
    Fetches real-time price and volume data for a given ticker from Yahoo Finance.
    Provides grounding data for the AI analysis pipeline.
    
    Args:
        ticker_symbol: The stock ticker (e.g., 'RELIANCE.NS')
        
    Returns:
        dict: A structured dictionary mapping to the MarketSnapshot schema.
    """
    try:
        # Fetch data
        ticker = yf.Ticker(ticker_symbol)
        
        # Get historical data for the last 30 days to calculate a basic Z-score
        history = ticker.history(period="1mo")
        if history.empty:
            raise ValueError(f"No pricing data found for {ticker_symbol}")
            
        current_data = history.iloc[-1]
        current_price = float(current_data['Close'])
        current_volume = float(current_data['Volume'])
        
        # Calculate a basic Volume Z-Score (how unusual is today's volume?)
        # For hackathon demo simplicity, we compare today's volume to the 30-day mean.
        volumes = history['Volume'][:-1] # Exclude today for the baseline
        if not volumes.empty and volumes.std() > 0:
            mean_vol = volumes.mean()
            std_vol = volumes.std()
            volume_z_score = round((current_volume - mean_vol) / std_vol, 2)
        else:
            volume_z_score = 0.0
            
        # Calculate a basic Momentum Score (e.g., % change from the 30-day low)
        lowest_price = history['Low'].min()
        momentum_score = round(((current_price - lowest_price) / lowest_price) * 100, 2) if lowest_price > 0 else 0.0

        return {
            "source": "Yahoo Finance via yfinance",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "ticker": ticker_symbol,
            "current_price": current_price,
            "volume_z_score": volume_z_score,
            "momentum_score": momentum_score,
            "raw_volume": current_volume,
        }
        
    except Exception as e:
        # In a real app we'd log this, but we raise it here so the AI Synthesis Agent knows retrieval failed.
        raise Exception(f"Failed to fetch live data for {ticker_symbol}: {str(e)}")

# Quick test execution block
if __name__ == "__main__":
    test_ticker = "RELIANCE.NS"
    print(f"Fetching data for: {test_ticker}")
    data = fetch_market_snapshot(test_ticker)
    for key, value in data.items():
        print(f"{key}: {value}")
