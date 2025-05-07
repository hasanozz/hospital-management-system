# 🏥 Hospital Management System

This project is a comprehensive **Hospital Database Management System** developed using **Oracle SQL** and **Python with Tkinter GUI**.

It covers:
- ER modeling and database normalization
- SQL DDL & DML for table creation, constraints, and triggers
- PL/SQL packages and procedures for data operations
- Python GUI for managing patients, doctors, departments, and appointments

---

## 🧩 Features

### ✅ Database (Oracle SQL)
- 12+ normalized tables in **3rd Normal Form**
- Proper use of **primary, foreign and composite keys**
- **PL/SQL Package** for insert, update, delete operations
- **Trigger** for audit logging in `Admission_Log`
- Dynamic SQL queries with variable filters
- Duplicate removal procedure

### ✅ Python GUI (Tkinter)
- login(with oracle password)
- Modular UI with separate windows for:
  - Add & view patients
  - Add & view doctors (with department selection)
  - Add departments
- Record search with filter (e.g. search by name or contact)
- Edit and delete records
- Date input with format guidance

---

## 🛠 Requirements

- Oracle Database (tested on 21c XE)
- Python 3.10+
- Python packages:
  ```bash
  pip install tkcalendar cx_Oracle



GitHub: @cukuryunusemre
