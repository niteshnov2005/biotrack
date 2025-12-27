import random

class XRayAnalyzer:
    def __init__(self):
        # Mock initialization (No heavy model loading)
        print("XRayAnalyzer initialized (Mock Mode)")
        pass

    def predict(self, image_bytes):
        """
        Mock inference to save memory/build time for deployment.
        """
        # Simulate processing time or logic if needed
        is_abnormal = random.choice([True, False])
        confidence = random.uniform(0.7, 0.99)
        
        return {
            "prediction": "Abnormal" if is_abnormal else "Normal",
            "confidence": confidence,
            "status": "Success"
        }
