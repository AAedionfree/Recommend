#coding=utf-8
from biddingInfo import biddingInfo

import json
import re
import demjson
import warnings

import jieba

debug = True

bidingDataPath = "data/bidding/"
bidingDataFileName = [
    "t_model_head100.txt"
]

def Print(string):
    if debug == True:
        print(string)

def load_data():
    data = []
    for file_name in bidingDataFileName:
        path = bidingDataPath + file_name
        f = open(path)
        line = f.readline()
        while line:
            data.append(line)
            line = f.readline()
    print(len(data))
    return data

def filter(data):
    json_data = []
    filter_data = []
    pattern = re.compile(r'[^\u4e00-\u9fa5]+')
    for string in data:
        print(string)
        json_start = string.find("{")
        json_end = string.find("}")
        json_string = string[json_start:json_end+1]
        json_data.append(json_string)
        filter_string = re.sub(pattern, '\n', string.replace(json_string, ""))
        filter_data.append(filter_string)
    return filter_data, json_data

def toBiddingInfo(filter_data, json_data):
    biddingInfos = []
    for i in range(len(filter_data)):
        print("第" + str(i) + "条")
        json_string = json_data[i]
        filter_string = filter_data[i]
        print(json_string)
        # keywords
        map = json.loads(json_string, encoding="GB2312")
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
            print("ERROR: unknow classes")

        info = {}
        info['class'] = classes
        info['name'] = project_name
        info['company'] = company
        info['keywords'] = key_string
        if classes != "" and company != "" and project_name != "":
            bidding = biddingInfo.biddingInfo(info)
            bidding.print_data()
            biddingInfos.append(bidding)
        else:
            print("classes:" + classes)
            print("company:" + company)
            print("project_name:" + project_name)
            print("filter this sentence")



# def data2Map(data):
#     info = []
#     for item in data:
#         if item[0] == "招标公告" or item[0] == "投标公告":
#             info.append(item2Application(item))
#         else:
#             print("unknow kind of data " + item[0])
#             continue
#
# def map2Application(map):
#     return
#
# def item2Map(info):
#     def loadList(info, start, end):
#         start_flag = 0
#         res = []
#         for string in info:
#             if string == start and start_flag == 0:
#                 start_flag = 1
#                 continue
#             if start_flag == 1 and string != end:
#                 res.append(string)
#                 continue
#             if start_flag == 1 and string == end:
#                 break
#         return res
#     map = {}
#     map["class"] = info[0]
#     map["name"] = loadList(info, info[0], "中标金额")
#     # map["company"] =
#
#
#
# def item2Application(info):
#     return map2Application(item2Map(info))


if __name__ == '__main__':
    data = load_data()
    filter_data, json_data = filter(data)
    toBiddingInfo(filter_data, json_data)
    print("end")