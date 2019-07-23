import pandas_test as pt
import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

def encode_units(x):
    if x <= 0:
        return 0
    if x >= 1:
        return 1

def main():
    item_csv_path = r"D:\DB PRO\PBI\db\宝贝报表"
    items_data = pt.read_all_csv(item_csv_path)
    items_data = pt.fix_item_df(items_data)
    items_data.drop(['标题','价格','外部系统编号','商品属性','套餐信息','备注','订单状态'],axis=1,inplace= True)  # 加1为列
    items_data["商家编码"] = items_data["商家编码"].str[0:9]
    items_data =items_data.dropna(axis = 0)
    bool = items_data["商家编码"].str.contains('8182')
    items_data = items_data[bool]
    items_data = pd.pivot_table(data = items_data,values = '购买数量', index =['订单编号'] ,columns=['商家编码'],aggfunc=sum)
    items_data = items_data.fillna(0)
    items_data = items_data.applymap(encode_units)  #只能是0和1

    frequent_itemsets = apriori(items_data, min_support=0.02, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
    print(rules.head())

if __name__ == "__main__":
    main()
