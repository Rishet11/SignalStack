def analyze_signals(market_data: dict) -> dict:
    """
    Agent 2: Signal Detection Agent
    Purely quantitative. It takes the normalized market snapshot
    and computes technical flags completely free of LLM hallucination.
    """
    flags = []
    
    # Check for unusual volume
    z_score = market_data.get("volume_z_score", 0.0)
    if z_score > 3.0:
        flags.append("Extreme Unusual Volume")
    elif z_score > 1.5:
        flags.append("High Volume Breakout")
        
    # Check for intense momentum
    momentum = market_data.get("momentum_score", 0.0)
    if momentum > 20.0:
        flags.append("Hyper Momentum Growth")
    elif momentum < -15.0:
        flags.append("Steep Decline / Reversal Zone")
        
    if not flags:
        flags.append("Stable / Routine Activity")
        
    return {
        "quantitative_flags": flags,
        "primary_metric_attention": "Volume" if z_score > 2.0 else "Price Action"
    }
