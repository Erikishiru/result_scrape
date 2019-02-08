from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
import re
import csv

def getResult(roll, driver):
    marks_xpath = '/html/body/form/table[1]/tbody/tr/td/table/tbody/tr[17]/td/div/table/tbody/tr[2]/td[2]'
    marks = driver.find_element_by_xpath(marks_xpath).text
    marks = (int(marks)/850)*100
    csv_writer.writerow([roll, marks])

csv_file = open('result.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Roll No.", "Percentage"])

roll = 18312911001

while(roll<18312911045):

    url='http://duresult.in/students/Combine_GradeCard.aspx'
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    code = driver.page_source
    college = Select(driver.find_element_by_name('ddlcollege'))
    college.select_by_value("312")

    rollno = driver.find_element_by_name("txtrollno")
    rollno.send_keys(roll)

    captcha_re = re.compile('CaptchaCode=(\d{6})')
    captcha_value = captcha_re.findall(driver.page_source)
    captcha = driver.find_element_by_name("txtcaptcha")
    captcha.send_keys(captcha_value)

    submitButton = driver.find_element_by_name("btnsearch")
    submitButton.click()

    getResult(roll, driver)
    driver.close()
    roll +=1
csv_file.close()