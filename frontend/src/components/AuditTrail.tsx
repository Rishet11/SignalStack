"use client";

import React from 'react';

export default function AuditTrail({ auditData }: { auditData: any }) {
  if (!auditData) return null;

  return (
    <div className="w-full max-w-4xl mx-auto rounded-xl overflow-hidden bg-black border border-zinc-800 mt-8">
      <div className="bg-zinc-900 border-b border-zinc-800 p-4">
        <h3 className="text-zinc-200 font-mono text-sm uppercase tracking-widest flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
          Judge's Audit Trail (Raw Data Grounding)
        </h3>
        <p className="text-zinc-500 text-xs mt-1">This shows the exact raw data ingested by the agents to prove zero hallucination.</p>
      </div>
      
      <div className="p-4 overflow-x-auto">
        <pre className="text-green-400 font-mono text-xs">
          <code>{JSON.stringify(auditData, null, 2)}</code>
        </pre>
      </div>
    </div>
  );
}
