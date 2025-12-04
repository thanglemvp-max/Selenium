from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import re
import sys 

sys.stdout.reconfigure(encoding='utf-8')
# --- HÀM LÀM SẠCH ---
def clean_text(text):
    if not text: return ""
    # Xóa số tham chiếu [1], [2]...
    text = re.sub(r'\[\d+\]', '', text)
    return text.strip()

# --- CẤU HÌNH ---
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

url = 'https://vi.wikipedia.org/wiki/Danh_s%C3%A1ch_tr%C6%B0%E1%BB%9Dng_%C4%91%E1%BA%A1i_h%E1%BB%8Dc_t%E1%BA%A1i_Vi%E1%BB%87t_Nam'
driver.get(url)

print("Đang xử lý dữ liệu thông minh...")
tat_ca_dong = driver.find_elements(By.XPATH, "//table[contains(@class, 'wikitable')]//tr")

ket_qua = []

# Những từ khóa để nhận diện Tên trường
tu_khoa_truong = ["Trường", "Học viện", "Đại học", "Khoa", "Viện", "Phân hiệu", "Trung tâm"]

for dong in tat_ca_dong:
    cols = dong.find_elements(By.TAG_NAME, "td")
    
    if len(cols) > 2:
        # Lấy nội dung text của cả dòng
        texts = [clean_text(c.text) for c in cols]
        
        idx_ten = -1 # Vị trí cột chứa Tên trường
        
        # --- LOGIC MỚI: QUÉT TỪNG CỘT ĐỂ TÌM TỪ KHÓA ---
        for i, text in enumerate(texts):
            # Nếu ô này chứa từ khóa (VD: bắt đầu bằng "Trường...")
            # Và ô này không quá ngắn (tránh nhầm chữ viết tắt)
            if any(text.startswith(tk) for tk in tu_khoa_truong) and len(text) > 5:
                
                # Mẹo xử lý trường hợp "Đại học Quốc gia" (Trường mẹ) và "Trường ĐH KHXH&NV" (Trường con)
                # Nếu tìm thấy rồi, nhưng cột BÊN PHẢI nó cũng lại là Tên trường nữa -> Ưu tiên cột bên phải (chi tiết hơn)
                if i + 1 < len(texts):
                    text_next = texts[i+1]
                    if any(text_next.startswith(tk) for tk in tu_khoa_truong):
                        idx_ten = i + 1 # Lấy trường con
                        break
                
                idx_ten = i # Lấy trường hiện tại
                break 
        
        # Nếu tìm thấy vị trí tên trường
        if idx_ten != -1:
            ten_truong = texts[idx_ten]
            
            # Mã trường thường nằm ngay sau Tên trường
            ma_truong = texts[idx_ten + 1] if (idx_ten + 1) < len(texts) else ""
            
            # Năm lập thường nằm sau Mã trường
            nam_lap = texts[idx_ten + 2] if (idx_ten + 2) < len(texts) else ""

            ket_qua.append({
                "Tên trường": ten_truong,
                "Mã trường": ma_truong,
                "Năm thành lập": nam_lap
            })

driver.quit()

# --- XUẤT KẾT QUẢ ---
if ket_qua:
    df = pd.DataFrame(ket_qua)
    print("\n--- KẾT QUẢ MỚI (Đã sửa lỗi lệch dòng) ---")
    print(df.head(10))
    df.to_excel("DaiHoc_FixLoi.xlsx", index=False)
else:
    print("Không tìm thấy dữ liệu.")