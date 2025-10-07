"""
Configuration management for LLM interactions
Supports multiple providers: Abacus.AI, OpenAI, etc.
"""

import os
from dataclasses import dataclass
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class ModelConfig:
    """Configuration for a specific model"""
    provider: str  # 'abacus', 'openai', 'anthropic', etc.
    model_name: str  # e.g., 'gpt-5', 'claude-3', 'custom-deployment'
    api_key: Optional[str] = None
    deployment_id: Optional[str] = None
    deployment_token: Optional[str] = None
    base_url: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 4000
    additional_params: Optional[Dict[str, Any]] = None

class LLMConfig:
    """Main configuration class for LLM interactions"""
    
    def __init__(self):
        self.models = self._load_model_configs()
        self.default_model = os.getenv('DEFAULT_MODEL', 'abacus-gpt5')
    
    def _load_model_configs(self) -> Dict[str, ModelConfig]:
        """Load model configurations from environment variables and defaults"""
        configs = {}
        
        # Abacus.AI GPT-5 configuration
        configs['abacus-gpt5'] = ModelConfig(
            provider='abacus',
            model_name='gpt-5',
            api_key=os.getenv('ABACUS_API_KEY'),
            deployment_id=os.getenv('ABACUS_DEPLOYMENT_ID'),
            deployment_token=os.getenv('ABACUS_DEPLOYMENT_TOKEN'),
            base_url='https://api.abacus.ai/api/v0',
            temperature=float(os.getenv('ABACUS_TEMPERATURE', '0.7')),
            max_tokens=int(os.getenv('ABACUS_MAX_TOKENS', '4000'))
        )
        
        # OpenAI GPT-4 configuration
        configs['openai-gpt4'] = ModelConfig(
            provider='openai',
            model_name='gpt-4',
            api_key=os.getenv('OPENAI_API_KEY'),
            base_url='https://api.openai.com/v1',
            temperature=float(os.getenv('OPENAI_TEMPERATURE', '0.7')),
            max_tokens=int(os.getenv('OPENAI_MAX_TOKENS', '4000'))
        )
        
        # OpenAI GPT-5 configuration (when available)
        configs['openai-gpt5'] = ModelConfig(
            provider='openai',
            model_name='gpt-5',
            api_key=os.getenv('OPENAI_API_KEY'),
            base_url='https://api.openai.com/v1',
            temperature=float(os.getenv('OPENAI_TEMPERATURE', '0.7')),
            max_tokens=int(os.getenv('OPENAI_MAX_TOKENS', '4000'))
        )
        
        # Anthropic Claude configuration
        configs['anthropic-claude'] = ModelConfig(
            provider='anthropic',
            model_name='claude-3-sonnet-20240229',
            api_key=os.getenv('ANTHROPIC_API_KEY'),
            base_url='https://api.anthropic.com/v1',
            temperature=float(os.getenv('ANTHROPIC_TEMPERATURE', '0.7')),
            max_tokens=int(os.getenv('ANTHROPIC_MAX_TOKENS', '4000'))
        )
        
        return configs
    
    def get_model_config(self, model_name: Optional[str] = None) -> ModelConfig:
        """Get configuration for a specific model"""
        if model_name is None:
            model_name = self.default_model
        
        if model_name not in self.models:
            raise ValueError(f"Model '{model_name}' not found in configuration. Available models: {list(self.models.keys())}")
        
        return self.models[model_name]
    
    def list_available_models(self) -> Dict[str, str]:
        """List all available models with their providers"""
        return {name: config.provider for name, config in self.models.items()}
    
    def add_custom_model(self, name: str, config: ModelConfig):
        """Add a custom model configuration"""
        self.models[name] = config
    
    def set_default_model(self, model_name: str):
        """Set the default model to use"""
        if model_name not in self.models:
            raise ValueError(f"Model '{model_name}' not found in configuration")
        self.default_model = model_name

# Global configuration instance
llm_config = LLMConfig()

def get_config() -> LLMConfig:
    """Get the global LLM configuration instance"""
    return llm_config
