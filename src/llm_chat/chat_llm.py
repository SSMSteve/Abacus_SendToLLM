"""
Enhanced chat system for LLM interactions with multiple provider support
Supports Abacus.AI, OpenAI, and other providers with file attachments
"""

import json
import os
import requests
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass
from .config import get_config, ModelConfig

@dataclass
class ChatMessage:
    """Represents a chat message"""
    role: str  # 'user', 'assistant', 'system'
    content: str
    attachments: Optional[List[Dict[str, Any]]] = None

@dataclass
class ChatResponse:
    """Represents a response from the LLM"""
    content: str
    model: str
    provider: str
    usage: Optional[Dict[str, Any]] = None
    raw_response: Optional[Dict[str, Any]] = None

class LLMChatClient:
    """Universal chat client for multiple LLM providers"""
    
    def __init__(self, model_name: Optional[str] = None):
        self.config = get_config()
        self.model_config = self.config.get_model_config(model_name)
        self.conversation_history: List[ChatMessage] = []
    
    def add_message(self, role: str, content: str, attachments: Optional[List[Dict[str, Any]]] = None):
        """Add a message to the conversation history"""
        message = ChatMessage(role=role, content=content, attachments=attachments)
        self.conversation_history.append(message)
    
    def clear_history(self):
        """Clear the conversation history"""
        self.conversation_history = []
    
    def send_message(self, 
                    message: str, 
                    attachments: Optional[List[str]] = None,
                    system_prompt: Optional[str] = None,
                    include_history: bool = True) -> ChatResponse:
        """
        Send a message to the LLM
        
        Args:
            message: The user message to send
            attachments: List of file paths to attach
            system_prompt: Optional system prompt
            include_history: Whether to include conversation history
        
        Returns:
            ChatResponse object with the LLM's response
        """
        
        # Process attachments if provided
        processed_attachments = []
        if attachments:
            processed_attachments = self._process_attachments(attachments)
        
        # Add system prompt if provided
        if system_prompt and not include_history:
            self.add_message('system', system_prompt)
        
        # Add user message
        self.add_message('user', message, processed_attachments)
        
        # Send to appropriate provider
        if self.model_config.provider == 'abacus':
            response = self._send_to_abacus(include_history)
        elif self.model_config.provider == 'openai':
            response = self._send_to_openai(include_history)
        elif self.model_config.provider == 'anthropic':
            response = self._send_to_anthropic(include_history)
        else:
            raise ValueError(f"Unsupported provider: {self.model_config.provider}")
        
        # Add assistant response to history
        self.add_message('assistant', response.content)
        
        return response
    
    def _process_attachments(self, attachment_paths: List[str]) -> List[Dict[str, Any]]:
        """Process file attachments"""
        processed = []
        
        for path in attachment_paths:
            if not os.path.exists(path):
                print(f"Warning: Attachment file not found: {path}")
                continue
            
            try:
                # Read file content
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Determine file type
                file_ext = os.path.splitext(path)[1].lower()
                if file_ext == '.json':
                    try:
                        content = json.loads(content)
                        file_type = 'json'
                    except json.JSONDecodeError:
                        file_type = 'text'
                elif file_ext in ['.md', '.txt']:
                    file_type = 'text'
                else:
                    file_type = 'text'
                
                processed.append({
                    'filename': os.path.basename(path),
                    'path': path,
                    'type': file_type,
                    'content': content
                })
                
            except Exception as e:
                print(f"Error processing attachment {path}: {e}")
        
        return processed
    
    def _send_to_abacus(self, include_history: bool) -> ChatResponse:
        """Send message to Abacus.AI"""
        url = f"{self.model_config.base_url}/getChatResponse"
        
        headers = {"Content-Type": "application/json"}
        if self.model_config.api_key:
            headers["apiKey"] = self.model_config.api_key
        
        # Prepare messages
        messages = []
        if include_history:
            for msg in self.conversation_history:
                abacus_msg = {
                    "is_user": msg.role == 'user',
                    "text": msg.content
                }
                
                # Add attachments for Abacus format
                if msg.attachments:
                    attachment_text = self._format_attachments_for_abacus(msg.attachments)
                    abacus_msg["text"] = str(abacus_msg["text"]) + f"\n\n{attachment_text}"
                
                messages.append(abacus_msg)
        else:
            # Just the last message
            last_msg = self.conversation_history[-1]
            abacus_msg = {
                "is_user": True,
                "text": last_msg.content
            }
            
            if last_msg.attachments:
                attachment_text = self._format_attachments_for_abacus(last_msg.attachments)
                abacus_msg["text"] = str(abacus_msg["text"]) + f"\n\n{attachment_text}"
            
            messages = [abacus_msg]
        
        payload = {
            "deploymentId": self.model_config.deployment_id,
            "messages": messages,
            "temperature": self.model_config.temperature,
            "numCompletionTokens": self.model_config.max_tokens
        }
        
        if self.model_config.deployment_token:
            payload["deploymentToken"] = self.model_config.deployment_token
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            
            # Extract response content
            if 'result' in result and 'messages' in result['result']:
                messages = result['result']['messages']
                if messages:
                    content = messages[-1].get('text', '')
                else:
                    content = "No response received"
            else:
                content = "Unexpected response format"
            
            return ChatResponse(
                content=str(content),
                model=self.model_config.model_name,
                provider=self.model_config.provider,
                raw_response=result
            )
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Abacus.AI API request failed: {e}")
    
    def _format_attachments_for_abacus(self, attachments: List[Dict[str, Any]]) -> str:
        """Format attachments for Abacus.AI message"""
        if not attachments:
            return ""
        
        parts = ["## Attached Files:"]
        
        for attachment in attachments:
            parts.append(f"\n### {attachment['filename']}")
            
            if attachment['type'] == 'json':
                parts.append("```json")
                parts.append(json.dumps(attachment['content'], indent=2))
                parts.append("```")
            else:
                parts.append("```")
                parts.append(str(attachment['content']))
                parts.append("```")
        
        return "\n".join(parts)
    
    def _send_to_openai(self, include_history: bool) -> ChatResponse:
        """Send message to OpenAI (placeholder for future implementation)"""
        raise NotImplementedError("OpenAI integration not yet implemented")
    
    def _send_to_anthropic(self, include_history: bool) -> ChatResponse:
        """Send message to Anthropic (placeholder for future implementation)"""
        raise NotImplementedError("Anthropic integration not yet implemented")

def create_chat_client(model_name: Optional[str] = None) -> LLMChatClient:
    """Create a new chat client instance"""
    return LLMChatClient(model_name)
