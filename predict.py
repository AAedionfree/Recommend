import json

from Biterm.btmModel import oBTM
from sklearn.feature_extraction.text import CountVectorizer
from Biterm.utility import vec_to_biterms, topic_summuary

from train import phi_wz_path, vocabulary_path, theta_z_path

def predictLoad():
    # load vocabulary
    vocabularyJson = json.load(open(vocabulary_path))
    vocabulary = CountVectorizer(vocabulary=vocabularyJson)
    # load btm Model
    btm = oBTM(num_topics=20, V=vocabulary, theta_z_path=theta_z_path, phi_wz_path=phi_wz_path)
    return btm, vocabulary

def _predict(testData, btm, vec):
    newX = vec.transform(testData).toarray()
    newBiterms = vec_to_biterms(newX)
    newtopics = btm.transform(newBiterms)
    return newtopics

def predict(test=["工程 局 全国 工程施工 监理 研究院 采购"]):
    btm, vocabulary = predictLoad()
    topic = _predict(test, btm, vocabulary)
    print(topic)
    return topic

if __name__ == '__main__':
    predict(test=["工程 局 全国 工程施工 监理 研究院 采购"])