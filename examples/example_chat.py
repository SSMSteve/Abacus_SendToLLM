#!/usr/bin/env python3
"""
Example usage of the configurable LLM chat system
Demonstrates how to use different models and handle attachments
"""

import os
import sys
import json

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from llm_chat import create_chat_client, get_config

def example_basic_chat():
    """Example of basic chat without attachments"""
    print("=== Basic Chat Example ===")
    
    # Create chat client with default model (abacus-gpt5)
    chat = create_chat_client()
    
    # Send a simple message
    response = chat.send_message("Hello! Can you help me analyze some data?")
    print(f"Model: {response.model} ({response.provider})")
    print(f"Response: {response.content[:200]}...")
    print()

def example_chat_with_attachments():
    """Example of chat with file attachments"""
    print("=== Chat with Attachments Example ===")
    
    # Create chat client
    chat = create_chat_client('abacus-gpt5')
    
    # Prepare some sample files (if they exist)
    attachment_files = []
    
    # Check for existing data files
    data_files = [
        './data/24-12-00016_aggregated_data_for_LLM.json',
        './data/correlation_report.json',
        './data/prompt_v14.txt'
    ]
    
    for file_path in data_files:
        if os.path.exists(file_path):
            attachment_files.append(file_path)
    
    if attachment_files:
        print(f"Found {len(attachment_files)} files to attach:")
        for file_path in attachment_files:
            print(f"  - {file_path}")
        
        # Send message with attachments
        message = "Please analyze the attached files and provide a summary of the key information."
        response = chat.send_message(
            message=message,
            attachments=attachment_files
        )
        
        print(f"Model: {response.model} ({response.provider})")
        print(f"Response: {response.content[:300]}...")
        
        # Save response to output
        os.makedirs('./output', exist_ok=True)
        with open('./output/chat_response.txt', 'w', encoding='utf-8') as f:
            f.write(response.content)
        print("Full response saved to ./output/chat_response.txt")
    else:
        print("No data files found for attachment example")
    print()

def example_conversation():
    """Example of multi-turn conversation"""
    print("=== Multi-turn Conversation Example ===")
    
    chat = create_chat_client()
    
    # First message
    response1 = chat.send_message("What is machine learning?")
    print(f"User: What is machine learning?")
    print(f"Assistant: {response1.content[:150]}...")
    print()
    
    # Follow-up message (includes history)
    response2 = chat.send_message("Can you give me a specific example?")
    print(f"User: Can you give me a specific example?")
    print(f"Assistant: {response2.content[:150]}...")
    print()

def example_different_models():
    """Example of using different model configurations"""
    print("=== Different Models Example ===")
    
    config = get_config()
    available_models = config.list_available_models()
    
    print("Available models:")
    for model_name, provider in available_models.items():
        print(f"  - {model_name} ({provider})")
    
    # Try to use different models (if configured)
    for model_name in ['abacus-gpt5', 'openai-gpt4']:
        if model_name in available_models:
            try:
                print(f"\nTesting {model_name}:")
                chat = create_chat_client(model_name)
                response = chat.send_message("Hello, what model are you?")
                print(f"Response: {response.content[:100]}...")
            except Exception as e:
                print(f"Error with {model_name}: {e}")
    print()

def example_medical_correlation():
    """Example specifically for medical correlation analysis"""
    print("=== Medical Correlation Analysis Example ===")
    
    # Check for medical data files
    medical_files = [
        './data/to_llm/attachments/keyword_search_results_27977577.json',
        './data/to_llm/attachments/vector_search_results_27977577.json',
        './data/to_llm/attachments/Correlation_Report.md'
    ]
    
    existing_files = [f for f in medical_files if os.path.exists(f)]
    
    if existing_files:
        print(f"Found {len(existing_files)} medical data files")
        
        # Load prompt
        prompt_file = './data/to_llm/prompt/prompt_v8.txt'
        if os.path.exists(prompt_file):
            with open(prompt_file, 'r', encoding='utf-8') as f:
                prompt = f.read()
        else:
            prompt = "Please analyze the attached medical correlation data and provide a comprehensive report."
        
        chat = create_chat_client('abacus-gpt5')
        
        response = chat.send_message(
            message=prompt,
            attachments=existing_files
        )
        
        print(f"Medical analysis response length: {len(response.content)} characters")
        
        # Try to extract JSON if present
        try:
            if "JSON_REPORT_START" in response.content:
                json_start = response.content.find("JSON_REPORT_START") + len("JSON_REPORT_START")
                json_end = response.content.find("JSON_REPORT_END")
                if json_end != -1:
                    json_content = response.content[json_start:json_end].strip()
                    json_data = json.loads(json_content)
                    
                    os.makedirs('./output', exist_ok=True)
                    with open('./output/medical_correlation_report.json', 'w', encoding='utf-8') as f:
                        json.dump(json_data, f, indent=4, ensure_ascii=False)
                    print("✅ Medical correlation report saved to ./output/medical_correlation_report.json")
        except Exception as e:
            print(f"Could not extract JSON: {e}")
        
        # Save full response
        os.makedirs('./output', exist_ok=True)
        with open('./output/medical_analysis_full.txt', 'w', encoding='utf-8') as f:
            f.write(response.content)
        print("Full medical analysis saved to ./output/medical_analysis_full.txt")
    else:
        print("No medical data files found")
    print()

def main():
    """Run all examples"""
    print("LLM Chat System Examples")
    print("=" * 50)
    
    try:
        # Check configuration
        config = get_config()
        print(f"Default model: {config.default_model}")
        print(f"Available models: {list(config.list_available_models().keys())}")
        print()
        
        # Run examples
        example_basic_chat()
        example_chat_with_attachments()
        example_conversation()
        example_different_models()
        example_medical_correlation()
        
    except Exception as e:
        print(f"Error running examples: {e}")
        print("Make sure you have set the required environment variables:")
        print("  - ABACUS_DEPLOYMENT_TOKEN or ABACUS_API_KEY")
        print("  - ABACUS_DEPLOYMENT_ID")

if __name__ == "__main__":
    main()
