from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re 
import sys

# --- FIX LỖI FONT TIẾNG VIỆT TRÊN WINDOWS ---
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass # Bỏ qua nếu phiên bản python cũ ko hỗ trợ

# --- CẤU HÌNH ---
# Khởi tạo DataFrame rỗng
d = pd.DataFrame({'name':[], 'birth':[], 'death': [], 'nationality':[]})
all_links = []

# Khởi tạo Webdriver 1 lần duy nhất
driver = webdriver.Chrome()

# --- I. LẤY LINK PROFILES ---
print("Dang lay danh sach link...") # Viết không dấu để an toàn tuyệt đối nếu máy vẫn lỗi

for i in range(70, 71): # Chữ cái 'F'
    url = "https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_%22"+chr(i)+"%22"
    try: 
        driver.get(url)
        time.sleep(2)

        # Tìm div chứa nội dung chính
        content_div = driver.find_element(By.ID, "mw-content-text")
        
        # Lấy tất cả thẻ <li> nằm trong vùng nội dung
        links_elements = content_div.find_elements(By.CSS_SELECTOR, "div.mw-category li a")
        
        # Dự phòng nếu cấu trúc web khác
        if not links_elements:
             links_elements = content_div.find_elements(By.CSS_SELECTOR, "ul li a")

        for tag in links_elements:
            href = tag.get_attribute("href")
            if href:
                all_links.append(href)
        
        print(f"Tim thay {len(all_links)} hoa si.")

    except Exception as e:
        print(f"Loi khi lay danh sach link: {e}")

# --- II. LẤY THÔNG TIN CHI TIẾT ---
print("Bat dau cao thong tin chi tiet...")

# all_links = all_links[:5] # Bỏ comment dòng này nếu muốn test nhanh 5 người đầu

for link in all_links:
    print(f"Dang xu ly: {link}")
    try:
        driver.get(link)
        time.sleep(1) 

        # 1. Lấy tên
        try: 
            name = driver.find_element(By.TAG_NAME, "h1").text 
        except:
            name = "N/A"
        
        # 2. Lấy ngày sinh
        try: 
            birth_element = driver.find_element(By.XPATH, "//th[text()='Born']/following-sibling::td")
            birth_text = birth_element.text
            found_birth = re.findall(r'[0-9]{1,2}\s+[A-Za-z]+\s+[0-9]{4}', birth_text)
            birth = found_birth[0] if found_birth else birth_text 
        except:
            birth = "N/A"
        
        # 3. Lấy ngày mất
        try:
            death_element = driver.find_element(By.XPATH, "//th[text()='Died']/following-sibling::td")
            death_text = death_element.text
            found_death = re.findall(r'[0-9]{1,2}\s+[A-Za-z]+\s+[0-9]{4}', death_text)
            death = found_death[0] if found_death else death_text
        except:
            death = "N/A"

        # 4. Lấy quốc tịch
        try:
            nationality_element = driver.find_element(By.XPATH, "//th[contains(text(),'Nationality') or contains(text(),'Citizenship')]/following-sibling::td")
            nationality = nationality_element.text
        except:
            nationality = "N/A"

        # Thêm vào DF
        painter = {'name': name, 'birth': birth, 'death': death, 'nationality': nationality}
        d = pd.concat([d, pd.DataFrame([painter])], ignore_index=True)

    except Exception as e:
        print(f"Loi: {e}")
        continue

driver.quit()

# --- III. XUẤT FILE ---
print(d)
file_name = 'Painters_Fixed.xlsx'
d.to_excel(file_name, index=False)
print('Xuat file Excel thanh cong!')