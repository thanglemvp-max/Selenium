from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import getpass
import sys 

# --- CẤU HÌNH ---
sys.stdout.reconfigure(encoding='utf-8')
gecko_path = r"D:\Python\29-11-2025\geckodriver.exe"

print("--- TOOL ĐĂNG NHẬP LMS HUTECH (FIX) ---")
MY_EMAIL = input("Nhập Email/MSSV: ")
MY_PASSWORD = getpass.getpass("Nhập Mật khẩu: ") 

# Khởi tạo driver
ser = Service(gecko_path)
options = webdriver.firefox.options.Options()
options.binary_location = "C:/Program Files/Mozilla Firefox/firefox.exe"
options.headless = False 

driver = webdriver.Firefox(options=options, service=ser)
wait = WebDriverWait(driver, 20)

try:
    # 1. THAY ĐỔI QUAN TRỌNG: Vào thẳng link đăng nhập, bỏ qua trang chủ
    target_url = 'https://apps.lms.hutech.edu.vn/authn/login'
    print(f"1. Đang truy cập thẳng vào: {target_url}")
    driver.get(target_url)
    
    # Chờ 3 giây để trang ổn định
    time.sleep(3)
    current_url = driver.current_url

    # 2. KIỂM TRA & XỬ LÝ
    # Trường hợp A: Trang đăng nhập nội bộ HUTECH (Form màu trắng)
    if "authn/login" in current_url:
        print(">> Phát hiện form đăng nhập nội bộ.")
        
        # Điền User/Email
        print("   - Đang điền tên đăng nhập...")
        user_box = wait.until(EC.visibility_of_element_located((By.ID, "emailOrUsername")))
        user_box.clear()
        user_box.send_keys(MY_EMAIL)
        
        # Điền Pass
        print("   - Đang điền mật khẩu...")
        pass_box = driver.find_element(By.ID, "password")
        pass_box.clear()
        pass_box.send_keys(MY_PASSWORD)
        
        # Click nút Đăng nhập
        print("   - Click nút đăng nhập...")
        btn_login = driver.find_element(By.ID, "sign-in")
        btn_login.click()

    # Trường hợp B: Trang Microsoft (Nếu nó tự chuyển tiếp)
    elif "microsoft" in current_url:
        print(">> Phát hiện form Microsoft.")
        
        email_box = wait.until(EC.visibility_of_element_located((By.NAME, "loginfmt")))
        email_box.send_keys(MY_EMAIL)
        driver.find_element(By.ID, "idSIButton9").click() # Next
        
        time.sleep(2)
        
        pass_box = wait.until(EC.visibility_of_element_located((By.NAME, "passwd")))
        pass_box.send_keys(MY_PASSWORD)
        driver.find_element(By.ID, "idSIButton9").click() # Sign in
        
        # Nhấn Yes nếu hỏi duy trì đăng nhập
        try:
            time.sleep(1)
            driver.find_element(By.ID, "idSIButton9").click()
        except:
            pass

    # 3. KIỂM TRA KẾT QUẢ
    time.sleep(10)

except Exception as e:
    print(f"\n[LỖI]: {e}")

finally:
    driver.quit()