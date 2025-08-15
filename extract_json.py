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
    
    # Clean the content - remove markdown formatting
    cleaned_content = raw_content.strip()
    
    # Remove ```json and ``` markers
    if cleaned_content.startswith('```json'):
        cleaned_content = cleaned_content.replace('```json', '', 1)
    if cleaned_content.endswith('```'):
        cleaned_content = cleaned_content.rsplit('```', 1)[0]
    
    cleaned_content = cleaned_content.strip()
    
    # Fix the JSON syntax error (missing bracket in timeline_of_events)
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
        print(f"📊 Report contains {len(json_data['correlation_report']['matched_pdf_documents'])} matched PDF documents")
        print(f"👤 Patient: {json_data['correlation_report']['patient_information']['name']}")
        print(f"📅 Study Date: {json_data['correlation_report']['dicom_study']['study_date']}")
        
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
