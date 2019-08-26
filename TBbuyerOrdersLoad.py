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
    'Cookie': 'swfstore=229904; _uab_collina=156678274788858821570739; ali_ab=124.42.239.19.1512958473425.8; thw=cn; t=d1352b8b5de6a613c530f74f0860d748; ucn=center; UM_distinctid=16cae4c3ad82f8-0454d61d1a5e76-e353165-15f900-16cae4c3ad95af; cookie2=172daba6cf6923686f21aa6479774fe2; _tb_token_=f6e03779bfe38; _m_h5_tk=649f8eb7f011da43361db8fb65ddfbb9_1566794289698; _m_h5_tk_enc=1c55f8d15c50bca605f6e913be8fc615; whl=-1%260%260%261566787254797; x=817958615; enc=LqU0GcZ08pSzaveQ%2BBtFf2uO9CmcDEfTcDGfozh42eYpf2jK2XFNNIloZo5URXc3xJzJyo%2BOAdSkgEC6DHjRCg%3D%3D; cna=/9e0EtzC2nwCAXwq7xO1H0bX; v=0; unb=475153329; uc3=vt3=F8dBy3MMd8YLtiT1ndU%3D&nk2=AHXKcKQApWI%3D&id2=Vyu7DG8LZqOq&lg2=URm48syIIVrSKA%3D%3D; csg=f115ec4d; lgc=cook0422; cookie17=Vyu7DG8LZqOq; dnk=cook0422; skt=5aa3b739daef18e7; existShop=MTU2NjgwNTQ5NQ%3D%3D; uc4=id4=0%40VXwn2X12r0PPHkj7VIf9QZVo0uw%3D&nk4=0%40Ahsn0dV7DrLGVC8tcaJ4kMN0LA%3D%3D; publishItemObj=Ng%3D%3D; tracknick=cook0422; _cc_=UIHiLt3xSw%3D%3D; tg=0; _l_g_=Ug%3D%3D; sg=299; _nk_=cook0422; cookie1=B0BSX4hWlcYsL3eBCantdfX%2BNv4qooOwxxOGTrNUmAc%3D; mt=ci=78_1; uc1=cookie16=UIHiLt3xCS3yM2h4eKHS9lpEOw%3D%3D&cookie21=URm48syIZJWWDwI%3D&cookie15=W5iHLLyFOGW7aA%3D%3D&existShop=false&pas=0&cookie14=UoTaHoPNrHpQtA%3D%3D&tag=10&lng=zh_CN; isg=BAwM3lzWvTzs-ahvHCZmcKS13Wr-7aT_TvgTXGbMVLda8a77jlaafz4DlbnsuehH; l=cBM0zlOgvzLRc4NoBOfCNuIJcI_TrIOb8sPzw4TwnICPOvC95LilWZEDAMTpCnGVK6A2R35fHFhYBuTMQyC4EM5_YQPpHPf..',}
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
        print("work done")


test = loadOrder()
test.getOrders()


