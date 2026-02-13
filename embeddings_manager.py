import pymongo 
from sentence_transformers import SentenceTransformer, util
import pandas as pd
import os

client = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = client['VadaPavFashion']
collection = mydb['fashion_items']


model = SentenceTransformer("all-MiniLM-L6-v2")
data = pd.read_csv('fashion-dataset/styles.csv', on_bad_lines='skip')

# Columns to vectorize
text_columns = ['gender', 'masterCategory', 'subCategory', 'articleType', 'baseColour', 'season', 'usage', 'productDisplayName'] 

for index, row in data.iterrows():
    id = row['id']
    try:
        text_combined = ''
        for col in text_columns:
            if pd.isna(row[col]):
                continue
            text_combined += str(row[col]) + ' '
        
        if text_combined.strip():
            vector = model.encode(text_combined.strip())
            update_dict = {'combined_vector': vector.tolist()}
            result = collection.find_one_and_update({"id": id}, {'$set': update_dict})
            if result:
                print(f'{id} combined vector updated')
            else:
                print(f'{id} not found in database')
        else:
            print(f'{id} no text to vectorize')
    except Exception as e:
        print(f'Error processing {id}: {e}')
        
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