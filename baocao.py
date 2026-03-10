import requests
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CẤU HÌNH ---
USER_GITHUB = "namnguyen7133-png"
KHO_TEP = "Dien_thoai"
EMAIL_GUI = "namnguyen7133@gmail.com"
EMAIL_NHAN = "namnguyen7133@gmail.com"

# Lấy mật khẩu ứng dụng từ GitHub Secrets (biến môi trường)
MAT_KHAU_APP = os.getenv('MY_EMAIL_PASS') 

def quet_va_gui():
    print("🤖 Đang quét hệ thống...")
    
    # URL API để lấy danh sách tệp trong repo
    url = f"https://api.github.com/repos/{USER_GITHUB}/{KHO_TEP}/contents/"
    
    try:
        res = requests.get(url)
        
        if res.status_code == 200:
            files = res.json()
            # Chỉ lấy các tệp có đuôi .html
            danh_sach = [f['name'] for f in files if isinstance(f, dict) and f['name'].endswith('.html')]
            
            # Soạn nội dung email
            noidung = f"Chào anh Nam,\n\nRobot Tâm Linh đã cập nhật trạng thái kho tệp:\n"
            noidung += f"📍 Tổng số tệp HTML hiện có: {len(danh_sach)}\n"
            noidung += "-"*35 + "\n"
            
            for i, ten in enumerate(danh_sach, 1):
                noidung += f"{i}. {ten}\n"
            
            noidung += f"\n🔗 Xem trực tiếp tại: https://{USER_GITHUB}.github.io/{KHO_TEP}/"
            
            # Thiết lập Email
            msg = MIMEMultipart()
            msg['From'] = EMAIL_GUI
            msg['To'] = EMAIL_NHAN
            msg['Subject'] = f"🔔 BÁO CÁO HỆ THỐNG HTML ({len(danh_sach)} TỆP)"
            msg.attach(MIMEText(noidung, 'plain', 'utf-8'))
            
            # Gửi Email qua SMTP Gmail
            if not MAT_KHAU_APP:
                print("❌ Lỗi: Không tìm thấy biến môi trường MY_EMAIL_PASS!")
                return

            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(EMAIL_GUI, MAT_KHAU_APP)
            server.send_message(msg)
            server.quit()
            print("✅ Đã gửi báo cáo vào Gmail thành công!")
            
        else:
            print(f"❌ Lỗi kết nối GitHub (Status: {res.status_code}): {res.text}")
            
    except Exception as e:
        print(f"❌ Có lỗi xảy ra: {e}")

if __name__ == "__main__":
    quet_va_gui()
