# test_models.py
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def check_available_models():
    api_key = os.getenv('ABACUS_API_KEY')
    
    if not api_key:
        print("Please set ABACUS_API_KEY environment variable")
        return
    
    # Try different API endpoints
    endpoints = [
        "https://api.abacus.ai/api/v0/listModels",
        "https://api.abacus.ai/api/v0/listDeployments",
        "https://api.abacus.ai/api/v0/listAvailableModels"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(endpoint, headers={"apiKey": api_key})
            if response.status_code == 200:
                print(f"\n✅ {endpoint}:")
                print(response.json())
            else:
                print(f"❌ {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint}: {e}")

if __name__ == "__main__":
    check_available_models()