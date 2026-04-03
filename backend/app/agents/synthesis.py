import time
import json
from typing import Dict, Any
from .state import SignalState
from ..schemas import OpportunityCard, EvidenceSource, AuditEntry
from ..config import logger, WEIGHTS
from .llm_factory import get_llm, get_system_prompt
from langchain_core.messages import SystemMessage, HumanMessage

async def synthesis_node(state: SignalState) -> Dict[str, Any]:
    """Agent 6: Synthesize all signals into a final opportunity card using Gemma 4."""
    start_time = time.time()
    request_id = state.get("request_id", "Unknown")
    ticker_info = state.get("ticker_info")
    technical_signals = state.get("technical_signals", [])
    context_summary = state.get("context_summary", "No news context available.")
    sentiment_score = state.get("sentiment_score", 0.0)
    historical_analogs = state.get("historical_analogs", [])
    behavioral_risks = state.get("behavioral_risks", [])
    
    if not ticker_info:
        logger.error(f"[{request_id}] Agent 6: No ticker info found.")
        return state

    logger.info(f"[{request_id}] Agent 6: Synthesizing with Gemma 4 Thinking Mode...")
    
    # 1. Compute weighted confidence score
    tech_score = max([s.strength for s in technical_signals]) * 100 if technical_signals else 50
    news_score = (sentiment_score + 1) * 50  # Map -1...1 to 0...100
    hist_score = (1 - historical_analogs[0].reversal_probability) * 100 if historical_analogs else 50
    risk_adj = -20 if any(r.severity in ["high", "critical"] for r in behavioral_risks) else 0
    
    confidence_score = (tech_score * WEIGHTS["technical"] +
                        news_score * WEIGHTS["news"] +
                        hist_score * WEIGHTS["historical"]) + risk_adj
    confidence_score = max(0, min(100, confidence_score))

    # 2. Determine primary direction
    direction = "neutral"
    if technical_signals:
        bull = sum(1 for s in technical_signals if s.direction == "bullish")
        bear = sum(1 for s in technical_signals if s.direction == "bearish")
        if bull > bear: direction = "bullish"
        elif bear > bull: direction = "bearish"

    # 3. Call Gemma 4 with Thinking Mode for synthesis
    # Data-first ordering per Gemma 4 best practices
    system_instruction = get_system_prompt(
        "You are a senior investment strategist synthesizing a market opportunity for Indian investors. "
        "Your analysis must be actionable, precise, and grounded in the provided data. "
        "Think step-by-step through the evidence before writing your final synthesis.",
        enable_thinking=True  # Most important agent — use full thinking mode
    )

    signals_str = ", ".join([s.signal_type for s in technical_signals]) or "No clear signals"
    patterns_str = ", ".join([a.pattern_name for a in historical_analogs]) or "No historical matches"
    risks_str = ", ".join([r.risk_type for r in behavioral_risks]) or "None detected"

    user_prompt = f"""Complete market analysis data for {ticker_info.name} ({ticker_info.symbol}):

TECHNICAL SIGNALS: {signals_str}
NEWS CONTEXT SUMMARY: {context_summary}
NEWS SENTIMENT SCORE: {sentiment_score:.2f}
HISTORICAL PATTERN MATCHES: {patterns_str}
BEHAVIORAL RISKS DETECTED: {risks_str}
COMPUTED CONFIDENCE SCORE: {confidence_score:.1f}% ({direction.upper()} bias)

Using the above comprehensive data, produce a final investment synthesis:
1. Write a one-line "Thesis" (max 15 words) capturing the single most critical takeaway.
2. Write "Detailed Reasoning" (2-3 short paragraphs) connecting all data points.
3. Suggest a precise action (e.g., "Wait for pullback to 2,980", "Strong momentum play").
4. Cite exactly 3 evidence sources (technical, news, historical).

Output ONLY in this JSON format:
{{
    "thesis": "...",
    "detailed_reasoning": "...",
    "action_suggestion": "...",
    "evidence_sources": [
        {{"source_type": "technical", "snippet": "..."}},
        {{"source_type": "news", "snippet": "..."}},
        {{"source_type": "historical", "snippet": "..."}}
    ]
}}"""
    
    try:
        llm = get_llm(thinking=True)
        response = await llm.ainvoke([
            SystemMessage(content=system_instruction),
            HumanMessage(content=user_prompt)
        ])
        
        json_str = response.content.strip()
        # Strip Gemma 4 thinking block before parsing JSON
        if "<channel|>" in json_str:
            json_str = json_str.split("<channel|>")[-1].strip()
        if "```json" in json_str:
            json_str = json_str.split("```json")[1].split("```")[0].strip()
        
        analysis = json.loads(json_str)
        evidence_sources = [EvidenceSource(**es) for es in analysis.get("evidence_sources", [])]
        
        opportunity_card = OpportunityCard(
            ticker=ticker_info.symbol,
            company_name=ticker_info.name,
            confidence_score=round(confidence_score, 1),
            primary_signal_type=technical_signals[0].signal_type if technical_signals else "Neutral",
            direction=direction,
            thesis=analysis.get("thesis"),
            detailed_reasoning=analysis.get("detailed_reasoning"),
            action_suggestion=analysis.get("action_suggestion"),
            evidence_sources=evidence_sources,
            behavioral_warning=behavioral_risks[0] if behavioral_risks else None
        )
        
        duration_ms = int((time.time() - start_time) * 1000)
        audit_entry = AuditEntry(
            agent_name="synthesis",
            duration_ms=duration_ms,
            status="success",
            input_state_summary=f"Signals: {len(technical_signals)} | Direction: {direction} | Confidence base: {confidence_score:.1f}",
            output_state_summary=f"Card created — Score: {opportunity_card.confidence_score}% | Thesis: {str(opportunity_card.thesis)[:80]}",
            llm_prompt_snippet=user_prompt[:120] + "...",
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
        )
        
        return {
            "opportunity_card": opportunity_card,
            "audit_entries": state["audit_entries"] + [audit_entry],
            "current_step": "synthesis_complete"
        }
        
    except Exception as e:
        logger.error(f"[{request_id}] Agent 6 Error: {e}")
        state["errors"].append(f"Agent 6 Error: {str(e)}")
        return state
