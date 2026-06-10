# Web UI for Self-Optimizing Agent

Beautiful web interface to visualize and interact with the self-optimizing customer service agent.

## 🎨 Two UI Options

### Option 1: Basic Chat UI (Port 5000)
- Interactive chat interface
- Real-time intent classification
- Live analytics dashboard
- Confidence scoring
- Intent breakdown visualization

### Option 2: Enhanced UI with Self-Optimization (Port 5001)
- Everything from Basic UI, plus:
- **Customer Simulator** - Simulate 10, 50, or 100 customer interactions
- **Automated Feedback** - Simulated customer ratings and feedback
- **Self-Optimization Engine** - Watch the agent learn and improve
- **A/B Testing** - See different strategies tested
- **Optimization History** - Track improvements over time
- **Performance Metrics** - Real-time satisfaction and resolution rates

## 🚀 Quick Start

### Method 1: Use the startup script
```bash
./run_ui.sh
```

Then choose option 1 or 2.

### Method 2: Run directly

**Basic UI:**
```bash
source venv/bin/activate
python3 app.py
# Open http://localhost:5000
```

**Enhanced UI:**
```bash
source venv/bin/activate
python3 app_enhanced.py
# Open http://localhost:5001
```

## 🎯 Using the Enhanced UI

### 1. Try the Chat
- Type messages in the chat box
- Watch real-time intent classification
- See confidence scores
- View entity extraction

### 2. Simulate Customers
- Click "Simulate 10 Customers" button
- Watch automated customer interactions
- See feedback being collected
- Analytics update in real-time

### 3. Run Optimization
- After simulating customers (need at least 10)
- Click "Run Optimization Cycle"
- Watch the agent analyze performance
- See improvements being applied
- View A/B test results

### 4. Track Learning
- Scroll down to see Optimization History
- Each version shows:
  - Issues found
  - Improvements made
  - A/B test winners
  - Performance gains

## 📊 What You'll See

### Analytics Dashboard
- **Total Interactions** - Running count
- **Satisfaction Score** - Customer ratings (1-5)
- **Resolution Rate** - % of issues resolved
- **Escalation Rate** - % requiring human intervention

### Intent Breakdown
Visual chart showing distribution across:
- Orders (green)
- Returns (orange)
- Products (blue)
- Refunds (purple)
- General (gray)

### Simulation Log
Real-time log of simulated interactions:
- Customer message
- Detected intent
- Customer rating
- Resolution status

### Optimization Results
When you run optimization, you'll see:
- Issues identified (e.g., "returns: 22% low confidence")
- Improvements applied (e.g., "Added examples to returns handler")
- A/B test results (which strategy won)
- Before/after performance metrics
- Version number

## 🎬 Demo Scenario

Here's a complete demo flow:

1. **Start the Enhanced UI**
   ```bash
   ./run_ui.sh
   # Choose option 2
   ```

2. **Try Manual Chat** (optional)
   - Type: "Track my order #12345"
   - See instant response with intent classification

3. **Simulate Initial Customers**
   - Click "Simulate 50 Customers"
   - Watch the log fill with interactions
   - See analytics update

4. **Run First Optimization**
   - Click "Run Optimization Cycle"
   - See version 2 deployed
   - Note the improvements

5. **Simulate More Customers**
   - Click "Simulate 50 Customers" again
   - New customers experience improved agent

6. **Run Second Optimization**
   - Click "Run Optimization Cycle" again
   - See version 3 deployed
   - Compare versions in history

7. **Review Progress**
   - Scroll to Optimization History
   - See how each version improved
   - Compare satisfaction and resolution rates

## 🎨 UI Features

### Beautiful Design
- Gradient purple theme
- Smooth animations
- Responsive layout
- Real-time updates

### Chat Interface
- User messages on right (purple gradient)
- Agent messages on left (white with shadow)
- Intent badges with colors
- Confidence bars
- Response time indicators

### Analytics Cards
- Large, easy-to-read numbers
- Color-coded metrics
- Progress bars
- Live updates

### Simulation Log
- Color-coded entries (green=success, orange=warning)
- Monospace font for clarity
- Scrollable history
- Detailed per-interaction data

## 🧪 Test Scenarios

Try these messages in the chat:

**Orders:**
- "Track my order #12345"
- "Cancel order #ABC123"
- "When will my package arrive?"

**Returns:**
- "I want to return this product"
- "How do I get a return label?"
- "Can I exchange this item?"

**Products:**
- "Do you have wireless headphones?"
- "What's in stock?"
- "Recommend a product for me"

**Refunds:**
- "I need a refund for order #XYZ"
- "Where's my money?"
- "Process a refund please"

**Escalation:**
- "I want to speak to a manager"
- "This is terrible service!"
- "Connect me with a human"

## 📈 Understanding the Optimization

### What Gets Optimized

1. **Intent Classification** - Better understanding of messages
2. **Response Quality** - More helpful answers
3. **Confidence Scores** - More accurate classifications
4. **Resolution Rates** - More issues solved without escalation

### How It Learns

1. **Collects Data** - Every interaction tracked
2. **Analyzes Patterns** - Finds what works and what doesn't
3. **Runs A/B Tests** - Tests different approaches
4. **Applies Improvements** - Deploys winning strategies
5. **Tracks Results** - Measures performance gains

### Metrics to Watch

- **Satisfaction**: Should increase over versions
- **Resolution Rate**: Should increase over versions
- **Escalation Rate**: Should decrease over versions
- **Confidence**: Should increase for each intent

## 🔧 Troubleshooting

**UI won't start:**
```bash
# Check if port is in use
lsof -i :5000  # or :5001
# Kill if needed, then restart
```

**Dependencies missing:**
```bash
source venv/bin/activate
pip install flask flask-cors --upgrade
```

**Analytics not updating:**
- Refresh the browser
- Check browser console for errors
- Restart the server

## 🎯 Next Steps

After exploring the UI:

1. **Customize** - Edit `app_enhanced.py` to change logic
2. **Integrate** - Connect to real Claude API (set ANTHROPIC_API_KEY)
3. **Deploy** - Use Docker or cloud platform
4. **Extend** - Add more capabilities or features

## 📝 Notes

- The UI uses **simulated responses** by default (no API needed)
- To use real Claude API, set environment variable and modify `app_enhanced.py`
- All data is in-memory (resets on restart)
- For production, add database persistence

## 🎉 Enjoy!

You now have a beautiful, interactive way to see the self-optimizing agent in action. Watch it learn, improve, and get better over time!

---

**Created with:** Flask, HTML5, CSS3, JavaScript
**Powered by:** Self-Optimizing Agent System
