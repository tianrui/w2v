import gensim.models
import os
import numpy as np
import logging

def train(modelname='t8model',corpus_path='./data/'):
    sentences = gensim.models.word2vec.Text8Corpus(corpus_path + 'text8')
    bigram = gensim.models.Phrases(sentences)
    trigram = gensim.models.Phrases(bigram[sentences])
    print "Starting to train"
    model = gensim.models.word2vec.Word2Vec(trigram[sentences], min_count=5, size=1000)

    model.save(modelname)
    print "Finished modelling"

if __name__ == '__main__':
    train()

