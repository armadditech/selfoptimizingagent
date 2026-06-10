# 🤖 Self-Optimizing Customer Service Agent

A powerful AI-powered customer service agent that continuously learns and improves from interactions. Built with Claude AI (Anthropic), featuring real-time simulation, live conversation feeds, and automatic optimization cycles.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.11+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## ✨ Key Features

### 🎯 Core Capabilities
- **Multi-Intent Handling**: Orders, returns, products, refunds, and general inquiries
- **Self-Optimization**: Automatically improves performance every 10 seconds
- **Context Awareness**: Maintains conversation history and customer context
- **Entity Extraction**: Automatically identifies order IDs, products, and key information

### 📊 Real-Time Web Dashboard
- **Live Auto-Simulation**: Generates 5 interactions per second
- **Conversation Feed**: Watch actual customer interactions in real-time
- **Analytics Dashboard**: Track performance metrics as they update
- **Optimization History**: See improvements over time with version tracking
- **Interactive Counters**: Animated displays with countdowns and timers

### 🧠 Learning & Improvement
- **A/B Testing**: Automatically tests different response strategies
- **Performance Tracking**: Monitors satisfaction, resolution rate, and confidence
- **Issue Detection**: Identifies low-confidence patterns
- **Auto-Optimization**: Applies improvements without manual intervention

### 🎨 Modern UI
- Real-time updates every 0.5 seconds
- Color-coded intent badges
- Smooth animations and transitions
- Responsive design
- Professional look and feel

## 🎭 Try Demo Mode First! (No API Key Needed)

**Want to see it working RIGHT NOW?**

```bash
# Clone and enter directory
git clone https://github.com/deepak-mukunthu/SelfOptimizingAgent.git
cd SelfOptimizingAgent

# Install dependencies
pip install -r requirements.txt

# Run demo mode - NO API KEY REQUIRED!
python demo_mode.py
```

Open `http://localhost:8080` → Click **"Start Auto-Simulation"** → Watch the magic! ✨

The demo mode has ALL features working with pre-built responses. Perfect for:
- 🎯 Quick evaluation (try it in 2 minutes!)
- 📚 Learning how it works
- 🎤 Presentations without API costs
- 👥 Sharing with others

👉 **Full demo guide:** [DEMO_MODE.md](DEMO_MODE.md)

---

## 🚀 Full Installation (Real AI with Claude)

Ready for actual AI responses? Follow these steps:

### Prerequisites

- Python 3.11 or higher
- Anthropic API key ([Get one here](https://console.anthropic.com/))
- Modern web browser

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/deepak-mukunthu/SelfOptimizingAgent.git
   cd SelfOptimizingAgent
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your API key:**
   ```bash
   cp .env.example .env
   # Edit .env and add your Anthropic API key
   ```
   
   ⚠️ **IMPORTANT**: Never commit your `.env` file to Git! See [SECURITY.md](SECURITY.md) for details.

5. **Run the application:**
   ```bash
   python app_enhanced.py
   ```

6. **Open your browser:**
   ```
   http://localhost:8080
   ```

7. **Start auto-simulation:**
   - Click "▶️ Start Auto-Simulation"
   - Watch the magic happen!

## 🎯 What You'll See

### Live Conversation Feed
Real customer interactions appearing in real-time:
```
👤 "Where is my order #12345?"
🤖 "I found your order! It's in transit with UPS..."
📦 orders | ⭐ 95% confidence | v2
```

### Real-Time Metrics
- **Total Interactions**: Climbing every second
- **Optimizations**: New cycle every 10 seconds
- **Satisfaction Score**: 4.6/5.0 and improving
- **Resolution Rate**: 85%+ success rate

### Optimization Cards
See improvements as they happen:
```
⚡ Version 2 - Optimization Complete
✅ Identified: general queries at 100% low confidence
✅ Applied: Added examples and guidelines
📈 Results: Satisfaction 3.95 → 4.15 (+5%)
```

## 📖 Documentation

- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Detailed setup guide
- **[FEATURES.md](FEATURES.md)** - Complete feature list
- **[CUSTOMIZATION.md](CUSTOMIZATION.md)** - How to customize for your business
- **[AUTO_SIMULATION_GUIDE.md](AUTO_SIMULATION_GUIDE.md)** - Auto-simulation documentation
- **[REAL_TIME_FEATURES.md](REAL_TIME_FEATURES.md)** - Real-time UI features
- **[LIVE_CONVERSATION_FEED.md](LIVE_CONVERSATION_FEED.md)** - Conversation feed guide
- **[SECURITY.md](SECURITY.md)** - ⚠️ Security best practices (READ THIS!)
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions

## 🎓 Use Cases

### Live Demonstrations
Perfect for showing stakeholders how AI handles customer service in real-time with visible improvements.

### Rapid Prototyping
Quickly test different customer service scenarios and see results immediately.

### Education & Training
Teach AI concepts with live visualization of intent classification, entity extraction, and machine learning.

### Development & Testing
Rapidly generate test data and validate changes with instant feedback.

## 🛠️ Technology Stack

- **AI**: Claude 4 (Anthropic)
- **Backend**: Python 3.11+, Flask
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Real-time Updates**: Server-sent events via polling
- **Threading**: Python threading for background simulation

## 📊 Performance

- **Generation Speed**: 5 interactions/second
- **Optimization Frequency**: Every 10 seconds
- **UI Update Rate**: Every 0.5 seconds
- **Response Time**: <10ms per request
- **Concurrent Users**: Supports multiple simultaneous users

## 🔒 Security

**⚠️ CRITICAL**: This project requires an API key that must be kept secret.

- Never commit `.env` files
- Never hardcode API keys
- See [SECURITY.md](SECURITY.md) for complete guidelines
- Monitor your API usage at [Anthropic Console](https://console.anthropic.com/)

## 🎨 Customization

The agent is highly customizable:

- **Business Information**: Company name, policies, hours
- **Product Catalog**: Add your products and inventory
- **Response Tone**: Adjust personality and style
- **Optimization Settings**: Configure learning parameters
- **UI Theming**: Modify colors and layout

See [CUSTOMIZATION.md](CUSTOMIZATION.md) for detailed instructions.

## 📈 Roadmap

- [ ] Persistent storage (database integration)
- [ ] Multi-language support
- [ ] Voice interface
- [ ] Advanced analytics dashboard
- [ ] Custom training on your data
- [ ] Slack/Teams integration
- [ ] Mobile app

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Claude](https://www.anthropic.com/claude) by Anthropic
- Inspired by modern customer service automation needs
- Community feedback and contributions

## 📞 Support

- **Documentation**: Check the `/docs` folder
- **Issues**: [GitHub Issues](https://github.com/deepak-mukunthu/SelfOptimizingAgent/issues)
- **Discussions**: [GitHub Discussions](https://github.com/deepak-mukunthu/SelfOptimizingAgent/discussions)

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

## 🎉 Demo

Want to see it in action? Check out the [demo video](link-to-demo) or:

1. Clone the repo
2. Add your API key
3. Run `python app_enhanced.py`
4. Open `http://localhost:8080`
5. Click "Start Auto-Simulation"
6. Watch the magic! ✨

---

**Made with ❤️ and AI** | [Report Bug](https://github.com/deepak-mukunthu/SelfOptimizingAgent/issues) | [Request Feature](https://github.com/deepak-mukunthu/SelfOptimizingAgent/issues)
