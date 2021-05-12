import sys
import numpy as np
import pandas as pd

from data.fileIndex import expDataFileName

class splitFIleReader():
    def __init__(self, path, filename, splitArr, splitCount, row = ""):
        self.file_map = {}
        self.path = path
        self.filename = filename
        self.split_arr = splitArr
        self.split_count = splitCount
        self.row = row


    def fileName2Index(self, filenamme):
        n = len(filenamme)
        charIndex = filenamme[n-2:n]
        ans = 0
        for ch in charIndex:
            ascii_value = ord(ch)
            ans += ans * 26 + ascii_value - ord('a')
        return ans

    def Index2FileName(self, index):
        base = "aa"
        ans = ""
        for ch in base:
            ascii_value = ord(ch)
            ascii_value += index // 26
            ans += str(chr(ascii_value))
            index //= 26
        return self.filename + ans

    def load(self, fileName):
        absPath = self.path + fileName
        print('load path is ' + absPath)
        if fileName not in self.split_arr:
            print('fileName ' + fileName + ' not in arr')
            sys.exit()
        if fileName not in self.file_map:
            if self.row == "":
                self.file_map[fileName] = np.array(pd.read_csv(absPath))
            else:
                self.file_map[fileName] = np.array(pd.read_csv(absPath)[self.row])
        return self.file_map[fileName]

    def get(self, index):
        real_index = index - 1 # delete header
        fileNameIndex = real_index // self.split_count
        offest = real_index % self.split_count
        print(fileNameIndex, offest)
        if fileNameIndex >= len(self.split_arr):
            print('fileNameIndex ' + str(fileNameIndex) + ' outbound ' + str(len(self.split_arr)))
        fileName = self.Index2FileName(fileNameIndex)
        fileHandler = self.load(fileName)
        return fileHandler[offest]

if __name__ == '__main__':
    fileReader = splitFIleReader("/Users/aaedion/workspace/design/data/company/", "exp_", expDataFileName, 100000)
    print(fileReader.get(85144))