# Getting Started Guide

Welcome! This guide will help you get your self-optimizing customer service agent up and running in minutes.

## Prerequisites

- Python 3.11 or higher
- Anthropic API key ([get one here](https://console.anthropic.com/))
- 5 minutes of your time

## Quick Start (Automated)

Run the quickstart script:

```bash
chmod +x quickstart.sh
./quickstart.sh
```

This will:
- Create a virtual environment
- Install dependencies
- Set up configuration files
- Create data directories

## Manual Setup

### 1. Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 2. Configure the Agent

```bash
# Copy example configuration
cp config/config.example.json config/config.json

# Copy environment file
cp .env.example .env
```

Edit `.env` and add your API key:

```bash
ANTHROPIC_API_KEY=your_actual_api_key_here
```

### 3. Customize for Your Business (Optional)

Edit `config/config.json`:

```json
{
  "business": {
    "name": "Your Company Name",
    "support_email": "support@yourcompany.com"
  },
  "agent": {
    "name": "Your Agent Name",
    "personality": "your brand voice"
  }
}
```

See [CUSTOMIZATION.md](CUSTOMIZATION.md) for detailed customization options.

## Your First Conversation

### Interactive Mode

```bash
python src/agent.py
```

Example conversation:
```
Agent: Hi! I'm here to help you with orders, returns, products...

You: I want to track my order #12345

Agent: [Provides tracking information]

You: feedback
[Rate the conversation]

You: exit
```

### Programmatic Usage

```python
from src.agent import CustomerServiceAgent

# Initialize
agent = CustomerServiceAgent()

# Start conversation
agent.start_conversation(customer_id="customer_123")

# Handle message
response = agent.handle_message("Track my order #12345")
print(response['text'])

# Collect feedback
agent.collect_feedback(
    conversation_id=agent.conversation_id,
    rating=5,
    resolved=True
)
```

See [examples/basic_usage.py](examples/basic_usage.py) for more examples.

## API Server Mode

Run as a REST API:

```bash
python src/api_server.py
```

Server starts on http://localhost:8080

### API Endpoints

**Send a message:**
```bash
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Track my order #12345",
    "customer_id": "customer_123"
  }'
```

**Submit feedback:**
```bash
curl -X POST http://localhost:8080/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "conv_id",
    "rating": 5,
    "resolved": true
  }'
```

**Get analytics:**
```bash
curl http://localhost:8080/analytics?days=7
```

## Testing Different Capabilities

### Orders
```python
agent.handle_message("Track my order #ABC123")
agent.handle_message("Cancel order #ABC123")
agent.handle_message("When will my order arrive?")
```

### Returns
```python
agent.handle_message("I want to return this product")
agent.handle_message("How do I get a return label?")
agent.handle_message("Can I exchange this item?")
```

### Products
```python
agent.handle_message("Do you have wireless headphones?")
agent.handle_message("What's the difference between Model A and B?")
agent.handle_message("Is this product in stock?")
```

### Refunds
```python
agent.handle_message("I want a refund for order #XYZ")
agent.handle_message("How long does a refund take?")
agent.handle_message("Can I get store credit instead?")
```

### General
```python
agent.handle_message("What are your store hours?")
agent.handle_message("Where is your nearest location?")
agent.handle_message("What's your return policy?")
```

## Enable Self-Optimization

After collecting ~100 interactions, run the optimization cycle:

```bash
python src/agent.py --optimize
```

This will:
- Analyze performance metrics
- Run A/B tests
- Optimize prompts based on feedback
- Identify areas for improvement

View analytics:

```bash
python src/agent.py --analytics
```

## Configuration Overview

Key settings in `config/config.json`:

### Business Information
- Company name, contact info
- Support hours and channels

### Agent Behavior
- Personality and tone
- Response style
- Escalation thresholds

### Capabilities
- Enable/disable features
- Configure policies (returns, refunds)
- Set thresholds and limits

### Optimization
- Learning rate
- A/B testing settings
- Auto-prompt updates
- Feedback weights

### Integrations
- E-commerce platforms
- CRM systems
- Payment processors
- Shipping providers

## Next Steps

### 1. Test Thoroughly
- Try various customer scenarios
- Test edge cases
- Verify escalation triggers

### 2. Customize
- Adjust policies to match your business
- Customize prompts and responses
- Add custom business logic
- See [CUSTOMIZATION.md](CUSTOMIZATION.md)

### 3. Integrate
- Connect to your e-commerce platform
- Integrate with CRM
- Set up webhooks
- Configure authentication

### 4. Monitor & Optimize
- Collect customer feedback
- Review analytics regularly
- Run optimization cycles
- Adjust based on insights

### 5. Deploy
- Use Docker for containerization
- Deploy to cloud (AWS, GCP, Azure)
- Set up monitoring and alerts
- Configure auto-scaling

## Deployment Options

### Docker
```bash
docker build -t cs-agent .
docker run -p 8080:8080 --env-file .env cs-agent
```

### Cloud Platforms

**AWS Lambda:**
- Serverless deployment
- Pay per request
- Auto-scaling

**Google Cloud Run:**
- Container-based
- Auto-scaling
- Simple deployment

**Azure Functions:**
- Serverless option
- Easy integration with Azure services

See deployment docs for detailed instructions.

## Troubleshooting

### API Key Issues
```
Error: ANTHROPIC_API_KEY not found
```
**Solution:** Set your API key in `.env` file or export it:
```bash
export ANTHROPIC_API_KEY="your_key_here"
```

### Import Errors
```
ModuleNotFoundError: No module named 'anthropic'
```
**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

### Configuration Not Found
```
FileNotFoundError: Configuration file not found
```
**Solution:** Copy example config:
```bash
cp config/config.example.json config/config.json
```

### Low Confidence Responses
**Solution:** 
- Provide more training examples
- Adjust capability configurations
- Enable optimization after sufficient data

## Common Workflows

### Daily Operations
1. Monitor conversations
2. Review escalations
3. Analyze customer feedback
4. Update knowledge base

### Weekly Tasks
1. Review analytics
2. Run optimization cycle
3. Update configurations
4. Test new scenarios

### Monthly Tasks
1. Deep performance analysis
2. Review and update policies
3. Plan feature additions
4. Benchmark against goals

## Getting Help

- **Documentation:** Check [README.md](README.md) and [CUSTOMIZATION.md](CUSTOMIZATION.md)
- **Examples:** See [examples/basic_usage.py](examples/basic_usage.py)
- **Issues:** Open an issue on GitHub
- **Contributing:** See [CONTRIBUTING.md](CONTRIBUTING.md)

## Resources

- [Anthropic Documentation](https://docs.anthropic.com/)
- [Claude API Reference](https://docs.anthropic.com/en/api/)
- [Best Practices for AI Agents](https://docs.anthropic.com/en/docs/build-with-claude)

## What's Next?

Ready to build something amazing? Here are some ideas:

1. **Multi-language Support:** Add translation capabilities
2. **Voice Integration:** Connect with phone systems
3. **Sentiment Analysis:** Detect customer emotions
4. **Advanced Analytics:** Build custom dashboards
5. **Workflow Automation:** Automate common tasks
6. **Knowledge Base:** Add your own documentation
7. **Custom Capabilities:** Build domain-specific features

Happy building! 🚀

---

**Need more help?** Check out the documentation or open an issue on GitHub.
