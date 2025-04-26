import requests

test_data = {
    "meal_plan": "Standard",
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

response = requests.post('http://127.0.0.1:8000/pricing/', json=test_data)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")

# Now get all pricing records
get_response = requests.get('http://127.0.0.1:8000/pricing/')
print("\nAll pricing records:")
print(get_response.json()) 