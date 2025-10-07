# LLM Chat System API Reference

## Overview

This document provides comprehensive API reference for the LLM Chat System, including all classes, methods, and configuration options.

## Core Classes

### ModelConfig

Configuration dataclass for individual LLM models.

```python
@dataclass
class ModelConfig:
    provider: str                           # Provider name ('abacus', 'openai', 'anthropic')
    model_name: str                        # Model identifier
    api_key: Optional[str] = None          # API key for authentication
    deployment_id: Optional[str] = None    # Deployment ID (Abacus.AI)
    deployment_token: Optional[str] = None # Deployment token (Abacus.AI)
    base_url: Optional[str] = None         # API base URL
    temperature: float = 0.7               # Sampling temperature
    max_tokens: int = 4000                 # Maximum response tokens
    additional_params: Optional[Dict[str, Any]] = None  # Provider-specific params
```

**Example**:
```python
from llm_chat import ModelConfig

config = ModelConfig(
    provider='abacus',
    model_name='gpt-5',
    deployment_id='your-deployment-id',
    api_key='your-api-key',
    temperature=0.5,
    max_tokens=8000
)
```

### LLMConfig

Main configuration manager for the system.

#### Methods

##### `get_model_config(model_name: Optional[str] = None) -> ModelConfig`
Get configuration for a specific model.

**Parameters**:
- `model_name`: Model identifier. If None, returns default model.

**Returns**: ModelConfig instance

**Raises**: ValueError if model not found

**Example**:
```python
from llm_chat import get_config

config = get_config()
model_config = config.get_model_config('abacus-gpt5')
```

##### `list_available_models() -> Dict[str, str]`
List all available models with their providers.

**Returns**: Dictionary mapping model names to provider names

**Example**:
```python
models = config.list_available_models()
# {'abacus-gpt5': 'abacus', 'openai-gpt4': 'openai'}
```

##### `add_custom_model(name: str, config: ModelConfig)`
Add a custom model configuration.

**Parameters**:
- `name`: Unique model identifier
- `config`: ModelConfig instance

**Example**:
```python
custom_model = ModelConfig(provider='abacus', model_name='custom-gpt5')
config.add_custom_model('my-model', custom_model)
```

##### `set_default_model(model_name: str)`
Set the default model to use.

**Parameters**:
- `model_name`: Model identifier

**Raises**: ValueError if model not found

### ChatMessage

Represents a single message in a conversation.

```python
@dataclass
class ChatMessage:
    role: str                                    # 'user', 'assistant', 'system'
    content: str                                 # Message content
    attachments: Optional[List[Dict[str, Any]]] = None  # File attachments
```

### ChatResponse

Represents a response from an LLM.

```python
@dataclass
class ChatResponse:
    content: str                           # Response content
    model: str                            # Model that generated response
    provider: str                         # Provider name
    usage: Optional[Dict[str, Any]] = None # Token usage information
    raw_response: Optional[Dict[str, Any]] = None  # Raw API response
```

### LLMChatClient

Main chat client for interacting with LLMs.

#### Constructor

```python
def __init__(self, model_name: Optional[str] = None)
```

**Parameters**:
- `model_name`: Model to use. If None, uses default model.

#### Methods

##### `send_message(message: str, attachments: Optional[List[str]] = None, system_prompt: Optional[str] = None, include_history: bool = True) -> ChatResponse`

Send a message to the LLM.

**Parameters**:
- `message`: User message to send
- `attachments`: List of file paths to attach
- `system_prompt`: Optional system prompt
- `include_history`: Whether to include conversation history

**Returns**: ChatResponse object

**Example**:
```python
from llm_chat import create_chat_client

chat = create_chat_client('abacus-gpt5')
response = chat.send_message(
    message="Analyze this data",
    attachments=["data.json", "report.md"],
    system_prompt="You are a data analyst"
)
print(response.content)
```

##### `add_message(role: str, content: str, attachments: Optional[List[Dict[str, Any]]] = None)`

Add a message to conversation history.

**Parameters**:
- `role`: Message role ('user', 'assistant', 'system')
- `content`: Message content
- `attachments`: Processed attachments

##### `clear_history()`

Clear the conversation history.

**Example**:
```python
chat.clear_history()  # Start fresh conversation
```

## Factory Functions

### `create_chat_client(model_name: Optional[str] = None) -> LLMChatClient`

Create a new chat client instance.

**Parameters**:
- `model_name`: Model to use. If None, uses default model.

**Returns**: LLMChatClient instance

**Example**:
```python
from llm_chat import create_chat_client

# Use default model
chat = create_chat_client()

# Use specific model
chat = create_chat_client('abacus-gpt5')
```

### `get_config() -> LLMConfig`

Get the global configuration instance.

**Returns**: LLMConfig instance

## Legacy API (SendToLLM.py)

### `send_json_to_gpt5(json_file_path, prompt, deployment_token=None, deployment_id=None, api_key=None)`

Send JSON file to Abacus.AI using legacy interface.

**Parameters**:
- `json_file_path`: Path to JSON file
- `prompt`: Prompt text
- `deployment_token`: Abacus.AI deployment token
- `deployment_id`: Abacus.AI deployment ID
- `api_key`: Abacus.AI API key

**Returns**: Raw API response dictionary

### `send_json_content_to_gpt5(json_content, prompt, deployment_token=None, deployment_id=None, api_key=None)`

Send JSON content to Abacus.AI using legacy interface.

**Parameters**:
- `json_content`: JSON data as Python dict
- `prompt`: Prompt text
- `deployment_token`: Abacus.AI deployment token
- `deployment_id`: Abacus.AI deployment ID
- `api_key`: Abacus.AI API key

**Returns**: Raw API response dictionary

## Configuration Reference

### Environment Variables

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `DEFAULT_MODEL` | string | No | `abacus-gpt5` | Default model identifier |
| `ABACUS_API_KEY` | string | Yes* | None | Abacus.AI API key |
| `ABACUS_DEPLOYMENT_TOKEN` | string | Yes* | None | Abacus.AI deployment token |
| `ABACUS_DEPLOYMENT_ID` | string | Yes | None | Abacus.AI deployment ID |
| `ABACUS_TEMPERATURE` | float | No | 0.7 | Sampling temperature |
| `ABACUS_MAX_TOKENS` | integer | No | 4000 | Maximum response tokens |
| `OPENAI_API_KEY` | string | No | None | OpenAI API key |
| `OPENAI_TEMPERATURE` | float | No | 0.7 | OpenAI temperature |
| `OPENAI_MAX_TOKENS` | integer | No | 4000 | OpenAI max tokens |
| `ANTHROPIC_API_KEY` | string | No | None | Anthropic API key |
| `ANTHROPIC_TEMPERATURE` | float | No | 0.7 | Anthropic temperature |
| `ANTHROPIC_MAX_TOKENS` | integer | No | 4000 | Anthropic max tokens |

*Either `ABACUS_API_KEY` or `ABACUS_DEPLOYMENT_TOKEN` required for Abacus.AI

### Predefined Models

| Model ID | Provider | Description |
|----------|----------|-------------|
| `abacus-gpt5` | Abacus.AI | GPT-5 via Abacus.AI (default) |
| `openai-gpt4` | OpenAI | GPT-4 via OpenAI API |
| `openai-gpt5` | OpenAI | GPT-5 via OpenAI API |
| `anthropic-claude` | Anthropic | Claude 3 Sonnet |

## Error Handling

### Exception Types

#### `ValueError`
Raised for configuration errors, invalid model names, or missing credentials.

#### `FileNotFoundError`
Raised when attachment files cannot be found.

#### `requests.RequestException`
Raised for network-related errors during API calls.

### Error Examples

```python
from llm_chat import create_chat_client

try:
    chat = create_chat_client('invalid-model')
except ValueError as e:
    print(f"Configuration error: {e}")

try:
    response = chat.send_message("Hello", attachments=["nonexistent.json"])
except FileNotFoundError as e:
    print(f"File error: {e}")

try:
    response = chat.send_message("Hello")
except requests.RequestException as e:
    print(f"Network error: {e}")
```

## Usage Patterns

### Basic Chat
```python
from llm_chat import create_chat_client

chat = create_chat_client()
response = chat.send_message("Hello!")
print(response.content)
```

### Multi-turn Conversation
```python
chat = create_chat_client()
chat.send_message("What is machine learning?")
response = chat.send_message("Give me an example")  # Includes history
```

### File Attachments
```python
response = chat.send_message(
    "Analyze these files",
    attachments=["data.json", "report.md"]
)
```

### Custom Configuration
```python
from llm_chat import get_config, ModelConfig

config = get_config()
custom_model = ModelConfig(
    provider='abacus',
    model_name='specialized-model',
    deployment_id='custom-id',
    temperature=0.1
)
config.add_custom_model('my-model', custom_model)

chat = create_chat_client('my-model')
```
