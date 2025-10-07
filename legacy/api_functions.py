"""
Legacy API Functions

This module provides the original SendToLLM.py API functions
for backward compatibility, now implemented using the modular components.
"""

import json
from typing import Optional, Dict, Any, List
from .abacus_client import get_client
from .file_operations import FileProcessor


def send_json_to_gpt5(json_file_path: str, 
                     prompt: str, 
                     deployment_token: Optional[str] = None, 
                     deployment_id: Optional[str] = None, 
                     api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Send a JSON file along with a prompt to a deployed LLM using Abacus.AI API
    
    Args:
        json_file_path: Path to the JSON file
        prompt: The prompt to send along with the JSON
        deployment_token: Abacus.AI deployment token for authentication
        deployment_id: The unique identifier of the deployment
        api_key: Abacus.AI API key (alternative to deployment_token)
        
    Returns:
        Response from the API
    """
    # Read the JSON file
    json_data = FileProcessor.read_json_file(json_file_path)
    
    # Prepare the message
    message_text = f"{prompt}\n\nJSON Data:\n{json.dumps(json_data, indent=2)}"
    messages = [{
        "is_user": True,
        "text": message_text
    }]
    
    # Send to API
    client = get_client()
    return client.send_chat_request(
        messages=messages,
        deployment_token=deployment_token,
        deployment_id=deployment_id,
        api_key=api_key,
        temperature=0.1,
        max_tokens=8000
    )


def send_json_content_to_gpt5(json_content: Dict[str, Any], 
                             prompt: str, 
                             deployment_token: Optional[str] = None, 
                             deployment_id: Optional[str] = None, 
                             api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Send JSON content (as dict/object) along with a prompt to a deployed LLM using Abacus.AI API
    
    Args:
        json_content: JSON content as Python dict
        prompt: The prompt to send along with the JSON
        deployment_token: Abacus.AI deployment token for authentication
        deployment_id: The unique identifier of the deployment
        api_key: Abacus.AI API key (alternative to deployment_token)
        
    Returns:
        Response from the API
    """
    # Prepare the message
    message_text = f"{prompt}\n\nJSON Data:\n{json.dumps(json_content, indent=2)}"
    messages = [{
        "is_user": True,
        "text": message_text
    }]
    
    # Send to API
    client = get_client()
    return client.send_chat_request(
        messages=messages,
        deployment_token=deployment_token,
        deployment_id=deployment_id,
        api_key=api_key,
        temperature=0.7,
        max_tokens=4000
    )


def send_json_to_llm_completion(json_file_path: str, 
                               prompt: str, 
                               deployment_token: Optional[str] = None, 
                               deployment_id: Optional[str] = None, 
                               api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Send a JSON file along with a prompt to a fine-tuned LLM using Abacus.AI getCompletion API
    
    Args:
        json_file_path: Path to the JSON file
        prompt: The prompt to send along with the JSON
        deployment_token: Abacus.AI deployment token for authentication
        deployment_id: The unique identifier of the deployment
        api_key: Abacus.AI API key (alternative to deployment_token)
        
    Returns:
        Response from the API
    """
    # Read the JSON file
    json_data = FileProcessor.read_json_file(json_file_path)
    
    # Prepare the prompt
    full_prompt = f"{prompt}\n\nJSON Data:\n{json.dumps(json_data, indent=2)}"
    
    # Send to completion API
    client = get_client()
    return client.send_completion_request(
        prompt=full_prompt,
        deployment_token=deployment_token,
        deployment_id=deployment_id,
        api_key=api_key
    )


def upload_file_to_abacus(file_path: str, 
                         deployment_id: Optional[str] = None, 
                         api_key: Optional[str] = None, 
                         deployment_token: Optional[str] = None) -> str:
    """
    Upload a file to Abacus.AI for use in chat
    
    Args:
        file_path: Path to the file to upload
        deployment_id: The unique identifier of the deployment
        api_key: Abacus.AI API key
        deployment_token: Abacus.AI deployment token
        
    Returns:
        File ID for use in chat messages
    """
    client = get_client()
    return client.upload_file(
        file_path=file_path,
        deployment_token=deployment_token,
        deployment_id=deployment_id,
        api_key=api_key
    )


def send_chat_with_attachments(prompt: str, 
                              file_ids: Optional[List[str]] = None, 
                              deployment_token: Optional[str] = None, 
                              deployment_id: Optional[str] = None, 
                              api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Send a chat message with file attachments to Abacus.AI
    
    Args:
        prompt: The prompt/message to send
        file_ids: List of file IDs from uploaded files
        deployment_token: Abacus.AI deployment token
        deployment_id: The unique identifier of the deployment
        api_key: Abacus.AI API key
        
    Returns:
        Response from the API
    """
    # Prepare message with attachments
    message = {
        "is_user": True,
        "text": prompt
    }
    
    # Add file attachments if provided
    if file_ids:
        message["attachments"] = [{"fileId": file_id} for file_id in file_ids]
    
    messages = [message]
    
    # Send to API
    client = get_client()
    return client.send_chat_request(
        messages=messages,
        deployment_token=deployment_token,
        deployment_id=deployment_id,
        api_key=api_key,
        temperature=0.7,
        max_tokens=4000
    )


# Import medical workflow functions for backward compatibility
from .medical_workflow import MedicalWorkflow
from .file_operations import MedicalFileValidator

# Create global workflow instance
_workflow = None

def get_workflow() -> MedicalWorkflow:
    """Get the global medical workflow instance"""
    global _workflow
    if _workflow is None:
        _workflow = MedicalWorkflow()
    return _workflow


def send_medical_correlation_data_with_attachments(attachments_dir: str = "./data/to_llm/attachments",
                                                  prompt_file: str = "./data/to_llm/prompt/prompt_v8.txt",
                                                  deployment_token: Optional[str] = None,
                                                  deployment_id: Optional[str] = None,
                                                  api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Send medical correlation data with file contents embedded in the chat message
    (Updated approach - embeds file contents instead of uploading as attachments)
    """
    workflow = get_workflow()
    return workflow.send_medical_correlation_data_with_attachments(
        attachments_dir=attachments_dir,
        prompt_file=prompt_file,
        deployment_token=deployment_token,
        deployment_id=deployment_id,
        api_key=api_key
    )


def send_medical_correlation_data_to_llm(attachments_dir: str = "./data/to_llm/attachments",
                                        prompt_file: str = "./data/to_llm/prompt/prompt_v8.txt",
                                        deployment_token: Optional[str] = None,
                                        deployment_id: Optional[str] = None,
                                        api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Send medical correlation data (keyword search, vector search, and correlation report) to LLM
    (Legacy function - embeds data in message text)
    """
    workflow = get_workflow()
    return workflow.send_medical_correlation_data_to_llm(
        attachments_dir=attachments_dir,
        prompt_file=prompt_file,
        deployment_token=deployment_token,
        deployment_id=deployment_id,
        api_key=api_key
    )


def validate_attachments_directory(attachments_dir: str) -> Dict[str, Dict[str, Any]]:
    """
    Validate that the attachments directory exists and contains expected files
    """
    return MedicalFileValidator.validate_attachments_directory(attachments_dir)
