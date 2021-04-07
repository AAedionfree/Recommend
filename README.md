# bistu graduation project
## Src
Pretreatment.py: rawData => data.csv 

data.csv header:["类别", "公司名称", "公司位置", "项目名字", "关键词", "文件路径", "下标位置"]

train.py: load data.csv tarin biterm topic model and store it as *.npy

predict: testSentence => P(topic|testSentence)

fermat: P(topic|trainSentences) => construct hnsw index && P(topic|testSentence) => topK similar trainSentence

main.py: all steps

## folder
### Biterm
####[biterm topic model](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.402.4032&rep=rep1&type=pdf)
This model is accurate in short text classification. It explicitly models the word co-occurrence patterns in the whole corpus to solve the problem of sparse word co-occurrence at document-level. (implementation with python)

### hnswlib
#### [hnsw](https://github.com/nmslib/hnswlib)
Fast approximate nearest neighbor search (python bidding)

### bidding info
Origin bidding data

### save
Stores P(z|d), wz, theta as .npy
Stores vocabulary as vocabulary.json

### data
bidding: split files
fileIndex.py: stores list of file name

### log
python xxxx.py >> xxxx.log

### utility
.sh file
