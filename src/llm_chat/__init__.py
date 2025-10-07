"""
LLM Chat System - Configurable multi-provider LLM client

This package provides a unified interface for interacting with multiple LLM providers
including Abacus.AI, OpenAI, and Anthropic. It supports conversation history,
file attachments, and easy model switching.

Main Components:
- config: Model configuration and credential management
- chat_llm: Universal chat client with provider abstraction
- SendToLLM: Legacy functions for backward compatibility

Example Usage:
    from llm_chat import create_chat_client
    
    chat = create_chat_client('abacus-gpt5')
    response = chat.send_message("Hello!", attachments=["data.json"])
    print(response.content)
"""

from .config import get_config, ModelConfig, LLMConfig
from .chat_llm import create_chat_client, LLMChatClient, ChatMessage, ChatResponse

__version__ = "0.2.0"
__author__ = "LLM Chat System"
__email__ = "support@example.com"

__all__ = [
    # Configuration
    'get_config',
    'ModelConfig', 
    'LLMConfig',
    
    # Chat Client
    'create_chat_client',
    'LLMChatClient',
    'ChatMessage',
    'ChatResponse',
]

# Package metadata
SUPPORTED_PROVIDERS = ['abacus', 'openai', 'anthropic']
DEFAULT_MODEL = 'abacus-gpt5'
