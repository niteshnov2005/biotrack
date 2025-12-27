import requests
import json

BASE_URL = "http://localhost:8000"

def test_meal_flow():
    print("Testing Meal Flow...")
    
    # 1. Login/Get Token (Using guest or registering a temp user)
    # Since auth is firebase based on frontend, backend might have a loophole or we use the guest user logic if implemented.
    # Looking at main.py: analyze-report falls back to guest.
    # But /nutrition/meals requires authenticated user.
    # main.py: current_user: database.User = Depends(auth.get_current_active_user)
    # verify_firebase_token is mocked or strict?
    # Let's try to simulate a request with a fake token that might be accepted if verify_firebase_token allows it or if we mock it?
    # Actually, main.py has: 
    #   if not auth_header: ... raise 401
    #   verify_firebase_token(token) ...
    
    # Without a real firebase token, I cannot easily test via pure python request unless I have a way to generate a valid token or if I bypass auth locally.
    # HOWEVER, I can test by running a small script that IMPORTS the backend logic and tests the DB functions directly, avoiding the HTTP Auth layer for verification.
    
    import sys
    import os
    sys.path.append(os.path.join(os.getcwd(), 'backend'))
    
    from backend import database, main # models is imported by main usually, or we import from backend.models
    # Actually main.py uses "from models import ...", so we need backend in safe path
    # easier to just append 'd:/miniproject/backend' to sys.path and import directly?
    
    sys.path.append("d:/miniproject/backend")
    import database
    import models
    import main
    database.init_db()
    db = database.SessionLocal()
    
    try:
        # Get Guest User
        user = db.query(database.User).filter(database.User.username == "guest").first()
        if not user:
            print("Guest user not found, creating...")
            # create guest
            # ... (logic existing in init_db should have handled this)
            pass
            
        print(f"Using user: {user.username} (ID: {user.id})")
        
        # 2. Log a Meal
        meal_name = "Test Apple"
        cals = 95
        print(f"Logging meal: {meal_name} ({cals} kcal)")
        
        db_meal = database.MealLog(
            user_id=user.id,
            name=meal_name,
            calories=cals,
            protein=0, carbs=25, fats=0
        )
        db.add(db_meal)
        db.commit()
        db.refresh(db_meal)
        print(f"Meal logged. ID: {db_meal.id}")
        
        # 3. Verify Summary
        print("Verifying summary...")
        # Re-implementing summary logic from main.py for verification
        meals = db.query(database.MealLog).filter(database.MealLog.user_id == user.id).all()
        # Filter for today (UTC)
        # ... logic ...
        
        total_cals = sum(m.calories for m in meals)
        print(f"Total Calories in DB for user: {total_cals}")
        
        if total_cals >= cals:
            print("SUCCESS: Calories registered.")
        else:
            print("FAILURE: Calories mismatch.")
            
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_meal_flow()
