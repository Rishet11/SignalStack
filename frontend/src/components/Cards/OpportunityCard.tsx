import React from 'react';
import type { OpportunityCard as OpportunityCardType } from '../../types';
import { TrendingUp, TrendingDown, Info, ShieldAlert } from 'lucide-react';
import { Link } from 'react-router-dom';

interface OpportunityCardProps {
  opportunity: OpportunityCardType;
}

const OpportunityCard: React.FC<OpportunityCardProps> = ({ opportunity }) => {
  const isBullish = opportunity.direction === 'bullish';

  return (
    <div className="glass-card opp-card hover-lift">
      <div className="card-header">
        <div className="ticker-badge">
          <span className="symbol">{opportunity.ticker}</span>
          <span className="exchange">NSE</span>
        </div>
        <div className={`confidence-gauge ${opportunity.direction}`}>
          <div className="score">{opportunity.confidence_score}%</div>
          <div className="label">Confidence</div>
        </div>
      </div>

      <div className="card-body">
        <div className="company-name">{opportunity.company_name}</div>
        <div className="signal-type">
          {isBullish ? <TrendingUp size={13} /> : <TrendingDown size={13} />}
          <span>{opportunity.primary_signal_type.replace(/_/g, ' ')}</span>
        </div>

        <p className="thesis">{opportunity.thesis}</p>

        {opportunity.behavioral_warning && (
          <div className="warning-pulse">
            <ShieldAlert size={13} />
            <span>{opportunity.behavioral_warning.risk_type}</span>
          </div>
        )}
      </div>

      <div className="card-footer">
        <div className="evidence-count">
          <Info size={13} />
          <span>{opportunity.evidence_sources.length} sources cited</span>
        </div>
        <Link to={`/ticker/${opportunity.ticker}`} className="detail-link">
          Deep Dive →
        </Link>
      </div>
    </div>
  );
};

export default OpportunityCard;
