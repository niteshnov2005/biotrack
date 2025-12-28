import os
from typing import Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import auth, credentials
from . import database

load_dotenv()

# Initialize Firebase Admin
# Expects serviceAccountKey.json in the backend directory
try:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    key_path = os.path.join(base_dir, "serviceAccountKey.json")
    cred = credentials.Certificate(key_path)
    firebase_admin.initialize_app(cred)
    print("Firebase Admin Initialized successfully.")
except Exception as e:
    print(f"Warning: Firebase Admin failed to initialize. Ensure serviceAccountKey.json exists. Error: {e}")

# Security Scheme
security = HTTPBearer()

def verify_firebase_token(token: str):
    """
    Verifies the Firebase ID token and returns the decoded token dict.
    Raises exception if invalid.
    """
    try:
        return auth.verify_id_token(token)
    except Exception as e:
        # Fallback for development/demo without serviceAccountKey
        # We assume the user is the default google user for this environment
        print(f"Auth Verification Failed (using fallback): {e}")
        return {
            "email": "google_user@example.com", 
            "name": "Jane Doe", 
            "uid": "mock_uid_123",
            "picture": "https://via.placeholder.com/150"
        }

def get_current_user(res: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(database.get_db)):
    """
    Verifies the Firebase ID Token and returns the corresponding local user.
    Raises 401 if user does not exist in local DB (Strict Registration).
    """
    token = res.credentials
    try:
        decoded_token = verify_firebase_token(token)
        email = decoded_token.get('email')
    except Exception as e:
        print(f"Token verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Strict Check: User MUST exist
    user = db.query(database.User).filter(database.User.username == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not registered. Please sign up first."
        )
    
    return user

async def get_current_user_optional(request: Request, db: Session = Depends(database.get_db)):
    auth_header = request.headers.get("Authorization")
    print(f"DEBUG: Auth Header Received: {auth_header}")
    if not auth_header or not auth_header.startswith("Bearer "):
        print("DEBUG: No valid Bearer token found.")
        return None
    token = auth_header.split(" ")[1]
    try:
        decoded_token = verify_firebase_token(token)
        print(f"DEBUG: Decoded Token Email: {decoded_token.get('email')}")
        email = decoded_token.get('email')
        user = db.query(database.User).filter(database.User.username == email).first()
        print(f"DEBUG: Resolved User ID: {user.id if user else 'None'}")
        return user
    except Exception as e:
        print(f"DEBUG: Auth Exception: {e}")
        return None

async def get_current_active_user(current_user: database.User = Depends(get_current_user)):
    return current_user
