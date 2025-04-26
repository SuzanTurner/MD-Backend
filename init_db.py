from database import engine
from models import Base

def init_db():
    try:
        # Drop all tables
        Base.metadata.drop_all(bind=engine)
        print("Existing tables dropped successfully!")
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error managing database tables: {e}")

if __name__ == "__main__":
    init_db() 