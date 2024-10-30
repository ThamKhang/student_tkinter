import re
import tkinter as tk
from tkinter import scrolledtext
from student_management.functions import delete_student, update_treeview, load_students_from_excel, \
    sort_students_in_treeview, search_student, filter_by_class, filter_by_absences
from student_management.getter_data import SAMPLE_DATA

# Initialize session_state to keep track of user sessions
session_state = {}

# Mapping keywords to functions
keyword_function_map = {
    r"(tìm(?: kiếm)? sinh viên|tìm theo MSSV)": search_student,
    r"(tìm lớp|lọc lớp)": filter_by_class,
    r"(tỷ lệ vắng mặt|vắng mặt)": filter_by_absences,
    r"sắp xếp theo (tên|lớp|môn học|buổi vắng)": lambda tree, criteria: sort_students_in_treeview(tree, criteria),
    r"(thêm sinh viên|nhập sinh viên)": load_students_from_excel,
    r"xóa sinh viên": delete_student,
    r"(hiển thị tất cả sinh viên|hiện tất cả sinh viên)": update_treeview,
}

def extract_keywords(user_input):
    for pattern, function in keyword_function_map.items():
        match = re.search(pattern, user_input, re.IGNORECASE)
        if match:
            return match.group(0), function  # Return matched keyword and function
    return None, None

def chatbox(user_input, tree, user_id='0001'):

    """Handle user input and respond accordingly."""
    # Create a new session if the user_id is not in the session state
    if user_id not in session_state:
        session_state[user_id] = {"waiting_for": None}

    # Get the user's session state
    state = session_state[user_id]

    # Extract keywords and function from user input
    keyword, function = extract_keywords(user_input)

    if state["waiting_for"]:
        # Handle based on what the bot is waiting for
        if state["waiting_for"] == "student_query":
            query = user_input.strip()
            results = search_student(query, tree)  # Call search function
            state["waiting_for"] = None  # Reset state
            return f"Đã tìm kiếm sinh viên với từ khóa '{query}'. Kết quả tìm thấy: {results} sinh viên."

        elif state["waiting_for"] == "class_filter":
            class_name = user_input.strip()
            filter_by_class(tree, class_name)  # Call filter function
            state["waiting_for"] = None
            return f"Đã lọc lớp '{class_name}'."

        elif state["waiting_for"] == "absences_filter":
            try:
                min_absences = int(user_input.strip())
                filter_by_absences(tree, min_absences)  # Call filter function
                state["waiting_for"] = None
                return f"Đã lọc sinh viên có hơn {min_absences} buổi vắng mặt."
            except ValueError:
                return "Vui lòng nhập một số hợp lệ cho tỷ lệ vắng mặt."

    if function:
        # Check for specific keyword functions
        if re.search(r"tìm(?: kiếm)? sinh viên|tìm theo MSSV", keyword, flags=re.IGNORECASE):
            state["waiting_for"] = "student_query"  # Set waiting state
            return "Vui lòng nhập tên hoặc mã sinh viên."

        elif re.search(r"tìm lớp|lọc lớp", keyword, flags=re.IGNORECASE):
            state["waiting_for"] = "class_filter"  # Set waiting state
            return "Vui lòng nhập tên lớp."

        elif re.search(r"tỷ lệ vắng mặt", keyword, flags=re.IGNORECASE):
            state["waiting_for"] = "absences_filter"  # Set waiting state
            return "Vui lòng nhập tỷ lệ vắng mặt cần lọc dưới dạng số."

        elif re.search(r"sắp xếp theo (.+)", keyword, flags=re.IGNORECASE):
            criteria = re.search(r"sắp xếp theo (.+)", keyword, flags=re.IGNORECASE).group(1).strip()
            function(tree, criteria)  # Call sorting function
            return f"Đã sắp xếp sinh viên theo '{criteria}'."

        elif re.search(r"thêm sinh viên", keyword, flags=re.IGNORECASE):
            filename = "students.xlsx"  # Example filename
            function(filename)  # Call function to load students
            return f"Đã thêm sinh viên từ file '{filename}'."

        elif re.search(r"xóa sinh viên", keyword, flags=re.IGNORECASE):
            function(tree)  # Call delete function
            return "Đã xóa sinh viên được chọn trong danh sách."

        elif re.search(r"hiển thị tất cả sinh viên", keyword, flags=re.IGNORECASE):
            function(tree)  # Call update function
            return "Hiển thị tất cả sinh viên."

    return "Xin lỗi, tôi không hiểu yêu cầu của bạn. Vui lòng thử lại với một yêu cầu khác hoặc xem hướng dẫn sử dụng."


def chat_box(tree, main_window_ref):  # Thêm tham số cho cửa sổ chính
    # Lấy kích thước và vị trí của cửa sổ chính
    main_x = main_window_ref.winfo_x()  # Vị trí X của cửa sổ chính
    main_y = main_window_ref.winfo_y()  # Vị trí Y của cửa sổ chính
    main_width = main_window_ref.winfo_width()  # Chiều rộng của cửa sổ chính

    # Đẩy cửa sổ chính sang trái 200 pixel
    new_main_x = main_x - 200
    main_window_ref.geometry(f"{main_width}x800+{new_main_x}+{main_y}")

    # Tạo cửa sổ chat
    chat_window = tk.Toplevel()
    chat_window.title("Chat Box")
    chat_window.geometry("400x800")
    chat_window.configure(bg="#f0f0f0")  # Màu nền của cửa sổ chat

    # Đặt vị trí cho cửa sổ chat_box
    chat_window.geometry(f"+{new_main_x + main_width}+{main_y}")  # Vị trí bên phải cửa sổ chính

    # Thanh tiêu đề cho khung trò chuyện
    title_label = tk.Label(chat_window, text="Chat Bot", font=("Arial", 14, "bold"), bg="#4a90e2", fg="white")
    title_label.pack(fill=tk.X, pady=(0, 5))

    # Khu vực hiển thị tin nhắn
    output_box = scrolledtext.ScrolledText(chat_window, wrap=tk.WORD, width=60, height=30, state='disabled', bg="white",
                                           font=("Arial", 11))
    output_box.pack(pady=(10, 5))

    # Khung nhập tin nhắn
    input_frame = tk.Frame(chat_window, bg="#f0f0f0")
    input_frame.pack(fill=tk.X, padx=10, pady=(5, 10))

    # Khung nhập tin nhắn
    input_box = tk.Entry(input_frame, width=38, font=("Arial", 12))  # Ô nhập tin nhắn
    input_box.grid(row=0, column=0, padx=(0, 5), sticky="ew")

    # Đưa con trỏ vào ô nhập tin nhắn ngay khi mở cửa sổ chat
    input_box.focus_set()

    # Nút Gửi tin nhắn nằm dưới ô nhập
    send_button = tk.Button(input_frame, text="Gửi", font=("Arial", 12), command=lambda: send_message(), width=10)
    send_button.grid(row=1, column=0, pady=(5, 0))  # Đặt nút Gửi ở dòng 1, dưới ô nhập tin nhắn

    # Liên kết phím Enter với hàm gửi tin nhắn
    input_box.bind("<Return>", lambda event: send_message())

    # Hàm gửi tin nhắn
    def send_message():
        user_input = input_box.get()
        response = chatbox(user_input, tree)
        output_box.config(state='normal')
        output_box.insert(tk.END, f"User: {user_input}\nBot: {response}\n\n")
        output_box.config(state='disabled')
        output_box.yview(tk.END)  # Tự động cuộn xuống cuối
        input_box.delete(0, tk.END)

    # Nút Đóng để khôi phục lại vị trí cửa sổ chính
    close_button = tk.Button(chat_window, text="Đóng", font=("Arial", 12), command=lambda: close_chat(chat_window, restore_main_window))
    close_button.pack(pady=10)

    # Hàm khôi phục vị trí cửa sổ chính
    def restore_main_window():
        main_window_ref.geometry(f"{main_width}x800+{main_x}+{main_y}")

    # Hàm xử lý khi đóng cửa sổ chat
    def close_chat(chat_win, restore_func):
        chat_win.destroy()  # Đóng cửa sổ chat
        restore_func()  # Khôi phục vị trí cửa sổ chính

    chat_window.protocol("WM_DELETE_WINDOW", lambda: close_chat(chat_window, restore_main_window))

def on_chat_close(chat_window, main_window_ref):
    # Đặt lại vị trí cửa sổ chính về vị trí ban đầu khi cửa sổ chat đóng
    main_x = main_window_ref.winfo_x() + 200  # Trở về vị trí ban đầu
    main_width = main_window_ref.winfo_width()
    main_window_ref.geometry(f"{main_width}x800+{main_x}+{main_window_ref.winfo_y()}")

    chat_window.destroy()  # Đóng cửa sổ chat

