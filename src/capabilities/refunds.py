"""
Refunds capability handler for processing refund requests.
"""

from typing import Dict, List, Optional, Any


class RefundsHandler:
    """Handles refund processing and inquiries."""

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
        """Handle refund requests."""
        auto_approve = self.config.get("auto_approve_threshold", 50.0)
        manager_approval = self.config.get("manager_approval_threshold", 500.0)

        system_prompt = f"""You are a customer service agent handling refund requests.

Refund Policy:
- Auto-approve amounts under ${auto_approve}
- Manager approval required over ${manager_approval}
- Processing time: {self.config.get('processing_days', 5)} business days
- Methods: {', '.join(self.config.get('methods', ['original_payment']))}
- Partial refunds: {'Allowed' if self.config.get('partial_refunds', True) else 'Not allowed'}

Be empathetic and clear about the refund process and timeline."""

        messages = self._build_messages(message, context)

        try:
            response = self.llm_client.create_message(
                messages=messages,
                system=system_prompt,
                tools=self._get_refund_tools(),
                max_tokens=1000
            )

            tool_uses = self.llm_client.extract_tool_uses(response)
            actions = [self._execute_action(t["name"], t["input"]) for t in tool_uses]
            response_text = self.llm_client.extract_text(response)

            needs_escalation = any(
                a.get("data", {}).get("requires_approval", False) for a in actions
            )

            return {
                "text": response_text or "I've processed your refund request.",
                "actions": actions,
                "needs_escalation": needs_escalation
            }

        except Exception as e:
            return {
                "text": "I'm having trouble processing your refund. Let me connect you with our refunds team.",
                "actions": [],
                "needs_escalation": True
            }

    def _build_messages(self, message: str, context: Dict) -> List[Dict]:
        messages = []
        for msg in context.get("messages", [])[-5:]:
            messages.append({"role": msg["role"], "content": msg["content"]})
        if not messages or messages[-1]["content"] != message:
            messages.append({"role": "user", "content": message})
        return messages

    def _get_refund_tools(self) -> List[Dict]:
        """Get refund tool definitions."""
        return [
            {
                "name": "process_refund",
                "description": "Process a refund for an order or item",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "order_id": {"type": "string"},
                        "amount": {"type": "number"},
                        "reason": {"type": "string"},
                        "method": {
                            "type": "string",
                            "enum": self.config.get("methods", ["original_payment", "store_credit"]),
                            "default": "original_payment"
                        }
                    },
                    "required": ["order_id", "amount", "reason"]
                }
            },
            {
                "name": "check_refund_status",
                "description": "Check the status of an existing refund",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "refund_id": {"type": "string"}
                    },
                    "required": ["refund_id"]
                }
            },
            {
                "name": "calculate_refund_amount",
                "description": "Calculate the refund amount for an order",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "order_id": {"type": "string"},
                        "items": {"type": "array", "items": {"type": "string"}, "description": "Optional specific items"}
                    },
                    "required": ["order_id"]
                }
            }
        ]

    def _execute_action(self, action_name: str, params: Dict) -> Dict:
        """Execute refund action (simulated)."""
        if action_name == "process_refund":
            amount = params["amount"]
            auto_threshold = self.config.get("auto_approve_threshold", 50.0)
            manager_threshold = self.config.get("manager_approval_threshold", 500.0)

            if amount <= auto_threshold:
                return {
                    "action": action_name,
                    "status": "success",
                    "data": {
                        "refund_id": f"REF-{params['order_id']}",
                        "amount": amount,
                        "method": params.get("method", "original_payment"),
                        "status": "approved",
                        "processing_days": self.config.get("processing_days", 5),
                        "message": f"Refund of ${amount:.2f} approved and will be processed in {self.config.get('processing_days', 5)} business days."
                    }
                }
            elif amount >= manager_threshold:
                return {
                    "action": action_name,
                    "status": "pending",
                    "data": {
                        "refund_id": f"REF-{params['order_id']}",
                        "amount": amount,
                        "status": "pending_approval",
                        "requires_approval": True,
                        "message": f"This refund amount requires manager approval. I'll escalate this for you."
                    }
                }
            else:
                return {
                    "action": action_name,
                    "status": "success",
                    "data": {
                        "refund_id": f"REF-{params['order_id']}",
                        "amount": amount,
                        "method": params.get("method", "original_payment"),
                        "status": "approved",
                        "processing_days": self.config.get("processing_days", 5),
                        "message": f"Refund of ${amount:.2f} has been approved."
                    }
                }

        elif action_name == "check_refund_status":
            return {
                "action": action_name,
                "status": "success",
                "data": {
                    "refund_id": params["refund_id"],
                    "status": "processing",
                    "amount": 99.99,
                    "initiated_date": "2024-06-01",
                    "expected_completion": "2024-06-08"
                }
            }

        elif action_name == "calculate_refund_amount":
            return {
                "action": action_name,
                "status": "success",
                "data": {
                    "order_id": params["order_id"],
                    "original_amount": 149.99,
                    "refund_amount": 149.99,
                    "breakdown": {
                        "items": 149.99,
                        "shipping": 0.0,
                        "tax": 0.0
                    }
                }
            }

        return {"action": action_name, "status": "unknown"}
