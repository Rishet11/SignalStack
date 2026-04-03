import React, { useEffect, useState } from 'react';
import { signalsApi } from '../services/api';
import type { OpportunityCard as OpportunityCardType } from '../types';
import OpportunityCard from '../components/Cards/OpportunityCard';
import { Loader } from '../components/Common';

const Opportunities: React.FC = () => {
  const [opportunities, setOpportunities] = useState<OpportunityCardType[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchOpps = async () => {
      try {
        const data = await signalsApi.getOpportunities();
        // Sort descending by confidence score
        const sorted = [...data].sort((a, b) => b.confidence_score - a.confidence_score);
        setOpportunities(sorted);
      } catch (err) {
        console.error("Failed to fetch opportunities:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchOpps();
  }, []);

  return (
    <div className="opportunities-page animate-fade-up">
      <header className="page-header">
        <h1>Market Opportunities</h1>
        <p className="subtitle">Ranked signals by our multi-agent scoring model.</p>
      </header>

      {loading ? (
        <Loader message="Ranking opportunities..." />
      ) : (
        <div className="opportunities-grid">
          {opportunities.length > 0 ? (
            opportunities.map((opp, i) => (
              <div key={opp.ticker} className={`animate-fade-up stagger-${Math.min(i + 1, 5)}`}>
                <OpportunityCard opportunity={opp} />
              </div>
            ))
          ) : (
            <div className="empty-state glass-card">
              <p>No opportunities detected yet. Try analyzing a ticker!</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Opportunities;
