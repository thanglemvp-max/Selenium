from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

# --- 1. CẤU HÌNH ---
print("Đang khởi động...")
options = Options()
# Giả danh User-Agent để tránh bị chặn và có giao diện chuẩn
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
# Tắt thông báo
options.add_argument("--disable-notifications")

driver = webdriver.Chrome(options=options)

try:
    url = 'https://www.reddit.com/r/Python/'
    print(f"Đang vào: {url}")
    driver.get(url)
    time.sleep(5) 

    # --- 2. SỬA LỖI TẠI ĐÂY: CUỘN TRANG BẰNG JAVASCRIPT ---
    print("Đang cuộn trang...")
    
    # Cuộn 5 lần
    for i in range(5):
        # Lệnh này bảo trình duyệt: "Cuộn xuống đáy trang hiện tại đi"
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print(f"-> Đã cuộn lần {i+1}")
        time.sleep(3) # Reddit cần nghỉ lâu chút để load React

    # --- 3. CÀO DỮ LIỆU ---
    print("Đang đọc dữ liệu...")
    data_list = []
    
    # Tìm thẻ bài viết. Reddit dùng nhiều loại thẻ, ta quét nhiều trường hợp
    # Cách an toàn nhất: Tìm thẻ tiêu đề (thường là H3 hoặc shreddit-post)
    
    # Thử tìm thẻ shreddit-post trước (Giao diện mới)
    posts = driver.find_elements(By.TAG_NAME, "shreddit-post")
    
    if len(posts) > 0:
        print(f"Phát hiện giao diện mới (Shreddit). Tìm thấy {len(posts)} bài.")
        for post in posts:
            try:
                title = post.get_attribute("post-title")
                author = post.get_attribute("author")
                link = post.get_attribute("content-href")
                if title:
                    data_list.append({"Tiêu đề": title, "Tác giả": author, "Link": link})
            except: continue
            
    else:
        # Nếu không thấy shreddit-post, tìm thẻ H3 (Giao diện cũ/React)
        print("Phát hiện giao diện React cũ. Tìm theo thẻ H3.")
        titles = driver.find_elements(By.TAG_NAME, "h3")
        for t in titles:
            try:
                text = t.text.strip()
                if len(text) > 5:
                    # Cố gắng lấy link từ thẻ cha
                    try:
                        parent = t.find_element(By.XPATH, "./..")
                        link = parent.get_attribute("href")
                    except: link = ""
                    
                    data_list.append({"Tiêu đề": text, "Tác giả": "N/A", "Link": link})
            except: continue

    # --- 4. KẾT QUẢ ---
    if data_list:
        df = pd.DataFrame(data_list)
        print("\n--- KẾT QUẢ ---")
        print(df.head(10))
    else:
        print("Không tìm thấy dữ liệu (Reddit đã chặn hoặc đổi cấu trúc).")

except Exception as e:
    print(f"Lỗi: {e}")

finally:
    driver.quit()