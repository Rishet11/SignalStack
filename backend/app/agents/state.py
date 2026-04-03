from typing import List, Optional, Dict, Any, TypedDict
from ..schemas import TickerInfo, NewsItem, TechnicalSignal, HistoricalAnalog, BehavioralRisk, OpportunityCard, AuditEntry

class SignalState(TypedDict):
    # Metadata
    ticker: str
    request_id: str
    ticker_info: Optional[TickerInfo]
    
    # Data layer (Agent 1)
    price_data: Optional[Dict[str, Any]] # Latest data/indicators
    news_items: Optional[List[NewsItem]]
    
    # Agent 2 Outputs
    technical_signals: Optional[List[TechnicalSignal]]
    
    # Agent 3 Outputs
    context_summary: Optional[str]
    sentiment_score: Optional[float]
    
    # Agent 4 Outputs
    historical_analogs: Optional[List[HistoricalAnalog]]
    
    # Agent 5 Outputs
    behavioral_risks: Optional[List[BehavioralRisk]]
    
    # Agent 6 Outputs (Final)
    opportunity_card: Optional[OpportunityCard]
    
    # Audit trail
    audit_entries: List[AuditEntry]
    errors: List[str]
    current_step: Optional[str]
