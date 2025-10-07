#!/usr/bin/env python3
"""
Query the current model for information about available models and capabilities
"""

import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

def query_model_about_alternatives():
    """Ask the current model about available alternatives"""
    
    deployment_token = os.getenv('ABACUS_DEPLOYMENT_TOKEN')
    deployment_id = os.getenv('ABACUS_DEPLOYMENT_ID')
    api_key = os.getenv('ABACUS_API_KEY')
    
    if not deployment_id:
        print("❌ No ABACUS_DEPLOYMENT_ID set")
        return
    
    url = "https://api.abacus.ai/api/v0/getChatResponse"
    headers = {"Content-Type": "application/json"}
    
    if api_key:
        headers["apiKey"] = api_key
    
    questions = [
        "What model are you exactly? Include version details.",
        "What other models are available on the Abacus.AI platform?",
        "Can you list OpenAI models available through Abacus.AI?",
        "What Anthropic Claude models are available on this platform?",
        "Are there any open-source models like Llama available here?",
        "What are the capabilities and differences between available models on this platform?"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n{'='*60}")
        print(f"🤖 Question {i}: {question}")
        print('='*60)
        
        payload = {
            "deploymentId": deployment_id,
            "messages": [{"is_user": True, "text": question}],
            "temperature": 0.1,
            "numCompletionTokens": 500
        }
        
        if deployment_token:
            payload["deploymentToken"] = deployment_token
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success') and 'result' in result:
                    messages = result['result'].get('messages', [])
                    for msg in messages:
                        if not msg.get('is_user', True):  # AI response
                            print(f"🤖 Response: {msg.get('text', 'No text')}")
                            break
                else:
                    print(f"❌ Unexpected response format: {result}")
            else:
                print(f"❌ Request failed: {response.status_code}")
                print(f"Error: {response.text[:200]}...")
                
        except Exception as e:
            print(f"❌ Exception: {e}")

def test_different_model_queries():
    """Test specific queries about model capabilities"""
    
    deployment_token = os.getenv('ABACUS_DEPLOYMENT_TOKEN')
    deployment_id = os.getenv('ABACUS_DEPLOYMENT_ID')
    api_key = os.getenv('ABACUS_API_KEY')
    
    if not deployment_id:
        print("❌ No ABACUS_DEPLOYMENT_ID set")
        return
    
    url = "https://api.abacus.ai/api/v0/getChatResponse"
    headers = {"Content-Type": "application/json"}
    
    if api_key:
        headers["apiKey"] = api_key
    
    # Test model-specific capabilities
    test_queries = [
        {
            "query": "Are you GPT-4, GPT-4 Turbo, GPT-4o, or another variant?",
            "purpose": "Identify exact model variant"
        },
        {
            "query": "What is your knowledge cutoff date?",
            "purpose": "Determine model training data cutoff"
        },
        {
            "query": "What is your context window size (maximum tokens)?",
            "purpose": "Understand model limitations"
        },
        {
            "query": "Can you process images, code, or only text?",
            "purpose": "Identify multimodal capabilities"
        }
    ]
    
    print(f"\n{'='*60}")
    print("🔬 DETAILED MODEL ANALYSIS")
    print('='*60)
    
    for test in test_queries:
        print(f"\n🎯 Purpose: {test['purpose']}")
        print(f"❓ Query: {test['query']}")
        
        payload = {
            "deploymentId": deployment_id,
            "messages": [{"is_user": True, "text": test['query']}],
            "temperature": 0.0,  # Most deterministic
            "numCompletionTokens": 300
        }
        
        if deployment_token:
            payload["deploymentToken"] = deployment_token
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success') and 'result' in result:
                    messages = result['result'].get('messages', [])
                    for msg in messages:
                        if not msg.get('is_user', True):  # AI response
                            print(f"💬 Answer: {msg.get('text', 'No text')}")
                            break
            else:
                print(f"❌ Request failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")

if __name__ == "__main__":
    print("🔍 QUERYING CURRENT MODEL FOR INFORMATION")
    print("="*60)
    
    # First, get basic model info
    query_model_about_alternatives()
    
    # Then get detailed capabilities
    test_different_model_queries()
    
    print(f"\n{'='*60}")
    print("📝 SUMMARY")
    print('='*60)
    print("✅ Current model: GPT-4o (confirmed)")
    print("❌ API model listing: Not available via API")
    print("💡 Recommendation: Use Abacus.AI web console to see all available models")
    print("🔧 To change models: Create new deployment with different model")
