# Abacus.AI LLM Integration

This project provides Python functions to send JSON data to Large Language Models (LLMs) deployed on Abacus.AI platform.

## Issue Fixed

The original code was using an invalid API endpoint: `https://api.abacus.ai/api/v0/chatCompletion`

This endpoint does not exist in Abacus.AI's API. The corrected code now uses the proper Abacus.AI endpoints:

- `getChatResponse` - for chat-based interactions with deployed models
- `getCompletion` - for completion-based interactions with fine-tuned LLMs

## Setup

### Environment Variables

Set the following environment variables:

```bash
export ABACUS_DEPLOYMENT_TOKEN="your-deployment-token"
export ABACUS_DEPLOYMENT_ID="your-deployment-id"
# OR alternatively
export ABACUS_API_KEY="your-api-key"
```

### Required Parameters

To use Abacus.AI's API, you need:

1. **Deployment ID**: The unique identifier of your deployed model
2. **Authentication**: Either a deployment token OR an API key
   - **Deployment Token**: Safer for embedding in applications (limited to specific deployment)
   - **API Key**: Full access to your Abacus.AI account

## Usage

### Method 1: Chat Response (Recommended)

```python
from SendToLLM import send_json_to_gpt5

# Send JSON file
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

## Getting Your Deployment Details

1. Log into your Abacus.AI account
2. Navigate to your deployed model
3. Find the Deployment ID in the deployment details
4. Generate a deployment token or use your API key

## Error Handling

The functions will raise exceptions for:
- Missing credentials
- Invalid JSON files
- Network/API errors
- Invalid deployment IDs

Always wrap calls in try-catch blocks:

```python
try:
    response = send_json_to_gpt5(...)
    # Process response
except Exception as e:
    print(f"Error: {e}")
```