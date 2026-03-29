"use client";

import { useState } from 'react';
import OpportunityCard from '@/components/OpportunityCard';
import AuditTrail from '@/components/AuditTrail';
import { Search, Loader2, Zap } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function Home() {
  const [ticker, setTicker] = useState('RELIANCE.NS');
  const [demoMode, setDemoMode] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState('');

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    setResult(null);

    try {
      const payload = {
        ticker: ticker.toUpperCase(),
        use_mock: demoMode,
        mock_scenario_name: 'fomo_breakout' // Hardcoded demo trigger for the pitch
      };

      const res = await fetch('http://localhost:8000/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
      });

      if (!res.ok) {
        throw new Error("Failed to fetch from SignalStack engine.");
      }

      const data = await res.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message || 'An unknown error occurred.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-black text-white selection:bg-blue-500/30 font-sans pb-24">
      {/* Premium Header */}
      <div className="absolute top-0 w-full h-96 bg-gradient-to-b from-blue-900/20 via-black to-black border-b border-zinc-900 z-0" />
      
      <div className="relative z-10 max-w-6xl mx-auto pt-20 px-6">
        <header className="mb-16 text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-bold tracking-widest uppercase mb-6">
            <Zap className="w-3 h-3" /> SignalStack AI
          </div>
          <h1 className="text-5xl md:text-7xl font-black tracking-tighter mb-4">
            Find the Signal.<br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-600">
              Ignore the Noise.
            </span>
          </h1>
          <p className="text-xl text-zinc-400 max-w-2xl mx-auto font-light leading-relaxed">
            The opportunity radar that detects high-conviction market setups and stops you from buying the top.
          </p>
        </header>

        {/* Search Interface */}
        <form onSubmit={handleSearch} className="max-w-2xl mx-auto mb-16 relative">
          <div className="relative flex items-center">
            <Search className="absolute left-6 text-zinc-500 w-6 h-6" />
            <input 
              type="text"
              value={ticker}
              onChange={(e) => setTicker(e.target.value)}
              placeholder="Enter NSE Ticker (e.g., RELIANCE.NS)"
              className="w-full bg-zinc-900 border border-zinc-800 rounded-full py-5 pl-16 pr-36 text-lg text-white font-mono focus:outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/50 transition-all shadow-2xl"
            />
            <button 
              type="submit"
              disabled={isLoading}
              className="absolute right-2 bg-white text-black font-bold rounded-full px-6 py-3 hover:bg-zinc-200 transition-colors disabled:opacity-50 flex items-center gap-2"
            >
              {isLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : "Analyze"}
            </button>
          </div>
          
          <div className="mt-4 flex justify-center items-center gap-2 text-sm text-zinc-500">
            <input 
              type="checkbox" 
              id="demoMode" 
              checked={demoMode} 
              onChange={(e) => setDemoMode(e.target.checked)}
              className="rounded bg-zinc-800 border-zinc-700 text-blue-500 focus:ring-blue-500 focus:ring-offset-black"
            />
            <label htmlFor="demoMode" className="cursor-pointer hover:text-zinc-300 transition-colors">
              Enable Pitch Demo Mode (Inject FOMO Breakout Scenario)
            </label>
          </div>
        </form>

        {/* Error State */}
        {error && (
          <div className="max-w-4xl mx-auto mb-8 p-4 border border-red-500/50 bg-red-500/10 text-red-400 rounded-lg text-center">
            {error}
          </div>
        )}

        {/* Dynamic Results Area */}
        <AnimatePresence mode="wait">
          {result && (
            <motion.div
              key="results"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95 }}
              transition={{ duration: 0.5, ease: "easeOut" }}
              className="space-y-12"
            >
              <OpportunityCard cardData={result.card} />
              <AuditTrail auditData={result.audit_trail} />
            </motion.div>
          )}
        </AnimatePresence>

      </div>
    </main>
  );
}
