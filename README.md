# 🚀 SignalStack: GenAI Market Signal Engine

**SignalStack** is a production-quality, multi-agent engine designed to detect high-conviction market opportunities in the Indian stock market (NSE). It bypasses traditional "dumb" screeners by using a 6-agent LangGraph swarm to synthesize technicals, news context, historical analogs, and behavioral risks into actionable opportunity cards.

---

## 🌟 Features

- **6-Agent Pipeline**: 
    - 🛰️ **Data Ingestion**: Real-time NSE data + multi-source news scraping.
    - 📈 **Signal Detection**: Advanced technical indicator & pattern recognition.
    - 🧠 **Context Intel**: LLM-powered news sentiment & catalyst analysis.
    - 🕒 **Historical Analogs**: Matches current setups with past market behavior.
    - ⚠️ **Behavioral Risk**: Detects FOMO, over-extension, and crowded trades.
    - 🃏 **Synthesis**: Generates lead-gen ready opportunity cards with evidence.
- **Premium Dashboard**: Glassmorphic UI with real-time confidence gauges and trending setups.
- **Deep Dive View**: Interactive **TradingView** charts with signal overlays and thesis breakdown.
- **Transparency First**: Full **Audit Trail** showing the reasoning trace of every agent in the swarm.
- **NSE Native**: Built-in support for top 200 NSE tickers with fuzzy search resolution.

---

## 🛠️ Tech Stack

- **Frontend**: React 19, TypeScript, Vite, CSS Modules (Premium Dark Theme).
- **Charts**: Lightweight Charts (TradingView).
- **Backend**: FastAPI (Python), LangGraph, Pydantic.
- **AI**: Google Gemini 2.0 Flash (Fast & Structured).
- **Data**: yfinance, pandas-ta, NewsData.io + RSS fallbacks.
- **Database**: SQLite (aiosqlite) with automated caching.

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10+
- Node.js 18+
- [Google Gemini API Key](https://aistudio.google.com/)

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
cp ../.env.example ../.env
python -m app.main
```

### 2a. Backend Smoke Test
Run this before the demo to verify the repo contains the expected demo assets and, when available, that the backend imports cleanly:

```bash
python backend/scripts/smoke_test.py
```

To check a running backend as well:

```bash
SIGNALSTACK_HEALTHCHECK_URL="http://localhost:8000/health" python backend/scripts/smoke_test.py
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

To point the frontend at a non-local backend, set `VITE_API_BASE_URL` before starting or building:

```bash
export VITE_API_BASE_URL="https://your-backend.example.com/api"
```

---

## 📊 Demo Hardening
The system comes pre-loaded with high-conviction setups for **RELIANCE** and **TCS** to demonstrate the 'zero-latency' user experience even without live API calls.

---

## 🏗️ Architecture
SignalStack uses a **Stateful Directed Acyclic Graph (DAG)** via LangGraph to ensure each agent contributes its specialized intelligence before the final synthesis. 

- **State Management**: Shared `SignalState` TypedDict.
- **Concurrency**: Parallel execution of technical and contextual analysis for reduced latency (<12s target).
- **Reliability**: Tiered fallbacks for news and market data sources.

---

*Built for the PS6 Hackathon — AI for the Indian Investor.*
