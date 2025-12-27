import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'backend'))
sys.path.append("d:/miniproject/backend")
from backend import auth, database
from fastapi import Request

# Mock proper DB session
database.init_db()
db = database.SessionLocal()

# Test Verify Token directly
print("Testing verify_firebase_token with garbage token...")
try:
    token_data = auth.verify_firebase_token("garbage_token")
    print("Token Data:", token_data)
except Exception as e:
    print("Verification Failed:", e)

# Test User Resolution
print("\nTesting User Resolution from Email...")
email = "google_user@example.com"
user = db.query(database.User).filter(database.User.username == email).first()
if user:
    print(f"User Found: ID {user.id}, Username {user.username}")
else:
    print("User NOT Found in DB!")

print("\nTesting get_current_user_optional logic simulation...")
try:
    # Simulate what happens in auth.py
    decoded = auth.verify_firebase_token("garbage")
    email_extracted = decoded.get("email")
    print(f"Extracted Email: {email_extracted}")
    user_resolved = db.query(database.User).filter(database.User.username == email_extracted).first()
    print(f"Resolved User: {user_resolved.id if user_resolved else 'None'}")
except Exception as e:
    print(f"Logic Failed: {e}")

db.close()
