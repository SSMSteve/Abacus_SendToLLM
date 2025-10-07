# LLM Chat System Architecture

## Overview

The LLM Chat System is a configurable Python framework for interacting with multiple Large Language Model (LLM) providers. It provides a unified interface for chat conversations, file attachments, and model switching across different providers including Abacus.AI, OpenAI, and Anthropic.

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Client Applications                       │
├─────────────────────────────────────────────────────────────┤
│                  LLM Chat System API                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Config    │  │ Chat Client │  │   Legacy SendToLLM  │  │
│  │  Management │  │   (New)     │  │    (Backward Compat)│  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│                Provider Abstraction Layer                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  Abacus.AI  │  │   OpenAI    │  │     Anthropic       │  │
│  │   Adapter   │  │   Adapter   │  │      Adapter        │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│                    External APIs                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ Abacus.AI   │  │ OpenAI API  │  │   Anthropic API     │  │
│  │     API     │  │             │  │                     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Core Components

#### 1. Configuration System (`src/llm_chat/config.py`)

**Purpose**: Centralized configuration management for multiple LLM providers and models.

**Key Classes**:
- `ModelConfig`: Dataclass containing provider-specific configuration
- `LLMConfig`: Main configuration manager with model registry
- `get_config()`: Global configuration instance accessor

**Responsibilities**:
- Load environment variables for credentials
- Manage model configurations for different providers
- Provide default model selection
- Support custom model registration

#### 2. Chat Client (`src/llm_chat/chat_llm.py`)

**Purpose**: Universal chat interface with provider abstraction.

**Key Classes**:
- `ChatMessage`: Message representation with role, content, and attachments
- `ChatResponse`: Standardized response format across providers
- `LLMChatClient`: Main chat client with conversation management

**Responsibilities**:
- Maintain conversation history
- Process file attachments
- Route requests to appropriate provider adapters
- Standardize response formats

#### 3. Legacy Support (`SendToLLM.py`)

**Purpose**: Backward compatibility with existing code.

**Key Functions**:
- `send_json_to_gpt5()`: Direct JSON file processing
- `send_json_content_to_gpt5()`: Direct JSON content processing
- `send_medical_correlation_data_with_attachments()`: Specialized medical workflow

### Data Flow

#### 1. Configuration Loading
```
Environment Variables → ModelConfig → LLMConfig → Global Registry
```

#### 2. Chat Message Flow
```
User Input → ChatMessage → Provider Adapter → External API → ChatResponse
     ↓
Conversation History ← Response Processing ← API Response
```

#### 3. File Attachment Processing
```
File Paths → File Reading → Content Processing → Message Embedding
```

## Provider Adapters

### Abacus.AI Adapter

**Endpoint**: `https://api.abacus.ai/api/v0/getChatResponse`

**Authentication**: 
- API Key (header: `apiKey`)
- Deployment Token (payload: `deploymentToken`)

**Message Format**:
```json
{
  "deploymentId": "string",
  "messages": [
    {
      "is_user": true,
      "text": "message content with attachments"
    }
  ],
  "temperature": 0.7,
  "numCompletionTokens": 4000
}
```

### OpenAI Adapter (Planned)

**Endpoint**: `https://api.openai.com/v1/chat/completions`

**Authentication**: Bearer token

**Message Format**:
```json
{
  "model": "gpt-4",
  "messages": [
    {
      "role": "user",
      "content": "message content"
    }
  ],
  "temperature": 0.7,
  "max_tokens": 4000
}
```

### Anthropic Adapter (Planned)

**Endpoint**: `https://api.anthropic.com/v1/messages`

**Authentication**: `x-api-key` header

## File Attachment System

### Supported File Types
- **JSON**: Parsed and embedded as structured data
- **Text/Markdown**: Embedded as plain text with formatting preservation
- **Binary**: Base64 encoded (future enhancement)

### Processing Pipeline
1. **File Detection**: Check file existence and type
2. **Content Reading**: Read file content with appropriate encoding
3. **Format Processing**: Parse JSON or preserve text formatting
4. **Message Embedding**: Integrate content into chat message

## Configuration Management

### Environment Variables

| Variable | Purpose | Required | Default |
|----------|---------|----------|---------|
| `DEFAULT_MODEL` | Default model selection | No | `abacus-gpt5` |
| `ABACUS_API_KEY` | Abacus.AI authentication | Yes* | None |
| `ABACUS_DEPLOYMENT_TOKEN` | Abacus.AI deployment token | Yes* | None |
| `ABACUS_DEPLOYMENT_ID` | Abacus.AI deployment ID | Yes | None |
| `OPENAI_API_KEY` | OpenAI authentication | No | None |
| `ANTHROPIC_API_KEY` | Anthropic authentication | No | None |

*Either API key or deployment token required

### Model Registry

Models are registered in the configuration system with the following structure:

```python
ModelConfig(
    provider='abacus',
    model_name='gpt-5',
    api_key=os.getenv('ABACUS_API_KEY'),
    deployment_id=os.getenv('ABACUS_DEPLOYMENT_ID'),
    deployment_token=os.getenv('ABACUS_DEPLOYMENT_TOKEN'),
    base_url='https://api.abacus.ai/api/v0',
    temperature=0.7,
    max_tokens=4000
)
```

## Error Handling

### Error Categories
1. **Configuration Errors**: Missing credentials, invalid model names
2. **Network Errors**: API connectivity issues, timeouts
3. **Authentication Errors**: Invalid credentials, expired tokens
4. **Validation Errors**: Invalid input formats, file not found
5. **Provider Errors**: API-specific error responses

### Error Propagation
- Configuration errors raise `ValueError` with descriptive messages
- Network errors raise `requests.RequestException` with context
- File errors raise `FileNotFoundError` or `IOError`
- All errors include sufficient context for debugging

## Security Considerations

### Credential Management
- Environment variables for sensitive data
- No hardcoded credentials in source code
- Support for both API keys and deployment tokens

### Data Privacy
- No logging of sensitive message content
- Secure transmission via HTTPS
- Provider-specific data handling policies apply

### Input Validation
- File path validation to prevent directory traversal
- Content size limits to prevent memory exhaustion
- JSON validation for structured data

## Performance Characteristics

### Scalability
- Stateless design for horizontal scaling
- Connection pooling via requests library
- Configurable timeout and retry policies

### Memory Usage
- Conversation history stored in memory (configurable retention)
- File content loaded on-demand
- Streaming support for large responses (future enhancement)

### Latency
- Direct API calls without unnecessary middleware
- Efficient file processing with minimal copying
- Async support planned for concurrent requests
