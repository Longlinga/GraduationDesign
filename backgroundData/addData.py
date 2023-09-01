
from django.http import HttpResponse
from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.common.by import By
from . import models
import time
from django.contrib import messages
import pymysql

mydb=pymysql.connect(
    host="127.0.0.1",
    user="root",
    passwd="11111111",
    database="price_data",
    autocommit=True

)

def commodity_id1(request):
    if request.method == 'POST':
        # 获取用户指定京东商品id
        jd_id = request.POST.get('jd_id')
        print(jd_id)
        #判断jd_id是否为链接
        if jd_id.find('https://item.jd.com/') != -1:
            # 提取其中。html前面的数字
            jd_id = jd_id.split('/')[-1].split('.')[0]
            print(jd_id)
        count = models.jd_data.objects.filter(id=jd_id).count()
        if count:
            mes='该商品ID已记录！已为您更新价格记录...'
            # 使用无界面模式
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            # 创建浏览器对象
            driver = webdriver.Chrome(chrome_options=options)
            # driver = webdriver.Chrome()

            # 获取指定京东商品名称及价格
            try:
                commodity_id = jd_id
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
                mes_notfound= '未找到该商品ID或该商品以下架，请检查后重新输入！'
                return render(request, 'function/addItem.html', {'mes_notfound':mes_notfound})

            # 写入数据库
            user_id=request.user.id
            models.user_subscription.objects.create(user_id=user_id, commodity_id=jd_id)
            updata_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
            sql_i = "INSERT INTO `{id}` (id,price,update_time) VALUES ( {id},{price},{time})".format(id=commodity_id,
                                                                                                     price=price,
                                                                                                     time=updata_time)
            myc = mydb.cursor()
            try:
                myc.execute(sql_i)
            except Exception as e:
                print(e)
            myc.close()
            return render(request, 'function/addItem.html', {"title": title, "price": price, "mes": mes})
            # return render(request, "function/addItem.html")
        else:
            # 使用无界面模式
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            # 创建浏览器对象
            driver = webdriver.Chrome(chrome_options=options)
            # driver = webdriver.Chrome()

            # 获取指定京东商品名称及价格
            try:
                commodity_id = jd_id
                driver.get(f'https://item.jd.com/{commodity_id}.html')
                title = driver.find_element(by=By.CLASS_NAME, value='sku-name').text
                price = driver.find_element(by=By.CLASS_NAME, value='price').text
                server_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                # driver.implicitly_wait(20)  # 隐式等待
                #等待5s
                time.sleep(5)
                if price =="":
                    price = driver.find_element(by=By.CLASS_NAME, value='price').text
                print('商品名：' + title)
                print('价格：' + price)
                driver.quit()
            except Exception as e:
                mes_notfound = '未找到该商品ID或该商品以下架，请检查后重新输入！'
                return render(request, 'function/addItem.html', {'mes_notfound': mes_notfound})

            # 写入数据库
            user_id=request.user.id
            updata_time=time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
            models.jd_data.objects.create(id=jd_id, d_titel=title, d_price=price, add_time=server_time)
            models.user_subscription.objects.create(user_id=user_id,commodity_id=jd_id)
            sql_c = 'CREATE TABLE `{id}`(id bigint,price double,update_time datetime)'.format(id=commodity_id)
            sql_i= "INSERT INTO `{id}` (id,price,update_time) VALUES ( {id},{price},{time})".format(id=commodity_id,price=price,time=updata_time)
            myc = mydb.cursor()
            try:
                myc.execute(sql_c)
                myc.execute(sql_i)
            except Exception as e:
                print(e)
            myc.close()
            return render(request, 'function/addItem.html', {"title": title, "price": price})
    return render(request, 'function/addItem.html')
