from typing import Literal
from langgraph.graph import StateGraph, START, END
from .state import SignalState
from .data_ingestion import data_ingestion_node
from .signal_detection import signal_detection_node
from .context_intel import context_intel_node
from .historical_pattern import historical_pattern_node
from .behavioral_risk import behavioral_risk_node
from .synthesis import synthesis_node

def create_signal_graph():
    """Create and compile the LangGraph workflow for SignalStack."""
    
    # 1. Initialize StateGraph
    workflow = StateGraph(SignalState)
    
    # 2. Add nodes
    workflow.add_node("data_ingestion", data_ingestion_node)
    workflow.add_node("signal_detection", signal_detection_node)
    workflow.add_node("context_intel", context_intel_node)
    workflow.add_node("historical_pattern", historical_pattern_node)
    workflow.add_node("behavioral_risk", behavioral_risk_node)
    workflow.add_node("synthesis", synthesis_node)
    
    # 3. Add edges (define the flow)
    # START → data_ingestion
    workflow.add_edge(START, "data_ingestion")
    
    # Parallel: [signal_detection, context_intel] (independent)
    workflow.add_edge("data_ingestion", "signal_detection")
    workflow.add_edge("data_ingestion", "context_intel")
    
    # Both lead to historical_pattern
    workflow.add_edge("signal_detection", "historical_pattern")
    workflow.add_edge("context_intel", "historical_pattern")
    
    # Sequential: historical_pattern → behavioral_risk → synthesis → END
    workflow.add_edge("historical_pattern", "behavioral_risk")
    workflow.add_edge("behavioral_risk", "synthesis")
    workflow.add_edge("synthesis", END)
    
    # 4. Compile the graph
    app = workflow.compile()
    return app

# Main entry point for starting an analysis
async def run_signal_analysis(ticker: str, request_id: str):
    """Run the graph for the given ticker."""
    graph = create_signal_graph()
    
    initial_state = {
        "ticker": ticker,
        "request_id": request_id,
        "ticker_info": None,
        "price_data": None,
        "news_items": [],
        "technical_signals": [],
        "context_summary": None,
        "sentiment_score": 0.0,
        "historical_analogs": [],
        "behavioral_risks": [],
        "opportunity_card": None,
        "audit_entries": [],
        "errors": [],
        "current_step": "start"
    }
    
    final_state = await graph.ainvoke(initial_state)
    return final_state
