"""
Contains utilities for loading and preprocessing data from database
"""
import os
import gensim


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
