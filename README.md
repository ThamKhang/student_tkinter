# Hệ thống Quản Lý Sinh Viên

Hệ thống này được xây dựng bằng Python và Tkinter, cho phép quản lý thông tin sinh viên, điểm danh, và gửi cảnh báo học vụ tự động.

## Chức năng chính:

* **Nạp dữ liệu từ file Excel:** Hệ thống có thể nạp dữ liệu sinh viên từ file Excel (.xls và .xlsx) vào cơ sở dữ liệu SQLite. Chức năng chuyển đổi định dạng file .xls sang .xlsx được tích hợp sẵn. Tên file Excel sẽ được tự động đổi tên theo mã lớp trong file (yêu cầu sử dụng plugin `file_format_plugin.py`).
* **Tìm kiếm sinh viên:** Cho phép tìm kiếm sinh viên theo tên hoặc MSSV.
* **Lọc và sắp xếp:** Hỗ trợ lọc sinh viên theo lớp, số buổi vắng và sắp xếp theo tên, lớp, môn học, hoặc tổng số buổi vắng.
* **Xem chi tiết sinh viên:** Hiển thị thông tin chi tiết của sinh viên, bao gồm lịch sử điểm danh.
* **Thêm và xóa sinh viên:** Cho phép thêm sinh viên mới vào cơ sở dữ liệu và xóa sinh viên hiện có.
* **Cảnh báo học vụ:** Tự động gửi email cảnh báo đến sinh viên và phòng đào tạo khi sinh viên vắng quá số buổi quy định (20% và 50%).
* **Báo cáo tổng hợp:** Tạo báo cáo tổng hợp về tình hình điểm danh của sinh viên dưới dạng file Excel và gửi email báo cáo kèm file đính kèm đến phòng đào tạo.
* **Chat box:** Tích hợp chat box với các lệnh để thực hiện các chức năng quản lý sinh viên một cách nhanh chóng.  Hỗ trợ các lệnh như:
    * `tìm kiếm sinh viên <từ khóa>`: Tìm kiếm sinh viên theo tên hoặc MSSV.
    * `tìm lớp <tên lớp>`: Lọc sinh viên theo lớp.
    * `tỷ lệ vắng mặt <số buổi vắng>`: Lọc sinh viên có số buổi vắng lớn hơn giá trị nhập vào.
    * `sắp xếp theo <tên|lớp|môn học|buổi vắng>`: Sắp xếp sinh viên theo tiêu chí.
    * `thêm sinh viên`: (Chưa được cài đặt đầy đủ, cần hoàn thiện thêm)
    * `xóa sinh viên`: Xóa sinh viên đã chọn.
    * `hiển thị tất cả sinh viên`: Hiển thị lại toàn bộ danh sách sinh viên.
* **Kiểm tra email chưa trả lời:** Kiểm tra hộp thư đến và thư đã gửi để xác định email nào chưa được trả lời trong vòng 24 giờ và hiển thị thông báo. Cho phép chuyển tiếp email chưa trả lời cho quản lý.
* **Xem hộp thư:** Cho phép xem 10 email mới nhất trong hộp thư đến.



## Cấu trúc thư mục:

├── plugin/
│ └── chatbox.py
│ └── file_format_plugin.py
├── student_management/
│ ├──class_list/
│   └── <excel_files>.xlsx
│ ├── data.py
│ ├── email_handler.py
│ ├── functions.py
│ ├── getter_data.py
│ ├── gui.py
│ ├── main.py
│ └── report.py
├── main.py
└── utils.py

## Hướng dẫn sử dụng:

1. **Cài đặt các thư viện cần thiết:**
```bash
pip install -r requirements.txt

2. **Chạy chương trình: python main.py **

Nạp dữ liệu từ file Excel: Sử dụng plugin file_format_plugin.py để đổi tên file và chuyển đổi định dạng nếu cần. Sau đó, trong giao diện chính, chọn file Excel từ danh sách và nhấn "Load".

Sử dụng các chức năng: Sử dụng giao diện đồ họa hoặc chat box để thực hiện các chức năng quản lý sinh viên.


**Lưu ý:**
Cần cấu hình thông tin tài khoản Gmail trong file email_handler.py để sử dụng chức năng gửi email.

File Excel cần tuân theo định dạng được quy định trong code (xem file mẫu trong class_list).

Cơ sở dữ liệu SQLite student_data.db sẽ được tạo tự động nếu chưa tồn tại.

Để sử dụng chức năng format file, cần chạy hàm open_format_file_window() từ file file_format_plugin.py. Ví dụ, bạn có thể thêm một nút gọi hàm này trong giao diện chính gui.py.
