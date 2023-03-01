import pymysql

from django.shortcuts import render
from . import models
from backgroundData import models

mydb = pymysql.connect(
    host="127.0.0.1",
    user="root",
    passwd="11111111",
    database="graduationdesign",
    autocommit=True
)
priceDB = pymysql.connect(
    host="127.0.0.1",
    user="root",
    passwd="11111111",
    database="price_data",
    autocommit=True
)


def test(request):
    user_id = request.user.id
    count = models.user_subscription.objects.filter(user_id=user_id).count()
    if count:
        all_data={}
        all_title = []
        all_price = []
        #查询user_subscription表中user_id为user_id的记录
        mycursor = mydb.cursor()
        sql = "SELECT commodity_id FROM `backgrounddata_user_subscription` WHERE user_id = {user_id}".format(user_id=user_id)
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        mycursor.close()
        for x in myresult:
            #查询jd_data表中id为x[0]的d_titel记录
            mycursor = mydb.cursor()
            sql = "SELECT d_titel FROM `backgrounddata_jd_data` WHERE id = {id}".format(id=x[0])
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            mycursor.close()
            for y in myresult:
                all_title.append(y[0])
            #查询表名为x[0]的表中最新的一条记录
            mycursor = priceDB.cursor()
            sql = "SELECT price FROM `{table_name}` ORDER BY id DESC LIMIT 1".format(table_name=x[0])
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            mycursor.close()
            for z in myresult:
                all_price.append(z[0])
            #将all_title和all_price组合成字典
            all_data = dict(zip(all_title, all_price))


        return render(request, 'function/user_attention.html',{'all_title':all_title,'all_price':all_price,'all_data':all_data})
    else:
        mes = '您还没有关注任何商品'
        return render(request, 'function/user_attention.html', {"mes": mes})
