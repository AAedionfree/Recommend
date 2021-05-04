import os
import json

import numpy as np
from Biterm.btmModel import oBTM
from sklearn.feature_extraction.text import CountVectorizer
from Biterm.utility import vec_to_biterms, topic_summuary
from gensim.models import Doc2Vec

from train import phi_wz_path, vocabulary_path, theta_z_path
from fermat import hnswIndex, index_path
from train import company_doc2vec_path, bidding_doc2vec_Path

def path(file_path):
    current_path = os.path.abspath(__file__)
    father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
    config_file_path = os.path.join(father_path, file_path)
    return config_file_path


class doc2vecPredictor():
    def __init__(self, doc2vec_Path):
        self.doc2vec_Path = path(doc2vec_Path)
        self.model = self.__predict__init()

    def __predict__init(self):
        return Doc2Vec.load(self.doc2vec_Path)

    def predict(self, testData, k):
        text = testData.split(' ')
        infer = self.model.infer_vector(doc_words=text, steps=500, alpha=0.005)
        most_similar = self.model.dv.most_similar([infer], topn=k)
        return most_similar


class btmPredictor():
    def __init__(self):
        self.btm, self.vocabulary = self._predict_init()
        self.index = hnswIndex(load=True, index_path=path(index_path))

    def _predict_init(self):
        # load vocabulary
        vocabularyJson = json.load(open(path(vocabulary_path), "r"))
        vec = CountVectorizer(vocabulary=vocabularyJson, decode_error='replace')
        print("vocabulary size " + str(len(vocabularyJson)))
        # load btm Model
        btm = oBTM(num_topics=20, V=np.array(vec.get_feature_names()), theta_z_path=path(theta_z_path), phi_wz_path=path(phi_wz_path))
        return btm, vec

    def predict(self, testData):
        newX = self.vocabulary.transform(testData).toarray()
        newBiterms = vec_to_biterms(newX)
        return self.btm.transform(newBiterms)


if __name__ == '__main__':
    Test = "doc2vec"
    testData = "修缮 工程"
    topk = 10
    if Test == "btm":
        btmPredictor = btmPredictor()
        topics = btmPredictor.predict([testData])
        print(topics)
        index = hnswIndex(load=True)
        print(index.query(topics, topk))
        zd = np.load("save/P_zd.npy")
        print(zd[1])
    if Test == "doc2vec":
        doc2vecPredictor = doc2vecPredictor(bidding_doc2vec_Path)
        most_similar = doc2vecPredictor.predict(testData, topk)
        for item in most_similar:
            print(item[0])
            print(item[1])