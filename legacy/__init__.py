"""
Legacy SendToLLM System

This package contains the refactored components of the original SendToLLM.py file,
organized into logical modules for better maintainability and reusability.

The package maintains backward compatibility with the original API while providing
a cleaner, more modular architecture.
"""

# Import main API functions for backward compatibility
from .api_functions import (
    send_json_to_gpt5,
    send_json_content_to_gpt5,
    send_json_to_llm_completion,
    upload_file_to_abacus,
    send_chat_with_attachments,
    send_medical_correlation_data_with_attachments,
    send_medical_correlation_data_to_llm,
    validate_attachments_directory
)

# Import core components for advanced usage
from .auth_config import AbacusAuthConfig, get_auth_config, validate_environment
from .abacus_client import AbacusAPIClient, get_client
from .file_operations import FileProcessor, MedicalFileValidator, OutputManager
from .response_processor import ResponseProcessor
from .medical_workflow import MedicalWorkflow, MedicalMessageBuilder

# Import main execution function
from .main import main

__version__ = "1.0.0"
__author__ = "Legacy SendToLLM System"

# Backward compatibility exports
__all__ = [
    # Main API functions (backward compatibility)
    'send_json_to_gpt5',
    'send_json_content_to_gpt5', 
    'send_json_to_llm_completion',
    'upload_file_to_abacus',
    'send_chat_with_attachments',
    'send_medical_correlation_data_with_attachments',
    'send_medical_correlation_data_to_llm',
    'validate_attachments_directory',
    
    # Core components (advanced usage)
    'AbacusAuthConfig',
    'get_auth_config',
    'validate_environment',
    'AbacusAPIClient',
    'get_client',
    'FileProcessor',
    'MedicalFileValidator',
    'OutputManager',
    'ResponseProcessor',
    'MedicalWorkflow',
    'MedicalMessageBuilder',
    
    # Main execution
    'main'
]

# Package metadata
SUPPORTED_APIS = ['getChatResponse', 'getCompletion', 'uploadFile']
DEFAULT_ATTACHMENTS_DIR = "./data/to_llm/attachments"
DEFAULT_PROMPT_FILE = "./data/to_llm/prompt/prompt_v8.txt"
DEFAULT_OUTPUT_DIR = "./output"
