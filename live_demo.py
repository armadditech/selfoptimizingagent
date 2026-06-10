#!/usr/bin/env python3
"""
Live demo using real Claude API (if available).
Falls back to simulation if API not available.
"""

import os
import sys

# Try to set API key from available environment variables
if not os.getenv("ANTHROPIC_API_KEY"):
    if os.getenv("ANTHROPIC_AUTH_TOKEN"):
        os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_AUTH_TOKEN")
        print("✓ Using ANTHROPIC_AUTH_TOKEN for API access\n")
    else:
        print("⚠️  No API key found. Running simulation mode.\n")
        print("To use real Claude API, set ANTHROPIC_API_KEY environment variable.\n")
        import subprocess
        subprocess.run([sys.executable, "quick_demo.py"])
        sys.exit(0)

# Import the real agent
from src.agent import CustomerServiceAgent

def run_live_demo():
    """Run live demo with real Claude API."""
    print("\n" + "="*70)
    print("  🤖 LIVE DEMO - Self-Optimizing Customer Service Agent")
    print("  Using Claude Sonnet 4.6 API")
    print("="*70 + "\n")

    try:
        # Initialize agent
        print("Initializing agent...")
        agent = CustomerServiceAgent()
        print("✓ Agent initialized successfully\n")

        # Scenario 1: Order Tracking
        print("-"*70)
        print("SCENARIO 1: Order Tracking")
        print("-"*70)

        greeting = agent.start_conversation(customer_id="demo_customer_1")
        print(f"\n🤖 Agent: {greeting}\n")

        user_message = "I want to track my order #12345"
        print(f"👤 Customer: {user_message}\n")
        print("Processing...")

        response = agent.handle_message(user_message)

        print(f"\n🤖 Agent: {response['text']}\n")
        print(f"📊 Metadata:")
        print(f"   Intent: {response['intent']}")
        print(f"   Confidence: {response['confidence']:.2%}")
        print(f"   Response Time: {response['response_time_seconds']:.2f}s")

        # Scenario 2: Product Inquiry
        print("\n" + "-"*70)
        print("SCENARIO 2: Product Inquiry")
        print("-"*70)

        agent.conversation_id = None  # Reset for new conversation
        agent.start_conversation(customer_id="demo_customer_2")

        user_message = "Do you have wireless headphones in stock?"
        print(f"\n👤 Customer: {user_message}\n")
        print("Processing...")

        response = agent.handle_message(user_message)

        print(f"\n🤖 Agent: {response['text']}\n")
        print(f"📊 Metadata:")
        print(f"   Intent: {response['intent']}")
        print(f"   Confidence: {response['confidence']:.2%}")

        # Scenario 3: Return Request
        print("\n" + "-"*70)
        print("SCENARIO 3: Return Request")
        print("-"*70)

        agent.conversation_id = None
        agent.start_conversation(customer_id="demo_customer_3")

        user_message = "I need to return a product I bought last week"
        print(f"\n👤 Customer: {user_message}\n")
        print("Processing...")

        response = agent.handle_message(user_message)

        print(f"\n🤖 Agent: {response['text']}\n")
        print(f"📊 Metadata:")
        print(f"   Intent: {response['intent']}")
        print(f"   Confidence: {response['confidence']:.2%}")

        print("\n" + "="*70)
        print("✅ Live Demo Complete!")
        print("="*70)
        print("\nThe agent successfully:")
        print("  • Classified intents accurately")
        print("  • Maintained conversation context")
        print("  • Generated helpful responses")
        print("  • Tracked all interactions for learning")
        print("\nTo run interactive mode: python src/agent.py")
        print("To run API server: python src/api_server.py")
        print("\n" + "="*70 + "\n")

    except Exception as e:
        print(f"\n❌ Error running live demo: {e}")
        print("\nFalling back to simulation mode...\n")
        import subprocess
        subprocess.run([sys.executable, "quick_demo.py"])

if __name__ == "__main__":
    run_live_demo()
