from ast import main
from atexit import register
from operator import truediv
from unicodedata import name
from xml.etree.ElementPath import xpath_tokenizer
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import os
import base64
# get the gui interface
basedirEx = os.path.dirname(__file__)

# /html/body/div[2]/div/div[2]/div/div[3]/div/table/tbody/tr[1]/td[11]
# /html/body/div[2]/div/div[2]/div/div[3]/div/table/tbody/tr[1]/td[2]/span/input

def course_order_default(all_course_tr, usr_setting=False, usr_setting_course_order=[]):
    # 对课程进行爬去并排序保存
    course_order = {}
    if usr_setting == False:
        for i in all_course_tr:
            ideal_num = i.find_element(By.XPATH, "./td[5]").text
            max_num = i.find_element(By.XPATH, "./td[4]").text

            diff = int(ideal_num) - int(max_num)

            # add i and diff to course_order
            course_order[i] = diff

        ordered_course = dict(sorted(course_order.items(), key=lambda x: x[1], reverse=True))
        print(ordered_course)
        return ordered_course
    else:
        for i in usr_setting_course_order:
            course_index = int(i)-1
            ideal_num = all_course_tr[course_index].find_element(
                By.XPATH, "./td[5]").text
            max_num = all_course_tr[course_index].find_element(
                By.XPATH, "./td[4]").text

            diff = int(ideal_num) - int(max_num)
            course_order[all_course_tr[course_index]] = diff
        return course_order


def execute(id_num, password, usr_setting, usr_setting_course_order):
    # encoding:utf-8
    '''
    通用文字识别（高精度版）
    '''

    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    # 二进制方式打开图片文件

    APP_ID = '26935485'
    API_KEY = 'gcZNdCT94vcaGHURTq1lLK6h'
    SECRET_KEY = 'W28MrEb9L5hCbGjA3L0gp1STzXilnzeq'
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={API_KEY}&client_secret={SECRET_KEY}'

    response = requests.get(host)
    if response:
        access_token = response.json()['access_token']
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}

    def captcha_ocr(base):
        params = {"image": base}
        response = requests.post(request_url, data=params, headers=headers)

        if response:
            captcha = response.json(
            )['words_result'][0]['words'].replace(" ", "")
            print(captcha)
        return captcha

    # 获得url，开始selenium测试
    # add options

    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option(
        "excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('lang=zh-CN,zh,zh-TW,en-US,en')
    options.add_argument(
        'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36')
    # options.add_argument(r"user-data-dir=/Users/dylanmengzhou/Library/Application Support/Google/Chrome")

    chrome = webdriver.Chrome(
        options=options, executable_path=os.path.join(basedirEx, "chromedriver"))

    # chrome.maximize_window()
    url = "https://portal.hanyang.ac.kr/sugang/sulg.do"
    chrome.get(url)

    # 点击英文portal
    english_btn = chrome.find_element(
        By.XPATH, "/html/body/div[1]/div[3]/div/span/span[4]")
    english_btn.click()
    time.sleep(1)

    # 找到login按钮并点击
    login_btn = chrome.find_element(By.XPATH, "/html/body/div[1]/div[3]/div/a")
    login_btn.click()

    # 切换窗口并输入账号密码登陆
    chrome.switch_to.window(chrome.window_handles[1])
    time.sleep(1)

    # 输入账号
    id_input = chrome.find_element(
        By.XPATH, "/html/body/div/div/div[1]/form/div[1]/div/div[1]/fieldset/p[1]/input")
    id_input.send_keys(id_num)

    # 输入密码
    password_input = chrome.find_element(
        By.XPATH, "/html/body/div/div/div[1]/form/div[1]/div/div[1]/fieldset/p[2]/input")
    password_input.send_keys(password)

    # 点击登陆按钮
    complete_btn = chrome.find_element(
        By.XPATH, "/html/body/div/div/div[1]/form/div[1]/div/div[1]/fieldset/p[3]/a").click()

    time.sleep(2)
    chrome.switch_to.window(chrome.window_handles[-1])
    time.sleep(1)
    course_selection = chrome.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/ul/li[6]/a")
    # course_selection = WebDriverWait(chrome, 1000,0.1).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='snb']/ul/li[6]/a")))
    course_selection.click()
    time.sleep(2)

    all_course_tr = chrome.find_elements(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[3]/div/table/tbody/tr")
        # //*[@id="btn_apply"]
        # /html/body/div[2]/div/div[2]/div/div[3]/div/table/tbody/tr[1]/td[2]/span/input


# fixme:

    ordered_course = course_order_default(
        all_course_tr, usr_setting, usr_setting_course_order)

    # # get current time
    # course_time="10:59:55"

    # # test: test time
    # # course_time=""
    # current_time = time.strftime("%H:%M:%S", time.localtime())
    # while(current_time != course_time):
    #     current_time = time.strftime("%H:%M:%S", time.localtime())

    # 根据顺序点击课程
    n = 1
    for key, value in ordered_course.items():
        course_name = key.find_element(By.XPATH, "./td[11]").text
        

        while 1:
            print("课程名称:",course_name)
            
            register= key.find_element(By.XPATH, "td[2]/span/input")
            register_status = register.is_displayed()
            if register_status:
                register.click()
            else:
                print("选课按钮没显示")
                print("--------------------------------")
                break
            # //*[@id="btn_apply"]
            # register = WebDriverWait(key, 1000,0.1).until(EC.visibility_of_element_located((By.XPATH, "/td[2]/span/input")))
            try:

                captcha_statue = chrome.find_element(
                    By.XPATH, "//*[@id='hyinContents']/div[4]").is_displayed()
                print(captcha_statue)

                while captcha_statue:
                    print("验证码: 有")

                    # captcha_status = chrome.find_element(
                    #     By.XPATH, "//*[@id='hyinContents']/div[4]").isDisplayed()
                    pic = WebDriverWait(chrome, 1, 0.1).until(EC.visibility_of_element_located(
                        (By.XPATH, "//*[@id='susc0100_pop8']/table/tbody/tr/td[1]/img")))
                    pic = pic.screenshot_as_base64
                    # print(1)
                    # pic = chrome.find_element(
                    #     By.XPATH, "//*[@id='susc0100_pop8']/table/tbody/tr/td[1]/img").screenshot_as_base64
                    # get the captcha
                    time.sleep(1)
                    captcha = captcha_ocr(pic)
                    # print(2)
                    # captcha = "123456"
                    # input the captcha
                    captcha_input = chrome.find_element(
                        By.XPATH, "/html/body/div[2]/div/div[2]/div/div[4]/div/div/table/tbody/tr/td[2]/input")
                    captcha_input.send_keys(str(captcha))
                    # print(3)

                    captcha_confirm_btn = chrome.find_element(
                        By.XPATH, "//*[@id='btn_confirm_susc0100_pop8']")
                    captcha_confirm_btn.click()
                    # print(4)
                    print("captcha Done")
                    print("--------------------------------")

                    captcha_statue = WebDriverWait(chrome, 1, 0.1).until(
                        EC.visibility_of_element_located((By.XPATH, "//*[@id='hyinContents']/div[4]")))
                    captcha_statue = captcha_statue.is_displayed()
                    print("loop captcha: ", captcha_statue)

            except:
                print("验证码: 无")
                pass

            key_word = ["수강 신청이", "comp",
                        "conflict", "Com", "Fu", "fu","already","It is not a registration period."]
            course_status = WebDriverWait(chrome, 500, 0.1).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='messageBox']")))
            course_status = course_status.text

            if any(key in course_status for key in key_word):
                print("抢课成功")
                # if "re" in course_status:
                # yes = WebDriverWait(chrome, 1000, 0.1).until(
                #     EC.presence_of_element_located((By.TAG_NAME, "button")))
                # yes.click()

                
                n += 1
                # time.sleep(2)
                break
            else:
                print("抢课失败，重新抢课")
                # yes = WebDriverWait(chrome, 1000, 0.1).until(
                #     EC.presence_of_element_located((By.TAG_NAME, "button")))
                # yes.click()
            yes = WebDriverWait(chrome, 1000, 0.1).until(EC.presence_of_element_located((By.TAG_NAME, "button")))
            yes.click()
            
            print("抢课落差：",value)
            print("--------------------------------")
