from tagmodel import *
from data_utils import *
import os

def main():
    #host_string = 'mongodb://localhost:27017'
    host_string = 'mongodb://heroku_73s67dx7:2d6hshk9a78f2dlfkachg486t7@ds011399.mlab.com:11399/heroku_73s67dx7'
    #database_string = 'test'
    database_string = 'heroku_73s67dx7'
    product_collection_string = 'products'
    recom_collection_string = 'recommendations'
    datadir = './data/'
    modelfname = './t8model'

    # try on client
    print "Testing client"
    client = MongoClient(host_string)
    db = client[database_string]
    recom = db['recommendations']
    print recom
    print recom.find_one()
    print "Accessed client"

    target_tags = ['games', 'sports']
    model = W2Vmodel(datadir,
                     modelfname,
                     host_string,
                     database_string,
                     product_collection_string,
                     recom_collection_string)

    model.load_model()
    #print model.model.vocab

    #raw_input('stop')
    res = model.find_similar(target_tags)
    print "Target tags: ", target_tags
    print "Returned products:"
    for prod in res:
        print prod, '\n'
    return

if __name__ == '__main__':
    main()
