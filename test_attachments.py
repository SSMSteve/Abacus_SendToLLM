#!/usr/bin/env python3
"""
Test script for SendToLLM.py attachment functionality
"""

import os
from SendToLLM import (
    validate_attachments_directory, 
    upload_file_to_abacus, 
    send_chat_with_attachments,
    send_medical_correlation_data_with_attachments
)

def test_attachment_validation():
    """Test attachment directory validation"""
    print("Testing attachment validation...")
    print("=" * 50)
    
    attachments_dir = "./data/to_llm/attachments"
    
    try:
        file_status = validate_attachments_directory(attachments_dir)
        print("✅ Attachment validation successful")
        
        for key, status in file_status.items():
            status_icon = "✅" if status['exists'] else "❌"
            print(f"  {status_icon} {key}: {status['filename']}")
            
        return True
    except Exception as e:
        print(f"❌ Attachment validation failed: {e}")
        return False

def test_file_upload_dry_run():
    """Test file upload preparation (without actual upload)"""
    print("\nTesting file upload preparation...")
    print("=" * 50)
    
    attachments_dir = "./data/to_llm/attachments"
    
    try:
        file_status = validate_attachments_directory(attachments_dir)
        
        print("Files ready for upload:")
        for key, status in file_status.items():
            if status['exists']:
                file_size = os.path.getsize(status['path'])
                print(f"  📄 {status['filename']}")
                print(f"     Path: {status['path']}")
                print(f"     Size: {file_size:,} bytes")
                print(f"     Ready: ✅")
            else:
                print(f"  ❌ {status['filename']} - Missing")
        
        return True
    except Exception as e:
        print(f"❌ File upload preparation failed: {e}")
        return False

def test_prompt_loading():
    """Test prompt file loading"""
    print("\nTesting prompt loading...")
    print("=" * 50)
    
    prompt_file = "./data/to_llm/prompt/prompt_v8.txt"
    
    try:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            prompt_content = f.read()
        
        print(f"✅ Prompt loaded successfully")
        print(f"   File: {prompt_file}")
        print(f"   Size: {len(prompt_content):,} characters")
        print(f"   Preview: {prompt_content[:150]}...")
        
        return True
    except Exception as e:
        print(f"❌ Prompt loading failed: {e}")
        return False

def test_environment_variables():
    """Test if required environment variables are set"""
    print("\nTesting environment variables...")
    print("=" * 50)
    
    required_vars = ['ABACUS_DEPLOYMENT_TOKEN', 'ABACUS_DEPLOYMENT_ID']
    optional_vars = ['ABACUS_API_KEY']
    
    all_good = True
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: Set (length: {len(value)})")
        else:
            print(f"❌ {var}: Not set (REQUIRED)")
            all_good = False
    
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: Set (length: {len(value)})")
        else:
            print(f"⚠️  {var}: Not set (optional)")
    
    return all_good

def show_usage_examples():
    """Show usage examples"""
    print("\nUsage Examples:")
    print("=" * 50)
    
    print("1. With file attachments (recommended):")
    print("   python SendToLLM.py")
    print("   # Uses send_medical_correlation_data_with_attachments()")
    print()
    
    print("2. With embedded data (legacy):")
    print("   # Modify main() to use send_medical_correlation_data_to_llm()")
    print()
    
    print("3. Environment setup:")
    print("   export ABACUS_DEPLOYMENT_TOKEN='your_token_here'")
    print("   export ABACUS_DEPLOYMENT_ID='your_deployment_id_here'")
    print("   # Optional: export ABACUS_API_KEY='your_api_key_here'")

if __name__ == "__main__":
    print("SendToLLM Attachment Test Suite")
    print("=" * 60)
    
    # Run tests
    validation_ok = test_attachment_validation()
    upload_prep_ok = test_file_upload_dry_run()
    prompt_ok = test_prompt_loading()
    env_ok = test_environment_variables()
    
    print("\nTest Results:")
    print("=" * 60)
    print(f"Attachment Validation: {'✅ PASSED' if validation_ok else '❌ FAILED'}")
    print(f"Upload Preparation: {'✅ PASSED' if upload_prep_ok else '❌ FAILED'}")
    print(f"Prompt Loading: {'✅ PASSED' if prompt_ok else '❌ FAILED'}")
    print(f"Environment Variables: {'✅ PASSED' if env_ok else '❌ FAILED'}")
    
    all_tests_passed = validation_ok and upload_prep_ok and prompt_ok and env_ok
    
    if all_tests_passed:
        print("\n🎉 All tests passed! SendToLLM.py is ready for attachment-based processing.")
        print("\nThe script will now:")
        print("1. 📤 Upload attachment files to Abacus.AI")
        print("2. 💬 Send the prompt with file attachments in chat")
        print("3. 📄 Generate correlation reports from the LLM response")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        
        if not env_ok:
            print("\n🔧 To fix environment variables:")
            print("   Set ABACUS_DEPLOYMENT_TOKEN and ABACUS_DEPLOYMENT_ID")
    
    show_usage_examples()
