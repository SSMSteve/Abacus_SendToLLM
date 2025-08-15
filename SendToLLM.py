import requests
import json
import os

def send_json_to_gpt5(json_file_path, prompt, api_key=None):
    """
    Send a JSON file along with a prompt to GPT-5 using Abacus.AI API
    
    Args:
        json_file_path (str): Path to the JSON file
        prompt (str): The prompt to send along with the JSON
        api_key (str): Abacus.AI API key (if None, will try to get from environment)
    
    Returns:
        dict: Response from the API
    """
    
    # Get API key from environment if not provided
    if api_key is None:
        api_key = os.getenv('ABACUS_API_KEY')
        if not api_key:
            raise ValueError("API key not provided. Set ABACUS_API_KEY environment variable or pass api_key parameter")
    
    # Read the JSON file
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"JSON file not found: {json_file_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON file: {e}")
    
    # Abacus.AI API endpoint for chat completion
    url = "https://api.abacus.ai/api/v0/chatCompletion"
    
    # Prepare the headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Prepare the payload
    payload = {
        "model": "gpt-5",  # Specify GPT-5 model
        "messages": [
            {
                "role": "user",
                "content": f"{prompt}\n\nJSON Data:\n{json.dumps(json_data, indent=2)}"
            }
        ],
        "temperature": 0.7,
        "max_tokens": 4000
    }
    
    try:
        # Send the request
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {e}")

def send_json_content_to_gpt5(json_content, prompt, api_key=None):
    """
    Send JSON content (as dict/object) along with a prompt to GPT-5
    
    Args:
        json_content (dict): JSON content as Python dict
        prompt (str): The prompt to send along with the JSON
        api_key (str): Abacus.AI API key
    
    Returns:
        dict: Response from the API
    """
    
    if api_key is None:
        api_key = os.getenv('ABACUS_API_KEY')
        if not api_key:
            raise ValueError("API key not provided")
    
    url = "https://api.abacus.ai/api/v0/chatCompletion"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-5",
        "messages": [
            {
                "role": "user",
                "content": f"{prompt}\n\nJSON Data:\n{json.dumps(json_content, indent=2)}"
            }
        ],
        "temperature": 0.7,
        "max_tokens": 4000
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {e}")

# Example usage
if __name__ == "__main__":
    # Example 1: Send JSON file
    try:
        response = send_json_to_gpt5(
            json_file_path="data.json",
            prompt="Analyze this JSON data and provide insights about the structure and content.",
            api_key="your-abacus-api-key-here"  # Or set ABACUS_API_KEY environment variable
        )
        
        # Extract the response content
        if 'choices' in response and len(response['choices']) > 0:
            gpt5_response = response['choices'][0]['message']['content']
            print("GPT-5 Response:")
            print(gpt5_response)
        else:
            print("Unexpected response format:", response)
            
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
        
        if 'choices' in response and len(response['choices']) > 0:
            gpt5_response = response['choices'][0]['message']['content']
            print("\nGPT-5 Response for sample data:")
            print(gpt5_response)
            
    except Exception as e:
        print(f"Error: {e}")