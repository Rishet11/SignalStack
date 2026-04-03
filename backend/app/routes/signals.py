from fastapi import APIRouter, HTTPException
from typing import List
import uuid
import json
from ..schemas import OpportunityCard, AnalyzeTickerResponse
from ..agents.graph import run_signal_analysis
from ..database import cache_opportunity_card, log_audit_entry, DB_PATH
import aiosqlite
from ..config import logger

router = APIRouter()

@router.get("/opportunities", response_model=List[OpportunityCard])
async def get_opportunities():
    """Retrieve all cached daily opportunities."""
    opportunities = []
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute("SELECT opportunity_card FROM signal_cache ORDER BY timestamp DESC LIMIT 20")
            rows = await cursor.fetchall()
            for row in rows:
                opportunities.append(OpportunityCard(**json.loads(row[0])))
        return opportunities
    except Exception as e:
        logger.error(f"Error fetching opportunities: {e}")
        return []

@router.post("/analyze/{ticker}", response_model=AnalyzeTickerResponse)
async def analyze_ticker(ticker: str):
    """Trigger a full 6-agent analysis for a given ticker."""
    request_id = str(uuid.uuid4())
    logger.info(f"Starting analysis for {ticker} (Request ID: {request_id})")
    
    try:
        final_state = await run_signal_analysis(ticker, request_id)
        
        if final_state.get("errors"):
             raise HTTPException(status_code=400, detail=f"Analysis failed: {final_state['errors']}")
             
        card = final_state.get("opportunity_card")
        if not card:
             raise HTTPException(status_code=500, detail="Analysis completed but no card was generated.")
             
        # 1. Cache the result
        await cache_opportunity_card(ticker, card.model_dump_json())
        
        # 2. Log all audit entries
        for entry in final_state.get("audit_entries", []):
             await log_audit_entry(request_id, ticker, entry.model_dump())
             
        return AnalyzeTickerResponse(request_id=request_id, opportunity_card=card)

    except Exception as e:
        logger.error(f"Error analyzing {ticker}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
