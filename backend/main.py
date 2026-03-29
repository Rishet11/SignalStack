from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the current directory to sys.path to allow module imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ingestion.live_data import fetch_market_snapshot
from ingestion.mock_injector import inject_demo_scenario
from agents.synthesis_agent import generate_opportunity_card

app = FastAPI(
    title="SignalStack AI Engine",
    description="Backend orchestration for the ET Gen AI Hackathon",
    version="1.0.0"
)

# Crucial constraint: Allow Next.js frontend to talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TickerRequest(BaseModel):
    ticker: str
    use_mock: bool = False
    mock_scenario_name: str = ""

@app.get("/")
def health_check():
    return {"status": "ok", "message": "SignalStack Multi-Agent Backend is Running"}

@app.post("/api/snapshot")
def get_snapshot(request: TickerRequest):
    """
    Phase 2 Integration: Retrieves the grounded data before it is sent to the LLM Synthesis agents.
    """
    try:
        if request.use_mock:
            data = inject_demo_scenario(request.mock_scenario_name)
        else:
            data = fetch_market_snapshot(request.ticker)
            
        return {"status": "success", "data": data}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/analyze")
def synthesize_opportunity(request: TickerRequest):
    """
    Phase 3 Integration: Triggers the multi-agent orchestration pipeline.
    This generates the final grounded JSON object for the frontend dashboard.
    """
    try:
        # Step 1: Ingest Data (Agent 1)
        if request.use_mock:
            raw_data = inject_demo_scenario(request.mock_scenario_name)
        else:
            raw_data = fetch_market_snapshot(request.ticker)
            
        # Step 2: Trigger Synthesis Engine (Agents 2-6)
        card = generate_opportunity_card(raw_data)
        
        # Step 3: Return Grounded Output
        return {
            "status": "success",
            # We also return raw_data so the frontend's Audit Trail can prove no hallucination
            "audit_trail": raw_data, 
            "card": card.model_dump() 
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
