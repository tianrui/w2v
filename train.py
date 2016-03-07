from bson.objectid import ObjectId
import pymongo
import argparse
import nltk
from recommendation import *
from tagmodel import *
from data_utils import *
# get receiverTags from recommendation schema based on _id
# modify product, productName in recommendation schema
# Recommendation schema
# sender: {type: Number, ref: 'User'},
#    receiver: String,
#        receiverTags: [String],
#            //product: {type: Number, ref: 'Product'},
#                productName: String,
#                    rating: Number,
#                        date: String

def arg_parse():
    """Parse input args"""
    host_string = 'mongodb://localhost/'
    product_database_string = 'test'
    product_collection_string = 'Product'
    recom_collection_string = 'Recommendation'
    datadir = './data/'
    modelfname = './model'

    parser = argparse.ArgumentParser(description='Training word2vec model with Amazon database')
    parser.add_argument('-host', default=host_string, type=String,
                        help='Mongo DB client host')
    parser.add_argument('-database', default=database_string, type=String,
                        help='Mongo DB database')
    parser.add_argument('-prod_collection', default=product_collection_string, type=String,
                        help='MongoDB Collection of products')
    parser.add_argument('-recom_collection', default=recom_collection_string, type=String,
                        help='MongoDB Collection of recommendations')
    parser.add_argument('-datadir', default=datadir, type=String,
                        help='Directory for storing training data')
    parser.add_argument('-modelfname', default=modelfname, type=String,
                        help='Store model as this name')
    args = parser.parse_args()

    return args

def main():
    args = arg_parse()
    opt = {
        'host_string': args.host,
        'product_database': args.database,
        'product_collection': args.product_collection_string,
        'datadir': args.datadir,
        'modelfname': args.modelfname,
        'recom_collection': args.recom_collection_string
        }
    # download punkt tokenizer if necessary
    nltk.download('punkt')
    
    model = W2Vmodel(opt.datadir,
                     opt.modelfname,
                     opt.host_string,
                     opt.product_database,
                     opt.recom_collection)
    model.load_model()
    model.construct_word_model()
    model.save_model()

if __name__ == '__main__':
    main()