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
    jd_id=100011848193
    test = models.jd_data.objects.filter(id=int(jd_id)).first()
    title = test.d_titel
    time1= test.add_time

    #查询100011848193表中price字段的前十条记录
    mycursor = mydb.cursor()
    mycursor.execute("SELECT price FROM `100011848193` LIMIT 10")
    myresult = mycursor.fetchall()
    price = []
    for x in myresult:
        price.append(x[0])
    #查询100011848193表中time字段的前十条记录
    mycursor = mydb.cursor()
    mycursor.execute("SELECT DATE_FORMAT( update_time, '%Y-%m-%d' ) FROM `100011848193` LIMIT 10")
    myresult = mycursor.fetchall()
    time=[]
    for x in myresult:
        time.append(x[0])
    mycursor.close()
    return render(request, 'function/index.html',{"time":time,"price":price,"title":title})
