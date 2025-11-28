from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Tạo 1 driver để bắt đầu điều khiển 
driver = webdriver.Chrome()

# Mở một trang wed 
driver.get("http://gomotungkinh.com/")
time.sleep(5)

try: 
    while True:
        driver.find_element(By.ID, "bonk").click()
        time.sleep(2)
except:
    driver.quit()