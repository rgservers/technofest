import pymongo 
from sentence_transformers import SentenceTransformer, util
import pandas as pd
from PIL import Image
import httpx
from io import BytesIO
from transformers import Blip2Processor, Blip2ForConditionalGeneration
import torch
import os

client = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = client['VadaPavFashion']
collection = mydb['fashion_items']


model = SentenceTransformer("all-MiniLM-L6-v2")
data = pd.read_csv('fashion-dataset/styles.csv', on_bad_lines='skip')
data_image = pd.read_csv('fashion-dataset/images.csv', on_bad_lines='skip')

dse = 0
device = "cuda" if torch.cuda.is_available() else "cpu"
dir = 'fashion-dataset/images/'

processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
model = Blip2ForConditionalGeneration.from_pretrained(
    "Salesforce/blip2-opt-2.7b", load_in_8bit=True, device_map={"": 0}, dtype=torch.float16
) 

for index, row in data.iterrows():
    id = row['id']
    try:
        update_dict = {}
        text_total = ''
        for col in ['gender', 'masterCategory', 'subCategory', 'articleType', 'baseColour', 'season', 'usage', 'productDisplayName']:
            if pd.isna(row[col]):
                print(f'Skipping {col} for {id}: {col} is NaN')
                continue
            text_total += row[col] + ' '
        vector = model.encode(text_total)
        update_dict['main_vector'] = vector.tolist()
        
        if update_dict:
            result = collection.find_one_and_update({"id": id}, {'$set': update_dict})
            if result:
                dse += 1
                print(f'{id} vectors updated, documents processed: {dse}')
            else:
                print(f'{id} not found in database')
        else:
            print(f'{id} no vectors to update')
        
    except Exception as e:
        print(f'Error processing {id}: {e}')

for index, rows in data_image.iterrows():
    update_dict = {'image_number': rows['filename']}
    item_id = rows['id']

    image_path = os.path.join(dir, f"{item_id}.jpg")

    if os.path.exists(image_path):
        try :
            image = Image.open(image_path).convert("RGB")

            inputs = processor(images=image, return_tensors="pt").to(device, torch.float16)
            generated_ids = model.generate(**inputs)
            generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
            
            vector = model.encode(generated_text)
            update_dict['image vector'] = vector.tolist()

            if update_dict:
                result = collection.find_one_and_update({"id": id}, {'$set': update_dict})
                if result:
                    dse += 1
                    print(f'{id} vectors updated, documents processed: {dse}')
                else:
                    print(f'{id} not found in database')
            else:
                print(f'{id} no vectors to update')

        except Exception as e:
            print(e)

    




# get each image
# get the model
# store image embeddings