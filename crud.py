from sqlalchemy.orm import Session
from models import PricingTable

def create_pricing(db: Session, meal_plan: str, price: float, additional_services: str):
    db_pricing = PricingTable(
        meal_plan=meal_plan,
        price=price,
        additional_services=additional_services
    )
    db.add(db_pricing)
    db.commit()
    db.refresh(db_pricing)
    return db_pricing

def get_pricing(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PricingTable).offset(skip).limit(limit).all()