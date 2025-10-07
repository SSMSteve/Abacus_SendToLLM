# LLM Chat System

A professional, configurable Python framework for interacting with Large Language Models (LLMs) from multiple providers. Features unified chat interface, conversation history, file attachments, and seamless model switching.

## 🚀 Quick Start

```python
from llm_chat import create_chat_client

# Create chat client
chat = create_chat_client('abacus-gpt5')

# Send message with attachments
response = chat.send_message(
    message="Analyze this data",
    attachments=["data.json", "report.md"]
)
print(response.content)
```

## Issue Fixed

The original code was using an invalid API endpoint: `https://api.abacus.ai/api/v0/chatCompletion`

This endpoint does not exist in Abacus.AI's API. The corrected code now uses the proper Abacus.AI endpoints:

- `getChatResponse` - for chat-based interactions with deployed models
- `getCompletion` - for completion-based interactions with fine-tuned LLMs

## ✨ Features

- 🔄 **Multi-Provider Support**: Abacus.AI, OpenAI, Anthropic with unified interface
- 🎯 **Model Flexibility**: Easy switching between GPT-4, GPT-5, Claude, and custom models
- 📎 **File Attachments**: JSON, text, and markdown file support
- 💬 **Conversation History**: Automatic multi-turn conversation management
- ⚙️ **Smart Configuration**: Environment-based setup with intelligent defaults
- 🔒 **Production Ready**: Comprehensive error handling, security, and monitoring
- 📚 **Well Documented**: Complete API reference and operations guides
- 🔄 **Backward Compatible**: Legacy API preserved for existing code

## 📁 Project Structure

```
├── src/llm_chat/              # Core package
├── tests/                     # Test suite
├── examples/                  # Usage examples
├── scripts/                   # Utility scripts
├── docs/                      # Documentation
├── data/                      # Data files
└── output/                    # Generated outputs
```

## Setup

### Environment Variables

Copy `.env.example` to `.env` and configure your credentials:

```bash
# Copy the example file
cp .env.example .env

# Edit with your credentials
# For Abacus.AI (primary provider):
export ABACUS_DEPLOYMENT_TOKEN="your-deployment-token"
export ABACUS_DEPLOYMENT_ID="your-deployment-id"
# OR alternatively
export ABACUS_API_KEY="your-api-key"

# For OpenAI (optional):
export OPENAI_API_KEY="your-openai-api-key"

# Set default model
export DEFAULT_MODEL="abacus-gpt5"
```

### Required Parameters

To use Abacus.AI's API, you need:

1. **Deployment ID**: The unique identifier of your deployed model
2. **Authentication**: Either a deployment token OR an API key
   - **Deployment Token**: Safer for embedding in applications (limited to specific deployment)
   - **API Key**: Full access to your Abacus.AI account

## Usage

### Quick Start with New Chat System

```python
from chat_llm import create_chat_client

# Create a chat client (uses default model from config)
chat = create_chat_client()

# Send a simple message
response = chat.send_message("Hello! Can you help me analyze some data?")
print(f"Response: {response.content}")

# Send message with file attachments
response = chat.send_message(
    message="Please analyze these files",
    attachments=["data.json", "report.md"]
)
print(f"Analysis: {response.content}")
```

### Using Different Models

```python
from chat_llm import create_chat_client

# Use specific model
chat = create_chat_client('abacus-gpt5')  # or 'openai-gpt4', etc.

# Multi-turn conversation
chat.send_message("What is machine learning?")
response = chat.send_message("Can you give me an example?")  # Includes history
```

### Legacy Method: Direct API Calls

```python
from SendToLLM import send_json_to_gpt5

# Send JSON file (legacy method)
response = send_json_to_gpt5(
    json_file_path="data.json",
    prompt="Analyze this data",
    deployment_token="your-token",
    deployment_id="your-deployment-id"
)

# Extract response
if 'result' in response and 'messages' in response['result']:
    messages = response['result']['messages']
    if messages:
        ai_response = messages[-1].get('text', '')
        print(ai_response)
```

### Method 2: Completion (For Fine-tuned Models)

```python
from SendToLLM import send_json_to_llm_completion

response = send_json_to_llm_completion(
    json_file_path="data.json",
    prompt="Analyze this data",
    deployment_token="your-token",
    deployment_id="your-deployment-id"
)

# Extract completion
if 'result' in response:
    completion = response['result'].get('completion', '')
    print(completion)
```

### Method 3: Direct JSON Content

```python
from SendToLLM import send_json_content_to_gpt5

data = {"users": [{"name": "Alice", "age": 30}]}

response = send_json_content_to_gpt5(
    json_content=data,
    prompt="Summarize this user data"
)
```

## API Differences from OpenAI

| OpenAI | Abacus.AI |
|--------|-----------|
| `messages` with `role` and `content` | `messages` with `is_user` and `text` |
| `max_tokens` | `numCompletionTokens` |
| `model` parameter | Specified by `deploymentId` |
| Bearer token auth | `apiKey` header or `deploymentToken` in payload |

## Available Models

The system supports multiple LLM providers and models:

| Model Name | Provider | Description |
|------------|----------|-------------|
| `abacus-gpt5` | Abacus.AI | GPT-5 model deployed on Abacus.AI (default) |
| `openai-gpt4` | OpenAI | GPT-4 via OpenAI API |
| `openai-gpt5` | OpenAI | GPT-5 via OpenAI API (when available) |
| `anthropic-claude` | Anthropic | Claude 3 Sonnet |

### Model Configuration

You can configure models in several ways:

```python
from config import get_config

# Get current configuration
config = get_config()

# List available models
print(config.list_available_models())

# Set default model
config.set_default_model('abacus-gpt5')

# Add custom model
from config import ModelConfig
custom_model = ModelConfig(
    provider='abacus',
    model_name='custom-gpt5',
    deployment_id='your-custom-deployment-id',
    api_key='your-api-key'
)
config.add_custom_model('my-custom-model', custom_model)
```

## Getting Your Deployment Details

### For Abacus.AI:
1. Log into your Abacus.AI account
2. Navigate to your deployed model
3. Find the Deployment ID in the deployment details
4. Generate a deployment token or use your API key

### For OpenAI:
1. Get your API key from https://platform.openai.com/api-keys
2. Set `OPENAI_API_KEY` environment variable

## Error Handling

The functions will raise exceptions for:
- Missing credentials
- Invalid JSON files
- Network/API errors
- Invalid deployment IDs

## 📖 Documentation

- **[Architecture Guide](docs/ARCHITECTURE.md)**: System design and components
- **[Operations Manual](docs/OPERATIONS.md)**: Deployment and maintenance
- **[API Reference](docs/API_REFERENCE.md)**: Complete API documentation
- **[Project Summary](PROJECT_SUMMARY.md)**: Cleanup and reorganization report

## 🧪 Testing

```bash
# Run system tests
python tests/test_chat_system.py

# Run with API tests (uses credits)
python tests/test_chat_system.py --include-api

# Run comprehensive example
python examples/comprehensive_example.py
```

## 🔧 Error Handling

Always wrap calls in try-catch blocks:

```python
try:
    response = send_json_to_gpt5(...)
    # Process response
except Exception as e:
    print(f"Error: {e}")
```