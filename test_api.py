import requests
import json

def test_api():
    base_url = "http://127.0.0.1:8000"
    
    # Test root endpoint
    print("\nTesting root endpoint...")
    response = requests.get(f"{base_url}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test get pricing plans
    print("\nTesting get pricing plans...")
    response = requests.get(f"{base_url}/pricing/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test add pricing plan
    print("\nTesting add pricing plan...")
    new_plan = {
        "meal_plan": "Test Plan",
        "price": 999.99,
        "additional_services": "Test Services"
    }
    response = requests.post(f"{base_url}/pricing/", json=new_plan)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    test_api() 