import logging, gensim, nltk.data
import gensim.models as models
from data_utils import *
from tagmodel import *

import os
import argparse
import io
import scipy

def arg_parse():
    """Parse input args"""
    #host_string = 'mongodb://localhost:27017'
    #host_string = 'mongodb://011399.mlab.com:11399'
    host_string = 'mongodb://heroku_73s67dx7:2d6hshk9a78f2dlfkachg486t7@ds011399.mlab.com:11399/heroku_73s67dx7'
    #database_string = 'test'
    database_string = 'heroku_73s67dx7'
    product_collection_string = 'products'
    recom_collection_string = 'recommendations'
    datadir = './data/'
    modelfname = './model'
    updatefname = 'recommendation_data.txt'

    parser = argparse.ArgumentParser(description='Training word2vec model with Amazon database')
    parser.add_argument('-host', default=host_string, type=str,
                        help='Mongo DB client host')
    parser.add_argument('-database', default=database_string, type=str,
                        help='Mongo DB database')
    parser.add_argument('-prod_collection', default=product_collection_string, type=str,
                        help='MongoDB Collection of products')
    parser.add_argument('-recom_collection', default=recom_collection_string, type=str,
                        help='MongoDB Collection of recommendations')
    parser.add_argument('-datadir', default=datadir, type=str,
                        help='Directory for storing training data')
    parser.add_argument('-modelfname', default=modelfname, type=str,
                        help='Store model as this name')
    parser.add_argument('-updatefname', default=updatefname, type=str,
                        help='Store update file as this name')
    args = parser.parse_args()

    return args

def main():
    args = arg_parse()
    opt = AttrDict({
        'host_string': args.host,
        'product_database': args.database,
        'product_collection': args.prod_collection,
        'datadir': args.datadir,
        'modelfname': args.modelfname,
        'updatefname': args.updatefname,
        'recom_collection': args.recom_collection
        })
    # download punkt tokenizer if necessary
    #nltk.download('punkt')
    
    model = W2Vmodel(opt.datadir,
                     opt.modelfname,
                     opt.host_string,
                     opt.product_database,
                     opt.product_collection,
                     opt.recom_collection)
    model.fetch_data_list(opt.updatefname)
    model.load_model()
    model.update_model(opt.updatefname)
    model.save_model()

if __name__ == '__main__':
    main()
