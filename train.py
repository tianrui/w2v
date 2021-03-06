from bson.objectid import ObjectId
import pymongo
import argparse
import nltk
import scipy
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
    #host_string = 'mongodb://localhost:27017'
    host_string = 'mongodb://011399.mlab.com:11399'
    #database_string = 'test'
    database_string = 'heroku_73s67dx7'
    product_collection_string = 'products'
    recom_collection_string = 'recommendations'
    datadir = './data/'
    modelfname = './model'

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
    args = parser.parse_args()

    return args

def train(modelname='model',corpus_path='./data/'):
    sentences = gensim.models.word2vec.Text8Corpus(corpus_path + 'text8')
    bigram = gensim.models.Phrases(sentences)
    trigram = gensim.models.Phrases(bigram[sentences])
    print "Starting to train"
    model = gensim.models.word2vec.Word2Vec(trigram[sentences], min_count=5, size=1000)

    model.save(modelname)
    print "Finished modelling"
    return

def main():
    args = arg_parse()
    opt = AttrDict({
        'host_string': args.host,
        'product_database': args.database,
        'product_collection': args.prod_collection,
        'datadir': args.datadir,
        'modelfname': args.modelfname,
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
    #model.fetch_data_list()
    model.load_model()
    train(modelname=opt.modelfname, corpus_path=opt.datadir)
    #model.construct_word_model()
    model.save_model()

if __name__ == '__main__':
    main()
