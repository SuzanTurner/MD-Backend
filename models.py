from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class PricingTable(Base):
    __tablename__ = 'pricing_table'

    id = Column(Integer, primary_key=True, index=True)
    meal_plan = Column(String, index=True)  # Meal plan type (e.g., "Standard", Premium)
    price = Column(Float)  # Price for the meal plan
    additional_services = Column(String)  # Any additional services or details
    created_at = Column(DateTime, default=func.now())


