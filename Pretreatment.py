#coding=utf-8
from Info import biddingInfo, companyInfo
from data import fileIndex

import json
import re

import pandas as pd
import jieba

debug = False

bidingDataPath = "data/bidding/"
bidingDataFileName = fileIndex.bidingDataFileName

companyDataPath = "data/company/"
companyDataFileName = fileIndex.companyDataFileName

stopWord = ["（", "）", "、", "，", ".", "。", "]", "[", "【", "】"]

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
    f.close()
    Print(len(data))
    return data

def deletePartString(string):
    for stopword in stopWord:
        string = string.replace(stopword, "")
    return string

def filter(data):
    json_data = []
    filter_data = []
    pattern = re.compile(r'[^\u4e00-\u9fa5]+')
    for string in data:
        string = deletePartString(string)
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
                key_string = " ".join(jieba.cut(map["关键信息:"].replace(",", ""))).strip()
            if "招标单位:" in map:
                location = ""
                for word in jieba.cut(map["招标单位:"]):
                    location = word
                key_string += " " + location.strip()
            key_string = key_string.strip()
            # classes proj_name company
            filter_arr = filter_string.split("\n")
            if len(filter_arr) <= 3:
                continue
            classes = filter_arr[1].replace(r"[^\u4e00-\u9fa5]+", "").strip()
            location = filter_arr[2].replace(r"[^\u4e00-\u9fa5]+", "").strip()
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

            if location == "":
                location = "null"
            else:
                key_string += " " + location

            if classes != "" and company != ""\
                    and len(key_string.strip().split(" ")) >= 4 and len(project_name) >= 8:
                info = {}
                info['class'] = classes
                info['location'] = location
                info['name'] = project_name
                info['company'] = company
                info['keywords'] = key_string
                info['path'] = path
                info['index'] = i
                bidding = biddingInfo.biddingInfo(info)
                bidding.print_data(debug)
                biddingInfos.append(bidding)
            else:
                Print("classes:" + classes)
                Print("company:" + company)
                Print("project_name:" + project_name)
                Print("filter this sentence")
    return biddingInfos

def preBidding():
    columns = ["类别", "公司名称", "公司位置", "项目名字", "关键词", "文件路径", "下标位置"]
    for i in range(len(bidingDataFileName)):
        path = bidingDataPath + bidingDataFileName[i]
        data = load_data(path)
        filter_data, json_data = filter(data)
        biddingInfos = toBiddingInfo(filter_data, json_data, path)
        res = [info.toList() for info in biddingInfos]
        df = pd.DataFrame(res, columns=columns)
        if i == 0:
            df.to_csv("data.csv", index=False, encoding='utf_8_sig', mode='a')
        else:
            df.to_csv("data.csv", index=False, encoding='utf_8_sig', mode='a', header=False)
        print(str(i+1) + "/" + str(len(bidingDataFileName)) + " " + path + " " + "biddingInfos:" + str(len(biddingInfos)))
    Print("\n预处理结束")

def preCompany():
    columns = ["公司名称", "经营范围", "公司类型", "公司位置", "文件路径", "下标位置"]
    pattern = re.compile(r'[^\u4e00-\u9fa5]+')
    for i in range(len(companyDataFileName)):
        path = companyDataPath + companyDataFileName[i]
        data = load_data(path)
        companyInfos = []
        for j, item in enumerate(data):
            splits = item.split("^")
            if len(splits) == 34:
                companyRange =  " ".join(jieba.cut(re.sub(pattern, '', splits[13]))).strip()
                if len(companyRange) >= 10:
                    info = {}
                    info['range'] = companyRange
                    info['name'] = splits[2]
                    info['class'] = splits[8]
                    info['location'] = splits[9]
                    info['path'] = companyDataFileName[i]
                    info['index'] = j
                    company_info = companyInfo.companyInfo(info)
                    company_info.print_data(debug=True)
                    companyInfos.append(company_info.toList())
        df = pd.DataFrame(companyInfos, columns=columns)
        if i == 0:
            df.to_csv("companyData.csv", index=False, encoding='utf_8_sig', mode='a')
        else:
            df.to_csv("companyData.csv", index=False, encoding='utf_8_sig', mode='a', header=False)
        print(str(i+1) + "/" + str(len(companyDataFileName)) + " " + path + " " + "companyInfos:" + str(len(companyInfos)))

if __name__ == '__main__':
    # preBidding()
    preCompany()

