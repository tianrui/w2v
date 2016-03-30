from bson.objectid import ObjectId
import pymongo
import nltk

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
    def __init__(self, datadir, modelfname, host, database, recom_collection, product_collection):
        self.datadir = datadir
        self.modelfname = modelfname
        self.model = W2Vmodel(datadir, modelfname, host, database, product_collection, recom_collection)
        self.host_string = host
        self.database = database
        self.recom_collection = recom_collection
        self.product_collection = product_collection
        return
 
    def get_target_tags(self, rid):
        client = pymongo.MongoClient(self.host_string)
        db = client[self.database]
        recom_posts = db[self.recom_collection]
        post = recom_posts.find_one({"_id": rid})
        tags = post['receiverTags']
        return tags

    def inference(self, target_tags):
        """
        Inference from the model based on target tags
        target_tags: list of strings
        """
        #testmodel = W2Vmodel(self.datadir, self.modelfname,
        #self.host_string,
        #self.database,
        #self.product_collection,
        #self.recom_collection)
        #testmodel.load_model()
        #top_products = testmodel.find_similar(target_tags)
        self.model.load_model()
        top_products = self.model.find_similar(target_tags)

        return top_products

    def send_recommendation(self, recom, rid):
        """
        recom: list of productIDs of top 10 recommended gifts

        id: ObjectId of the recommendation to be updated, in string representation
        """
        client = pymongo.MongoClient(self.host_string)
        db = client[self.database]
        recom_posts = db[self.recom_collection]
        #post = recom_posts.find_one({'_id': rid})
        #print rid, recom
        #post['productID'] = recom
        result = recom_posts.update_one({'_id': rid}, {'$set': {'productID': recom}})

        #recom_posts.replace_one({'_id': rid}, post)

        return


