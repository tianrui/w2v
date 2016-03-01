import logging, gensim
import gensim.models as models
from data_utils import *

class W2Vmodel():

    def __init__(self, datadir, modelfname):
        self.datadir = datadir
        self.modelfname = modelfname
        self.model = models.Word2Vec()
        return

    def construct_model(self, min_count=5, size=200, workers=1):
        sentence_list = load_data_sentences(self.datadir)
        self.model = models.Word2Vec(sentence_list[0], min_count=min_count, size=size, workers=workers)
        for sentencefile in sentence_list[1:]:
            self.model.train(sentencefile)
        return

    def save_model(self):
        self.model.save(self.modelfname)
        return

    def update_model(self, sentences):
        self.model.train(sentences)
        return

    def find_similar(self, target_tags, avoid_tags=[], topn=10):
        """
        Find the most similar n words in the vocabulary
        """
        product_list = get_product_list()
        top_products = []
        kk = 0
        for product in product_list:
            similarity = self.model.n_similarity(target_tags, product.tags)
            if (len(top_products) < topn):
                top_products.append((product, similarity))
            else:
                # Insert if similarity is higher than the top products
                if (similarity > top_products[-1][1]):
                    top_products.remove(top_products[-1])
                    top_products.append((product, similarity))
                    top_products.sort(key=lambda item: item[1])
                    top_products.reverse()
        
        return top_products

    def construct_text8(self):
        self.model = models.word2vec.Text8Corpus(self.modelfname)
        return

    def get_product_list(self):
        return
