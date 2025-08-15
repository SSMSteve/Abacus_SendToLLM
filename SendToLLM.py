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
        "temperature": 0.7,
        "numCompletionTokens": 4000
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

# Example usage
if __name__ == "__main__":
    # Example 1: Send JSON file with prompt from file
    try:
        # Read the prompt from file
        with open('./data/prompt_v14.txt', 'r', encoding='utf-8') as prompt_file:
            base_prompt = prompt_file.read()

        # Modify the prompt to request JSON output only
        modified_prompt = f"{base_prompt}\n\nIMPORTANT: Please provide your response as a valid JSON object only. Do not include any explanatory text, code blocks, or other formatting. Output only the JSON data that would be saved to a report file."

        response = send_json_to_gpt5(
            json_file_path="./data/24-12-00016_aggregated_data_for_LLM.json",
            prompt=modified_prompt,
            deployment_token=os.getenv('ABACUS_DEPLOYMENT_TOKEN'),  # Or set ABACUS_DEPLOYMENT_TOKEN environment variable
            deployment_id=os.getenv('ABACUS_DEPLOYMENT_ID')  # Or set ABACUS_DEPLOYMENT_ID environment variable
        )

        # Extract the response content from Abacus.AI response format
        if 'result' in response and 'messages' in response['result']:
            messages = response['result']['messages']
            if messages and len(messages) > 0:
                # Get the last message (AI response)
                ai_response = messages[-1].get('text', '')
                print("AI Response received, saving to file...")

                # Create output directory if it doesn't exist
                import os
                os.makedirs('./output', exist_ok=True)

                # Try to parse and save as JSON
                try:
                    # Clean the response (remove any markdown formatting if present)
                    cleaned_response = ai_response.strip()
                    if cleaned_response.startswith('```json'):
                        cleaned_response = cleaned_response.replace('```json', '').replace('```', '').strip()
                    elif cleaned_response.startswith('```'):
                        cleaned_response = cleaned_response.replace('```', '').strip()

                    # Parse as JSON to validate
                    json_data = json.loads(cleaned_response)

                    # Save to file
                    with open('./output/report.json', 'w', encoding='utf-8') as output_file:
                        json.dump(json_data, output_file, indent=4, ensure_ascii=False)

                    print("✅ JSON report saved to ./output/report.json")
                    print(f"Preview: {json.dumps(json_data, indent=2)[:500]}...")

                except json.JSONDecodeError as e:
                    print(f"❌ Failed to parse AI response as JSON: {e}")
                    print("Raw response:")
                    print(ai_response[:1000] + "..." if len(ai_response) > 1000 else ai_response)

                    # Save raw response for debugging
                    with open('./output/raw_response.txt', 'w', encoding='utf-8') as debug_file:
                        debug_file.write(ai_response)
                    print("Raw response saved to ./output/raw_response.txt for debugging")

            else:
                print("No messages in response")
        else:
            print("Unexpected response format:", response)

    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except Exception as e:
        print(f"Error: {e}")

    # Example 2: Send JSON content directly
    sample_data = {
        "users": [
            {"id": 1, "name": "Alice", "age": 30},
            {"id": 2, "name": "Bob", "age": 25}
        ],
        "metadata": {
            "total_users": 2,
            "created_at": "2024-01-01"
        }
    }

    try:
        response = send_json_content_to_gpt5(
            json_content=sample_data,
            prompt="Summarize this user data and suggest improvements to the data structure."
        )

        # Extract the response content from Abacus.AI response format
        if 'result' in response and 'messages' in response['result']:
            messages = response['result']['messages']
            if messages and len(messages) > 0:
                # Get the last message (AI response)
                ai_response = messages[-1].get('text', '')
                print("\nAI Response for sample data:")
                print(ai_response)
            else:
                print("No messages in response")
        else:
            print("Unexpected response format:", response)

    except Exception as e:
        print(f"Error: {e}")