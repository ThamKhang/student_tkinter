# data.py
import sqlite3
from tkinter import messagebox

from student_management.getter_data import SAMPLE_DATA, SAMPLE_ABSENCES, get_sample_absences


def load_all_students():
    """Loads the sample student data."""
    return SAMPLE_DATA

def load_absences_for_student(mssv, ma_lop):
    """Loads absence data for the selected student."""
    print(f"Fetching absences for MSSV: {mssv}, Ma lop: {ma_lop}")  # Debugging line

    absences = [a for a in get_sample_absences() if str(a['mssv']) == str(mssv) and str(a['ma_lop']) == str(ma_lop)]

    # Debugging print to show the filtering process
    for absence in get_sample_absences():
        print(f"Checking absence: MSSV: {absence['mssv']}, Ma lop: {absence['ma_lop']}")

    if not absences:
        print("No absences found for this student in the specified class.")  # Additional debug line
    else:
        print(f"Found absences: {absences}")  # Debugging line

    return absences




def sort_students(data, key, reverse=False):
    """Sorts the students based on a specified key."""
    return sorted(data, key=lambda x: x[key], reverse=reverse)

def add_student_to_db(dot, ma_lop, ten_mh, name, mssv):
    conn = sqlite3.connect('student_data.db')
    cursor = conn.cursor()
    # Kiểm tra xem sinh viên có tồn tại dựa trên MSSV và mã lớp
    cursor.execute('''SELECT * FROM students WHERE mssv = ? AND ma_lop = ?''', (mssv, ma_lop))
    result = cursor.fetchone()

    if result:
        messagebox.showwarning("Duplicate Entry", "Sinh viên với MSSV và Mã lớp này đã tồn tại.")
    else:
        cursor.execute('''INSERT INTO students (dot, ma_lop, ten_mh, name, mssv)
                          VALUES (?, ?, ?, ?, ?)''', (dot, ma_lop, ten_mh, name, mssv))
        conn.commit()
    conn.close()


def delete_student_from_db(mssv, ma_lop):
    conn = sqlite3.connect('student_data.db')
    cursor = conn.cursor()
    # Debugging line
    print(f"Executing DELETE for MSSV: {mssv}, Ma lop: {ma_lop}")

    # Delete student based on MSSV and ma_lop
    cursor.execute('DELETE FROM students WHERE mssv = ? AND ma_lop = ?', (mssv, ma_lop))
    conn.commit()
    conn.close()
