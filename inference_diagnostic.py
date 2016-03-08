from tagmodel import *
from data_utils import *
import os

def main():
    host_string = 'mongodb://localhost:27017/'
    database_string = 'test'
    product_collection_string = 'Product'
    recom_collection_string = 'Recommendation'
    datadir = './data/'
    modelfname = './t8model'

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
