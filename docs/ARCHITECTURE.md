# SignalStack Architecture

Use this file as the source for the hackathon architecture diagram.

## Core Flow

1. Frontend React app calls FastAPI endpoints under `/api`.
2. FastAPI resolves tickers, loads cached cards, and triggers on-demand analysis.
3. LangGraph coordinates the six-agent pipeline:
   - data ingestion
   - signal detection
   - context intel
   - historical pattern matching
   - behavioral risk analysis
   - synthesis
4. Market data comes from `yfinance`; news comes from NewsData.io and RSS fallbacks.
5. Analysis outputs and audit entries are stored in SQLite for replay in the UI.

## Diagram Nodes

- React/Vite frontend
- FastAPI backend
- LangGraph agent workflow
- Gemini/Gemma model endpoint
- Market/news providers
- SQLite cache and audit store

## Diagram Edges

- Frontend -> FastAPI: search, opportunities, ticker chart, analysis, audit trail
- FastAPI -> SQLite: cached cards and audit logs
- FastAPI -> LangGraph: analysis execution
- LangGraph -> Data providers: market and news fetches
- LangGraph -> LLM: structured reasoning and synthesis

## Demo Narrative

- Dashboard shows preloaded cached opportunities for instant first paint.
- Ticker detail loads chart data and can trigger fresh analysis.
- Completed analyses expose an audit trail through the returned `request_id`.
