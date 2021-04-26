class companyInfo:
    def __init__(self, info):
        self.range = info['range']
        self.companyName = info['name']
        self._class = info['class']
        self.location = info['location']
        self.filepath = info['path']
        self.file_index = str(info["index"])

    def print_data(self, debug):
        if debug:
            print("公司名称: " + self.companyName)
            print("经营范围: " + self.range)
            print("公司类别: " + self._class)
            print("公司位置: " + self.location)
            print("源文件路径:" + self.filepath)
            print("所处源文件位置:" + self.file_index)

    def toList(self):
        return [self.companyName, self.range, self._class, self.location, self.filepath, self.file_index]