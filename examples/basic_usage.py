#!/usr/bin/env python3
"""
Basic usage examples for the Self-Optimizing Customer Service Agent.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agent import CustomerServiceAgent


def example_1_simple_conversation():
    """Example 1: Simple conversation flow."""
    print("=" * 60)
    print("Example 1: Simple Conversation")
    print("=" * 60)

    # Initialize agent
    agent = CustomerServiceAgent()

    # Start conversation
    greeting = agent.start_conversation(customer_id="customer_123")
    print(f"Agent: {greeting}\n")

    # Customer asks about order
    response = agent.handle_message(
        message="I want to track my order #12345",
        customer_id="customer_123"
    )

    print(f"Customer: I want to track my order #12345")
    print(f"Agent: {response['text']}")
    print(f"[Intent: {response['intent']}, Confidence: {response['confidence']:.2f}]")
    print()


def example_2_multi_turn_conversation():
    """Example 2: Multi-turn conversation with context."""
    print("=" * 60)
    print("Example 2: Multi-Turn Conversation")
    print("=" * 60)

    agent = CustomerServiceAgent()
    agent.start_conversation(customer_id="customer_456")

    # Turn 1
    print("Customer: I bought a product last week")
    response1 = agent.handle_message("I bought a product last week")
    print(f"Agent: {response1['text']}\n")

    # Turn 2 - agent maintains context
    print("Customer: I want to return it")
    response2 = agent.handle_message("I want to return it")
    print(f"Agent: {response2['text']}\n")

    # Turn 3
    print("Customer: How long does the refund take?")
    response3 = agent.handle_message("How long does the refund take?")
    print(f"Agent: {response3['text']}\n")


def example_3_different_capabilities():
    """Example 3: Testing different capabilities."""
    print("=" * 60)
    print("Example 3: Different Capabilities")
    print("=" * 60)

    agent = CustomerServiceAgent()

    test_cases = [
        ("Track my order #ABC123", "orders"),
        ("I need to return a defective item", "returns"),
        ("Do you have wireless headphones?", "products"),
        ("I want a refund for order #XYZ789", "refunds"),
        ("What are your store hours?", "general")
    ]

    for message, expected_intent in test_cases:
        agent.conversation_id = None  # Reset conversation
        agent.start_conversation()

        response = agent.handle_message(message)

        print(f"Message: {message}")
        print(f"Detected Intent: {response['intent']} (expected: {expected_intent})")
        print(f"Confidence: {response['confidence']:.2f}")
        print(f"Response: {response['text'][:100]}...")
        print()


def example_4_feedback_collection():
    """Example 4: Collecting and using feedback."""
    print("=" * 60)
    print("Example 4: Feedback Collection")
    print("=" * 60)

    agent = CustomerServiceAgent()

    # Have a conversation
    agent.start_conversation(customer_id="customer_789")
    response = agent.handle_message("Track my order #99999")

    print(f"Conversation: Track my order #99999")
    print(f"Response: {response['text'][:100]}...\n")

    # Collect feedback
    print("Collecting feedback...")
    agent.collect_feedback(
        conversation_id=agent.conversation_id,
        rating=5,
        feedback_text="Very helpful and quick response!",
        resolved=True
    )
    print("✓ Feedback recorded\n")


def example_5_batch_processing():
    """Example 5: Batch process multiple inquiries."""
    print("=" * 60)
    print("Example 5: Batch Processing")
    print("=" * 60)

    agent = CustomerServiceAgent()

    inquiries = [
        {"customer_id": "C001", "message": "Where is my order?"},
        {"customer_id": "C002", "message": "I want to return this"},
        {"customer_id": "C003", "message": "Do you have this in blue?"},
        {"customer_id": "C004", "message": "Request a refund please"}
    ]

    results = []

    for inquiry in inquiries:
        agent.conversation_id = None  # New conversation
        agent.start_conversation(customer_id=inquiry["customer_id"])

        response = agent.handle_message(
            message=inquiry["message"],
            customer_id=inquiry["customer_id"]
        )

        results.append({
            "customer_id": inquiry["customer_id"],
            "message": inquiry["message"],
            "intent": response["intent"],
            "confidence": response["confidence"],
            "response": response["text"][:80] + "..."
        })

    # Display results
    for i, result in enumerate(results, 1):
        print(f"{i}. Customer {result['customer_id']}")
        print(f"   Query: {result['message']}")
        print(f"   Intent: {result['intent']} ({result['confidence']:.2f})")
        print(f"   Response: {result['response']}")
        print()


def example_6_analytics():
    """Example 6: View analytics."""
    print("=" * 60)
    print("Example 6: Analytics")
    print("=" * 60)

    agent = CustomerServiceAgent()

    # Generate some test interactions
    print("Generating test interactions...")
    for i in range(5):
        agent.conversation_id = None
        agent.start_conversation(customer_id=f"test_{i}")
        agent.handle_message(f"Test message {i}")

    print("✓ Test interactions generated\n")

    # Get analytics
    print("Fetching analytics summary...")
    summary = agent.get_analytics_summary()

    print("\nAnalytics Summary:")
    print(f"  Total interactions: {summary['overview']['total_interactions']}")
    print(f"  Avg confidence: {summary['performance']['avg_confidence']:.2%}")
    print(f"  Avg response time: {summary['performance']['avg_response_time_seconds']:.2f}s")
    print(f"  Escalation rate: {summary['performance']['escalation_rate']:.2%}")
    print()


def example_7_api_integration():
    """Example 7: Using as API (programmatic)."""
    print("=" * 60)
    print("Example 7: API Integration Pattern")
    print("=" * 60)

    # This shows how you'd integrate the agent into your application

    class CustomerSupportAPI:
        """Wrapper for integrating agent into your app."""

        def __init__(self):
            self.agent = CustomerServiceAgent()
            self.active_conversations = {}

        def handle_customer_message(self, customer_id: str, message: str) -> dict:
            """Handle incoming customer message."""
            # Get or create conversation
            if customer_id not in self.active_conversations:
                self.active_conversations[customer_id] = \
                    self.agent.start_conversation(customer_id=customer_id)

            # Process message
            response = self.agent.handle_message(
                message=message,
                customer_id=customer_id
            )

            return {
                "success": True,
                "response": response["text"],
                "needs_human": response.get("needs_escalation", False),
                "conversation_id": response["conversation_id"]
            }

        def submit_feedback(self, conversation_id: str, rating: int, resolved: bool):
            """Submit feedback for a conversation."""
            self.agent.collect_feedback(
                conversation_id=conversation_id,
                rating=rating,
                resolved=resolved
            )
            return {"success": True}

    # Usage example
    api = CustomerSupportAPI()

    # Customer interaction 1
    result1 = api.handle_customer_message(
        customer_id="API_USER_1",
        message="Track my order"
    )
    print(f"API Response 1: {result1['response'][:80]}...")
    print(f"Needs human: {result1['needs_human']}\n")

    # Customer interaction 2
    result2 = api.handle_customer_message(
        customer_id="API_USER_2",
        message="I need a refund immediately!"
    )
    print(f"API Response 2: {result2['response'][:80]}...")
    print(f"Needs human: {result2['needs_human']}\n")


def main():
    """Run all examples."""
    examples = [
        example_1_simple_conversation,
        example_2_multi_turn_conversation,
        example_3_different_capabilities,
        example_4_feedback_collection,
        example_5_batch_processing,
        example_6_analytics,
        example_7_api_integration
    ]

    print("\n" + "=" * 60)
    print("  Self-Optimizing Agent - Usage Examples")
    print("=" * 60 + "\n")

    for i, example_func in enumerate(examples, 1):
        try:
            example_func()
        except Exception as e:
            print(f"❌ Example {i} failed: {e}\n")

        if i < len(examples):
            input("Press Enter to continue to next example...")
            print("\n")

    print("=" * 60)
    print("  All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
