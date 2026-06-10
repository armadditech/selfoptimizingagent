"""
General capability handler for company info, policies, FAQs, and general inquiries.
"""

from typing import Dict, List, Optional, Any
import json
from pathlib import Path


class GeneralHandler:
    """Handles general customer service inquiries."""

    def __init__(self, llm_client, config: Dict):
        self.llm_client = llm_client
        self.config = config
        self.knowledge_base = self._load_knowledge_base()

    def _load_knowledge_base(self) -> Dict:
        """Load knowledge base, FAQs, and policies."""
        kb = {
            "company_info": {
                "about": "We are a leading e-commerce company dedicated to customer satisfaction.",
                "values": ["Customer first", "Quality products", "Fast delivery", "Easy returns"],
                "established": "2010"
            },
            "policies": {
                "shipping": {
                    "standard": "5-7 business days",
                    "express": "2-3 business days",
                    "overnight": "Next business day",
                    "free_shipping_threshold": 50.0
                },
                "payment": {
                    "accepted_methods": ["Credit Card", "Debit Card", "PayPal", "Apple Pay"],
                    "payment_plans": "Available for orders over $500"
                },
                "privacy": "We protect your personal information and never sell your data.",
                "warranty": "All products come with a 1-year manufacturer warranty."
            },
            "faqs": [
                {
                    "question": "How do I track my order?",
                    "answer": "You can track your order using the tracking number sent to your email, or by logging into your account."
                },
                {
                    "question": "What is your return policy?",
                    "answer": "We offer 30-day returns on most items. Items must be in original condition."
                },
                {
                    "question": "Do you ship internationally?",
                    "answer": "Yes, we ship to over 100 countries. International shipping rates vary by destination."
                },
                {
                    "question": "How can I contact customer support?",
                    "answer": "You can reach us via chat, email at support@example.com, or phone at 1-800-123-4567."
                },
                {
                    "question": "Do you offer price matching?",
                    "answer": "Yes, we match prices from authorized retailers. Contact us with proof of the lower price."
                }
            ],
            "contact": {
                "email": "support@example.com",
                "phone": "1-800-123-4567",
                "hours": "24/7",
                "chat": "Available on website"
            }
        }

        # Try to load custom knowledge base if configured
        kb_path = self.config.get("knowledge_base_path")
        if kb_path:
            kb_dir = Path(kb_path)
            if kb_dir.exists():
                # Load any custom JSON files
                for json_file in kb_dir.glob("*.json"):
                    try:
                        with open(json_file, 'r') as f:
                            custom_data = json.load(f)
                            kb[json_file.stem] = custom_data
                    except Exception:
                        pass

        return kb

    def handle(
        self,
        message: str,
        entities: Dict,
        context: Dict,
        customer_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Handle general inquiries."""
        system_prompt = f"""You are a helpful customer service agent for answering general questions.

You have access to:
- Company information and history
- Policies (shipping, returns, payment, privacy, warranty)
- FAQs and common questions
- Contact information
- Store locations

Knowledge Base:
{json.dumps(self.knowledge_base, indent=2)}

Be friendly, accurate, and helpful. If you don't know something, be honest and offer to connect them with someone who can help."""

        messages = self._build_messages(message, context)

        try:
            response = self.llm_client.create_message(
                messages=messages,
                system=system_prompt,
                max_tokens=1000
            )

            response_text = self.llm_client.extract_text(response)

            # Check if question was answered
            if not response_text or len(response_text) < 20:
                response_text = "I'd be happy to help! Could you provide more details about what you'd like to know?"

            return {
                "text": response_text,
                "actions": [],
                "needs_escalation": False
            }

        except Exception as e:
            return {
                "text": "I'm here to help! What would you like to know about our company, policies, or services?",
                "actions": [],
                "needs_escalation": False
            }

    def _build_messages(self, message: str, context: Dict) -> List[Dict]:
        """Build message history."""
        messages = []
        for msg in context.get("messages", [])[-5:]:
            messages.append({"role": msg["role"], "content": msg["content"]})
        if not messages or messages[-1]["content"] != message:
            messages.append({"role": "user", "content": message})
        return messages
