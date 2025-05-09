# 🏥 Hospital Management System

This repository contains a Hospital Management System developed as an academic project using Oracle SQL/PLSQL and Python (Tkinter) for the graphical user interface.

It allows users to efficiently manage patient admissions, doctor records, payments, medical records, and departmental data in a structured and user-friendly database environment.

---

## 🧩 Project Overview

### 📚 Database (Oracle SQL/PLSQL)

* **Database Normalization**: Designed using 12 relational tables that meet **3rd Normal Form (3NF)** requirements.
* **Integrity Constraints**: Includes well-defined **Primary Keys**, **Foreign Keys**, and **Composite Keys**.
* **PL/SQL Packages**:

  * `Patient_Pkg`: Manages patient-related operations (add, update, delete).
  * `Payment_Pkg`: Handles payment operations and statuses.
* **Trigger**: Records audit logs for patient admissions using the `Admission_Log` table.
* **Dynamic Queries**: Various query examples provided in `queries/dynamic_select_examples.sql`.
* **Procedures**: Includes a procedure to remove duplicate patient entries.

### 🖥️ Python GUI (Tkinter)

* **User Login**: Secure Oracle database login.
* **Modular GUI Components**:

  * Patient management (add, view, edit, delete)
  * Doctor management with department selection
  * Department management
  * Medical records management
  * Payment management (add, view, mark as paid)
  * Admission management (admission, discharge, room allocation)
* **Search and Filter**: Allows dynamic searching by patient, doctor, or payment details.
* **User-friendly Inputs**: Includes calendar-based date entry using `tkcalendar`.

---

## 🚀 Getting Started

### 📦 Requirements

* Oracle Database (Oracle XE 21c recommended)
* Python 3.10 or newer
* Python libraries:

  ```bash
  pip install tkcalendar cx_Oracle
  ```

### 🔧 Installation

1. **Clone the Repository:**

```bash
git clone https://github.com/hasanozz/hospital-management-system.git
```

2. **Setup Oracle Database:**

Run the SQL scripts in the given order from their respective folders:

```bash
tables/create_tables.sql
tables/create_constraints.sql
packages/patient_pkg.sql
packages/payment_pkg.sql
triggers/trg_admission_log.sql
procedures/remove_duplicates.sql
```

3. **Run Python Application:**

Navigate to the project root folder and execute:

```bash
python hospital_gui.py
```

Enter your Oracle SYSTEM password when prompted.

---

## 📌 Project Structure

```
hospital-management-system/
├── hospital_gui.py
├── packages
│   ├── patient_pkg.sql
│   └── payment_pkg.sql
├── procedures
│   └── remove_duplicates.sql
├── queries
│   └── dynamic_select_examples.sql
├── tables
│   ├── create_constraints.sql
│   └── create_tables.sql
├── triggers
│   └── trg_admission_log.sql
├── .gitignore
├── e-r.pdf
└── README.md
```

---

## 📐 ER Diagram

The database follows a clear and structured design:

* **Patients**: Personal and contact details.
* **Doctors**: Associated with departments, managing appointments.
* **Appointments**: Linked to patients and doctors.
* **Departments**: Doctors are assigned here.
* **Admissions & Rooms**: Tracks patient admissions, room allocation.
* **Medical Records & Prescriptions**: Detailed patient health records.
* **Payments**: Financial tracking related to patients.

---

## 👨‍💻 Author

* **GitHub:** [@hasanozz](https://github.com/hasanozz)

---
