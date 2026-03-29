from pydantic import BaseModel, Field
from typing import List, Optional

# FR1 / Phase 2: Input Data Schema
class SignalSource(BaseModel):
    source_name: str = Field(description="Name of the source, e.g., 'Yahoo Finance' or 'NSE Announcements'")
    source_url: str = Field(description="Direct URL to the exact filing or news piece to prevent hallucinated URLs.")
    date_published: str = Field(description="Timestamp of the event.")
    snippet: str = Field(description="Exact snippet from the source. Must be a direct quote.")

class MarketSnapshot(BaseModel):
    ticker: str
    current_price: float
    volume_z_score: float = Field(description="Measures how unusual the daily volume is.")
    momentum_score: float

# FR3 / Phase 3: Agent Outputs
class BehavioralWarning(BaseModel):
    is_fomo: bool = Field(description="True if the stock has run up too fast on low quality news.")
    is_late_entry: bool
    warning_message: str = Field(description="A 1-sentence warning for the user.")
    historical_reversal_prob: float = Field(description="Probability it reverses based on historical analogs.")

class OpportunityCard(BaseModel):
    ticker: str
    signal_type: str = Field(description="e.g., 'Breakout', 'Earnings Catalyst', 'Unusual Volume'")
    confidence_score: int = Field(ge=0, le=100)
    primary_reasoning: str = Field(description="Plain English summary of why this matters.")
    evidence_sources: List[SignalSource] = Field(description="MUST include at least 1 valid source.")
    behavioral_warning: Optional[BehavioralWarning] = None

# Audit Trail Schema for the Judges
class AuditLog(BaseModel):
    agent_name: str
    raw_input_data: str
    prompt_used: str
    agent_output: str
