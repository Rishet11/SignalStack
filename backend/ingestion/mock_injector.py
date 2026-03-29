from pydantic import BaseModel
from datetime import datetime, timezone

class MockScenario(BaseModel):
    ticker: str
    scenario_type: str
    price: float
    volume_z_score: float
    momentum_score: float
    simulated_news_headline: str
    simulated_source: str

def inject_demo_scenario(scenario_name: str) -> dict:
    """
    Returns a highly structured, extreme edge-case for your live demo.
    This guarantees that the AI acts predictably when you are presenting
    to the judges, showcasing the Behavioral Layer perfectly.
    """
    
    scenarios = {
        "fomo_breakout": MockScenario(
            ticker="DEMO_FOMO",
            scenario_type="FOMO / Late Entry",
            price=150.0,
            volume_z_score=4.5, # Insanely high volume relative to history
            momentum_score=45.2, # Massive run-up
            simulated_news_headline="Random YouTube influencer says DEMO_FOMO is the next big thing, retail rushes in.",
            simulated_source="Twitter / Social Media Gossip"
        ),
        "earnings_collapse": MockScenario(
            ticker="DEMO_CRASH",
            scenario_type="Negative Earnings Surprise",
            price=45.0,
            volume_z_score=3.2,
            momentum_score=-25.0,
            simulated_news_headline="DEMO_CRASH misses Q3 earnings by 40%, CEO steps down unexpectedly.",
            simulated_source="Official NSE Corporate Filing"
        )
    }
    
    if scenario_name not in scenarios:
        raise ValueError(f"Scenario {scenario_name} not found. Available: {list(scenarios.keys())}")
        
    s = scenarios[scenario_name]
    
    # Map the scenario to the identical schema the live data uses so the AI doesn't know the difference.
    return {
        "source": "SignalStack Secure Demo Injector",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "ticker": s.ticker,
        "current_price": s.price,
        "volume_z_score": s.volume_z_score,
        "momentum_score": s.momentum_score,
        "raw_volume": 15000000,
        "_simulated_news": s.simulated_news_headline, # Hidden field for the Context Agent to pick up
        "_simulated_news_source": s.simulated_source
    }
