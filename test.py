from bson.objectid import ObjectId
import pymongo
import argparse

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

class Recommendation():
    def __init__(self, datadir, modelfname, host, database, recom_collection):
        self.datadir = datadir
        self.modelfname = modelfname
        self.model = models.Word2Vec()
        self.host_string = host_string
        self.database = database
        self.recom_collection = recom_collection
        return
 
    def get_target_tags(self, id):
        client = pymongo.MongoClient(self.host_string)
        db = client[self.database]
        recom_posts = db[self.recom_collection]
        post = recom_posts.find_one({'_id': ObjectId(id)})

        tags = post['receiverTags']
        return tags

    def inference(self, target_tags):
        testmodel = W2Vmodel(self.datadir, self.modelfname)
        top_products = testmodel.find_similar(target_tags)

        return top_products

    def send_recommendation(self, recom, id):
        client = pymongo.MongoClient(self.host_string)
        db = client[self.database]
        recom_posts = db[self.recom_collection]
        post = recom_posts.find_one({'_id': ObjectId(id)})

        post['productName'] = recom
        recom_posts.replace_one({'_id': ObjectId(id)}, post)

        return



def arg_parse():
    """Parse input args"""
    host_string = 'mongodb://localhost/'
    product_database_string = 'test'
    product_collection_string = 'Product'
    recom_collection_string = 'Recommendation'
    datadir = './data/'
    modelfname = './model'
    id = '0'

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
    parser.add_argument('-recom_id', default=id, type=String,
                        help='ID of recommendation')

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
        'recom_collection': args.recom_collection_string,
        'recom_id': args.recom_id
        }

    model = W2Vmodel(opt.datadir,
                     opt.modelfname,
                     opt.host_string,
                     opt.product_database,
                     opt.product_collection,
                     opt.recom_collection)

if __name__ == '__main__':
    main()
