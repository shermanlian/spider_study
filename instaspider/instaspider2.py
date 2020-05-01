# -*- coding: utf-8 -*-
import scrapy
import sys
import io
import requests
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException,StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
import time

'''
之前那个是分析json来解决动态加载的问题，这里想试一下使用selenium，需要登录爬取
不用到源码里的json
'''
# 解决编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

#要爬取的博主名字
INSTER_NAME = 'craziejulia'

# 配置图片存放路径(和上一个爬虫的存放路径区分加了个2)
PIC_DIR = 'D:/爬虫学习/'+INSTER_NAME+'2/'

    #实例化驱动程序的chrome对象
driver = webdriver.Chrome()

    #打开ins主页
driver.get('https://www.instagram.com/')
wait = WebDriverWait(driver,30,1)
pics = set()
ahrefs =set() # 用来判断这个帖子是不是点击过
def login_ins(driver):

    '''
    这里处理了一个问题：定位用户密码框的时候，还没加载出这个元素，会提示定位不到
    加了个sleep(10)可以解决但是不合理，10秒可能太短或者太长
    改用WebDriverWait(driver,timeout,poll_frequency=0.5,ignored_exceptions=None)
    '''
    # time.sleep(10)

    try:
        # 操作用户名部分
        username =wait.until(lambda driver:driver.find_element_by_xpath('//*[@name = "username"]'))
        # username = driver.find_element_by_xpath('//*[@name = "username"]')
        username.clear()
        username.send_keys('xxx') # 上传时注意改掉这里
        username.send_keys(Keys.RETURN)
        time.sleep(3)
        #操作密码部分
        password = wait.until(lambda driver:driver.find_element_by_xpath('//*[@name = "password"]'))
        password.clear()
        password.send_keys('xxx')
        password.send_keys(Keys.RETURN)
        time.sleep(10)
        driver.get('https://www.instagram.com/'+INSTER_NAME+'/')
        driver.implicitly_wait(10)
        global num
        num = int(driver.find_elements_by_xpath('//span[@class="g47SY "]')[0].text)
        # print('num %d' %num)
        # # 这里的等待用implicitly_wait()比较好
        # driver.implicitly_wait(10)
        #点击登录(这里不需要，因为密码回车默认登录)
        # button = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[4]/button')
        # button.click()
        # time.sleep(3)

        #处理有可能出现的弹出框问题(这里不用处理，因为应该直接从url到博主地址)
        # print(EC.alert_is_present()(driver))
        # if EC.text_to_be_present_in_element(driver,'打开通知'):
        #     print('111111111111111111111111')
        #     time.sleep(5)
        #     # driver.find_element_by_tag_name('button').click()
        #     elem =driver.find_element_by_class_name('aOOlW   HoLwm ').click()
    except NoSuchElementException as e:
        print(e)
    except TimeoutException:
        print('Time Out')

def scrapy_ins_pic(driver):
        #判断是否登录成功，登录成功后跳转到指定博主的页面
    try:
        #打开每个帖子，保存图片
        elemts = driver.find_elements_by_xpath('//div[@class="v1Nh3 kIKUG  _bz0w"]/a')
        lens = len(elemts)
        for i in range(lens):
            print(i+1)
            posts = elemts[i]
            if posts not in ahrefs:
                print(posts.get_attribute("href"))
                driver.execute_script("arguments[0].click();", posts) #代替i.click()
                print(driver.current_url)
                ahrefs.add(posts)
                # driver.back()
                # time.sleep(4)
                while True:
                    if hasElem(driver,'//button[@class="  _6CZji "]'):
                        driver.find_element_by_xpath('//button[@class="  _6CZji "]').click()
                    else:
                        elems = wait.until(lambda driver:driver.find_elements_by_xpath('//div[@class="KL4Bh"]/img'))
                        for j in range(len(elems)):
                            print(j)
                            print(len(elems))
                            pics.add(driver.find_elements_by_xpath('//div[@class="KL4Bh"]/img')[j].get_attribute("src"))
                        driver.back()
                        time.sleep(4)
                        break
    except NoSuchElementException as e:
        print(e)
    except TimeoutException:
        print('Time Out')
    # except StaleElementReferenceException:
    #     print("什么鸡巴错误")

def hasElem(driver,str):

    try:
        driver.find_element_by_xpath(str)
    except NoSuchElementException as e:
        return False
    return True

def save_pic(*pics):
    for pic_src in pics:
        pic = requests.get(url=pic_src)
        pic_name = pic_src.split('?')[0].split('/')[-1]
        pic_filename = PIC_DIR+pic_name
        try:
            if not os.path.exists(PIC_DIR):
                os.mkdir(PIC_DIR)
            if not os.path.exists(pic_filename):
                with open(pic_filename,'wb') as f:
                    f.write(pic.content)
                    f.close()
        except Exception as e:
            print(e)

def scoll_to_end(driver):
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')

def main():
    login_ins(driver)
    test = set()
    for x in range(int(num/12)+2):
        print('roll %d' %(x+1))
        for p in range(x+1):
            scoll_to_end(driver)
        # elemts1 = driver.find_elements_by_xpath('//div[@class="v1Nh3 kIKUG  _bz0w"]/a')
        # lene = len(elemts1)
        # for o in range(lene):
        #     test.add(elemts1[o].get_attribute("href"))
        # print('有多少个post: %d' %len(test))
        # print('当前界面有多少个post: %d' %lene)
        scrapy_ins_pic(driver)
        # save_pic(*pics)
    save_pic(*pics)

if __name__ == "__main__":
    main()
    driver.quit()
