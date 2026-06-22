import os
import sys

# Ensure backend is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.database.database import engine
from backend.database.models.base import Base

def init_db():
    print("Initializing the database tables...")
    try:
        # Create all tables defined in models
        Base.metadata.create_all(bind=engine)
        print("Success: Database tables created successfully!")
        
        # Display registered tables
        print("\nCreated tables:")
        for table_name in Base.metadata.tables.keys():
            print(f" - {table_name}")
            
    except Exception as e:
        print(f"Error initializing the database: {e}", file=sys.stderr)

if __name__ == "__main__":
    init_db()
