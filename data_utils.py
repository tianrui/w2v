"""
Contains utilities for loading and preprocessing data from database
"""
import os


def load_data_sentences(dirname):
"""
Load all sentences in files under dirname
"""
    for fname in os.listdir(dirname):
        for line in open(os.path.join(dirname, fname):
                yield line.split()

