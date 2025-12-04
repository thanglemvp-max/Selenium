from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')
# --- 1. GIỮ NGUYÊN PHẦN KHỞI TẠO ---
driver = webdriver.Chrome()

# --- 2. THAY ĐỔI: KHÔNG CẦN ĐĂNG NHẬP ---
# Cào dữ liệu công khai thì không cần đăng nhập (tránh bị khóa nick)
# Truy cập thẳng vào một nhóm (ví dụ nhóm Lập trình Python)
url = 'https://www.reddit.com/r/Python/'
driver.get(url)
time.sleep(3)

# --- 3. SỬA LẠI ACTIONCHAINS (ĐỂ CUỘN TRANG) ---
# Code cũ của bạn dùng TAB để nhảy ô. Code cào dùng PAGE_DOWN để tải thêm bài.
print("Đang cuộn trang...")
action = ActionChains(driver)

for i in range(5): # Cuộn 5 lần
    action.send_keys(Keys.PAGE_DOWN).perform()
    time.sleep(2) # Nghỉ chút cho bài mới hiện ra

# --- 4. THÊM LOGIC CÀO DỮ LIỆU (QUAN TRỌNG NHẤT) ---
print("Đang đọc dữ liệu...")

# Tìm tất cả các thẻ bài viết (Reddit dùng thẻ shreddit-post)
posts = driver.find_elements(By.TAG_NAME, "shreddit-post")

danh_sach_bai = []

for post in posts:
    try:
        # Thay vì send_keys (nhập), ta dùng get_attribute (đọc)
        tieu_de = post.get_attribute("post-title")
        tac_gia = post.get_attribute("author")
        so_vote = post.get_attribute("score")
        
        # Chỉ lấy bài có tiêu đề
        if tieu_de:
            danh_sach_bai.append({
                "Tiêu đề": tieu_de,
                "Tác giả": tac_gia,
                "Vote": so_vote
            })
            print(f"-> Đã lấy: {tieu_de[:50]}...") # In thử 50 ký tự đầu
    except:
        continue

# --- 5. XUẤT RA EXCEL ---
driver.quit()

if danh_sach_bai:
    df = pd.DataFrame(danh_sach_bai)
    print("\n--- KẾT QUẢ ---")
    print(df.head())
    # df.to_excel("ket_qua_cao_du_lieu.xlsx", index=False)
else:
    print("Không cào được gì cả.")