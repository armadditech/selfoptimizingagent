"""
Products capability handler for product inquiries, recommendations, and availability.
"""

from typing import Dict, List, Optional, Any


class ProductsHandler:
    """Handles product-related inquiries."""

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
        """Handle product inquiries."""
        system_prompt = f"""You are a knowledgeable product specialist.

Capabilities:
- Answer product questions
- Check availability and inventory
- Provide recommendations (max {self.config.get('max_recommendations', 3)})
- Compare products
- Share specifications

Be helpful, accurate, and provide relevant details. Use tools to look up current information."""

        messages = self._build_messages(message, context)

        try:
            response = self.llm_client.create_message(
                messages=messages,
                system=system_prompt,
                tools=self._get_product_tools(),
                max_tokens=1000
            )

            tool_uses = self.llm_client.extract_tool_uses(response)
            actions = [self._execute_action(t["name"], t["input"]) for t in tool_uses]
            response_text = self.llm_client.extract_text(response)

            return {
                "text": response_text or "Here's what I found about that product.",
                "actions": actions,
                "needs_escalation": False
            }

        except Exception as e:
            return {
                "text": "I'm having trouble accessing product information. Let me help you find what you need another way.",
                "actions": [],
                "needs_escalation": False
            }

    def _build_messages(self, message: str, context: Dict) -> List[Dict]:
        messages = []
        for msg in context.get("messages", [])[-5:]:
            messages.append({"role": msg["role"], "content": msg["content"]})
        if not messages or messages[-1]["content"] != message:
            messages.append({"role": "user", "content": message})
        return messages

    def _get_product_tools(self) -> List[Dict]:
        """Get product tool definitions."""
        return [
            {
                "name": "search_products",
                "description": "Search for products by keyword",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"},
                        "category": {"type": "string", "description": "Optional category filter"}
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "get_product_details",
                "description": "Get detailed information about a specific product",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "product_id": {"type": "string"}
                    },
                    "required": ["product_id"]
                }
            },
            {
                "name": "check_availability",
                "description": "Check if a product is in stock",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "product_id": {"type": "string"},
                        "location": {"type": "string", "description": "Optional store location"}
                    },
                    "required": ["product_id"]
                }
            },
            {
                "name": "get_recommendations",
                "description": "Get product recommendations",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "based_on": {"type": "string", "description": "Product or category to base recommendations on"},
                        "count": {"type": "integer", "default": 3}
                    },
                    "required": ["based_on"]
                }
            }
        ]

    def _execute_action(self, action_name: str, params: Dict) -> Dict:
        """Execute product action (simulated)."""
        if action_name == "search_products":
            return {
                "action": action_name,
                "status": "success",
                "data": {
                    "results": [
                        {"id": "PROD001", "name": "Widget Pro", "price": 49.99, "rating": 4.5},
                        {"id": "PROD002", "name": "Widget Deluxe", "price": 79.99, "rating": 4.8},
                        {"id": "PROD003", "name": "Widget Basic", "price": 29.99, "rating": 4.2}
                    ]
                }
            }
        elif action_name == "get_product_details":
            return {
                "action": action_name,
                "status": "success",
                "data": {
                    "id": params["product_id"],
                    "name": "Widget Pro",
                    "description": "High-quality widget with advanced features",
                    "price": 49.99,
                    "specifications": {
                        "weight": "2 lbs",
                        "dimensions": "10x5x3 inches",
                        "color": "Blue"
                    },
                    "in_stock": True
                }
            }
        elif action_name == "check_availability":
            return {
                "action": action_name,
                "status": "success",
                "data": {
                    "in_stock": True,
                    "quantity": 47,
                    "locations": ["Warehouse A", "Store 123"]
                }
            }
        elif action_name == "get_recommendations":
            return {
                "action": action_name,
                "status": "success",
                "data": {
                    "recommendations": [
                        {"id": "REC001", "name": "Premium Cable", "price": 14.99},
                        {"id": "REC002", "name": "Protective Case", "price": 24.99},
                        {"id": "REC003", "name": "Extended Warranty", "price": 19.99}
                    ]
                }
            }
        return {"action": action_name, "status": "unknown"}
