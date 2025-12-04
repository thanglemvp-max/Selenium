from pygments.formatters.html import webify
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd 
import re 

# Tạo dataframe rỗng
d = pd.DataFrame({'name':[], 'birth':[], 'death':[], 'nationality':[]})

# Khởi tạo webdriver 
driver = webdriver.Chrome()

# Mo trang 
url = "https://en.wikipedia.org/wiki/Edvard_Munch"
driver.get(url)

# đợi 2 giây
time.sleep(2)

# Lấy tên họa sĩ
try: 
    name = driver.find_element(By.TAG_NAME,"hl").text
except:
    name = ""

# Lấy ngay sinh
try:
    birth_element = driver.find_element(By.XPATH,"//th[text()='Born']/following-sibling::td")
    birth = birth_element.text
    birth = re.findall(r'[0-9]{1,2}+\s+[A-Za-z]+\s+[0-9]{4}',birth)[0] # regex
except:
    birth = ""

# Lấy ngày mất
try:
    death_element = driver.find_element(By.XPATH,"//th[text()='Died']/following-sibling::td")
    death = death_element.text
    death =re.findall(r'[0-9]{1,2}+\s+[A-Za-z]+\s+[0-9]{4}',death)[0]
except:
    death = ""

# Lấy ngày mất 
try:
    nationality_element = driver.find_element(By.XPATH,"//th[text() = 'Nationality']/following-sibling::td")
    nationality = nationality_element.text
except:
    nationality = ""

# Tạo dictioinary thông tin của họa sĩ 
painter = {'name':name, 'birth':birth, 'death':death, 'nationality':nationality}

# Chuyển đổi dictionary thành DataFrame 
painter_df = pd.DataFrame([painter])

#Thêm thông tin vào DF chính
d = pd.concat([d,painter_df], ignore_index=True)

# In ra DF
print(d)

# Đóng web driver
driver.quit()
