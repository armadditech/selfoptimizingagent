#!/usr/bin/env python3
"""
Self-Optimizing Customer Service Agent
Main orchestrator that coordinates intent routing, capability handling, and optimization.
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

from core.llm_client import LLMClient
from core.intent_router import IntentRouter
from core.context_manager import ContextManager
from capabilities.orders import OrdersHandler
from capabilities.returns import ReturnsHandler
from capabilities.products import ProductsHandler
from capabilities.refunds import RefundsHandler
from capabilities.general import GeneralHandler
from optimization.learning_engine import LearningEngine
from optimization.analytics import Analytics


class CustomerServiceAgent:
    """
    Main agent orchestrator that handles customer service interactions
    with self-optimization capabilities.
    """

    def __init__(self, config_path: str = "config/config.json"):
        """Initialize the customer service agent with configuration."""
        self.config = self._load_config(config_path)

        # Initialize core components
        self.llm_client = LLMClient(self.config["llm"])
        self.intent_router = IntentRouter(self.llm_client, self.config)
        self.context_manager = ContextManager(self.config["conversation"])

        # Initialize capability handlers
        self.handlers = self._initialize_handlers()

        # Initialize optimization engine
        self.learning_engine = LearningEngine(self.config["optimization"])
        self.analytics = Analytics(self.config["analytics"])

        # Track conversation metadata
        self.conversation_id = None
        self.customer_id = None

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from file with environment variable substitution."""
        config_file = Path(config_path)

        # Fall back to example config if config.json doesn't exist
        if not config_file.exists():
            example_config = Path("config/config.example.json")
            if example_config.exists():
                print(f"⚠️  {config_path} not found, using {example_config}")
                config_file = example_config
            else:
                raise FileNotFoundError(f"Configuration file not found: {config_path}")

        with open(config_file, 'r') as f:
            config_text = f.read()

        # Replace environment variables
        for key, value in os.environ.items():
            config_text = config_text.replace(f"${{{key}}}", value)

        return json.loads(config_text)

    def _initialize_handlers(self) -> Dict:
        """Initialize all capability handlers based on configuration."""
        handlers = {}
        capabilities = self.config["capabilities"]

        if capabilities["orders"]["enabled"]:
            handlers["orders"] = OrdersHandler(
                self.llm_client,
                capabilities["orders"]
            )

        if capabilities["returns"]["enabled"]:
            handlers["returns"] = ReturnsHandler(
                self.llm_client,
                capabilities["returns"]
            )

        if capabilities["products"]["enabled"]:
            handlers["products"] = ProductsHandler(
                self.llm_client,
                capabilities["products"]
            )

        if capabilities["refunds"]["enabled"]:
            handlers["refunds"] = RefundsHandler(
                self.llm_client,
                capabilities["refunds"]
            )

        if capabilities["general"]["enabled"]:
            handlers["general"] = GeneralHandler(
                self.llm_client,
                capabilities["general"]
            )

        return handlers

    def start_conversation(
        self,
        customer_id: Optional[str] = None,
        channel: str = "chat"
    ) -> str:
        """
        Start a new customer service conversation.

        Args:
            customer_id: Optional customer identifier
            channel: Communication channel (chat, email, phone)

        Returns:
            Conversation ID
        """
        self.conversation_id = self.context_manager.create_conversation(
            customer_id=customer_id,
            channel=channel
        )
        self.customer_id = customer_id

        # Log conversation start
        self.analytics.log_event("conversation_started", {
            "conversation_id": self.conversation_id,
            "customer_id": customer_id,
            "channel": channel,
            "timestamp": datetime.now().isoformat()
        })

        # Return greeting message
        greeting = self.config["conversation"]["greeting_message"]
        self.context_manager.add_message(
            self.conversation_id,
            "assistant",
            greeting
        )

        return greeting

    def handle_message(
        self,
        message: str,
        customer_id: Optional[str] = None,
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Process a customer message and generate a response.

        Args:
            message: Customer's message
            customer_id: Optional customer identifier
            context: Optional additional context

        Returns:
            Response dictionary with text, metadata, and actions
        """
        start_time = datetime.now()

        # Initialize conversation if needed
        if not self.conversation_id:
            self.start_conversation(customer_id)

        # Add customer message to context
        self.context_manager.add_message(
            self.conversation_id,
            "user",
            message
        )

        # Get conversation context
        conversation_context = self.context_manager.get_context(
            self.conversation_id
        )

        # Classify intent
        intent_result = self.intent_router.classify_intent(
            message,
            conversation_context
        )

        intent = intent_result["intent"]
        confidence = intent_result["confidence"]
        entities = intent_result.get("entities", {})

        # Check if escalation is needed
        if self._should_escalate(message, intent_result, conversation_context):
            return self._handle_escalation(message, intent_result)

        # Route to appropriate handler
        if intent in self.handlers:
            handler = self.handlers[intent]
            response_result = handler.handle(
                message=message,
                entities=entities,
                context=conversation_context,
                customer_id=customer_id
            )
        else:
            # Fallback to general handler
            handler = self.handlers.get("general")
            if handler:
                response_result = handler.handle(
                    message=message,
                    entities=entities,
                    context=conversation_context,
                    customer_id=customer_id
                )
            else:
                response_result = {
                    "text": "I apologize, but I'm not sure how to help with that. Let me connect you with someone who can assist you better.",
                    "needs_escalation": True
                }

        # Add response to context
        self.context_manager.add_message(
            self.conversation_id,
            "assistant",
            response_result["text"]
        )

        # Calculate response time
        response_time = (datetime.now() - start_time).total_seconds()

        # Prepare response object
        response = {
            "text": response_result["text"],
            "intent": intent,
            "confidence": confidence,
            "entities": entities,
            "actions": response_result.get("actions", []),
            "needs_escalation": response_result.get("needs_escalation", False),
            "response_time_seconds": response_time,
            "conversation_id": self.conversation_id
        }

        # Log interaction for learning
        self._log_interaction(
            message=message,
            response=response,
            intent_result=intent_result,
            context=conversation_context
        )

        # Track analytics
        self.analytics.log_interaction(
            conversation_id=self.conversation_id,
            intent=intent,
            confidence=confidence,
            response_time=response_time,
            escalated=response.get("needs_escalation", False)
        )

        return response

    def _should_escalate(
        self,
        message: str,
        intent_result: Dict,
        context: Dict
    ) -> bool:
        """
        Determine if the conversation should be escalated to a human agent.

        Args:
            message: Customer's message
            intent_result: Intent classification result
            context: Conversation context

        Returns:
            True if escalation is needed
        """
        if not self.config["escalation"]["enabled"]:
            return False

        triggers = self.config["escalation"]["triggers"]

        # Check for explicit request
        if triggers["explicit_request"]:
            escalation_keywords = ["human", "person", "agent", "manager", "supervisor"]
            if any(keyword in message.lower() for keyword in escalation_keywords):
                return True

        # Check for low confidence
        if triggers["low_confidence"]:
            if intent_result["confidence"] < self.config["agent"]["confidence_threshold"]:
                return True

        # Check for frustration keywords
        if triggers["customer_frustration"]:
            frustration_keywords = self.config["escalation"]["frustration_keywords"]
            if any(keyword in message.lower() for keyword in frustration_keywords):
                return True

        # Check for repeated failures
        if triggers["repeated_failures"]:
            failed_attempts = context.get("metadata", {}).get("failed_attempts", 0)
            if failed_attempts >= self.config["agent"]["escalation_threshold"]:
                return True

        return False

    def _handle_escalation(self, message: str, intent_result: Dict) -> Dict:
        """Handle escalation to human agent."""
        escalation_message = self.config["escalation"]["handoff_message"]

        # Prepare context for human agent
        handoff_context = {
            "conversation_id": self.conversation_id,
            "customer_id": self.customer_id,
            "last_message": message,
            "intent": intent_result["intent"],
            "conversation_history": self.context_manager.get_context(
                self.conversation_id
            )["messages"][-5:] if self.config["escalation"]["collect_context"] else []
        }

        return {
            "text": escalation_message,
            "needs_escalation": True,
            "escalation_context": handoff_context,
            "intent": "escalation",
            "confidence": 1.0,
            "conversation_id": self.conversation_id
        }

    def _log_interaction(
        self,
        message: str,
        response: Dict,
        intent_result: Dict,
        context: Dict
    ):
        """Log interaction for learning and optimization."""
        interaction_data = {
            "timestamp": datetime.now().isoformat(),
            "conversation_id": self.conversation_id,
            "customer_id": self.customer_id,
            "message": message,
            "intent": intent_result["intent"],
            "confidence": intent_result["confidence"],
            "entities": intent_result.get("entities", {}),
            "response": response["text"],
            "response_time": response["response_time_seconds"],
            "escalated": response.get("needs_escalation", False),
            "actions": response.get("actions", [])
        }

        # Pass to learning engine if optimization is enabled
        if self.config["optimization"]["enabled"]:
            self.learning_engine.record_interaction(interaction_data)

    def collect_feedback(
        self,
        conversation_id: str,
        rating: Optional[int] = None,
        feedback_text: Optional[str] = None,
        resolved: bool = True
    ):
        """
        Collect customer feedback for a conversation.

        Args:
            conversation_id: Conversation identifier
            rating: Customer satisfaction rating (1-5)
            feedback_text: Optional text feedback
            resolved: Whether the issue was resolved
        """
        feedback_data = {
            "conversation_id": conversation_id,
            "timestamp": datetime.now().isoformat(),
            "rating": rating,
            "feedback_text": feedback_text,
            "resolved": resolved
        }

        # Log feedback
        self.analytics.log_feedback(feedback_data)

        # Update learning engine
        if self.config["optimization"]["enabled"]:
            self.learning_engine.record_feedback(
                conversation_id,
                feedback_data
            )

    def run_optimization_cycle(self):
        """
        Run the self-optimization cycle to improve agent performance.
        This should be called periodically (e.g., daily).
        """
        if not self.config["optimization"]["enabled"]:
            print("Optimization is disabled in configuration.")
            return

        print("🔄 Running optimization cycle...")

        # Analyze recent interactions
        insights = self.learning_engine.analyze_performance()

        print(f"📊 Performance Insights:")
        print(f"  - Total interactions: {insights['total_interactions']}")
        print(f"  - Resolution rate: {insights['resolution_rate']:.2%}")
        print(f"  - Avg confidence: {insights['avg_confidence']:.2%}")
        print(f"  - Escalation rate: {insights['escalation_rate']:.2%}")

        # Run A/B tests
        if self.config["optimization"]["ab_testing"]["enabled"]:
            ab_results = self.learning_engine.run_ab_tests()
            print(f"\n🧪 A/B Test Results:")
            for test_name, result in ab_results.items():
                print(f"  - {test_name}: {result['winner']} (lift: {result['lift']:.2%})")

        # Update prompts if needed
        if self.config["optimization"]["auto_update_prompts"]:
            prompt_updates = self.learning_engine.optimize_prompts()
            print(f"\n✨ Prompt Optimizations:")
            for capability, update in prompt_updates.items():
                print(f"  - {capability}: {update['improvement']:.2%} improvement")

        print("\n✅ Optimization cycle complete!")

    def get_analytics_summary(self) -> Dict:
        """Get summary of agent performance analytics."""
        return self.analytics.get_summary()

    def interactive_mode(self):
        """Run the agent in interactive console mode."""
        print("=" * 60)
        print("  🤖 Self-Optimizing Customer Service Agent")
        print("=" * 60)
        print(f"\nAgent: {self.config['agent']['name']}")
        print(f"Business: {self.config['business']['name']}")
        print("\nType 'quit' or 'exit' to end the conversation")
        print("Type 'feedback' to provide feedback on the conversation")
        print("-" * 60)

        # Start conversation
        greeting = self.start_conversation(channel="console")
        print(f"\n{self.config['agent']['name']}: {greeting}\n")

        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()

                if not user_input:
                    continue

                # Check for exit commands
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print(f"\n{self.config['agent']['name']}: Thank you for contacting us! Have a great day! 👋\n")
                    break

                # Check for feedback command
                if user_input.lower() == 'feedback':
                    self._collect_interactive_feedback()
                    continue

                # Process message
                response = self.handle_message(user_input)

                # Display response
                print(f"\n{self.config['agent']['name']}: {response['text']}")

                # Show metadata in debug mode
                if os.getenv("DEBUG") == "1":
                    print(f"\n[Debug] Intent: {response['intent']} "
                          f"(confidence: {response['confidence']:.2f})")

                print()

            except KeyboardInterrupt:
                print("\n\nGoodbye! 👋\n")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")
                if os.getenv("DEBUG") == "1":
                    import traceback
                    traceback.print_exc()

    def _collect_interactive_feedback(self):
        """Collect feedback in interactive mode."""
        print("\n--- Feedback ---")
        try:
            rating = input("How would you rate this conversation? (1-5): ").strip()
            rating = int(rating) if rating.isdigit() and 1 <= int(rating) <= 5 else None

            resolved = input("Was your issue resolved? (yes/no): ").strip().lower()
            resolved = resolved in ['yes', 'y']

            feedback_text = input("Any additional comments? (optional): ").strip()

            self.collect_feedback(
                conversation_id=self.conversation_id,
                rating=rating,
                feedback_text=feedback_text if feedback_text else None,
                resolved=resolved
            )

            print("Thank you for your feedback! 🙏\n")
        except Exception as e:
            print(f"Error collecting feedback: {e}\n")


def main():
    """Main entry point for the customer service agent."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Self-Optimizing Customer Service Agent"
    )
    parser.add_argument(
        "--config",
        default="config/config.json",
        help="Path to configuration file"
    )
    parser.add_argument(
        "--optimize",
        action="store_true",
        help="Run optimization cycle"
    )
    parser.add_argument(
        "--analytics",
        action="store_true",
        help="Show analytics summary"
    )

    args = parser.parse_args()

    # Initialize agent
    agent = CustomerServiceAgent(config_path=args.config)

    # Run optimization cycle if requested
    if args.optimize:
        agent.run_optimization_cycle()
        return

    # Show analytics if requested
    if args.analytics:
        summary = agent.get_analytics_summary()
        print(json.dumps(summary, indent=2))
        return

    # Default: run in interactive mode
    agent.interactive_mode()


if __name__ == "__main__":
    main()
