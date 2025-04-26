from sqlalchemy.orm import Session
from models import PricingTable

def create_pricing(
    db: Session,
    meal_plan: str,
    price: float,
    food_type: str,
    people_count: int,
    frequency: str,
    meal_details: str,
    utensil_washing_price: float | None = None,
    utensil_washing_commission: float | None = None,
    children_special_price: float | None = None,
    preference_community_percentage: float | None = None,
    kitchen_platform_price: float | None = None
):
    db_pricing = PricingTable(
        meal_plan=meal_plan,
        price=price,
        food_type=food_type,
        people_count=people_count,
        frequency=frequency,
        meal_details=meal_details,
        utensil_washing_price=utensil_washing_price,
        utensil_washing_commission=utensil_washing_commission,
        children_special_price=children_special_price,
        preference_community_percentage=preference_community_percentage,
        kitchen_platform_price=kitchen_platform_price
    )
    db.add(db_pricing)
    db.commit()
    db.refresh(db_pricing)
    return db_pricing

def get_pricing(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PricingTable).offset(skip).limit(limit).all()

def get_pricing_by_id(db: Session, pricing_id: int):
    return db.query(PricingTable).filter(PricingTable.id == pricing_id).first()

def update_pricing(
    db: Session,
    pricing_id: int,
    meal_plan: str | None = None,
    price: float | None = None,
    food_type: str | None = None,
    people_count: int | None = None,
    frequency: str | None = None,
    meal_details: str | None = None,
    utensil_washing_price: float | None = None,
    utensil_washing_commission: float | None = None,
    children_special_price: float | None = None,
    preference_community_percentage: float | None = None,
    kitchen_platform_price: float | None = None
):
    db_pricing = get_pricing_by_id(db, pricing_id)
    if db_pricing:
        update_data = {
            "meal_plan": meal_plan,
            "price": price,
            "food_type": food_type,
            "people_count": people_count,
            "frequency": frequency,
            "meal_details": meal_details,
            "utensil_washing_price": utensil_washing_price,
            "utensil_washing_commission": utensil_washing_commission,
            "children_special_price": children_special_price,
            "preference_community_percentage": preference_community_percentage,
            "kitchen_platform_price": kitchen_platform_price
        }
        
        # Update only provided fields
        for key, value in update_data.items():
            if value is not None:
                setattr(db_pricing, key, value)
        
        db.commit()
        db.refresh(db_pricing)
    return db_pricing

def delete_pricing(db: Session, pricing_id: int):
    db_pricing = get_pricing_by_id(db, pricing_id)
    if db_pricing:
        db.delete(db_pricing)
        db.commit()
        return True
    return False