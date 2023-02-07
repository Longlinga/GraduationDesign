import pymysql
from django.shortcuts import render
from . import models
from backgroundData import models

mydb = pymysql.connect(
    host="127.0.0.1",
    user="root",
    passwd="11111111",
    database="price_data",
    autocommit=True

)


def test(request):
    user_id= request.user.id
    count = models.user_subscription.objects.filter(user_id=user_id).count()
    if count:
        jd_id=models.user_subscription.objects.filter(user_id=user_id).first()
        test = models.jd_data.objects.filter(id=jd_id.commodity_id).first()
        # 查询对应商品表中price字段的前十条记录
        mycursor = mydb.cursor()
        sql_price = "SELECT price FROM `{id}` LIMIT 10".format(id=jd_id.commodity_id)
        mycursor.execute(sql_price)
        myresult = mycursor.fetchall()
        price = []
        for x in myresult:
            price.append(x[0])
        # 查询对用商品表中time字段的前十条记录
        sql_time = "SELECT DATE_FORMAT( update_time, '%Y-%m-%d' ) FROM `{id}` LIMIT 10".format(id=jd_id.commodity_id)
        mycursor.execute(sql_time)
        myresult = mycursor.fetchall()
        update_time = []
        for x in myresult:
            update_time.append(x[0])
        mycursor.close()
        return render(request, 'function/user_attention.html',{"time": update_time, "price": price, "title": test.d_titel})
    else:
        mes='您还没有关注任何商品'
        return render(request, 'function/user_attention.html',{"mes":mes})
