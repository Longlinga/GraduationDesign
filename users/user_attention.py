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


def follow(request):
    user_id = request.user.id
    count = models.user_subscription.objects.filter(user_id=user_id).count()
    if count:
        all_data = {}
        all_id= []
        all_title = []
        # all_price = []
        # 查询user_subscription表中user_id为user_id的记录
        mycursor = mydb.cursor()
        sql = "SELECT commodity_id FROM `backgrounddata_user_subscription` WHERE user_id = {user_id}".format(
            user_id=user_id)
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        mycursor.close()
        for x in myresult:
            all_id.append(x[0])
            # 查询jd_data表中id为x[0]的d_titel记录
            mycursor = mydb.cursor()
            sql = "SELECT d_titel FROM `backgrounddata_jd_data` WHERE id = {id}".format(id=x[0])
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            mycursor.close()
            for y in myresult:
                all_title.append(y[0])
            # 查询表名为x[0]的表中最新的一条记录
            # mycursor = priceDB.cursor()
            # sql = "SELECT price FROM `{table_name}` ORDER BY id DESC LIMIT 1".format(table_name=x[0])
            # mycursor.execute(sql)
            # myresult = mycursor.fetchall()
            # mycursor.close()
            # for z in myresult:
            #     all_price.append(z[0])
            # 将all_title和all_price组合成字典
            all_data = dict(zip(all_title, all_id))

        return render(request, 'function/user_attention.html',
                      {'all_data': all_data, 'all_id': all_id})
    else:
        mes = '您还没有关注任何商品'
        return render(request, 'function/user_attention.html', {"mes": mes})

def details(requset):
    if 'details_bt' in requset.POST:
        id = requset.POST.get('id')
        print(id)
        test = models.jd_data.objects.filter(id=int(id)).first()
        title = test.d_titel
        # 查询对应商品表中price字段的后十条记录并倒序
        mycursor = priceDB.cursor()
        sql_price = "SELECT price FROM( SELECT * FROM `{id}` ORDER BY update_time DESC LIMIT 10) AS A ORDER BY update_time ASC".format(
            id=id)
        mycursor.execute(sql_price)
        myresult = mycursor.fetchall()
        price = []
        for x in myresult:
            price.append(x[0])
        # 查询对用商品表中time字段的后十条记录
        sql_time = "SELECT DATE_FORMAT( update_time, '%Y-%m-%d' ) FROM ( SELECT * FROM `{id}` ORDER BY update_time DESC LIMIT 10) as A ORDER BY update_time ASC".format(
            id=id)
        mycursor.execute(sql_time)
        myresult = mycursor.fetchall()
        update_time = []
        for x in myresult:
            update_time.append(x[0])
        mycursor.close()
        return render(requset, 'function/details.html', {"time": update_time, "price": price, "title": title})
    elif 'del_bt' in requset.POST:
        id = requset.POST.get('id')
        user_id = requset.user.id
        #删除user_subscription表中user_id为user_id且commodity_id为id的记录
        mycursor = mydb.cursor()
        sql = "DELETE FROM `backgrounddata_user_subscription` WHERE user_id = {user_id} AND commodity_id = {id}".format(
            user_id=user_id, id=id)
        mycursor.execute(sql)
        mycursor.close()
        return follow(requset)