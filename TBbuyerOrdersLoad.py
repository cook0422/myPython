import os
import sqlite3
import requests,urllib
import re
import win32crypt
from pyquery import PyQuery as pq
from ctypes import *

#from win32crypt import CryptUnprotectData
def getcookiefromchrome(host='.taobao.com'):
    cookiepath=os.environ['LOCALAPPDATA']+r"\Google\Chrome\User Data\Default\Cookies"
    sql="select host_key,name,encrypted_value from cookies where host_key='%s'" % host
    with sqlite3.connect(cookiepath) as conn:
        cu=conn.cursor()        
        cookies={name:win32crypt.CryptUnprotectData(encrypted_value)[1].decode() for host_key,name,encrypted_value in cu.execute(sql).fetchall()}
        #print(cookies)
        return cookies


import win32clipboard as w   
def set_clipboard(aString):#写入剪切板  
    w.OpenClipboard()  
    w.EmptyClipboard()  
    w.SetClipboardText(aString)  
    w.CloseClipboard()  

class loadOrder(object):
    httphead = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Cookie': '请手动输入cookie',}
    order_list_url = "https://buyertrade.taobao.com/trade/itemlist/list_bought_items.htm?action=itemlist/BoughtQueryAction&event_submit_do_query=1&tabCode=waitConfirm"
    express_url = "https://detail.i56.taobao.com/trace/trace_detail.htm?"
    express_url_pattern =r"tId=[0-9]{5,20}&userId=[0-9]{5,15}"

    def __init__(self):
        self.cookies = getcookiefromchrome(".taobao.com")
        print("初始化cookies")

    def getOrders(self):
        html = requests.get(self.order_list_url,headers = self.httphead).content.decode('gbk')
        html = html.replace("trade_id","tId").replace("seller_id","userId")
        exporess_search = re.findall(self.express_url_pattern,html)
        result = ""
        for express in exporess_search:
            url = self.express_url + express
            html = requests.get(url,headers = self.httphead, cookies = self.cookies).content.decode('gbk')
            doc = pq(html)
            buyer_info = doc("body > div.order-detail > div.detail-content > div.detail-panel > div.panel-order > div > div:nth-child(4) > span")
            express_info = doc("body > div.order-detail > div.detail-content > div.detail-panel > div.panel-order > div > div:nth-child(1)")
            result += buyer_info.text() + "=====" + express_info.text() + "\r\n"
            set_clipboard(result)


test = loadOrder()
test.getOrders()


