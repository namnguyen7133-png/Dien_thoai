import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Tải dữ liệu công thức
with open(r'E:\HTML\database.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    topic = data.get('topic')
    inputs = data.get('inputs') # Dạng dictionary: {'traffic': 1000, ...}
    
    if topic in db:
        # Thực hiện tính toán dựa trên công thức lưu trong JSON
        # Lưu ý: Sử dụng eval() cẩn thận trong môi trường thực tế
        try:
            context = inputs
            result = eval(db[topic]['formula'].split('=')[1], {"__builtins__": None}, context)
            return jsonify({"reply": f"Kết quả bài toán {topic} của bạn là: {result:.2f}"})
        except Exception as e:
            return jsonify({"reply": "Lỗi tính toán: hãy kiểm tra lại các con số."})
    
    return jsonify({"reply": "Tôi chưa có công thức cho chủ đề này."})