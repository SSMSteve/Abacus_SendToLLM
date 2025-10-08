"""
File Operations for Legacy SendToLLM System

This module handles file reading, validation, processing, and output
operations for the medical correlation analysis workflow.
"""

import json
import os
from typing import Dict, Any, Optional, List, Union


class FileProcessor:
    """Handles file operations for the legacy system"""
    
    @staticmethod
    def read_json_file(file_path: str) -> Dict[str, Any]:
        """
        Read and parse a JSON file
        
        Args:
            file_path: Path to the JSON file
            
        Returns:
            Parsed JSON data as dictionary
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If JSON is invalid
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"JSON file not found: {file_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON file: {e}")
    
    @staticmethod
    def read_text_file(file_path: str) -> str:
        """
        Read a text file
        
        Args:
            file_path: Path to the text file
            
        Returns:
            File contents as string
            
        Raises:
            FileNotFoundError: If file doesn't exist
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Text file not found: {file_path}")
    
    @staticmethod
    def write_json_file(file_path: str, data: Dict[str, Any]) -> None:
        """
        Write data to a JSON file
        
        Args:
            file_path: Path to write the JSON file
            data: Data to write
        """
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    
    @staticmethod
    def write_text_file(file_path: str, content: str) -> None:
        """
        Write content to a text file
        
        Args:
            file_path: Path to write the text file
            content: Content to write
        """
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)


class MedicalFileValidator:
    """Validates medical correlation analysis files"""

    @classmethod
    def validate_attachments_directory(cls, attachments_dir: str) -> Dict[str, Dict[str, Any]]:
        """
        Validate that the attachments directory exists and contains expected files
        Automatically detects files based on patterns instead of hard-coded names

        Args:
            attachments_dir: Path to the attachments directory

        Returns:
            Dictionary with file paths and their existence status

        Raises:
            FileNotFoundError: If attachments directory doesn't exist
        """
        if not os.path.exists(attachments_dir):
            raise FileNotFoundError(f"Attachments directory not found: {attachments_dir}")

        # Get all files in the directory
        all_files = os.listdir(attachments_dir)

        # Define patterns to match different file types
        file_patterns = {
            'keyword_search': ['keyword_search', '_keyword', 'keyword'],
            'vector_search': ['vector_search', '_vector', 'vector'],
            'correlation_report': ['correlation_report', 'Correlation_Report']
        }

        file_status = {}

        # Find files matching each pattern
        for key, patterns in file_patterns.items():
            found_file = None

            # Look for JSON files for search results, MD files for correlation report
            expected_extensions = ['.json'] if key != 'correlation_report' else ['.md', '.txt']

            for filename in all_files:
                # Check if filename matches any pattern and has correct extension
                if any(pattern.lower() in filename.lower() for pattern in patterns):
                    if any(filename.lower().endswith(ext) for ext in expected_extensions):
                        found_file = filename
                        break

            if found_file:
                file_path = os.path.join(attachments_dir, found_file)
                file_status[key] = {
                    'path': file_path,
                    'exists': True,
                    'filename': found_file
                }
            else:
                # Create a placeholder entry for missing files
                expected_name = f"{key}.json" if key != 'correlation_report' else "correlation_report.md"
                file_status[key] = {
                    'path': os.path.join(attachments_dir, expected_name),
                    'exists': False,
                    'filename': expected_name
                }

        return file_status
    
    @classmethod
    def load_medical_files(cls, attachments_dir: str) -> Dict[str, Union[Dict[str, Any], None]]:
        """
        Load all medical files from the attachments directory
        
        Args:
            attachments_dir: Path to the attachments directory
            
        Returns:
            Dictionary with loaded file contents
        """
        file_status = cls.validate_attachments_directory(attachments_dir)
        processor = FileProcessor()
        attachments_content: Dict[str, Union[Dict[str, Any], None]] = {}
        
        for key, status in file_status.items():
            if status['exists']:
                try:
                    print(f"📄 Loading {status['filename']}...")
                    if status['filename'].endswith('.json'):
                        json_content = processor.read_json_file(status['path'])
                        attachments_content[key] = {
                            'filename': status['filename'],
                            'type': 'json',
                            'content': json_content
                        }
                    elif status['filename'].endswith('.md'):
                        text_content = processor.read_text_file(status['path'])
                        attachments_content[key] = {
                            'filename': status['filename'],
                            'type': 'markdown',
                            'content': text_content
                        }
                    print(f"✅ Loaded {status['filename']}")
                except Exception as e:
                    print(f"❌ Failed to load {status['filename']}: {e}")
                    attachments_content[key] = None
            else:
                print(f"⚠️  Skipping missing file: {status['filename']}")
                attachments_content[key] = None
        
        return attachments_content
    
    @classmethod
    def print_file_status(cls, file_status: Dict[str, Dict[str, Any]]) -> None:
        """
        Print the status of medical files
        
        Args:
            file_status: File status dictionary from validate_attachments_directory
        """
        for _, status in file_status.items():
            status_icon = "✅" if status['exists'] else "❌"
            status_text = "Found" if status['exists'] else "Missing"
            print(f"{status_icon} {status['filename']}: {status_text}")


class OutputManager:
    """Manages output file operations"""
    
    DEFAULT_OUTPUT_DIR = "./output"
    
    def __init__(self, output_dir: str = DEFAULT_OUTPUT_DIR):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def save_raw_response(self, response: str) -> str:
        """
        Save raw API response to file
        
        Args:
            response: Raw response text
            
        Returns:
            Path to saved file
        """
        file_path = os.path.join(self.output_dir, 'raw_response.txt')
        FileProcessor.write_text_file(file_path, response)
        return file_path
    
    def save_json_report(self, data: Dict[str, Any]) -> str:
        """
        Save JSON report to file
        
        Args:
            data: JSON data to save
            
        Returns:
            Path to saved file
        """
        file_path = os.path.join(self.output_dir, 'correlation_report.json')
        FileProcessor.write_json_file(file_path, data)
        return file_path
    
    def save_text_report(self, content: str) -> str:
        """
        Save text report to file
        
        Args:
            content: Text content to save
            
        Returns:
            Path to saved file
        """
        file_path = os.path.join(self.output_dir, 'correlation_report.txt')
        FileProcessor.write_text_file(file_path, content)
        return file_path
