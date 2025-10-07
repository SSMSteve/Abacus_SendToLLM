#!/usr/bin/env python3
"""
Test script for the configurable LLM chat system
"""

import os
import sys

# Add src directory to Python path for development imports
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

try:
    from llm_chat import create_chat_client, get_config  # type: ignore[import-untyped]
except ImportError:
    # Fallback for development environment
    import llm_chat  # type: ignore[import-untyped]
    create_chat_client = llm_chat.create_chat_client
    get_config = llm_chat.get_config

def test_configuration():
    """Test that configuration is loaded correctly"""
    print("=== Testing Configuration ===")
    
    try:
        config = get_config()
        print(f"✅ Configuration loaded successfully")
        print(f"Default model: {config.default_model}")
        
        available_models = config.list_available_models()
        print(f"Available models: {list(available_models.keys())}")
        
        # Test getting model config
        model_config = config.get_model_config()
        print(f"Default model config: {model_config.provider}/{model_config.model_name}")
        
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_chat_client_creation():
    """Test creating chat clients"""
    print("\n=== Testing Chat Client Creation ===")
    
    try:
        # Test default client
        chat = create_chat_client()
        print(f"✅ Default chat client created: {chat.model_config.provider}/{chat.model_config.model_name}")
        
        # Test specific model client
        chat_abacus = create_chat_client('abacus-gpt5')
        print(f"✅ Abacus chat client created: {chat_abacus.model_config.provider}/{chat_abacus.model_config.model_name}")
        
        return True
    except Exception as e:
        print(f"❌ Chat client creation test failed: {e}")
        return False

def test_message_preparation():
    """Test message preparation without actually sending"""
    print("\n=== Testing Message Preparation ===")
    
    try:
        chat = create_chat_client()
        
        # Add a test message
        chat.add_message('user', 'Test message')
        print(f"✅ Message added to history: {len(chat.conversation_history)} messages")
        
        # Test attachment processing
        test_files = []
        for file_path in ['./data/prompt_v14.txt', './README.md', './config.py']:
            if os.path.exists(file_path):
                test_files.append(file_path)
        
        if test_files:
            attachments = chat._process_attachments(test_files)
            print(f"✅ Processed {len(attachments)} attachments from {len(test_files)} files")
            for att in attachments:
                print(f"   - {att['filename']} ({att['type']})")
        else:
            print("⚠️  No test files found for attachment processing")
        
        return True
    except Exception as e:
        print(f"❌ Message preparation test failed: {e}")
        return False

def test_environment_variables():
    """Test that required environment variables are set"""
    print("\n=== Testing Environment Variables ===")
    
    required_vars = {
        'ABACUS_DEPLOYMENT_ID': os.getenv('ABACUS_DEPLOYMENT_ID'),
        'ABACUS_DEPLOYMENT_TOKEN': os.getenv('ABACUS_DEPLOYMENT_TOKEN'),
        'ABACUS_API_KEY': os.getenv('ABACUS_API_KEY')
    }
    
    print("Environment variables status:")
    for var_name, var_value in required_vars.items():
        if var_value:
            print(f"✅ {var_name}: Set (length: {len(var_value)})")
        else:
            print(f"❌ {var_name}: Not set")
    
    # Check if we have minimum required credentials
    has_auth = bool(required_vars['ABACUS_DEPLOYMENT_TOKEN'] or required_vars['ABACUS_API_KEY'])
    has_deployment = bool(required_vars['ABACUS_DEPLOYMENT_ID'])
    
    if has_auth and has_deployment:
        print("✅ Minimum required credentials are available")
        return True
    else:
        print("❌ Missing required credentials for Abacus.AI")
        print("   Set either ABACUS_DEPLOYMENT_TOKEN or ABACUS_API_KEY")
        print("   Set ABACUS_DEPLOYMENT_ID")
        return False

def test_actual_api_call():
    """Test an actual API call (if credentials are available)"""
    print("\n=== Testing Actual API Call ===")
    
    if not test_environment_variables():
        print("⚠️  Skipping API test due to missing credentials")
        return False
    
    try:
        chat = create_chat_client('abacus-gpt5')
        
        print("Sending test message to Abacus.AI...")
        response = chat.send_message(
            message="Hello! Please respond with just 'Hello back!' to confirm the connection is working.",
            include_history=False
        )
        
        print(f"✅ API call successful!")
        print(f"Model: {response.model} ({response.provider})")
        print(f"Response length: {len(response.content)} characters")
        print(f"Response preview: {response.content[:100]}...")
        
        return True
    except Exception as e:
        print(f"❌ API call test failed: {e}")
        print("This might be due to:")
        print("  - Invalid credentials")
        print("  - Network connectivity issues")
        print("  - Abacus.AI service unavailable")
        return False

def main():
    """Run all tests"""
    print("LLM Chat System Test Suite")
    print("=" * 50)
    
    tests = [
        test_configuration,
        test_chat_client_creation,
        test_message_preparation,
        test_environment_variables,
    ]
    
    # Only run API test if user confirms
    if len(sys.argv) > 1 and sys.argv[1] == '--include-api':
        tests.append(test_actual_api_call)
        print("Note: Including actual API test (may use credits)")
    else:
        print("Note: Skipping actual API test. Use --include-api to test API calls")
    
    print()
    
    results = []
    for test_func in tests:
        result = test_func()
        results.append(result)
    
    print("\n" + "=" * 50)
    print("Test Results Summary:")
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! The system is ready to use.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        print("\nCommon issues:")
        print("- Missing environment variables (copy .env.example to .env)")
        print("- Invalid Abacus.AI credentials")
        print("- Missing data files")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
