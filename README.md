# Student Management System

This project is a **Student Management System** with a user-friendly GUI built using **Tkinter**. It allows users to manage student information, track absences, generate reports, process emails, and apply filtering and sorting on student data. 

## Features
- **Add, View, and Delete Students:** Easily manage student records including student IDs, class codes, names, and total absences.
- **Absence Tracking:** Track student absences and display total absences per course.
- **Filter and Sort Students:** Sort students by name, total absences, class, or subject. Filter by class or absence count.
- **Excel Data Import:** Load student data from Excel files stored in a specific directory.
- **Email Processing:** Monitor incoming emails for student-related queries, check replies, and auto-generate reports.
- **Chat Box Integration:** Includes a chatbot for basic student information management.

## Setup

1. **Install Dependencies:**  
   Ensure you have Python installed. Required libraries include `tkinter`, `ttk`, `pandas`, and `openpyxl` (for Excel handling).

   ```bash
   pip install pandas openpyxl
Directory Structure:
Organize your project files as follows:

kotlin
Sao chép mã
student_management/
    ├── functions.py
    ├── data.py
    ├── email_handler.py
    ├── getter_data.py
    ├── report.py
    ├── ...
utils.py
gui.py
README.md
Run the Application:
Execute the main GUI file to start the application.

bash
Sao chép mã
python gui.py
Usage
Main Window
Load Excel Data: Select an Excel file from the class_list directory to populate the student data.
Search: Search for students by name or student ID (MSSV).
Filter & Sort Options: Select sorting criteria (name, total absences, class, subject) and apply filters by class or minimum absences.
Add, View, and Delete Students: Add new students, view details, and delete records as needed.
Reports and Email Handling: Generate absence reports and monitor email inbox for queries or reports not replied to within 24 hours.
Chat Box: Access a chatbot for interactive student information management.
Requirements
Python 3.6 or higher
tkinter (usually included with Python)
pandas and openpyxl for Excel handling
Contributing
Contributions to improve the functionality or design are welcome! Feel free to submit pull requests or open issues for feedback.

License
This project is licensed under the MIT License.

vbnet
Sao chép mã

This README provides an overview of features, setup instructions, and usage details for users to get started with the application.
