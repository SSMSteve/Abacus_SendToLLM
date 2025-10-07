"""
Core Abacus.AI API Client

This module provides the core API client functionality for interacting
with Abacus.AI's LLM services, including chat and completion endpoints.
"""

import json
import requests
from typing import Optional, Dict, Any, List
from .auth_config import get_auth_config


class AbacusAPIClient:
    """Core client for Abacus.AI API interactions"""
    
    BASE_URL = "https://api.abacus.ai/api/v0"
    
    def __init__(self):
        self.auth_config = get_auth_config()
    
    def send_chat_request(self,
                         messages: List[Dict[str, Any]],
                         deployment_token: Optional[str] = None,
                         deployment_id: Optional[str] = None,
                         api_key: Optional[str] = None,
                         temperature: float = 0.7,
                         max_tokens: int = 4000) -> Dict[str, Any]:
        """
        Send a chat request to Abacus.AI getChatResponse endpoint
        
        Args:
            messages: List of message dictionaries
            deployment_token: Optional deployment token override
            deployment_id: Optional deployment ID override
            api_key: Optional API key override
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            API response as dictionary
            
        Raises:
            Exception: If API request fails
        """
        # Get credentials
        token, dep_id, key = self.auth_config.get_credentials(
            deployment_token, deployment_id, api_key
        )
        
        # Prepare request
        url = f"{self.BASE_URL}/getChatResponse"
        headers = self.auth_config.get_headers(key)
        
        payload = {
            "deploymentId": dep_id,
            "messages": messages,
            "temperature": temperature,
            "numCompletionTokens": max_tokens
        }
        
        if token:
            payload["deploymentToken"] = token
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {e}")
    
    def send_completion_request(self,
                               prompt: str,
                               deployment_token: Optional[str] = None,
                               deployment_id: Optional[str] = None,
                               api_key: Optional[str] = None) -> Dict[str, Any]:
        """
        Send a completion request to Abacus.AI getCompletion endpoint
        
        Args:
            prompt: The prompt text
            deployment_token: Optional deployment token override
            deployment_id: Optional deployment ID override
            api_key: Optional API key override
            
        Returns:
            API response as dictionary
            
        Raises:
            Exception: If API request fails
        """
        # Get credentials
        token, dep_id, key = self.auth_config.get_credentials(
            deployment_token, deployment_id, api_key
        )
        
        # Prepare request
        url = f"{self.BASE_URL}/getCompletion"
        headers = self.auth_config.get_headers(key)
        
        payload = {
            "deploymentId": dep_id,
            "prompt": prompt
        }
        
        if token:
            payload["deploymentToken"] = token
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {e}")
    
    def upload_file(self,
                   file_path: str,
                   deployment_token: Optional[str] = None,
                   deployment_id: Optional[str] = None,
                   api_key: Optional[str] = None) -> str:
        """
        Upload a file to Abacus.AI
        
        Args:
            file_path: Path to the file to upload
            deployment_token: Optional deployment token override
            deployment_id: Optional deployment ID override
            api_key: Optional API key override
            
        Returns:
            File ID for use in chat messages
            
        Raises:
            FileNotFoundError: If file doesn't exist
            Exception: If upload fails
        """
        import os
        
        # Get credentials
        token, dep_id, key = self.auth_config.get_credentials(
            deployment_token, deployment_id, api_key
        )
        
        # Prepare request
        url = f"{self.BASE_URL}/uploadFile"
        headers = {}
        if key:
            headers["apiKey"] = key
        
        try:
            with open(file_path, 'rb') as file:
                files = {
                    'file': (os.path.basename(file_path), file, 'application/octet-stream')
                }
                
                data = {'deploymentId': dep_id}
                if token:
                    data['deploymentToken'] = token
                
                response = requests.post(url, headers=headers, files=files, data=data)
                response.raise_for_status()
                
                result = response.json()
                if 'result' in result and 'fileId' in result['result']:
                    return result['result']['fileId']
                else:
                    raise Exception(f"Unexpected upload response format: {result}")
                    
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"File upload failed: {e}")


# Global client instance
_client = None


def get_client() -> AbacusAPIClient:
    """Get the global API client instance"""
    global _client
    if _client is None:
        _client = AbacusAPIClient()
    return _client
