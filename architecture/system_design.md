# SignalStack Architecture

## 1. System Design
SignalStack operates as a modular, multi-agent pipeline designed to ingest, process, and synthesize unstructured market data into structured, evidence-backed "Opportunity Cards."

### The 6-Agent System Flow
1. **Data Ingestion Agent**
   - **Role:** The foundation layer. Connects to live APIs (e.g., Yahoo Finance) and reads stored mock data specifically required for edge-case testing (historical anomalies).
   - **Objective:** Normalize raw HTML/JSON into a structured `MarketSnapshot` schema.

2. **Signal Detection Agent**
   - **Role:** Quantitative analysis.
   - **Objective:** Computes Z-scores for volume spikes, identifies moving average breakouts, and flags raw momentum without context.

3. **Context Intelligence Agent**
   - **Role:** Qualitative analysis.
   - **Objective:** Parses news headlines and corporate filings to extract sentiment, identifying the underlying "catalyst" for a technical movement.

4. **Historical Pattern Agent**
   - **Role:** Validation layer.
   - **Objective:** Compares current setups to historical analogs (e.g., "How often has this stock reversed after an earnings miss accompanied by a 3x volume spike?").

5. **Behavioral Risk Agent**
   - **Role:** Guardrail layer. The core differentiator of the project.
   - **Objective:** Assesses whether the setup screams "FOMO" or "Late Entry" based on extreme momentum deviations.

6. **Synthesis Agent**
   - **Role:** Output generation.
   - **Objective:** Combines outputs from Agents 1-5 to produce the final `OpportunityCard` JSON. Employs "Citation Enforcement" to ensure all claims trace back directly to data collected by Agent 1.

## 2. Pydantic Schemas (Anti-Hallucination)
To prevent the LLM from making up financial data, the backend strictly enforces Pydantic models. The AI cannot respond with raw text; it must output JSON matching the predefined schema, consisting of explicit enum categories and required array structures for sources.

## 3. Technology Stack
*   **Frontend:** Next.js (React) leveraging App Router for rapid component rendering and a premium user experience. Custom UI components built with Tailwind CSS.
*   **Backend:** Python 3 (FastAPI) acting as the orchestration layer for the multi-agent pipeline. 
*   **AI Integration:** LangChain / raw API schemas targeting secure, deterministic LLM outputs.
