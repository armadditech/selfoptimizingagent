# Self-Optimizing Customer Service Agent

A comprehensive, customizable AI-powered customer service agent that handles orders, returns, product inquiries, refunds, and general questions. The agent continuously learns and optimizes its performance based on real interactions.

## Features

- **Multi-Capability Support**: Orders, returns, product Q&A, refunds, and general inquiries
- **Self-Optimization**: Learns from successful and failed interactions
- **Easy Customization**: Configuration-driven setup for any business
- **Conversation Memory**: Maintains context across interactions
- **Analytics Dashboard**: Track performance and identify improvements
- **A/B Testing**: Test different response strategies
- **Escalation Logic**: Smart handoff to human agents when needed
- **Multi-Channel Ready**: Works with chat, email, or API integrations

## Quick Start

### 1. Installation

```bash
npm install
# or
pip install -r requirements.txt
```

### 2. Configuration

Copy the example configuration and customize for your business:

```bash
cp config/config.example.json config/config.json
```

Edit `config/config.json` with your:
- API keys
- Business information
- Product catalog
- Policy details
- Customization preferences

### 3. Run the Agent

```bash
# Interactive mode
npm start

# API server mode
npm run serve

# Python version
python src/agent.py
```

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Customer Input                      │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│           Intent Classifier & Router                 │
│  (Determines: Order/Return/Product/Refund/General)  │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│              Capability Handlers                     │
├─────────────┬─────────────┬─────────────┬──────────┤
│   Orders    │   Returns   │  Products   │ Refunds  │
└──────┬──────┴──────┬──────┴──────┬──────┴────┬─────┘
       │             │              │           │
       └─────────────┴──────┬───────┴───────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────┐
│            Response Generator                        │
│     (Context-aware, personalized responses)         │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│         Self-Optimization Engine                     │
│  • Tracks success/failure rates                     │
│  • A/B tests response strategies                    │
│  • Updates prompts based on feedback                │
│  • Identifies improvement patterns                  │
└─────────────────────────────────────────────────────┘
```

## Directory Structure

```
.
├── config/                 # Configuration files
│   ├── config.example.json # Example configuration
│   ├── prompts/           # Prompt templates
│   └── policies/          # Business policies
├── src/
│   ├── agent.py           # Main agent orchestrator
│   ├── core/
│   │   ├── llm_client.py  # Claude API integration
│   │   ├── intent_router.py # Intent classification
│   │   └── context_manager.py # Conversation state
│   ├── capabilities/
│   │   ├── orders.py      # Order management
│   │   ├── returns.py     # Return processing
│   │   ├── products.py    # Product inquiries
│   │   ├── refunds.py     # Refund handling
│   │   └── general.py     # General questions
│   ├── optimization/
│   │   ├── learning_engine.py # Self-optimization
│   │   ├── ab_testing.py      # Strategy testing
│   │   └── analytics.py       # Performance tracking
│   └── integrations/
│       ├── ecommerce.py   # E-commerce platform APIs
│       └── crm.py         # CRM integrations
├── data/
│   ├── conversations/     # Interaction logs
│   ├── feedback/          # Customer feedback
│   └── optimizations/     # Learning data
├── tests/                 # Test suites
└── docs/                  # Documentation
```

## Configuration Guide

### Basic Setup

```json
{
  "business": {
    "name": "Your Company Name",
    "industry": "retail",
    "support_email": "support@example.com",
    "support_hours": "24/7"
  },
  "agent": {
    "name": "Support Agent",
    "personality": "friendly and professional",
    "response_style": "concise",
    "escalation_threshold": 3
  }
}
```

### Capability Configuration

Each capability can be customized independently:

- **Orders**: Track, cancel, modify orders
- **Returns**: Process returns based on your policy
- **Products**: Answer questions, recommend items
- **Refunds**: Handle refund requests and processing
- **General**: Company info, policies, FAQs

### Self-Optimization Settings

```json
{
  "optimization": {
    "enabled": true,
    "learning_rate": 0.01,
    "ab_testing": true,
    "feedback_weight": 0.7,
    "auto_update_prompts": true,
    "review_interval_hours": 24
  }
}
```

## Self-Optimization Features

### 1. Success Pattern Learning
- Tracks which responses lead to customer satisfaction
- Identifies successful phrasing and approaches
- Automatically incorporates winning patterns

### 2. Failure Analysis
- Detects when customers are frustrated
- Identifies common failure points
- Adjusts strategies to avoid similar issues

### 3. A/B Testing
- Tests multiple response strategies
- Statistically validates improvements
- Gradually shifts to better approaches

### 4. Prompt Evolution
- Continuously refines system prompts
- Adapts to changing customer needs
- Maintains version history for rollback

## Usage Examples

### Interactive Chat

```python
from src.agent import CustomerServiceAgent

agent = CustomerServiceAgent()
agent.start_conversation()

# Customer: "I want to return a product I bought last week"
# Agent: [Analyzes intent → Routes to Returns → Processes request]
```

### API Integration

```python
from src.agent import CustomerServiceAgent

agent = CustomerServiceAgent()
response = agent.handle_message(
    message="Track my order #12345",
    customer_id="cust_789",
    context={}
)
```

### Batch Processing

```python
from src.agent import CustomerServiceAgent

agent = CustomerServiceAgent()
results = agent.process_batch(
    messages_file="customer_inquiries.json",
    output_file="responses.json"
)
```

## Analytics & Monitoring

View performance metrics:

```bash
npm run analytics
# or
python src/analytics.py --dashboard
```

Metrics tracked:
- Resolution rate by category
- Average response time
- Customer satisfaction scores
- Escalation rates
- Self-optimization improvements

## Customization Examples

### Adding a New Capability

1. Create handler in `src/capabilities/`
2. Register in `config/capabilities.json`
3. Add training examples
4. Test and deploy

### Custom Business Logic

```python
# config/custom_logic.py
def custom_refund_policy(order):
    if order.age_days > 30:
        return "outside_policy"
    if order.total > 500:
        return "requires_approval"
    return "auto_approve"
```

### Integration with Your Systems

```python
# src/integrations/your_system.py
class YourSystemIntegration:
    def get_order(self, order_id):
        # Your implementation
        pass
    
    def process_refund(self, order_id, amount):
        # Your implementation
        pass
```

## Testing

```bash
# Run all tests
npm test

# Test specific capability
python -m pytest tests/test_orders.py

# Run optimization simulation
python tests/optimization_test.py
```

## Deployment

### Docker

```bash
docker build -t cs-agent .
docker run -p 8080:8080 cs-agent
```

### Cloud Deployment

- AWS Lambda ready
- Google Cloud Functions compatible
- Azure Functions supported

## Best Practices

1. **Start with conservative settings** and gradually enable optimization
2. **Monitor the first 100 conversations** closely before full automation
3. **Regularly review escalated conversations** to improve handling
4. **Update your product/policy data** to keep responses accurate
5. **Set up feedback loops** to capture customer satisfaction

## Troubleshooting

See [docs/troubleshooting.md](docs/troubleshooting.md) for common issues and solutions.

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Support

- Documentation: [docs/](docs/)
- Issues: GitHub Issues
- Email: support@example.com
