from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class PricingTable(Base):
    __tablename__ = 'pricing_table'

    id = Column(Integer, primary_key=True, index=True)
    meal_plan = Column(String, index=True)  # Meal plan type (e.g., "Standard", Premium)
    price = Column(Float)  # Base price for the meal plan
    food_type = Column(String)  # Veg or Non-veg
    people_count = Column(Integer)  # Number of people
    frequency = Column(String)  # Frequency of service
    meal_details = Column(String)  # Details of meals provided

    # Additional Services
    utensil_washing_price = Column(Float)  # Service A
    utensil_washing_commission = Column(Float)
    children_special_price = Column(Float)  # Service B
    preference_community_percentage = Column(Float)  # Service C
    kitchen_platform_price = Column(Float)  # Service D

    created_at = Column(DateTime, default=func.now())

class AdditionalServicesPricing(Base):
    __tablename__ = 'additional_services_pricing'

    id = Column(Integer, primary_key=True, index=True)
    people_count = Column(Integer)
    
    # Service A - Utensil Washing
    utensil_washing_price = Column(Float)
    utensil_washing_commission = Column(Float)
    
    # Service B - Children Special
    children_special_price = Column(Float)
    
    # Service C - Preference Community
    preference_community_percentage = Column(Float)
    
    # Service D - Kitchen Platform & Gas Stove
    kitchen_platform_price = Column(Float)
    
    created_at = Column(DateTime, default=func.now())


