import logging, gensim, nltk.data
import gensim.models as models
from data_utils import *
import os
import pdb
class Sentences():
    def __init__(self, datadir):
        self.datadir = datadir

    def __iter__(self):
        dirname = self.datadir
        for fname in os.listdir(dirname):
            with open(os.path.join(dirname, fname)) as file:
                for line in open(os.path.join(self.dirname, fname)):
                    print line.split()
                    yield line.split()


class W2Vmodel():

    def __init__(self, datadir, modelfname,
            host_string, product_database, product_collection, recom_collection):
        self.datadir = datadir
        self.modelfname = modelfname
        self.model = models.Word2Vec()
        self.host_string = host_string
        self.product_database = product_database
        self.product_collection = product_collection
        self.recom_collection = recom_collection
        return

    def save_model(self):
        self.model.save(self.modelfname)
        print "Model saved."
        return

    def load_model(self):
        if os.path.isfile(self.modelfname):
            self.model = models.Word2Vec.load(self.modelfname)
            print "Model loaded."
        else:
            print "Model not found, could not be loaded."
        return

    def update_model(self, sentences):
        self.model.train(sentences)
        return

    def find_similar(self, target_tags, avoid_tags=[], topn=10):
        """
        Find the most similar n words in the vocabulary
        """
        product_list = self.fetch_product_list()
        top_products = []
        kk = 0
        for product in product_list:
            similarity = self.model.n_similarity(target_tags, product.tags)
            if (len(top_products) < topn):
                top_products.append((product, similarity))
            else:
                # Insert if similarity is higher than the top products
                if (similarity > top_products[-1][1]):
                    top_products.append((product, similarity))
                    top_products.sort(key=lambda item: item[1])
                    top_products.reverse()
        
        return top_products

    def construct_word_model(self, min_count=1, size=500, workers=1):
        sentence_list = self.load_data_sentences()
        sentence_list = sentence_tokenize(sentence_list[0][0])
        
        transformer = gensim.models.Phrases(sentence_list)
        self.model = models.Word2Vec(sorted_vocab=1, min_count=min_count, size=size, workers=workers, iter=10, window=10)
        self.model.scan_vocab(transformer[sentence_list])
        self.model.build_vocab(transformer[sentence_list])
        self.model.train(transformer[sentence_list])

        print('Finished training')
        #for fname in os.listdir(self.datadir):
        #    with open(os.path.join(datadir, fname)) as file:
        #        for line in file:
        #            self.model.train(line)
        return

    def load_data_sentences(self):
        """
        Load all sentences in files under dirname
        """
        sentence_list = []
        for fname in os.listdir(self.datadir):
            with open(os.path.join(self.datadir, fname)) as file:
                for line in file:
                    sentence_list.append([line])
        return sentence_list

    def train_dynamic(self):
        """
        Extract webpage information from each page,
        add as a batch of training data
        """
        self.save_model()

        return

    def fetch_product_list(self):
        """
        Fetch list of all products in model's collection
        """
        product_list = []
        client = MongoClient(self.host_string)
        db = client[self.product_database]
        product_posts = db[self.product_collection]

        for product_post in product_posts.find():
            if 'ID' in product_post:
                tag_list = []
                for tag in product_post['tag']:
                    split_tag = tag.split('&')
                    if len(split_tag) > 1:
                        for split in split_tag:
                            tag_list.append(split.strip().replace(' ', '_').lower())
                    else:
                        tag_list.append(tag.replace(' ', '_').lower())
                product = AttrDict({'prodID': product_post['ID'],
                                     'tags': tag_list})
                product_list.append(product)
                #print product_post, product
                #raw_input('stop')
        return product_list

    def fetch_review(self, id):
        """
        Fetch all reviews of product ID in model's collection
        """
        review_list = []
        client = MongoClient(self.host_string)
        db = client[self.product_database]
        product_posts = db[self.product_collection]

        post = product_posts.find_one({'_id': ObjectId(id)})
        review_list.extend(post['review'])
        return review_list

    def fetch_review_list(self):
        """
        Fetch list of all reviews in model's collection
        """
        review_list = []
        client = MongoClient(self.host_string)
        db = client[self.product_database]
        product_posts = db[self.product_collection]

        for product_post in product_posts.find():
            review_list.extend(product_post['review'])
        return review_list


    def fetch_data_list(self):
        """
        Fetch data from all recommendations, store in data directory
        """
        review_list = self.fetch_review_list()
        with open(self.datadir + 'recommendation_data.txt', 'w') as file:
            for review in review_list:
                review_lines = sentence_tokenize(review)
                #pdb.set_trace()
                line_sentence = []
                for line in review_lines:
                    line_sentence.extend(line.encode('ascii', 'ignore').split('\n'))
                #print review
                #print review_lines
                print line_sentence
                file.writelines(line_sentence)
        file.close()

        raw_input('stop')
        return
