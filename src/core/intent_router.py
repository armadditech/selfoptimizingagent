"""
Intent Router for classifying customer messages and routing to appropriate handlers.
"""

from typing import Dict, List, Optional, Any
import json
import re


class IntentRouter:
    """Routes customer messages to appropriate capability handlers."""

    def __init__(self, llm_client, config: Dict):
        """
        Initialize intent router.

        Args:
            llm_client: LLM client instance
            config: Agent configuration
        """
        self.llm_client = llm_client
        self.config = config
        self.enabled_capabilities = self._get_enabled_capabilities()

    def _get_enabled_capabilities(self) -> List[str]:
        """Get list of enabled capabilities from config."""
        capabilities = []
        for cap_name, cap_config in self.config["capabilities"].items():
            if cap_config.get("enabled", False):
                capabilities.append(cap_name)
        return capabilities

    def classify_intent(
        self,
        message: str,
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Classify the intent of a customer message.

        Args:
            message: Customer's message
            context: Optional conversation context

        Returns:
            Dictionary with intent, confidence, and extracted entities
        """
        # Build system prompt for intent classification
        system_prompt = self._build_classification_prompt()

        # Build user message with context
        user_message = self._build_user_message(message, context)

        # Get classification from LLM
        messages = [
            {"role": "user", "content": user_message}
        ]

        try:
            response = self.llm_client.create_message(
                messages=messages,
                system=system_prompt,
                tools=self._get_classification_tools(),
                max_tokens=1000,
                temperature=0.3
            )

            # Extract tool use for structured output
            tool_uses = self.llm_client.extract_tool_uses(response)

            if tool_uses:
                # Use structured output from tool
                classification = tool_uses[0]["input"]
                return {
                    "intent": classification["intent"],
                    "confidence": classification["confidence"],
                    "entities": classification.get("entities", {}),
                    "reasoning": classification.get("reasoning", "")
                }
            else:
                # Fallback: parse from text
                text = self.llm_client.extract_text(response)
                return self._parse_classification_text(text)

        except Exception as e:
            print(f"Intent classification error: {e}")
            # Fallback to rule-based classification
            return self._rule_based_classification(message)

    def _build_classification_prompt(self) -> str:
        """Build system prompt for intent classification."""
        capabilities_desc = []
        for cap in self.enabled_capabilities:
            capabilities_desc.append(f"- {cap}: {self._get_capability_description(cap)}")

        capabilities_text = "\n".join(capabilities_desc)

        return f"""You are an intent classifier for a customer service agent.

Your task is to analyze customer messages and classify them into one of these intents:
{capabilities_text}

For each message:
1. Determine the primary intent
2. Assign a confidence score (0.0 to 1.0)
3. Extract relevant entities (order IDs, product names, amounts, etc.)
4. Provide brief reasoning

Rules:
- If a message has multiple intents, choose the primary one
- If unsure, use the "general" intent
- Extract all relevant entities (IDs, dates, amounts, product names)
- Be concise but accurate

Use the classify_intent tool to provide your classification."""

    def _get_capability_description(self, capability: str) -> str:
        """Get description for a capability."""
        descriptions = {
            "orders": "Track, cancel, modify, or inquire about orders",
            "returns": "Initiate returns, check return status, get return labels",
            "products": "Product information, availability, recommendations, comparisons",
            "refunds": "Process refunds, check refund status, refund inquiries",
            "general": "Company info, policies, FAQs, store locations, account help"
        }
        return descriptions.get(capability, "General customer inquiries")

    def _build_user_message(self, message: str, context: Optional[Dict]) -> str:
        """Build user message with context for classification."""
        parts = [f"Customer message: {message}"]

        if context and context.get("messages"):
            # Add recent context
            recent_messages = context["messages"][-3:]
            if len(recent_messages) > 0:
                context_text = []
                for msg in recent_messages:
                    role = "Customer" if msg["role"] == "user" else "Agent"
                    context_text.append(f"{role}: {msg['content']}")

                parts.append("\nRecent conversation:")
                parts.append("\n".join(context_text))

        return "\n".join(parts)

    def _get_classification_tools(self) -> List[Dict]:
        """Get tool definition for structured classification output."""
        return [
            {
                "name": "classify_intent",
                "description": "Classify the customer message intent with confidence and entities",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "intent": {
                            "type": "string",
                            "enum": self.enabled_capabilities,
                            "description": "The classified intent category"
                        },
                        "confidence": {
                            "type": "number",
                            "description": "Confidence score from 0.0 to 1.0",
                            "minimum": 0.0,
                            "maximum": 1.0
                        },
                        "entities": {
                            "type": "object",
                            "description": "Extracted entities from the message",
                            "properties": {
                                "order_id": {"type": "string"},
                                "product_name": {"type": "string"},
                                "amount": {"type": "number"},
                                "date": {"type": "string"},
                                "email": {"type": "string"},
                                "phone": {"type": "string"}
                            }
                        },
                        "reasoning": {
                            "type": "string",
                            "description": "Brief explanation of the classification"
                        }
                    },
                    "required": ["intent", "confidence"]
                }
            }
        ]

    def _parse_classification_text(self, text: str) -> Dict:
        """Parse classification from text response (fallback)."""
        # Simple pattern matching fallback
        intent = "general"
        confidence = 0.5

        text_lower = text.lower()

        # Try to extract intent
        for cap in self.enabled_capabilities:
            if cap in text_lower:
                intent = cap
                confidence = 0.7
                break

        # Try to extract confidence
        confidence_match = re.search(r'confidence[:\s]+(\d+\.?\d*)', text_lower)
        if confidence_match:
            confidence = float(confidence_match.group(1))
            if confidence > 1.0:
                confidence = confidence / 100.0

        return {
            "intent": intent,
            "confidence": confidence,
            "entities": {},
            "reasoning": "Fallback text parsing"
        }

    def _rule_based_classification(self, message: str) -> Dict:
        """Simple rule-based classification as ultimate fallback."""
        message_lower = message.lower()

        # Order keywords
        if any(word in message_lower for word in ['order', 'track', 'shipping', 'delivery', 'cancel order']):
            return {
                "intent": "orders",
                "confidence": 0.7,
                "entities": self._extract_order_id(message),
                "reasoning": "Rule-based: order keywords detected"
            }

        # Return keywords
        if any(word in message_lower for word in ['return', 'send back', 'exchange']):
            return {
                "intent": "returns",
                "confidence": 0.7,
                "entities": {},
                "reasoning": "Rule-based: return keywords detected"
            }

        # Product keywords
        if any(word in message_lower for word in ['product', 'item', 'stock', 'available', 'recommend']):
            return {
                "intent": "products",
                "confidence": 0.7,
                "entities": {},
                "reasoning": "Rule-based: product keywords detected"
            }

        # Refund keywords
        if any(word in message_lower for word in ['refund', 'money back', 'reimburse']):
            return {
                "intent": "refunds",
                "confidence": 0.7,
                "entities": {},
                "reasoning": "Rule-based: refund keywords detected"
            }

        # Default to general
        return {
            "intent": "general",
            "confidence": 0.6,
            "entities": {},
            "reasoning": "Rule-based: no specific keywords, using general"
        }

    def _extract_order_id(self, message: str) -> Dict:
        """Extract order ID from message."""
        # Look for common order ID patterns
        patterns = [
            r'#(\w+)',  # #ABC123
            r'order[:\s]+(\w+)',  # order: ABC123
            r'(?:order|tracking)[:\s]*#?(\w+)'  # order #ABC123 or tracking ABC123
        ]

        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                return {"order_id": match.group(1)}

        return {}
