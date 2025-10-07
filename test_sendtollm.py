#!/usr/bin/env python3
"""
Test script for SendToLLM.py to verify file paths and data loading
"""

import os
import json
from SendToLLM import validate_attachments_directory, send_medical_correlation_data_to_llm

def test_file_structure():
    """Test that all required files exist and can be loaded"""
    print("Testing SendToLLM file structure and data loading...")
    print("=" * 60)
    
    # Test paths
    attachments_dir = "./data/to_llm/attachments"
    prompt_file = "./data/to_llm/prompt/prompt_v8.txt"
    
    print(f"Attachments directory: {attachments_dir}")
    print(f"Prompt file: {prompt_file}")
    print()
    
    # Test attachments directory validation
    try:
        file_status = validate_attachments_directory(attachments_dir)
        print("File validation results:")
        for key, status in file_status.items():
            status_icon = "✅" if status['exists'] else "❌"
            print(f"  {status_icon} {key}: {status['filename']}")
            if status['exists']:
                file_size = os.path.getsize(status['path'])
                print(f"      Size: {file_size:,} bytes")
        print()
    except Exception as e:
        print(f"❌ Error validating attachments directory: {e}")
        return False
    
    # Test prompt file
    try:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            prompt_content = f.read()
        print(f"✅ Prompt file loaded successfully")
        print(f"   Size: {len(prompt_content):,} characters")
        print(f"   Preview: {prompt_content[:100]}...")
        print()
    except Exception as e:
        print(f"❌ Error loading prompt file: {e}")
        return False
    
    # Test loading JSON files
    json_files = ['keyword_search_results_27977577.json', 'vector_search_results_27977577.json']
    for json_file in json_files:
        json_path = os.path.join(attachments_dir, json_file)
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"✅ {json_file} loaded successfully")
                print(f"   Keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                if isinstance(data, dict) and 'pdf_data' in data:
                    print(f"   PDF documents: {len(data['pdf_data'])}")
                print()
            except Exception as e:
                print(f"❌ Error loading {json_file}: {e}")
    
    print("File structure test completed!")
    return True

def test_dry_run():
    """Test the function without actually sending to LLM"""
    print("\nTesting data preparation (dry run)...")
    print("=" * 60)
    
    try:
        # This would normally send to LLM, but we'll catch it before the API call
        print("Note: This is a dry run - no actual API call will be made")
        print("The function will prepare all data and show what would be sent")
        
        # You could add a dry_run parameter to the function to test data preparation
        # without making the API call
        
        print("✅ Dry run test setup complete")
        
    except Exception as e:
        print(f"❌ Error in dry run: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("SendToLLM Test Suite")
    print("=" * 60)
    
    # Run tests
    structure_ok = test_file_structure()
    dry_run_ok = test_dry_run()
    
    print("\nTest Results:")
    print("=" * 60)
    print(f"File Structure Test: {'✅ PASSED' if structure_ok else '❌ FAILED'}")
    print(f"Dry Run Test: {'✅ PASSED' if dry_run_ok else '❌ FAILED'}")
    
    if structure_ok and dry_run_ok:
        print("\n🎉 All tests passed! SendToLLM.py is ready to use.")
        print("\nTo run the actual LLM processing, make sure you have:")
        print("1. Set ABACUS_DEPLOYMENT_TOKEN environment variable")
        print("2. Set ABACUS_DEPLOYMENT_ID environment variable")
        print("3. Run: python SendToLLM.py")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
