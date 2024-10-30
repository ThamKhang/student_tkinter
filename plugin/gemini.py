import tkinter as tk
from tkinter import scrolledtext
import requests
import json
import sqlite3

# Đặt URL và API Key
url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent'
api_key = 'AIzaSyBnqnqYFoPDneBpfjSRdr97ncDOOhhvsf4'  # Thay bằng API Key của bạn

# Đặt prompt tùy chỉnh ở đây
CUSTOM_PROMPT = "Bạn là một trợ lý AI."


class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat với Gemini")
        self.root.geometry("400x600")

        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', bg="#F0F0F0")
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.user_input = tk.Entry(root, bg="#FFFFFF")
        self.user_input.pack(padx=10, pady=(0, 10), fill=tk.X)
        self.user_input.bind('<Return>', self.send_message)

        self.send_button = tk.Button(root, text="Gửi", command=self.send_message, bg="#007BFF", fg="white")
        self.send_button.pack(padx=10, pady=(0, 10))

        # Tải dữ liệu từ student.db khi khởi động ứng dụng
        self.load_data_from_db()

    def load_data_from_db(self):
        db_path = '../student_management/student_data.db'  # Đường dẫn đến tệp cơ sở dữ liệu của bạn
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Truy vấn dữ liệu từ bảng cần thiết, ví dụ: bảng student
            cursor.execute("SELECT * FROM student")  # Thay đổi tên bảng theo cấu trúc của bạn
            rows = cursor.fetchall()

            # Tạo một chuỗi từ dữ liệu truy xuất được
            data_content = "\n".join([str(row) for row in rows])
            self.display_message("Dữ liệu đã tải lên: \n" + data_content)

            # Gửi dữ liệu đến API Gemini
            self.get_response(data_content)

            # Đóng kết nối
            conn.close()
        except Exception as e:
            self.display_message("Lỗi khi tải dữ liệu: " + str(e))

    def send_message(self, event=None):
        user_message = self.user_input.get()

        if user_message.strip():
            full_message = f"{CUSTOM_PROMPT}: {user_message}"

            self.display_message("Bạn: " + user_message)
            self.user_input.delete(0, tk.END)
            self.get_response(full_message)

    def get_response(self, message):
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": message
                        }
                    ]
                }
            ]
        }

        headers = {
            'Content-Type': 'application/json',
        }

        try:
            response = requests.post(f"{url}?key={api_key}", headers=headers, data=json.dumps(payload))
            if response.status_code == 200:
                response_data = response.json()
                gemini_message = response_data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get(
                    'text', 'Không có phản hồi.')
                self.display_message("Gemini: " + gemini_message.strip())
            else:
                self.display_message(f"Lỗi: {response.status_code} - {response.text}")
        except Exception as e:
            self.display_message("Lỗi kết nối: " + str(e))

    def display_message(self, message):
        self.chat_area.configure(state='normal')
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.configure(state='disabled')
        self.chat_area.yview(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    chat_app = ChatApp(root)
    root.mainloop()
