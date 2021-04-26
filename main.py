from train import train
from predict import btmPredictor
from fermat import hnswIndex


def main():
    originText = train()
    predictor = btmPredictor()
    topic = predictor.predict()
    index = hnswIndex()
    labels, distances = index.query(topic, k=2)
    for i in range(len(labels)):
        print(originText[labels[i]])
        print(distances[i])
    return

if __name__ == "__main__":
    main()