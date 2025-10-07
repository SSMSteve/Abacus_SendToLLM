# LLM Chat System Operations Manual

## Table of Contents
1. [Installation and Setup](#installation-and-setup)
2. [Configuration](#configuration)
3. [Deployment](#deployment)
4. [Monitoring and Logging](#monitoring-and-logging)
5. [Troubleshooting](#troubleshooting)
6. [Maintenance](#maintenance)
7. [Security](#security)

## Installation and Setup

### Prerequisites
- Python 3.12 or higher
- pip or uv package manager
- Access to at least one LLM provider (Abacus.AI, OpenAI, or Anthropic)

### Installation Steps

#### 1. Clone Repository
```bash
git clone <repository-url>
cd py_abacus_sendToLLM
```

#### 2. Install Dependencies
```bash
# Using pip
pip install -r requirements.txt

# Using uv (recommended)
uv sync
```

#### 3. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit configuration
nano .env
```

#### 4. Verify Installation
```bash
# Run system tests
python tests/test_chat_system.py

# Run with API test (optional)
python tests/test_chat_system.py --include-api
```

## Configuration

### Environment Variables

#### Required for Abacus.AI
```bash
ABACUS_DEPLOYMENT_ID=your_deployment_id_here
# Either API key OR deployment token (not both)
ABACUS_API_KEY=your_api_key_here
# OR
ABACUS_DEPLOYMENT_TOKEN=your_deployment_token_here
```

#### Optional Configuration
```bash
# Default model selection
DEFAULT_MODEL=abacus-gpt5

# Model parameters
ABACUS_TEMPERATURE=0.7
ABACUS_MAX_TOKENS=4000

# OpenAI (if using)
OPENAI_API_KEY=your_openai_key_here

# Anthropic (if using)
ANTHROPIC_API_KEY=your_anthropic_key_here
```

### Model Configuration

#### Adding Custom Models
```python
from llm_chat import get_config, ModelConfig

config = get_config()
custom_model = ModelConfig(
    provider='abacus',
    model_name='custom-gpt5',
    deployment_id='custom-deployment-id',
    api_key='your-api-key',
    temperature=0.1,
    max_tokens=8000
)
config.add_custom_model('my-custom-model', custom_model)
```

#### Switching Default Model
```python
from llm_chat import get_config

config = get_config()
config.set_default_model('abacus-gpt5')
```

## Deployment

### Development Environment
```bash
# Install in development mode
pip install -e .

# Run examples
python examples/example_chat.py

# Run tests
python -m pytest tests/
```

### Production Environment

#### Docker Deployment (Recommended)
```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

# Set environment variables
ENV PYTHONPATH=/app/src

CMD ["python", "your_application.py"]
```

#### Direct Deployment
```bash
# Install package
pip install .

# Set Python path
export PYTHONPATH=/path/to/installation/src

# Run application
python your_application.py
```

### Environment-Specific Configuration

#### Development
```bash
DEFAULT_MODEL=abacus-gpt5
ABACUS_TEMPERATURE=0.7
LOG_LEVEL=DEBUG
```

#### Staging
```bash
DEFAULT_MODEL=abacus-gpt5
ABACUS_TEMPERATURE=0.5
LOG_LEVEL=INFO
```

#### Production
```bash
DEFAULT_MODEL=abacus-gpt5
ABACUS_TEMPERATURE=0.3
LOG_LEVEL=WARNING
```

## Monitoring and Logging

### Built-in Logging
The system provides console output for key operations:
- Configuration loading status
- API request/response summaries
- File processing results
- Error conditions

### Custom Logging Setup
```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('llm_chat.log'),
        logging.StreamHandler()
    ]
)
```

### Metrics to Monitor
- **API Response Times**: Track latency for each provider
- **Error Rates**: Monitor failed requests by provider
- **Token Usage**: Track consumption for cost management
- **File Processing**: Monitor attachment processing times

### Health Checks
```python
from llm_chat import create_chat_client

def health_check():
    try:
        chat = create_chat_client()
        response = chat.send_message("Health check", include_history=False)
        return response.content is not None
    except Exception as e:
        print(f"Health check failed: {e}")
        return False
```

## Troubleshooting

### Common Issues

#### 1. Import Errors
**Problem**: `ModuleNotFoundError: No module named 'llm_chat'`

**Solution**:
```bash
# Ensure Python path is set
export PYTHONPATH=/path/to/project/src

# Or install package
pip install -e .
```

#### 2. Authentication Errors
**Problem**: `ValueError: Either deployment_token or api_key must be provided`

**Solution**:
```bash
# Check environment variables
echo $ABACUS_API_KEY
echo $ABACUS_DEPLOYMENT_TOKEN

# Set missing variables
export ABACUS_API_KEY=your_key_here
```

#### 3. API Connection Errors
**Problem**: `requests.exceptions.ConnectionError`

**Solutions**:
- Check internet connectivity
- Verify API endpoints are accessible
- Check firewall/proxy settings
- Validate credentials

#### 4. File Not Found Errors
**Problem**: `FileNotFoundError: Attachment file not found`

**Solutions**:
- Verify file paths are correct
- Check file permissions
- Ensure files exist before processing

### Debugging Steps

#### 1. Enable Verbose Logging
```python
import logging
logging.getLogger().setLevel(logging.DEBUG)
```

#### 2. Test Configuration
```bash
python tests/test_chat_system.py
```

#### 3. Test API Connectivity
```bash
python tests/test_chat_system.py --include-api
```

#### 4. Validate Environment
```python
import os
from llm_chat import get_config

# Check environment
config = get_config()
print(config.list_available_models())

# Check credentials
print("API Key:", "Set" if os.getenv('ABACUS_API_KEY') else "Not set")
print("Deployment ID:", "Set" if os.getenv('ABACUS_DEPLOYMENT_ID') else "Not set")
```

## Maintenance

### Regular Tasks

#### 1. Update Dependencies
```bash
# Check for updates
pip list --outdated

# Update packages
pip install --upgrade requests python-dotenv

# Or with uv
uv sync --upgrade
```

#### 2. Clean Up Outputs
```bash
# Remove old output files
rm -rf output/*

# Clean Python cache
find . -type d -name "__pycache__" -exec rm -rf {} +
```

#### 3. Backup Configuration
```bash
# Backup environment file (without secrets)
cp .env .env.backup.$(date +%Y%m%d)
```

### Version Updates

#### 1. Check Current Version
```python
from llm_chat import __version__
print(__version__)
```

#### 2. Update Process
1. Review changelog
2. Test in development environment
3. Update dependencies
4. Run full test suite
5. Deploy to staging
6. Deploy to production

### Performance Optimization

#### 1. Monitor Response Times
```python
import time
from llm_chat import create_chat_client

start_time = time.time()
chat = create_chat_client()
response = chat.send_message("Test message")
end_time = time.time()

print(f"Response time: {end_time - start_time:.2f} seconds")
```

#### 2. Optimize File Processing
- Use streaming for large files
- Implement file size limits
- Cache frequently used files

## Security

### Best Practices

#### 1. Credential Management
- Never commit credentials to version control
- Use environment variables for all secrets
- Rotate API keys regularly
- Use deployment tokens when possible (limited scope)

#### 2. Input Validation
- Validate file paths to prevent directory traversal
- Limit file sizes to prevent memory exhaustion
- Sanitize user inputs

#### 3. Network Security
- Use HTTPS for all API communications
- Implement request timeouts
- Consider rate limiting for production use

### Security Checklist
- [ ] Credentials stored in environment variables
- [ ] No hardcoded secrets in code
- [ ] File path validation implemented
- [ ] Input size limits configured
- [ ] HTTPS used for all API calls
- [ ] Error messages don't expose sensitive data
- [ ] Logging doesn't include credentials

### Incident Response

#### 1. Credential Compromise
1. Immediately revoke compromised credentials
2. Generate new credentials
3. Update environment configuration
4. Review access logs
5. Notify relevant stakeholders

#### 2. Service Outage
1. Check provider status pages
2. Verify network connectivity
3. Review error logs
4. Implement fallback procedures
5. Communicate status to users
