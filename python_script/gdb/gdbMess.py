import os
import openpyxl


class GdbDebugMess:
    def __init__(self, gdb_path, excel_path, xlsx_name):
        self.gdb_list = []  # 存储gdb的列表
        self.excel_path = excel_path
        self.path = gdb_path  # gdb文件路径
        self.final = []  # 最终需要被加载的数据的列表
        self.name = xlsx_name

        os.chdir(self.excel_path)  # 修改工作环境
        self.workbook = openpyxl.load_workbook(self.name)  # 返回一个workbook数据类型的值
        self.sheet = self.workbook.active  # 获取活动表

    def read_from_gdb(self):
        """将gdb.txt中的信息(去掉开头和结尾的空格)按照行存储在列表中"""
        with open(self.path, "r", encoding="utf-8") as fin:
            for line in fin.readlines():
                self.gdb_list.append(line.strip())

    def deal_with_line(self, mess):
        """处理每一行数据，判断是代码的说明还是函数的调用关系"""
        for i in range(0, len(mess)):
            if '0' <= mess[i] <= '9':
                continue
            elif mess[i] == '\t' or mess[i] == '\n':
                # 说明这一行是代码的说明，需要跳过这一行，继续执行
                return 0
            else:
                # 说明这一行是需要添加到excel表中的数据
                return 1

    def deal_with_gdb(self):
        """处理gdb列表"""
        
        message = ''  # 最终需要被加载的数据
        for index in range(0, len(self.gdb_list)):
            # 处理gdb.txt中前四行元素：不做任何处理
            if index < 3:
                continue
            # 处理后面的元素
            mess = self.gdb_list[index]  # 获取当前行元素
            # 判断当前行元素的类型
            flags = self.deal_with_line(mess)
            # 根据flags判断该行数据是否需要加载到excel中
            if flags == 1:
                # 该行数据需要被加载
                message += mess
            else:
                # 该行数据不需要被加载
                if message:
                    self.final.append(message)
                message = ''

    def show(self):
        """显示最终要被加载的数据的列表"""
        # for j in self.gdb_list:
        #     print(j)
        for i in self.final:
            print("########################")
            print(i)

    def write_to_excel(self):
        """将处理后的结果写入到excel中"""
        for row in self.final:
            self.sheet.append([row])
        self.workbook.save(self.name)


path = "C:/Users/12744/Desktop/gdb.txt"
xlsx_path = "C:/Users/12744/Desktop"
xlsx_name = "test.xlsx"
gdb = GdbDebugMess(path, xlsx_path, xlsx_name)
gdb.read_from_gdb()
gdb.deal_with_gdb()
gdb.write_to_excel()
