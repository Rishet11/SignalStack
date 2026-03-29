import React from 'react';
import { ShieldAlert, TrendingUp, TrendingDown, Clock, Search, ExternalLink } from 'lucide-react';
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

const getConfidenceColor = (score: number) => {
    if (score >= 80) return 'text-green-400';
    if (score >= 50) return 'text-yellow-400';
    return 'text-red-400';
};

export default function OpportunityCard({ cardData }: { cardData: any }) {
  if (!cardData) return null;

  const { ticker, signal_type, confidence_score, primary_reasoning, evidence_sources, behavioral_warning } = cardData;

  const isWarning = !!behavioral_warning;

  return (
    <div className="w-full max-w-4xl mx-auto rounded-2xl overflow-hidden shadow-2xl bg-zinc-900 border border-zinc-800 transition-all hover:border-zinc-700">
      
      {/* Heavy Warning Header specifically for the Hackathon Demo */}
      {isWarning && (
        <div className="bg-red-500/10 border-b border-red-500/20 p-4 flex items-start gap-3">
          <ShieldAlert className="w-6 h-6 text-red-500 flex-shrink-0 mt-1" />
          <div>
            <h3 className="text-red-500 font-bold text-lg uppercase tracking-wider">
              {behavioral_warning.is_fomo ? "High FOMO Warning Detected" : "Late Entry Warning"}
            </h3>
            <p className="text-red-200 mt-1">{behavioral_warning.warning_message}</p>
            <div className="mt-2 text-sm text-red-400 font-mono">
              Historical Reversal Prob: {behavioral_warning.historical_reversal_prob}%
            </div>
          </div>
        </div>
      )}

      {/* Main Content Area */}
      <div className="p-8">
        <div className="flex justify-between items-start mb-6">
          <div>
            <div className="text-sm text-zinc-400 uppercase tracking-widest font-semibold mb-1">Ticker / Setup</div>
            <h1 className="text-4xl font-extrabold text-white flex items-center gap-3">
              {ticker}
              <span className="text-xl font-medium px-3 py-1 rounded-full bg-zinc-800 text-zinc-300">
                {signal_type}
              </span>
            </h1>
          </div>
          
          <div className="text-right">
            <div className="text-sm text-zinc-400 uppercase tracking-widest font-semibold mb-1">Confidence</div>
            <div className={cn("text-5xl font-black font-mono tracking-tighter", getConfidenceColor(confidence_score))}>
              {confidence_score}<span className="text-2xl text-zinc-500">%</span>
            </div>
          </div>
        </div>

        {/* Reasoning */}
        <div className="mb-8">
          <h4 className="text-zinc-500 uppercase text-xs font-bold tracking-widest mb-2">AI Synthesis Reasoning</h4>
          <p className="text-xl text-zinc-300 leading-relaxed font-light">
            {primary_reasoning}
          </p>
        </div>

        {/* Evidence Sources */}
        <div>
          <h4 className="text-zinc-500 uppercase text-xs font-bold tracking-widest mb-3 flex items-center gap-2">
            <Search className="w-4 h-4" /> Hard Grounding Evidence
          </h4>
          <div className="space-y-3">
            {evidence_sources?.map((source: any, i: number) => (
              <div key={i} className="bg-zinc-800/50 rounded-lg p-4 border border-zinc-800/80">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-blue-400 font-medium font-mono text-sm">{source.source_name}</span>
                  <span className="text-zinc-500 text-xs flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    {new Date(source.date_published).toLocaleDateString()}
                  </span>
                </div>
                <blockquote className="border-l-2 border-zinc-700 pl-4 py-1 text-zinc-400 italic text-sm">
                  {source.snippet}
                </blockquote>
              </div>
            ))}
          </div>
        </div>
        
      </div>
    </div>
  );
}
