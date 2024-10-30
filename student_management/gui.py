# gui.py
import os
import tkinter as tk
from tkinter import ttk, messagebox

from plugin.chatbox import chat_box
from student_management.functions import search_student, update_treeview, sort_students_in_treeview, delete_student, \
    load_students_from_excel, filter_by_class, filter_by_absences, apply_filters_and_sort
from student_management.data import load_absences_for_student, load_all_students, SAMPLE_DATA, SAMPLE_ABSENCES, add_student_to_db
from student_management.email_handler import process_emails, process_emails_auto, check_if_replied_within_24_hours
from student_management.getter_data import get_sample_data
from utils import center_window
from student_management.report import warn_if_absent_too_much, generate_report, warn_if_absent_too_much_view


def view_details(tree):
    """Trigger for the 'View Details' button to show the detailed information window."""
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)
        print(f"Tree item selected: {item}")  # Debugging line
        values = item['values']
        dot, ma_lop, ten_mh, name, mssv, total_absences = values

        # Convert ma_lop to a string to ensure correct matching
        ma_lop = str(ma_lop).zfill(12)  # Adjust the length as needed if it's always 12 digits

        print(f"Selected student: MSSV: {mssv}, Ma lop: {ma_lop}, Name: {name}, Dot: {dot}, Ten mh: {ten_mh}")

        # Pass the extracted values to show_student_details
        show_student_details(mssv, ma_lop, name, dot, ten_mh)
    else:
        messagebox.showwarning("No selection", "Vui lòng chọn sinh viên muốn xem thông tin chi tiết trước!")


def show_student_details(mssv=None, ma_lop=None, name=None, dot=None, ten_mh=None, add_mode=False):
    print(f"Showing details for: MSSV: {mssv}, Ma lop: {ma_lop}, Name: {name}, Dot: {dot}, Ten mh: {ten_mh}")  # Debugging line
    """Displays detailed student information and absences in a new window or allows adding a new student."""
    details_win = tk.Toplevel()
    details_win.title(f"{'Add Student' if add_mode else 'Details for ' + name}")
    center_window(details_win, 1200, 800)

    # Display title based on mode
    details_label = tk.Label(details_win,
                             text=f"{'Thêm sinh viên' if add_mode else f'Thông tin chi tiết của {name} - MSSV: {mssv}'}",
                             font=("Arial", 18, "bold"))
    details_label.pack(pady=10)

    # Student details frame
    details_frame = tk.Frame(details_win)
    details_frame.pack(pady=20)

    # Input fields for student details
    dot_var = tk.StringVar(value=dot)
    ma_lop_var = tk.StringVar(value=ma_lop)
    ten_mh_var = tk.StringVar(value=ten_mh)
    name_var = tk.StringVar(value=name)
    mssv_var = tk.StringVar(value=mssv)

    tk.Label(details_frame, text="Đợt:").grid(row=0, column=0, sticky="w")
    tk.Entry(details_frame, textvariable=dot_var, state="normal" if add_mode else "readonly", width=50).grid(row=0,
                                                                                                             column=1,
                                                                                                             sticky="w",
                                                                                                             padx=(
                                                                                                             0, 20))

    tk.Label(details_frame, text="Mã lớp:").grid(row=1, column=0, sticky="w")
    tk.Entry(details_frame, textvariable=ma_lop_var, state="normal" if add_mode else "readonly", width=50).grid(row=1,
                                                                                                                column=1,
                                                                                                                sticky="w",
                                                                                                                padx=(
                                                                                                                0, 20))

    tk.Label(details_frame, text="Tên môn học:").grid(row=2, column=0, sticky="w")
    tk.Entry(details_frame, textvariable=ten_mh_var, state="normal" if add_mode else "readonly", width=50).grid(row=2,
                                                                                                                column=1,
                                                                                                                sticky="w",
                                                                                                                padx=(
                                                                                                                0, 20))

    tk.Label(details_frame, text="Tên sinh viên:").grid(row=3, column=0, sticky="w")
    tk.Entry(details_frame, textvariable=name_var, state="normal" if add_mode else "readonly", width=50).grid(row=3,
                                                                                                              column=1,
                                                                                                              sticky="w",
                                                                                                              padx=(
                                                                                                              0, 20))

    tk.Label(details_frame, text="MSSV:").grid(row=4, column=0, sticky="w")
    tk.Entry(details_frame, textvariable=mssv_var, state="normal" if add_mode else "readonly", width=50).grid(row=4,
                                                                                                              column=1,
                                                                                                              sticky="w",
                                                                                                              padx=(
                                                                                                              0, 20))

    # Adding absences functionality if in Add Mode
    if add_mode:
        def add_student():
            # Create a new student entry
            new_student = {
                "dot": dot_var.get(),
                "ma_lop": ma_lop_var.get(),
                "ten_mh": ten_mh_var.get(),
                "name": name_var.get(),
                "mssv": mssv_var.get()
            }
            # Add to the SAMPLE_DATA
            SAMPLE_DATA.append(new_student)
            add_student_to_db(dot_var.get(), ma_lop_var.get(), ten_mh_var.get(), name_var.get(), mssv_var.get())
            update_treeview(SAMPLE_DATA, tree)
            details_win.destroy()

        tk.Button(details_win, text="Thêm", font=("Arial", 12), bg="#28a745", fg="white",
                  command=add_student).pack(pady=10)
    else:
        # Fetch absence data
        absences = load_absences_for_student(mssv, ma_lop)
        print(f"Absences loaded for {name}: {absences}")  # Debugging line

        # Calculate total classes and total absences
        total_classes = 30  # Replace with actual total class count
        total_absences = sum(absence['tong_tiet'] for absence in absences)

        # Calculate absence percentage
        absence_percentage = (total_absences / total_classes) * 100 if total_classes > 0 else 0

        # Frame for Absences Treeview
        absences_frame = tk.Frame(details_win)
        absences_frame.pack(pady=10)

        # Create Treeview for displaying absences
        absences_tree = ttk.Treeview(absences_frame, columns=(
            "ngay", "vang_phep", "vang_khong_phep", "tong_tiet"),
                                     show='headings', height=7)
        absences_tree.heading("ngay", text="Ngày")
        absences_tree.heading("vang_phep", text="Vắng Phép")
        absences_tree.heading("vang_khong_phep", text="Vắng Không Phép")
        absences_tree.heading("tong_tiet", text="Số tiết Vắng")

        # Đặt chiều rộng cho các cột
        absences_tree.column("ngay", width=250, anchor="center")
        absences_tree.column("vang_phep", width=100, anchor="center")
        absences_tree.column("vang_khong_phep", width=120, anchor="center")
        absences_tree.column("tong_tiet", width=120, anchor="center")

        # Insert absences into the Treeview
        for absence in absences:
            vng_phep = "✔️" if absence['vang_phep'] > 0 else ""
            vng_khong_phep = "✖️" if absence['vang_khong_phep'] > 0 else ""
            absences_tree.insert("", "end", values=(
                absence['ngay'],
                vng_phep,
                vng_khong_phep,
                absence['tong_tiet'],
            ))
        # Display total classes and absence percentage
        summary_frame = tk.Frame(details_win)
        summary_frame.pack(pady=10)

        tk.Label(summary_frame, text=f"Tổng số tiết: {total_classes}", font=("Arial", 12)).pack()
        tk.Label(summary_frame, text=f"Tổng số tiết vắng: {total_absences}", font=("Arial", 12)).pack()
        tk.Label(summary_frame, text=f"Tỷ lệ vắng: {absence_percentage:.2f}%", font=("Arial", 12)).pack()
        absences_tree.pack()
    tk.Button(details_win, text="Close", font=("Arial", 12), bg="#007bff", fg="white",
              command=details_win.destroy).pack(pady=10)


def open_add_student_window():
    """Opens the Add Student interface."""
    show_student_details(add_mode=True)


def load_excel_files(directory):
    """Load all Excel files in the given directory."""
    files = [f for f in os.listdir(directory) if f.endswith('.xlsx')]
    print("Excel files found:", files)  # Debugging line
    return files


def load_selected_file(excel_combobox):
    # Lấy tên file được chọn từ ComboBox
    selected_file = excel_combobox.get()

    if not selected_file:
        print("Vui lòng chọn một file Excel.")
        return

    # Tạo đường dẫn đầy đủ tới file Excel (nếu class_list là thư mục chứa các file)
    file_path = os.path.join('class_list', selected_file)

    if not os.path.exists(file_path):
        print(f"File {file_path} không tồn tại.")
        return

    try:
        # Gọi hàm load_students_from_excel để nạp dữ liệu từ file Excel vào database
        load_students_from_excel(file_path)
        print(f"Đã tải dữ liệu từ file {selected_file} vào cơ sở dữ liệu thành công.")
        # Tải lại dữ liệu sinh viên từ database và cập nhật TreeView
        global SAMPLE_DATA
        SAMPLE_DATA = get_sample_data()  # Lấy dữ liệu sinh viên từ database
        update_treeview(SAMPLE_DATA, tree)  # Cập nhật TreeView
    except Exception as e:
        print(f"Đã xảy ra lỗi khi tải dữ liệu từ file {selected_file}: {e}")


def map_sort_criteria(sort_option):
    if sort_option == "Tổng Số Nghỉ":
        return 'total_absences'
    elif sort_option == "Tên":
        return 'name'
    elif sort_option == "Lớp":
        return 'class'
    elif sort_option == "Môn Học":
        return 'subject'
    else:
        return None  # Nếu không chọn gì, không thực hiện sắp xếp


def load_selected_class_name():
    """Lấy danh sách các tên lớp từ SAMPLE_DATA."""
    # Sử dụng set để loại bỏ các lớp trùng lặp
    class_names = {sinh_vien['ma_lop'] for sinh_vien in SAMPLE_DATA}
    return sorted(class_names)  # Trả về danh sách lớp đã sắp xếp



def main_window():
    """Main function to create the UI."""
    global tree
    global main_win  # Sử dụng biến toàn cục
    main_win = tk.Tk()
    main_win.title("Quản Lý Sinh Viên")
    main_win.configure(bg="#f0f0f0")
    center_window(main_win, 1200, 800)
    top_frame = tk.Frame(main_win, bg="#f0f0f0")
    top_frame.pack(pady=10)

    # ComboBox for displaying Excel files
    tk.Label(top_frame, text="Chọn File Excel:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, padx=10,
                                                                                        pady=5)
    excel_files = load_excel_files('class_list')
    excel_combobox = ttk.Combobox(top_frame, values=excel_files, font=("Arial", 12), width=50)
    excel_combobox.grid(row=0, column=1, padx=10, pady=5)

    tk.Button(top_frame, text="Load", font=("Arial", 12), bg="#5cb85c", fg="black",
              command=lambda: load_selected_file(excel_combobox)).grid(row=0, column=2, padx=10, pady=5)

    # Search section
    tk.Label(top_frame, text="Tìm kiếm theo Tên hoặc MSSV:", font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=0,
                                                                                                    padx=10)
    search_entry = tk.Entry(top_frame, font=("Arial", 12), width=30)
    search_entry.grid(row=1, column=1, padx=10)
    tk.Button(top_frame, text="Tìm kiếm", font=("Arial", 12), bg="#5bc0de", fg="black",
              command=lambda: search_student(search_entry.get(), tree)).grid(row=1, column=2, padx=10, pady=5)

    # Khung tổng hợp sắp xếp và lọc
    sort_filter_frame = tk.Frame(main_win, bg="#f0f0f0")
    sort_filter_frame.pack(pady=10, padx=10, anchor="w")

    # Phần khung sắp xếp và lọc
    sort_filter_frame = tk.Frame(main_win, bg="#f0f0f0")
    sort_filter_frame.pack(pady=10, padx=10)

    # Phần sắp xếp
    tk.Label(sort_filter_frame, text="Sắp xếp theo:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, padx=10)
    sort_options = ["Tổng Số Nghỉ", "Tên", "Lớp", "Môn Học"]
    sort_var = tk.StringVar(value=sort_options[0])
    sort_menu = ttk.Combobox(sort_filter_frame, textvariable=sort_var, values=sort_options)
    sort_menu.grid(row=0, column=1, padx=10)
    # Nút áp dụng cả lọc và sắp xếp
    ascending_var = tk.BooleanVar(value=True)  # Thêm một biến Boolean để chọn tăng hoặc giảm
    tk.Checkbutton(sort_filter_frame, text="Tăng dần", variable=ascending_var).grid(row=0, column=3, padx=10)

    # Lọc theo lớp
    tk.Label(sort_filter_frame, text="Lọc theo Lớp:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=4, padx=10)
    class_list = load_selected_class_name()  # Hàm này sẽ load danh sách lớp từ SAMPLE_DATA
    class_filter = ttk.Combobox(sort_filter_frame, values=class_list, font=("Arial", 12), width=20)
    class_filter.grid(row=0, column=4, padx=10)

    # Lọc theo số buổi vắng
    tk.Label(sort_filter_frame, text="Số buổi vắng >", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=7, padx=10)
    absence_entry = tk.Entry(sort_filter_frame, font=("Arial", 12), width=5)
    absence_entry.grid(row=0, column=8, padx=10)

    # Nút áp dụng cả lọc và sắp xếp
    tk.Button(
        sort_filter_frame,
        text="Áp dụng",
        font=("Arial", 12),
        bg="#007bff",
        fg="white",
        command=lambda: apply_filters_and_sort(
            tree,
            selected_class=class_filter.get(),
            min_absences=int(absence_entry.get()) if absence_entry.get() else None,
            sort_criteria=map_sort_criteria(sort_var.get()),
            ascending=ascending_var.get()
        )
    ).grid(row=0, column=8, padx=10)

    # Tạo Style
    style = ttk.Style()
    style.configure("Treeview", bordercolor="black", borderwidth=1)
    style.map("Treeview", background=[("selected", "#00BFFF")])

    # TreeView hiển thị sinh viên
    tree = ttk.Treeview(main_win, columns=("dot", "ma_lop", "ten_mh", "name", "mssv", 'total_absences'), show='headings', height=20)

    # Đặt tiêu đề cho các cột
    tree.heading("dot", text="Đợt")
    tree.heading("ma_lop", text="Mã lớp")
    tree.heading("ten_mh", text="Tên môn học")
    tree.heading("name", text="Tên sinh viên")
    tree.heading("mssv", text="MSSV")
    tree.heading("total_absences", text="Vắng/Tổng Số Tiết")

    # Gói widget vào cửa sổ chính
    tree.pack(pady=20)

    # Định dạng kích thước các cột
    tree.column("dot", width=150, anchor="center")
    tree.column("ma_lop", width=130, anchor="center")
    tree.column("ten_mh", width=350, anchor="center")
    tree.column("name", width=200, anchor="w")  # Đã sửa lại tên cột
    tree.column("mssv", width=150, anchor="center")
    tree.column("total_absences", width=120, anchor="center")

    # Tải dữ liệu sinh viên vào TreeView
    update_treeview(load_all_students(), tree)

    # Phần nút trong hai cột
    button_frame = tk.Frame(main_win, bg="#f0f0f0")
    button_frame.pack(pady=10)

    # Nút Xem Chi Tiết
    tk.Button(button_frame, text="Xem Chi Tiết", font=("Arial", 12), bg="#5bc0de", fg="black",
              command=lambda: view_details(tree)).grid(row=0, column=0, padx=10, pady=5, sticky='ew')

    # Nút Thêm Sinh Viên
    tk.Button(button_frame, text="Thêm Sinh Viên", font=("Arial", 12), bg="#6f42c1", fg="white",
              command=open_add_student_window).grid(row=0, column=1, padx=10, pady=5, sticky='ew')

    # Nút Xóa Sinh Viên
    tk.Button(button_frame, text="Xóa Sinh Viên", font=("Arial", 12), bg="#dc3545", fg="white",
              command=lambda: delete_student(tree)).grid(row=0, column=2, padx=10, pady=5, sticky='ew')

    # Button to open Chat Box
    user_id = "user_1"  # Example static user ID
    tk.Button(button_frame, text="Chat Box", font=("Arial", 12), bg="#5cb85c", fg="white",
              command=lambda: chat_box(tree, main_win)).grid(row=0, column=3, padx=10, pady=5, sticky='ew')

    # Nút Cảnh Báo Học Vụ
    tk.Button(button_frame, text="Cảnh Báo Học Vụ", font=("Arial", 12), bg="#ffcccb", fg="black",
              command=lambda: warn_if_absent_too_much_view(SAMPLE_DATA, SAMPLE_ABSENCES)).grid(row=1, column=0, padx=10,
                                                                                               pady=5, sticky='ew')

    # Nút Báo Cáo Tổng Hợp
    tk.Button(button_frame, text="Gửi Báo Cáo Tổng Hợp", font=("Arial", 12), bg="#007BFF", fg="white",
              command=generate_report).grid(row=1, column=1, padx=10, pady=5, sticky='ew')

    # Nút Xem Hộp Thư
    tk.Button(button_frame, text="Xem Hộp Thư", font=("Arial", 12), bg="#ffc107", fg="black",
              command=process_emails).grid(row=1, column=2, padx=10, pady=5, sticky='ew')

    # Nút Kiểm Tra Mail Chưa Trả Lời
    tk.Button(button_frame, text="Kiểm tra mail chưa trả lời", font=("Arial", 12), bg="#ffc107", fg="black",
              command=check_if_replied_within_24_hours).grid(row=1, column=3, padx=10, pady=5, sticky='ew')

    # Đảm bảo rằng các cột đều có trọng số để có thể căn giữa
    for col in range(4):  # Nếu bạn có 4 cột
        button_frame.grid_columnconfigure(col, weight=1)

    main_win.mainloop()
