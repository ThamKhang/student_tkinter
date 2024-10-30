import os
import pandas as pd
from openpyxl import load_workbook
import tkinter as tk
from tkinter import filedialog, messagebox

from plugin.file_format_plugin import open_format_file_window
from student_management.main import main_window
from utils import center_window  # Nhập hàm center_window



def convert_xls_to_xlsx(file_path):
    """Chuyển đổi file .xls thành .xlsx."""
    new_file_path = file_path.replace('.xls', '.xlsx')
    try:
        # Sử dụng pandas để chuyển đổi
        df = pd.read_excel(file_path)
        df.to_excel(new_file_path, index=False)
        return new_file_path
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể chuyển đổi {file_path}: {str(e)}")
        return None


def rename_excel_files_in_directory(entry_directory_path):
    directory_path = entry_directory_path.get()

    if not directory_path:
        messagebox.showerror("Lỗi", "Vui lòng chọn thư mục chứa file Excel.")
        return

    try:
        # Duyệt qua tất cả file trong thư mục
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)

            if filename.endswith('.xls'):
                # Chuyển đổi file .xls thành .xlsx
                new_file_path = convert_xls_to_xlsx(file_path)
                if new_file_path:
                    filename = new_file_path  # Cập nhật tên file thành file mới đã chuyển đổi

            if filename.endswith(('.xlsx', '.xls')) and os.path.isfile(file_path):
                # Tải file Excel
                workbook = load_workbook(file_path)
                sheet = workbook.active  # Lấy sheet đầu tiên

                # Lấy giá trị ô C8
                new_name = sheet['C8'].value

                # Kiểm tra nếu giá trị ô C8 không rỗng
                if new_name:
                    # Thay đổi tên file
                    new_file_path = os.path.join(directory_path, f"{new_name}.xlsx")
                    os.rename(file_path, new_file_path)
                    messagebox.showinfo("Thành công", f"Đã đổi tên: {filename} thành {new_name}.xlsx")
                else:
                    messagebox.showwarning("Cảnh báo", f"Ô C8 rỗng trong file: {filename}. Không thể đổi tên.")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")


def select_directory(entry_directory_path):
    directory_path = filedialog.askdirectory()
    if directory_path:
        entry_directory_path.delete(0, tk.END)
        entry_directory_path.insert(0, directory_path)


def show_selection_window():
    # Tạo cửa sổ mới cho việc lựa chọn
    selection_win = tk.Tk()
    selection_win.title("Chọn chức năng")
    selection_win.configure(bg="#f0f0f0")
    center_window(selection_win, 400, 200)

    tk.Label(selection_win, text="Chọn chức năng:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)

    # Nút để vào giao diện chính
    button_main = tk.Button(selection_win, text="Vào giao diện chính", font=("Arial", 12), bg="#007bff", fg="white",
                            command=open_main_window)
    button_main.pack(pady=10)

    # Nút để vào chức năng chuyển đổi và đổi tên file Excel
    button_format_file = tk.Button(selection_win, text="Chuyển đổi và đổi tên file Excel", font=("Arial", 12), bg="#007bff",
                                   fg="white", command=open_format_file_window)
    button_format_file.pack(pady=10)

    selection_win.mainloop()


def login():
    username = entry_username.get()
    password = entry_password.get()
    if username == "admin" and password == "123":
        login_win.destroy()  # Đóng cửa sổ đăng nhập
        show_selection_window()  # Mở giao diện chọn chức năng
    else:
        error_label.config(text="Invalid credentials!", fg="red")


def show_selection_window():
    # Tạo cửa sổ mới cho việc lựa chọn
    selection_win = tk.Tk()
    selection_win.title("Chọn chức năng")
    selection_win.configure(bg="#f0f0f0")
    center_window(selection_win, 400, 200)

    tk.Label(selection_win, text="Chọn chức năng:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)

    # Nút để vào giao diện chính
    button_main = tk.Button(selection_win, text="Vào giao diện chính", font=("Arial", 12), bg="#007bff", fg="white",
                            command=open_main_window)
    button_main.pack(pady=10)

    # Nút để vào chức năng chuyển đổi file
    button_format_file = tk.Button(selection_win, text="Chuyển đổi file XLS", font=("Arial", 12), bg="#007bff",
                                   fg="white", command=open_format_file_window)
    button_format_file.pack(pady=10)

    selection_win.mainloop()


def open_main_window():
    main_window()  # Gọi hàm mở giao diện chính


def login_window():
    global login_win, entry_username, entry_password, error_label
    login_win = tk.Tk()
    login_win.title("Login")
    login_win.configure(bg="#f0f0f0")
    center_window(login_win, 1200, 800)

    frame = tk.Frame(login_win, bg="#f0f0f0")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame, text="Username", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5)
    entry_username = tk.Entry(frame, font=("Arial", 12))
    entry_username.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame, text="Password", font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=5)
    entry_password = tk.Entry(frame, show="*", font=("Arial", 12))
    entry_password.grid(row=1, column=1, padx=10, pady=5)

    tk.Button(frame, text="Login", font=("Arial", 12), bg="#007bff", fg="white", command=login).grid(row=2, column=1,
                                                                                                     padx=10, pady=10)
    error_label = tk.Label(frame, text="", font=("Arial", 10), bg="#f0f0f0")
    error_label.grid(row=3, column=1, pady=5)

    login_win.mainloop()


# Gọi hàm để mở cửa sổ đăng nhập
login_window()
