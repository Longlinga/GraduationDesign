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

def select_id(request):
    if request.method == 'GET' and 'bt2' in request.GET:
        jd_id = request.GET.get('select_id')
        print(jd_id)
        # 判断jd_id是否为链接
        if jd_id.find('https://item.jd.com/') != -1:
            # 提取其中。html前面的数字
            jd_id = jd_id.split('/')[-1].split('.')[0]
            print(jd_id)
        count = models.jd_data.objects.filter(id=jd_id).count()
        if count:#如果存在
            test = models.jd_data.objects.filter(id=int(jd_id)).first()
            title = test.d_titel
            # 查询对应商品表中price字段的后十条记录并倒序
            mycursor = mydb.cursor()
            sql_price = "SELECT price FROM( SELECT * FROM `{id}` ORDER BY update_time DESC LIMIT 30) AS A ORDER BY update_time ASC".format(id=jd_id)
            mycursor.execute(sql_price)
            myresult = mycursor.fetchall()
            price = []
            for x in myresult:
                price.append(x[0])
            # 查询对用商品表中time字段的后十条记录
            sql_time = "SELECT DATE_FORMAT( update_time, '%Y-%m-%d' ) FROM ( SELECT * FROM `{id}` ORDER BY update_time DESC LIMIT 30) as A ORDER BY update_time ASC".format(id=jd_id)
            mycursor.execute(sql_time)
            myresult = mycursor.fetchall()
            update_time = []
            for x in myresult:
                update_time.append(x[0])
            mycursor.close()
            return render(request, 'function/queryData.html', {"time":update_time,"price":price,"title":title})

        else:#不存在则添加
            # messages.info(request, '该商品id尚未添加，已为您自动添加')
            m1='该商品id尚未添加，请先登陆添加！'
            return  render(request, 'function/queryData.html', {'m1':m1})

    return render(request, 'function/queryData.html')