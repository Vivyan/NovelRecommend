#coding=utf-8


# import warnings
# warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import logging
from gensim import corpora, models, similarities

datapath = 'D:/hellowxc/python/testres0519.txt'
querypath = 'D:/hellowxc/python/queryres0519.txt'
storepath = 'D:/hellowxc/python/store0519.txt'
def similarity(datapath, querypath, storepath):
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    class MyCorpus(object):
        def __iter__(self):
            for line in open(datapath):
                yield line.split()

    Corp = MyCorpus()
    dictionary = corpora.Dictionary(Corp)
    corpus = [dictionary.doc2bow(text) for text in Corp]

    tfidf = models.TfidfModel(corpus)

    corpus_tfidf = tfidf[corpus]

    q_file = open(querypath, 'r')
    query = q_file.readline()
    q_file.close()
    vec_bow = dictionary.doc2bow(query.split())
    vec_tfidf = tfidf[vec_bow]

    index = similarities.MatrixSimilarity(corpus_tfidf)
    sims = index[vec_tfidf]

    similarity = list(sims)

    sim_file = open(storepath, 'w')
    for i in similarity:
        sim_file.write(str(i)+'\n')
    sim_file.close()
similarity(datapath, querypath, storepath)
