import os
import pandas as pd
from openpyxl import load_workbook
import tkinter as tk
from tkinter import filedialog, messagebox

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

def rename_excel_files_in_directory(directory_path):
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
                    file_path = new_file_path  # Cập nhật tên file thành file mới đã chuyển đổi

            if file_path.endswith(('.xlsx', '.xls')):
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
                    messagebox.showinfo("Thành công", f"Đã đổi tên: {file_path} thành {new_name}.xlsx")
                else:
                    messagebox.showwarning("Cảnh báo", f"Ô C8 rỗng trong file: {file_path}. Không thể đổi tên.")
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

def select_directory(entry_widget):
    directory_path = filedialog.askdirectory()
    if directory_path:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, directory_path)


def center_window(win, width, height):
    # Lấy kích thước màn hình
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    # Tính toán tọa độ x, y để căn giữa
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # Đặt kích thước và vị trí cho cửa sổ
    win.geometry(f'{width}x{height}+{x}+{y}')


def open_format_file_window():
    # Cửa sổ đổi tên file
    format_win = tk.Toplevel()
    format_win.title("Đổi tên file Excel trong thư mục")
    format_win.configure(bg="#f0f0f0")

    # Đặt cửa sổ ở phía trước và tập trung vào cửa sổ này
    format_win.grab_set()
    format_win.focus_set()

    # Gọi hàm căn giữa cửa sổ
    center_window(format_win, 400, 250)

    # Nhãn và ô nhập thư mục
    label_directory_path = tk.Label(format_win, text="Chọn thư mục chứa file Excel:", font=("Arial", 12), bg="#f0f0f0")
    label_directory_path.pack(pady=10)

    entry_directory_path = tk.Entry(format_win, width=50)
    entry_directory_path.pack(pady=5)

    # Truyền entry_directory_path vào hàm select_directory
    button_browse = tk.Button(format_win, text="Duyệt", command=lambda: select_directory(entry_directory_path),
                              font=("Arial", 11), bg="#007bff", fg="white")
    button_browse.pack(pady=5)

    # Nút để thực hiện đổi tên file
    button_rename = tk.Button(format_win, text="Đổi tên tất cả file",
                              command=lambda: rename_excel_files_in_directory(entry_directory_path.get()),
                              font=("Arial", 11), bg="#28a745", fg="white")
    button_rename.pack(pady=5)

    # Nút để đóng cửa sổ
    button_close = tk.Button(format_win, text="Đóng", command=format_win.destroy,
                             font=("Arial", 11), bg="#dc3545", fg="white")
    button_close.pack(pady=20)

