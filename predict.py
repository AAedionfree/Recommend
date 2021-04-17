import json

import numpy as np
from Biterm.btmModel import oBTM
from sklearn.feature_extraction.text import CountVectorizer
from Biterm.utility import vec_to_biterms, topic_summuary

from train import phi_wz_path, vocabulary_path, theta_z_path
from fermat import hnswIndex

class btmPredictor():
    def __init__(self):
        self.btm, self.vocabulary = self._predict_init()

    def _predict_init(self):
        # load vocabulary
        vocabularyJson = json.load(open(vocabulary_path, "r"))
        vec = CountVectorizer(vocabulary=vocabularyJson, decode_error='replace')
        print("vocabulary size " + str(len(vocabularyJson)))
        # load btm Model
        btm = oBTM(num_topics=20, V=np.array(vec.get_feature_names()), theta_z_path=theta_z_path, phi_wz_path=phi_wz_path)
        return btm, vec

    def predict(self, testData):
        newX = self.vocabulary.transform(testData).toarray()
        newBiterms = vec_to_biterms(newX)
        return self.btm.transform(newBiterms)


if __name__ == '__main__':
    btmPredictor = btmPredictor()
    topics = btmPredictor.predict(["健康 体检 健康检查 研究所 北京市"])
    index = hnswIndex(load=True)
    print(index.query(topics, 2))