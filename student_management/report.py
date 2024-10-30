import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from student_management.data import load_all_students, SAMPLE_ABSENCES, load_absences_for_student
from utils import center_window



import tkinter as tk

def show_email_info(subject, recipient, body, attach):
    # Tạo một cửa sổ mới để hiển thị nội dung email
    email_window = tk.Toplevel()
    email_window.title("Email Đã Gửi")

    # Đặt kích thước cho cửa sổ
    center_window(email_window, width=800, height=500)

    # Hiển thị các thông tin của email
    tk.Label(email_window, text="Email đã được gửi đến:", font=('Arial', 12, 'bold')).grid(row=0, column=0, sticky='w', padx=10, pady=5)
    tk.Label(email_window, text=recipient, font=('Arial', 12)).grid(row=0, column=1, sticky='w', padx=10, pady=5)

    tk.Label(email_window, text="Tiêu đề:", font=('Arial', 12, 'bold')).grid(row=1, column=0, sticky='w', padx=10, pady=5)
    tk.Label(email_window, text=subject, font=('Arial', 12)).grid(row=1, column=1, sticky='w', padx=10, pady=5)

    tk.Label(email_window, text="Nội dung:", font=('Arial', 12, 'bold')).grid(row=2, column=0, sticky='nw', padx=10, pady=5)

    # Tạo Text widget và sau đó chèn nội dung
    body_text = tk.Text(email_window, wrap='word', height=15, width=80, font=('Arial', 11, 'italic'))
    body_text.insert("1.0", body)
    body_text.grid(row=2, column=1, padx=10, pady=5)  # Áp dụng grid trên Text widget

    if attach:
        tk.Label(email_window, text="File đính kèm:", font=('Arial', 12, 'bold')).grid(row=3, column=0, sticky='w', padx=10, pady=5)
        tk.Label(email_window, text=attach, font=('Arial', 12, 'italic')).grid(row=3, column=1, sticky='w', padx=10, pady=5)

    # Tạo nút Close
    close_button = tk.Button(email_window, text="Close", font=("Arial", 12), bg="#007bff", fg="white", command=email_window.destroy)
    close_button.grid(row=4, column=1, pady=10)  # Đặt nút ở hàng 4, cột 1
    close_button.config(width=10)  # Đặt chiều rộng cho nút
    # Căn giữa nút
    email_window.grid_columnconfigure(1, weight=1)

    email_window.mainloop()


def send_email(subject, recipient, body, attach=None):
    sender_email = "thamkhang122@gmail.com"
    sender_password = "wges hngz qqsh oirp"

    # Thiết lập kết nối SMTP
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    try:
        server.login(sender_email, sender_password)
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        # Kiểm tra xem có file đính kèm hay không và xử lý nếu có
        if attach:
            part = MIMEBase('application', 'octet-stream')
            with open(attach, 'rb') as file:
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % attach)
            msg.attach(part)

        # Gửi email
        server.sendmail(sender_email, recipient, msg.as_string())
        print(f"Email sent to {recipient}")

        # Hiển thị thông tin email đã gửi
        show_email_info(subject, recipient, body, attach)

    except smtplib.SMTPAuthenticationError as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()

def warn_if_absent_too_much(students_data, absences_data):
    total_classes = 30  # Giả sử tổng số tiết học mỗi kỳ là 30
    for student in students_data:
        mssv = student['mssv']
        ma_lop = student['ma_lop']  # Lấy mã lớp từ dữ liệu sinh viên

        # Tính tổng số tiết vắng cho sinh viên này từ dữ liệu vắng mặt
        total_absences = sum(absence['tong_tiet'] for absence in absences_data if
                             absence['mssv'] == mssv and absence['ma_lop'] == ma_lop)

        # Tính tỷ lệ vắng mặt
        absence_rate = total_absences / total_classes

        email_address = f"{mssv}@gmail.com"
        print(
            f"MSSV: {mssv}, Email: {email_address}, Total Absences: {total_absences}, Absence Rate: {absence_rate:.2f}")  # Thêm dòng này để kiểm tra

        # Gửi email cảnh báo nếu tỷ lệ vắng mặt vượt quá ngưỡng
        # if absence_rate >= 0.5:
        #     send_email("Cảnh báo học vụ nghiêm trọng", "thamkhang2003@gmail.com",
        #                f"Sinh viên {student['name']} đã vắng {total_absences} trên tổng số {total_classes} tiết học.")
        # elif absence_rate >= 0.2:
        #     send_email("Cảnh báo học vụ", email_address,
        #                f"Bạn đã vắng {total_absences} trên tổng số {total_classes} tiết học.")


import pandas as pd


import pandas as pd

def calculate_absences(row, absences_data):
    mssv = row['MSSV']  # Thay 'mssv' thành 'MSSV'
    ma_lop = row['Mã Lớp']  # Thay 'ma_lop' thành 'Mã Lớp'
    student_absences = absences_data[(absences_data['mssv'] == mssv) & (absences_data['ma_lop'] == ma_lop)]
    absences_details = {}
    for _, absence in student_absences.iterrows():
        date_key = absence['ngay']
        absences_details[(date_key, 'tong_tiet')] = absence['tong_tiet']
        absences_details[(date_key, 'vang_khong_phep')] = absence['vang_khong_phep']
        absences_details[(date_key, 'vang_phep')] = absence['vang_phep']
    return absences_details


def generate_report():
    data = load_all_students()  # Giả định rằng hàm này tải dữ liệu sinh viên
    df = pd.DataFrame(data)

    # Chuyển đổi tên cột thành viết hoa chữ cái đầu
    df.rename(columns={
        'dot': 'Đợt',
        'ma_lop': 'Mã Lớp',
        'ten_mh': 'Tên Môn Học',
        'name': 'Tên Sinh Viên',
        'mssv': 'MSSV'
    }, inplace=True)

    absences_df = pd.DataFrame(SAMPLE_ABSENCES)  # Giả định SAMPLE_ABSENCES là biến đã có sẵn

    # Cập nhật DataFrame với thông tin vắng mặt
    absences_info = df.apply(lambda row: calculate_absences(row, absences_df), axis=1)
    absences_info = absences_info.apply(pd.Series)  # Chuyển dictionary thành các cột

    # Tạo MultiIndex cho các cột với tên viết hoa chữ cái đầu
    absences_info.columns = pd.MultiIndex.from_tuples(
        [(date, 'Tổng Tiết' if info == 'tong_tiet' else 'Vắng Không Phép' if info == 'vang_khong_phep' else 'Vắng Phép')
         for date, info in absences_info.columns],
        names=['Ngày', 'Thông tin'])

    df = pd.concat([df, absences_info], axis=1)

    # Tính tổng số tiết vắng và thêm vào DataFrame chỉ một lần
    total_absences_columns = [col for col in absences_info.columns if col[1] == 'Tổng Tiết']
    df['Tổng Số Tiết Vắng'] = df[total_absences_columns].sum(axis=1)

    # Sắp xếp lại thứ tự cột, đưa cột "Tổng Số Tiết Vắng" sau cột MSSV
    mssv_index = df.columns.get_loc('MSSV')
    cols = df.columns.tolist()
    new_col_order = cols[:mssv_index + 1] + ['Tổng Số Tiết Vắng'] + cols[mssv_index + 1:-1]  # Sắp xếp lại mà không thêm lại cột
    df = df[new_col_order]

    # Xuất ra Excel với tiêu đề đã được chỉnh sửa
    df.to_excel("report.xlsx", index=False)
    print(df.head())  # In 5 dòng đầu của DataFrame để kiểm tra

    # Tính số sinh viên vắng trên 20% và 50%
    total_students = len(df)  # Tổng số sinh viên
    absent_20_percent = len(df[df['Tổng Số Tiết Vắng'] / 30 > 0.2])  # Số sinh viên vắng trên 20%
    absent_50_percent = len(df[df['Tổng Số Tiết Vắng'] / 30 > 0.5])  # Số sinh viên vắng trên 50%

    # Cập nhật nội dung email với thông tin thực tế
    body = (
        "Kính gửi,\n\n"
        "Chúng tôi xin thông báo rằng báo cáo tổng hợp đã được tạo thành công. "
        "Dưới đây là một số thông tin quan trọng:\n\n"
        f"- Tổng số sinh viên: {total_students}\n"
        f"- Số sinh viên vắng trên 20%: {absent_20_percent}\n"
        f"- Số sinh viên vắng trên 50%: {absent_50_percent}\n\n"
        "Bạn có thể xem chi tiết trong tệp đính kèm.\n\n"
        "Trân trọng,\n"
        "Phòng Đào Tạo"
    )

    # Gửi email với tệp đính kèm
    send_email("Báo Cáo Tổng Hợp", "thamkhang2003@gmail.com", body, attach="report.xlsx")


import pandas as pd

def get_student_absence_info(mssv):
    total_classes = 0
    total_absences = 0
    for absence in SAMPLE_ABSENCES:
        if absence['mssv'] == mssv:
            total_classes += absence['tong_tiet']
            total_absences += absence['vang_phep'] + absence['vang_khong_phep']
    return total_classes, total_absences




import tkinter as tk
from tkinter import messagebox, ttk

def warn_if_absent_too_much_view(students_data, absences_data):
    # Tạo cửa sổ giao diện
    root = tk.Tk()
    root.title("Thông tin sinh viên và vắng học")
    center_window(root, 800, 500)  # Căn giữa cửa sổ

    # Frame chứa tìm kiếm và sắp xếp
    control_frame = tk.Frame(root)
    control_frame.pack(side="top", anchor="center", padx=10, pady=5, expand=True)

    # Tạo Entry và Button cho tìm kiếm
    search_label = tk.Label(control_frame, text="Tìm kiếm:")
    search_label.grid(row=0, column=0, padx=5)
    search_entry = tk.Entry(control_frame, width=20)
    search_entry.grid(row=0, column=1, padx=5)
    search_button = tk.Button(control_frame, text="Tìm", command=lambda: search_students(tree, search_entry.get()))
    search_button.grid(row=0, column=2, padx=5)

    # Combobox sắp xếp
    sort_label = tk.Label(control_frame, text="Sắp xếp theo tỷ lệ vắng:")
    sort_label.grid(row=0, column=3, padx=5)
    sort_options = ["Tăng dần", "Giảm dần"]
    sort_combobox = ttk.Combobox(control_frame, values=sort_options, state="readonly")
    sort_combobox.grid(row=0, column=4, padx=5)
    sort_combobox.bind("<<ComboboxSelected>>", lambda e: sort_by_absence(tree, sort_combobox.get()))

    # Thiết lập bảng Treeview với cột mới "Mã Lớp"
    columns = ("MSSV", "Tên Sinh Viên", "Mã Lớp", "Vắng/Tổng Số Tiết", "Tỷ Lệ Vắng", "Cảnh Báo")
    tree = ttk.Treeview(root, columns=columns, show="headings", height=15)

    # Đặt tiêu đề cho các cột
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")  # Căn giữa cho tất cả các cột

    # Định dạng kích thước các cột
    tree.column("MSSV", width=100)
    tree.column("Tên Sinh Viên", width=150)
    tree.column("Mã Lớp", width=100)  # Đặt chiều rộng cho cột "Mã Lớp"
    tree.column("Vắng/Tổng Số Tiết", width=120)
    tree.column("Tỷ Lệ Vắng", width=100)
    tree.column("Cảnh Báo", width=100)

    # Tổng số tiết giả định
    total_classes = 30

    # Điền thông tin vào bảng
    for student in students_data:
        mssv = student['mssv']
        name = student['name']
        ma_lop = student['ma_lop']

        # Tính số tiết vắng và tỷ lệ
        total_absences = sum(absence['tong_tiet'] for absence in absences_data if
                             absence['mssv'] == mssv and absence['ma_lop'] == ma_lop)
        absence_rate = total_absences / total_classes
        absence_text = f"{total_absences}/{total_classes}"
        absence_rate_text = f"{absence_rate:.2%}"

        # Hiển thị cảnh báo nếu tỷ lệ vắng học >= 20%
        warning_status = "Cảnh Báo" if absence_rate >= 0.2 else ""

        # Chèn thông tin vào bảng, thêm mã lớp vào giá trị
        tree.insert("", "end", values=(mssv, name, ma_lop, absence_text, absence_rate_text, warning_status))

    tree.pack(pady=10, padx=10)

    # Hàm tìm kiếm
    def search_students(tree, keyword):
        for row in tree.get_children():
            tree.delete(row)
        for student in students_data:
            if keyword.lower() in student['name'].lower() or keyword in student['mssv']:
                tree.insert("", "end", values=(student['mssv'], student['name'], student['ma_lop'], "0/0", "0%", ""))

    # Hàm sắp xếp
    def sort_by_absence(tree, order):
        data = [(tree.item(child)["values"], child) for child in tree.get_children()]
        data.sort(key=lambda x: float(x[0][4].strip('%')), reverse=(order == "Giảm dần"))
        for i, (_, item_id) in enumerate(data):
            tree.move(item_id, "", i)

    # Nhãn hiển thị trạng thái email đang gửi
    status_label = tk.Label(root, text="", font=('Arial', 10, 'italic'), bg="#f0f0f0")
    status_label.pack(pady=5)

    # Nút gửi cảnh báo
    def send_warning():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một sinh viên để gửi cảnh báo.")
            root.focus_force()  # Đảm bảo cửa sổ chính luôn nằm trên
            return

        values = tree.item(selected_item[0], "values")
        mssv, name, ma_lop, absence_text, absence_rate_text, warning_status = values

        # Kiểm tra nếu có cảnh báo
        if warning_status == "Cảnh Báo":
            email_address = f"{mssv}@gmail.com"
            total_absences = int(absence_text.split('/')[0])  # Lấy số tiết vắng
            absence_rate = float(absence_rate_text[:-1]) / 100

            # Tạo nội dung email chi tiết hơn
            if absence_rate >= 0.5:
                subject = "Cảnh báo học vụ nghiêm trọng"
                body = (
                    f"Kính gửi {name},\n\n"
                    f"Chúng tôi xin thông báo rằng bạn đã vắng {total_absences} tiết "
                    f"trong tổng số {total_classes} tiết học, tương đương với tỷ lệ vắng "
                    f"{absence_rate * 100:.2f}%. \n\n"
                    "Điều này có thể ảnh hưởng đến kết quả học tập của bạn.\n"
                    "Chúng tôi khuyến nghị bạn nên tham gia đầy đủ các tiết học "
                    "để đảm bảo tiến bộ trong việc học.\n\n"
                    "Trân trọng,\n"
                    "Phòng Đào Tạo"
                )
            else:
                subject = "Cảnh báo học vụ"
                body = (
                    f"Kính gửi {name},\n\n"
                    f"Chúng tôi ghi nhận rằng bạn đã vắng {total_absences} tiết "
                    f"trong tổng số {total_classes} tiết học, tương đương với tỷ lệ vắng "
                    f"{absence_rate * 100:.2f}%. \n\n"
                    "Chúng tôi khuyến nghị bạn theo dõi số tiết vắng của mình "
                    "để duy trì thành tích học tập tốt.\n\n"
                    "Trân trọng,\n"
                    "Phòng Đào Tạo"
                )

            # Gửi email
            send_email(subject, email_address, body)

            status_label.config(text=f"Đã gửi email đến {email_address}")
        else:
            messagebox.showinfo("Thông báo", "Sinh viên này không đủ điều kiện cảnh báo.")

    # Frame chứa các nút
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    # Thêm nút "Gửi Cảnh Báo" với màu xanh trong cùng frame
    send_button = tk.Button(button_frame, text="Gửi Cảnh Báo", command=send_warning, bg="green", fg="white",
                            font=('Arial', 12, 'bold'), width=15)
    send_button.grid(row=0, column=0, padx=5)

    # Nút đóng
    close_button = tk.Button(button_frame, text="Đóng", command=root.destroy, bg="#007bff", fg="white",
                             font=('Arial', 12, 'bold'), width=15)
    close_button.grid(row=0, column=1, padx=5)

    root.mainloop()