"""
Response Processing for Legacy SendToLLM System

This module handles processing of API responses, JSON extraction,
and output file generation for medical correlation analysis.
"""

import json
from typing import Dict, Any, Optional, Tuple
from .file_operations import OutputManager


class ResponseProcessor:
    """Processes API responses and extracts structured data"""
    
    JSON_START_MARKER = "JSON_REPORT_START"
    JSON_END_MARKER = "JSON_REPORT_END"
    
    def __init__(self, output_manager: Optional[OutputManager] = None):
        self.output_manager = output_manager or OutputManager()
    
    def extract_ai_response(self, api_response: Dict[str, Any]) -> Optional[str]:
        """
        Extract AI response text from API response
        
        Args:
            api_response: Full API response dictionary
            
        Returns:
            AI response text or None if not found
        """
        if 'result' in api_response and 'messages' in api_response['result']:
            messages = api_response['result']['messages']
            if messages and len(messages) > 0:
                # Get the last message (AI response)
                return messages[-1].get('text', '')
        return None
    
    def extract_json_with_markers(self, response_text: str) -> Optional[str]:
        """
        Extract JSON content using start/end markers
        
        Args:
            response_text: Full response text
            
        Returns:
            JSON content string or None if markers not found
        """
        start_pos = response_text.find(self.JSON_START_MARKER)
        end_pos = response_text.find(self.JSON_END_MARKER)
        
        if start_pos != -1 and end_pos != -1:
            start_pos += len(self.JSON_START_MARKER)
            return response_text[start_pos:end_pos].strip()
        
        return None
    
    def extract_json_fallback(self, response_text: str) -> Optional[str]:
        """
        Fallback JSON extraction by finding first { to last }
        
        Args:
            response_text: Full response text
            
        Returns:
            JSON content string or None if not found
        """
        start_pos = response_text.find('{')
        end_pos = response_text.rfind('}') + 1
        
        if start_pos != -1 and end_pos > start_pos:
            return response_text[start_pos:end_pos]
        
        return None
    
    def validate_and_parse_json(self, json_content: str) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
        """
        Validate and parse JSON content
        
        Args:
            json_content: JSON string to validate
            
        Returns:
            Tuple of (is_valid, parsed_data, error_message)
        """
        try:
            parsed_data = json.loads(json_content)
            return True, parsed_data, None
        except json.JSONDecodeError as e:
            return False, None, str(e)
    
    def extract_json_report(self, response_text: str) -> Tuple[bool, Optional[Dict[str, Any]], str]:
        """
        Extract and validate JSON report from response text
        
        Args:
            response_text: Full response text
            
        Returns:
            Tuple of (success, json_data, method_used)
        """
        # Try marker-based extraction first
        json_content = self.extract_json_with_markers(response_text)
        if json_content:
            is_valid, data, error = self.validate_and_parse_json(json_content)
            if is_valid:
                return True, data, "markers"
            else:
                print(f"⚠️  JSON parsing failed with markers: {error}")
                print(f"JSON content preview: {json_content[:200]}...")
        
        # Fallback to brace-based extraction
        json_content = self.extract_json_fallback(response_text)
        if json_content:
            is_valid, data, error = self.validate_and_parse_json(json_content)
            if is_valid:
                return True, data, "fallback"
            else:
                print(f"⚠️  Fallback JSON parsing failed: {error}")
                print(f"JSON content preview: {json_content[:200]}...")
        
        return False, None, "none"
    
    def process_medical_response(self, api_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process medical correlation analysis response
        
        Args:
            api_response: Full API response from Abacus.AI
            
        Returns:
            Processing results dictionary
        """
        results = {
            'success': False,
            'json_saved': False,
            'text_saved': False,
            'raw_saved': False,
            'files_created': [],
            'errors': []
        }
        
        # Extract AI response
        ai_response = self.extract_ai_response(api_response)
        if not ai_response:
            results['errors'].append("No AI response found in API response")
            return results
        
        print("AI Response received, processing and saving files...")
        
        # Save raw response
        try:
            raw_path = self.output_manager.save_raw_response(ai_response)
            results['raw_saved'] = True
            results['files_created'].append(raw_path)
            print(f"Raw response saved to {raw_path}")
        except Exception as e:
            results['errors'].append(f"Failed to save raw response: {e}")
        
        # Extract and save JSON report
        json_success, json_data, method = self.extract_json_report(ai_response)
        
        if json_success and json_data:
            try:
                json_path = self.output_manager.save_json_report(json_data)
                results['json_saved'] = True
                results['files_created'].append(json_path)
                print(f"✅ JSON correlation report saved to {json_path} (method: {method})")
            except Exception as e:
                results['errors'].append(f"Failed to save JSON report: {e}")
        else:
            # Save as text file if JSON extraction fails
            try:
                text_path = self.output_manager.save_text_report(ai_response)
                results['text_saved'] = True
                results['files_created'].append(text_path)
                print(f"⚠️  Could not extract valid JSON, saved as text: {text_path}")
            except Exception as e:
                results['errors'].append(f"Failed to save text report: {e}")
        
        results['success'] = results['json_saved'] or results['text_saved']
        
        # Show preview
        if ai_response:
            print(f"Response preview: {ai_response[:500]}...")
        
        return results
    
    def print_processing_summary(self, results: Dict[str, Any]) -> None:
        """
        Print a summary of processing results
        
        Args:
            results: Results dictionary from process_medical_response
        """
        print("\n" + "="*50)
        print("Response Processing Summary:")
        print("="*50)
        
        if results['success']:
            print("✅ Processing completed successfully")
        else:
            print("❌ Processing failed")
        
        if results['files_created']:
            print(f"📁 Files created: {len(results['files_created'])}")
            for file_path in results['files_created']:
                print(f"   - {file_path}")
        
        if results['errors']:
            print(f"⚠️  Errors encountered: {len(results['errors'])}")
            for error in results['errors']:
                print(f"   - {error}")
        
        print("="*50)
