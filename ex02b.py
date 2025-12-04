from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time
import pandas as pd
import sys

# --- CẤU HÌNH ---
# (Giữ nguyên phần này của bạn)
try:
    sys.stdout.reconfigure(encoding='utf-8')
except:
    pass

gecko_path = r"D:\Python\29-11-2025\geckodriver.exe"
ser = Service(gecko_path)
options = webdriver.firefox.options.Options()
options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
options.headless = False

try:
    driver = webdriver.Firefox(options=options, service=ser)
except Exception as e:
    print(f"Lỗi mở trình duyệt: {e}")
    sys.exit()

# --- TRUY CẬP ---
url = 'https://gochek.vn/collections/all'
print(f"Đang vào: {url}")
driver.get(url)
time.sleep(3)

# Tắt popup (nếu có)
try:
    driver.find_element(By.CSS_SELECTOR, "#close-popup, .modal-close, button.close-window").click()
    time.sleep(1)
except:
    pass

# --- CUỘN TRANG (Quan trọng để load ảnh) ---
print("Đang cuộn trang...")
body = driver.find_element(By.TAG_NAME, "body")
for i in range(25): # Cuộn nhiều hơn chút
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.5)
driver.execute_script("window.scrollTo(0, 0);") # Cuộn lại lên đầu
time.sleep(2)

# --- LẤY DỮ LIỆU ---
stt = []
ten_san_pham = []
gia_ban = []
hinh_anh = []

# Tìm khối sản phẩm (Class 'product-block' có vẻ vẫn đúng vì bạn lấy được Tên)
product_cards = driver.find_elements(By.CLASS_NAME, "product-block")
print(f"Tìm thấy {len(product_cards)} sản phẩm. Bắt đầu bóc tách...")

for i, card in enumerate(product_cards, 1):
    try:
        # 1. LẤY TÊN (Giữ nguyên vì đã chạy đúng)
        try:
            tsp = card.find_element(By.CSS_SELECTOR, "h3 a, .pro-name a").text
        except:
            tsp = "Không tên"

        # 2. LẤY GIÁ (SỬA ĐỔI: Dùng selector đa năng)
        # Tìm bất kỳ class nào có chữ 'price'
        try:
            # Thử tìm thẻ có class chứa chữ "price"
            price_element = card.find_element(By.CSS_SELECTOR, ".price, .pro-price, .current-price, .p-price")
            gsp = price_element.text.strip()
            if not gsp: # Nếu text rỗng, thử tìm thẻ cha
                gsp = card.find_element(By.CLASS_NAME, "box-pro-prices").text.strip()
        except:
            gsp = "Liên hệ"

        # 3. LẤY ẢNH (SỬA ĐỔI: Tìm thẻ img trực tiếp)
        try:
            # Tìm thẻ img bất kỳ trong card (không quan tâm class cha là gì)
            img_tag = card.find_element(By.TAG_NAME, "img")
            
            # Logic lấy link ảnh: ưu tiên srcset > data-src > src
            srcset = img_tag.get_attribute('srcset')
            data_src = img_tag.get_attribute('data-src')
            src = img_tag.get_attribute('src')

            if srcset:
                ha = srcset.split(",")[0].split(" ")[0] # Lấy link đầu tiên trong chuỗi
            elif data_src:
                ha = data_src
            else:
                ha = src

            # Nếu lấy nhầm ảnh icon/base64, xóa đi
            if ha and ("base64" in ha or "data:image" in ha):
                 ha = ""
            
            # Fix lỗi thiếu https
            if ha and ha.startswith("//"):
                ha = "https:" + ha
                
        except:
            ha = ""

        # Lưu dữ liệu
        stt.append(i)
        ten_san_pham.append(tsp)
        gia_ban.append(gsp)
        hinh_anh.append(ha)
        
        # In kiểm tra ngay lập tức xem có lấy được không
        print(f"SP {i}: {tsp} | Giá: {gsp} | Ảnh: {'Có' if ha else 'KHÔNG'}")

    except Exception as e:
        print(f"Lỗi dòng {i}: {e}")
        continue

# --- XUẤT FILE ---
df = pd.DataFrame({
    "STT": stt,
    "Tên sản phẩm": ten_san_pham,
    "Giá bán": gia_ban,
    "Hình ảnh": hinh_anh
})

file_name = 'danh_sach_gochek_fixed.xlsx'
df.to_excel(file_name, index=False)
print(f"\nĐã xuất file: {file_name}")

driver.quit()