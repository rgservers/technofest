import pymongo
import pandas as pd
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel
import os

# MongoDB setup
client = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = client['VadaPavFashion']
collection = mydb['fashion_items']

# Load CLIP model
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Load dataset metadata
styles_df = pd.read_csv('fashion-dataset/styles.csv', on_bad_lines='skip')

# Directory for images
image_dir = 'fashion-dataset/images/'

# Function to get image vector
def get_image_vector(image_path):
    try:
        image = Image.open(image_path).convert("RGB")
        inputs = processor(images=image, return_tensors="pt")
        with torch.no_grad():
            vision_outputs = model.vision_model(pixel_values=inputs['pixel_values'])
            pooled_output = vision_outputs.pooler_output
            image_features = model.visual_projection(pooled_output)
        return image_features.squeeze().tolist()
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

# Process each item
for index, row in styles_df.iterrows():
    item_id = row['id']
    image_path = os.path.join(image_dir, f"{item_id}.jpg")

    if os.path.exists(image_path):
        vector = get_image_vector(image_path)
        if vector:
            # Prepare document
            document = {
                'id': item_id,
                'gender': row['gender'],
                'masterCategory': row['masterCategory'],
                'subCategory': row['subCategory'],
                'articleType': row['articleType'],
                'baseColour': row['baseColour'],
                'season': row['season'],
                'year': row['year'],
                'usage': row['usage'],
                'productDisplayName': row['productDisplayName'],
                'vector': vector
            }
            # Insert into MongoDB
            collection.insert_one(document)
            print(f"Inserted item {item_id}")
        else:
            print(f"Skipped {item_id} due to vector error")
    else:
        print(f"Image not found for {item_id}")

print("Vectorization and MongoDB insertion completed.")

