"""
Authentication and Configuration Management for Abacus.AI API

This module handles environment variable loading, credential validation,
and configuration management for the legacy SendToLLM system.
"""

import os
from dotenv import load_dotenv
from typing import Optional, Tuple

# Load environment variables from .env file
load_dotenv()


class AbacusAuthConfig:
    """Manages authentication and configuration for Abacus.AI API"""
    
    def __init__(self):
        self.deployment_token = os.getenv('ABACUS_DEPLOYMENT_TOKEN')
        self.deployment_id = os.getenv('ABACUS_DEPLOYMENT_ID')
        self.api_key = os.getenv('ABACUS_API_KEY')
    
    def get_credentials(self, 
                       deployment_token: Optional[str] = None,
                       deployment_id: Optional[str] = None,
                       api_key: Optional[str] = None) -> Tuple[str, str, str]:
        """
        Get credentials with fallback to environment variables
        
        Args:
            deployment_token: Optional deployment token override
            deployment_id: Optional deployment ID override
            api_key: Optional API key override
            
        Returns:
            Tuple of (deployment_token, deployment_id, api_key)
            
        Raises:
            ValueError: If required credentials are missing
        """
        # Use provided values or fall back to environment
        final_token = deployment_token or self.deployment_token
        final_id = deployment_id or self.deployment_id
        final_key = api_key or self.api_key
        
        # Validate required credentials
        if not final_token and not final_key:
            raise ValueError(
                "Either deployment_token or api_key must be provided. "
                "Set ABACUS_DEPLOYMENT_TOKEN or ABACUS_API_KEY environment variable"
            )
        
        if not final_id:
            raise ValueError(
                "deployment_id is required. "
                "Set ABACUS_DEPLOYMENT_ID environment variable or pass deployment_id parameter"
            )
        
        return final_token, final_id, final_key
    
    def validate_credentials(self) -> bool:
        """
        Validate that minimum required credentials are available
        
        Returns:
            True if credentials are valid, False otherwise
        """
        try:
            self.get_credentials()
            return True
        except ValueError:
            return False
    
    def get_headers(self, api_key: Optional[str] = None) -> dict:
        """
        Get HTTP headers for API requests
        
        Args:
            api_key: Optional API key override
            
        Returns:
            Dictionary of HTTP headers
        """
        headers = {"Content-Type": "application/json"}
        
        final_key = api_key or self.api_key
        if final_key:
            headers["apiKey"] = final_key
            
        return headers


# Global configuration instance
auth_config = AbacusAuthConfig()


def get_auth_config() -> AbacusAuthConfig:
    """Get the global authentication configuration instance"""
    return auth_config


def validate_environment() -> dict:
    """
    Validate environment setup and return status
    
    Returns:
        Dictionary with validation results
    """
    config = get_auth_config()
    
    status = {
        'deployment_token': bool(config.deployment_token),
        'deployment_id': bool(config.deployment_id),
        'api_key': bool(config.api_key),
        'valid': config.validate_credentials()
    }
    
    return status
