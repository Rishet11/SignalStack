import React, { useEffect, useState } from 'react';
import { signalsApi } from '../services/api';
import type { OpportunityCard as OpportunityCardType } from '../types';
import OpportunityCard from '../components/Cards/OpportunityCard';
import { Loader } from '../components/Common';
import TickerSearch from '../components/Search/TickerSearch';
import { Zap } from 'lucide-react';

const Dashboard: React.FC = () => {
  const [trending, setTrending] = useState<OpportunityCardType[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTrending = async () => {
      try {
        const data = await signalsApi.getOpportunities();
        // Sort descending by confidence, take top 3
        const sorted = [...data]
          .sort((a, b) => b.confidence_score - a.confidence_score)
          .slice(0, 3);
        setTrending(sorted);
      } catch (err) {
        console.error("Dashboard fetch failed:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchTrending();
  }, []);

  return (
    <div className="dashboard-page animate-fade-up">
      <header className="page-header">
        <h1 className="neon-gradient-text">What's worth looking at today?</h1>
        <p className="subtitle">Real-time market signals powered by SignalStack's 6-agent AI engine.</p>
        <div className="hero-search">
          <TickerSearch />
        </div>
      </header>

      <section className="trending-section">
        <div className="section-header">
          <h2><Zap size={18} style={{ display: 'inline', marginRight: 8, color: 'var(--warning)' }} />Trending Now</h2>
          <p className="small">Top opportunities ranked by confidence score from our multi-agent swarm.</p>
        </div>

        {loading ? (
          <Loader message="Scanning NSE for setups..." />
        ) : (
          <div className="opportunities-grid">
            {trending.length > 0 ? (
              trending.map((opp, i) => (
                <div key={opp.ticker} className={`animate-fade-up stagger-${i + 1}`}>
                  <OpportunityCard opportunity={opp} />
                </div>
              ))
            ) : (
              <div className="empty-state glass-card">
                <p>No trending opportunities yet. Start by searching for a ticker above!</p>
              </div>
            )}
          </div>
        )}
      </section>
    </div>
  );
};

export default Dashboard;
