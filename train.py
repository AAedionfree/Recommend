import json

import pandas as pd
import numpy as np
import pyLDAvis
import gensim
from gensim.models import Doc2Vec

from Biterm.btmModel import oBTM
from sklearn.feature_extraction.text import CountVectorizer
from Biterm.utility import vec_to_biterms, topic_summuary

vocabulary_path = "save/vocabulary.json"
theta_z_path = "save/theta_z.npy"
phi_wz_path = "save/phi_wz.npy"
P_zd_path = "save/P_zd.npy"
doc2vec_Path = "save/doc2vec.bin"
num_topics=20
iterations=150

def loadText(Path="./data.csv"):
    file = pd.read_csv(Path, nrows=100000)
    return np.array(file["关键词"])

def doc2vecLoadTrain():
    texts = loadText()
    X_train = []
    TaggedDocument = gensim.models.doc2vec.TaggedDocument
    for i, item in enumerate(texts):
        word_list = item.split(' ')
        for j, word in enumerate(word_list):
            word_list[j] = word.strip()
        document = TaggedDocument(word_list, tags=[i])
        X_train.append(document)
    return X_train

def doc2vecTrain():
    X_train = doc2vecLoadTrain()
    doc2vec=Doc2Vec(X_train, min_count=10, alpha=0.001, window=3)
    doc2vec.train(X_train, total_examples=doc2vec.corpus_count, epochs=100)
    doc2vec.save(doc2vec_Path)


def btmTrain():
    texts = loadText()
    vec = CountVectorizer(dtype=np.uint8, token_pattern='\w+')
    X = vec.fit_transform(texts).toarray()
    json.dump(vec.vocabulary_, open(vocabulary_path, 'w'))
    print("vocabulary_ size is " + str(len(vec.vocabulary_)))
    vocab = np.array(vec.get_feature_names())
    biterms = vec_to_biterms(X)

    btm = oBTM(num_topics=num_topics, V=vocab)
    print("\n\n Train Online BTM ..")
    for i in range(0, len(biterms), 100):  # prozess chunk of 200 texts
        biterms_chunk = biterms[i:i + 100]
        btm.fit(biterms_chunk, iterations=iterations)
    topics = btm.transform(biterms)

    print("\n\n Visualize Topics ..")
    vis = pyLDAvis.prepare(btm.phi_wz.T, topics, np.count_nonzero(X, axis=1), vocab, np.sum(X, axis=0))
    pyLDAvis.save_html(vis, './vis/online_btm.html')

    print("\n\n Topic coherence ..")
    topic_summuary(btm.phi_wz.T, X, vocab, 10)

    print("\n\n Texts & Topics ..")
    for i in range(len(texts)):
        print("{} (topic: {})".format(texts[i], topics[i].argmax()))

    # btm.save(theta_z_path, phi_wz_path, P_zd_path)

    return texts

if __name__=="__main__":
    doc2vecTrain()




