"""
Contains utilities for loading and preprocessing data from database
"""
import os
import gensim
import pymongo
from pymongo import MongoClient
from attrdict import AttrDict
import nltk.data, nltk.tokenize

def load_data_sentences(dirname):
    """
    Load all sentences in files under dirname
    """
    sentence_list = []
    for fname in os.listdir(dirname):
        with open(os.path.join(dirname, fname)) as file:
            #sentence_list.append(gensim.models.word2vec.LineSentence(file))
            sentence_list.append(file)
    return sentence_list

def train_dynamic(batch_size=10):
    """
    Extract webpage information from each page,
    add as a batch of training data
    """
    
    return

def sentence_tokenize(text, language='english'):
    tokenizer = nltk.data.load('tokenizers/punkt/{0}.pickle'.format(language))

    return tokenizer.tokenize(text)

def word_tokenize(text, language='english'):
    return nltk.tokenize.word_tokenize(text)
