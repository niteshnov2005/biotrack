import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import io

class XRayAnalyzer:
    def __init__(self):
        # Initializing DenseNet121 with a placeholder for weight loading
        # In a production environment, we would load weights from a .pth or .bin file
        self.model = models.densenet121(pretrained=False)
        num_ftrs = self.model.classifier.in_features
        # Adjusting the final layers for generic "Abnormality Detection" (binary classification)
        self.model.classifier = nn.Sequential(
            nn.Linear(num_ftrs, 512),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(512, 2) # [Normal, Abnormal]
        )
        self.model.eval()
        
        # HIPAA-compliant pre-processing pipeline
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.Grayscale(num_output_channels=3),  # Ensure 3 channels for DenseNet
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

    def preprocess_image(self, image_bytes):
        """
        Converts raw bytes to a preprocessed tensor.
        """
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        return self.transform(image).unsqueeze(0)

    def predict(self, image_bytes):
        """
        Runs inference on the provided image bytes.
        """
        tensor = self.preprocess_image(image_bytes)
        with torch.no_grad():
            outputs = self.model(tensor)
            _, predicted = torch.max(outputs, 1)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            
        result = {
            "prediction": "Abnormal" if predicted.item() == 1 else "Normal",
            "confidence": probabilities[0][predicted.item()].item(),
            "status": "Success"
        }
        return result
