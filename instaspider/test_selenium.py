# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import io
import sys
import time
from selenium.webdriver.common.keys import Keys #输入关键词
# #测试打开简书界面（简书首页每次刷新出来的内容不一样）
driver= webdriver.Chrome()
# driver.maximize_window()
# driver.implicitly_wait(3)#等待3秒
driver.get('https://www.jianshu.com')
# 解决编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
try:
    #注意这里elements有个s，要不然会报'WebElement' object is not iterable的错误
    title = driver.find_elements_by_xpath('//*[@class="title"]')
    for ti in title:
        print(ti.text)
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(3)
    print('已经到达最后')
except NoSuchElementException as e:
    print(e)
finally:
    driver.quit()
#自动关闭


'''
测试下一些基础操作
https://www.jianshu.com/p/a1a64f649472
'''
# 实例化
# driver = webdriver.Chrome()
# 请求
# driver.get('https://3416230579.github.io/page/index.html')
# 操作一：根据id,name 取值赋值 给输入框填值
# elem = driver.find_element_by_id('element_id') #根据id获取对象
# elem.send_keys('hhh') # 给对象输入值
# time.sleep(4)
# print(elem.tag_name) # 返回标签的名字
# print(elem.text) # 返回对象的值
# elem2 = driver.find_element_by_name('element_id')
# elem2.send_keys('www')
# time.sleep(4)
# print(elem2.tag_name)
# print(elem2.text)

#操作二：根据link的text来取值,跳转到链接的界面并获取源码
# elem3 = driver.find_element_by_link_text('find_element_by_link_text')
# print(elem3.text)
# print(elem3.tag_name)
# print(type(elem3))
# elem3.click()
# time.sleep(5)
# driver.switch_to.window(driver.window_handles[1])
# print(driver.page_source)

# # 操作三：利用css和xpath，获取框来填值
# elem4 = driver.find_element_by_css_selector('.highlight')
# elem4.send_keys('css')
# elem5 = driver.find_element_by_xpath('//*[@id="xpathname"]')
# elem5.send_keys('xpath')
# time.sleep(3)

# # 操作四：根据标签名字来获取值，并且操作弹出框
# elem6 = driver.find_element_by_tag_name('button')
# elem6.click()
# time.sleep(2)
# driver.switch_to_alert().accept()
# time.sleep(2)


# # 操作五：跳转、回退操作
# elem7 = driver.find_element_by_link_text('forward_back')
# elem7.click()
# time.sleep(3)
# driver.back()
# time.sleep(3)
# driver.forward()
# time.sleep(3)
# driver.back()
# time.sleep(3)

# 操作六：cookie的操作，添加cookie，查看cookies，删除cookie等
# driver.get('https://www.baidu.com')
# print(driver.get_cookies())
# driver.add_cookie({"name":"lianweyi","domain":"baidu.com","value":"xxx"})
# print(driver.get_cookies())
# driver.delete_all_cookies()
# print("---------------------")
# print(driver.get_cookies())

# 操作七：自动打开搜索框，填值，回车
# elem8 = driver.find_element_by_id('kw')
# time.sleep(3)
# elem8.send_keys('爬虫')
# time.sleep(3)
# elem8.send_keys(Keys.RETURN)
# time.sleep(3)
# 关闭
driver.quit()