import pytesseract
from PIL import Image
import io
import json
from cryptography.fernet import Fernet
import os
from typing import Dict, Any

class MedicalCryptoService:
    def __init__(self):
        # In production, this key should be managed via a secure KMS (Key Management Service)
        self.key = os.getenv("ENCRYPTION_KEY", Fernet.generate_key())
        self.cipher = Fernet(self.key)

    def encrypt_file(self, file_content: bytes) -> bytes:
        return self.cipher.encrypt(file_content)

    def decrypt_file(self, encrypted_content: bytes) -> bytes:
        return self.cipher.decrypt(encrypted_content)

class OCRService:
    @staticmethod
    def extract_text(image_content: bytes) -> str:
        image = Image.open(io.BytesIO(image_content))
        text = pytesseract.image_to_string(image)
        return text

class DietRecommendationEngine:
    @staticmethod
    def generate_diet_plan(diagnosis_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Maps medical markers to specific diet templates with structured data.
        """
        markers = {m["name"]: m["value"] for m in diagnosis_data.get("biomarkers", [])}
        
        # Default Plan: Balanced
        diet_type = "Balanced Maintenance"
        macros = {"calories": 2000, "protein": 150, "carbs": 200, "fats": 65, "hydration": 2500}
        meals = [
            {"time": "Breakfast", "name": "Oatmeal with Berries", "calories": 400, "protein": 12, "carbs": 60, "fats": 8, "desc": "Steel-cut oats with blueberries and almonds"},
            {"time": "Lunch", "name": "Grilled Chicken Salad", "calories": 600, "protein": 45, "carbs": 20, "fats": 35, "desc": "Mixed greens, cherry tomatoes, balsamic vinaigrette"},
            {"time": "Snack", "name": "Greek Yogurt Parfait", "calories": 250, "protein": 15, "carbs": 30, "fats": 5, "desc": "Low-fat yogurt with honey and granola"},
            {"time": "Dinner", "name": "Baked Salmon & Quinoa", "calories": 550, "protein": 40, "carbs": 45, "fats": 20, "desc": "Lemon herb salmon with steamed broccoli"}
        ]
        shopping_list = ["Oats", "Blueberries", "Chicken Breast", "Mixed Greens", "Salmon", "Quinoa", "Greek Yogurt"]

        # Logic layer
        if markers.get("Glucose", 0) > 126 or markers.get("HbA1c", 0) > 6.5:
            diet_type = "Low Glycemic / Diabetic Friendly"
            macros = {"calories": 1800, "protein": 140, "carbs": 130, "fats": 70, "hydration": 2200}
            meals = [
                {"time": "Breakfast", "name": "Vegetable Omelet", "calories": 350, "protein": 22, "carbs": 8, "fats": 25, "desc": "3 eggs with spinach and mushrooms"},
                {"time": "Lunch", "name": "Turkey Lettuce Wraps", "calories": 450, "protein": 35, "carbs": 15, "fats": 28, "desc": "Lean ground turkey, asian slaw, lettuce cups"},
                {"time": "Snack", "name": "Handful of Almonds", "calories": 180, "protein": 6, "carbs": 6, "fats": 16, "desc": "Raw almonds (unsalted)"},
                {"time": "Dinner", "name": "Zucchini Noodles with Pesto", "calories": 400, "protein": 28, "carbs": 12, "fats": 24, "desc": "Spiralized zucchini, chicken, basil pesto"}
            ]
            shopping_list = ["Eggs", "Spinach", "Ground Turkey", "Lettuce", "Zucchini", "Chicken Breast", "Almonds", "Pesto"]
        
        elif markers.get("Systolic BP", 0) > 140:
            diet_type = "DASH (Heart Healthy)"
            macros = {"calories": 1900, "protein": 130, "carbs": 220, "fats": 50, "hydration": 2000}
            meals = [
                {"time": "Breakfast", "name": "Banana & Spinach Smoothie", "calories": 300, "protein": 10, "carbs": 55, "fats": 4, "desc": "Spinach, banana, skim milk, chia seeds"},
                {"time": "Lunch", "name": "Lentil Soup", "calories": 450, "protein": 25, "carbs": 65, "fats": 8, "desc": "Low-sodium lentil soup with whole wheat roll"},
                {"time": "Snack", "name": "Apple Slices", "calories": 100, "protein": 1, "carbs": 25, "fats": 0, "desc": "Fresh apple slices"},
                {"time": "Dinner", "name": "Grilled White Fish", "calories": 500, "protein": 45, "carbs": 40, "fats": 15, "desc": "Cod or Tilapia with brown rice and asparagus"}
            ]
            shopping_list = ["Banana", "Spinach", "Skim Milk", "Lentils", "Whole Wheat Rolls", "Cod/Tilapia", "Brown Rice", "Asparagus"]

        elif markers.get("Creatinine", 0) > 1.2:
            diet_type = "Renal Friendly"
            macros = {"calories": 1800, "protein": 60, "carbs": 250, "fats": 60, "hydration": 1800}
            meals = [
                {"time": "Breakfast", "name": "Rice Cereal with Berries", "calories": 350, "protein": 4, "carbs": 70, "fats": 4, "desc": "Rice cereal with almond milk and strawberries"},
                {"time": "Lunch", "name": "Pasta with Olive Oil", "calories": 500, "protein": 10, "carbs": 80, "fats": 14, "desc": "White pasta with garlic, olive oil, and bell peppers"},
                {"time": "Snack", "name": "Rice Cakes", "calories": 100, "protein": 2, "carbs": 22, "fats": 0, "desc": "Plain rice cakes"},
                {"time": "Dinner", "name": "Eggplant Stir-fry", "calories": 450, "protein": 8, "carbs": 60, "fats": 20, "desc": "Eggplant, onions, carrots, white rice"}
            ]
            shopping_list = ["Rice Cereal", "Strawberries", "Pasta", "Bell Peppers", "Eggplant", "White Rice", "Rice Cakes"]

        return {
            "diet_type": diet_type,
            "macros": macros,
            "meals": meals,
            "shopping_list": shopping_list,
            "recommendations": [f"Follow the {diet_type} plan.", "Stay hydrated.", "Monitor portion sizes."]
        }

class BiomarkerExtractor:
    @staticmethod
    def parse_with_llm(text: str) -> Dict[str, Any]:
        """
        Extracts structured biomarkers with reference ranges.
        """
        # Hardcoded simulation of typical lab report findings
        biomarkers = [
            {"name": "Glucose", "value": 142, "unit": "mg/dL", "range": "70 - 99", "status": "High"},
            {"name": "HbA1c", "value": 7.2, "unit": "%", "range": "4.0 - 5.6", "status": "High"},
            {"name": "Cholesterol", "value": 225, "unit": "mg/dL", "range": "< 200", "status": "High"},
            {"name": "Systolic BP", "value": 145, "unit": "mmHg", "range": "90 - 120", "status": "High"},
            {"name": "Creatinine", "value": 0.9, "unit": "mg/dL", "range": "0.7 - 1.3", "status": "Normal"}
        ]
        
        return {
            "biomarkers": biomarkers,
            "interpretation": "Analysis shows elevated blood sugar and blood pressure. Renal markers are within normal range."
        }


class NutritionEstimator:
    @staticmethod
    def estimate_nutrition(query: str) -> Dict[str, Any]:
        """
        Simulates an AI estimation of nutrition from natural language text.
        In a real app, this would call an LLM or Nutrition API (e.g., Edamam, Nutritionix).
        """
        query = query.lower()
        
        # Simple local database for demo purposes
        db = {
            "oatmeal": {"calories": 150, "protein": 5, "carbs": 27, "fats": 3},
            "egg": {"calories": 70, "protein": 6, "carbs": 1, "fats": 5},
            "chicken": {"calories": 165, "protein": 31, "carbs": 0, "fats": 3.6},
            "salad": {"calories": 50, "protein": 2, "carbs": 10, "fats": 0},
            "apple": {"calories": 95, "protein": 0.5, "carbs": 25, "fats": 0.3},
            "rice": {"calories": 130, "protein": 2.7, "carbs": 28, "fats": 0.3},
            "banana": {"calories": 105, "protein": 1.3, "carbs": 27, "fats": 0.3},
            "yogurt": {"calories": 59, "protein": 10, "carbs": 3.6, "fats": 0.4},
            "salmon": {"calories": 208, "protein": 20, "carbs": 0, "fats": 13},
            "avocado": {"calories": 160, "protein": 2, "carbs": 9, "fats": 15},
            "almonds": {"calories": 164, "protein": 6, "carbs": 6, "fats": 14},
            "steak": {"calories": 271, "protein": 26, "carbs": 0, "fats": 19},
        }

        # Fuzzy match logic
        for key, data in db.items():
            if key in query:
                return data
        
        # Default fallback if unknown
        return {"calories": 0, "protein": 0, "carbs": 0, "fats": 0}
