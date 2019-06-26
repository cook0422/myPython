import os
import sqlite3
import requests
import win32crypt
import xlrd
import xlwt
import re
from pyquery import PyQuery as pq
import time

#from win32crypt import CryptUnprotectData
def getcookiefromchrome(host='.taobao.com'):
    cookiepath=os.environ['LOCALAPPDATA']+r"\Google\Chrome\User Data\Default\Cookies"
    sql="select host_key,name,encrypted_value from cookies where host_key='%s'" % host
    with sqlite3.connect(cookiepath) as conn:
        cu=conn.cursor()        
        cookies={name:win32crypt.CryptUnprotectData(encrypted_value)[1].decode() for host_key,name,encrypted_value in cu.execute(sql).fetchall()}
        #print(cookies)
        return cookies

#运行环境windows 2012 server python3.4 x64 chrome 50
#以下是测试代码

url='https://larchyfs.tmall.com/i/asynSearch.htm?_ksTS=1561354976656_470&callback=jsonp471&mid=w-12276223078-0&wid=12276223078&path=/category.htm&spm=a1z10.5-b.w4011-12276223078.360.4c062798wA7XKu&scene=taobao_shop&pageNo=%s'
httphead={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',}

workbook = xlwt.Workbook(encoding = 'utf-8') # 创建一个workbook 设置编码
worksheet = workbook.add_sheet('My Worksheet', cell_overwrite_ok=True) # 创建一个worksheet
worksheet.write(0,0, label = 'itemID') # 写入excel # 参数对应 行, 列, 值
worksheet.write(0,1, label = '价格') # 写入excel # 参数对应 行, 列, 值
rowid = 0
rowprice = 0
for page in range(1,8):
    #设置allow_redirects为真，访问http://my.taobao.com/ 可以跟随跳转到个人空间
    print(page)
    html=requests.get(url % page,headers=httphead,cookies=getcookiefromchrome('.taobao.com'),allow_redirects=1).content
    print(html)
    html_query = pq(html)
    dc = str(html_query("dd:nth-child(3) > a:nth-child(1)"))
    id_list = re.findall(r'id=[0-9]{11,13}',dc)
    for item_id in id_list:
        rowid += 1
        worksheet.write(rowid,0,item_id[3:])
        print(item_id[3:])
    for price in html_query("dd:nth-child(3) > div:nth-child(2) > div:nth-child(1) > span:nth-child(2)").items():
        rowprice += 1
        worksheet.write(rowprice,1,price.text())
        print(price.text())
    time.sleep(60)

# 保存
workbook.save('Excel_test.xls')
