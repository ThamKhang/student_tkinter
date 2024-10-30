import imaplib
import email
from email.header import decode_header
import smtplib
from email.mime.text import MIMEText
import ssl
import tkinter as tk  # Sử dụng tkinter trực tiếp
from tkinter import scrolledtext, messagebox
import time
from datetime import datetime, timedelta
from email.header import decode_header
from utils import center_window

from student_management.report import send_email, show_email_info


# Hàm để giải mã tên người gửi
def decode_email_address(email_address):
    name, addr = email.utils.parseaddr(email_address)
    decoded_name, encoding = decode_header(name)[0]
    if isinstance(decoded_name, bytes):
        decoded_name = decoded_name.decode(encoding if encoding else 'utf-8')
    return f"{decoded_name} <{addr}>"

# Hàm để đăng nhập và lấy email từ hộp thư đến
def fetch_emails(limit=10):
    try:
        # Thông tin tài khoản Gmail
        username = "thamkhang122@gmail.com"
        password = "wges hngz qqsh oirp"

        # Kết nối tới hộp thư Gmail
        context = ssl.create_default_context()
        mail = imaplib.IMAP4_SSL("imap.gmail.com", port=993, ssl_context=context)
        mail.login(username, password)

        # Chọn hộp thư đến
        mail.select("inbox")

        # Tìm tất cả các email trong hộp thư đến
        status, messages = mail.search(None, 'ALL')
        mail_ids = messages[0].split()

        # Đảo ngược danh sách mail_ids để lấy email mới nhất trước
        mail_ids = mail_ids[::-1]  # Đảo ngược danh sách

        # Giới hạn lấy tối đa 10 email đầu tiên
        mail_ids = mail_ids[:limit]  # Lấy 10 email mới nhất

        email_data = []

        # Duyệt qua các email
        for mail_id in mail_ids:
            status, msg_data = mail.fetch(mail_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8", errors="ignore")

                    # Lấy thông tin người gửi
                    from_ = msg.get("From")
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            if "attachment" in content_disposition:
                                continue
                            if content_type == "text/plain" or content_type == "text/html":
                                try:
                                    body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                                except Exception as e:
                                    print(f"Error decoding body: {e}")
                                break
                    else:
                        try:
                            body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")
                        except Exception as e:
                            print(f"Error decoding body: {e}")

                    # Lưu thông tin email
                    email_data.append({"subject": subject, "from": from_, "body": body, "date": msg.get("Date")})

        mail.logout()
        return email_data

    except Exception as e:
        print(f"Error: {e}")
        return []
def fetch_sent_emails(limit=10):
    try:
        username = "thamkhang122@gmail.com"
        password = "wges hngz qqsh oirp"

        context = ssl.create_default_context()
        mail = imaplib.IMAP4_SSL("imap.gmail.com", port=993, ssl_context=context)
        mail.login(username, password)

        # Kiểm tra tất cả thư mục
        status, folders = mail.list()
        print(f"Available folders: {folders}")

        # Sử dụng tên thư mục mã hóa chính xác cho thư đã gửi
        folder_name = '"[Gmail]/Th&AbA- &AREA4w- g&Hu0-i"'
        print(f"Selecting folder: {folder_name}")
        status, _ = mail.select(folder_name)
        if status != 'OK':
            print(f"Failed to select folder: {folder_name}")
            return []

        # Fetch emails từ thư mục đã chọn
        status, messages = mail.search(None, 'ALL')
        if status != 'OK':
            print("No messages found!")
            return []

        mail_ids = messages[0].split()
        mail_ids = mail_ids[::-1][:limit]  # Lấy tối đa 10 email mới nhất

        email_data = []
        for mail_id in mail_ids:
            status, msg_data = mail.fetch(mail_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8", errors="ignore")

                    from_ = msg.get("From")
                    to_ = msg.get("To")  # Lấy thông tin trường "To"
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            if content_type == "text/plain" or content_type == "text/html":
                                try:
                                    body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                                except Exception as e:
                                    print(f"Error decoding body: {e}")
                                break
                    else:
                        try:
                            body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")
                        except Exception as e:
                            print(f"Error decoding body: {e}")

                    email_data.append({
                        "subject": subject,
                        "from": from_,
                        "to": to_,  # Lưu thông tin trường "To"
                        "body": body,
                        "date": msg.get("Date")
                    })

        mail.logout()
        return email_data

    except Exception as e:
        print(f"Error fetching sent emails: {e}")
        return []


def send_report(report_message):
    try:
        sender_email = "thamkhang122@gmail.com"
        receiver_email = "thamkhang2003@gmail.com"
        password = "wges hngz qqsh oirp"
        msg = MIMEText(report_message)
        msg["Subject"] = "Báo cáo trễ hạn nộp dữ liệu lớp học"
        msg["From"] = sender_email
        msg["To"] = receiver_email

        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

        # Hiển thị thông tin email đã gửi
        show_email_info(msg["Subject"], receiver_email, report_message, None)

        server.quit()
        print("Email báo cáo đã được gửi thành công!")
    except Exception as e:
        print(f"Error: {e}")

# Hàm tổng hợp để xử lý email và gửi báo cáo
from datetime import datetime, timezone  # Import timezone để làm việc với múi giờ


import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime, timezone

def process_emails():
    emails = fetch_emails()
    root = tk.Tk()
    root.title("Xem báo cáo và kiểm tra email")

    # Gọi hàm `center_window` để căn giữa cửa sổ với kích thước 1200x800
    center_window(root, width=1200, height=800)

    # Tạo tiêu đề
    title_label = tk.Label(root, text="Báo cáo và Kiểm tra Email", font=("Arial", 16, "bold"), fg="blue")
    title_label.pack(pady=10)

    # Khung hiển thị email
    email_frame = tk.LabelFrame(root, text="Danh Sách Email", font=("Arial", 12, "bold"), padx=10, pady=10)
    email_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    # Danh sách cuộn để hiển thị nội dung email
    email_list_box = scrolledtext.ScrolledText(email_frame, wrap=tk.WORD, width=40, height=20, font=("Arial", 10))
    email_list_box.pack(fill="both", expand=True)

    # Khung hiển thị báo cáo
    report_frame = tk.LabelFrame(root, text="Báo Cáo Nộp Dữ Liệu", font=("Arial", 12, "bold"), padx=10, pady=10)
    report_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    # Hộp text để hiển thị báo cáo
    report_box = scrolledtext.ScrolledText(report_frame, wrap=tk.WORD, width=40, height=20, font=("Arial", 10))
    report_box.pack(fill="both", expand=True)

    # Danh sách lưu thông tin nộp dữ liệu
    class_submissions = []
    late_submissions = []
    due_date = datetime(2024, 10, 10, tzinfo=timezone.utc)

    # Hiển thị danh sách email
    for idx, email in enumerate(emails):
        subject = email["subject"]
        from_ = email["from"]
        body = email["body"][:1000]
        email_date = email.get("date")

        # Thêm định dạng cho các tag của danh sách email
        email_list_box.tag_configure("title", font=("Arial", 12, "bold"), foreground="blue")
        email_list_box.tag_configure("subject", font=("Arial", 10, "bold"), foreground="darkgreen")
        email_list_box.tag_configure("from", font=("Arial", 10, "italic"), foreground="purple")
        email_list_box.tag_configure("body", font=("Arial", 10), foreground="black")
        email_list_box.tag_configure("separator", foreground="gray")

        # Chèn từng email vào danh sách với các tag định dạng
        email_list_box.insert(tk.END, f"Email {idx + 1}:\n", "title")
        email_list_box.insert(tk.END, f"Subject: {subject}\n", "subject")
        email_list_box.insert(tk.END, f"From: {decode_email_address(from_)}\n", "from")
        email_list_box.insert(tk.END, f"Body: {body}...\n", "body")
        email_list_box.insert(tk.END, f"{'-' * 100}\n", "separator")

        if "Nộp dữ liệu lớp" in subject:
            class_info = subject.replace("Nộp dữ liệu lớp", "").strip()
            class_submissions.append((class_info, from_))

            if email_date:
                email_date_parsed = datetime.strptime(email_date, '%a, %d %b %Y %H:%M:%S %z')
                if email_date_parsed > due_date:
                    late_submissions.append((class_info, from_))

    # Tạo báo cáo
    report_message = "BÁO CÁO TÌNH HÌNH NỘP DỮ LIỆU\n\n"
    report_message += "Danh sách lớp đã nộp dữ liệu:\n"
    for class_info, sender in class_submissions:
        sender_decoded = decode_email_address(sender)
        report_message += f"Lớp: {class_info} - Người gửi: {sender_decoded}\n"

    report_box.insert(tk.END, report_message)

    if late_submissions:
        late_report = "Các lớp nộp trễ:\n"
        for class_info, sender in late_submissions:
            late_report += f"Lớp: {class_info} - Người gửi: {sender_decoded}\n"
        report_box.insert(tk.END, late_report)

    def confirm_and_send_report():
        send_report(report_message + "\n" + late_report)
        root.quit()

    send_button = tk.Button(root, text="Gửi báo cáo", font=("Arial", 12), command=confirm_and_send_report, bg="green", fg="white")
    send_button.pack(pady=10)

    close_button = tk.Button(root, text="Close", font=("Arial", 12), bg="#007bff", fg="white", command=root.destroy)
    close_button.pack(pady=10)

    root.mainloop()
def process_emails_auto():

    emails = fetch_emails()

    # Danh sách lưu thông tin nộp dữ liệu
    class_submissions = []
    late_submissions = []
    due_date = datetime(2024, 10, 10, tzinfo=timezone.utc)  # Đặt due_date thành offset-aware

    # Hiển thị danh sách email
    for idx, email in enumerate(emails):
        subject = email["subject"]
        from_ = email["from"]
        email_date = email.get("date")

        # Kiểm tra tiêu đề xem có phải nộp dữ liệu lớp không
        if "Nộp dữ liệu lớp" in subject:
            class_info = subject.replace("Nộp dữ liệu lớp", "").strip()
            class_submissions.append((class_info, from_))

            # Kiểm tra ngày gửi email có trễ hạn không
            if email_date:
                email_date_parsed = datetime.strptime(email_date, '%a, %d %b %Y %H:%M:%S %z')
                if email_date_parsed > due_date:
                    late_submissions.append((class_info, from_))

    # Tạo báo cáo dựa trên dữ liệu đã nộp
    report_message = "Danh sách lớp đã nộp dữ liệu:\n"
    for class_info, sender in class_submissions:
        sender_decoded = decode_email_address(sender)  # Giải mã người gửi
        report_message += f"Lớp: {class_info} - Người gửi: {sender_decoded}\n"

    # Kiểm tra nếu có lớp nào nộp trễ
    if late_submissions:
        late_report = "Các lớp nộp trễ:\n"
        for class_info, sender in late_submissions:
            sender_decoded = decode_email_address(sender)  # Giải mã người gửi
            late_report += f"Lớp: {class_info} - Người gửi: {sender_decoded}\n"

        # Gửi báo cáo tự động nếu có lớp nộp trễ
        send_report(report_message + "\n" + late_report)
    else:
        # Nếu không có lớp nào trễ hạn, chỉ gửi báo cáo các lớp đã nộp
        send_report(report_message)

def send_forward_email(unreplied_email_info):
    # Giải mã địa chỉ email của người gửi
    decoded_sender = decode_email_address(unreplied_email_info['from'])

    # Tạo tiêu đề cho email
    subject = f"Chuyển tiếp email chưa trả lời của nhân viên phụ trách"
    recipient = "thamkhang2003@gmail.com"
    body = (
        f"Email từ: {unreplied_email_info['from']}\n"
        f"Ngày gửi: {unreplied_email_info['date']}\n"
        f"Nội dung: {unreplied_email_info['body']}"
    )

    send_email(subject, recipient, body)  # Gọi hàm send_email với các tham số đúng thứ tự

def show_popup(from_, date_sent, unreplied_email_info):
    def on_ok():
        root.destroy()

    def on_forward():
        send_forward_email(unreplied_email_info)
        messagebox.showinfo("Thông báo", "Thông tin đã được chuyển tiếp cho quản lý.")
        root.destroy()

    root = tk.Tk()
    root.withdraw()  # Ẩn cửa sổ chính
    message = f"Chưa gửi phản hồi lại cho '{decode_email_address(from_)}' trong vòng 24 giờ. (Ngày gửi: {date_sent})"
    if messagebox.askyesno("Thông báo", message + "\nBạn có muốn chuyển tiếp thông tin này cho quản lý?"):
        on_forward()
    else:
        on_ok()

def check_if_replied_within_24_hours():
    inbox_emails = fetch_emails()
    sent_emails = fetch_sent_emails()

    for email_info in inbox_emails:
        from_ = email_info["from"]
        date_sent = email.utils.parsedate_to_datetime(email_info["date"])

        replied = False  # Biến đánh dấu đã trả lời hay chưa
        for sent_email_info in sent_emails:
            sent_to = sent_email_info["to"]
            sent_date = email.utils.parsedate_to_datetime(sent_email_info["date"])

            if from_ in sent_to:
                if sent_date - date_sent <= timedelta(hours=24):
                    print(f"Đã gửi phản hồi lại cho '{from_}' trong vòng 24 giờ.")
                    replied = True
                    break

        if not replied:
            print(f"Chưa gửi phản hồi lại cho '{from_}' trong vòng 24 giờ. (Ngày gửi: {date_sent})")
            show_popup(from_, date_sent, email_info)  # Hiện popup khi chưa trả lời