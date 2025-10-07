import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def send_json_to_gpt5(json_file_path, prompt, deployment_token=None, deployment_id=None, api_key=None):
    """
    Send a JSON file along with a prompt to a deployed LLM using Abacus.AI API

    Args:
        json_file_path (str): Path to the JSON file
        prompt (str): The prompt to send along with the JSON
        deployment_token (str): Abacus.AI deployment token for authentication
        deployment_id (str): The unique identifier of the deployment
        api_key (str): Abacus.AI API key (alternative to deployment_token)

    Returns:
        dict: Response from the API
    """

    # Get credentials from environment if not provided
    if deployment_token is None:
        deployment_token = os.getenv('ABACUS_DEPLOYMENT_TOKEN')
    if deployment_id is None:
        deployment_id = os.getenv('ABACUS_DEPLOYMENT_ID')
    if api_key is None:
        api_key = os.getenv('ABACUS_API_KEY')

    if not deployment_token and not api_key:
        raise ValueError("Either deployment_token or api_key must be provided. Set ABACUS_DEPLOYMENT_TOKEN or ABACUS_API_KEY environment variable")
    if not deployment_id:
        raise ValueError("deployment_id is required. Set ABACUS_DEPLOYMENT_ID environment variable or pass deployment_id parameter")

    # Read the JSON file
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"JSON file not found: {json_file_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON file: {e}")

    # Abacus.AI API endpoint for chat response
    url = "https://api.abacus.ai/api/v0/getChatResponse"

    # Prepare the headers
    headers = {
        "Content-Type": "application/json"
    }
    if api_key:
        headers["apiKey"] = api_key

    # Prepare the payload for getChatResponse
    payload = {
        "deploymentId": deployment_id,
        "messages": [
            {
                "is_user": True,
                "text": f"{prompt}\n\nJSON Data:\n{json.dumps(json_data, indent=2)}"
            }
        ],
        "temperature": 0.1,
        "numCompletionTokens": 8000
    }

    if deployment_token:
        payload["deploymentToken"] = deployment_token

    try:
        # Send the request
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes

        return response.json()

    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {e}")

def send_json_content_to_gpt5(json_content, prompt, deployment_token=None, deployment_id=None, api_key=None):
    """
    Send JSON content (as dict/object) along with a prompt to a deployed LLM using Abacus.AI API

    Args:
        json_content (dict): JSON content as Python dict
        prompt (str): The prompt to send along with the JSON
        deployment_token (str): Abacus.AI deployment token for authentication
        deployment_id (str): The unique identifier of the deployment
        api_key (str): Abacus.AI API key (alternative to deployment_token)

    Returns:
        dict: Response from the API
    """

    # Get credentials from environment if not provided
    if deployment_token is None:
        deployment_token = os.getenv('ABACUS_DEPLOYMENT_TOKEN')
    if deployment_id is None:
        deployment_id = os.getenv('ABACUS_DEPLOYMENT_ID')
    if api_key is None:
        api_key = os.getenv('ABACUS_API_KEY')

    if not deployment_token and not api_key:
        raise ValueError("Either deployment_token or api_key must be provided")
    if not deployment_id:
        raise ValueError("deployment_id is required")

    url = "https://api.abacus.ai/api/v0/getChatResponse"

    headers = {
        "Content-Type": "application/json"
    }
    if api_key:
        headers["apiKey"] = api_key

    payload = {
        "deploymentId": deployment_id,
        "messages": [
            {
                "is_user": True,
                "text": f"{prompt}\n\nJSON Data:\n{json.dumps(json_content, indent=2)}"
            }
        ],
        "temperature": 0.7,
        "numCompletionTokens": 4000
    }

    if deployment_token:
        payload["deploymentToken"] = deployment_token

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {e}")

def send_json_to_llm_completion(json_file_path, prompt, deployment_token=None, deployment_id=None, api_key=None):
    """
    Send a JSON file along with a prompt to a fine-tuned LLM using Abacus.AI getCompletion API

    Args:
        json_file_path (str): Path to the JSON file
        prompt (str): The prompt to send along with the JSON
        deployment_token (str): Abacus.AI deployment token for authentication
        deployment_id (str): The unique identifier of the deployment
        api_key (str): Abacus.AI API key (alternative to deployment_token)

    Returns:
        dict: Response from the API
    """

    # Get credentials from environment if not provided
    if deployment_token is None:
        deployment_token = os.getenv('ABACUS_DEPLOYMENT_TOKEN')
    if deployment_id is None:
        deployment_id = os.getenv('ABACUS_DEPLOYMENT_ID')
    if api_key is None:
        api_key = os.getenv('ABACUS_API_KEY')

    if not deployment_token and not api_key:
        raise ValueError("Either deployment_token or api_key must be provided")
    if not deployment_id:
        raise ValueError("deployment_id is required")

    # Read the JSON file
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"JSON file not found: {json_file_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON file: {e}")

    # Abacus.AI API endpoint for completion
    url = "https://api.abacus.ai/api/v0/getCompletion"

    # Prepare the headers
    headers = {
        "Content-Type": "application/json"
    }
    if api_key:
        headers["apiKey"] = api_key

    # Prepare the payload for getCompletion
    payload = {
        "deploymentId": deployment_id,
        "prompt": f"{prompt}\n\nJSON Data:\n{json.dumps(json_data, indent=2)}"
    }

    if deployment_token:
        payload["deploymentToken"] = deployment_token

    try:
        # Send the request
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes

        return response.json()

    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {e}")

def upload_file_to_abacus(file_path, deployment_id=None, api_key=None, deployment_token=None):
    """
    Upload a file to Abacus.AI for use in chat

    Args:
        file_path (str): Path to the file to upload
        deployment_id (str): The unique identifier of the deployment
        api_key (str): Abacus.AI API key
        deployment_token (str): Abacus.AI deployment token

    Returns:
        str: File ID for use in chat messages
    """
    # Get credentials from environment if not provided
    if deployment_token is None:
        deployment_token = os.getenv('ABACUS_DEPLOYMENT_TOKEN')
    if deployment_id is None:
        deployment_id = os.getenv('ABACUS_DEPLOYMENT_ID')
    if api_key is None:
        api_key = os.getenv('ABACUS_API_KEY')

    if not deployment_token and not api_key:
        raise ValueError("Either deployment_token or api_key must be provided")
    if not deployment_id:
        raise ValueError("deployment_id is required")

    # Abacus.AI API endpoint for file upload
    url = "https://api.abacus.ai/api/v0/uploadFile"

    # Prepare headers
    headers = {}
    if api_key:
        headers["apiKey"] = api_key

    # Prepare the file for upload
    try:
        with open(file_path, 'rb') as file:
            files = {
                'file': (os.path.basename(file_path), file, 'application/octet-stream')
            }

            data = {
                'deploymentId': deployment_id
            }

            if deployment_token:
                data['deploymentToken'] = deployment_token

            response = requests.post(url, headers=headers, files=files, data=data)
            response.raise_for_status()

            result = response.json()
            if 'result' in result and 'fileId' in result['result']:
                return result['result']['fileId']
            else:
                raise Exception(f"Unexpected upload response format: {result}")

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"File upload failed: {e}")

def send_chat_with_attachments(prompt, file_ids=None, deployment_token=None, deployment_id=None, api_key=None):
    """
    Send a chat message with file attachments to Abacus.AI

    Args:
        prompt (str): The prompt/message to send
        file_ids (list): List of file IDs from uploaded files
        deployment_token (str): Abacus.AI deployment token
        deployment_id (str): The unique identifier of the deployment
        api_key (str): Abacus.AI API key

    Returns:
        dict: Response from the API
    """
    # Get credentials from environment if not provided
    if deployment_token is None:
        deployment_token = os.getenv('ABACUS_DEPLOYMENT_TOKEN')
    if deployment_id is None:
        deployment_id = os.getenv('ABACUS_DEPLOYMENT_ID')
    if api_key is None:
        api_key = os.getenv('ABACUS_API_KEY')

    if not deployment_token and not api_key:
        raise ValueError("Either deployment_token or api_key must be provided")
    if not deployment_id:
        raise ValueError("deployment_id is required")

    url = "https://api.abacus.ai/api/v0/getChatResponse"

    headers = {
        "Content-Type": "application/json"
    }
    if api_key:
        headers["apiKey"] = api_key

    # Prepare message with attachments
    message = {
        "is_user": True,
        "text": prompt
    }

    # Add file attachments if provided
    if file_ids:
        message["attachments"] = [{"fileId": file_id} for file_id in file_ids]

    payload = {
        "deploymentId": deployment_id,
        "messages": [message],
        "temperature": 0.7,
        "numCompletionTokens": 4000
    }

    if deployment_token:
        payload["deploymentToken"] = deployment_token

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {e}")

def validate_attachments_directory(attachments_dir):
    """
    Validate that the attachments directory exists and contains expected files

    Args:
        attachments_dir (str): Path to the attachments directory

    Returns:
        dict: Dictionary with file paths and their existence status
    """
    if not os.path.exists(attachments_dir):
        raise FileNotFoundError(f"Attachments directory not found: {attachments_dir}")

    expected_files = {
        'keyword_search': 'keyword_search_results_27977577.json',
        'vector_search': 'vector_search_results_27977577.json',
        'correlation_report': 'Correlation_Report.md'
    }

    file_status = {}
    for key, filename in expected_files.items():
        file_path = os.path.join(attachments_dir, filename)
        file_status[key] = {
            'path': file_path,
            'exists': os.path.exists(file_path),
            'filename': filename
        }

    return file_status

def send_medical_correlation_data_with_attachments(attachments_dir="./data/to_llm/attachments", prompt_file="./data/to_llm/prompt/prompt_v8.txt", deployment_token=None, deployment_id=None, api_key=None):
    """
    Send medical correlation data with file contents embedded in the chat message
    (Updated approach - embeds file contents instead of uploading as attachments)

    Args:
        attachments_dir (str): Path to the attachments directory
        prompt_file (str): Path to the prompt file
        deployment_token (str): Abacus.AI deployment token for authentication
        deployment_id (str): The unique identifier of the deployment
        api_key (str): Abacus.AI API key (alternative to deployment_token)

    Returns:
        dict: Response from the API
    """

    # Validate attachments directory and files
    print(f"Validating attachments directory: {attachments_dir}")
    file_status = validate_attachments_directory(attachments_dir)

    # Print file status
    for _, status in file_status.items():
        status_icon = "✅" if status['exists'] else "❌"
        print(f"{status_icon} {status['filename']}: {'Found' if status['exists'] else 'Missing'}")

    # Read the prompt from file
    try:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            prompt_text = f.read()
        print(f"✅ Prompt file loaded: {prompt_file}")
    except FileNotFoundError:
        raise FileNotFoundError(f"Prompt file not found: {prompt_file}")

    # Read attachment file contents
    print("\nLoading attachment file contents...")
    attachments_content = {}

    for key, status in file_status.items():
        if status['exists']:
            try:
                print(f"� Loading {status['filename']}...")
                if status['filename'].endswith('.json'):
                    with open(status['path'], 'r', encoding='utf-8') as f:
                        attachments_content[key] = {
                            'filename': status['filename'],
                            'type': 'json',
                            'content': json.load(f)
                        }
                elif status['filename'].endswith('.md'):
                    with open(status['path'], 'r', encoding='utf-8') as f:
                        attachments_content[key] = {
                            'filename': status['filename'],
                            'type': 'markdown',
                            'content': f.read()
                        }
                print(f"✅ Loaded {status['filename']}")
            except Exception as e:
                print(f"❌ Failed to load {status['filename']}: {e}")
                attachments_content[key] = None
        else:
            print(f"⚠️  Skipping missing file: {status['filename']}")
            attachments_content[key] = None

    # Create comprehensive message with prompt and file contents
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

    message_parts.append("---")
    message_parts.append("")
    message_parts.append("CRITICAL: Split into TWO separate sections as specified in the prompt:")
    message_parts.append("")
    message_parts.append("SECTION 1 - KEYWORD SEARCH RESULTS (2 documents):")
    message_parts.append("1. Wave Imag (SUB 2023-09-29)_M_DL_2024-07-02_OCR.pdf")
    message_parts.append("2. K Trinh MD_Pain_Pac Spn Ortho (SUB 2024-01-08)_MB_DL_2024-07-02_OCR.pdf")
    message_parts.append("")
    message_parts.append("SECTION 2 - VECTOR SEARCH RESULTS (5 documents):")
    message_parts.append("3. Beach Imag (SUB 2023-10-06)_M_DL_2024-07-02_OCR.pdf")
    message_parts.append("4. Nguyen, N_Tsuruda.Chidi_2024-20-24.pdf")
    message_parts.append("5. Orng Cst Mem Med Ctr (SUB 2023-10-05)_M_DL_2024-07-02_OCR.pdf")
    message_parts.append("6. Healthpiont Med Grp (SUB 2023-10-18)_M_DL_2024-07-02_OCR.pdf")
    message_parts.append("7. Heights Surg Inst (SUB 2023-11-10)_M_DL_2024-07-02_OCR.pdf")
    message_parts.append("")
    message_parts.append("Requirements:")
    message_parts.append("- Create separate 'Keyword_Search_Results' and 'Vector_Search_Results' sections")
    message_parts.append("- Follow the prompt structure exactly with two distinct sections")
    message_parts.append("- Include ALL documents with paths, pages, and highlights")
    message_parts.append("- Include source references with document names and page numbers")
    message_parts.append("- Include Findings & Impression, Procedures and Billing, Timeline sections")
    message_parts.append("")
    message_parts.append("Output format:")
    message_parts.append("JSON_REPORT_START")
    message_parts.append("{json with separate keyword and vector search sections}")
    message_parts.append("JSON_REPORT_END")

    final_message = "\n".join(message_parts)

    print(f"� Created comprehensive message ({len(final_message):,} characters)")
    print("💬 Sending message to LLM...")

    # Send using the standard chat response API
    return send_json_content_to_gpt5(
        json_content={"message_type": "medical_correlation_analysis", "attachments_loaded": True},
        prompt=final_message,
        deployment_token=deployment_token,
        deployment_id=deployment_id,
        api_key=api_key
    )

def send_medical_correlation_data_to_llm(attachments_dir="./data/to_llm/attachments", prompt_file="./data/to_llm/prompt/prompt_v8.txt", deployment_token=None, deployment_id=None, api_key=None):
    """
    Send medical correlation data (keyword search, vector search, and correlation report) to LLM
    (Legacy function - embeds data in message text)

    Args:
        attachments_dir (str): Path to the attachments directory
        prompt_file (str): Path to the prompt file
        deployment_token (str): Abacus.AI deployment token for authentication
        deployment_id (str): The unique identifier of the deployment
        api_key (str): Abacus.AI API key (alternative to deployment_token)

    Returns:
        dict: Response from the API
    """

    # Validate attachments directory and files
    print(f"Validating attachments directory: {attachments_dir}")
    file_status = validate_attachments_directory(attachments_dir)

    # Print file status
    for key, status in file_status.items():
        status_icon = "✅" if status['exists'] else "❌"
        print(f"{status_icon} {status['filename']}: {'Found' if status['exists'] else 'Missing'}")

    # Read the prompt from file
    try:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            base_prompt = f.read()
        print(f"✅ Prompt file loaded: {prompt_file}")
    except FileNotFoundError:
        raise FileNotFoundError(f"Prompt file not found: {prompt_file}")

    # Read all attachment files
    attachments_data = {}

    for key, status in file_status.items():
        if status['exists']:
            try:
                if status['filename'].endswith('.json'):
                    with open(status['path'], 'r', encoding='utf-8') as f:
                        attachments_data[key] = json.load(f)
                elif status['filename'].endswith('.md'):
                    with open(status['path'], 'r', encoding='utf-8') as f:
                        attachments_data[key] = f.read()
                print(f"✅ Loaded {status['filename']}")
            except Exception as e:
                print(f"❌ Error loading {status['filename']}: {e}")
                attachments_data[key] = None
        else:
            print(f"⚠️  Skipping missing file: {status['filename']}")
            attachments_data[key] = None

    # Combine all data
    combined_data = {
        "prompt_instructions": base_prompt,
        "attachments": attachments_data
    }

    # Create the final prompt
    final_prompt = f"""
{base_prompt}

ATTACHED DATA:

1. KEYWORD SEARCH RESULTS:
{json.dumps(attachments_data.get('keyword_search'), indent=2) if attachments_data.get('keyword_search') else 'No keyword search data available'}

2. VECTOR SEARCH RESULTS:
{json.dumps(attachments_data.get('vector_search'), indent=2) if attachments_data.get('vector_search') else 'No vector search data available'}

3. CORRELATION REPORT TEMPLATE:
{attachments_data.get('correlation_report', 'No correlation report template available')}

Please generate the correlation reports as specified in the prompt instructions.
"""

    # Send to LLM using the existing function
    return send_json_content_to_gpt5(
        json_content=combined_data,
        prompt=final_prompt,
        deployment_token=deployment_token,
        deployment_id=deployment_id,
        api_key=api_key
    )

# Example usage
if __name__ == "__main__":
    # Example 1: Send medical correlation data with file attachments
    try:
        print("Sending medical correlation data to LLM with file attachments...")
        response = send_medical_correlation_data_with_attachments(
            attachments_dir="./data/to_llm/attachments",
            prompt_file="./data/to_llm/prompt/prompt_v8.txt",
            deployment_token=os.getenv('ABACUS_DEPLOYMENT_TOKEN'),
            deployment_id=os.getenv('ABACUS_DEPLOYMENT_ID')
        )

        # Extract the response content from Abacus.AI response format
        if 'result' in response and 'messages' in response['result']:
            messages = response['result']['messages']
            if messages and len(messages) > 0:
                # Get the last message (AI response)
                ai_response = messages[-1].get('text', '')
                print("AI Response received, processing and saving files...")

                # Create output directory if it doesn't exist
                os.makedirs('./output', exist_ok=True)

                # Save raw response for debugging
                with open('./output/raw_response.txt', 'w', encoding='utf-8') as debug_file:
                    debug_file.write(ai_response)
                print("Raw response saved to ./output/raw_response.txt")

                # Try to extract and save JSON report using markers
                try:
                    json_saved = False

                    # Look for JSON content using markers
                    json_start_marker = "JSON_REPORT_START"
                    json_end_marker = "JSON_REPORT_END"
                    json_start = ai_response.find(json_start_marker)
                    json_end = ai_response.find(json_end_marker)

                    if json_start != -1 and json_end != -1:
                        json_start += len(json_start_marker)
                        json_content = ai_response[json_start:json_end].strip()

                        try:
                            # Parse as JSON to validate
                            json_data = json.loads(json_content)

                            # Save JSON report
                            with open('./output/correlation_report.json', 'w', encoding='utf-8') as output_file:
                                json.dump(json_data, output_file, indent=4, ensure_ascii=False)
                            print("✅ JSON correlation report saved to ./output/correlation_report.json")
                            json_saved = True
                        except json.JSONDecodeError as e:
                            print(f"⚠️  JSON parsing failed: {e}")
                            print(f"JSON content preview: {json_content[:200]}...")

                    # Fallback: try to find JSON without markers
                    if not json_saved:
                        json_start = ai_response.find('{')
                        json_end = ai_response.rfind('}') + 1

                        if json_start != -1 and json_end > json_start:
                            json_content = ai_response[json_start:json_end]

                            try:
                                json_data = json.loads(json_content)
                                with open('./output/correlation_report.json', 'w', encoding='utf-8') as output_file:
                                    json.dump(json_data, output_file, indent=4, ensure_ascii=False)
                                print("✅ JSON correlation report saved (fallback method)")
                                json_saved = True
                            except json.JSONDecodeError as e:
                                print(f"⚠️  Fallback JSON parsing failed: {e}")
                                print(f"JSON content preview: {json_content[:200]}...")

                    if not json_saved:
                        print("❌ Could not extract valid JSON from response")

                    print(f"Response preview: {ai_response[:500]}...")

                except json.JSONDecodeError as e:
                    print(f"❌ Failed to parse JSON from AI response: {e}")
                    print("Attempting to save as text file...")

                    # Save as text file if JSON parsing fails
                    with open('./output/correlation_report.txt', 'w', encoding='utf-8') as output_file:
                        output_file.write(ai_response)
                    print("Response saved to ./output/correlation_report.txt")

                except Exception as e:
                    print(f"❌ Error processing response: {e}")
                    print("Response saved to raw_response.txt for manual review")

            else:
                print("No messages in response")
        else:
            print("Unexpected response format:", response)

    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except Exception as e:
        print(f"Error: {e}")

    print("\n" + "="*50)
    print("Medical Correlation Report Generation Complete!")
    print("="*50)