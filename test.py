from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time



chrome = Chrome()


url = "https://portal.hanyang.ac.kr/sugang/sulg.do"

chrome.get(url)

main = chrome.current_window_handle



element = chrome.find_element(By.XPATH,'//*[@id="logo-area"]/div[3]/div/span/span[4]/a/img')
element.click()
time.sleep(1)

element = chrome.find_element(By.XPATH,'//*[@id="btn-user2"]')
element.click()
time.sleep(1)


for handle in chrome.window_handles:
    if handle != main:
        login_page = handle

chrome.switch_to.window(login_page)
chrome.find_element(By.XPATH,'//*[@id="pop_login"]/form/div[1]/div/div[1]/fieldset/p[1]/input').send_keys('llf0307')
time.sleep(1)

chrome.find_element(By.XPATH,'//*[@id="pop_login"]/form/div[1]/div/div[1]/fieldset/p[2]/input').send_keys('LLFns0307.',Keys.ENTER)
time.sleep(1)
chrome.switch_to.window(main)
element = chrome.find_element(By.XPATH,'//*[@id="snb"]/ul/li[5]/a')
element.click()
time.sleep(1)

element = chrome.find_elements(By.XPATH,'/html/body/div[2]/div/div[2]/div/div[3]/div/table/tbody/tr')
for i in element:
    new = i.find_element(By.XPATH,'./td[13]/span/input')
    new.click()
    confirm = chrome.switch_to.alert
    confirm.accept()
    time.sleep(1)