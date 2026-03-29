import os
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ContextExtraction(BaseModel):
    identified_catalyst: str = Field(description="The primary news event or catalyst driving the price action.")
    catalyst_sentiment: str = Field(description="Must be 'Positive', 'Negative', or 'Neutral'.")
    verified_source: str = Field(description="The name of the source (e.g. 'Financial Times', 'NSE Filing', 'Rumor').")

def analyze_context(market_data: dict) -> dict:
    """
    Agent 3: Context Intelligence Agent (Live LLM Version)
    Qualitative. Uses LangChain to parse raw text and extract sentiment.
    Includes a graceful fallback for the live demo if the API Key is missing.
    """
    simulated_news = market_data.get("_simulated_news", None)
    simulated_source = market_data.get("_simulated_news_source", None)
    
    # Check if API Key exists
    api_key = os.environ.get("GOOGLE_API_KEY")
    
    if api_key and api_key != "your_gemini_key_here" and simulated_news:
        try:
            print("Attempting LIVE GENAI CONTEXT EXTRACTION...")
            # LIVE GENAI EXTRACTION
            from langchain_google_genai import ChatGoogleGenerativeAI
            
            print("Imports successful. Initializing model...")
            llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
            extractor = llm.with_structured_output(ContextExtraction)
            
            prompt = f"Analyze this market event: '{simulated_news}' sourced from '{simulated_source}'. Extract the core catalyst and its sentiment."
            result = extractor.invoke(prompt)
            return result.model_dump()
            
        except Exception as e:
            print(f"GenAI Context Fallback Triggered: {e}")
            pass # Fall through to deterministic logic
            
    # DETERMINISTIC FALLBACK (Guarantees the demo never crashes)
    if simulated_news:
        return {
            "identified_catalyst": simulated_news,
            "catalyst_sentiment": "Negative" if "crash" in simulated_news.lower() or "misses" in simulated_news.lower() else "Positive",
            "verified_source": simulated_source
        }
    else:
        return {
            "identified_catalyst": f"Routine trading activity for {market_data.get('ticker', 'Unknown')}.",
            "catalyst_sentiment": "Neutral",
            "verified_source": "General Market Data"
        }
