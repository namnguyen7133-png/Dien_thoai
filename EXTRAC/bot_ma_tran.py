import json
import datetime
import requests

# 1. ĐỌC DỮ LIỆU TỪ JSON
with open("database.json", "r", encoding="utf-8") as f:
    data = json.load(f)

members = data["danh_sach_32_nguoi"]
special_nums = data["so_dac_biet"]
ma_thang = data["ma_thang"]
pb_token = "o.dvjnPqSpLbPFkvPFAQEx9lvHjDQyhfJ2" # Token của anh

def calculate_logic(ngay_sinh, phut_hien_tai, ma_thang):
    # Đây là nơi anh dán công thức toán học ma trận của anh vào
    # Ví dụ tạm thời: (Ngày + Tháng + Năm + Phút + Mã Tháng) % 1000
    try:
        d, m, y = map(int, ngay_sinh.split('/'))
        res = (d + m + y + phut_hien_tai + ma_thang) % 1000
        return res
    except:
        return 0

def run_task():
    now = datetime.datetime.now()
    phut_ht = now.hour * 60 + now.minute
    alert_list = []

    for m in members:
        ket_qua = calculate_logic(m["ngay_sinh"], phut_ht, ma_thang)
        if ket_qua in special_nums:
            alert_list.append(f"- {m['id']}: số {ket_qua}")

    if alert_list:
        msg = f"⚠️ CẢNH BÁO MA TRẬN ({now.strftime('%H:%M')})\n" + "\n".join(alert_list)
        requests.post('https://api.pushbullet.com/v2/pushes', 
                      headers={'Access-Token': pb_token},
                      json={'type': 'note', 'title': 'Hệ thống Ma Trận', 'body': msg})
        print("Đã gửi thông báo!")
    else:
        print("Không có số đặc biệt nào.")

if __name__ == "__main__":
    run_task()