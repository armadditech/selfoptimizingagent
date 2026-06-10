# Contributing to Self-Optimizing Agent

Thank you for your interest in contributing! This project welcomes contributions from the community.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Error messages or logs

### Suggesting Features

Feature requests are welcome! Please include:
- Clear description of the feature
- Use case and benefits
- Any implementation ideas

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
   - Follow existing code style
   - Add tests for new features
   - Update documentation as needed
4. **Run tests**
   ```bash
   pytest tests/
   ```
5. **Commit your changes**
   ```bash
   git commit -m "Add feature: description"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Open a Pull Request**

## Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/self-optimizing-agent.git
cd self-optimizing-agent

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies including dev tools
pip install -r requirements.txt

# Run tests
pytest tests/
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions focused and modular

Format code with:
```bash
black src/ tests/
flake8 src/ tests/
```

## Testing

- Write tests for new features
- Ensure existing tests pass
- Aim for good test coverage

Run tests:
```bash
# All tests
pytest tests/

# With coverage
pytest --cov=src tests/

# Specific test file
pytest tests/test_agent.py
```

## Documentation

When adding features:
- Update README.md if needed
- Add examples to examples/
- Update CUSTOMIZATION.md for configuration changes
- Add docstrings to new functions

## Pull Request Guidelines

- Clear, descriptive title
- Description of changes and motivation
- Link related issues
- Include tests
- Update documentation
- Ensure CI passes

## Community Guidelines

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Follow the code of conduct

## Questions?

Open an issue or discussion if you have questions about contributing.

Thank you for helping improve this project! 🙏
