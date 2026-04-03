import time
from typing import Dict, Any, List
from .state import SignalState
from ..schemas import TechnicalSignal, AuditEntry
from ..config import logger

async def signal_detection_node(state: SignalState) -> Dict[str, Any]:
    """Agent 2: Detect technical signals and patterns."""
    start_time = time.time()
    request_id = state.get("request_id", "Unknown")
    price_data = state.get("price_data")
    
    if not price_data:
        logger.warning(f"[{request_id}] Agent 2: No price data available.")
        return state

    logger.info(f"[{request_id}] Agent 2: Detecting signals...")
    
    # 1. Capture basic signals
    raw_signals = price_data.get("signals", [])
    technical_signals = []
    
    for rs in raw_signals:
        technical_signals.append(TechnicalSignal(
            signal_type=rs.get("type", "Unknown"),
            strength=0.8, # Default (0 to 1) 
            direction=rs.get("direction", "neutral"),
            description=f"Detected {rs.get('type')}.",
            z_score=rs.get("value") if "Volume" in rs.get("type", "") else None
        ))

    # 2. Add some more refined signals (logic here)
    indicators = price_data.get("indicators", {})
    rsi = indicators.get("RSI")
    if rsi and rsi > 70:
        technical_signals.append(TechnicalSignal(
            signal_type="MomentumExhaustion",
            strength=0.9,
            direction="bearish",
            description=f"RSI {rsi:.2f} indicates extreme overbought conditions."
        ))
    elif rsi and rsi < 30:
         technical_signals.append(TechnicalSignal(
            signal_type="OversoldBounce",
            strength=0.9,
            direction="bullish",
            description=f"RSI {rsi:.2f} indicates extreme oversold conditions."
        ))

    # 3. Create Audit Entry
    duration_ms = int((time.time() - start_time) * 1000)
    audit_entry = AuditEntry(
        agent_name="signal_detection",
        duration_ms=duration_ms,
        status="success",
        input_state_summary=f"Signals count logic: {len(technical_signals)}",
        output_state_summary=f"Technical Signals count: {len(technical_signals)}",
        timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
    )
    
    return {
        "technical_signals": technical_signals,
        "audit_entries": state["audit_entries"] + [audit_entry],
        "current_step": "signal_detection_complete"
    }
