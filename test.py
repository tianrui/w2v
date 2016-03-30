from bson.objectid import ObjectId
import pymongo
import argparse
import nltk
import attrdict
import scipy
import sys

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
    #host_string = 'mongodb://localhost:27017/'
    host_string = 'mongodb://heroku_73s67dx7:2d6hshk9a78f2dlfkachg486t7@ds011399.mlab.com:11399/heroku_73s67dx7'
    #database_string = 'test'
    database_string = 'heroku_73s67dx7'
    product_collection_string = 'products'
    recom_collection_string = 'recommendations'
    datadir = './data/'
    modelfname = './model'
    rid = '22'

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
    parser.add_argument('-recom_id', default=rid, type=str,
                        help='ID of recommendation')

    args = parser.parse_args()

    return args

def main():
    #host_string = 'mongodb://heroku_73s67dx7:2d6hshk9a78f2dlfkachg486t7@ds011399.mlab.com:11399/heroku_73s67dx7'
    ##database_string = 'test'
    #database_string = 'heroku_73s67dx7'
    #product_collection_string = 'products'
    #recom_collection_string = 'recommendations'
    #datadir = './data/'
    #modelfname = './model'
    #recom_id = int(sys.argv[2])
    #print recom_id

    args = arg_parse()
    opt = AttrDict({
        'host_string': args.host,
        'database': args.database,
        'product_collection': args.prod_collection,
        'datadir': args.datadir,
        'modelfname': args.modelfname,
        'recom_collection': args.recom_collection,
        'recom_id': int(args.recom_id)
        })
    
#    opt = AttrDict({
#        'host_string': host_string,
#        'database': database_string,
#        'product_collection': product_collection_string,
#        'datadir': datadir,
#        'modelfname': modelfname,
#        'recom_collection': recom_collection_string,
#        'recom_id': recom_id
#        })
    # hack for local call from node JS
    #opt.recom_id = sys.argv[2]

    recommendation = Recommendation(opt.datadir,
                     opt.modelfname,
                     opt.host_string,
                     opt.database,
                     opt.recom_collection,
                     opt.product_collection)
    target_tags = recommendation.get_target_tags(opt.recom_id)
    #print "User {0} has target tags: ".format(opt.recom_id) + "\n".join(target_tags)
    recommendation_list = recommendation.inference(target_tags)
    ID_list = []
    # list containing products and similarity matching scores
    print "Recommended the following gift IDs from database: \n"
    for product in recommendation_list:
        #pdb.set_trace()
        #print product, len(product), product[1]
        #print "ID: {0}, score: {1}".format(product[0]['prodID'], product[1])
        #print "Product tags: ", product[0]['tags']
        ID_list.append(product[0]['prodID'])

    recommendation.send_recommendation(ID_list, opt.recom_id)
    print("Updated recommendation in database")
    #sys.stdout.flush()
    return


if __name__ == '__main__':
    print("Starting script")
    #sys.stdout.flush()
    main()
