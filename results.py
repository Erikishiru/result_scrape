from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
import base64
import pytesseract
from io import BytesIO
from PIL import Image
import csv

def getCaptcha(driver):
    ele_captcha = driver.find_element_by_id("imgCaptcha")

    # get the captcha as a base64 string
    img_captcha_base64 = driver.execute_async_script("""
        var ele = arguments[0], callback = arguments[1];
        ele.addEventListener('load', function fn(){
        ele.removeEventListener('load', fn, false);
        var cnv = document.createElement('canvas');
        cnv.width = this.width; cnv.height = this.height;
        cnv.getContext('2d').drawImage(this, 0, 0);
        callback(cnv.toDataURL('image/jpeg').substring(22));
        }, false);
        ele.dispatchEvent(new Event('load'));
        """, ele_captcha)

    # save the captcha to a file
    with open(r"captcha.jpg", 'wb') as f:
        f.write(base64.b64decode(img_captcha_base64))

    img = Image.open("./captcha.jpg")

    img.save('captcha_original.png')
    gray = img.convert('L')
    gray.save('captcha_gray.png')
    bw = gray.point(lambda x: 0 if x < 200 else 255, mode='1')
    bw.save('captcha_thresholded.png')

    captcha_value = pytesseract.image_to_string(bw)
    captcha = driver.find_element_by_name("txtcaptcha")
    captcha.send_keys(captcha_value)

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

    getCaptcha(driver)

    submitButton = driver.find_element_by_name("btnsearch")
    submitButton.click()

    try:
       driver.find_element_by_id('lblmsg')
       print (roll,"Captcha error")
       driver.close()
    except:
        getResult(roll, driver)
        driver.close()
        roll +=1
csv_file.close()