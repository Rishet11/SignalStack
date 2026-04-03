"""
LLM Factory — Centralizes model initialization for SignalStack agents.
Supports Gemini (default) and Gemma 4 (via Google AI Studio cloud API).
"""
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from ..config import logger

# Model routing — set SIGNAL_MODEL in .env to switch
# Options:
#   gemini-2.0-flash          (fast, free tier)
#   gemini-1.5-flash          (fast, free tier)
#   gemma-4-27b-it-gai        (Gemma 4 31B via AI Studio — most capable)
#   gemma-4-E4B-it            (Gemma 4 E4B via AI Studio — fast)
SIGNAL_MODEL = os.getenv("SIGNAL_MODEL", "gemma-4-27b-it-gai")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemma 4 recommended sampling parameters (per official docs)
GEMMA4_CONFIG = {
    "temperature": 1.0,
    "top_p": 0.95,
    "top_k": 64,
}

# Gemini fast config
GEMINI_CONFIG = {
    "temperature": 0.7,
    "top_p": 0.9,
}

def get_llm(thinking: bool = False) -> ChatGoogleGenerativeAI:
    """
    Returns a configured LLM instance.
    
    Args:
        thinking: If True and using Gemma 4, enables Thinking Mode
                  for deeper step-by-step reasoning.
    
    Returns:
        ChatGoogleGenerativeAI instance.
    """
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set. Please configure your .env file.")

    is_gemma = SIGNAL_MODEL.startswith("gemma")
    
    model_kwargs = {}
    if is_gemma:
        logger.info(f"[LLM Factory] Using Gemma 4 cloud model: {SIGNAL_MODEL}")
        model_kwargs = GEMMA4_CONFIG.copy()
        
        # Gemma 4 native Thinking Mode is enabled via extra body param
        # when supported by the endpoint
        if thinking:
            model_kwargs["thinking_mode"] = "enabled"
    else:
        logger.info(f"[LLM Factory] Using Gemini model: {SIGNAL_MODEL}")
        model_kwargs = GEMINI_CONFIG.copy()

    llm = ChatGoogleGenerativeAI(
        model=SIGNAL_MODEL,
        google_api_key=GEMINI_API_KEY,
        **model_kwargs,
    )
    
    return llm


def get_system_prompt(base_instruction: str, enable_thinking: bool = False) -> str:
    """
    Wraps a system prompt with Gemma 4's native thinking trigger token
    if thinking mode is enabled.
    
    Gemma 4 uses <|think|> at the start of the system prompt to trigger
    step-by-step internal reasoning before the final answer.
    """
    is_gemma = SIGNAL_MODEL.startswith("gemma")
    if is_gemma and enable_thinking:
        return f"<|think|>\n{base_instruction}"
    return base_instruction
