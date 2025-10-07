"""
Medical Correlation Analysis Workflow

This module contains the specialized medical workflow functions for
PDF-DICOM correlation analysis using the legacy SendToLLM system.
"""

import json
from typing import Dict, Any, Optional, List, Union
from .file_operations import MedicalFileValidator, FileProcessor
from .abacus_client import get_client
from .response_processor import ResponseProcessor


class MedicalMessageBuilder:
    """Builds comprehensive messages for medical correlation analysis"""
    
    @staticmethod
    def build_comprehensive_message(prompt_text: str, 
                                  attachments_content: Dict[str, Any]) -> str:
        """
        Build a comprehensive message with prompt and file contents
        
        Args:
            prompt_text: The main prompt instructions
            attachments_content: Dictionary of loaded file contents
            
        Returns:
            Complete message string
        """
        message_parts = [
            "# Medical PDF-DICOM Correlation Analysis",
            "",
            "## Instructions:",
            prompt_text,
            "",
            "## Attached Files:",
            ""
        ]
        
        # Add each file's content to the message
        for key, content_info in attachments_content.items():
            if content_info:
                message_parts.append(f"### {content_info['filename']}")
                message_parts.append("")
                
                if content_info['type'] == 'json':
                    message_parts.append("```json")
                    message_parts.append(json.dumps(content_info['content'], indent=2))
                    message_parts.append("```")
                elif content_info['type'] == 'markdown':
                    message_parts.append("```markdown")
                    message_parts.append(content_info['content'])
                    message_parts.append("```")
                
                message_parts.append("")
        
        # Add critical instructions and requirements
        message_parts.extend([
            "---",
            "",
            "CRITICAL: Split into TWO separate sections as specified in the prompt:",
            "",
            "SECTION 1 - KEYWORD SEARCH RESULTS (2 documents):",
            "1. Wave Imag (SUB 2023-09-29)_M_DL_2024-07-02_OCR.pdf",
            "2. K Trinh MD_Pain_Pac Spn Ortho (SUB 2024-01-08)_MB_DL_2024-07-02_OCR.pdf",
            "",
            "SECTION 2 - VECTOR SEARCH RESULTS (5 documents):",
            "3. Beach Imag (SUB 2023-10-06)_M_DL_2024-07-02_OCR.pdf",
            "4. Nguyen, N_Tsuruda.Chidi_2024-20-24.pdf",
            "5. Orng Cst Mem Med Ctr (SUB 2023-10-05)_M_DL_2024-07-02_OCR.pdf",
            "6. Healthpiont Med Grp (SUB 2023-10-18)_M_DL_2024-07-02_OCR.pdf",
            "7. Heights Surg Inst (SUB 2023-11-10)_M_DL_2024-07-02_OCR.pdf",
            "",
            "Requirements:",
            "- Create separate 'Keyword_Search_Results' and 'Vector_Search_Results' sections",
            "- Follow the prompt structure exactly with two distinct sections",
            "- Include ALL documents with paths, pages, and highlights",
            "- Include source references with document names and page numbers",
            "- Include Findings & Impression, Procedures and Billing, Timeline sections",
            "",
            "Output format:",
            "JSON_REPORT_START",
            "{json with separate keyword and vector search sections}",
            "JSON_REPORT_END"
        ])
        
        return "\n".join(message_parts)
    
    @staticmethod
    def build_legacy_message(prompt_text: str, 
                           attachments_data: Dict[str, Any]) -> str:
        """
        Build a legacy-style message with embedded data
        
        Args:
            prompt_text: The main prompt instructions
            attachments_data: Dictionary of loaded attachment data
            
        Returns:
            Complete message string
        """
        message_parts = [
            prompt_text,
            "",
            "ATTACHED DATA:",
            "",
            "1. KEYWORD SEARCH RESULTS:",
            json.dumps(attachments_data.get('keyword_search'), indent=2) 
            if attachments_data.get('keyword_search') else 'No keyword search data available',
            "",
            "2. VECTOR SEARCH RESULTS:",
            json.dumps(attachments_data.get('vector_search'), indent=2) 
            if attachments_data.get('vector_search') else 'No vector search data available',
            "",
            "3. CORRELATION REPORT TEMPLATE:",
            attachments_data.get('correlation_report', 'No correlation report template available'),
            "",
            "Please generate the correlation reports as specified in the prompt instructions."
        ]
        
        return "\n".join(message_parts)


class MedicalWorkflow:
    """Main medical correlation analysis workflow"""
    
    DEFAULT_ATTACHMENTS_DIR = "./data/to_llm/attachments"
    DEFAULT_PROMPT_FILE = "./data/to_llm/prompt/prompt_v8.txt"
    
    def __init__(self):
        self.client = get_client()
        self.processor = ResponseProcessor()
        self.message_builder = MedicalMessageBuilder()
    
    def send_medical_correlation_data_with_attachments(self,
                                                     attachments_dir: str = DEFAULT_ATTACHMENTS_DIR,
                                                     prompt_file: str = DEFAULT_PROMPT_FILE,
                                                     deployment_token: Optional[str] = None,
                                                     deployment_id: Optional[str] = None,
                                                     api_key: Optional[str] = None) -> Dict[str, Any]:
        """
        Send medical correlation data with file contents embedded in the chat message
        (Updated approach - embeds file contents instead of uploading as attachments)
        
        Args:
            attachments_dir: Path to the attachments directory
            prompt_file: Path to the prompt file
            deployment_token: Abacus.AI deployment token for authentication
            deployment_id: The unique identifier of the deployment
            api_key: Abacus.AI API key (alternative to deployment_token)
            
        Returns:
            API response dictionary
        """
        # Validate attachments directory and files
        print(f"Validating attachments directory: {attachments_dir}")
        file_status = MedicalFileValidator.validate_attachments_directory(attachments_dir)
        MedicalFileValidator.print_file_status(file_status)
        
        # Read the prompt from file
        try:
            prompt_text = FileProcessor.read_text_file(prompt_file)
            print(f"✅ Prompt file loaded: {prompt_file}")
        except FileNotFoundError:
            raise FileNotFoundError(f"Prompt file not found: {prompt_file}")
        
        # Load attachment file contents
        print("\nLoading attachment file contents...")
        attachments_content = MedicalFileValidator.load_medical_files(attachments_dir)
        
        # Create comprehensive message
        final_message = self.message_builder.build_comprehensive_message(
            prompt_text, attachments_content
        )
        
        print(f"📝 Created comprehensive message ({len(final_message):,} characters)")
        print("💬 Sending message to LLM...")
        
        # Prepare chat message
        messages = [{
            "is_user": True,
            "text": final_message
        }]
        
        # Send to API
        return self.client.send_chat_request(
            messages=messages,
            deployment_token=deployment_token,
            deployment_id=deployment_id,
            api_key=api_key,
            temperature=0.7,
            max_tokens=4000
        )
    
    def send_medical_correlation_data_to_llm(self,
                                           attachments_dir: str = DEFAULT_ATTACHMENTS_DIR,
                                           prompt_file: str = DEFAULT_PROMPT_FILE,
                                           deployment_token: Optional[str] = None,
                                           deployment_id: Optional[str] = None,
                                           api_key: Optional[str] = None) -> Dict[str, Any]:
        """
        Send medical correlation data (keyword search, vector search, and correlation report) to LLM
        (Legacy function - embeds data in message text)
        
        Args:
            attachments_dir: Path to the attachments directory
            prompt_file: Path to the prompt file
            deployment_token: Abacus.AI deployment token for authentication
            deployment_id: The unique identifier of the deployment
            api_key: Abacus.AI API key (alternative to deployment_token)
            
        Returns:
            API response dictionary
        """
        # Validate and load files
        print(f"Validating attachments directory: {attachments_dir}")
        file_status = MedicalFileValidator.validate_attachments_directory(attachments_dir)
        MedicalFileValidator.print_file_status(file_status)
        
        # Read the prompt from file
        try:
            base_prompt = FileProcessor.read_text_file(prompt_file)
            print(f"✅ Prompt file loaded: {prompt_file}")
        except FileNotFoundError:
            raise FileNotFoundError(f"Prompt file not found: {prompt_file}")
        
        # Read all attachment files
        attachments_data: Dict[str, Union[Dict[str, Any], str, None]] = {}
        for key, status in file_status.items():
            if status['exists']:
                try:
                    if status['filename'].endswith('.json'):
                        attachments_data[key] = FileProcessor.read_json_file(status['path'])
                    elif status['filename'].endswith('.md'):
                        attachments_data[key] = FileProcessor.read_text_file(status['path'])
                    print(f"✅ Loaded {status['filename']}")
                except Exception as e:
                    print(f"❌ Error loading {status['filename']}: {e}")
                    attachments_data[key] = None
            else:
                print(f"⚠️  Skipping missing file: {status['filename']}")
                attachments_data[key] = None
        
        # Build legacy message
        final_prompt = self.message_builder.build_legacy_message(base_prompt, attachments_data)
        
        # Combine all data for the API call
        combined_data = {
            "prompt_instructions": base_prompt,
            "attachments": attachments_data
        }
        
        # Prepare chat message
        messages = [{
            "is_user": True,
            "text": f"{final_prompt}\n\nJSON Data:\n{json.dumps(combined_data, indent=2)}"
        }]
        
        # Send to API
        return self.client.send_chat_request(
            messages=messages,
            deployment_token=deployment_token,
            deployment_id=deployment_id,
            api_key=api_key,
            temperature=0.7,
            max_tokens=4000
        )
