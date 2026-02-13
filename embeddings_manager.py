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
data = pd.read_csv('fashon-dataset/styles.csv')

for index, row in data.iterrows():
    id = row['id']
    if os.path.exists:
        try:
            vector_text = model.encode(row['productDisplayName'])
        except:
            print('error1')
        try:
            collection.find_one_and_update({"id":id}, {'text_vector': vector_text})
            print(f'{id} is done')
        except:
            print('error2')




# get each image
# get the model
# store image embeddings