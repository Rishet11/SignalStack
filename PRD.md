# PRD: SignalStack

**Working Title:** SignalStack  
**Track:** PS6 — AI for the Indian Investor  
**Positioning:** AI opportunity radar that detects high-conviction market setups from public data, explains why they matter, and warns when timing is behaviorally bad.

---

## 1. Product Summary
SignalStack is a GenAI-powered decision intelligence system for retail investors. It ingests public market signals such as corporate filings, bulk/block deals, insider activity, earnings commentary, price/volume patterns, and news. It converts these into ranked opportunity cards with source citations, confidence scores, and plain-English reasoning. A behavioral layer warns users when they are entering a trade too late or for the wrong reason.

**This is not a chatbot. It is a multi-agent signal engine with a reasoning layer.**

## 2. Problem Statement
Retail investors in India often react to tips, headlines, and price spikes without structured evidence. PS6 explicitly wants an intelligence layer that surfaces missed opportunities and detects technical patterns with historical success rates, not just summaries.

**The current gap is:**
*   Useful signals are scattered across public sources.
*   Most tools are either screeners or news aggregators.
*   Retail users do not get a clean “why this matters now” explanation.
*   Users also need timing discipline, not just stock picks.

## 3. Product Goal
Help a user answer:
*   “What is worth looking at today?”
*   “Why does this setup matter?”
*   “Is the current entry moment good or stupid?”

## 4. Target Users
### Primary
*   Indian retail investors.
*   Students and beginners trying to learn market interpretation.
*   Self-directed investors who read headlines but lack structured analysis.

### Secondary
*   Finance content creators.
*   Small research teams.
*   Hackathon judges evaluating GenAI and financial intelligence.

## 5. Core Value Proposition
SignalStack turns messy public market data into:
1.  **Ranked opportunities.**
2.  **Evidence-backed explanations.**
3.  **Behavioral timing warnings.**

The differentiator is not prediction. It is **cross-signal conviction with interpretability.**

---

## 6. Product Scope

### In Scope for MVP
*   **Ticker Search:** Support for single ticker or daily universe exploration.
*   **Public Data Ingestion:**
    *   Price/Volume data.
    *   Corporate announcements / filings.
    *   Bulk/Block deals & Insider trades (public sources).
    *   News headlines and articles.
*   **Technical Signal Detection:** Breakouts, reversals, support/resistance proximity, unusual volume.
*   **Event Signal Detection:** Earnings beat/miss, management commentary shifts, promoter activity.
*   **GenAI Synthesis:** Explain "why", provide source-backed rationale.
*   **Behavioral Layer:** Detect FOMO/late-entry, show caution cards for poor timing.
*   **Ranked Output:** Opportunity cards with citations.

### Out of Scope for MVP
*   Broker integration / Order placement.
*   Portfolio rebalancing.
*   Personalized investment advisory.
*   Long-horizon forecasting.

---

## 7. User Journey

### Primary Flow
1.  User opens app.
2.  User searches a ticker or chooses from daily ranked opportunities.
3.  System shows: Signal summary, confidence score, evidence sources, and historical pattern matches.
4.  User clicks “Why is this flagged?” → System shows structured reasoning.
5.  If setup is extended, the **Behavioral Layer** displays a warning (e.g., "Late entry pattern", "Historical reversal rate").

---

## 8. Functional Requirements (FR)
*   **FR1 — Ticker Normalization:** Map aliases, company names, and support NSE naming conventions.
*   **FR2 — Signal Ingestion:** Collect, deduplicate, timestamp, and cache market/event data.
*   **FR3 — Signal Scoring:** Unified score from momentum, volume, event strength, sentiment, and historical similarity.
*   **FR4 — Evidence Retrieval:** Show source links, snippets, filing excerpts, and credibility tags.
*   **FR5 — Opportunity Cards:** Ticker, signal type, confidence, evidence, historical analogs, and action suggestions.
*   **FR6 — Behavioral Layer:** Detect patterns like FOMO, breakout chasing, and momentum exhaustion.
*   **FR7 — Historical Backtest Display:** Show match counts and reversal probabilities for setup classes.
*   **FR8 — Audit Trail:** Log data sources, intermediate scores, agent outputs, and final synthesis.

---

## 9. Agent Architecture
SignalStack uses a modular multi-agent system:

1.  **Agent 1: Data Ingestion Agent** — Fetches price/volume, filings, deals, news; normalizes and caches.
2.  **Agent 2: Signal Detection Agent** — Computes technical indicators (Z-score, breakouts, volume spikes).
3.  **Agent 3: Context Intelligence Agent** — Summarizes catalysts, extracts sentiment/credibility from news/filings.
4.  **Agent 4: Historical Pattern Agent** — Finds analogs and computes outcome statistics (reversal probability).
5.  **Agent 5: Behavioral Risk Agent** — Classifies late-entry/FOMO risk and provides timing recommendations.
6.  **Agent 6: Synthesis Agent** — Combines all outputs into the final scannable opportunity card.

---

## 10. Scoring Model (Weighted)
*   **Technical Breakout Strength:** 30%
*   **Event/Catalyst Quality:** 25%
*   **News/Context Credibility:** 15%
*   **Historical Analog Confidence:** 20%
*   **Behavioral Risk Adjustment:** 10%

---

## 11. Data Sources
*   Market price/volume libraries (publicly accessible).
*   Public announcements and filings (NSE/BSE).
*   News feeds / RSS.
*   Corporate result PDFs.
*   Historical price data for backtesting.

---

## 12. UX Requirements
*   **Screen 1: Search/Watchlist** — Ticker search, trending opportunities.
*   **Screen 2: Opportunity Cards** — Scannable cards with scores and warning badges.
*   **Screen 3: Detail View** — Chart snippets, evidence sources, analogs, and behavioral warnings.
*   **Screen 4: Audit Trail** — Developer/Judge view showing agent steps and source traces.

---

## 13. Build Plan
1.  **Phase 1: Product Skeleton** — Scaffold frontend/backend, define schemas.
2.  **Phase 2: Data Pipeline** — Implement ingestion and reliable fallbacks.
3.  **Phase 3: Signal Logic** — Build technical scoring and historical matcher.
4.  **Phase 4: GenAI Layer** — Implement synthesis prompts for structured JSON.
5.  **Phase 5: Behavioral Layer** — Add late-entry classifier.
6.  **Phase 6: UI Polish** — Render cards, citations, and audit trail.
7.  **Phase 7: Demo Hardening** — Preload cases, tune latency.

---

## 14. Success Metrics
*   3+ clean opportunity cards generated end-to-end.
*   1+ behavioral warning triggered correctly.
*   3+ evidence sources cited per card.
*   Demo latency < 15 seconds.
*   Clear audit trail for validation.
