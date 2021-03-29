class biddingInfo:
    def __init__(self, info):
        self.classes = info['class']            # 类别
        self.name = info['name']                # 项目名
        self.company = info['company']          # 招标/中标公司
        self.keywords = info['keywords']        # 关键词
        self.keywords_len = len(self.keywords)
        self.filepath = info["path"]
        self.file_index = str(info["index"])
        # self.condition = info['condition']      # 资格条件
        # self.certificate = info['certificate']  # 证书

    def empty(self):
        if self.classes == "" or self.name == "" \
            or self.keywords_len == 0 or self.company == "":
            return True
        return False

    def print_data(self):
        print("类别: " + self.classes)
        print("项目名: " + self.name)
        print("中标公司: " + self.company)
        print("训练文本: " + self.keywords)
        print("源文件路径:" + self.filepath)
        print("所处源文件位置:" + self.file_index)
        if len(self.keywords) <= 2:
            print("warning")

    def toList(self):
        return [self.classes, self.company, self.name, self.keywords, self.filepath, self.file_index]