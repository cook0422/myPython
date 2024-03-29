import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt  #引入matplotlib

# 支持中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

def order_csv_cover(val):
    return val.replace("元","").replace("=","").replace('"','')

def read_all_csv(file_path, file_type="csv", encoding = "ANSI"):
    if os.path.isfile(file_path):
        return pd.read_csv(file_path,encoding = encoding)
    if not os.path.isdir(file_path):
        print(file_path, "   文件路径不正确")
        return
    fs = os.listdir(file_path)
    datas = []
    for file in fs:
        full_path = os.path.join(file_path,file)
        file_t = str(file.split('.')[-1])
        if file_t == file_type:
            print(file)
            data = pd.read_csv(full_path,encoding = encoding)
            datas.append(data)
    return pd.concat(datas, join= "inner")  #默认索引会重复

def fix_order_df(order_data):
    order_data['打款商家金额'] = order_data['打款商家金额'].str.replace("元","").astype("float")
    order_data['订单编号'] = order_data['订单编号'].astype("str")
    order_data["订单编号"] = order_data["订单编号"].apply(order_csv_cover)
    order_data = order_data.drop_duplicates(subset="订单编号",keep="first")  #去重,保留first，可选last、留空（则整行）
    order_data["订单创建时间"] = pd.to_datetime(order_data["订单创建时间"])
    order_data["订单创建年份"] = order_data["订单创建时间"].dt.year
    order_data["订单创建月份"] = order_data["订单创建时间"].dt.month
    return order_data

def fix_item_df(item_data):
    item_data['订单编号'] = item_data['订单编号'].astype("str")
    item_data['订单编号'] = item_data["订单编号"].apply(order_csv_cover)
    item_data = item_data.drop_duplicates(subset=["订单编号","外部系统编号","商家编码","购买数量"],keep="first")  #去重,保留first，可选last、留空（则整行）
    return item_data

#np.set_printoptions(suppress=True, threshold=np.nan) #suppress=True 取消科学记数法  threshold=np.nan 完整输出（没有省略号）
#data = pd.read_csv("D:/DB PRO/PBI/db/3个月前/ExportOrderList201907091554.csv")

def main():
    order_csv_path = r"D:\DB PRO\PBI\db\3个月前"
    item_csv_path = r"D:\DB PRO\PBI\db\宝贝报表"

    #data = pd.read_csv(order_csv_path2,encoding="ANSI",dtype={"订单编号":"str"},converters={"订单编号":order_csv_cover})  #dtype/conver只会执行其一
    orders_data = read_all_csv(order_csv_path)
    orders_data = fix_order_df(orders_data)
    orders_data.groupby(['订单创建年份','订单创建月份']).sum()
    temp_data = orders_data.pivot_table(values = '打款商家金额', index =['订单创建年份'] ,columns=['订单状态'],aggfunc=np.sum) #维度转换
    temp_data.plot()
    plt.scatter(orders_data['打款商家金额'],orders_data['买家应付货款'],alpha=0.1)
    plt.show()

    items_data = read_all_csv(item_csv_path)
    items_data = fix_item_df(items_data)
    items_data.info()
    items_data[items_data['订单状态'] == '交易成功'].count()

    #orders_data.to_excel(r'E:\Cook\git_pro\myPython\foo.xlsx', sheet_name='Sheet1') 
    #orders_data.to_csv(r'E:\Cook\git_pro\myPython\foo.csv')

    orders_data.head()
    orders_data.dtypes
    orders_data.describe()

