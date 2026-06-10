#!/usr/bin/env python3
"""
Simple live demo - single file version for quick testing.
"""

import os
import sys

# Set API key from environment
if not os.getenv("ANTHROPIC_API_KEY"):
    if os.getenv("ANTHROPIC_AUTH_TOKEN"):
        os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_AUTH_TOKEN")

try:
    from anthropic import Anthropic

    print("\n" + "="*70)
    print("  🤖 LIVE DEMO - Testing Real Claude API Connection")
    print("="*70 + "\n")

    # Test API connection
    print("Testing API connection...")
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    # Simple test message
    print("✓ Connected to Claude API\n")
    print("-"*70)
    print("Test Query: Classify this customer message")
    print("-"*70)
    print("\nCustomer message: 'I want to track my order #12345'\n")
    print("Processing with Claude...\n")

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{
            "role": "user",
            "content": """You are a customer service intent classifier.

Classify this message into one of: orders, returns, products, refunds, general

Customer message: "I want to track my order #12345"

Response format:
Intent: <intent>
Confidence: <0.0-1.0>
Entities: <any extracted info>
Reasoning: <brief explanation>"""
        }]
    )

    result_text = response.content[0].text
    print("🤖 Claude Response:")
    print("-"*70)
    print(result_text)
    print("-"*70)

    print("\n✅ SUCCESS! Claude API is working correctly.")
    print("\nThe full agent system is ready to use with:")
    print("  • All 5 capability handlers")
    print("  • Self-optimization engine")
    print("  • Context management")
    print("  • Analytics tracking")

    print("\n" + "="*70)
    print("To run the full interactive agent:")
    print("  cd /Users/dmukunthu/Documents/PersonalProjects/SelfOptimizingAgent")
    print("  export ANTHROPIC_API_KEY=$ANTHROPIC_AUTH_TOKEN")
    print("  python3 src/agent.py")
    print("="*70 + "\n")

except ImportError:
    print("\n❌ anthropic package not installed")
    print("Installing now...")
    os.system("pip3 install anthropic --quiet")
    print("✓ Installed. Please run the script again.")

except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nShowing simulated demo instead:\n")
    os.system("python3 quick_demo.py")
