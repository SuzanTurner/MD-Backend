from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from crud import create_pricing, get_pricing

app = FastAPI(
    title="Meal Delivery API",
    description="API for managing meal delivery pricing and services",
    version="1.0.0"
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
            "POST /pricing/": "Add a new pricing plan"
        }
    }

@app.post("/pricing/", summary="Add new pricing plan")
def add_pricing(meal_plan: str, price: float, additional_services: str, db: Session = Depends(get_db)):
    """
    Add a new pricing plan with the following information:
    - **meal_plan**: Name of the meal plan
    - **price**: Price of the meal plan
    - **additional_services**: Any additional services included
    """
    return create_pricing(db=db, meal_plan=meal_plan, price=price, additional_services=additional_services)

@app.get("/pricing/", summary="Get all pricing plans")
def read_pricing(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all pricing plans with pagination:
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100)
    """
    return get_pricing(db=db, skip=skip, limit=limit)
