"""
Orders capability handler for tracking, canceling, and modifying orders.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json


class OrdersHandler:
    """Handles order-related customer service requests."""

    def __init__(self, llm_client, config: Dict):
        """
        Initialize orders handler.

        Args:
            llm_client: LLM client instance
            config: Orders configuration
        """
        self.llm_client = llm_client
        self.config = config
        self.functions = config.get("functions", [])

    def handle(
        self,
        message: str,
        entities: Dict,
        context: Dict,
        customer_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Handle order-related request.

        Args:
            message: Customer message
            entities: Extracted entities
            context: Conversation context
            customer_id: Customer identifier

        Returns:
            Response dictionary with text and actions
        """
        # Build system prompt
        system_prompt = self._build_system_prompt()

        # Build context for order handling
        order_context = self._build_order_context(entities, customer_id)

        # Create messages
        messages = self._build_messages(message, context, order_context)

        # Get tools for order operations
        tools = self._get_order_tools()

        try:
            # Get response from LLM
            response = self.llm_client.create_message(
                messages=messages,
                system=system_prompt,
                tools=tools,
                max_tokens=1000
            )

            # Extract tool uses (actions to take)
            tool_uses = self.llm_client.extract_tool_uses(response)
            actions = []

            for tool_use in tool_uses:
                action_result = self._execute_action(
                    tool_use["name"],
                    tool_use["input"]
                )
                actions.append(action_result)

            # Get response text
            response_text = self.llm_client.extract_text(response)

            # If no text but we have actions, generate response
            if not response_text and actions:
                response_text = self._generate_action_response(actions)

            return {
                "text": response_text,
                "actions": actions,
                "needs_escalation": self._check_escalation_needed(actions)
            }

        except Exception as e:
            print(f"Orders handler error: {e}")
            return {
                "text": "I apologize, but I'm having trouble accessing order information right now. Let me connect you with someone who can help.",
                "actions": [],
                "needs_escalation": True
            }

    def _build_system_prompt(self) -> str:
        """Build system prompt for order handling."""
        return """You are a helpful customer service agent specializing in order management.

Your capabilities:
- Track order status and shipping information
- Cancel orders within the cancellation window
- Modify orders (if allowed and within timeframe)
- Provide delivery estimates
- Explain order issues

Guidelines:
- Be clear and helpful about order status
- If an order can't be canceled, explain why and offer alternatives
- Always confirm order IDs before taking actions
- If order information isn't available, ask for the order number
- Escalate if the issue requires manager approval

Available tools:
- track_order: Get current status and tracking info
- cancel_order: Cancel an order (within allowed timeframe)
- modify_order: Change order details (if modification is enabled)
- get_order_details: Retrieve full order information

Use tools when you have enough information. Ask clarifying questions if needed."""

    def _build_order_context(
        self,
        entities: Dict,
        customer_id: Optional[str]
    ) -> str:
        """Build context about order configuration and customer."""
        context_parts = []

        # Add order policy information
        cancel_window = self.config.get("cancellation_window_hours", 24)
        context_parts.append(
            f"Order cancellation allowed within {cancel_window} hours of placement."
        )

        if self.config.get("modification_allowed", True):
            context_parts.append("Order modifications are allowed before shipping.")
        else:
            context_parts.append("Order modifications are not available.")

        # Add extracted entities
        if entities.get("order_id"):
            context_parts.append(f"Customer mentioned order ID: {entities['order_id']}")

        if customer_id:
            context_parts.append(f"Customer ID: {customer_id}")

        return "\n".join(context_parts)

    def _build_messages(
        self,
        message: str,
        context: Dict,
        order_context: str
    ) -> List[Dict]:
        """Build message history for LLM."""
        messages = []

        # Add order context as user message
        messages.append({
            "role": "user",
            "content": f"Context:\n{order_context}"
        })

        # Add recent conversation history
        for msg in context.get("messages", [])[-5:]:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

        # Add current message if not already included
        if not messages or messages[-1]["content"] != message:
            messages.append({
                "role": "user",
                "content": message
            })

        return messages

    def _get_order_tools(self) -> List[Dict]:
        """Get tool definitions for order operations."""
        tools = []

        if "track_order" in self.functions:
            tools.append({
                "name": "track_order",
                "description": "Get current tracking and shipping information for an order",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "order_id": {
                            "type": "string",
                            "description": "The order ID to track"
                        }
                    },
                    "required": ["order_id"]
                }
            })

        if "cancel_order" in self.functions:
            tools.append({
                "name": "cancel_order",
                "description": "Cancel an order if within cancellation window",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "order_id": {
                            "type": "string",
                            "description": "The order ID to cancel"
                        },
                        "reason": {
                            "type": "string",
                            "description": "Reason for cancellation"
                        }
                    },
                    "required": ["order_id"]
                }
            })

        if "modify_order" in self.functions:
            tools.append({
                "name": "modify_order",
                "description": "Modify order details before shipping",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "order_id": {
                            "type": "string",
                            "description": "The order ID to modify"
                        },
                        "changes": {
                            "type": "object",
                            "description": "Changes to make (address, items, etc.)"
                        }
                    },
                    "required": ["order_id", "changes"]
                }
            })

        if "order_status" in self.functions:
            tools.append({
                "name": "get_order_details",
                "description": "Retrieve complete order information",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "order_id": {
                            "type": "string",
                            "description": "The order ID"
                        }
                    },
                    "required": ["order_id"]
                }
            })

        return tools

    def _execute_action(self, action_name: str, params: Dict) -> Dict:
        """
        Execute an order action (simulated for demo).

        In production, this would call real e-commerce APIs.
        """
        # Simulate order operations
        if action_name == "track_order":
            return self._simulate_track_order(params["order_id"])
        elif action_name == "cancel_order":
            return self._simulate_cancel_order(
                params["order_id"],
                params.get("reason")
            )
        elif action_name == "modify_order":
            return self._simulate_modify_order(
                params["order_id"],
                params["changes"]
            )
        elif action_name == "get_order_details":
            return self._simulate_get_order_details(params["order_id"])

        return {"action": action_name, "status": "unknown", "params": params}

    def _simulate_track_order(self, order_id: str) -> Dict:
        """Simulate order tracking."""
        # In production, call shipping API
        return {
            "action": "track_order",
            "status": "success",
            "order_id": order_id,
            "data": {
                "status": "in_transit",
                "carrier": "UPS",
                "tracking_number": "1Z999AA10123456784",
                "estimated_delivery": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
                "last_update": "Package departed facility",
                "location": "Distribution center"
            }
        }

    def _simulate_cancel_order(self, order_id: str, reason: Optional[str]) -> Dict:
        """Simulate order cancellation."""
        # Check if within cancellation window
        cancel_window = self.config.get("cancellation_window_hours", 24)

        # In production, check actual order timestamp
        # For demo, assume it's within window
        return {
            "action": "cancel_order",
            "status": "success",
            "order_id": order_id,
            "data": {
                "cancelled": True,
                "refund_initiated": True,
                "refund_amount": 99.99,
                "refund_method": "original_payment",
                "message": f"Order {order_id} has been cancelled. Refund will be processed in 3-5 business days."
            }
        }

    def _simulate_modify_order(self, order_id: str, changes: Dict) -> Dict:
        """Simulate order modification."""
        if not self.config.get("modification_allowed", True):
            return {
                "action": "modify_order",
                "status": "error",
                "order_id": order_id,
                "data": {
                    "message": "Order modifications are not currently available."
                }
            }

        return {
            "action": "modify_order",
            "status": "success",
            "order_id": order_id,
            "data": {
                "modified": True,
                "changes_applied": changes,
                "message": f"Order {order_id} has been updated successfully."
            }
        }

    def _simulate_get_order_details(self, order_id: str) -> Dict:
        """Simulate getting order details."""
        return {
            "action": "get_order_details",
            "status": "success",
            "order_id": order_id,
            "data": {
                "order_id": order_id,
                "order_date": "2024-06-01",
                "status": "processing",
                "total": 149.99,
                "items": [
                    {"name": "Product A", "quantity": 2, "price": 49.99},
                    {"name": "Product B", "quantity": 1, "price": 50.01}
                ],
                "shipping_address": "123 Main St, City, ST 12345",
                "payment_method": "Credit card ending in 1234"
            }
        }

    def _generate_action_response(self, actions: List[Dict]) -> str:
        """Generate response text based on actions taken."""
        if not actions:
            return "I wasn't able to complete that action. Can you provide more details?"

        action = actions[0]

        if action["action"] == "track_order" and action["status"] == "success":
            data = action["data"]
            return (
                f"I found your order #{action['order_id']}. It's currently {data['status']} "
                f"with {data['carrier']} (tracking: {data['tracking_number']}). "
                f"Expected delivery: {data['estimated_delivery']}. "
                f"Last update: {data['last_update']}."
            )

        elif action["action"] == "cancel_order" and action["status"] == "success":
            data = action["data"]
            return data["message"]

        elif action["action"] == "modify_order" and action["status"] == "success":
            return action["data"]["message"]

        return "Action completed successfully."

    def _check_escalation_needed(self, actions: List[Dict]) -> bool:
        """Check if any actions require escalation."""
        for action in actions:
            if action.get("status") == "error":
                return True
            if action.get("requires_approval"):
                return True
        return False
