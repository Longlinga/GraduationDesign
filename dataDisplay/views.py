# coding=utf8
from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.common.by import By

def index(request):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    # 创建浏览器对象
    global driver
    driver = webdriver.Chrome(chrome_options=options)
    # 使用无界面模式
    # commodity_id = input("请输入京东商品id：)
    commodity_id = 100049486743
    driver.get(f'https://item.jd.com/{commodity_id}.function')
    title = driver.find_element(by=By.CLASS_NAME, value='sku-name').text
    price = driver.find_element(by=By.CLASS_NAME, value='price').text

    driver.implicitly_wait(10)  # 隐式等待
    print('商品名：' + title)
    print('价格：' + price)
    driver.quit()
    return render(request, 'function/index.html', {"titel":title, "price":price})