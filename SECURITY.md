# Security Guidelines

## 🔐 API Key Security

### ⚠️ NEVER commit your API keys to GitHub!

This project requires an Anthropic API key to function. **API keys are sensitive credentials** and should never be committed to version control.

### How to Securely Configure

1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Add your API key to `.env`:**
   ```bash
   ANTHROPIC_API_KEY=your_actual_api_key_here
   ```

3. **Verify `.env` is in `.gitignore`:**
   ```bash
   cat .gitignore | grep ".env"
   ```
   You should see `.env` listed (without the `.example` extension)

### Getting Your API Key

1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Generate a new key
5. Copy it to your `.env` file immediately
6. **Never share this key publicly**

### What's Protected

The following files are automatically excluded from Git:
- `.env` - Your actual API key
- `.env.local` - Local overrides
- `.env.production` - Production credentials
- `*.log` - May contain sensitive data
- `server.pid` - Runtime process IDs
- `.claude/` - Personal IDE settings

### What's Safe to Commit

- `.env.example` - Template without real keys
- `*.py` - Source code (no keys hardcoded)
- `*.md` - Documentation
- `requirements.txt` - Dependencies

## 🛡️ Best Practices

### Do's ✅

- ✅ Use environment variables for all secrets
- ✅ Keep `.env` in `.gitignore`
- ✅ Rotate API keys periodically
- ✅ Use different keys for development/production
- ✅ Set usage limits on your API keys
- ✅ Monitor your API usage regularly

### Don'ts ❌

- ❌ Never hardcode API keys in Python files
- ❌ Never commit `.env` to Git
- ❌ Never share API keys in issues or pull requests
- ❌ Never post keys in screenshots
- ❌ Never use production keys for testing
- ❌ Never commit log files that might contain keys

## 🚨 What to Do If You Accidentally Commit a Key

If you accidentally commit an API key:

1. **Immediately revoke the key:**
   - Go to [Anthropic Console](https://console.anthropic.com/)
   - Delete the exposed key

2. **Generate a new key:**
   - Create a replacement key
   - Update your `.env` file

3. **Remove from Git history:**
   ```bash
   # This is complex - consider these options:
   # Option 1: Remove the commit (if not pushed)
   git reset --soft HEAD~1
   
   # Option 2: Use git filter-branch (if pushed)
   # Contact GitHub support for help
   ```

4. **Notify:**
   - If this is a shared repository, notify all collaborators
   - Consider the key compromised

## 💰 Cost Management

### API Usage Monitoring

- Check your usage at [Anthropic Console](https://console.anthropic.com/settings/usage)
- Set up billing alerts
- Use rate limiting in production

### Free Tier Considerations

- Understand your plan's limits
- The auto-simulation feature can consume tokens quickly
- Run simulations in moderation during testing
- Stop auto-simulation when not actively demonstrating

### Recommended Settings for Testing

```python
# Slower simulation = lower cost
{"interval": 5, "batch_size": 3}  # ~36 interactions/min

# Stop after testing
# Don't leave running overnight
```

## 🔒 Production Deployment

### Additional Security Measures

1. **Use separate API keys:**
   ```bash
   # Development
   ANTHROPIC_API_KEY=sk-ant-dev-...
   
   # Production
   ANTHROPIC_API_KEY=sk-ant-prod-...
   ```

2. **Environment-specific configs:**
   - Use `.env.development`
   - Use `.env.production`
   - Never commit either

3. **Access control:**
   - Limit who has access to production keys
   - Use key rotation policies
   - Implement audit logging

4. **Secrets management:**
   - Consider using AWS Secrets Manager
   - Or HashiCorp Vault
   - Or your cloud provider's solution

## 📋 Pre-Push Checklist

Before pushing to GitHub, verify:

- [ ] No API keys in code
- [ ] `.env` is in `.gitignore`
- [ ] No `.env` file staged for commit
- [ ] No log files with sensitive data
- [ ] No hardcoded credentials anywhere
- [ ] `.env.example` has placeholder values only

### Quick Check Command

```bash
# Search for potential API keys in staged files
git diff --cached | grep -i "sk-ant"

# If this returns anything, DON'T PUSH!
```

## 🆘 Support

If you have security concerns:
- Open an issue (without posting sensitive data)
- Review Anthropic's [security best practices](https://docs.anthropic.com/claude/docs/security)

## 📚 Additional Resources

- [Anthropic API Documentation](https://docs.anthropic.com/)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

---

**Remember: Security is everyone's responsibility. When in doubt, ask!** 🔐
