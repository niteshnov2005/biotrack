import requests
import json
import os
import sys

# Add backend to path to import services safely
sys.path.append(os.path.join(os.getcwd(), 'backend'))
sys.path.append("d:/miniproject/backend")

from backend import database, services, main
from fastapi.testclient import TestClient

# We can use TestClient to simulate the API call without running the server separately!
client = TestClient(main.app)

def test_upload():
    print("Testing Report Upload & Analysis Generation...")
    
    # 1. Create a dummy PDF/Image
    dummy_pdf = b"%PDF-1.4 header dummy content"
    files = {'file': ('test_report.pdf', dummy_pdf, 'application/pdf')}
    
    # 2. Mock Auth? 
    # analyze-report requires auth. 
    # TestClient doesn't automatically auth.
    # But main.py uses Depends(auth.get_current_user_optional).
    # If we don't send header, it falls back to guest.
    
    response = client.post("/analyze-report", files=files)
    
    if response.status_code == 200:
        print("Upload Success.")
        data = response.json()
        print("Response Keys:", data.keys())
        
        if "diet_plan" in data:
            dp = data["diet_plan"]
            print("Diet Plan Keys:", dp.keys())
            if "macros" in dp:
                print("SUCCESS: Macros found in response:", dp["macros"])
            else:
                print("FAILURE: Macros MISSING in response.")
        else:
            print("FAILURE: Diet Plan missing.")
            
    else:
        print(f"Upload Failed: {response.status_code} {response.text}")

if __name__ == "__main__":
    test_upload()
