#!/usr/bin/env python3
"""
Web UI application for the Self-Optimizing Customer Service Agent.
Beautiful visual interface with real-time chat and analytics.
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import os
import json
import uuid
from datetime import datetime
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
CORS(app)

# Simulated agent responses (works without API)
class SimulatedAgent:
    """Simulates agent responses for demo purposes."""

    def __init__(self):
        self.conversations = {}
        self.analytics = {
            "total_interactions": 0,
            "by_intent": {
                "orders": 0,
                "returns": 0,
                "products": 0,
                "refunds": 0,
                "general": 0
            },
            "avg_confidence": 0.87,
            "escalation_rate": 0.08,
            "satisfaction": 4.6
        }

    def classify_intent(self, message):
        """Classify message intent."""
        message_lower = message.lower()

        # Order keywords
        if any(word in message_lower for word in ['track', 'order', 'shipping', 'delivery']):
            return {
                "intent": "orders",
                "confidence": 0.95,
                "entities": self._extract_order_id(message)
            }

        # Return keywords
        if any(word in message_lower for word in ['return', 'send back', 'exchange']):
            return {
                "intent": "returns",
                "confidence": 0.92,
                "entities": {}
            }

        # Product keywords
        if any(word in message_lower for word in ['product', 'item', 'stock', 'available', 'headphone', 'buy']):
            return {
                "intent": "products",
                "confidence": 0.94,
                "entities": {}
            }

        # Refund keywords
        if any(word in message_lower for word in ['refund', 'money back', 'reimburse']):
            return {
                "intent": "refunds",
                "confidence": 0.97,
                "entities": self._extract_order_id(message)
            }

        # Escalation
        if any(word in message_lower for word in ['manager', 'terrible', 'awful', 'angry', 'supervisor']):
            return {
                "intent": "escalation",
                "confidence": 1.0,
                "entities": {}
            }

        return {
            "intent": "general",
            "confidence": 0.78,
            "entities": {}
        }

    def _extract_order_id(self, message):
        """Extract order ID from message."""
        import re
        match = re.search(r'#?(\w{5,})', message)
        if match:
            return {"order_id": match.group(1)}
        return {}

    def generate_response(self, message, intent_data):
        """Generate appropriate response."""
        intent = intent_data["intent"]
        entities = intent_data["entities"]

        responses = {
            "orders": f"I found your order {entities.get('order_id', '#12345')}! It's currently in transit with UPS (tracking: 1Z999AA10123456784). Expected delivery: June 8, 2026. Last update: Package departed facility. Is there anything else I can help you with?",

            "returns": "I'd be happy to help you with your return! Our return policy allows returns within 30 days of purchase. To get started, I'll need your order number. Do you have that available?",

            "products": "Yes, we have several great options in stock! Here are our top picks:\n\n• **Premium Wireless Pro** - $79.99 (4.8★) - In stock\n  Advanced noise cancellation, 30hr battery\n\n• **Budget Wireless Basic** - $29.99 (4.2★) - In stock\n  Great sound quality, 20hr battery\n\n• **Sports Wireless Active** - $49.99 (4.5★) - In stock\n  Water-resistant, secure fit\n\nWould you like more details about any of these?",

            "refunds": f"I'm sorry to hear you need a refund. I've processed your refund of $149.99 for order {entities.get('order_id', '#99999')} to your original payment method. You should see the credit within 5-7 business days. Your refund ID is REF-{entities.get('order_id', '99999')} for your records. Is there anything else I can help you with?",

            "escalation": "I understand this situation needs special attention. Let me connect you with one of our specialist team members who can help you better. They'll have full context of our conversation and will reach out to you shortly. Your case has been marked as high priority.",

            "general": "I'm here to help! I can assist you with orders, returns, products, refunds, and general questions. What would you like to know about?"
        }

        return responses.get(intent, "I'd be happy to help! Could you tell me more about what you need?")

    def handle_message(self, message, conversation_id=None):
        """Handle incoming message."""
        if not conversation_id:
            conversation_id = str(uuid.uuid4())

        # Classify intent
        intent_data = self.classify_intent(message)

        # Generate response
        response_text = self.generate_response(message, intent_data)

        # Update analytics
        self.analytics["total_interactions"] += 1
        self.analytics["by_intent"][intent_data["intent"]] += 1

        # Simulate processing time
        import time
        response_time = 0.8 + (hash(message) % 10) / 10

        return {
            "response": response_text,
            "intent": intent_data["intent"],
            "confidence": intent_data["confidence"],
            "entities": intent_data["entities"],
            "response_time": response_time,
            "conversation_id": conversation_id,
            "needs_escalation": intent_data["intent"] == "escalation"
        }

    def get_analytics(self):
        """Get current analytics."""
        return self.analytics

# Initialize agent
agent = SimulatedAgent()

@app.route('/')
def index():
    """Main page."""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat message."""
    data = request.json
    message = data.get('message', '')
    conversation_id = session.get('conversation_id')

    if not conversation_id:
        conversation_id = str(uuid.uuid4())
        session['conversation_id'] = conversation_id

    # Get response from agent
    result = agent.handle_message(message, conversation_id)

    return jsonify(result)

@app.route('/api/analytics', methods=['GET'])
def analytics():
    """Get analytics data."""
    return jsonify(agent.get_analytics())

@app.route('/api/reset', methods=['POST'])
def reset():
    """Reset conversation."""
    session.clear()
    return jsonify({"status": "success"})

if __name__ == '__main__':
    print("\n" + "="*70)
    print("  🤖 Self-Optimizing Customer Service Agent - Web UI")
    print("="*70)
    print("\n✨ Starting web server...")
    print("\n🌐 Open your browser to: http://localhost:5000")
    print("\n📱 Features:")
    print("  • Interactive chat interface")
    print("  • Real-time intent classification")
    print("  • Entity extraction visualization")
    print("  • Live analytics dashboard")
    print("  • Confidence scoring")
    print("\n⏹  Press Ctrl+C to stop")
    print("\n" + "="*70 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
