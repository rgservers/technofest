import pymongo
import elasticsearch
import flask
import numpy as np
from sentence_transformers import SentenceTransformer, util
import pandas as pd

model = SentenceTransformer("all-MiniLM-L6-v2")



# get each image
# get the model
# store image embeddings