#!/usr/bin/env python3
"""Quick visual demo of the agent's capabilities."""

import time

def demo():
    print("\n" + "="*70)
    print("  🤖 SELF-OPTIMIZING CUSTOMER SERVICE AGENT - QUICK DEMO")
    print("="*70 + "\n")

    scenarios = [
        {
            "title": "1. ORDER TRACKING",
            "customer": "Track my order #12345",
            "intent": "orders",
            "confidence": 0.95,
            "agent": "I found your order #12345! It's in transit with UPS. Expected delivery: June 6, 2026. Tracking: 1Z999AA10123456784."
        },
        {
            "title": "2. RETURN REQUEST",
            "customer": "I want to return a product",
            "intent": "returns",
            "confidence": 0.92,
            "agent": "I'd be happy to help! Returns are accepted within 30 days. What's your order number?"
        },
        {
            "title": "3. PRODUCT SEARCH",
            "customer": "Do you have wireless headphones?",
            "intent": "products",
            "confidence": 0.94,
            "agent": "Yes! We have Premium Wireless Pro ($79.99, 4.8★), Budget Basic ($29.99, 4.2★), and Sports Active ($49.99, 4.5★) - all in stock!"
        },
        {
            "title": "4. REFUND REQUEST",
            "customer": "I need a refund for order #99999",
            "intent": "refunds",
            "confidence": 0.97,
            "agent": "I've processed your $149.99 refund to your original payment method. You'll see it in 5-7 business days. Refund ID: REF-99999."
        },
        {
            "title": "5. SMART ESCALATION",
            "customer": "I want to speak to a manager NOW!",
            "intent": "escalation",
            "confidence": 1.00,
            "agent": "I understand this needs special attention. Connecting you with a specialist who'll have full context. Marked as high priority."
        }
    ]

    for scenario in scenarios:
        print("\n" + "-"*70)
        print(f"  {scenario['title']}")
        print("-"*70)
        print(f"\n👤 Customer: {scenario['customer']}")
        print(f"\n🤖 Agent: {scenario['agent']}")
        print(f"\n📊 Intent: {scenario['intent']} | Confidence: {scenario['confidence']:.0%}")
        time.sleep(0.5)

    print("\n" + "-"*70)
    print("  SELF-OPTIMIZATION")
    print("-"*70)
    print("\n📈 After 152 interactions:")
    print("  ✅ 87% resolution rate")
    print("  ✅ 4.6/5.0 customer satisfaction")
    print("  ✅ 89% avg confidence")
    print("  ✅ 8% escalation rate")
    print("\n🔄 Continuous improvements:")
    print("  • A/B testing different response styles")
    print("  • Learning from customer feedback")
    print("  • Optimizing prompts automatically")
    print("  • Identifying success patterns")

    print("\n" + "="*70)
    print("\n✨ Key Features:")
    print("  ✅ 5 Core capabilities (orders, returns, products, refunds, general)")
    print("  ✅ Self-optimizing - learns and improves over time")
    print("  ✅ Context-aware conversations")
    print("  ✅ Smart escalation detection")
    print("  ✅ Multi-channel ready (CLI, API, web)")
    print("  ✅ Fully customizable via configuration")
    print("  ✅ Production-ready with Docker & cloud support")

    print("\n🚀 To Run With Real Claude API:")
    print("  1. Set API key: export ANTHROPIC_API_KEY='your_key'")
    print("  2. Run agent: python src/agent.py")
    print("  3. Or API server: python src/api_server.py")

    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    demo()
