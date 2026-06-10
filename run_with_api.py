#!/usr/bin/env python3
"""
Run the agent with your Anthropic credentials.
"""

import os
import sys

# Use your Anthropic auth token
os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_AUTH_TOKEN", "")
base_url = os.getenv("ANTHROPIC_BASE_URL")
if base_url:
    os.environ["ANTHROPIC_BASE_URL"] = base_url

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("\n" + "="*70)
print("  🤖 LIVE AGENT - Using Your Anthropic Account")
print("="*70 + "\n")

try:
    # Import and run
    from anthropic import Anthropic

    print("✓ Anthropic SDK imported")
    print("✓ Using your auth token")
    if base_url:
        print(f"✓ Using base URL: {base_url[:50]}...")

    # Quick API test
    print("\n" + "-"*70)
    print("Testing API Connection...")
    print("-"*70 + "\n")

    client = Anthropic(
        api_key=os.environ["ANTHROPIC_API_KEY"],
        base_url=base_url if base_url else None
    )

    # Test with a simple query
    print("Sending test query to Claude...\n")

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        messages=[{
            "role": "user",
            "content": "You are a customer service intent classifier. Classify this message: 'Track my order #12345'. Respond with just: Intent: <intent>, Confidence: <0-1>"
        }]
    )

    result = response.content[0].text

    print("✅ API Connection Successful!")
    print("\nClaude Response:")
    print("-"*70)
    print(result)
    print("-"*70)

    print("\n" + "="*70)
    print("Your agent is ready to use!")
    print("="*70)

    print("\n🎯 Now let's test the full agent system:\n")

    # Now run a real agent test
    from src.core.llm_client import LLMClient
    from src.core.intent_router import IntentRouter

    print("Initializing agent components...")

    # Create minimal config
    config = {
        "llm": {
            "api_key": os.environ["ANTHROPIC_API_KEY"],
            "model": "claude-sonnet-4-6",
            "max_tokens": 1000,
            "enable_caching": True,
            "base_url": base_url if base_url else None
        },
        "capabilities": {
            "orders": {"enabled": True},
            "returns": {"enabled": True},
            "products": {"enabled": True},
            "refunds": {"enabled": True},
            "general": {"enabled": True}
        }
    }

    llm_client = LLMClient(config["llm"])
    intent_router = IntentRouter(llm_client, config)

    print("✓ LLM Client initialized")
    print("✓ Intent Router initialized")

    # Test intent classification
    print("\n" + "-"*70)
    print("TEST: Intent Classification with Real Agent")
    print("-"*70)

    test_message = "I want to track my order #12345"
    print(f"\nCustomer message: '{test_message}'")
    print("\nClassifying intent...")

    result = intent_router.classify_intent(test_message, {})

    print("\n✅ Classification Result:")
    print(f"   Intent: {result['intent']}")
    print(f"   Confidence: {result['confidence']:.2%}")
    print(f"   Entities: {result.get('entities', {})}")
    print(f"   Reasoning: {result.get('reasoning', 'N/A')}")

    print("\n" + "="*70)
    print("🎉 SUCCESS! Your agent is working with Claude API!")
    print("="*70)

    print("\n📚 Next steps:")
    print("  1. Run full interactive mode:")
    print("     export ANTHROPIC_API_KEY=$ANTHROPIC_AUTH_TOKEN")
    print("     python src/agent.py")
    print("\n  2. Or run API server:")
    print("     python src/api_server.py")
    print("\n  3. Customize for your business:")
    print("     Edit config/config.json")

    print("\n" + "="*70 + "\n")

except ImportError as e:
    print(f"\n❌ Import Error: {e}")
    print("\nInstalling anthropic package...")
    os.system("pip3 install --user anthropic")
    print("\n✓ Installed. Please run this script again.")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    print("\nFull error:")
    traceback.print_exc()
    print("\nNote: If you see authentication errors, the token might need refresh.")
