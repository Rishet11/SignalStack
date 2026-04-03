from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Literal, Dict, Any
from datetime import datetime

class TickerInfo(BaseModel):
    symbol: str
    name: str
    sector: Optional[str] = None
    exchange: str = "NSE"

class NewsItem(BaseModel):
    headline: str
    source: str
    url: Optional[str] = None
    published_at: str
    summary: Optional[str] = None
    sentiment: Optional[Literal["bullish", "bearish", "neutral"]] = None
    credibility_tag: Optional[Literal["tier-1", "tier-2", "tier-3"]] = None
    is_event: bool = False
    event_type: Optional[str] = None

class TechnicalSignal(BaseModel):
    signal_type: str
    strength: float # 0 to 100
    direction: Literal["bullish", "bearish", "neutral"]
    description: str
    z_score: Optional[float] = None

class HistoricalAnalog(BaseModel):
    pattern_name: str
    match_count: int
    reversal_probability: float # 0.0 to 1.0
    forward_returns_5d: float
    forward_returns_10d: float
    forward_returns_20d: float
    explanation: str

class BehavioralRisk(BaseModel):
    risk_type: str
    severity: Literal["low", "medium", "high", "critical"]
    explanation: str

class EvidenceSource(BaseModel):
    source_type: str # "news", "filings", "technical", "pattern"
    url: Optional[str] = None
    snippet: str
    credibility_tag: Optional[str] = None

class OpportunityCard(BaseModel):
    ticker: str
    company_name: str
    confidence_score: float # 0 to 100
    primary_signal_type: str
    direction: Literal["bullish", "bearish", "neutral"]
    thesis: str
    detailed_reasoning: str
    action_suggestion: str
    evidence_sources: List[EvidenceSource]
    behavioral_warning: Optional[BehavioralRisk] = None

class AnalyzeTickerResponse(BaseModel):
    request_id: str
    opportunity_card: OpportunityCard

# We can define the SignalState type natively in state.py using TypedDict.
# Here we define the audit trail outputs

class AuditEntry(BaseModel):
    agent_name: str
    duration_ms: int
    status: Literal["success", "error"]
    input_state_summary: str
    output_state_summary: str
    llm_prompt_snippet: Optional[str] = None
    timestamp: Optional[str] = None
    error_message: Optional[str] = None

class AuditTrail(BaseModel):
    request_id: str
    ticker: str
    entries: List[AuditEntry]
    completed_at: str
