import os
import sqlite3
import requests
import win32crypt
import xlrd
import xlwt

#from win32crypt import CryptUnprotectData
def getcookiefromchrome(host='.taobao.com'):
    cookiepath=os.environ['LOCALAPPDATA']+r"\Google\Chrome\User Data\Default\Cookies"
    sql="select host_key,name,encrypted_value from cookies where host_key='%s'" % host
    with sqlite3.connect(cookiepath) as conn:
        cu=conn.cursor()        
        cookies={name:win32crypt.CryptUnprotectData(encrypted_value)[1].decode() for host_key,name,encrypted_value in cu.execute(sql).fetchall()}
        print(cookies)
        return cookies

#运行环境windows 2012 server python3.4 x64 chrome 50
#以下是测试代码


url='https://sycm.taobao.com/adm/v2/downloadById.do?id=853524&reportType=1'
httphead={'User-Agent':'Safari/537.36',}

#设置allow_redirects为真，访问http://my.taobao.com/ 可以跟随跳转到个人空间
r=requests.get(url,headers=httphead,cookies=getcookiefromchrome('.taobao.com'),allow_redirects=1).content
with open("E:/Cook/git_pro/myPython/biaobiao.xls","wb") as f:
    f.write(r)

data = xlrd.open_workbook('E:/Cook/git_pro/myPython/biaobiao.xls')
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
