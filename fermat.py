import hnswlib
import numpy as np
import pickle

from train import P_zd_path

index_path = "save/hnsw.bin"

class hnswIndex():
    def __init__(self, load=False):
        if load == True:
            self.p = hnswlib.Index(space = 'l2', dim = 20)
            self.p.load_index(index_path)
        else:
            self.data = np.load(P_zd_path)
            self.num_elements = self.data.shape[0]
            self.dim = self.data.shape[1]
            self.data_labels = np.arange(self.data.shape[0])
            self._construction_index()

    def _construction_index(self):
        # Declaring index
        p = hnswlib.Index(space = 'l2', dim = self.dim) # possible options are l2, cosine or ip
        # Initializing index - the maximum number of elements should be known beforehand
        p.init_index(max_elements = self.num_elements, ef_construction = 200, M = 16)

        # Element insertion (can be called several times):
        p.add_items(self.data, self.data_labels)

        # Controlling the recall by setting ef:
        p.set_ef(150000) # ef should always be > k

        self.p = p

        # Index objects support pickling
        # WARNING: serialization via pickle.dumps(p) or p.__getstate__() is NOT thread-safe with p.add_items method!
        # Note: ef parameter is included in serialization; random number generator is initialized with random_seed on Index load
        p_copy = pickle.loads(pickle.dumps(p))  # creates a copy of index p using pickle round-trip

        ### Index parameters are exposed as class properties:
        print(f"Parameters passed to constructor:  space={p_copy.space}, dim={p_copy.dim}")
        print(f"Index construction: M={p_copy.M}, ef_construction={p_copy.ef_construction}")
        print(f"Index size is {p_copy.element_count} and index capacity is {p_copy.max_elements}")
        print(f"Search speed/quality trade-off parameter: ef={p_copy.ef}")

        self._save_index()

    def query(self, data, k):
        # Query dataset, k - number of closest elements (returns 2 numpy arrays)
        labels, distances = self.p.knn_query(data, k = k)
        print(labels, distances)
        return labels[0], distances[0]

    def _save_index(self):
        self.p.save_index(index_path)

if __name__ == '__main__':
    index = hnswIndex()