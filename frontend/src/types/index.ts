export interface TickerInfo {
  symbol: string;
  name: string;
  sector?: string;
  exchange: string;
}

export interface NewsItem {
  headline: string;
  source: string;
  url?: string;
  published_at: string;
  summary?: string;
  sentiment?: 'bullish' | 'bearish' | 'neutral';
  credibility_tag?: 'tier-1' | 'tier-2' | 'tier-3';
  is_event: boolean;
  event_type?: string;
}

export interface TechnicalSignal {
  signal_type: string;
  strength: number;
  direction: 'bullish' | 'bearish' | 'neutral';
  description: string;
  z_score?: number;
}

export interface HistoricalAnalog {
  pattern_name: string;
  match_count: number;
  reversal_probability: number;
  forward_returns_5d: number;
  forward_returns_10d: number;
  forward_returns_20d: number;
  explanation: string;
}

export interface BehavioralRisk {
  risk_type: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  explanation: string;
}

export interface EvidenceSource {
  source_type: string;
  url?: string;
  snippet: string;
  credibility_tag?: string;
}

export interface OpportunityCard {
  ticker: string;
  company_name: string;
  confidence_score: number;
  primary_signal_type: string;
  direction: 'bullish' | 'bearish' | 'neutral';
  thesis: string;
  detailed_reasoning: string;
  action_suggestion: string;
  evidence_sources: EvidenceSource[];
  behavioral_warning?: BehavioralRisk;
}

export interface AuditEntry {
  agent_name: string;
  duration_ms: number;
  status: 'success' | 'error';
  input_state_summary: string;
  output_state_summary: string;
  llm_prompt_snippet?: string;
  timestamp?: string;
  error_message?: string;
}

export interface AuditTrail {
  request_id: string;
  ticker: string;
  entries: AuditEntry[];
  completed_at: string;
}
