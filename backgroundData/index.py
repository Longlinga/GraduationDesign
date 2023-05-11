import pymysql
from django.http import HttpResponse
from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.common.by import By
from . import models
import time
from django.contrib import messages
mydb=pymysql.connect(
    host="127.0.0.1",
    user="root",
    passwd="11111111",
    database="price_data",
    autocommit=True

)

def commodity_id(request):
    jd_id=100047649648
    test = models.jd_data.objects.filter(id=int(jd_id)).first()
    title = test.d_titel

    #查询jd_id表中price字段的数值最大的前十条记录
    max = models.jd_data.objects.filter().order_by('-d_price')[:10]
    max_10 = []
    for x in max:
        max_10.append(x.d_price)


    #查询100047649648表中price字段的前十条记录
    mycursor = mydb.cursor()
    sql_price = "SELECT price FROM( SELECT * FROM `100047649648` ORDER BY update_time DESC LIMIT 10) AS A ORDER BY update_time ASC".format(
        id=id)
    mycursor.execute(sql_price)
    myresult = mycursor.fetchall()
    price = []
    for x in myresult:
        price.append(x[0])
    #查询100047649648表中time字段的前十条记录
    mycursor = mydb.cursor()
    sql_time = "SELECT DATE_FORMAT( update_time, '%Y-%m-%d' ) FROM ( SELECT * FROM `100047649648` ORDER BY update_time DESC LIMIT 10) as A ORDER BY update_time ASC".format(
        id=id)
    mycursor.execute(sql_time)
    myresult = mycursor.fetchall()
    time=[]
    for x in myresult:
        time.append(x[0])
    #查询数据库中有多少张表
    mycursor = mydb.cursor()
    mycursor.execute("SELECT table_name FROM information_schema.TABLES WHERE table_schema='price_data'")
    myresult = mycursor.fetchall()
    table_name=[]
    for x in myresult:
        table_name.append(x[0])
    mycursor.close()
    # 统计table_name中有多少个元素
    table_name = len(table_name)
    #shuliang的第一个元素为table_name
    ShuLiang = []
    ShuLiang.append(table_name)



    return render(request, 'function/index.html', {"time":time,"price":price,"title":title,"dingyueSL":ShuLiang,"max_10":max_10})
