"""
Contains utilities for loading and preprocessing data from database
"""
import os
import gensim
import pymongo
from pymongo import MongoClient
from attrdict import AttrDict


def load_data_sentences(dirname):
    """
    Load all sentences in files under dirname
    """
    sentence_list = []
    for fname in os.listdir(dirname):
        with open(os.path.join(dirname, fname)) as file:
            sentence_list.append(gensim.models.LineSentence(file)
    return sentence_list

def train_dynamic(batch_size=10):
    """
    Extract webpage information from each page,
    add as a batch of training data
    """
    
    return

def fetch_product_list(host_string, product_database, product_collection):
    product_list = []
    client = MongoClient(host_string)
    db = client[product_database]
    product_posts = db[product_collection]

    for product_post in product_posts.find():
        product = AttrDicti({'prodID': product_post['product'],
                             'tags': product_post['tags']})
        product_list.append(product)
    return product_list
    
