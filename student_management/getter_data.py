# getter_data.py
import sqlite3


# Kết nối đến cơ sở dữ liệu (tạo mới nếu chưa có)
conn = sqlite3.connect('student_data.db')
cursor = conn.cursor()

# Tạo bảng students nếu chưa tồn tại
cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                    dot TEXT, 
                    ma_lop TEXT, 
                    ten_mh TEXT, 
                    name TEXT, 
                    mssv TEXT, 
                    UNIQUE(mssv, ma_lop) -- Đảm bảo mssv và ma_lop là duy nhất trong tổ hợp
                )''')

# Tạo bảng absences nếu chưa tồn tại
cursor.execute('''CREATE TABLE IF NOT EXISTS absences (
                    mssv TEXT, 
                    ma_lop TEXT, 
                    ngay TEXT, 
                    vang_phep INTEGER, 
                    vang_khong_phep INTEGER, 
                    tong_tiet INTEGER,
                    FOREIGN KEY (mssv, ma_lop) REFERENCES students(mssv, ma_lop) -- Tham chiếu tới cặp mssv và ma_lop
                )''')
# # Thêm dữ liệu mẫu
# SAMPLE_DATA = [
#     {"dot": "2023", "ma_lop": "IT01", "ten_mh": "Computer Science", "name": "Nguyen Van A", "mssv": "123456"},
#     {"dot": "2023", "ma_lop": "IT02", "ten_mh": "Mathematics", "name": "Le Thi B", "mssv": "789012"},
#     {"dot": "2023", "ma_lop": "IT01", "ten_mh": "Computer Science", "name": "Pham Van C", "mssv": "345678"},
# ]
#
# SAMPLE_ABSENCES = [
#     {"mssv": "123456", "ma_lop": "IT01", "ngay": "2024-09-10", "vang_phep": 1, "vang_khong_phep": 0, "tong_tiet": 5},
#     {"mssv": "123456", "ma_lop": "IT01", "ngay": "2024-09-15", "vang_phep": 0, "vang_khong_phep": 1, "tong_tiet": 5},
#     {"mssv": "789012", "ma_lop": "IT02", "ngay": "2024-09-12", "vang_phep": 0, "vang_khong_phep": 1, "tong_tiet": 5},
# ]
#
# # Chèn dữ liệu sinh viên vào bảng students
# for student in SAMPLE_DATA:
#     cursor.execute("INSERT OR IGNORE INTO students VALUES (?, ?, ?, ?, ?)",
#                    (student["dot"], student["ma_lop"], student["ten_mh"], student["name"], student["mssv"]))
#
# # Chèn dữ liệu vắng mặt vào bảng absences
# for absence in SAMPLE_ABSENCES:
#     cursor.execute("INSERT OR IGNORE INTO absences VALUES (?, ?, ?, ?, ?, ?)",
#                    (absence["mssv"], absence["ma_lop"], absence["ngay"], absence["vang_phep"], absence["vang_khong_phep"], absence["tong_tiet"]))
# Lưu và đóng kết nối
conn.commit()
conn.close()


def get_sample_data():
    conn = sqlite3.connect('student_data.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    student_data = [
        {"dot": row[0], "ma_lop": row[1], "ten_mh": row[2], "name": row[3], "mssv": row[4]}
        for row in rows
    ]

    conn.close()
    return student_data

def get_sample_absences():
    conn = sqlite3.connect('student_data.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM absences")
    rows = cursor.fetchall()
    absence_data = [
        {"mssv": row[0], "ma_lop": row[1], "ngay": row[2], "vang_phep": row[3], "vang_khong_phep": row[4], "tong_tiet": row[5]}
        for row in rows
    ]

    conn.close()
    return absence_data

# Gọi hàm để lấy dữ liệu thay vì truy cập trực tiếp vào biến
SAMPLE_DATA = get_sample_data()
SAMPLE_ABSENCES = get_sample_absences()

# Ví dụ khi sử dụng
print(SAMPLE_DATA)
print(SAMPLE_ABSENCES)