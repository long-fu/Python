import requests
from bs4 import BeautifulSoup
import time
import re
import xlwt
import xlsxwriter
import datetime
import time
import urllib.request
__rooturl = 'http://www.52cili.com/info/news_more.asp?page=%d&word=&lm=&lm2=73&lmname=&open=&n=&hot=&tj=&soso=&dot=0&lryname=&XsUser='
__itemurl = 'http://www.52cili.com/info/%s'

#设置表格样式
def set_style(name,height,bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style

urlList =[]
all_item = []
class ItemData:

    content_text = None
    def __init__(self, type, title, creation_time, item_url,count):
        self.type = type
        self.title = title
        self.creation_time = creation_time
        self.item_url = item_url
        self.count = count
        pass

    def getContent_text(self):
        print("当前url",self.item_url)
        r = requests.get(self.item_url)
        print(r.encoding)
        r.encoding = 'gb2312'
        soup = BeautifulSoup(r.text, 'lxml')
        table = soup.select('body > table:nth-of-type(4)')
        context_table = table[0]
        context = context_table.get_text(separator=';', strip=True).split(';')
        context.pop()
        context.pop()
        self.content_text = ''.join(context)
        print('爬去到的内容数据',self.content_text)
        pass

    def save_data(self):
        print("保存当前数据")

        pass
# body > table:nth-child(9)




def init_data(rn):
    for i in range(rn):
        temp_url = __rooturl % (i + 1)
        urlList.append(temp_url)



def get_item_data(i):
    print("爬取分页数据",urlList[i])
    r = requests.get(urlList[i])
    soup = BeautifulSoup(r.text.encode(r.encoding),'lxml')
    allList = soup.find_all('div',id="list")
    i = 0
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
        item_data = ItemData(type_str,title_str,create_time,item_url,count_str)
        all_item.append(item_data)
        i += 1

def ppa_main():
    init_data(9)

    for i in range(9):
        get_item_data(i)

    row = 0
    for item in all_item:
        # if row == 8 :
        #     break
        item.getContent_text()
        row += 1


    workbook = xlsxwriter.Workbook('/Users/luofengyuan/PycharmProjects/Cili/info.xls')
    sheet1 = workbook.add_worksheet(name='info')
    bold = workbook.add_format({'bold': True})
    title = ["标题", "类别", "内容", "时间", "活跃度"]


    col = 0
    for item in title :
        sheet1.write(0,col,item,bold)
        col += 1

    row = 1
    for item in all_item:
        # if row == 9 :
        #     break
        # print(type(item.content_text),item.content_text)
        data = [item.title,item.type,item.content_text,item.creation_time,item.count]
        sheet1.write(row, 0, data[0])
        sheet1.write(row, 1, data[1])
        sheet1.write(row, 2, data[2])
        sheet1.write(row, 3, data[3])
        sheet1.write(row, 4, data[4])
        row += 1


    workbook.close()
    pass

# 测试内容数据
def get_context(url):
    # res = urllib.request.urlopen(url)

    # htmlBytes = res.read()
    # print(htmlBytes.decode('ISO-8859-1'))
    r = requests.get(url,)
    r.encoding = 'gb2312'
    print(r.encoding,'\r\n',r.text)
    # print("xxxxx")
    # print(r.content)
    # r.text.decode(r.encoding)

    # print(r.text.encode('gb2312'))
    # text = r.text.replace(u'\xa0 ', u' ')
    # print(text.encode(r.encoding))
    # text = text.decode('uft-8').replace('\r','').replace('\n','')
    # print(text)
    html = r.text
    # print(html)
    soup = BeautifulSoup(html, 'lxml')

    table = soup.select('body > table:nth-of-type(4)')


    context_table = table[0]
    print(context_table)
    con = context_table.get_text(separator=';',strip=True).split(';')
    con.pop()
    con.pop()
    print(con)
    # print('爬去到的数据'.join(con))
    content_text = ''.join(con)

    print('爬去到的数据', content_text)
    return ''

if __name__ == '__main__':
    print("开始爬取数据",time.time())
    # test_contURL()
    # get_context('http://www.52cili.com/info/News_View.asp?NewsID=51573')
    ppa_main()


