import time
import json
from typing import Dict, Any
from .state import SignalState
from ..schemas import BehavioralRisk, AuditEntry
from ..config import logger
from .llm_factory import get_llm, get_system_prompt
from langchain_core.messages import SystemMessage, HumanMessage

async def behavioral_risk_node(state: SignalState) -> Dict[str, Any]:
    """Agent 5: Detect FOMO and behavioral timing risks using LLM."""
    start_time = time.time()
    request_id = state.get("request_id", "Unknown")
    technical_signals = state.get("technical_signals", [])
    sentiment_score = state.get("sentiment_score", 0.0)
    ticker_info = state.get("ticker_info")
    
    if not ticker_info or not technical_signals:
         logger.warning(f"[{request_id}] Agent 5: Insufficient data for behavioral risk analysis.")
         return state

    logger.info(f"[{request_id}] Agent 5: Analyzing behavioral risks with Gemma 4...")
    
    # Data first (Gemma 4 recommended ordering)
    signal_str = "\n".join([f"- {s.signal_type}: {s.description}" for s in technical_signals])

    system_instruction = get_system_prompt(
        "You are a behavioral finance expert specializing in Indian retail investor psychology. "
        "You identify dangerous timing patterns like FOMO, exhaustion, and herd behavior. "
        "Output structured JSON with precise risk assessments.",
        enable_thinking=True
    )

    user_prompt = f"""Behavioral risk data for {ticker_info.name} ({ticker_info.symbol}):

TECHNICAL SIGNALS DETECTED:
{signal_str}

NEWS SENTIMENT SCORE: {sentiment_score:.2f} (scale: -1.0 bearish to +1.0 bullish)

Based on this data, identify any behavioral timing risks present:
1. Is this a "late entry" (FOMO) setup?
2. Is there momentum exhaustion or over-extension?
3. Is the trade crowded or chasing recent news?

Output ONLY in this JSON format:
{{
    "risks": [
        {{
            "risk_type": "...",
            "severity": "low/medium/high/critical",
            "explanation": "..."
        }}
    ]
}}
If no significant risks, return an empty list: {{"risks": []}}"""
    
    try:
        llm = get_llm(thinking=True)
        response = await llm.ainvoke([
            SystemMessage(content=system_instruction),
            HumanMessage(content=user_prompt)
        ])
        
        json_str = response.content.strip()
        if "<channel|>" in json_str:
            json_str = json_str.split("<channel|>")[-1].strip()
        if "```json" in json_str:
            json_str = json_str.split("```json")[1].split("```")[0].strip()
        
        analysis = json.loads(json_str)
        behavioral_risks = [BehavioralRisk(**r) for r in analysis.get("risks", [])]
        
        duration_ms = int((time.time() - start_time) * 1000)
        audit_entry = AuditEntry(
            agent_name="behavioral_risk",
            duration_ms=duration_ms,
            status="success",
            input_state_summary=f"Signals: {len(technical_signals)} | Sentiment: {sentiment_score:.2f}",
            output_state_summary=f"Risks found: {len(behavioral_risks)} | Severities: {[r.severity for r in behavioral_risks]}",
            llm_prompt_snippet=user_prompt[:120] + "...",
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
        )
        
        return {
            "behavioral_risks": behavioral_risks,
            "audit_entries": state["audit_entries"] + [audit_entry],
            "current_step": "behavioral_risk_complete"
        }
        
    except Exception as e:
        logger.error(f"[{request_id}] Agent 5 Error: {e}")
        state["errors"].append(f"Agent 5 Error: {str(e)}")
        return state
