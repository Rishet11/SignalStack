import React, { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { tickerApi, signalsApi } from '../services/api';
import type { TickerInfo, OpportunityCard, ChartPoint } from '../types';
import PriceChart from '../components/Charts/PriceChart';
import { Loader } from '../components/Common';
import { ShieldAlert, Info, Clock } from 'lucide-react';

const getAuditKey = (ticker: string) => `signalstack:last-audit:${ticker.toUpperCase()}`;

const TickerDetail: React.FC = () => {
  const { symbol } = useParams<{ symbol: string }>();
  const [tickerInfo, setTickerInfo] = useState<TickerInfo | null>(null);
  const [card, setCard] = useState<OpportunityCard | null>(null);
  const [chartData, setChartData] = useState<ChartPoint[]>([]);
  const [requestId, setRequestId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);

  useEffect(() => {
    if (!symbol) return;
    const normalizedSymbol = symbol.toUpperCase();
    
    const fetchData = async () => {
      try {
        const [info, chart] = await Promise.all([
          tickerApi.getInfo(normalizedSymbol),
          tickerApi.getChartData(normalizedSymbol)
        ]);
        setTickerInfo(info);
        setChartData(chart);
        setRequestId(localStorage.getItem(getAuditKey(normalizedSymbol)));
        
        // Try to fetch existing card
        const opps = await signalsApi.getOpportunities();
        const existing = opps.find(o => o.ticker === normalizedSymbol);
        if (existing) setCard(existing);
      } catch (err) {
        console.error("Failed to fetch ticker data:", err);
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, [symbol]);

  const handleAnalyze = async () => {
     if (!symbol) return;
     setAnalyzing(true);
     try {
       const normalizedSymbol = symbol.toUpperCase();
       const result = await signalsApi.analyzeTicker(normalizedSymbol);
       setCard(result.opportunity_card);
       setRequestId(result.request_id);
       localStorage.setItem(getAuditKey(normalizedSymbol), result.request_id);
     } catch (err) {
       console.error("Analysis failed:", err);
     } finally {
       setAnalyzing(false);
     }
  };

  if (loading) return <Loader message={`Loading ${symbol}...`} />;

  return (
    <div className="ticker-detail-page">
      <header className="detail-header">
        <div className="ticker-meta">
          <h1>{tickerInfo?.symbol}</h1>
          <p>{tickerInfo?.name} • {tickerInfo?.sector} • {tickerInfo?.exchange}</p>
        </div>
        {!card && !analyzing && (
           <button onClick={handleAnalyze} className="btn-primary">Analyze Setup</button>
        )}
        {analyzing && <Loader message="Running Agent Swarm..." />}
      </header>

      <div className="detail-grid">
        <div className="left-column">
          <div className="glass-card chart-card">
             <div className="card-title">Technical View</div>
             <PriceChart data={chartData} />
          </div>

          <div className="glass-card info-card">
              <div className="card-title">Thesis & Reasoning</div>
              {card ? (
                <div className="thesis-content">
                   <h2 className="neon-gradient-text">{card.thesis}</h2>
                   <p className="detailed-reasoning">{card.detailed_reasoning}</p>
                   <div className="action-suggestion">
                      <strong>Action Suggestion:</strong> {card.action_suggestion}
                   </div>
                </div>
              ) : (
                <p className="hint">Run the agent swarm to generate a synthesis.</p>
              )}
          </div>
        </div>

        <div className="right-column">
          {card && (
             <>
               <div className="glass-card score-card">
                  <div className="score-main">{card.confidence_score}%</div>
                  <div className="label">Confidence Score</div>
               </div>

               {card.behavioral_warning && (
                  <div className={`glass-card risk-card ${card.behavioral_warning.severity}`}>
                     <div className="card-title"><ShieldAlert size={18} /> Timing Warning</div>
                     <p>{card.behavioral_warning.risk_type}</p>
                     <p className="small">{card.behavioral_warning.explanation}</p>
                  </div>
               )}

               <div className="glass-card evidence-card">
                  <div className="card-title"><Info size={18} /> Key Evidence</div>
                  <ul className="evidence-list">
                     {card.evidence_sources.map((source, i) => (
                        <li key={i}>
                           <div className="source-tag">{source.source_type}</div>
                           <p className="small">{source.snippet}</p>
                        </li>
                     ))}
                  </ul>
               </div>

               {requestId && (
                  <Link to={`/audit/${requestId}`} className="link-audit">
                     <Clock size={16} />
                     <span>View agent trace</span>
                  </Link>
               )}
             </>
          )}
        </div>
      </div>
    </div>
  );
};

export default TickerDetail;
