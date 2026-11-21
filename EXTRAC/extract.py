import json

# 1. DANH SÁCH 32 NGƯỜI ANH CUNG CẤP (Đã được xử lý định dạng)
danh_sach_tho = [
    "NGUYENKHACNANG|04/06/1944", "TOTHIHA|29/08/1948", "NGUYENMINHNAM|03/03/1971",
    "THANTHIKIMANH|23/09/1981", "NGUYENTONGANAN|28/09/2014", "NGUYENTOMINHCHAU|25/07/2016",
    "NGUYENTOBICHNGOC|05/02/2020", "NGUYENTHIMINHHANG|07/01/1974", "NGOQUYCUONG|23/05/1973",
    "NGOGIABACH|12/10/2000", "NGOGIALINH|05/04/2005", "NGUYENTHIMINHPHUONG|06/11/1978",
    "HOANGANHDUNG|21/09/1978", "HOANGHAIVINH|03/06/2010", "HOANGTHIENBACHANH|14/11/2015",
    "TOKIMHUE|09/08/1960", "NGUYENTUANANH|23/10/1983", "NGUYENTHEANH|24/03/2001",
    "NGOTHIMAI|12/12/1948", "TOVIETHUNG|17/06/1996", "TOTHIHONG|10/10/1964",
    "VUVANHIEP|24/04/1974", "NGUYENTHICHI|08/02/1946", "NGUYENTANBAC|30/11/1957",
    "NGUYENTHITAM|08/08/1954", "THANVANGIU|18/04/1955", "NGUYENTHIBINH|21/05/1958",
    "THANTHIBICHNGUYET|21/05/1980", "THANVANTUAN|21/05/1983", "THANYENNHI|26/03/2010",
    "LETHIPHUONG|26/06/1990", "NGUYENHOAINAM|02/06/2004"
]

def tao_database():
    # 2. BỘ SỐ ĐẶC BIỆT TỔNG LỰC (Không bỏ sót số nào của anh)
    special_numbers = [
        307, 14, 41, 72, 627, 168, 111, 222, 333, 444, 555, 666, 777, 888, 999,
        123, 234, 345, 456, 567, 678, 789, 1234, 159, 285, 258, 492, 816, 357, 
        195, 186, 267, 276, 249, 294, 375, 384, 348, 438, 483, 429, 528, 582, 
        537, 573, 519, 591, 672, 618, 681, 726, 762, 735, 753, 825, 852, 861, 
        843, 834, 915, 951, 924, 942
    ]

    members = []
    for item in danh_sach_tho:
        parts = item.split('|')
        members.append({
            "id": parts[0],
            "ngay_sinh": parts[1]
        })

    database = {
        "ma_thang": 4, # Anh có thể sửa số này hàng tháng
        "so_dac_biet": sorted(list(set(special_numbers))),
        "danh_sach_32_nguoi": members
    }

    # Xuất ra file JSON
    with open("database.json", "w", encoding="utf-8") as f:
        json.dump(database, f, ensure_ascii=False, indent=4)
    
    print("--- THANH CONG ---")
    print(f"Da tao file database.json voi {len(members)} nguoi.")
    print("Anh co the dung file nay de chay GitHub Actions.")

if __name__ == "__main__":
    tao_database()