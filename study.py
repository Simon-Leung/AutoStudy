# coding:utf-8
"""
This file is part of AutoStudy.

Permissions of this weak copyleft license are conditioned on making available
source code of licensed files and modifications of those files under the same
license (or in certain cases, one of the GNU licenses). Copyright and license 
notices must be preserved. Contributors provide an express grant of patent 
rights. However, a larger work using the licensed work may be distributed 
under different terms and without source code for files added in the larger 
work.

Created on Fri Jun 29 15:52:49 2018

@author: Simon Leung
"""
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedAlertPresentException

def course_select():
    for i in range(0,10):
        try:
            WebDriverWait(driver,60).until(lambda x: x.find_element_by_xpath("//*/tbody/tr/td/a/img[@src='images/jlkt_b1.gif']")).click()
        except:
            driver.refresh();
    if i >= 10:
        driver.quit()
        exit("选课出错")
    time.sleep(2)

def alert_before_course():
    try:
        WebDriverWait(driver,60).until(lambda x: x.switch_to_alert()).accept()  # 通过switch_to.alert切换到alert
        print("请抓紧学习！")
        driver.switch_to_window(second_handle) #返回主窗口 开始下一个跳转
        time.sleep(1)
    except:
        print("没有弹窗")

def course_complete(learn, total):
    if total != 0:
        if learn >= total:
            driver.close()
            driver.switch_to.window(now_handle)
            return True
    return False

driver = webdriver.Ie()
driver.get('http://www.gzcee.com.cn/')
now_handle = driver.current_window_handle#在这里得到当前窗口句柄
#等待登录
WebDriverWait(driver,600).until(lambda x: x.find_element_by_link_text("我的在读课程")).click()
while 1:
    course_select()
    
    handles = driver.window_handles # 获取当前全部窗口句柄集合
    print(handles) # 输出句柄集合 
    for handle in handles:# 切换窗口
        if handle != now_handle:
            print('switch to second window',handle)
            second_handle = handle
            driver.switch_to.window(second_handle) #切换到第二个窗口
            break
        
    alert_before_course()
    
    num_course = 0
    i = 0
    while 1:
        #driver.find_element_by_xpath('//*/tr/td/img[@src="skin/BlueNewNC/gif-2.gif"]')
        if course_complete(i, num_course):
            break;
        try:
            course = WebDriverWait(driver,60).until(lambda x: x.find_elements_by_xpath('//*/td/a/img[@width="87"]'))
        except UnexpectedAlertPresentException:
            alert_before_course()
            continue
        else:
            driver.quit()
            exit("选课时出错")
            
        if num_course == 0:
            num_course = len(course)
            print("number of coures is ", num_course)
            i = num_course - 1
        if i < num_course:
            i += 1
            if i >= num_course:
                i = 0
        print("Now learn ", i + 1)
        course[i].click()
        
        while 1:
            try:
                answer = driver.find_element_by_xpath("//*/tr/input[@name='answer']")
                print("Answer window exist!")
                print(answer)
                answer.click()
                driver.find_element_by_name("确定").click()
                time.sleep(1)
                try:
                    answer2 = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"//*/tr/input[@name='answer']")))
                    answer2.click()
                    driver.find_element_by_name("确定").click()
                    time.sleep(1)
                except:
                    driver.refresh()
                driver.find_element_by_name("返回").click()
            except:
                try:
                    a2 = driver.switch_to_alert()
                    print("Finish alert exist!")
                    print(a2.text)
                    a2.accept()
                    driver.switch_to_window(second_handle)
                    WebDriverWait(driver,10).until(lambda x: x.find_element_by_xpath('//*/tr/td/a/img[@alt="课程学习"]')).click()
                    time.sleep(1)
                    break
                except:
                    print("Finish alert dose not exist!")
                    time.sleep(1)
                    try:
                        leanring = driver.find_element_by_id("state")
                        print(leanring.text)
                        tm = leanring.text.split("：")[1]
                        try:
                            tm1 = float(tm.split()[0])
                            tm2 = float(tm.split()[3])
                            print(tm1)
                            print(tm2)
                            if tm2 > tm1: 
                                while 1:
                                    try:
                                        WebDriverWait(driver,10).until(lambda x: x.find_element_by_xpath('//*/tr/td/a/img[@alt="课程学习"]')).click()
                                        break
                                    except:
                                        time.sleep(1)
                                time.sleep(1)
                                break
                        except:
                            if leanring == "这是你第一次学习该课件，加油！":
                                time.sleep(1)
                            else:
                                driver.refresh()
                    except:
                        driver.refresh()
            time.sleep(1)