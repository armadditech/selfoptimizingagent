# Project Structure

```
SelfOptimizingAgent/
├── README.md                      # Project overview and features
├── GETTING_STARTED.md             # Quick start guide
├── CUSTOMIZATION.md               # Detailed customization guide
├── CONTRIBUTING.md                # Contribution guidelines
├── LICENSE                        # MIT License
├── .gitignore                     # Git ignore rules
├── .env.example                   # Environment variables template
├── requirements.txt               # Python dependencies
├── package.json                   # NPM scripts and metadata
├── Dockerfile                     # Docker container definition
├── quickstart.sh                  # Automated setup script
│
├── config/                        # Configuration files
│   ├── config.example.json        # Example configuration (use as template)
│   └── config.json                # Your actual config (not in git)
│
├── src/                           # Source code
│   ├── __init__.py
│   ├── agent.py                   # Main agent orchestrator
│   ├── api_server.py              # REST API server
│   │
│   ├── core/                      # Core components
│   │   ├── __init__.py
│   │   ├── llm_client.py          # Claude API client with caching
│   │   ├── intent_router.py       # Intent classification and routing
│   │   └── context_manager.py     # Conversation state management
│   │
│   ├── capabilities/              # Feature handlers
│   │   ├── __init__.py
│   │   ├── orders.py              # Order tracking, cancellation, modification
│   │   ├── returns.py             # Return processing and exchanges
│   │   ├── products.py            # Product inquiries and recommendations
│   │   ├── refunds.py             # Refund processing
│   │   └── general.py             # General inquiries and FAQs
│   │
│   ├── optimization/              # Self-optimization engine
│   │   ├── __init__.py
│   │   ├── learning_engine.py     # Learning from interactions
│   │   └── analytics.py           # Performance tracking and metrics
│   │
│   └── integrations/              # External system integrations
│       ├── ecommerce.py           # E-commerce platform APIs (Shopify, etc.)
│       └── crm.py                 # CRM integrations (HubSpot, Zendesk, etc.)
│
├── data/                          # Data storage (not in git)
│   ├── conversations/             # Conversation history
│   ├── analytics/                 # Analytics data
│   ├── optimizations/             # Learning data
│   ├── feedback/                  # Customer feedback
│   └── knowledge_base/            # Custom knowledge base files
│
├── tests/                         # Test suite
│   ├── __init__.py
│   ├── test_agent.py              # Main agent tests
│   ├── test_capabilities.py       # Capability handler tests
│   ├── test_optimization.py       # Optimization tests
│   └── test_integrations.py       # Integration tests
│
├── examples/                      # Usage examples
│   ├── basic_usage.py             # Basic usage examples
│   ├── api_integration.py         # API integration examples
│   └── custom_capability.py       # Adding custom capabilities
│
├── logs/                          # Application logs (not in git)
│   └── agent.log
│
└── docs/                          # Additional documentation
    ├── architecture.md            # Architecture overview
    ├── api_reference.md           # API documentation
    ├── deployment.md              # Deployment guides
    └── troubleshooting.md         # Troubleshooting guide
```

## Key Components

### Main Agent (`src/agent.py`)
The central orchestrator that:
- Initializes all components
- Routes messages to appropriate handlers
- Manages conversation state
- Triggers optimization cycles
- Provides both interactive and API modes

### Core Components

#### LLM Client (`src/core/llm_client.py`)
- Handles all Claude API interactions
- Implements prompt caching for efficiency
- Supports streaming and tool use
- Manages extended thinking

#### Intent Router (`src/core/intent_router.py`)
- Classifies customer message intent
- Extracts entities (order IDs, amounts, etc.)
- Routes to appropriate capability handler
- Provides confidence scores

#### Context Manager (`src/core/context_manager.py`)
- Maintains conversation history
- Manages customer context across sessions
- Handles conversation persistence
- Implements memory retention policies

### Capability Handlers

Each handler is self-contained and follows the same interface:

**Orders Handler** (`src/capabilities/orders.py`)
- Order tracking
- Order cancellation
- Order modification
- Shipping information

**Returns Handler** (`src/capabilities/returns.py`)
- Return eligibility checking
- Return initiation
- Label generation
- Exchange processing

**Products Handler** (`src/capabilities/products.py`)
- Product search
- Availability checking
- Product recommendations
- Specifications and comparisons

**Refunds Handler** (`src/capabilities/refunds.py`)
- Refund processing with tiered approval
- Refund status checking
- Amount calculation
- Multiple refund methods

**General Handler** (`src/capabilities/general.py`)
- Company information
- Policy questions
- FAQs
- Store locations and contact info

### Optimization Engine

#### Learning Engine (`src/optimization/learning_engine.py`)
- Records all interactions
- Analyzes performance patterns
- Identifies improvement opportunities
- Runs A/B tests
- Updates prompts automatically
- Tracks prompt versions

#### Analytics (`src/optimization/analytics.py`)
- Tracks key performance metrics
- Generates performance reports
- Intent-level analytics
- Trend analysis
- Data export capabilities

## Data Flow

```
Customer Message
       ↓
Intent Classification
       ↓
Capability Handler Selection
       ↓
Context Retrieval
       ↓
LLM Processing (with caching)
       ↓
Response Generation
       ↓
Learning Engine Recording
       ↓
Response to Customer
```

## Configuration Structure

```json
{
  "business": { /* Your company info */ },
  "agent": { /* Agent personality and behavior */ },
  "llm": { /* Claude API settings */ },
  "capabilities": {
    "orders": { /* Order handling config */ },
    "returns": { /* Return policy config */ },
    "products": { /* Product handling config */ },
    "refunds": { /* Refund policy config */ },
    "general": { /* General settings */ }
  },
  "optimization": { /* Self-optimization settings */ },
  "conversation": { /* Context management */ },
  "escalation": { /* Escalation rules */ },
  "integrations": { /* External system configs */ },
  "analytics": { /* Analytics settings */ },
  "security": { /* Security settings */ },
  "logging": { /* Logging configuration */ }
}
```

## Deployment Artifacts

### Docker Container
- Self-contained application
- All dependencies included
- Environment-based configuration
- Ready for cloud deployment

### API Server
- RESTful endpoints
- JSON request/response
- Health checks
- CORS support

## Extension Points

### Adding New Capabilities
1. Create handler in `src/capabilities/`
2. Register in `src/agent.py`
3. Add configuration section
4. Update intent router

### Custom Integrations
1. Create integration in `src/integrations/`
2. Implement required methods
3. Add configuration
4. Use in capability handlers

### Custom Learning Logic
1. Extend `LearningEngine`
2. Override optimization methods
3. Add custom metrics
4. Implement custom A/B tests

## Performance Considerations

- **Prompt Caching**: Reduces API costs by 90%+ for repeated system prompts
- **Conversation Context**: Sliding window to manage token usage
- **Async Operations**: Parallel processing where possible
- **Data Persistence**: Efficient storage with JSONL format
- **Memory Management**: Automatic cleanup of old conversations

## Security Features

- **PII Masking**: Sensitive data protection
- **Rate Limiting**: Prevent abuse
- **Audit Logs**: Track all actions
- **Data Retention**: Configurable retention policies
- **API Key Security**: Environment-based configuration

## Scalability

- **Stateless Design**: Easy horizontal scaling
- **Distributed Caching**: Redis support for session state
- **Database Support**: PostgreSQL for production deployments
- **Load Balancing**: Multiple instance support
- **Queue Support**: Background job processing

## Monitoring

- **Health Checks**: `/health` endpoint
- **Metrics Export**: Prometheus-compatible
- **Log Aggregation**: Structured JSON logging
- **Error Tracking**: Detailed error reporting
- **Performance Monitoring**: Response time tracking
