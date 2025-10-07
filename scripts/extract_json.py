#!/usr/bin/env python3
"""
Extract JSON from raw_response.txt and save to report.json
"""
import json
import os

def extract_and_save_json():
    """Extract JSON from raw response and save to report.json"""
    
    # Read the raw response
    try:
        with open('./output/raw_response.txt', 'r', encoding='utf-8') as file:
            raw_content = file.read()
    except FileNotFoundError:
        print("❌ Error: ./output/raw_response.txt not found")
        return False
    
    # Clean the content - remove markdown formatting and extract JSON
    cleaned_content = raw_content.strip()

    # Find JSON content between ```json and ``` markers
    json_start_marker = '```json'
    json_end_marker = '```'

    json_start = cleaned_content.find(json_start_marker)
    if json_start != -1:
        # Start after the ```json marker
        json_start += len(json_start_marker)
        # Find the closing ``` marker
        json_end = cleaned_content.find(json_end_marker, json_start)
        if json_end != -1:
            cleaned_content = cleaned_content[json_start:json_end].strip()
        else:
            # If no closing marker, take everything after ```json
            cleaned_content = cleaned_content[json_start:].strip()
    else:
        # If no ```json marker, try to find JSON by looking for opening brace
        brace_start = cleaned_content.find('{')
        if brace_start != -1:
            # Find the last closing brace
            brace_end = cleaned_content.rfind('}')
            if brace_end != -1 and brace_end > brace_start:
                cleaned_content = cleaned_content[brace_start:brace_end + 1].strip()

    # Fix common JSON syntax errors (if any)
    # This is a specific fix for a known issue - can be removed if not needed
    if '"timeline_of_events"' in cleaned_content:
        cleaned_content = cleaned_content.replace(
            '"2024-05-15: Surgery scheduled after patient consent. *(Source: Document 4, Page 579)*"\n    }',
            '"2024-05-15: Surgery scheduled after patient consent. *(Source: Document 4, Page 579)*"\n    ]'
        )
    
    try:
        # Parse the JSON to validate it
        json_data = json.loads(cleaned_content)
        
        # Create output directory if it doesn't exist
        os.makedirs('./output', exist_ok=True)
        
        # Save to report.json
        with open('./output/report.json', 'w', encoding='utf-8') as output_file:
            json.dump(json_data, output_file, indent=4, ensure_ascii=False)
        
        print("✅ Successfully extracted and saved JSON to ./output/report.json")

        # Try to print summary information if available
        try:
            if 'correlation_report' in json_data:
                # Old format
                report_data = json_data['correlation_report']
                if 'matched_pdf_documents' in report_data:
                    print(f"📊 Report contains {len(report_data['matched_pdf_documents'])} matched PDF documents")
                if 'patient_information' in report_data:
                    print(f"👤 Patient: {report_data['patient_information']['name']}")
                if 'dicom_study' in report_data:
                    print(f"📅 Study Date: {report_data['dicom_study']['study_date']}")
            else:
                # New format - direct structure
                if 'patient_information' in json_data:
                    print(f"👤 Patient: {json_data['patient_information']['name']}")
                if 'dicom_study' in json_data:
                    print(f"📅 Study Date: {json_data['dicom_study']['study_date']}")

                # Count documents from both search results
                doc_count = 0
                if 'keyword_search_results' in json_data:
                    doc_count += len(json_data['keyword_search_results'])
                if 'vector_search_results' in json_data:
                    doc_count += len(json_data['vector_search_results'])
                if doc_count > 0:
                    print(f"📊 Report contains {doc_count} matched PDF documents")
        except Exception as e:
            print(f"ℹ️  Could not extract summary info: {e}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        print("Raw content preview:")
        print(cleaned_content[:500] + "..." if len(cleaned_content) > 500 else cleaned_content)
        return False
    
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    extract_and_save_json()
