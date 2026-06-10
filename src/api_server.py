#!/usr/bin/env python3
"""
API Server for customer service agent.
Provides REST API endpoints for integration with other systems.
"""

from flask import Flask, request, jsonify
from agent import CustomerServiceAgent
import os

app = Flask(__name__)

# Initialize agent
agent = CustomerServiceAgent()

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "version": "1.0.0"})


@app.route('/chat', methods=['POST'])
def chat():
    """
    Handle chat message.

    Request body:
    {
        "message": "customer message",
        "customer_id": "optional customer ID",
        "conversation_id": "optional conversation ID"
    }
    """
    data = request.json

    if not data or 'message' not in data:
        return jsonify({"error": "Message is required"}), 400

    message = data['message']
    customer_id = data.get('customer_id')
    conversation_id = data.get('conversation_id')

    try:
        # Start new conversation if needed
        if not conversation_id:
            agent.start_conversation(customer_id=customer_id, channel='api')

        # Handle message
        response = agent.handle_message(
            message=message,
            customer_id=customer_id
        )

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/feedback', methods=['POST'])
def feedback():
    """
    Submit feedback for a conversation.

    Request body:
    {
        "conversation_id": "conversation ID",
        "rating": 1-5,
        "feedback_text": "optional text",
        "resolved": true/false
    }
    """
    data = request.json

    if not data or 'conversation_id' not in data:
        return jsonify({"error": "conversation_id is required"}), 400

    try:
        agent.collect_feedback(
            conversation_id=data['conversation_id'],
            rating=data.get('rating'),
            feedback_text=data.get('feedback_text'),
            resolved=data.get('resolved', True)
        )

        return jsonify({"status": "success", "message": "Feedback recorded"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/analytics', methods=['GET'])
def analytics():
    """Get analytics summary."""
    try:
        days = request.args.get('days', default=7, type=int)
        summary = agent.get_analytics_summary()
        return jsonify(summary)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/optimize', methods=['POST'])
def optimize():
    """Trigger optimization cycle."""
    try:
        agent.run_optimization_cycle()
        return jsonify({
            "status": "success",
            "message": "Optimization cycle completed"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def main():
    """Start the API server."""
    port = int(os.getenv('PORT', 8080))
    host = os.getenv('HOST', '0.0.0.0')
    debug = os.getenv('DEBUG', '0') == '1'

    print(f"🚀 Starting Customer Service Agent API Server")
    print(f"📍 Server: http://{host}:{port}")
    print(f"🔧 Debug mode: {debug}")
    print()
    print("Available endpoints:")
    print("  GET  /health       - Health check")
    print("  POST /chat         - Handle customer message")
    print("  POST /feedback     - Submit feedback")
    print("  GET  /analytics    - Get analytics summary")
    print("  POST /optimize     - Run optimization cycle")
    print()

    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    main()
