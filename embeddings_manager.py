import pymongo 
import flask
import numpy as np
from sentence_transformers import SentenceTransformer, util
import pandas as pd
import os
import json

client = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = client['VadaPavFashion']
collection = mydb['fashion_items']


model = SentenceTransformer("all-MiniLM-L6-v2")
data = pd.read_csv('fashion-dataset/styles.csv', on_bad_lines='skip')

# Columns to vectorize
dse = 0

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




# get each image
# get the model
# store image embeddings