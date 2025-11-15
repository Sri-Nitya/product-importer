import time
import sys
from sqlalchemy.exc import OperationalError
from app.db.session import engine
from app.db.model import Base


def wait_for_db(max_retries: int = 10, delay: int = 3) -> None:
    attempt = 0
    while attempt < max_retries:
        try:
            # try to connect
            with engine.connect():
                print("Database connection successful.")
                return
        except OperationalError as e:
            attempt += 1
            print(f"Database not ready (attempt {attempt}/{max_retries}): {e}")
            time.sleep(delay)
    print("Exceeded maximum retries waiting for database.")
    raise RuntimeError("Database not available")


def create_table():
    wait_for_db()
    Base.metadata.create_all(bind=engine)
    print("Table created successfully.")


if __name__ == "__main__":
    try:
        create_table()
    except Exception as e:
        print(f"Failed to create tables: {e}", file=sys.stderr)
        sys.exit(1)

