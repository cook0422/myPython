import os
import sqlite3
import requests,urllib
import win32crypt
import json
import xlrd
import xlwt
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


url='https://sycm.taobao.com/adm/v2/downloadById.do?id=853524&reportType=1'
httphead={'User-Agent':'Safari/537.36','accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',}
html = requests.get('https://sycm.taobao.com/adm/v2/execute/previewById.json?id=591115&reportType=1',headers=httphead,cookies=getcookiefromchrome('.taobao.com')).content
html = json.loads(html)
for money in html['data']['data']:
        print(money[6])
raise

#设置allow_redirects为真，访问http://my.taobao.com/ 可以跟随跳转到个人空间
r=requests.get(url,headers=httphead,cookies=getcookiefromchrome('.taobao.com'),allow_redirects=1)
r.encoding = "utf-8"
requst_headers = json.loads(json.dumps(dict(r.headers)))
file_name = re.search('filename=(.*)\"',requst_headers['Content-disposition'])
if file_name:
        file_name = file_name.group(1).replace("\\","").replace("\"","")      
        print(file_name)  
        file_name = urllib.parse.unquote(file_name,encoding='gb2312')
else:
        import time
        file_name = print (time.strftime("%Y-%m-%d %H%M%S", time.localtime()))
with open("E:/Cook/git_pro/myPython/" + file_name,"wb") as f:
    f.write(r.content)


raise
data = xlrd.open_workbook('E:/Cook/git_pro/myPython/biaobiaos.xls')
table = data.sheets()[0]
row = table.nrows
col = table.ncols
a=0
b=0

print(table.row_values(2))
while a < row:
        while b < col:
                print("行：%s 列：%s" % (a,b))
                b += 1
        print(row)
        b = 0
        a += 1
