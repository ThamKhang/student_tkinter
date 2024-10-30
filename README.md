# Quản Lý Sinh Viên - Python GUI App

This is a Python GUI application built with Tkinter for managing student information, absences, and related tasks. 

## Features

* **Student Data Management:**
    * Load student data from Excel files (`class_list` directory).
    * Database integration (using `sqlite3`).
    * Search and filtering by name, MSSV (Student ID), class, subject, and absences.
    * Add and delete student records.
    * View detailed student information with absence details, total classes, and absence percentage.
* **Absences Management:**
    * View a treeview of absence records for selected students.
    * Calculate total classes, total absences, and absence percentage.
* **Report Generation:**
    * Generate reports summarizing student data (requires implementation).
    * Warn students with excessive absences.
* **Email Handling:**
    * Send emails (using `smtplib`).
    * Automatically process emails (requires implementation).
    * Check if emails have been replied to within 24 hours.
* **Chat Box Integration:**
    * Chat box functionality (requires implementation).
* **User Interface:**
    * User-friendly GUI using Tkinter.
    * Comboboxes and checkboxes for easy selection and filtering.
    * Centralized window management.

## Requirements

* Python 3
* Tkinter
* `sqlite3` (optional)
* `smtplib` (for email handling)

## Installation

1. Install Python 3.
2. Install Tkinter (usually comes with Python).
3. Install other required libraries:
   ```bash
   pip install sqlite3
   pip install smtplib
