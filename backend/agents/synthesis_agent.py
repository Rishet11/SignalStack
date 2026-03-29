import os
import json
import sys
from schemas import OpportunityCard, BehavioralWarning, SignalSource
from agents.signal_agent import analyze_signals
from agents.context_agent import analyze_context
from agents.behavioral_agent import evaluate_behavioral_risk
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def generate_opportunity_card(market_data: dict) -> OpportunityCard:
    """
    Agent 6: Synthesis Agent (Live LLM Version)
    Orchestrates the inputs from Agents 1-5 and dynamically compiles them 
    using Gemini LangChain Structured Output.
    """
    
    # 1-3. Run intermediate logic
    sys_signals = analyze_signals(market_data)
    sys_context = analyze_context(market_data)
    sys_behavior = evaluate_behavioral_risk(market_data, sys_signals["quantitative_flags"], sys_context)
    
    ticker = market_data.get("ticker", "UNKNOWN")
    
    # Check for live GenAI Integration
    api_key = os.environ.get("GOOGLE_API_KEY")
    
    if api_key and api_key != "your_gemini_key_here":
        try:
            print("Attempting LIVE GENAI SYNTHESIS...")
            # LIVE GENAI SYNTHESIS
            from langchain_google_genai import ChatGoogleGenerativeAI
            from langchain_core.prompts import ChatPromptTemplate
            
            print("Imports successful. Initializing model...")
            llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.1)
            synthesizer = llm.with_structured_output(OpportunityCard)
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are an elite quantitative AI designed to output financial opportunity cards. You must conform exactly to the JSON schema. You must explicitly cite the provided data without hallucination."),
                ("user", "Analyze the following grounded data for {ticker}:\nQuantitative: {signals}\nQualitative: {context}\nBehavioral Risk: {behavior}\nCompile the final OpportunityCard.")
            ])
            
            chain = prompt | synthesizer
            
            # The LLM does the reasoning natively!
            result = chain.invoke({
                "ticker": ticker,
                "signals": json.dumps(sys_signals),
                "context": json.dumps(sys_context),
                "behavior": json.dumps(sys_behavior)
            })
            
            return result
        except Exception as e:
            print(f"GenAI Synthesis Fallback Triggered: {e}")
            pass # Fall through to deterministic

    # DETERMINISTIC FALLBACK (Guarantees the demo never crashes)
    signal_type = "Baseline Setup"
    if sys_behavior["is_fomo"]:
        signal_type = "Hype/FOMO Spike"
    elif "High Volume Breakout" in sys_signals["quantitative_flags"]:
        signal_type = "Volume Breakout"
    elif sys_behavior["is_late_entry"] and sys_context["catalyst_sentiment"] == "Negative":
        signal_type = "Panic Selloff"
        
    confidence_score = 50 + (20 if sys_context["catalyst_sentiment"] != "Neutral" else 0) + (15 if sys_signals["quantitative_flags"] != ["Stable / Routine Activity"] else 0) - (10 if sys_behavior["is_late_entry"] else 0)
    confidence_score = min(max(confidence_score, 0), 100)
    
    primary_reasoning = f"SignalStack detected a {signal_type} for {ticker} driven by {sys_context['identified_catalyst']}. Technical indicators show: {', '.join(sys_signals['quantitative_flags'])}."
    
    evidence = [SignalSource(source_name=sys_context["verified_source"], source_url="#", date_published=market_data.get("timestamp", ""), snippet=f"'{sys_context['identified_catalyst']}'")]
    
    behavior_card = None
    if sys_behavior["is_fomo"] or sys_behavior["is_late_entry"]:
        behavior_card = BehavioralWarning(is_fomo=sys_behavior["is_fomo"], is_late_entry=sys_behavior["is_late_entry"], warning_message=sys_behavior["warning_message"], historical_reversal_prob=sys_behavior["historical_reversal_prob"])

    return OpportunityCard(
        ticker=ticker, signal_type=signal_type, confidence_score=confidence_score,
        primary_reasoning=primary_reasoning, evidence_sources=evidence, behavioral_warning=behavior_card
    )
