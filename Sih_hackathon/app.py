import io
import torch
import torchvision.transforms as transforms
from fastapi import FastAPI, File, UploadFile
from PIL import Image
from torchvision.models import resnet101

# Initialize FastAPI app
app = FastAPI(title="Plant Disease Detection API")

# Load the model
MODEL_PATH = "model/ResNet_101_ImageNet_plant-model-84.pth"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = resnet101(pretrained=False)
# Adjust the final fully connected layer according to your number of classes
num_classes = 20  # Change this to match your model's output classes
model.fc = torch.nn.Linear(model.fc.in_features, num_classes)
model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model.to(device)
model.eval()

# Define the image transformations
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Define the class labels
class_labels = [
    "Apple Aphis spp", "Apple Erisosoma lanigerum",
    "Apple Monillia laxa", "Apple Venturia inaequalis",
    "Apricot Coryneum beijerinckii", "Apricot Monillia laxa",
    "Cancer symptom", "Cherry Aphis spp",
    "Downy mildew", "Drying symptom",
    "Gray mold", "Leaf scars",
    "Peach Monillia laxa", "Peach Parthenolecanium corni",
    "Pear Erwinia amylovora", "Plum Aphis spp",
    "RoughBark", "StripeCanker",
    "Walnut Eriophyies erineus", "Walnut Gnomonialeptostyla",
]

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Read and preprocess the image
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data)).convert('RGB')
    image_tensor = transform(image).unsqueeze(0).to(device)

    # Make prediction
    with torch.no_grad():
        outputs = model(image_tensor)
        _, predicted = torch.max(outputs, 1)

    # Get the predicted class label
    predicted_class = class_labels[predicted.item()]

    return {"predicted_disease": predicted_class}
    #return JSONResponse(content={"predicted_disease": predicted_class})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8001)




# import io
# import torch
# import torchvision.transforms as transforms
# from fastapi import FastAPI, File, UploadFile, HTTPException
# from fastapi.responses import JSONResponse
# from PIL import Image
# from torchvision.models import resnet101, ResNet101_Weights
# import logging

# # Configure logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# # Initialize FastAPI app
# app = FastAPI(title="Plant Disease Detection API")

# # Load the model
# MODEL_PATH = "model/ResNet_101_ImageNet_plant-model-84.pth"
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# try:
#     logging.info("Loading the model...")
#     model = resnet101(weights=None)
#     num_classes = 20
#     model.fc = torch.nn.Linear(model.fc.in_features, num_classes)
#     model.load_state_dict(torch.load(MODEL_PATH, map_location=device, weights_only=True))
#     model.to(device)
#     model.eval()
#     logging.info("Model loaded successfully.")
# except Exception as e:
#     logging.error(f"Error loading model: {str(e)}")
#     model = None

# # Define the image transformations
# transform = transforms.Compose([
#     transforms.Resize(256),
#     transforms.CenterCrop(224),
#     transforms.ToTensor(),
#     transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
# ])

# # Define the class labels
# class_labels = [
#     "Apple Aphis spp", "Apple Erisosoma lanigerum",
#     "Apple Monillia laxa", "Apple Venturia inaequalis",
#     "Apricot Coryneum beijerinckii", "Apricot Monillia laxa",
#     "Cancer symptom", "Cherry Aphis spp",
#     "Downy mildew", "Drying symptom",
#     "Gray mold", "Leaf scars",
#     "Peach Monillia laxa", "Peach Parthenolecanium corni",
#     "Pear Erwinia amylovora", "Plum Aphis spp",
#     "RoughBark", "StripeCanker",
#     "Walnut Eriophyies erineus", "Walnut Gnomonialeptostyla",
# ]

# @app.post("/predict")
# async def predict(file: UploadFile = File(...)):
#     if not model:
#         logging.error("Model not loaded")
#         raise HTTPException(status_code=500, detail="Model not loaded")
    
#     try:
#         logging.info("Reading uploaded file")
#         image_data = await file.read()
#         logging.info("Opening image")
#         image = Image.open(io.BytesIO(image_data)).convert('RGB')
#         logging.info("Transforming image")
#         image_tensor = transform(image).unsqueeze(0).to(device)

#         logging.info("Making prediction")
#         with torch.no_grad():
#             outputs = model(image_tensor)
#             _, predicted = torch.max(outputs, 1)

#         predicted_class = class_labels[predicted.item()]
#         logging.info(f"Prediction made: {predicted_class}")

#         return JSONResponse(content={"predicted_disease": predicted_class})
#     except Exception as e:
#         logging.error(f"Prediction error: {str(e)}", exc_info=True)
#         raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="localhost", port=8001)



# import io
# import torch
# import torchvision.transforms as transforms
# from fastapi import FastAPI, File, UploadFile, HTTPException
# from fastapi.responses import JSONResponse
# from PIL import Image
# from torchvision.models import resnet101

# # Initialize FastAPI app
# app = FastAPI(title="Plant Disease Detection API")

# # Load the model
# MODEL_PATH = "model/ResNet_101_ImageNet_plant-model-84.pth"
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# model = resnet101(pretrained=False)
# num_classes = 20  # Change this to match your model's output classes
# model.fc = torch.nn.Linear(model.fc.in_features, num_classes)
# model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
# model.to(device)
# model.eval()

# # Define the image transformations
# transform = transforms.Compose([
#     transforms.Resize(256),
#     transforms.CenterCrop(224),
#     transforms.ToTensor(),
#     transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
# ])

# # Define the class labels
# class_labels = [
#     "Apple Aphis spp", "Apple Erisosoma lanigerum",
#     "Apple Monillia laxa", "Apple Venturia inaequalis",
#     "Apricot Coryneum beijerinckii", "Apricot Monillia laxa",
#     "Cancer symptom", "Cherry Aphis spp",
#     "Downy mildew", "Drying symptom",
#     "Gray mold", "Leaf scars",
#     "Peach Monillia laxa", "Peach Parthenolecanium corni",
#     "Pear Erwinia amylovora", "Plum Aphis spp",
#     "RoughBark", "StripeCanker",
#     "Walnut Eriophyies erineus", "Walnut Gnomonialeptostyla",
# ]

# @app.post("/predict")
# async def predict(file: UploadFile = File(...)):
#     try:
#         # Read the file
#         image_data = await file.read()
#         # Print file type and size for debugging
#         print(f"File type: {type(image_data)}, File size: {len(image_data)} bytes")
        
#         # Open and process the image
#         image = Image.open(io.BytesIO(image_data)).convert('RGB')
#         image_tensor = transform(image).unsqueeze(0).to(device)

#         # Make prediction
#         with torch.no_grad():
#             outputs = model(image_tensor)
#             _, predicted = torch.max(outputs, 1)

#         # Get the predicted class label
#         predicted_class = class_labels[predicted.item()]
#         return JSONResponse(content={"predicted_disease": predicted_class})

#     except Exception as e:
#         # Log and return error message
#         import traceback
#         error_message = traceback.format_exc()
#         print(f"Error processing the image: {error_message}")
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8001)
