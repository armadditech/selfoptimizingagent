# Customization Guide

This guide walks you through customizing the self-optimizing agent for your specific business needs.

## Table of Contents

1. [Basic Configuration](#basic-configuration)
2. [Customizing Capabilities](#customizing-capabilities)
3. [Adding Custom Business Logic](#adding-custom-business-logic)
4. [Integrating with Your Systems](#integrating-with-your-systems)
5. [Customizing Prompts](#customizing-prompts)
6. [Adding New Capabilities](#adding-new-capabilities)
7. [Customizing the Learning Engine](#customizing-the-learning-engine)

## Basic Configuration

### 1. Create Your Configuration File

```bash
cp config/config.example.json config/config.json
```

### 2. Set Your API Key

Edit `config/config.json`:

```json
{
  "llm": {
    "api_key": "${ANTHROPIC_API_KEY}"
  }
}
```

Or set environment variable:

```bash
export ANTHROPIC_API_KEY="your_key_here"
```

### 3. Customize Business Information

```json
{
  "business": {
    "name": "Your Company",
    "industry": "retail",
    "support_email": "support@yourcompany.com",
    "support_phone": "1-800-YOUR-NUM"
  }
}
```

### 4. Customize Agent Personality

```json
{
  "agent": {
    "name": "Alex",
    "personality": "friendly and professional",
    "response_style": "concise but thorough",
    "tone": "empathetic"
  }
}
```

## Customizing Capabilities

### Enable/Disable Capabilities

In `config/config.json`:

```json
{
  "capabilities": {
    "orders": {
      "enabled": true
    },
    "returns": {
      "enabled": true
    },
    "products": {
      "enabled": false  // Disable if not needed
    }
  }
}
```

### Customize Order Handling

```json
{
  "capabilities": {
    "orders": {
      "enabled": true,
      "cancellation_window_hours": 48,  // Your policy
      "modification_allowed": true,
      "auto_track": true
    }
  }
}
```

### Customize Return Policy

```json
{
  "capabilities": {
    "returns": {
      "enabled": true,
      "return_window_days": 30,
      "free_return_shipping": true,
      "exchange_allowed": true,
      "restocking_fee": 0.0,
      "conditions": {
        "unopened": false,  // Your requirements
        "original_packaging": false,
        "receipt_required": false
      }
    }
  }
}
```

### Customize Refund Thresholds

```json
{
  "capabilities": {
    "refunds": {
      "auto_approve_threshold": 100.00,  // Your limit
      "manager_approval_threshold": 500.00,
      "processing_days": 5,
      "partial_refunds": true
    }
  }
}
```

## Adding Custom Business Logic

### Example: Custom Refund Policy

Create `config/custom_logic.py`:

```python
def custom_refund_policy(order):
    """
    Custom refund policy logic.
    Returns: "auto_approve", "manual_review", or "deny"
    """
    # VIP customers get instant approval
    if order.customer_tier == "VIP":
        return "auto_approve"
    
    # Large amounts need review
    if order.total > 1000:
        return "manual_review"
    
    # Recent orders auto-approved
    if order.age_days < 7:
        return "auto_approve"
    
    # Old orders need review
    if order.age_days > 60:
        return "deny"
    
    return "auto_approve"
```

Then import in your handler:

```python
# In src/capabilities/refunds.py
from config.custom_logic import custom_refund_policy

def _execute_action(self, action_name: str, params: Dict):
    if action_name == "process_refund":
        policy_result = custom_refund_policy(order)
        # Apply policy result...
```

### Example: Custom Order Validation

```python
def validate_order_cancellation(order):
    """Custom validation for order cancellations."""
    # Perishable items can't be cancelled
    if any(item.category == "perishable" for item in order.items):
        return False, "Perishable items cannot be cancelled"
    
    # Custom items need review
    if order.has_customization:
        return False, "Custom orders require manual review"
    
    # Shipped orders can't be cancelled
    if order.status == "shipped":
        return False, "Order has already shipped"
    
    return True, "OK"
```

## Integrating with Your Systems

### Shopify Integration

1. Add your credentials to `.env`:

```bash
SHOPIFY_API_KEY=your_key
SHOPIFY_STORE_URL=your-store.myshopify.com
```

2. Enable in config:

```json
{
  "integrations": {
    "ecommerce": {
      "enabled": true,
      "platform": "shopify",
      "api_endpoint": "https://your-store.myshopify.com/admin/api/2024-01",
      "api_key": "${SHOPIFY_API_KEY}"
    }
  }
}
```

3. Create `src/integrations/shopify.py`:

```python
import requests

class ShopifyIntegration:
    def __init__(self, config):
        self.api_key = config["api_key"]
        self.endpoint = config["api_endpoint"]
    
    def get_order(self, order_id):
        """Fetch order from Shopify."""
        url = f"{self.endpoint}/orders/{order_id}.json"
        headers = {"X-Shopify-Access-Token": self.api_key}
        response = requests.get(url, headers=headers)
        return response.json()
    
    def cancel_order(self, order_id, reason):
        """Cancel order in Shopify."""
        url = f"{self.endpoint}/orders/{order_id}/cancel.json"
        headers = {"X-Shopify-Access-Token": self.api_key}
        data = {"reason": reason}
        response = requests.post(url, headers=headers, json=data)
        return response.json()
```

### Custom CRM Integration

Create `src/integrations/your_crm.py`:

```python
class YourCRMIntegration:
    def __init__(self, config):
        self.api_key = config["api_key"]
        self.base_url = config["base_url"]
    
    def get_customer(self, customer_id):
        """Get customer data from your CRM."""
        # Your implementation
        pass
    
    def log_interaction(self, customer_id, interaction_data):
        """Log customer interaction to CRM."""
        # Your implementation
        pass
    
    def create_ticket(self, customer_id, issue_data):
        """Create support ticket."""
        # Your implementation
        pass
```

## Customizing Prompts

### Method 1: Update Handlers Directly

Edit `src/capabilities/orders.py`:

```python
def _build_system_prompt(self) -> str:
    return """You are a helpful order specialist for [YOUR COMPANY].

Our unique policies:
- [Your specific policy]
- [Your specific policy]

Your style:
- [Your brand voice]
- [Your tone guidelines]

Guidelines:
- [Your specific guidelines]
"""
```

### Method 2: Use Prompt Templates

Create `config/prompts/orders_prompt.txt`:

```
You are an order specialist for {company_name}.

Policies:
{order_policies}

Style: {agent_personality}

Current context:
{context}
```

Load in handler:

```python
from pathlib import Path

def _build_system_prompt(self) -> str:
    template = Path("config/prompts/orders_prompt.txt").read_text()
    return template.format(
        company_name=self.config["business"]["name"],
        order_policies=self._format_policies(),
        agent_personality=self.config["agent"]["personality"],
        context=self._get_context()
    )
```

## Adding New Capabilities

### Example: Adding "Warranty" Capability

1. Create `src/capabilities/warranty.py`:

```python
from typing import Dict, List, Optional, Any

class WarrantyHandler:
    """Handles warranty claims and inquiries."""
    
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
        """Handle warranty-related requests."""
        
        system_prompt = """You are a warranty specialist.
        
        Warranty Policy:
        - Standard warranty: 1 year
        - Extended warranty: available for purchase
        - Covers: manufacturing defects
        - Does not cover: user damage, normal wear
        
        Help customers with warranty claims and inquiries."""
        
        # ... implementation similar to other handlers
        
        return {
            "text": "Warranty response here",
            "actions": [],
            "needs_escalation": False
        }
```

2. Add to config:

```json
{
  "capabilities": {
    "warranty": {
      "enabled": true,
      "warranty_period_days": 365,
      "extended_available": true
    }
  }
}
```

3. Register in `src/agent.py`:

```python
from capabilities.warranty import WarrantyHandler

def _initialize_handlers(self):
    handlers = {}
    
    # ... existing handlers
    
    if capabilities["warranty"]["enabled"]:
        handlers["warranty"] = WarrantyHandler(
            self.llm_client,
            capabilities["warranty"]
        )
    
    return handlers
```

4. Update intent classifier in `src/core/intent_router.py`:

```python
def _get_capability_description(self, capability: str) -> str:
    descriptions = {
        # ... existing capabilities
        "warranty": "Warranty claims, coverage questions, extended warranty"
    }
    return descriptions.get(capability, "General inquiries")
```

## Customizing the Learning Engine

### Adjust Learning Parameters

```json
{
  "optimization": {
    "enabled": true,
    "learning_rate": 0.02,  // Higher = faster learning
    "min_interactions_for_learning": 100,  // Your threshold
    "feedback_weight": 0.8  // Emphasize feedback more
  }
}
```

### Custom Success Metrics

Edit `config/config.json`:

```json
{
  "optimization": {
    "success_metrics": {
      "resolution_rate": 0.5,  // 50% weight
      "customer_satisfaction": 0.3,  // 30% weight
      "response_time": 0.1,  // 10% weight
      "escalation_rate": 0.1  // 10% weight
    }
  }
}
```

### Add Custom Learning Logic

Create `config/custom_learning.py`:

```python
def custom_optimization_score(interaction):
    """Calculate custom optimization score."""
    score = 0
    
    # Reward fast responses
    if interaction["response_time"] < 3.0:
        score += 10
    
    # Reward high confidence
    if interaction["confidence"] > 0.8:
        score += 15
    
    # Penalize escalations
    if interaction["escalated"]:
        score -= 20
    
    # Reward positive feedback
    if interaction.get("feedback", {}).get("rating", 0) >= 4:
        score += 25
    
    return score
```

## Testing Your Customizations

### 1. Test Individual Capabilities

```python
# tests/test_custom.py
def test_warranty_handler():
    agent = CustomerServiceAgent()
    response = agent.handle_message(
        "I need to file a warranty claim"
    )
    assert response["intent"] == "warranty"
```

### 2. Test Custom Logic

```python
def test_custom_refund_policy():
    from config.custom_logic import custom_refund_policy
    
    vip_order = Order(customer_tier="VIP", total=100)
    assert custom_refund_policy(vip_order) == "auto_approve"
```

### 3. Run Full Test Suite

```bash
pytest tests/
```

## Next Steps

1. Start with basic configuration
2. Test with sample conversations
3. Add custom business logic gradually
4. Integrate with one system at a time
5. Monitor performance and adjust
6. Enable optimization after sufficient data

## Need Help?

- Check [docs/](docs/) for detailed documentation
- See [examples/](examples/) for code examples
- Open an issue on GitHub
- Contact support@example.com
