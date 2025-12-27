import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'backend'))
sys.path.append("d:/miniproject/backend")
from backend import database, main
from sqlalchemy import func
import json

def debug_data():
    database.init_db()
    db = database.SessionLocal()
    
    print("-" * 30)
    print("USERS:")
    users = db.query(database.User).all()
    for u in users:
        print(f"ID: {u.id}, Username: {u.username}, Role: {u.role}")

    print("-" * 30)
    print("ANALYSIS RESULTS:")
    results = db.query(database.AnalysisResult).all()
    for r in results:
        print(f"ID: {r.id}, UserID: {r.user_id}, Type: {r.analysis_type}, Created: {r.created_at}")

    print("-" * 30)
    print("-" * 30)
    print("ANALYSIS RESULTS (Latest 5):")
    results = db.query(database.AnalysisResult).order_by(database.AnalysisResult.id.desc()).limit(5).all()
    for r in results:
        print(f"ID: {r.id}, UserID: {r.user_id}, Type: {r.analysis_type}, Created: {r.created_at}")
    
    print("-" * 30)
    print("MEAL LOGS (User 2):")
    meals = db.query(database.MealLog).filter(database.MealLog.user_id == 2).all()
    if not meals:
        print("No meals found for User 2.")
    for m in meals:
        print(f"ID: {m.id}, Name: {m.name}, Cals: {m.calories}, Date: {m.created_at}")
    
    # Inspect specific report for User 2 (ID 4)
    target_report_id = 4
    report = db.query(database.AnalysisResult).filter(database.AnalysisResult.id == target_report_id).first()
    if report:
        print("-" * 30)
        print(f"INSPECTING REPORT ID {target_report_id}:")
        try:
            from backend import services
            crypto = services.MedicalCryptoService()
            key_env = os.getenv("ENCRYPTION_KEY")
            if not key_env:
                print("CRITICAL: ENCRYPTION_KEY missing.")
            else:
                 decrypted = crypto.decrypt_file(report.encrypted_data.encode())
                 data = json.loads(decrypted.decode())
                 if "diet_plan" in data:
                     dp = data["diet_plan"]
                     if "macros" in dp:
                         print("MACROS FOUND:", dp["macros"])
                     else:
                         print("MACROS MISSING in Report", target_report_id)
                 else:
                     print("DIET PLAN MISSING")
        except Exception as e:
            print(f"DECRYPTION FAILED: {e}")

if __name__ == "__main__":
    debug_data()
