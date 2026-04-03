import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { auditApi } from '../services/api';
import type { AuditTrail as AuditTrailType } from '../types';
import { Loader } from '../components/Common';
import { CheckCircle2, XCircle, Clock, Zap, Search, BarChart3, History, BrainCircuit, Sparkles } from 'lucide-react';

const AgentIcon = ({ name }: { name: string }) => {
  switch (name) {
    case 'data_ingestion': return <Search size={18} />;
    case 'signal_detection': return <BarChart3 size={18} />;
    case 'context_intel': return <BrainCircuit size={18} />;
    case 'historical_pattern': return <History size={18} />;
    case 'behavioral_risk': return <Zap size={18} />;
    case 'synthesis': return <Sparkles size={18} />;
    default: return <Clock size={14} />;
  }
};

const AuditTrail: React.FC = () => {
  const { requestId } = useParams<{ requestId: string }>();
  const [trail, setTrail] = useState<AuditTrailType | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!requestId) return;
    const fetchTrail = async () => {
      try {
        const data = await auditApi.getTrail(requestId);
        setTrail(data);
      } catch (err) {
        console.error("Failed to fetch audit trail:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchTrail();
  }, [requestId]);

  if (loading) return <Loader message="Retrieving agent trace..." />;
  if (!trail) return <div className="error-state">Audit trail not found.</div>;

  return (
    <div className="audit-trail-page">
      <header className="page-header">
        <h1>Agent Execution Audit</h1>
        <p>Request ID: <code className="request-id">{requestId}</code> • Ticker: <strong>{trail.ticker}</strong></p>
      </header>

      <div className="timeline">
        {trail.entries.map((entry, i) => (
          <div key={i} className={`timeline-item ${entry.status} animate-fade-in`} style={{ animationDelay: `${i * 100}ms` }}>
            <div className="agent-indicator">
               <div className="icon-wrapper">
                  <AgentIcon name={entry.agent_name} />
               </div>
               {i < trail.entries.length - 1 && <div className="node-line"></div>}
            </div>
            
            <div className="glass-card agent-card">
              <div className="card-header">
                <div className="agent-info">
                   <h3>{entry.agent_name.replace('_', ' ').toUpperCase()}</h3>
                   <span className="duration">{entry.duration_ms}ms</span>
                </div>
                {entry.status === 'success' ? (
                  <CheckCircle2 color="#10b981" size={20} />
                ) : (
                  <XCircle color="#ef4444" size={20} />
                )}
              </div>
              
              <div className="card-details">
                 <div className="detail-section">
                    <label>Input Summary</label>
                    <p>{entry.input_state_summary}</p>
                 </div>
                 <div className="detail-section">
                    <label>Output Result</label>
                    <p>{entry.output_state_summary}</p>
                 </div>
                 {entry.llm_prompt_snippet && (
                    <div className="detail-section prompt">
                       <label>Prompt Snippet</label>
                       <code>{entry.llm_prompt_snippet}</code>
                    </div>
                 )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AuditTrail;
