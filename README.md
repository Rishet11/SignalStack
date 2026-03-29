# SignalStack

**An AI-powered opportunity radar designed for the ET Gen AI Hackathon.**

SignalStack is a GenAI-powered decision intelligence system for retail investors. It ingests public market signals (corporate filings, bulk/block deals, insider activity, earnings commentary, price/volume patterns, and news) and converts them into ranked opportunity cards with source citations, confidence scores, and plain-English reasoning. 

A unique **Behavioral Layer** warns users when they are entering a trade too late or for the wrong reason.

**This is not a chatbot. It is a grounded multi-agent signal engine.**

## Project Structure
This repository contains two main applications:
1.  **Frontend (Next.js):** A modern, high-performance UI designed to render "Opportunity Cards" and a transparency-focused "Audit Trail."
2.  **Backend (Python/FastAPI):** A 6-agent orchestration pipeline that handles everything from data ingestion to LLM synthesis cleanly.

## Running Locally

### 1. Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
# Install requirements (once defined)
# pip install -r requirements.txt
# Run the FastAPI server
# uvicorn main:app --reload
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Navigate to `http://localhost:3000` to interact with the application.

## Architecture & Hackathon Deliverables
For our detailed system design and the required Multi-Agent Pipeline Mermaid diagram, refer to the documents inside the `/architecture` directory:
*   [System Design Documentation](architecture/system_design.md)
*   [Data Flow Mermaid Diagram](architecture/data_flow.md)
