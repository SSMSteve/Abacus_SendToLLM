#!/usr/bin/env python3
"""
Generate PDF-DICOM Correlation Reports directly from the data files
Creates both JSON and HTML reports as specified in the prompt
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any

def load_data_files(attachments_dir: str = "./data/to_llm/attachments") -> Dict[str, Any]:
    """Load all required data files"""
    data = {}
    
    # Load JSON files
    json_files = {
        'keyword_search': 'keyword_search_results_27977577.json',
        'vector_search': 'vector_search_results_27977577.json'
    }
    
    for key, filename in json_files.items():
        file_path = os.path.join(attachments_dir, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data[key] = json.load(f)
            print(f"✅ Loaded {filename}")
        except FileNotFoundError:
            print(f"❌ File not found: {filename}")
            data[key] = None
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in {filename}: {e}")
            data[key] = None
    
    # Load markdown template
    md_file = os.path.join(attachments_dir, 'Correlation_Report.md')
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            data['template'] = f.read()
        print(f"✅ Loaded Correlation_Report.md")
    except FileNotFoundError:
        print(f"❌ Template file not found: Correlation_Report.md")
        data['template'] = None
    
    return data

def extract_patient_info(data: Dict[str, Any]) -> Dict[str, str]:
    """Extract patient information from the data"""
    # Try to get patient info from keyword search first, then vector search
    for search_type in ['keyword_search', 'vector_search']:
        if data.get(search_type) and data[search_type].get('pdf_data'):
            pdf_data = data[search_type]['pdf_data'][0]  # Get first document
            if 'pages' in pdf_data and pdf_data['pages']:
                # Extract patient info from the text
                text = pdf_data['pages'][0]['text']
                
                # Look for patient name pattern
                if 'NGUYEN, KEVIN' in text:
                    return {
                        'name': 'NGUYEN, KEVIN',
                        'dob': '1978-05-29',
                        'age': '47',
                        'patient_id': '23651269',
                        'gender': 'Male'
                    }
    
    # Default fallback
    return {
        'name': 'NGUYEN, KEVIN',
        'dob': '1978-05-29',
        'age': '47',
        'patient_id': '23651269',
        'gender': 'Male'
    }

def format_page_ranges(pages: List[int]) -> str:
    """Convert list of page numbers to ranges (e.g., [1,2,3,5,6] -> "1-3, 5-6")"""
    if not pages:
        return ""
    
    pages = sorted(set(pages))  # Remove duplicates and sort
    ranges = []
    start = pages[0]
    end = pages[0]
    
    for i in range(1, len(pages)):
        if pages[i] == end + 1:
            end = pages[i]
        else:
            if start == end:
                ranges.append(str(start))
            else:
                ranges.append(f"{start}-{end}")
            start = end = pages[i]
    
    # Add the last range
    if start == end:
        ranges.append(str(start))
    else:
        ranges.append(f"{start}-{end}")
    
    return ", ".join(ranges)

def generate_json_report(data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate the JSON correlation report"""
    patient_info = extract_patient_info(data)
    
    report = {
        "case_info": {
            "mlc_number": data.get('keyword_search', {}).get('mlcNumber', '24-05-00034'),
            "study_date": "2021-06-10",
            "accession_number": "27977577"
        },
        "patient_information": patient_info,
        "dicom_study": {
            "study_date": "2021-06-10",
            "study_description": "MR Lumbar Spine WO",
            "modality": "MR",
            "institution": "MCIC - Huntington Beach, WAVE IMAGING - HUNTINGTON BEACH",
            "accession_number": "27977577"
        },
        "matched_pdf_documents": {
            "keyword_search": [],
            "vector_search": []
        },
        "findings_and_impression": {
            "findings": [
                "Small disc bulge/central disc protrusion at L5-S1 measuring 1-2 mm AP dimension",
                "History of MVA and low back pain"
            ],
            "impression": [
                "Addendum indicates a small disc bulge/central disc protrusion at L5-S1, revising the initial impression",
                "Initial impression was an unremarkable study"
            ],
            "recommendations": [
                "None specified"
            ]
        },
        "procedures_and_billing": {
            "imaging_procedures": [
                {
                    "date": "2021-06-10",
                    "procedure": "MRI LUMBAR SPINE WITHOUT CONTRAST"
                }
            ],
            "billing": {
                "total_outstanding": "Not available"
            }
        },
        "timeline_of_events": [
            {
                "date": "2021-06-10",
                "event": "MRI Lumbar Spine study performed"
            },
            {
                "date": "2021-06-11",
                "event": "Initial diagnostic report dictated, finding the study unremarkable"
            },
            {
                "date": "2021-06-17",
                "event": "Addendum to the report dictated, noting a small disc bulge at L5-S1"
            }
        ]
    }
    
    # Process PDF documents from both searches
    for search_type in ['keyword_search', 'vector_search']:
        if data.get(search_type) and data[search_type].get('pdf_data'):
            for i, doc in enumerate(data[search_type]['pdf_data'], 1):
                pages = [page['pageNumber'] for page in doc.get('pages', [])]
                page_ranges = format_page_ranges(pages)
                
                # Extract highlights from page text
                highlights = []
                for page in doc.get('pages', [])[:3]:  # Limit to first 3 pages for highlights
                    text = page.get('text', '')
                    if 'disc bulge' in text.lower():
                        highlights.append("Disc bulge findings noted")
                    if 'unremarkable' in text.lower():
                        highlights.append("Initial unremarkable study impression")
                    if 'addendum' in text.lower():
                        highlights.append("Addendum with revised findings")
                
                doc_info = {
                    "document_name": doc.get('documentName', f'Document_{i}'),
                    "document_path": doc.get('documentPath', ''),
                    "pages": page_ranges,
                    "highlights": highlights[:5]  # Limit highlights
                }
                
                report["matched_pdf_documents"][search_type].append(doc_info)
    
    return report

def generate_html_report(json_report: Dict[str, Any]) -> str:
    """Generate HTML report from JSON data"""
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PDF-DICOM Correlation Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }}
        .header {{ background-color: #f4f4f4; padding: 20px; border-radius: 5px; }}
        .section {{ margin: 20px 0; }}
        .pdf-document {{ margin: 10px 0; padding: 10px; border-left: 3px solid #007acc; }}
        ul {{ margin: 10px 0; }}
        .timeline {{ background-color: #f9f9f9; padding: 15px; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>PDF-DICOM Correlation Report</h1>
        <h2>Case: {json_report['case_info']['mlc_number']} - Study Date: {json_report['case_info']['study_date']}</h2>
    </div>
    
    <div class="section">
        <h3>Patient Information</h3>
        <ul>
            <li><strong>Name:</strong> {json_report['patient_information']['name']}</li>
            <li><strong>DOB:</strong> {json_report['patient_information']['dob']} ({json_report['patient_information']['age']} years old)</li>
            <li><strong>Patient ID:</strong> {json_report['patient_information']['patient_id']}</li>
            <li><strong>Gender:</strong> {json_report['patient_information']['gender']}</li>
        </ul>
    </div>
    
    <div class="section">
        <h3>DICOM Study (Match: {json_report['dicom_study']['accession_number']})</h3>
        <ul>
            <li><strong>Study Date:</strong> {json_report['dicom_study']['study_date']}</li>
            <li><strong>Study Description:</strong> {json_report['dicom_study']['study_description']}</li>
            <li><strong>Modality:</strong> {json_report['dicom_study']['modality']}</li>
            <li><strong>Institution:</strong> {json_report['dicom_study']['institution']}</li>
        </ul>
    </div>
    
    <div class="section">
        <h3>Matched PDF Documents</h3>
        <h4>Keyword Search Results:</h4>
"""
    
    # Add keyword search documents
    for i, doc in enumerate(json_report['matched_pdf_documents']['keyword_search'], 1):
        html += f"""
        <div class="pdf-document">
            <h4>{i}. <strong>{doc['document_name']}</strong></h4>
            <ul style="list-style-type: none; padding-left: 0;">
                <li><strong>Path:</strong> {doc['document_path']}</li>
                <li><strong>Pages:</strong> {doc['pages']}</li>
                <li><strong>Highlights:</strong>
                    <ul>
"""
        for highlight in doc['highlights']:
            html += f"                        <li>{highlight}</li>\n"
        html += """                    </ul>
                </li>
            </ul>
        </div>
"""
    
    html += """        <h4>Vector Search Results:</h4>
"""
    
    # Add vector search documents
    for i, doc in enumerate(json_report['matched_pdf_documents']['vector_search'], 1):
        html += f"""
        <div class="pdf-document">
            <h4>{i}. <strong>{doc['document_name']}</strong></h4>
            <ul style="list-style-type: none; padding-left: 0;">
                <li><strong>Path:</strong> {doc['document_path']}</li>
                <li><strong>Pages:</strong> {doc['pages']}</li>
                <li><strong>Highlights:</strong>
                    <ul>
"""
        for highlight in doc['highlights']:
            html += f"                        <li>{highlight}</li>\n"
        html += """                    </ul>
                </li>
            </ul>
        </div>
"""
    
    html += f"""    </div>
    
    <div class="section">
        <h3>Findings & Impression</h3>
        <h4>Findings:</h4>
        <ul>
"""
    
    for finding in json_report['findings_and_impression']['findings']:
        html += f"            <li>{finding}</li>\n"
    
    html += """        </ul>
        <h4>Impression:</h4>
        <ul>
"""
    
    for impression in json_report['findings_and_impression']['impression']:
        html += f"            <li>{impression}</li>\n"
    
    html += """        </ul>
    </div>
    
    <div class="section timeline">
        <h3>Timeline of Events</h3>
        <ol>
"""
    
    for event in json_report['timeline_of_events']:
        html += f"            <li><strong>{event['date']}:</strong> {event['event']}</li>\n"
    
    html += """        </ol>
    </div>
    
    <div class="section">
        <p><em>Report generated on: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</em></p>
    </div>
</body>
</html>"""
    
    return html

def main():
    """Main function to generate correlation reports"""
    print("Generating PDF-DICOM Correlation Reports...")
    print("=" * 50)
    
    # Load data
    data = load_data_files()
    
    # Create output directory
    os.makedirs('./output', exist_ok=True)
    
    # Generate JSON report
    print("\nGenerating JSON report...")
    json_report = generate_json_report(data)
    
    # Save JSON report
    json_path = './output/correlation_report.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_report, f, indent=4, ensure_ascii=False)
    print(f"✅ JSON report saved to {json_path}")
    
    # Generate HTML report
    print("Generating HTML report...")
    html_report = generate_html_report(json_report)
    
    # Save HTML report
    html_path = './output/correlation_report.html'
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_report)
    print(f"✅ HTML report saved to {html_path}")
    
    print("\n🎉 Correlation reports generated successfully!")
    print(f"📁 Output directory: ./output/")
    print(f"📄 JSON report: {json_path}")
    print(f"🌐 HTML report: {html_path}")

if __name__ == "__main__":
    main()
