import logging, gensim, nltk.data
import gensim.models as models
from data_utils import *

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
        # save empty model
        self.save_model(self.modelfname)
        return

    def construct_word_model(self, min_count=5, size=200, workers=1):
        sentence_list = load_data_sentences(self.datadir)
        self.model = models.Word2Vec(sentence_list[0], min_count=min_count, size=size, workers=workers)
        for sentencefile in sentence_list[1:]:
            self.model.train(sentencefile)
        return

    def save_model(self):
        self.model.save(self.modelfname)
        return

    def load_model(self):
        self.model = models.Word2Vec.load(self.modelfname)
        return

    def update_model(self, sentences):
        self.model.train(sentences)
        return

    def find_similar(self, target_tags, avoid_tags=[], topn=10):
        """
        Find the most similar n words in the vocabulary
        """
        product_list = fetch_product_list(self.host_string, self.product_database, self.product_collection)
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

    def load_data_sentences(self):
        """
        Load all sentences in files under dirname
        """
        sentence_list = []
        for fname in os.listdir(datadir):
            with open(os.path.join(datadir, fname)) as file:
                sentence_list.append(gensim.models.LineSentence(file))
        return sentence_list

    def train_dynamic(self):
        """
        Extract webpage information from each page,
        add as a batch of training data
        """
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
            product = AttrDict({'prodID': product_post['ID'],
                                 'tags': product_post['tag']})
            product_list.append(product)
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
                file.writelines(review_lines)
        file.close()

        return
