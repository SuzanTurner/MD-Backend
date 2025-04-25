import pandas as pd
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, PricingTable
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

def import_excel_to_db():
    try:
        # Read Excel file
        logger.info("Reading Excel file...")
        df = pd.read_excel("Pricing MD.xlsx", header=None)
        
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
                        
                    pricing = PricingTable(
                        meal_plan=f"{plan_type} - {num_people} people",
                        price=float(price),
                        additional_services=f"Food Type: {food_type}, Details: {basic_details}, Frequency: {frequency}"
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
    import_excel_to_db() 