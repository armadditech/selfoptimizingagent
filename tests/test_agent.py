"""
Tests for the main CustomerServiceAgent.
"""

import pytest
from src.agent import CustomerServiceAgent


@pytest.fixture
def agent():
    """Create agent instance for testing."""
    return CustomerServiceAgent(config_path="config/config.example.json")


def test_agent_initialization(agent):
    """Test agent initializes correctly."""
    assert agent is not None
    assert agent.llm_client is not None
    assert agent.intent_router is not None
    assert agent.context_manager is not None
    assert len(agent.handlers) > 0


def test_start_conversation(agent):
    """Test starting a new conversation."""
    greeting = agent.start_conversation(customer_id="test_123")

    assert greeting is not None
    assert isinstance(greeting, str)
    assert len(greeting) > 0
    assert agent.conversation_id is not None


def test_handle_order_message(agent):
    """Test handling an order-related message."""
    agent.start_conversation()

    response = agent.handle_message(
        message="I want to track my order #12345",
        customer_id="test_123"
    )

    assert response is not None
    assert "text" in response
    assert "intent" in response
    assert response["intent"] in ["orders", "general"]
    assert "confidence" in response


def test_handle_return_message(agent):
    """Test handling a return-related message."""
    agent.start_conversation()

    response = agent.handle_message(
        message="I need to return a product I bought last week",
        customer_id="test_123"
    )

    assert response is not None
    assert "text" in response
    assert response["intent"] in ["returns", "general"]


def test_handle_product_message(agent):
    """Test handling a product inquiry."""
    agent.start_conversation()

    response = agent.handle_message(
        message="Do you have wireless headphones in stock?",
        customer_id="test_123"
    )

    assert response is not None
    assert "text" in response
    assert response["intent"] in ["products", "general"]


def test_escalation_detection(agent):
    """Test that escalation triggers are detected."""
    agent.start_conversation()

    response = agent.handle_message(
        message="I want to speak to a manager right now!",
        customer_id="test_123"
    )

    assert response is not None
    # Should escalate due to "manager" keyword
    assert response.get("needs_escalation", False) or "manager" in response["text"].lower()


def test_collect_feedback(agent):
    """Test feedback collection."""
    agent.start_conversation()

    # Handle a message first
    agent.handle_message(
        message="Track my order",
        customer_id="test_123"
    )

    # Collect feedback
    agent.collect_feedback(
        conversation_id=agent.conversation_id,
        rating=5,
        feedback_text="Great service!",
        resolved=True
    )

    # Should not raise any errors
    assert True


def test_context_persistence(agent):
    """Test that conversation context is maintained."""
    agent.start_conversation()

    # Send multiple messages
    agent.handle_message("I want to track an order")
    agent.handle_message("The order number is #12345")

    context = agent.context_manager.get_context(agent.conversation_id)

    assert len(context["messages"]) >= 2
    assert any("track" in msg["content"].lower() for msg in context["messages"])
    assert any("12345" in msg["content"] for msg in context["messages"])


def test_multiple_conversations(agent):
    """Test handling multiple conversations."""
    conv_id_1 = agent.start_conversation(customer_id="customer_1")
    response_1 = agent.handle_message("Track my order", customer_id="customer_1")

    # Start second conversation
    agent.conversation_id = None
    conv_id_2 = agent.start_conversation(customer_id="customer_2")
    response_2 = agent.handle_message("Return a product", customer_id="customer_2")

    assert conv_id_1 != conv_id_2
    assert response_1["conversation_id"] != response_2["conversation_id"]


@pytest.mark.skip(reason="Requires optimization to be enabled and sufficient data")
def test_optimization_cycle(agent):
    """Test running optimization cycle."""
    # Generate some interactions first
    agent.start_conversation()
    for i in range(10):
        agent.handle_message(f"Test message {i}")

    # Run optimization
    agent.run_optimization_cycle()

    # Should not raise errors
    assert True
