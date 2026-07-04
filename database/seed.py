import uuid
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from database.models import Base, engine, SessionLocal, User, Task

def seed_data():
    # Create a new database session
    session = SessionLocal()

    try:
        # Insert sample users
        user1 = User(
            id=str(uuid.uuid4()),
            email="alice@example.com",
            password_hash="hashed_password_1",
            created_at=datetime(2023, 10, 1, 12, 0, 0)
        )
        user2 = User(
            id=str(uuid.uuid4()),
            email="bob@example.com",
            password_hash="hashed_password_2",
            created_at=datetime(2023, 10, 2, 12, 0, 0)
        )
        user3 = User(
            id=str(uuid.uuid4()),
            email="charlie@example.com",
            password_hash="hashed_password_3",
            created_at=datetime(2023, 10, 3, 12, 0, 0)
        )

        session.add_all([user1, user2, user3])

        # Insert sample tasks
        task1 = Task(
            id=str(uuid.uuid4()),
            user_id=user1.id,
            title="Buy groceries",
            description="Milk, Bread, Eggs",
            completed=False,
            created_at=datetime(2023, 10, 1, 13, 0, 0)
        )
        task2 = Task(
            id=str(uuid.uuid4()),
            user_id=user2.id,
            title="Finish project",
            description="Complete the final report",
            completed=False,
            created_at=datetime(2023, 10, 2, 14, 0, 0)
        )
        task3 = Task(
            id=str(uuid.uuid4()),
            user_id=user3.id,
            title="Call mom",
            description="Check in and say hello",
            completed=False,
            created_at=datetime(2023, 10, 3, 15, 0, 0)
        )

        session.add_all([task1, task2, task3])

        # Commit the transaction
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error seeding data: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    seed_data()