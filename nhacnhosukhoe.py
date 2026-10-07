import os
import sys
import json
from datetime import datetime, timedelta

# === TỰ ĐỘNG CÀI ĐẶT THƯ VIỆN NẾU THIẾU ===

def ensure_dependencies():
    pkgs = ["psutil"]
    if sys.platform == "win32":
        pkgs.append("pywin32")
    for pkg in pkgs:
        try:
            __import__(pkg)
        except ImportError:
            import subprocess
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "--quiet"])
            except:
                pass

ensure_dependencies()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR.startswith(("E:", "e:")):
    BASE_DIR = "D:" + BASE_DIR[2:]
if not os.path.exists(BASE_DIR):
    BASE_DIR = os.getcwd()

CONFIG_FILE = os.path.join(BASE_DIR, "app_config.json")
RESULT_JSON_FILE = os.path.join(BASE_DIR, "scheduler_results.json")
RETENTION_DAYS = 7  # Bảo lưu kết quả trong 1 tuần

def parse_date_safe(s):
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(s.strip(), fmt)
        except:
            continue
    return None

def get_data_file_path():
    """Lấy đường dẫn tệp dữ liệu cấu hình cũ nếu có (scheduler_data.json)"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                saved = cfg.get("last_data_file", "")
                if saved and os.path.exists(saved):
                    return saved
        except:
            pass
    default_json = os.path.join(BASE_DIR, "scheduler_data.json")
    if os.path.exists(default_json):
        return default_json
    return None

def run_calculation_and_export():
    """Thực hiện tính toán toàn bộ danh sách, bảng tham chiếu và các tab chuyên đề"""
    
    # Kiểm tra thời hạn bảo lưu 1 tuần của tệp kết quả cũ
    if os.path.exists(RESULT_JSON_FILE):
        try:
            with open(RESULT_JSON_FILE, "r", encoding="utf-8-sig") as f:
                old_data = json.load(f)
                saved_timestamp = old_data.get("export_timestamp", "")
                if saved_timestamp:
                    saved_dt = datetime.fromisoformat(saved_timestamp)
                    if datetime.now() - saved_dt < timedelta(days=RETENTION_DAYS):
                        print(f"📌 Kết quả JSON hiện tại vẫn trong thời hạn bảo lưu 1 tuần (từ {saved_timestamp}). Không cần tính lại.")
                        return
        except Exception as e:
            print(f"Lỗi kiểm tra tệp JSON cũ: {e}")

    # Khởi tạo dữ liệu mặc định
    people = []
    ref_numbers = []
    custom_tabs = {}

    # 1. Ưu tiên đọc từ tệp JSON dữ liệu cũ để lấy đầy đủ các tab chuyên đề và số chia cấu hình
    data_file = get_data_file_path()
    if data_file and os.path.exists(data_file):
        try:
            with open(data_file, "r", encoding="utf-8-sig") as f:
                data = json.load(f)
                people = data.get("people", []) or []
                ref_numbers = data.get("ref_numbers", []) or []
                custom_tabs = data.get("custom_tabs", {}) or {}
                print(f"📂 Đã nạp thành công dữ liệu từ tệp: {data_file}")
        except Exception as e:
            print(f"Lỗi đọc tệp dữ liệu JSON: {e}")

    # 2. Nếu tệp JSON chưa có dữ liệu hoặc thiếu, quét bổ sung từ các tệp TXT gốc
    if not people:
        dulieu_path = os.path.join(BASE_DIR, "DULIEUSK.txt")
        if os.path.exists(dulieu_path):
            try:
                with open(dulieu_path, "r", encoding="utf-8-sig") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        parts = line.split("\t")
                        if len(parts) >= 2:
                            name = parts[0].strip()
                            dob = parts[1].strip()
                            time_str = parts[2].strip() if len(parts) > 2 and ":" in parts[2] else ""
                            gender = "Nam"
                            for p_val in parts[2:]:
                                p_val_str = p_val.strip()
                                if p_val_str in ["Nam", "Nữ", "Khác", "T", "G"]:
                                    gender = "Nam" if p_val_str in ["Nam", "T"] else "Nữ"
                            people.append({"name": name, "dob": dob, "time": time_str, "gender": gender})
            except Exception as e:
                print(f"Lỗi đọc DULIEUSK.txt: {e}")
    
    if not ref_numbers:
        ref_path = os.path.join(BASE_DIR, "BANGSOTHAMCHIEU.txt")
        if os.path.exists(ref_path):
            try:
                nums = []
                with open(ref_path, "r", encoding="utf-8-sig") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        for part in line.replace(",", " ").replace(";", " ").split():
                            try:
                                n = int(part)
                                if 0 <= n <= 999:
                                    nums.append(n)
                            except:
                                pass
                ref_numbers = sorted(list(set(nums)))
            except Exception as e:
                print(f"Lỗi đọc BANGSOTHAMCHIEU.txt: {e}")

    # Nếu hoàn toàn không có tab chuyên đề nào, tạo một tab mặc định là "DULIEU" với divisor = 23
    if not custom_tabs:
        custom_tabs["DULIEU"] = {"divisor": 23, "results": []}

    ref_numbers_str = set(f"{n:03d}" for n in ref_numbers)
    ref_dt = datetime.now()

    # 3. Tiến hành tính toán cho TỪNG TAB CHUYÊN ĐỀ với số chia (`divisor`) riêng biệt của tab đó
    all_tab_results = {}
    for tab_name, tab_data in custom_tabs.items():
        divisor = int(tab_data.get("divisor", 23))
        results = []
        
        for p in people:
            dob = parse_date_safe(p["dob"])
            if not dob:
                continue
            birth_hour = int(p.get("time", "00:00").split(":")[0]) if ":" in p.get("time", "") else 0
            delta = ref_dt - dob
            if delta.total_seconds() < 0:
                delta = -delta
            
            vals = {
                "Năm": delta.days // 365,
                "Quý": delta.days // 90,
                "Tháng": delta.days // 30,
                "Tuần": delta.days // 7,
                "Ngày": delta.days,
                "Giờ": int(delta.total_seconds() // 3600),
                "Phút": int(delta.total_seconds() // 60)
            }
            
            for m_name, val in vals.items():
                if val == 0:
                    continue
                ng, du = val // divisor, val % divisor
                s_ng, s_du = f"{ng % 1000:03d}", f"{du % 1000:03d}"
                
                if s_ng in ref_numbers_str:
                    results.append({
                        "name": p["name"],
                        "metric": f"{m_name} (Nguyên)",
                        "val": val,
                        "div": divisor,
                        "ng": ng,
                        "du": du,
                        "code": s_ng,
                        "tab": tab_name,
                        "birth_hour": birth_hour
                    })
                if s_du in ref_numbers_str:
                    results.append({
                        "name": p["name"],
                        "metric": f"{m_name} (Dư)",
                        "val": val,
                        "div": divisor,
                        "ng": ng,
                        "du": du,
                        "code": s_du,
                        "tab": tab_name,
                        "birth_hour": birth_hour
                    })
        
        all_tab_results[tab_name] = {
            "divisor": divisor,
            "results": results
        }

    # 4. Đóng gói kết quả toàn bộ các tab ra tệp JSON kèm thời gian bảo lưu 1 tuần
    export_data = {
        "export_timestamp": datetime.now().isoformat(),
        "retention_days": RETENTION_DAYS,
        "total_people": len(people),
        "total_ref_numbers": len(ref_numbers),
        "tabs_calculation": all_tab_results
    }
    
    try:
        with open(RESULT_JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(export_data, f, ensure_ascii=False, indent=4)
        print(f"✅ Đã tính toán toàn bộ các tab và xuất kết quả ra tệp: {RESULT_JSON_FILE}")
    except Exception as e:
        print(f"❌ Lỗi ghi tệp JSON: {e}")

if __name__ == "__main__":
    run_calculation_and_export()
    # Tự động thoát hoàn toàn ngay sau khi xuất xong
    sys.exit(0)