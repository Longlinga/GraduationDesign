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


def test(request):
    user_id = request.user.id
    count = models.user_subscription.objects.filter(user_id=user_id).count()
    if count:
        all_data = []
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
                all_data.append(y[0])

        return render(request, 'function/user_attention.html',{'all_data':all_data})
    else:
        mes = '您还没有关注任何商品'
        return render(request, 'function/user_attention.html', {"mes": mes})
