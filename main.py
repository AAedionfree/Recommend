from train import train
from predict import predict
from fermat import hnswIndex

def main():
    originText = train()
    topic = predict()
    index = hnswIndex()
    index.construction_index()
    index.save_index()
    labels, distances = index.query(topic, k=2)
    for i in range(len(labels)):
        print(originText[labels[i]])
        print(distances[i])
    return

if __name__ == "__main__":
    main()