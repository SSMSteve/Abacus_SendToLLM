"""
Main Application Entry Point for Legacy SendToLLM System

This module provides the main execution logic that was originally
in the if __name__ == "__main__" block of SendToLLM.py
"""

import os
from .api_functions import send_medical_correlation_data_with_attachments
from .response_processor import ResponseProcessor
from .file_operations import OutputManager


def main():
    """
    Main execution function for medical correlation analysis
    """
    print("Sending medical correlation data to LLM with file attachments...")
    
    try:
        # Initialize components
        output_manager = OutputManager()
        processor = ResponseProcessor(output_manager)
        
        # Send medical correlation data
        response = send_medical_correlation_data_with_attachments(
            attachments_dir="./data/to_llm/attachments",
            prompt_file="./data/to_llm/prompt/prompt_v8.txt",
            deployment_token=os.getenv('ABACUS_DEPLOYMENT_TOKEN'),
            deployment_id=os.getenv('ABACUS_DEPLOYMENT_ID')
        )
        
        # Process the response
        results = processor.process_medical_response(response)
        
        # Print summary
        processor.print_processing_summary(results)
        
        if not results['success']:
            print("❌ Processing failed - check errors above")
            return 1
        
        print("\n" + "="*50)
        print("Medical Correlation Report Generation Complete!")
        print("="*50)
        
        return 0
        
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
