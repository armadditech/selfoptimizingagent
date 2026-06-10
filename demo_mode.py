#!/usr/bin/env python3
"""
Interactive Demo Mode - No API Key Required!

This demo mode runs the full application with simulated responses,
allowing anyone to experience the self-optimizing agent without
needing an Anthropic API key.

Perfect for:
- Quick evaluation
- Learning how it works
- Presentations
- Testing the UI
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import secrets
from datetime import datetime
import random
import time
import uuid
import threading

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
CORS(app)

class DemoAgent:
    """
    Demo agent with pre-built responses - works without API!
    """

    def __init__(self):
        self.conversations = []
        self.feedback_data = []
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
            "satisfaction": 4.6,
            "resolution_rate": 0.85
        }
        self.optimization_history = []
        self.current_version = 1
        self.auto_simulation_active = False
        self.auto_simulation_thread = None
        self.simulation_stats = {
            "total_simulated": 0,
            "total_optimizations": 0,
            "start_time": None,
            "last_activity": None
        }

        # Pre-built response templates
        self.response_templates = {
            "orders": [
                "I found your order {order_id}! It's in transit with UPS. Expected delivery: June 8, 2026. Tracking: 1Z999AA10123456784. Would you like me to send you tracking updates?",
                "Your order {order_id} was shipped on June 3rd and is currently out for delivery! You should receive it today. Is there anything else I can help with?",
                "I see your order {order_id}. It's currently being prepared for shipment. We'll send you a tracking number within 24 hours. Thank you for your patience!"
            ],
            "returns": [
                "I'd be happy to help with your return! Returns are accepted within 30 days. I'll generate a prepaid shipping label for you. What's your order number?",
                "No problem! To process your return, I'll need your order number and reason for return. We'll issue a full refund once we receive the item.",
                "I can definitely help with that return. You have 30 days from purchase. Would you like an exchange or refund?"
            ],
            "products": [
                "Yes! We have Premium Wireless Pro ($79.99, 4.8★) with noise cancellation, Budget Wireless Basic ($29.99, 4.2★) great for everyday use, and Sports Wireless Active ($49.99, 4.5★) water-resistant. Which interests you?",
                "Great question! Our top sellers are the Premium Wireless Pro and Sports Active. Both are in stock. The Premium has better noise cancellation, while the Sports are more durable. What's your priority?",
                "We have 3 excellent options in stock right now. Would you like me to compare features, or do you have specific requirements like battery life or water resistance?"
            ],
            "refunds": [
                "I've processed your $149.99 refund for order {order_id}. You'll see the credit in 5-7 business days. Your refund ID is REF-{order_id} for your records. Can I help with anything else?",
                "Absolutely! I'm initiating your refund now. The full amount of $149.99 will be returned to your original payment method within 5-7 business days. You'll receive a confirmation email shortly.",
                "I apologize for any inconvenience. Your refund of $149.99 has been approved and will be processed today. You should see it in your account within a week."
            ],
            "general": [
                "I'm here to help! I can assist with orders, returns, products, refunds, and general questions. Our hours are 9 AM - 9 PM EST, Monday-Saturday. What would you like to know about?",
                "Great question! We offer free shipping on orders over $50, 30-day returns, and lifetime customer support. Is there a specific topic I can help you with?",
                "I'd be happy to help! We have a comprehensive FAQ section, live chat support, and phone support available. What specifically would you like to know?"
            ]
        }

    def classify_intent(self, message):
        """Classify message intent using keyword matching."""
        message_lower = message.lower()

        # Order keywords
        if any(word in message_lower for word in ['track', 'order', 'shipping', 'delivery', 'package', 'where is']):
            return {
                "intent": "orders",
                "confidence": 0.93 + random.random() * 0.05,
                "entities": self._extract_order_id(message)
            }

        # Return keywords
        if any(word in message_lower for word in ['return', 'send back', 'exchange', 'damaged', 'wrong item']):
            return {
                "intent": "returns",
                "confidence": 0.89 + random.random() * 0.05,
                "entities": {}
            }

        # Product keywords
        if any(word in message_lower for word in ['product', 'item', 'stock', 'available', 'headphone', 'buy', 'purchase', 'price']):
            return {
                "intent": "products",
                "confidence": 0.91 + random.random() * 0.05,
                "entities": {}
            }

        # Refund keywords
        if any(word in message_lower for word in ['refund', 'money back', 'reimburse', 'credit', 'cancel order']):
            return {
                "intent": "refunds",
                "confidence": 0.95 + random.random() * 0.03,
                "entities": self._extract_order_id(message)
            }

        # Escalation keywords
        if any(word in message_lower for word in ['manager', 'terrible', 'awful', 'angry', 'supervisor', 'complaint']):
            return {
                "intent": "escalation",
                "confidence": 1.0,
                "entities": {}
            }

        return {
            "intent": "general",
            "confidence": 0.75 + random.random() * 0.08,
            "entities": {}
        }

    def _extract_order_id(self, message):
        """Extract order ID from message."""
        import re
        match = re.search(r'#?([A-Z0-9]{5,})', message)
        if match:
            return {"order_id": match.group(1)}
        return {"order_id": "ORD" + str(random.randint(10000, 99999))}

    def generate_response(self, message, intent_data):
        """Generate appropriate response based on intent."""
        intent = intent_data["intent"]
        entities = intent_data["entities"]

        if intent == "escalation":
            return "I understand this situation needs special attention. Let me connect you with one of our specialist team members who can help you better. They'll have full context of our conversation and will reach out to you shortly. Your case has been marked as high priority."

        # Get templates for this intent
        templates = self.response_templates.get(intent, self.response_templates["general"])

        # Pick a random template
        template = random.choice(templates)

        # Fill in order ID if present
        if "{order_id}" in template and entities.get("order_id"):
            template = template.replace("{order_id}", entities["order_id"])

        return template

    def handle_message(self, message, conversation_id=None):
        """Handle message and track interaction."""
        if not conversation_id:
            conversation_id = str(uuid.uuid4())

        intent_data = self.classify_intent(message)
        response_text = self.generate_response(message, intent_data)

        self.analytics["total_interactions"] += 1
        self.analytics["by_intent"][intent_data["intent"]] += 1

        interaction = {
            "conversation_id": conversation_id,
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "intent": intent_data["intent"],
            "confidence": intent_data["confidence"],
            "response": response_text,
            "version": self.current_version
        }
        self.conversations.append(interaction)

        response_time = 0.3 + random.random() * 0.2

        return {
            "response": response_text,
            "intent": intent_data["intent"],
            "confidence": intent_data["confidence"],
            "entities": intent_data["entities"],
            "response_time": response_time,
            "conversation_id": conversation_id,
            "needs_escalation": intent_data["intent"] == "escalation"
        }

    # (Include all the other methods from app_enhanced.py: simulate_customers, run_optimization, etc.)
    # For brevity, I'll add the essential ones...

    def simulate_customers(self, count=10):
        """Simulate customer interactions."""
        scenarios = [
            "Track my order #ABC123",
            "I want to return a defective item",
            "Do you have wireless headphones in stock?",
            "I need a refund for order #XYZ789",
            "What are your store hours?",
            "My package hasn't arrived yet",
            "Can I exchange this for a different color?",
            "Is this product available in blue?",
            "I want my money back for order #DEF456",
            "Where is my order #12345?",
            "What's the best wireless headphone?",
            "How do I start a return?",
            "My order is damaged",
            "Can you check stock for me?",
            "I'd like to cancel my order"
        ]

        results = []
        for i in range(count):
            message = random.choice(scenarios)
            result = self.handle_message(message)

            # Simulate feedback
            rating = random.choices([5, 4, 3, 2, 1], weights=[50, 30, 10, 7, 3])[0]
            resolved = rating >= 4
            self.record_feedback(result["conversation_id"], rating, resolved)

            results.append({
                "message": message,
                "intent": result["intent"],
                "rating": rating,
                "resolved": resolved
            })

        return results

    def record_feedback(self, conversation_id, rating, resolved):
        """Record customer feedback."""
        self.feedback_data.append({
            "conversation_id": conversation_id,
            "rating": rating,
            "resolved": resolved,
            "timestamp": datetime.now().isoformat()
        })

        # Update metrics
        ratings = [f["rating"] for f in self.feedback_data if f.get("rating")]
        self.analytics["satisfaction"] = sum(ratings) / len(ratings) if ratings else 4.6

        resolved_count = sum(1 for f in self.feedback_data if f.get("resolved"))
        self.analytics["resolution_rate"] = resolved_count / len(self.feedback_data) if self.feedback_data else 0.85

    def run_optimization(self):
        """Run optimization cycle."""
        if len(self.conversations) < 10:
            return {"status": "insufficient_data"}

        # Simulate optimization
        self.current_version += 1

        improvement = {
            "version": self.current_version,
            "timestamp": datetime.now().isoformat(),
            "issues_found": ["Improved response variety", "Enhanced intent detection"],
            "improvements": [f"Optimized templates for version {self.current_version}"],
            "before": {
                "satisfaction": self.analytics["satisfaction"],
                "resolution": self.analytics["resolution_rate"]
            }
        }

        # Simulate improvement
        self.analytics["satisfaction"] = min(5.0, self.analytics["satisfaction"] + random.uniform(0.05, 0.15))
        self.analytics["resolution_rate"] = min(1.0, self.analytics["resolution_rate"] + random.uniform(0.02, 0.05))

        improvement["after"] = {
            "satisfaction": self.analytics["satisfaction"],
            "resolution": self.analytics["resolution_rate"]
        }

        improvement["ab_test"] = {
            "winner": "variant_b",
            "improvement": random.uniform(0.05, 0.12),
            "variant_a": {"satisfaction": 4.3, "resolution": 0.82},
            "variant_b": {"satisfaction": 4.7, "resolution": 0.89}
        }

        self.optimization_history.append(improvement)
        return improvement

    def _auto_simulation_loop(self, interval=1, batch_size=5):
        """Background auto-simulation loop."""
        print(f"🤖 DEMO MODE: Auto-simulation started")

        last_optimization_time = time.time()
        optimization_interval = 10

        while self.auto_simulation_active:
            try:
                self.simulate_customers(batch_size)
                self.simulation_stats["total_simulated"] += batch_size
                self.simulation_stats["last_activity"] = datetime.now().isoformat()

                current_time = time.time()
                if (current_time - last_optimization_time) >= optimization_interval and self.analytics["total_interactions"] >= 10:
                    result = self.run_optimization()
                    if result.get("status") != "insufficient_data":
                        self.simulation_stats["total_optimizations"] += 1
                        last_optimization_time = current_time
                        print(f"✨ DEMO: Optimization #{self.simulation_stats['total_optimizations']} - v{self.current_version}")

                time.sleep(interval)
            except Exception as e:
                print(f"⚠️  Demo error: {e}")
                time.sleep(interval)

    def start_auto_simulation(self, interval=1, batch_size=5):
        """Start auto-simulation."""
        if self.auto_simulation_active:
            return {"status": "already_running"}

        self.auto_simulation_active = True
        self.simulation_stats["start_time"] = datetime.now().isoformat()
        self.simulation_stats["total_simulated"] = 0
        self.simulation_stats["total_optimizations"] = 0

        self.auto_simulation_thread = threading.Thread(
            target=self._auto_simulation_loop,
            args=(interval, batch_size),
            daemon=True
        )
        self.auto_simulation_thread.start()

        return {"status": "started", "interval": interval, "batch_size": batch_size}

    def stop_auto_simulation(self):
        """Stop auto-simulation."""
        if not self.auto_simulation_active:
            return {"status": "not_running"}

        self.auto_simulation_active = False
        return {"status": "stopped", "stats": self.simulation_stats}

    def get_auto_simulation_status(self):
        """Get auto-simulation status."""
        recent_conversations = []
        if len(self.conversations) > 0:
            recent_conversations = [
                {
                    "message": c["message"],
                    "response": c["response"],
                    "intent": c["intent"],
                    "confidence": c["confidence"],
                    "timestamp": c["timestamp"],
                    "version": c["version"]
                }
                for c in self.conversations[-5:]
            ]

        return {
            "active": self.auto_simulation_active,
            "stats": self.simulation_stats,
            "recent_conversations": recent_conversations
        }

    def get_analytics(self):
        """Get analytics."""
        return self.analytics

    def get_optimization_history(self):
        """Get optimization history."""
        return self.optimization_history


# Initialize demo agent
agent = DemoAgent()

# Flask routes
@app.route('/')
def index():
    return render_template('index_enhanced.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')
    conversation_id = session.get('conversation_id')

    if not conversation_id:
        conversation_id = str(uuid.uuid4())
        session['conversation_id'] = conversation_id

    result = agent.handle_message(message, conversation_id)
    return jsonify(result)

@app.route('/api/feedback', methods=['POST'])
def feedback():
    data = request.json
    conversation_id = session.get('conversation_id', str(uuid.uuid4()))
    rating = data.get('rating', 5)
    resolved = data.get('resolved', True)

    agent.record_feedback(conversation_id, rating, resolved)
    return jsonify({"status": "success"})

@app.route('/api/analytics', methods=['GET'])
def analytics():
    return jsonify(agent.get_analytics())

@app.route('/api/simulate', methods=['POST'])
def simulate():
    data = request.json
    count = data.get('count', 10)
    results = agent.simulate_customers(count)
    return jsonify({"results": results, "analytics": agent.get_analytics()})

@app.route('/api/optimize', methods=['POST'])
def optimize():
    result = agent.run_optimization()
    return jsonify(result)

@app.route('/api/optimization-history', methods=['GET'])
def optimization_history():
    return jsonify(agent.get_optimization_history())

@app.route('/api/reset', methods=['POST'])
def reset():
    global agent
    agent = DemoAgent()
    session.clear()
    return jsonify({"status": "success"})

@app.route('/api/auto-simulation/start', methods=['POST'])
def start_auto_simulation():
    data = request.json or {}
    interval = data.get('interval', 1)
    batch_size = data.get('batch_size', 5)

    result = agent.start_auto_simulation(interval, batch_size)
    return jsonify(result)

@app.route('/api/auto-simulation/stop', methods=['POST'])
def stop_auto_simulation():
    result = agent.stop_auto_simulation()
    return jsonify(result)

@app.route('/api/auto-simulation/status', methods=['GET'])
def auto_simulation_status():
    return jsonify(agent.get_auto_simulation_status())


if __name__ == '__main__':
    print("\n" + "="*70)
    print("  🎭 DEMO MODE - No API Key Required!")
    print("="*70)
    print("\n✨ Running in demonstration mode with simulated responses")
    print("   This lets you explore the full UI without an API key!")
    print("\n🌐 Open your browser to: http://localhost:8080")
    print("\n📝 Note: This demo uses pre-built responses")
    print("   For real AI responses, use app_enhanced.py with an API key")
    print("\n⏹  Press Ctrl+C to stop")
    print("\n" + "="*70 + "\n")

    app.run(debug=False, host='0.0.0.0', port=8080, use_reloader=False)
