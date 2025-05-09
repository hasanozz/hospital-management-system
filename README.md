# 🏥 Hospital Management System

This repository contains a **Hospital Management System** developed as an academic project using **Oracle SQL/PLSQL** and **Python (Tkinter)** for the graphical user interface.

It provides functionalities to manage patient admissions, doctor records, payments, medical records, and departmental data in a structured database environment.

---

## 🧩 Project Overview

### 📚 Database (Oracle SQL/PLSQL)

* **Database Normalization**: Designed with 12 relational tables adhering to **3rd Normal Form (3NF)**.
* **Integrity Constraints**: Implemented proper **Primary Keys**, **Foreign Keys**, and **Composite Keys**.
* **PL/SQL Packages**:

  * `Patient_Pkg`: CRUD operations for patients.
  * `Payment_Pkg`: Handles payments, marking payments as paid, and deletion.
* **Trigger**: Audit logging for admissions via `Admission_Log` table.
* **Dynamic Queries**: Demonstrates advanced query operations with variable filters.
* **Procedures**: Removal of duplicate patient records.

### 🖥️ Python GUI (Tkinter)

* **User Login**: Secure login prompt for Oracle credentials.
* **Modular GUI**:

  * Patient management (Add/View/Edit/Delete)
  * Doctor management (including department selection)
  * Department management
  * Medical records management
  * Payment management (Add, View, Mark as Paid)
  * Admission management (patient admissions, discharges, room assignments)
* **Dynamic Record Searching**: Filter records by multiple fields.
* **Enhanced User Experience**: Date selection using `tkcalendar` with formatted inputs.

---

## 🚀 Getting Started

### 📦 Requirements

* **Oracle Database**: Oracle XE (21c tested)
* **Python Version**: Python 3.10 or higher
* **Python Libraries**:

```bash
pip install tkcalendar cx_Oracle
```

### 🔧 Installation

1. **Clone the Repository:**

```bash
git clone https://github.com/hasanozz/hospital-management-system.git
```

2. **Setup Oracle Database**:

* Execute all SQL scripts located in the `sql_scripts/` directory in order:

  * `create_tables.sql`
  * `create_constraints.sql`
  * `patient_pkg.sql`
  * `payment_pkg.sql`
  * `trg_admission_log.sql`
  * `remove_duplicates.sql`

3. **Configure Python Application:**

* Navigate to the `gui/` directory and run:

```bash
python hospital_gui.py
```

* Enter your Oracle SYSTEM password at runtime.

---

## 🗂️ Project Structure

```
hospital-management-system/
├── gui/
│   └── hospital_gui.py
├── sql_scripts/
│   ├── create_tables.sql
│   ├── create_constraints.sql
│   ├── patient_pkg.sql
│   ├── payment_pkg.sql
│   ├── trg_admission_log.sql
│   └── remove_duplicates.sql
├── .gitignore
└── README.md
```

---

## 👨‍💻 Author

* **GitHub:** [@hasanozz](https://github.com/hasanozz)

---

**Note:** This project was developed strictly for educational purposes and should not be used in production environments.
