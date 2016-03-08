from bson.objectid import ObjectId
import pymongo
import argparse
import nltk
import attrdict

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
    database_string = 'test'
    product_collection_string = 'Product'
    recom_collection_string = 'Recommendation'
    datadir = './data/'
    modelfname = './model'
    id = '0'

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
    parser.add_argument('-recom_id', default=id, type=str,
                        help='ID of recommendation')

    args = parser.parse_args()

    return args

def main():
    args = arg_parse()
    opt = AttrDict({
        'host_string': args.host,
        'database': args.database,
        'product_collection': args.prod_collection,
        'datadir': args.datadir,
        'modelfname': args.modelfname,
        'recom_collection': args.recom_collection,
        'recom_id': args.recom_id
        })
    
    recommendation = Recommendation(opt.datadir,
                     opt.modelfname,
                     opt.host_string,
                     opt.database,
                     opt.recom_collection)

    target_tags = recommendation.get_target_tags(opt.recom_id)
    print "User {0} has target tags: ".format(self.opt.recom_id) + target_tags

    recommendation_list = recommendation.inference(target_tags)
    ID_list = []
# list containing products and similarity matching scores
    print "Recommended the following gift IDs from database: \n"
    for product in recommendation_list:
        print "ID: {0}, score: {0}".format(product[0]['prodID'], product[1])
        ID_list.append(product[0]['prodID'])

    recommendation.send_recommendation(ID_list, self.opt.recom_id)
    print "Updated recommendation in database"


if __name__ == '__main__':
    main()
