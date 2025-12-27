from sqlalchemy.orm import Session
from backend.database import SessionLocal, User, engine

# Ensure tables exist (they should, but just in case)
# database.Base.metadata.create_all(bind=engine)

def check_users():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        print(f"Total Users: {len(users)}")
        for user in users:
            print(f"ID: {user.id}, Username: {user.username}, Name: {user.full_name}, Role: {user.role}")
    finally:
        db.close()

if __name__ == "__main__":
    check_users()
