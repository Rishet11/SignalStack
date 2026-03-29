def evaluate_behavioral_risk(market_data: dict, signal_flags: list, context: dict) -> dict:
    """
    Agent 5: Behavioral Risk Agent
    The core differentiator of SignalStack. It detects FOMO, late-entry hype,
    and momentum exhaustion to save retail investors from buying tops.
    """
    
    is_fomo = False
    is_late_entry = False
    warning_message = "No behavioral risks detected. Setup is clean."
    reversal_prob = 15.0 # baseline
    
    z_score = market_data.get("volume_z_score", 0.0)
    momentum = market_data.get("momentum_score", 0.0)
    sentiment = context.get("catalyst_sentiment", "Neutral")
    
    # 1. Detect pure FOMO Breakout Chasing (High score, low quality news/no news)
    if z_score > 3.0 and momentum > 30.0 and sentiment != "Positive":
        is_fomo = True
        is_late_entry = True
        warning_message = "CAUTION: Pure FOMO rally. Volume is abnormally high without verified positive news. Retail is chasing the hype."
        reversal_prob = 85.0
        
    # 2. Detect Late Entry (Good setup, but too extended)
    elif momentum > 20.0 and sentiment == "Positive":
        is_late_entry = True
        warning_message = "WARNING: Setup was strong, but price is already highly extended. Risk of immediate pullback."
        reversal_prob = 65.0
        
    # 3. Detect "Catching a Falling Knife"
    elif z_score > 2.0 and momentum < -20.0 and sentiment == "Negative":
        is_fomo = False # Not FOMO, just panic
        is_late_entry = True # Too late to short, too early to buy
        warning_message = "WARNING: High volume crash on negative catalyst. Trying to buy the dip here is historically dangerous."
        reversal_prob = 55.0 # 55% chance it continues crashing
        
    return {
        "is_fomo": is_fomo,
        "is_late_entry": is_late_entry,
        "warning_message": warning_message,
        "historical_reversal_prob": reversal_prob
    }
