import requests
from bs4 import BeautifulSoup
import multiprocessing as mp
import xlsxwriter
import time
import operator
from functools import reduce
import asyncio
import aiohttp
import requests
import asyncio
import time
import numpy as np
from concurrent.futures import ThreadPoolExecutor
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
        self.write_page_index += 1
        if self.write_page_index > 99:
            self.__create_sheet()
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

def get_data_source_content(html):
    soup = BeautifulSoup(html, 'lxml')
    table = soup.select('body > table:nth-of-type(4)')
    content_table = table[0]
    content_table = content_table.get_text(separator=';', strip=True).split(';')
    content_table.pop()
    content_table.pop()
    context_str = ''.join(content_table)
    return context_str

# async def get_data_source_content_session(session,item_data):
#     response = await session.get(item_data.item_url_str)       # 等待并切换
#     item_data.content_str = get_data_source_content(response.text(encoding='gb2312'))
#     print(item_data.content_str)
#     return item_data

async def get_data_source_content_session(session,item_data,wb):

    async with session.get(item_data.item_url_str) as response:
         print("获取内容",item_data.item_url_str)
         html = await response.text('gb2312')
         item_data.content_str = get_data_source_content(html)
         return item_data


async def main1(loop,data_source_list,wb):

    print(len(data_source_list),type(data_source_list[0]))

    async with aiohttp.ClientSession() as session:      # 官网推荐建立 Session 的形式
        # tasks = [loop.create_task(get_data_source_content_session(session,data,wb)) for data in data_source_list]
        executor = ThreadPoolExecutor(3)
        tasks = []
        for data in data_source_list:
            task = loop.create_task(get_data_source_content_session(session,data,wb)) #await loop.run_in_executor(executor, get_data_source_content_session, session , data, wb)  # 阻塞的代码放到线程池
            tasks.append(task)
        finished, unfinished = await asyncio.wait(tasks)

        all_results = [r.result() for r in finished]    # 获取所有结果
        print(len(all_results),type(all_results[0]))


def get_list_url(start_index,end_index):
    for i in range(start_index,end_index):
        temp_url = __rooturl % i
        all_list_url.append(temp_url)
    return all_list_url

def get_list_html_data_source(html):
    soup = BeautifulSoup(html, 'lxml')
    allList = soup.find_all('div', id="list")
    temp = []
    for item in allList:
        all_count_text = item.get_text(separator=';', strip=True).replace('\n', '').replace('\r', '').replace('\t',
                                                                                                              '')
        text_all = all_count_text.split(';')
        alink = item.find_all('a')
        item_url = alink[1]['href']
        item_url = __itemurl % item_url
        creation_time_str = text_all[0]
        create_time = creation_time_str.replace('(', '')
        create_time = create_time.replace(')', '')
        # create_time = time.strptime(create_time, "%Y年%m月%d日")
        type_str = text_all[2]
        title_str = text_all[4]
        count_str = text_all[5]
        # print(title_str,item_url)
        item_data = ItemDataModel(type_str, title_str, create_time, item_url, count_str)
        # all_data_source.append(item_data)
        temp.append(item_data)
    return temp




async def get_list_data_source(session,url):
    await asyncio.sleep(1)
    async with session.get(url) as response:
        html = await response.text()
        print("获取列表数据", url,len(html), response.get_encoding())
        data_sour_list = get_list_html_data_source(html)
        return data_sour_list

async def main(loop):

    url_list = get_list_url(1,3)
    async with aiohttp.ClientSession() as session:      # 官网推荐建立 Session 的形式
        tasks = [loop.create_task(get_list_data_source(session,url)) for url in url_list]
        finished, unfinished = await asyncio.wait(tasks)
        all_results = [r.result() for r in finished]    # 获取所有结果
        all_data_source = np.ravel(all_results)
        # print("所有列表数据",len(all_data_source), type(all_data_source[0]))
        return all_data_source





if __name__ == '__main__':
    wb = Write_xlsx("info.xls")
    t1 = time.time()
    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(main(loop))

    print("所有列表数据",len(data),type(data[0]))
    t2 = time.time()
    print("Async total time:", t2 - t1, wb)
    loop.run_until_complete(main1(loop,data,wb))
    print("Async total time:", time.time() - t2)

    loop.close()
    wb.close()
