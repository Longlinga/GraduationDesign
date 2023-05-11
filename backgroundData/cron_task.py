import time

from django.http import HttpResponse
from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.common.by import By
from . import models
import pymysql

mydb=pymysql.connect(
    host="127.0.0.1",
    user="root",
    passwd="11111111",
    database="price_data",
    autocommit=True

)

def cron_task(request):
    all_data = models.jd_data.objects.all()
    all_id=[]
    for i in all_data:
        all_id.append(i.id)
    # 使用无界面模式

    myc = mydb.cursor()
    #遍历all_id
    for t_id in all_id:
        # 获取指定京东商品名称及价格
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            # 创建浏览器对象
            driver = webdriver.Chrome(chrome_options=options)
            # driver = webdriver.Chrome()
            commodity_id = t_id
            driver.get(f'https://item.jd.com/{commodity_id}.html')
            title = driver.find_element(by=By.CLASS_NAME, value='sku-name').text
            price = driver.find_element(by=By.CLASS_NAME, value='price').text
            server_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            # driver.implicitly_wait(20)  # 隐式等待
            time.sleep(5)
            if price =="":
                price = driver.find_element(by=By.CLASS_NAME, value='price').text
            print('商品名：' + title)
            print('价格：' + price)
            driver.quit()
        except Exception as e:
            mes_notfound = '未找到该商品ID或该商品以下架，请检查后重新输入！'
            print(e)
            return render(request, 'function/addItem.html', {'mes_notfound': mes_notfound})

        # 写入数据库
        updata_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        sql_i = "INSERT INTO `{id}` (id,price,update_time) VALUES ( {id},{price},{time})".format(id=commodity_id,price=price,time=updata_time)
        try:
            myc.execute(sql_i)
            print('↑写入成功↑')
        except Exception as e:
            print(e)
    myc.close()
    return render(request, 'function/cron.html', {'all_data':all_data})
