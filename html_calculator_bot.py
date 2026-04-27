import tkinter as tk
from tkinter import filedialog, messagebox
from bs4 import BeautifulSoup
import re

def analyze_html():
    files = filedialog.askopenfilenames(filetypes=[("HTML files","*.html")])

    if not files:
        return

    total_numbers = []
    report = ""

    for path in files:
        with open(path,"r",encoding="utf-8",errors="ignore") as f:
            soup = BeautifulSoup(f,"html.parser")

        text = soup.get_text()

        numbers = re.findall(r'\d+\.?\d*', text)
        numbers = [float(n) for n in numbers]

        total_numbers += numbers

        report += f"\nFILE: {path}\n"
        report += f"Số tìm được: {len(numbers)}\n"

    total = sum(total_numbers)

    result_text.delete("1.0",tk.END)
    result_text.insert(tk.END, report)
    result_text.insert(tk.END,"\n=================\n")
    result_text.insert(tk.END,f"Tổng tất cả số: {total}\n")
    result_text.insert(tk.END,f"Tổng số lượng số: {len(total_numbers)}")

root = tk.Tk()
root.title("Robot phân tích HTML")

btn = tk.Button(root,text="Chọn tệp HTML",command=analyze_html,font=("Arial",12))
btn.pack(pady=10)

result_text = tk.Text(root,width=80,height=25)
result_text.pack()

root.mainloop()