from app.db.session import engine
from app.db.model import Base

def create_table():
    Base.metadata.create_all(bind=engine)
    print("Table created successfully.")

if __name__ == "__main__":
    create_table()

