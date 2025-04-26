import pandas as pd
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, PricingTable, AdditionalServicesPricing
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def is_valid_price(value):
    try:
        if pd.isna(value):
            return False
        if isinstance(value, str) and value.strip().lower() == 'basic price':
            return False
        float(value)
        return True
    except (ValueError, TypeError):
        return False

def import_additional_services():
    try:
        logger.info("Importing additional services pricing...")
        df = pd.read_excel("Additional Services.xlsx", header=None, engine='openpyxl')
        
        db = SessionLocal()
        try:
            # Clear existing data
            db.query(AdditionalServicesPricing).delete()
            
            # Get the number of people columns (excluding the first column which has labels)
            people_counts = range(1, 8)  # 1 to 7+ people
            
            # Process each row
            for people_count in people_counts:
                col_idx = people_count  # Column index for this number of people
                
                service = AdditionalServicesPricing(
                    people_count=people_count if people_count < 7 else 7,
                    utensil_washing_price=float(df.iloc[1, col_idx]),  # Row 1: Utensil Washing
                    utensil_washing_commission=float(df.iloc[2, col_idx]),  # Row 2: Commission
                    children_special_price=float(df.iloc[3, col_idx]),  # Row 3: Children Special
                    preference_community_percentage=0.10,  # Fixed 10%
                    kitchen_platform_price=float(df.iloc[7, col_idx])  # Row 7: Kitchen Platform
                )
                db.add(service)
                logger.info(f"Added additional services pricing for {people_count} people")
            
            db.commit()
            logger.info("Additional services pricing imported successfully!")
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error importing additional services: {str(e)}")
            raise
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Error reading Additional Services Excel file: {str(e)}")
        raise

def import_excel_to_db():
    try:
        # Read Excel file
        logger.info("Reading Excel file...")
        df = pd.read_excel("Pricing MD.xlsx", header=None, engine='openpyxl')
        
        # Create database tables if they don't exist
        Base.metadata.create_all(bind=engine)
        
        # Create database session
        db = SessionLocal()
        
        try:
            # Clear existing data
            db.query(PricingTable).delete()
            
            # Process data in chunks of 8 columns (7 people + header)
            for chunk_start in range(0, len(df.columns), 8):
                chunk = df.iloc[:, chunk_start:chunk_start + 8]
                if len(chunk.columns) < 8:  # Skip incomplete chunks
                    continue
                
                # Get food type and plan type
                food_type = chunk.iloc[1, 1]  # Row 1, Column 1 (0-based)
                plan_type = chunk.iloc[2, 1]  # Row 2, Column 1 (0-based)
                
                # Skip if no food type or plan type
                if pd.isna(food_type) or pd.isna(plan_type):
                    continue
                
                # Get number of people (skip header column)
                people = chunk.iloc[3, 1:].tolist()
                
                # Get basic details
                basic_details = chunk.iloc[4, 1]  # Row 4, Column 1 (0-based)
                
                # Get frequency
                frequency = chunk.iloc[5, 1]  # Row 5, Column 1 (0-based)
                
                # Find the row with "Basic Price"
                for row_idx in range(len(chunk)):
                    if isinstance(chunk.iloc[row_idx, 0], str) and "Basic Price" in chunk.iloc[row_idx, 0]:
                        prices = chunk.iloc[row_idx, 1:].tolist()
                        break
                else:
                    continue  # Skip if no Basic Price row found
                
                # Import data for each number of people
                for i, (num_people, price) in enumerate(zip(people, prices)):
                    if not is_valid_price(price) or pd.isna(num_people):
                        continue
                    
                    # Get additional services pricing
                    additional_services = db.query(AdditionalServicesPricing).filter(
                        AdditionalServicesPricing.people_count == (i + 1 if i < 6 else 7)
                    ).first()
                    
                    pricing = PricingTable(
                        meal_plan=f"{plan_type} - {num_people} people",
                        price=float(price),
                        food_type=food_type,
                        people_count=i + 1 if i < 6 else 7,
                        frequency=frequency,
                        meal_details=basic_details,
                        utensil_washing_price=additional_services.utensil_washing_price if additional_services else None,
                        utensil_washing_commission=additional_services.utensil_washing_commission if additional_services else None,
                        children_special_price=additional_services.children_special_price if additional_services else None,
                        preference_community_percentage=additional_services.preference_community_percentage if additional_services else None,
                        kitchen_platform_price=additional_services.kitchen_platform_price if additional_services else None
                    )
                    db.add(pricing)
                    logger.info(f"Added pricing: {plan_type} - {num_people} people, Price: {price}")
            
            # Commit changes
            db.commit()
            logger.info("Data imported successfully!")
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error importing data: {str(e)}")
            raise
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Error reading Excel file: {str(e)}")
        raise

if __name__ == "__main__":
    import_additional_services()
    import_excel_to_db() 