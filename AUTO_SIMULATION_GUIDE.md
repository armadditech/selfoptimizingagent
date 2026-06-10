# Live Auto-Simulation Feature Guide

## Overview

The **Live Auto-Simulation** feature enables fully automated customer interaction simulation and self-optimization cycles, demonstrating the complete learning loop in real-time without manual intervention.

## 🎯 What It Does

The auto-simulation feature:

1. **Automatically generates** realistic customer interactions every few seconds
2. **Tracks performance** across all interaction types (orders, returns, products, refunds, general)
3. **Automatically optimizes** the agent every 20 interactions
4. **Updates analytics** in real-time
5. **Visualizes improvements** through the dashboard

## 🚀 How to Use

### Starting Auto-Simulation

#### Via Web UI
1. Open http://localhost:8080 in your browser
2. Scroll to the "Customer Simulator" section
3. Click the **"▶️ Start Auto-Simulation"** button
4. Watch the magic happen!

#### Via API
```bash
curl -X POST http://localhost:8080/api/auto-simulation/start \
  -H "Content-Type: application/json" \
  -d '{"interval": 5, "batch_size": 5}'
```

**Parameters:**
- `interval`: Seconds between batches (default: 5)
- `batch_size`: Number of interactions per batch (default: 5)

### Stopping Auto-Simulation

#### Via Web UI
- Click the **"⏸️ Stop Auto-Simulation"** button

#### Via API
```bash
curl -X POST http://localhost:8080/api/auto-simulation/stop
```

### Checking Status

```bash
curl http://localhost:8080/api/auto-simulation/status
```

**Response:**
```json
{
    "active": true,
    "stats": {
        "start_time": "2026-06-04T20:51:26.217574",
        "last_activity": "2026-06-04T20:51:50.263893",
        "total_simulated": 45,
        "total_optimizations": 2
    }
}
```

## 📊 What Happens During Auto-Simulation

### Phase 1: Interaction Generation (Every 3-5 seconds)
- Generates 5 realistic customer queries
- Simulates various scenarios:
  - Order tracking requests
  - Return inquiries
  - Product availability questions
  - Refund requests
  - General support questions
- Collects simulated customer feedback (ratings & resolution status)

### Phase 2: Performance Tracking
- Updates real-time analytics:
  - Total interactions count
  - Intent distribution
  - Confidence scores
  - Satisfaction ratings
  - Resolution rates

### Phase 3: Automatic Optimization (Every 20 interactions)
- **Analyzes** recent performance data
- **Identifies** low-confidence patterns
- **Runs** A/B testing simulation
- **Applies** improvements to the agent
- **Records** optimization history
- **Increments** version number

## 📈 Real-Time Monitoring

The dashboard displays:

### Status Panel
- **Status:** 🟢 Active / 🔴 Stopped
- **Interactions:** Live count of simulated interactions
- **Optimizations:** Number of optimization cycles completed
- **Info:** Configuration (batch size, interval)

### Analytics Updates
All analytics charts update automatically:
- Intent distribution pie chart
- Confidence levels
- Satisfaction trends
- Resolution rates

### Optimization History
- Version progression
- Issues identified
- Improvements applied
- A/B test results
- Performance metrics before/after

## 🧪 Testing the Feature

### Quick Test (30 seconds)
```bash
# Start auto-simulation
curl -X POST http://localhost:8080/api/auto-simulation/start \
  -H "Content-Type: application/json" \
  -d '{"interval": 3, "batch_size": 10}'

# Wait and check progress
sleep 10
curl http://localhost:8080/api/auto-simulation/status

# Check analytics
curl http://localhost:8080/api/analytics

# Stop
curl -X POST http://localhost:8080/api/auto-simulation/stop
```

### Extended Demo (2-3 minutes)
```bash
# Start with slower pace for observation
curl -X POST http://localhost:8080/api/auto-simulation/start \
  -H "Content-Type: application/json" \
  -d '{"interval": 5, "batch_size": 5}'

# Wait for multiple optimization cycles
sleep 120

# Check results
curl http://localhost:8080/api/optimization-history

# Stop
curl -X POST http://localhost:8080/api/auto-simulation/stop
```

## 🎓 Use Cases

### 1. Live Demonstrations
- Show the complete self-optimization cycle
- Demonstrate continuous learning
- Visualize improvement over time

### 2. Testing & Development
- Quickly generate test data
- Validate optimization logic
- Test system under load

### 3. Performance Analysis
- Observe long-term trends
- Identify optimization patterns
- Compare different configurations

### 4. Training & Education
- Teach ML concepts
- Show real-world AI improvement
- Demonstrate feedback loops

## 🔧 Configuration Options

### Batch Size
- **Small (1-3):** Slow, detailed observation
- **Medium (5-10):** Balanced demo pace
- **Large (20+):** Rapid data generation

### Interval
- **Fast (1-2s):** Quick demos, stress testing
- **Medium (3-5s):** Comfortable observation
- **Slow (10s+):** Detailed analysis

### Recommended Settings

**Live Demo:**
```json
{"interval": 5, "batch_size": 5}
```
- Generates ~60 interactions/minute
- 3 optimization cycles in 2 minutes
- Easy to follow

**Stress Test:**
```json
{"interval": 1, "batch_size": 20}
```
- Generates ~1200 interactions/minute
- Rapid optimization cycles
- Tests system performance

**Detailed Analysis:**
```json
{"interval": 10, "batch_size": 3}
```
- Generates ~18 interactions/minute
- Slower, more observable
- Good for debugging

## 📝 Example Output

### Console Output (Server Side)
```
🤖 Auto-simulation started: 5 interactions every 5s
✨ Optimization #1 complete - Version 2
✨ Optimization #2 complete - Version 3
🛑 Auto-simulation stopped
```

### API Response (Status Check)
```json
{
    "active": true,
    "stats": {
        "start_time": "2026-06-04T20:51:26",
        "last_activity": "2026-06-04T20:51:50",
        "total_simulated": 45,
        "total_optimizations": 2
    }
}
```

### Optimization Result
```json
{
    "version": 2,
    "issues_found": [
        "general: 100% low confidence"
    ],
    "improvements": [
        "Optimized general handler: Added examples and guidelines"
    ],
    "ab_test": {
        "winner": "variant_b",
        "improvement": 0.07
    },
    "before": {
        "satisfaction": 3.95,
        "resolution": 0.75
    },
    "after": {
        "satisfaction": 4.15,
        "resolution": 0.80
    }
}
```

## 🎨 UI Features

### Visual Indicators
- 🟢 Green: Active simulation
- 🔴 Red: Stopped
- 📊 Charts update in real-time
- 🎭 Simulation log shows activity

### Interactive Elements
- One-click start/stop
- Live statistics display
- Auto-refreshing analytics
- Optimization history timeline

## 🔒 Safety Features

- **Thread-safe:** Uses daemon threads
- **Clean shutdown:** Stops gracefully
- **Error handling:** Continues on errors
- **Resource-friendly:** Configurable pace

## 🚧 Troubleshooting

### Auto-simulation won't start
- Check if already running: `GET /api/auto-simulation/status`
- Restart the server
- Check server logs for errors

### No optimizations happening
- Need at least 10 interactions before first optimization
- Optimizations run every 20 interactions
- Check optimization history for details

### High resource usage
- Reduce batch_size
- Increase interval
- Stop simulation when not needed

## 🎯 Next Steps

After testing auto-simulation:

1. **Customize scenarios** in `EnhancedAgent.simulate_customers()`
2. **Adjust optimization logic** in `EnhancedAgent.run_optimization()`
3. **Add real API integration** to replace simulation
4. **Implement persistence** for optimization history
5. **Add alerting** for performance degradation

## 💡 Tips

- **Start slow:** Use 5-10 second intervals for first run
- **Watch the logs:** Console shows optimization triggers
- **Compare versions:** Check optimization history for improvements
- **Reset between demos:** Use `/api/reset` for clean slate
- **Combine features:** Mix manual and auto simulation

---

**Feature Status:** ✅ Fully Functional

**Tested:** June 4, 2026

**Endpoints:**
- `POST /api/auto-simulation/start` - Start simulation
- `POST /api/auto-simulation/stop` - Stop simulation
- `GET /api/auto-simulation/status` - Check status
