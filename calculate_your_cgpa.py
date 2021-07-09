from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
from selenium.webdriver.firefox.options import Options
class CpurBot:
    def __init__(self, username, password, sem):
        self.username = username
        self.password = password
        self.sem = sem
        opts = Options()
        opts.headless = True
        assert opts.headless
        self.driver = webdriver.Firefox(options=opts)
        
    def closeBrowser(self):
        self.driver.close()
    def login(self):
        driver = self.driver
        t = 4
        driver.get("http://student.cpuniversity.in/")
        time.sleep(t)
        user_name_elem = driver.find_element_by_xpath("//input[@name='txtUserName']")
        user_name_elem.clear()
        user_name_elem.send_keys(self.username)
        password_elem = driver.find_element_by_xpath("//input[@name='txtUserPassword']")
        password_elem.clear()
        password_elem.send_keys(self.password)
        password_elem.send_keys(Keys.RETURN)
        time.sleep(t)
        driver.get('http://student.cpuniversity.in/UI/performance.aspx')
        sem_num = self.sem
        credit_points = 0
        credit_score = 0
        for x in range(1, sem_num+1):
            time.sleep(t)
            sem_num = str(x)
            sem = driver.find_element_by_xpath(f'/html/body/form/div[4]/div[2]/div/div[3]/div/div/div[2]/div/div[2]/table/tbody/tr[6]/td/div/a')
            sem.click()
            first_sem = driver.find_element_by_xpath(f'//*[@id="ctl00_ContentPlaceHolder1_ddlstCurrentSem_chzn_o_{sem_num}"]')
            first_sem.click()
            html = driver.page_source
            table_MN = pd.read_html(html)
            table = table_MN[1]
            credit_points = credit_points+sum(table['Credit'].tolist())
            credit_score = credit_score+sum(table['Point Secured'].tolist())
        cgpa = credit_score/credit_points    
        return cgpa        
uid = input('Enter University Id: ')
password = input('Enter Password: ')
last_sem = int(input('Enter Last Sem: '))
dvjIG = CpurBot(uid, password, last_sem)
cgpa = dvjIG.login()
print('Your CGPA is: ', cgpa)