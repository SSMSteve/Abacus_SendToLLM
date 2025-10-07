#!/usr/bin/env python3
"""
Comprehensive example demonstrating the cleaned-up LLM Chat System
Shows all major features and usage patterns
"""

import os
import sys
import json
from pathlib import Path

# Add src directory to path for development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from llm_chat import create_chat_client, get_config, ModelConfig

def demonstrate_configuration():
    """Demonstrate configuration management"""
    print("=== Configuration Management ===")
    
    config = get_config()
    
    # Show available models
    print("Available models:")
    for model_name, provider in config.list_available_models().items():
        print(f"  - {model_name} ({provider})")
    
    print(f"Default model: {config.default_model}")
    
    # Add a custom model
    custom_model = ModelConfig(
        provider='abacus',
        model_name='custom-gpt5',
        deployment_id=os.getenv('ABACUS_DEPLOYMENT_ID'),
        api_key=os.getenv('ABACUS_API_KEY'),
        temperature=0.1,
        max_tokens=8000
    )
    config.add_custom_model('high-precision', custom_model)
    print("Added custom 'high-precision' model")
    print()

def demonstrate_basic_chat():
    """Demonstrate basic chat functionality"""
    print("=== Basic Chat ===")
    
    try:
        chat = create_chat_client()
        response = chat.send_message("Hello! Please respond with just 'Hello back!' to confirm the connection.")
        print(f"Model: {response.model} ({response.provider})")
        print(f"Response: {response.content[:100]}...")
        print()
        return True
    except Exception as e:
        print(f"Error in basic chat: {e}")
        return False

def demonstrate_conversation():
    """Demonstrate multi-turn conversation"""
    print("=== Multi-turn Conversation ===")
    
    try:
        chat = create_chat_client()
        
        # First message
        response1 = chat.send_message("What is the capital of France?")
        print(f"Q: What is the capital of France?")
        print(f"A: {response1.content[:100]}...")
        
        # Follow-up with history
        response2 = chat.send_message("What's the population of that city?")
        print(f"Q: What's the population of that city?")
        print(f"A: {response2.content[:100]}...")
        
        print(f"Conversation history: {len(chat.conversation_history)} messages")
        print()
        return True
    except Exception as e:
        print(f"Error in conversation: {e}")
        return False

def demonstrate_file_attachments():
    """Demonstrate file attachment processing"""
    print("=== File Attachments ===")
    
    # Create sample files for demonstration
    sample_data = {
        "patient": "John Doe",
        "age": 45,
        "diagnosis": "Hypertension",
        "medications": ["Lisinopril", "Hydrochlorothiazide"]
    }
    
    sample_report = """# Medical Report
    
Patient: John Doe
Age: 45
Diagnosis: Hypertension

## Treatment Plan
- Continue current medications
- Follow-up in 3 months
- Monitor blood pressure daily
"""
    
    # Ensure output directory exists
    os.makedirs('output', exist_ok=True)
    
    # Write sample files
    with open('output/sample_data.json', 'w') as f:
        json.dump(sample_data, f, indent=2)
    
    with open('output/sample_report.md', 'w') as f:
        f.write(sample_report)
    
    try:
        chat = create_chat_client()
        response = chat.send_message(
            message="Please analyze the attached medical data and provide a summary.",
            attachments=['output/sample_data.json', 'output/sample_report.md']
        )
        
        print("Sent message with 2 attachments:")
        print("  - sample_data.json (JSON)")
        print("  - sample_report.md (Markdown)")
        print(f"Response: {response.content[:200]}...")
        print()
        return True
    except Exception as e:
        print(f"Error with attachments: {e}")
        return False

def demonstrate_model_switching():
    """Demonstrate switching between different models"""
    print("=== Model Switching ===")
    
    models_to_test = ['abacus-gpt5', 'high-precision']
    
    for model_name in models_to_test:
        try:
            chat = create_chat_client(model_name)
            response = chat.send_message("What model are you?", include_history=False)
            print(f"Model {model_name}: {response.content[:100]}...")
        except Exception as e:
            print(f"Error with {model_name}: {e}")
    
    print()

def demonstrate_medical_workflow():
    """Demonstrate medical correlation workflow"""
    print("=== Medical Correlation Workflow ===")
    
    # Check for medical data files
    medical_files = [
        './data/to_llm/attachments/keyword_search_results_27977577.json',
        './data/to_llm/attachments/vector_search_results_27977577.json',
        './data/to_llm/attachments/Correlation_Report.md'
    ]
    
    existing_files = [f for f in medical_files if os.path.exists(f)]
    
    if not existing_files:
        print("No medical data files found. Skipping medical workflow demo.")
        print("Expected files:")
        for file_path in medical_files:
            print(f"  - {file_path}")
        print()
        return False
    
    print(f"Found {len(existing_files)} medical data files")
    
    # Load prompt if available
    prompt_file = './data/to_llm/prompt/prompt_v8.txt'
    if os.path.exists(prompt_file):
        with open(prompt_file, 'r', encoding='utf-8') as f:
            prompt = f.read()
    else:
        prompt = """Please analyze the attached medical correlation data and provide a comprehensive report.
        
Focus on:
1. Patient information correlation
2. DICOM study details
3. PDF document matches
4. Timeline of events
5. Key findings and recommendations

Provide the response in JSON format."""
    
    try:
        chat = create_chat_client('abacus-gpt5')
        response = chat.send_message(
            message=prompt,
            attachments=existing_files
        )
        
        print(f"Medical analysis completed. Response length: {len(response.content)} characters")
        
        # Try to extract JSON if present
        if "JSON_REPORT_START" in response.content or response.content.strip().startswith('{'):
            try:
                # Look for JSON content
                json_start = response.content.find('{')
                json_end = response.content.rfind('}') + 1
                
                if json_start != -1 and json_end > json_start:
                    json_content = response.content[json_start:json_end]
                    json_data = json.loads(json_content)
                    
                    # Save the report
                    os.makedirs('output', exist_ok=True)
                    with open('output/medical_correlation_report.json', 'w', encoding='utf-8') as f:
                        json.dump(json_data, f, indent=4, ensure_ascii=False)
                    
                    print("✅ Medical correlation report saved to output/medical_correlation_report.json")
                    
                    # Show summary
                    if 'patient_information' in json_data:
                        print(f"Patient: {json_data['patient_information'].get('name', 'Unknown')}")
                    if 'dicom_study' in json_data:
                        print(f"Study Date: {json_data['dicom_study'].get('study_date', 'Unknown')}")
                
            except json.JSONDecodeError as e:
                print(f"Could not parse JSON from response: {e}")
        
        # Save full response
        with open('output/medical_analysis_full.txt', 'w', encoding='utf-8') as f:
            f.write(response.content)
        print("Full analysis saved to output/medical_analysis_full.txt")
        print()
        return True
        
    except Exception as e:
        print(f"Error in medical workflow: {e}")
        return False

def demonstrate_error_handling():
    """Demonstrate error handling"""
    print("=== Error Handling ===")
    
    # Test invalid model
    try:
        chat = create_chat_client('invalid-model')
    except ValueError as e:
        print(f"✅ Caught expected error for invalid model: {e}")
    
    # Test missing file
    try:
        chat = create_chat_client()
        response = chat.send_message("Test", attachments=['nonexistent.json'])
    except Exception as e:
        print(f"✅ Caught expected error for missing file: {type(e).__name__}")
    
    print()

def main():
    """Run comprehensive demonstration"""
    print("LLM Chat System - Comprehensive Example")
    print("=" * 50)
    
    # Check environment
    required_vars = ['ABACUS_DEPLOYMENT_ID']
    auth_vars = ['ABACUS_API_KEY', 'ABACUS_DEPLOYMENT_TOKEN']
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    has_auth = any(os.getenv(var) for var in auth_vars)
    
    if missing_vars or not has_auth:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"  - {var}")
        if not has_auth:
            print(f"  - One of: {', '.join(auth_vars)}")
        print("\nPlease set these variables and try again.")
        return
    
    print("✅ Environment configuration looks good")
    print()
    
    # Run demonstrations
    demos = [
        demonstrate_configuration,
        demonstrate_basic_chat,
        demonstrate_conversation,
        demonstrate_file_attachments,
        demonstrate_model_switching,
        demonstrate_medical_workflow,
        demonstrate_error_handling
    ]
    
    results = []
    for demo in demos:
        try:
            result = demo()
            results.append(result if result is not None else True)
        except Exception as e:
            print(f"Demo failed: {e}")
            results.append(False)
    
    # Summary
    print("=" * 50)
    print("Demonstration Summary:")
    passed = sum(1 for r in results if r)
    total = len(results)
    print(f"Completed: {passed}/{total} demonstrations")
    
    if passed == total:
        print("🎉 All demonstrations completed successfully!")
    else:
        print("⚠️  Some demonstrations had issues. Check the output above.")
    
    print("\nGenerated files:")
    output_files = [
        'output/sample_data.json',
        'output/sample_report.md',
        'output/medical_correlation_report.json',
        'output/medical_analysis_full.txt'
    ]
    
    for file_path in output_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} (not created)")

if __name__ == "__main__":
    main()
