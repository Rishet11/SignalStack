import sys
import os
sys.path.append(os.path.dirname(__file__))
from ingestion.mock_injector import inject_demo_scenario
from agents.synthesis_agent import generate_opportunity_card
import json

if __name__ == "__main__":
    print("Testing Mock Scenario Integration...")
    raw_data = inject_demo_scenario("fomo_breakout")
    print("1. Ingestion Successful.")
    
    card = generate_opportunity_card(raw_data)
    print("2. Synthesis Successful.")
    
    print("\n--- FINAL OPPORTUNITY CARD ---")
    print(card.model_dump_json(indent=2))
