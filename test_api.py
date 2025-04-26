import requests
import json
from typing import Dict, Any

BASE_URL = "http://127.0.0.1:8000"

def print_response(description: str, response: requests.Response):
    print("\n" + "="*50)
    print(f"Test: {description}")
    print(f"Status Code: {response.status_code}")
    print("Response:")
    print(json.dumps(response.json(), indent=2))
    print("="*50)

def test_root_endpoint():
    """Test the root endpoint"""
    response = requests.get(f"{BASE_URL}/")
    print_response("GET Root Endpoint", response)

def test_create_pricing_plans():
    """Test creating different pricing plans"""
    
    # Test Case 1: Standard Veg Plan
    standard_veg = {
        "meal_plan": "Standard Veg",
        "price": 499.99,
        "food_type": "Veg",
        "people_count": 2,
        "frequency": "Daily",
        "meal_details": "Breakfast and Dinner",
        "utensil_washing_price": 99.99,
        "utensil_washing_commission": 10.0,
        "children_special_price": 149.99,
        "preference_community_percentage": 5.0,
        "kitchen_platform_price": 199.99
    }
    
    # Test Case 2: Premium Non-Veg Plan
    premium_nonveg = {
        "meal_plan": "Premium Non-Veg",
        "price": 699.99,
        "food_type": "Non-Veg",
        "people_count": 4,
        "frequency": "Weekly",
        "meal_details": "Lunch and Dinner with Special Menu",
        "utensil_washing_price": 149.99,
        "utensil_washing_commission": 15.0,
        "children_special_price": 199.99,
        "preference_community_percentage": 7.5,
        "kitchen_platform_price": 299.99
    }
    
    # Test Case 3: Basic Plan (with minimal services)
    basic_plan = {
        "meal_plan": "Basic",
        "price": 299.99,
        "food_type": "Veg",
        "people_count": 1,
        "frequency": "Monthly",
        "meal_details": "Dinner Only",
        "utensil_washing_price": None,
        "utensil_washing_commission": None,
        "children_special_price": None,
        "preference_community_percentage": None,
        "kitchen_platform_price": None
    }

    # Create all plans
    for plan in [standard_veg, premium_nonveg, basic_plan]:
        response = requests.post(f"{BASE_URL}/pricing/", json=plan)
        print_response(f"POST Create {plan['meal_plan']} Plan", response)

def test_get_all_pricing():
    """Test retrieving all pricing plans"""
    response = requests.get(f"{BASE_URL}/pricing/")
    print_response("GET All Pricing Plans", response)

def test_pagination():
    """Test pagination functionality"""
    # Test with different skip and limit values
    params = [
        {"skip": 0, "limit": 2},
        {"skip": 2, "limit": 2}
    ]
    
    for param in params:
        response = requests.get(f"{BASE_URL}/pricing/", params=param)
        print_response(f"GET Pricing Plans with pagination (skip={param['skip']}, limit={param['limit']})", response)

def test_get_pricing_by_id():
    """Test getting a specific pricing plan by ID"""
    # First get all plans to get an ID
    response = requests.get(f"{BASE_URL}/pricing/")
    plans = response.json()
    if plans:
        pricing_id = plans[0]['id']
        response = requests.get(f"{BASE_URL}/pricing/{pricing_id}")
        print_response(f"GET Pricing Plan by ID {pricing_id}", response)
        
        # Test non-existent ID
        response = requests.get(f"{BASE_URL}/pricing/99999")
        print_response("GET Non-existent Pricing Plan", response)

def test_update_pricing():
    """Test updating a pricing plan"""
    # First get all plans to get an ID
    response = requests.get(f"{BASE_URL}/pricing/")
    plans = response.json()
    if plans:
        pricing_id = plans[0]['id']
        
        # Update plan
        update_data = {
            "price": 599.99,
            "meal_details": "Updated meal details",
            "utensil_washing_price": 129.99
        }
        response = requests.put(f"{BASE_URL}/pricing/{pricing_id}", json=update_data)
        print_response(f"PUT Update Pricing Plan {pricing_id}", response)
        
        # Test non-existent ID
        response = requests.put(f"{BASE_URL}/pricing/99999", json=update_data)
        print_response("PUT Update Non-existent Pricing Plan", response)

def test_delete_pricing():
    """Test deleting a pricing plan"""
    # First get all plans to get an ID
    response = requests.get(f"{BASE_URL}/pricing/")
    plans = response.json()
    if plans:
        pricing_id = plans[0]['id']
        
        # Delete plan
        response = requests.delete(f"{BASE_URL}/pricing/{pricing_id}")
        print_response(f"DELETE Pricing Plan {pricing_id}", response)
        
        # Test non-existent ID
        response = requests.delete(f"{BASE_URL}/pricing/99999")
        print_response("DELETE Non-existent Pricing Plan", response)

def run_all_tests():
    """Run all API tests"""
    print("\nStarting API Tests...")
    
    # Test root endpoint
    test_root_endpoint()
    
    # Test creating pricing plans
    test_create_pricing_plans()
    
    # Test getting all pricing plans
    test_get_all_pricing()
    
    # Test pagination
    test_pagination()
    
    # Test getting specific pricing plan
    test_get_pricing_by_id()
    
    # Test updating pricing plan
    test_update_pricing()
    
    # Test deleting pricing plan
    test_delete_pricing()
    
    print("\nAPI Tests Completed!")

if __name__ == "__main__":
    run_all_tests() 