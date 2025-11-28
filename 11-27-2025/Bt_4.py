from builtins import range
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Khởi tạo Webdriver 
driver = webdriver.Chrome()

for i in range(65, 91):  # 65 = 'A', 90 = 'Z'
    url = "https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_%22" + chr(i) + "%22"   
    try:
        # Mở trang 

        driver.get(url)

        # Đợi một chút để trang tải
        time.sleep(3)

        #Lấy ra tất cả các cá thể ul
        ul_tags = driver.find_elements(By.TAG_NAME,"ul")
        print(len(ul_tags))

        # Chọn the ul thứ 21
        ul_painters = ul_tags[20] # list start with index=0

        # Lay ra tất cả the <li> thuoc ul_painters
        li_tags = ul_painters.find_elements(By.TAG_NAME,"li")

        # Tao danh sách các url
        titles = [tag.find_element(By.TAG_NAME,"a").get_attribute("title") for tag in li_tags]

        # In ra title
        for title in titles:
            print()
    except: 
        print("Error!")

# Dong webdrive
driver.quit()
