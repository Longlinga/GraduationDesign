import pandas as pd
import pymysql
import numpy as np
from sklearn.linear_model import LinearRegression


mydb=pymysql.connect(
    host="127.0.0.1",
    user="root",
    passwd="11111111",
    database="price_data",
    autocommit=True

)

# 检索表100047649648中的价格和时间数据
mycursor = mydb.cursor()
sql = "SELECT price,update_time FROM `100050992334`"
mycursor.execute(sql)
myresult = mycursor.fetchall()
mycursor.close()
# 将数据转换为DataFrame格式
df = pd.DataFrame(myresult, columns=['price', 'update_time'])
#创建线性回归模型
lr = LinearRegression()
#将时间数据转换为时间戳
df['update_time'] = pd.to_datetime(df['update_time'])
df['update_time'] = df['update_time'].map(pd.Timestamp.timestamp)
#将时间戳转换为二维数组
x = np.array(df['update_time']).reshape(-1, 1)
y = np.array(df['price']).reshape(-1, 1)
#训练模型
lr.fit(x, y)
#预测2023-05-11的价格
y_predict = lr.predict([[pd.Timestamp('2023-05-11').timestamp()]])
#将预测结果转换为一维数组
y_predict = y_predict.reshape(-1)





