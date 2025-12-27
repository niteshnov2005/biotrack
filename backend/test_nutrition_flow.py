from services import DietRecommendationEngine, MedicalCryptoService
import json

# 1. Simulate Biomarker Data (e.g. from a report)
biomarkers = {
    "blood_sugar": 130, # High -> Diabetic
    "hba1c": 7.0,
    "cholesterol": 200
}

# 2. Run Engine
engine = DietRecommendationEngine()
plan = engine.generate_diet_plan({"biomarkers": biomarkers})

print("Generated Plan Structure:")
print(json.dumps(plan, indent=2))

# 3. Verify Structure Keys
required_keys = ["diet_type", "macros", "meals", "shopping_list"]
missing = [k for k in required_keys if k not in plan]

if missing:
    print(f"FAILED: Missing keys {missing}")
else:
    print("SUCCESS: Plan has all required keys.")

# 4. encrypt/decrypt check to ensure mapped correctly in DB flow
crypto = MedicalCryptoService()
encrypted = crypto.encrypt_file(json.dumps(plan).encode())
decrypted = crypto.decrypt_file(encrypted)
loaded_plan = json.loads(decrypted.decode())

if loaded_plan == plan:
    print("SUCCESS: Encryption/Decryption flow preserves data integrity.")
else:
    print("FAILED: Data mismatch after encryption roundtrip.")
