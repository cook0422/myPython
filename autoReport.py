import os
import sqlite3
import requests,urllib
import win32crypt
import json
import re

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

class autoLoadReports(object):

    httphead = {'User-Agent':'Safari/537.36','accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',}
    cookies = getcookiefromchrome('.taobao.com')
    ReportsListUlr = 'https://sycm.taobao.com/adm/v2/userReport/reportList.json?dateType=day'           #报表LIST地址
    ReportsViewUrl = 'https://sycm.taobao.com/adm/v2/execute/previewById.json?id=%s&reportType=1'       #报表预览地址
    ReportsDloadtUlr = 'https://sycm.taobao.com/adm/v2/downloadById.do?id=%s&reportType=1'              #下载报表地址
    Repots = []

    def __init__(self,file = "Y:\运营资料\报表"):       #初始化报表任务List
        self.filepath = file.replace("\\","/")
        self.filepath = self.filepath if os.path.exists(self.filepath) else "d:/"
        self.filepath = self.filepath + ("" if self.filepath[-1] == "/" else "/")
        html = requests.get(self.ReportsListUlr,headers = self.httphead, cookies = self.cookies).content
        list_json = json.loads(html)
        for rp in list_json['data']:
            temp_rp:report = report(str(rp['id']),rp['name'])
            self.Repots.append(temp_rp)


    #下载预览报表
    def loadViewReports(self):
        for rp in self.Repots:
            print(rp.reportID  + ':' + rp.reportName)
            html = requests.get(self.ReportsViewUrl % rp.reportID,headers=self.httphead,cookies=self.cookies).content
            views_json = json.loads(html)
            print(type(views_json['data']['size']))
            for view in views_json['data']['data']:
                print(view[1])

    #下载报表
    def loadReports(self):
        for rp in self.Repots:
            req=requests.get(self.ReportsDloadtUlr % rp.reportID,headers=self.httphead,cookies= self.cookies)
            #requst_headers = json.loads(json.dumps(dict(req.headers)))
            #file_name = re.search('filename=(.*)\"',requst_headers['Content-disposition'])
            #file_name = file_name.group(1).replace("\\","").replace("\"","")  
            import time
            file_name = rp.reportName + time.strftime("%Y-%m-%d %H%M%S", time.localtime()) + ".xls"
            file_name = urllib.parse.unquote(file_name,encoding='gb2312')
            single_path = os.path.join(self.filepath,rp.reportName)
            if not os.path.exists(single_path):
                os.mkdir(single_path)
            with open(single_path + "/" + file_name,"wb") as f:
                f.write(req.content)
            print(file_name + "   ------> 下载成功")  



"""
报表类
"""
class report(object):
    def __init__(self,id:str,name:str):
        self.reportID = id
        self.reportName = name

print("-------start donwnload----------")
test = autoLoadReports('E:\Cook\git_pro\PBI\来尔佳昵\生意参谋')
test.loadReports()
print("-------download done !----------")
