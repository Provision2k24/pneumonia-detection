import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import os

class PneumoniaCNN(nn.Module):
    def __init__(self):
        super(PneumoniaCNN, self).__init__()
        self.model = nn.Sequential(
            nn.Conv2d(3, 32, 3), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 3), nn.ReLU(), nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(128 * 17 * 17, 128), nn.ReLU(),
            nn.Linear(128, 1), nn.Sigmoid()
        )
    
    def forward(self, x):
        return self.model(x)

# Load the model once when the module is imported
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = PneumoniaCNN().to(device)

# Load the trained weights
weights_path = os.path.join(os.path.dirname(__file__), 'pneumonia_cnn_weights.pth')
model.load_state_dict(torch.load(weights_path, map_location=device))
model.eval()

# Define the same transform used during training
transform = transforms.Compose([
    transforms.Resize((150, 150)),
    transforms.ToTensor()
])

def predict_pneumonia(image_path):
    """
    Predict whether an X-ray image shows pneumonia or not.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        tuple: (diagnosis, confidence, raw_output)
            - diagnosis (str): "Pneumonia" or "Normal"
            - confidence (float): Confidence percentage (0-100)
            - raw_output (float): Raw model output (0-1)
    """
    try:
        # Load and preprocess the image
        image = Image.open(image_path).convert('RGB')
        image_tensor = transform(image).unsqueeze(0).to(device)
        
        # Make prediction
        with torch.no_grad():
            output = model(image_tensor)
            probability = output.item()
            
        # Convert to diagnosis and confidence
        if probability > 0.5:
            diagnosis = "Pneumonia"
            confidence = probability * 100
        else:
            diagnosis = "Normal"
            confidence = (1 - probability) * 100
            
        return diagnosis, confidence, probability
        
    except Exception as e:
        print(f"Error in prediction: {str(e)}")
        return "Error", 0.0, 0.0

def get_model_info():
    """
    Get information about the loaded model.
    
    Returns:
        dict: Model information
    """
    return {
        "model_type": "PneumoniaCNN",
        "device": str(device),
        "weights_loaded": os.path.exists(weights_path),
        "input_size": (150, 150),
        "classes": ["Normal", "Pneumonia"]
    }