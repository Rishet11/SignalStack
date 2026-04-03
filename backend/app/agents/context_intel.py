import time
import json
from typing import Dict, Any
from .state import SignalState
from ..schemas import NewsItem, AuditEntry
from ..config import logger
from .llm_factory import get_llm, get_system_prompt
from langchain_core.messages import SystemMessage, HumanMessage

async def context_intel_node(state: SignalState) -> Dict[str, Any]:
    """Agent 3: Use LLM to analyze news context and sentiment."""
    start_time = time.time()
    request_id = state.get("request_id", "Unknown")
    news_items = state.get("news_items", [])
    ticker_info = state.get("ticker_info")
    
    if not news_items or not ticker_info:
        logger.warning(f"[{request_id}] Agent 3: No news items available.")
        return state

    logger.info(f"[{request_id}] Agent 3: Analyzing news context with Gemma 4...")
    
    # Format news data BEFORE the instruction text (Gemma 4 best practice)
    news_str = "\n".join([f"- {n.headline} (Source: {n.source})" for n in news_items[:10]])

    # Native system role (Gemma 4 supports this natively)
    system_instruction = get_system_prompt(
        "You are a financial analyst specializing in the Indian stock market (NSE/BSE). "
        "You analyze market-moving news with precision and output structured JSON.",
        enable_thinking=True  # Trigger Gemma 4 Thinking Mode for deeper reasoning
    )

    # Data first, then task (recommended Gemma 4 prompt ordering)
    user_prompt = f"""Here is the latest news data for {ticker_info.name} ({ticker_info.symbol}):

HEADLINES:
{news_str}

Based on the above data, perform the following analysis:
1. Summarize the major catalysts or events (max 3 bullets).
2. Determine the overall sentiment score from -1.0 (very bearish) to 1.0 (very bullish).
3. Identify if any major corporate action (earnings, deals, management change) is happening.

Output ONLY in this JSON format:
{{
    "summary": "...",
    "sentiment_score": 0.0,
    "catalysts": ["...", "..."],
    "event_type": "...",
    "is_event": true
}}"""
    
    try:
        llm = get_llm(thinking=True)
        response = await llm.ainvoke([
            SystemMessage(content=system_instruction),
            HumanMessage(content=user_prompt)
        ])
        
        json_str = response.content.strip()
        # Parse out thinking block if present (<|channel>thought\n...<channel|>)
        if "<channel|>" in json_str:
            json_str = json_str.split("<channel|>")[-1].strip()
        if "```json" in json_str:
            json_str = json_str.split("```json")[1].split("```")[0].strip()
        
        analysis = json.loads(json_str)
        context_summary = analysis.get("summary")
        sentiment_score = analysis.get("sentiment_score")
        
        duration_ms = int((time.time() - start_time) * 1000)
        audit_entry = AuditEntry(
            agent_name="context_intel",
            duration_ms=duration_ms,
            status="success",
            input_state_summary=f"News count: {len(news_items)}",
            output_state_summary=f"Sentiment: {sentiment_score:.2f} | Summary: {str(context_summary)[:80]}...",
            llm_prompt_snippet=user_prompt[:120] + "...",
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
        )
        
        return {
            "context_summary": context_summary,
            "sentiment_score": sentiment_score,
            "audit_entries": state["audit_entries"] + [audit_entry],
            "current_step": "context_intel_complete"
        }
        
    except Exception as e:
        logger.error(f"[{request_id}] Agent 3 Error: {e}")
        state["errors"].append(f"Agent 3 Error: {str(e)}")
        return state
