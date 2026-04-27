import os

def day_html_thoi():
    print("--- DỌN DẸP VÀ CHỈ ĐẨY FILE HTML ---")
    
    # 1. Hủy bỏ những gì đang gom dở (nếu bị kẹt file rác)
    os.system("git rm -r --cached .")
    
    # 2. Chỉ thêm các file .html và file cấu hình cần thiết
    os.system("git add *.html")
    os.system("git add .github/") 
    
    # 3. Commit
    os.system('git commit -m "Chi day cac file HTML quan trong"')
    
    # 4. Đẩy lên mạng
    print("--- ĐANG ĐẨY LÊN GITHUB ---")
    os.system("git push origin main")

if __name__ == "__main__":
    day_html_thoi()