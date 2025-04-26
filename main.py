from fastapi import FastAPI, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from crud import create_pricing, get_pricing, get_pricing_by_id, update_pricing, delete_pricing
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PricingCreate(BaseModel):
    meal_plan: str
    price: float
    food_type: str
    people_count: int
    frequency: str
    meal_details: str
    utensil_washing_price: float | None
    utensil_washing_commission: float | None
    children_special_price: float | None
    preference_community_percentage: float | None
    kitchen_platform_price: float | None

class PricingUpdate(BaseModel):
    meal_plan: str | None = None
    price: float | None = None
    food_type: str | None = None
    people_count: int | None = None
    frequency: str | None = None
    meal_details: str | None = None
    utensil_washing_price: float | None = None
    utensil_washing_commission: float | None = None
    children_special_price: float | None = None
    preference_community_percentage: float | None = None
    kitchen_platform_price: float | None = None

app = FastAPI(
    title="Meal Delivery API",
    description="API for managing meal delivery pricing and services",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Meal Delivery API",
        "documentation": "Visit /docs for API documentation",
        "endpoints": {
            "GET /pricing/": "Get all pricing plans",
            "GET /pricing/{id}": "Get a specific pricing plan",
            "POST /pricing/": "Add a new pricing plan",
            "PUT /pricing/{id}": "Update a pricing plan",
            "DELETE /pricing/{id}": "Delete a pricing plan"
        }
    }

@app.post("/pricing/", summary="Add new pricing plan")
def add_pricing(pricing: PricingCreate, db: Session = Depends(get_db)):
    """
    Add a new pricing plan with the following information:
    - **meal_plan**: Name of the meal plan
    - **price**: Price of the meal plan
    - **food_type**: Type of food (Veg/Non-veg)
    - **people_count**: Number of people
    - **frequency**: Frequency of service
    - **meal_details**: Details of meals provided
    - **utensil_washing_price**: Price for utensil washing service (optional)
    - **utensil_washing_commission**: Commission for utensil washing (optional)
    - **children_special_price**: Price for children special service (optional)
    - **preference_community_percentage**: Percentage for preference community (optional)
    - **kitchen_platform_price**: Price for kitchen platform service (optional)
    """
    try:
        return create_pricing(
            db=db,
            meal_plan=pricing.meal_plan,
            price=pricing.price,
            food_type=pricing.food_type,
            people_count=pricing.people_count,
            frequency=pricing.frequency,
            meal_details=pricing.meal_details,
            utensil_washing_price=pricing.utensil_washing_price,
            utensil_washing_commission=pricing.utensil_washing_commission,
            children_special_price=pricing.children_special_price,
            preference_community_percentage=pricing.preference_community_percentage,
            kitchen_platform_price=pricing.kitchen_platform_price
        )
    except Exception as e:
        logger.error(f"Error creating pricing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/pricing/", summary="Get all pricing plans")
def read_pricing(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all pricing plans with pagination:
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100)
    """
    try:
        return get_pricing(db=db, skip=skip, limit=limit)
    except Exception as e:
        logger.error(f"Error getting pricing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/pricing/{pricing_id}", summary="Get a specific pricing plan")
def read_pricing_by_id(pricing_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific pricing plan by ID:
    - **pricing_id**: The ID of the pricing plan to retrieve
    """
    try:
        pricing = get_pricing_by_id(db, pricing_id)
        if pricing is None:
            raise HTTPException(status_code=404, detail="Pricing plan not found")
        return pricing
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting pricing by ID: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/pricing/{pricing_id}", summary="Update a pricing plan")
def update_pricing_plan(pricing_id: int, pricing: PricingUpdate, db: Session = Depends(get_db)):
    """
    Update a pricing plan with the following information:
    - **pricing_id**: The ID of the pricing plan to update
    - **meal_plan**: Name of the meal plan (optional)
    - **price**: Price of the meal plan (optional)
    - **food_type**: Type of food (Veg/Non-veg) (optional)
    - **people_count**: Number of people (optional)
    - **frequency**: Frequency of service (optional)
    - **meal_details**: Details of meals provided (optional)
    - **utensil_washing_price**: Price for utensil washing service (optional)
    - **utensil_washing_commission**: Commission for utensil washing (optional)
    - **children_special_price**: Price for children special service (optional)
    - **preference_community_percentage**: Percentage for preference community (optional)
    - **kitchen_platform_price**: Price for kitchen platform service (optional)
    """
    try:
        updated_pricing = update_pricing(
            db=db,
            pricing_id=pricing_id,
            meal_plan=pricing.meal_plan,
            price=pricing.price,
            food_type=pricing.food_type,
            people_count=pricing.people_count,
            frequency=pricing.frequency,
            meal_details=pricing.meal_details,
            utensil_washing_price=pricing.utensil_washing_price,
            utensil_washing_commission=pricing.utensil_washing_commission,
            children_special_price=pricing.children_special_price,
            preference_community_percentage=pricing.preference_community_percentage,
            kitchen_platform_price=pricing.kitchen_platform_price
        )
        if updated_pricing is None:
            raise HTTPException(status_code=404, detail="Pricing plan not found")
        return updated_pricing
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating pricing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/pricing/{pricing_id}", summary="Delete a pricing plan")
def delete_pricing_plan(pricing_id: int, db: Session = Depends(get_db)):
    """
    Delete a pricing plan:
    - **pricing_id**: The ID of the pricing plan to delete
    """
    try:
        if not delete_pricing(db, pricing_id):
            raise HTTPException(status_code=404, detail="Pricing plan not found")
        return {"message": "Pricing plan deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting pricing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
