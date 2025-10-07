# test_models.py
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

def check_available_models():
    api_key = os.getenv('ABACUS_API_KEY')
    deployment_token = os.getenv('ABACUS_DEPLOYMENT_TOKEN')
    deployment_id = os.getenv('ABACUS_DEPLOYMENT_ID')
    
    print("🔍 Checking Abacus.AI API endpoints...")
    print(f"API Key: {'✅ Set' if api_key else '❌ Not set'}")
    print(f"Deployment Token: {'✅ Set' if deployment_token else '❌ Not set'}")
    print(f"Deployment ID: {'✅ Set' if deployment_id else '❌ Not set'}")
    print()
    
    if not api_key and not deployment_token:
        print("❌ Please set ABACUS_API_KEY or ABACUS_DEPLOYMENT_TOKEN environment variable")
        return
    
    # Try different API endpoints with various methods
    test_cases = [
        # Method 1: Try to list deployments with GET
        {
            "method": "GET",
            "url": "https://api.abacus.ai/api/v0/listDeployments",
            "headers": {"apiKey": api_key} if api_key else {},
            "description": "List deployments (GET)"
        },
        # Method 2: Try to list deployments with POST
        {
            "method": "POST", 
            "url": "https://api.abacus.ai/api/v0/listDeployments",
            "headers": {"Content-Type": "application/json", "apiKey": api_key} if api_key else {"Content-Type": "application/json"},
            "data": {"deploymentToken": deployment_token} if deployment_token else {},
            "description": "List deployments (POST)"
        },
        # Method 3: Try to get deployment info if we have deployment_id
        {
            "method": "POST",
            "url": "https://api.abacus.ai/api/v0/getDeployment",
            "headers": {"Content-Type": "application/json", "apiKey": api_key} if api_key else {"Content-Type": "application/json"},
            "data": {"deploymentId": deployment_id, "deploymentToken": deployment_token} if deployment_id else {},
            "description": "Get specific deployment info"
        },
        # Method 4: Try to list models
        {
            "method": "GET",
            "url": "https://api.abacus.ai/api/v0/listModels", 
            "headers": {"apiKey": api_key} if api_key else {},
            "description": "List models (GET)"
        },
        # Method 5: Try to list models with POST
        {
            "method": "POST",
            "url": "https://api.abacus.ai/api/v0/listModels",
            "headers": {"Content-Type": "application/json", "apiKey": api_key} if api_key else {"Content-Type": "application/json"},
            "data": {"deploymentToken": deployment_token} if deployment_token else {},
            "description": "List models (POST)"
        },
        # Method 6: Try to get organization info
        {
            "method": "GET",
            "url": "https://api.abacus.ai/api/v0/getOrganization",
            "headers": {"apiKey": api_key} if api_key else {},
            "description": "Get organization info"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}: {test_case['description']}")
        print(f"   URL: {test_case['url']}")
        
        try:
            if test_case["method"] == "GET":
                response = requests.get(test_case["url"], headers=test_case["headers"])
            else:
                response = requests.post(
                    test_case["url"], 
                    headers=test_case["headers"],
                    json=test_case.get("data", {})
                )
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print("   ✅ SUCCESS!")
                try:
                    result = response.json()
                    print(f"   Response keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
                    
                    # Pretty print relevant parts
                    if isinstance(result, dict):
                        if 'deployments' in result:
                            print(f"   Found {len(result['deployments'])} deployments")
                            for dep in result['deployments'][:3]:  # Show first 3
                                print(f"     - {dep.get('name', 'Unknown')} (ID: {dep.get('deploymentId', 'Unknown')})")
                        elif 'models' in result:
                            print(f"   Found {len(result['models'])} models")
                            for model in result['models'][:5]:  # Show first 5
                                print(f"     - {model.get('name', 'Unknown')} (ID: {model.get('modelId', 'Unknown')})")
                        elif 'deployment' in result:
                            dep = result['deployment']
                            print(f"   Deployment: {dep.get('name', 'Unknown')}")
                            print(f"   Model: {dep.get('modelName', 'Unknown')}")
                        else:
                            print(f"   Response preview: {str(result)[:200]}...")
                    
                except json.JSONDecodeError:
                    print(f"   Response (not JSON): {response.text[:200]}...")
                    
            elif response.status_code == 400:
                print("   ❌ Bad Request (400)")
                try:
                    error = response.json()
                    print(f"   Error: {error.get('message', 'Unknown error')}")
                except:
                    print(f"   Error text: {response.text[:200]}...")
            elif response.status_code == 401:
                print("   ❌ Unauthorized (401) - Check your API key/token")
            elif response.status_code == 403:
                print("   ❌ Forbidden (403) - Insufficient permissions")
            elif response.status_code == 404:
                print("   ❌ Not Found (404) - Endpoint doesn't exist")
            else:
                print(f"   ❌ Error {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")

def test_chat_endpoint():
    """Test if we can at least make a chat request to see what models are available"""
    print("\n" + "="*50)
    print("🧪 Testing Chat Endpoint (to infer model info)")
    print("="*50)
    
    deployment_token = os.getenv('ABACUS_DEPLOYMENT_TOKEN')
    deployment_id = os.getenv('ABACUS_DEPLOYMENT_ID')
    api_key = os.getenv('ABACUS_API_KEY')
    
    if not deployment_id:
        print("❌ No ABACUS_DEPLOYMENT_ID set - skipping chat test")
        return
    
    url = "https://api.abacus.ai/api/v0/getChatResponse"
    headers = {"Content-Type": "application/json"}
    
    if api_key:
        headers["apiKey"] = api_key
    
    payload = {
        "deploymentId": deployment_id,
        "messages": [{"is_user": True, "text": "What model are you?"}],
        "temperature": 0.1,
        "numCompletionTokens": 100
    }
    
    if deployment_token:
        payload["deploymentToken"] = deployment_token
    
    try:
        print(f"Making chat request to: {url}")
        response = requests.post(url, headers=headers, json=payload)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Chat request successful!")
            print(f"Response: {result}")
        else:
            print(f"❌ Chat request failed: {response.status_code}")
            print(f"Error: {response.text[:300]}...")
            
    except Exception as e:
        print(f"❌ Exception during chat test: {e}")

if __name__ == "__main__":
    check_available_models()
    test_chat_endpoint()
