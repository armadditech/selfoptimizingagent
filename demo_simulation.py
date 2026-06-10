#!/usr/bin/env python3
"""
Demo simulation showing the agent's capabilities without requiring API key.
This simulates the agent's behavior to demonstrate the system.
"""

import time
import json
from datetime import datetime

class DemoSimulation:
    """Simulates the customer service agent for demonstration."""

    def __init__(self):
        self.conversation_id = "demo_conv_123"
        self.turn = 0

    def print_header(self):
        """Print demo header."""
        print("\n" + "="*70)
        print("  🤖 SELF-OPTIMIZING CUSTOMER SERVICE AGENT - LIVE DEMO")
        print("="*70)
        print("\nThis demo simulates the agent's capabilities.")
        print("(For full functionality, set ANTHROPIC_API_KEY and run: python src/agent.py)")
        print("\n" + "-"*70 + "\n")

    def simulate_typing(self, text, delay=0.02):
        """Simulate typing effect."""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

    def show_metadata(self, intent, confidence, response_time):
        """Show interaction metadata."""
        print(f"\n[Metadata]")
        print(f"  Intent: {intent}")
        print(f"  Confidence: {confidence:.2%}")
        print(f"  Response Time: {response_time:.2f}s")
        print(f"  Conversation ID: {self.conversation_id}")
        print()

    def demo_scenario_1_order_tracking(self):
        """Demo scenario 1: Order tracking."""
        print("\n" + "="*70)
        print("SCENARIO 1: Order Tracking")
        print("="*70 + "\n")

        # Customer message
        print("Customer: Track my order #12345")
        time.sleep(1)

        # Simulate processing
        print("\n[Processing...]")
        print("  → Classifying intent...")
        time.sleep(0.5)
        print("  → Intent: orders (confidence: 0.95)")
        print("  → Extracting entities: order_id='12345'")
        time.sleep(0.5)
        print("  → Routing to OrdersHandler...")
        time.sleep(0.5)
        print("  → Executing: track_order(order_id='12345')")
        time.sleep(0.5)
        print("  → Generating response...")
        time.sleep(0.5)

        # Agent response
        print("\nAgent: ", end='')
        response = (
            "I found your order #12345! It's currently in transit with UPS "
            "(tracking: 1Z999AA10123456784). Expected delivery: June 6, 2026. "
            "Last update: Package departed facility. "
            "Is there anything else you'd like to know about your order?"
        )
        self.simulate_typing(response)

        self.show_metadata("orders", 0.95, 1.2)

    def demo_scenario_2_return(self):
        """Demo scenario 2: Return request."""
        print("\n" + "="*70)
        print("SCENARIO 2: Return Request")
        print("="*70 + "\n")

        # Customer message
        print("Customer: I want to return a product I bought last week")
        time.sleep(1)

        # Simulate processing
        print("\n[Processing...]")
        print("  → Classifying intent...")
        time.sleep(0.5)
        print("  → Intent: returns (confidence: 0.92)")
        time.sleep(0.5)
        print("  → Routing to ReturnsHandler...")
        time.sleep(0.5)
        print("  → Checking return eligibility...")
        time.sleep(0.5)

        # Agent response
        print("\nAgent: ", end='')
        response = (
            "I'd be happy to help you with your return! Our return policy allows "
            "returns within 30 days of purchase. To get started, I'll need your "
            "order number. Do you have that available?"
        )
        self.simulate_typing(response)

        self.show_metadata("returns", 0.92, 1.0)

        # Follow-up
        print("\nCustomer: Yes, it's order #67890")
        time.sleep(1)

        print("\n[Processing...]")
        print("  → Context: Previous intent was returns")
        print("  → Entity extraction: order_id='67890'")
        time.sleep(0.5)
        print("  → Executing: check_return_eligibility(order_id='67890')")
        time.sleep(0.5)
        print("  → Result: Eligible (15 days remaining)")
        time.sleep(0.5)
        print("  → Executing: initiate_return(order_id='67890')")
        time.sleep(0.5)

        print("\nAgent: ", end='')
        response = (
            "Good news! Your order is eligible for return. You have 15 days remaining. "
            "I've initiated your return (Return ID: RET-67890). You'll receive a prepaid "
            "return label at your email within 5 minutes. Just pack the item in its "
            "original packaging, attach the label, and drop it off at any UPS location. "
            "Once we receive it, your refund will be processed in 5-7 business days."
        )
        self.simulate_typing(response)

        self.show_metadata("returns", 0.95, 1.3)

    def demo_scenario_3_product_inquiry(self):
        """Demo scenario 3: Product inquiry."""
        print("\n" + "="*70)
        print("SCENARIO 3: Product Inquiry")
        print("="*70 + "\n")

        print("Customer: Do you have wireless headphones in stock?")
        time.sleep(1)

        print("\n[Processing...]")
        print("  → Classifying intent...")
        time.sleep(0.5)
        print("  → Intent: products (confidence: 0.94)")
        print("  → Extracting entities: product_type='wireless headphones'")
        time.sleep(0.5)
        print("  → Routing to ProductsHandler...")
        time.sleep(0.5)
        print("  → Executing: search_products(query='wireless headphones')")
        time.sleep(0.5)

        print("\nAgent: ", end='')
        response = (
            "Yes, we have several wireless headphones in stock! Here are our top options:\n\n"
            "1. **Premium Wireless Pro** - $79.99 (4.8★) - In stock\n"
            "   Advanced noise cancellation, 30hr battery\n\n"
            "2. **Budget Wireless Basic** - $29.99 (4.2★) - In stock\n"
            "   Great sound quality, 20hr battery\n\n"
            "3. **Sports Wireless Active** - $49.99 (4.5★) - In stock\n"
            "   Water-resistant, secure fit for workouts\n\n"
            "Would you like more details about any of these, or help choosing the right one?"
        )
        self.simulate_typing(response)

        self.show_metadata("products", 0.94, 0.9)

    def demo_scenario_4_refund(self):
        """Demo scenario 4: Refund request."""
        print("\n" + "="*70)
        print("SCENARIO 4: Refund Request")
        print("="*70 + "\n")

        print("Customer: I need a refund for order #99999, the item was defective")
        time.sleep(1)

        print("\n[Processing...]")
        print("  → Classifying intent...")
        time.sleep(0.5)
        print("  → Intent: refunds (confidence: 0.97)")
        print("  → Extracting entities: order_id='99999', reason='defective'")
        time.sleep(0.5)
        print("  → Routing to RefundsHandler...")
        time.sleep(0.5)
        print("  → Executing: calculate_refund_amount(order_id='99999')")
        time.sleep(0.5)
        print("  → Amount: $149.99")
        print("  → Checking approval: $149.99 > auto_approve_threshold ($50)")
        print("  → Checking approval: $149.99 < manager_threshold ($500)")
        print("  → Result: Standard approval")
        time.sleep(0.5)
        print("  → Executing: process_refund(order_id='99999', amount=149.99)")
        time.sleep(0.5)

        print("\nAgent: ", end='')
        response = (
            "I'm sorry to hear the item was defective. I've processed your refund "
            "of $149.99 to your original payment method. You should see the credit "
            "within 5-7 business days. Your refund ID is REF-99999 for your records. "
            "Is there anything else I can help you with?"
        )
        self.simulate_typing(response)

        self.show_metadata("refunds", 0.97, 1.1)

    def demo_scenario_5_escalation(self):
        """Demo scenario 5: Escalation detection."""
        print("\n" + "="*70)
        print("SCENARIO 5: Smart Escalation")
        print("="*70 + "\n")

        print("Customer: This is terrible! I want to speak to a manager NOW!")
        time.sleep(1)

        print("\n[Processing...]")
        print("  → Classifying intent...")
        time.sleep(0.5)
        print("  → Detected frustration keywords: 'terrible', 'manager'")
        print("  → Escalation check: frustration detected = True")
        print("  → Escalation check: explicit request ('manager') = True")
        time.sleep(0.5)
        print("  ⚠️  ESCALATION TRIGGERED")
        time.sleep(0.5)
        print("  → Preparing context handoff...")
        time.sleep(0.5)

        print("\nAgent: ", end='')
        response = (
            "I understand this situation needs special attention. Let me connect you "
            "with one of our specialist team members who can help you better. They'll "
            "have full context of our conversation and will reach out to you shortly. "
            "Your case has been marked as high priority."
        )
        self.simulate_typing(response)

        print("\n[Metadata]")
        print(f"  Intent: escalation")
        print(f"  Confidence: 1.00")
        print(f"  Escalation Reason: frustration_keywords + explicit_request")
        print(f"  Priority: HIGH")
        print(f"  Context: Preserved for human agent")
        print()

    def demo_optimization(self):
        """Demo optimization cycle."""
        print("\n" + "="*70)
        print("SELF-OPTIMIZATION IN ACTION")
        print("="*70 + "\n")

        print("After collecting interactions, the agent runs optimization:\n")
        time.sleep(1)

        print("🔄 Running optimization cycle...")
        time.sleep(1)

        print("\n📊 Performance Analysis:")
        time.sleep(0.5)
        print("  • Total interactions: 152")
        print("  • Resolution rate: 87%")
        print("  • Avg confidence: 0.89")
        print("  • Escalation rate: 8%")
        print("  • Customer satisfaction: 4.6/5.0")
        time.sleep(1)

        print("\n🧪 A/B Test Results:")
        time.sleep(0.5)
        print("  • Response style A: 82% satisfaction")
        print("  • Response style B: 89% satisfaction")
        print("  ✅ Winner: Style B (7% improvement)")
        print("  → Deploying winning variant")
        time.sleep(1)

        print("\n✨ Prompt Optimizations Identified:")
        time.sleep(0.5)
        print("  • Returns handler: High escalation rate (22%)")
        print("    Suggestion: Add more specific handling examples")
        print("    Expected improvement: 15%")
        print("  • Refunds handler: Low confidence (0.65)")
        print("    Suggestion: Provide detailed policy guidelines")
        print("    Expected improvement: 20%")
        time.sleep(1)

        print("\n✅ Optimization complete!")
        print("  → Performance improved by 12%")
        print("  → New prompt versions deployed")
        print("  → Rollback available if regression detected")
        print()

    def demo_analytics(self):
        """Demo analytics dashboard."""
        print("\n" + "="*70)
        print("ANALYTICS DASHBOARD")
        print("="*70 + "\n")

        analytics = {
            "overview": {
                "total_interactions": 152,
                "total_conversations": 89,
                "avg_per_day": 21.7
            },
            "performance": {
                "avg_confidence": 0.89,
                "avg_response_time": 1.15,
                "escalation_rate": 0.08,
                "resolution_rate": 0.87
            },
            "satisfaction": {
                "avg_rating": 4.6,
                "5_star": 67,
                "4_star": 18,
                "3_star": 8,
                "2_star": 4,
                "1_star": 3
            },
            "by_intent": {
                "orders": {"count": 52, "satisfaction": 4.7, "escalation": 0.04},
                "returns": {"count": 38, "satisfaction": 4.5, "escalation": 0.11},
                "products": {"count": 31, "satisfaction": 4.8, "escalation": 0.03},
                "refunds": {"count": 21, "satisfaction": 4.4, "escalation": 0.14},
                "general": {"count": 10, "satisfaction": 4.6, "escalation": 0.05}
            }
        }

        print(json.dumps(analytics, indent=2))
        print()

    def run_full_demo(self):
        """Run complete demonstration."""
        self.print_header()

        input("Press Enter to start Demo Scenario 1: Order Tracking...")
        self.demo_scenario_1_order_tracking()

        input("\nPress Enter for Demo Scenario 2: Return Request...")
        self.demo_scenario_2_return()

        input("\nPress Enter for Demo Scenario 3: Product Inquiry...")
        self.demo_scenario_3_product_inquiry()

        input("\nPress Enter for Demo Scenario 4: Refund Request...")
        self.demo_scenario_4_refund()

        input("\nPress Enter for Demo Scenario 5: Smart Escalation...")
        self.demo_scenario_5_escalation()

        input("\nPress Enter to see Self-Optimization in Action...")
        self.demo_optimization()

        input("\nPress Enter to view Analytics Dashboard...")
        self.demo_analytics()

        print("="*70)
        print("DEMO COMPLETE!")
        print("="*70)
        print("\nTo run the actual agent with Claude API:")
        print("  1. Set your API key: export ANTHROPIC_API_KEY='your_key'")
        print("  2. Run: python src/agent.py")
        print("\nTo run the API server:")
        print("  python src/api_server.py")
        print("\nFor more examples:")
        print("  python examples/basic_usage.py")
        print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    demo = DemoSimulation()
    demo.run_full_demo()
