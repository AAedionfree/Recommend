#coding=utf-8
from biddingInfo import biddingInfo
from data import fileIndex

import json
import re

import pandas as pd
import jieba

debug = True

bidingDataPath = "data/bidding/"
bidingDataFileName = fileIndex.bidingDataFileName[0:20]

def Print(string):
    if debug == True:
        print(string)

def load_data(path):
    data = []
    f = open(path)
    line = f.readline()
    while line:
        data.append(line)
        line = f.readline()
    Print(len(data))
    return data

def filter(data):
    json_data = []
    filter_data = []
    pattern = re.compile(r'[^\u4e00-\u9fa5]+')
    for string in data:
        Print(string)
        json_start = string.find("{")
        json_end = string.find("}")
        json_string = string[json_start:json_end+1]
        json_data.append(json_string)
        filter_string = re.sub(pattern, '\n', string.replace(json_string, ""))
        filter_data.append(filter_string)
    return filter_data, json_data

def toBiddingInfo(filter_data, json_data, path):
    biddingInfos = []
    for i in range(len(filter_data)):
        Print("\n第" + str(i) + "条")
        json_string = json_data[i].replace("\\*", "")
        filter_string = filter_data[i]
        # keywords
        if json_string != "":
            try:
                map = json.loads(json_string, encoding="GB2312")
            except:
                continue
            key_string = ""
            if "关键信息:" in map:
                key_string = " ".join(jieba.cut(map["关键信息:"].replace(",", "")))
            if "招标单位:" in map:
                location = ""
                for word in jieba.cut(map["招标单位:"]):
                    location = word
                key_string += " " + location
            # classes proj_name company
            filter_arr = filter_string.split("\n")
            classes = filter_arr[1].replace(r"[^\u4e00-\u9fa5]+", "")
            project_name = filter_arr[3]
            company = ""
            if classes == "招标公告":
                if "招标单位:" in map and map["招标单位:"] != "":
                    company = map["招标单位:"]
                else:
                    for item in filter_arr:
                        if "项目业主为" in item:
                            company = item.replace("项目业主为", "")
            elif classes == "中标公告":
                if "中标单位:" in map and map["中标单位:"] != "":
                    company = map["中标单位:"]
            else:
                Print("ERROR: unknow classes")

            if classes != "" and company != "" and project_name != "":
                info = {}
                info['class'] = classes
                info['name'] = project_name
                info['company'] = company
                info['keywords'] = key_string
                info['path'] = path
                info['index'] = i
                bidding = biddingInfo.biddingInfo(info)
                bidding.print_data()
                biddingInfos.append(bidding)
            else:
                Print("classes:" + classes)
                Print("company:" + company)
                Print("project_name:" + project_name)
                Print("filter this sentence")
    return biddingInfos


if __name__ == '__main__':
    columns = ["类别", "公司名称", "项目名字", "关键词", "文件路径", "下标位置"]
    for i in range(len(bidingDataFileName)):
        path = bidingDataPath + bidingDataFileName[i]
        data = load_data(path)
        filter_data, json_data = filter(data)
        biddingInfos = toBiddingInfo(filter_data, json_data, path)
        res = [info.toList() for info in biddingInfos]
        df = pd.DataFrame(res, columns = columns)
        if i == 0:
            df.to_csv("data.csv", index=False, encoding='utf_8_sig', mode='a')
        else:
            df.to_csv("data.csv", index=False, encoding='utf_8_sig', mode='a', header=False)
    Print("\n预处理结束")
    Print("biddingInfos:" + str(len(biddingInfos)))
