"""
Returns capability handler for processing product returns and exchanges.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta


class ReturnsHandler:
    """Handles return and exchange requests."""

    def __init__(self, llm_client, config: Dict):
        self.llm_client = llm_client
        self.config = config

    def handle(
        self,
        message: str,
        entities: Dict,
        context: Dict,
        customer_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Handle return-related requests."""
        system_prompt = f"""You are a customer service agent handling returns and exchanges.

Return Policy:
- Return window: {self.config.get('return_window_days', 30)} days
- Free return shipping: {'Yes' if self.config.get('free_return_shipping', True) else 'No'}
- Exchanges allowed: {'Yes' if self.config.get('exchange_allowed', True) else 'No'}
- Restocking fee: {self.config.get('restocking_fee', 0)*100}%
- Conditions: {json.dumps(self.config.get('conditions', {}))}

Be helpful and empathetic. Check eligibility, initiate returns, provide return labels, and process exchanges."""

        messages = self._build_messages(message, context)

        try:
            response = self.llm_client.create_message(
                messages=messages,
                system=system_prompt,
                tools=self._get_return_tools(),
                max_tokens=1000
            )

            tool_uses = self.llm_client.extract_tool_uses(response)
            actions = [self._execute_action(t["name"], t["input"]) for t in tool_uses]
            response_text = self.llm_client.extract_text(response)

            if not response_text and actions:
                response_text = self._generate_response(actions)

            return {
                "text": response_text,
                "actions": actions,
                "needs_escalation": any(a.get("status") == "error" for a in actions)
            }

        except Exception as e:
            return {
                "text": "I apologize, but I'm having trouble processing your return request. Let me connect you with a specialist.",
                "actions": [],
                "needs_escalation": True
            }

    def _build_messages(self, message: str, context: Dict) -> List[Dict]:
        """Build message history."""
        messages = []
        for msg in context.get("messages", [])[-5:]:
            messages.append({"role": msg["role"], "content": msg["content"]})
        if not messages or messages[-1]["content"] != message:
            messages.append({"role": "user", "content": message})
        return messages

    def _get_return_tools(self) -> List[Dict]:
        """Get return tool definitions."""
        return [
            {
                "name": "check_return_eligibility",
                "description": "Check if an order/item is eligible for return",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "order_id": {"type": "string"},
                        "item_id": {"type": "string", "description": "Optional specific item"}
                    },
                    "required": ["order_id"]
                }
            },
            {
                "name": "initiate_return",
                "description": "Start a return process",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "order_id": {"type": "string"},
                        "items": {"type": "array", "items": {"type": "string"}},
                        "reason": {"type": "string"}
                    },
                    "required": ["order_id", "items", "reason"]
                }
            },
            {
                "name": "generate_return_label",
                "description": "Generate a prepaid return shipping label",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "return_id": {"type": "string"}
                    },
                    "required": ["return_id"]
                }
            }
        ]

    def _execute_action(self, action_name: str, params: Dict) -> Dict:
        """Execute return action (simulated)."""
        if action_name == "check_return_eligibility":
            return {
                "action": action_name,
                "status": "success",
                "data": {
                    "eligible": True,
                    "days_remaining": 15,
                    "reason": "Within return window"
                }
            }
        elif action_name == "initiate_return":
            return {
                "action": action_name,
                "status": "success",
                "data": {
                    "return_id": "RET-" + params["order_id"],
                    "status": "initiated",
                    "message": "Return initiated successfully"
                }
            }
        elif action_name == "generate_return_label":
            return {
                "action": action_name,
                "status": "success",
                "data": {
                    "label_url": f"https://example.com/labels/{params['return_id']}.pdf",
                    "tracking": "1Z999AA10987654321"
                }
            }
        return {"action": action_name, "status": "unknown"}

    def _generate_response(self, actions: List[Dict]) -> str:
        """Generate response from actions."""
        if not actions:
            return "I couldn't process that request."

        action = actions[0]
        if action["action"] == "check_return_eligibility":
            if action["data"]["eligible"]:
                return f"Good news! Your order is eligible for return. You have {action['data']['days_remaining']} days remaining."
            return "Unfortunately, this order is outside our return window."
        elif action["action"] == "initiate_return":
            return f"I've initiated your return (ID: {action['data']['return_id']}). You'll receive a return label shortly."
        elif action["action"] == "generate_return_label":
            return f"Your return label is ready! You can download it here: {action['data']['label_url']}"
        return "Return processed successfully."


import json
