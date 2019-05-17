import requests
from bs4 import BeautifulSoup
import multiprocessing as mp
import time
import re
import xlwt
import xlsxwriter
import datetime
import time
import urllib.request
import operator
from functools import reduce

xlsxwriter_row = 0
__rooturl = 'http://www.52cili.com/info/news_more.asp?page=%d&word=&lm=&lm2=73&lmname=&open=&n=&hot=&tj=&soso=&dot=0&lryname=&XsUser='
__itemurl = 'http://www.52cili.com/info/%s'
all_list_url = []

all_data_source = []



class Write_xlsx():
    # workbook = xlsxwriter.Workbook('/Users/luofengyuan/PycharmProjects/Cili/info.xls')
    # workbook = None
    write_count = 0

    write_page = 1
    write_page_index = 1
    def __init__(self,path_url):
        self.workbook = xlsxwriter.Workbook(path_url)
        self.sheet = self.workbook.add_worksheet(name='%d' % self.write_page)
        bold = self.workbook.add_format({'bold': True})
        title = ["标题", "类别", "内容", "时间", "活跃度"]
        col = 0
        for item in title:
            self.sheet.write(0, col, item, bold)
            col += 1

    def __create_sheet(self):
        self.write_page += 1
        self.sheet = self.workbook.add_worksheet(name='%d' % self.write_page)
        bold = self.workbook.add_format({'bold': True})
        title = ["标题", "类别", "内容", "时间", "活跃度","URL"]
        col = 0
        for item in title:
            self.sheet.write(0, col, item, bold)
            col += 1

    def write(self,item_data):

        print(item_data.content_str)
        self.sheet.write(self.write_page_index, 0, item_data.title_str)
        self.sheet.write(self.write_page_index, 1, item_data.type_str)

        if item_data.content_str != None:
             self.sheet.write(self.write_page_index, 2, item_data.content_str)

        self.sheet.write(self.write_page_index, 3, item_data.creation_time_str)
        self.sheet.write(self.write_page_index, 4, item_data.count_str)
        self.sheet.write(self.write_page_index, 5, item_data.item_url_str)

        if self.write_page_index > 98:
            self.__create_sheet()
            self.write_page_index = 1

        self.write_page_index = 1
        self.write_count += 1
        pass

    def close(self):
        self.workbook.close()

class ItemDataModel:
    content_str = None
    def __init__(self, type, title, creation_time, item_url,count):
        self.type_str = type
        self.title_str = title
        self.creation_time_str = creation_time
        self.item_url_str = item_url
        self.count_str = count
        pass

def get_content(item_data):
    # print(item_data.item_url_str)
    r = requests.get(item_data.item_url_str)
    r.encoding = 'gb2312'
    soup = BeautifulSoup(r.text, 'lxml')
    table = soup.select('body > table:nth-of-type(4)')
    content_table = table[0]
    content_table = content_table.get_text(separator=';', strip=True).split(';')
    content_table.pop()
    content_table.pop()
    context_str = ''.join(content_table)
    item_data.content_str = context_str
    return item_data

def get_list_url(start_index,end_index):
    for i in range(start_index,end_index):
        temp_url = __rooturl % i
        all_list_url.append(temp_url)

def get_list_data_source(url):
    r = requests.get(url)
    # print('获取page',url)
    r.encoding = 'gb2312'
    soup = BeautifulSoup(r.text,'lxml')
    allList = soup.find_all('div',id="list")
    temp = []
    for item in allList:
        all_count_text = item.get_text(separator=';',strip=True).replace('\n','').replace('\r','').replace('\t','')
        text_all = all_count_text.split(';')
        alink = item.find_all('a')
        item_url = alink[1]['href']
        item_url = __itemurl % item_url
        creation_time_str = text_all[0]
        create_time = creation_time_str.replace('(','')
        create_time = create_time.replace(')','')
        # create_time = time.strptime(create_time, "%Y年%m月%d日")
        type_str = text_all[2]
        title_str = text_all[4]
        count_str = text_all[5]
        # print(title_str,item_url)
        item_data = ItemDataModel(type_str,title_str,create_time,item_url,count_str)
        # all_data_source.append(item_data)
        temp.append(item_data)
    return temp

if __name__ == '__main__':


    get_list_url(1,5)
    # print(all_list_url)
    pool = mp.Pool()
    tmep_data = pool.map(get_list_data_source,all_list_url)
    all_data_source = reduce(operator.add, tmep_data)
    print(len(all_data_source))
    print("开始获取详细内容",time.time_ns())
    all_data_source = pool.map(get_content, all_data_source)
    print("开始数据写入",time.time_ns(),len(all_data_source))
    wb = Write_xlsx('/Users/luofengyuan/PycharmProjects/Cili/info.xls')
    # map(wb.write,all_data_source)
    for item in all_data_source:
        wb.write(item)
    wb.close()

    # for item in all_data_source:
    #     print(item.content_str)
    pass
