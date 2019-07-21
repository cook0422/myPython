import pandas as pd
import numpy as np

data = pd.read_csv("D:/DB PRO/PBI/db/3个月前/ExportOrderList201907091554.csv")
data['打款商家金额'] = data['打款商家金额'].str.replace("元","")
data['打款商家金额'] = data['打款商家金额'].astype("float")
data.head()
data.dtypes
data.describe()
