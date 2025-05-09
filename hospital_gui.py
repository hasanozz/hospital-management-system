import os

os.environ['NLS_LANG'] = 'TURKISH_TURKEY.AL32UTF8'
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import cx_Oracle
from datetime import datetime
from tkcalendar import DateEntry


# ---------------------- ORACLE CONNECTION ----------------------
def connect_to_oracle():
    global PASSWORD
    dsn = cx_Oracle.makedsn("localhost", 1521, service_name="FREE")
    return cx_Oracle.connect("system", PASSWORD, dsn)

# ---------------------- COMMON WIDGET STYLING ----------------------
def configure_styles():
    style = ttk.Style()
    style.configure('TFrame', background='#f0f0f0')
    style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
    style.configure('TButton', font=('Arial', 10), padding=5)
    style.configure('Header.TLabel', font=('Arial', 12, 'bold'))

# ---------------------- ADD DOCTOR FORM ----------------------
def open_add_doctor():
    win = tk.Toplevel(root)
    win.title("Add Doctor")
    win.configure(bg='#f0f0f0')
    
    fields = [
        ("First Name", "text"),
        ("Last Name", "text"),
        ("Specialization", "text"),
        ("Contact", "text"),
        ("Email", "text"),
        ("Department", "combo", [])
    ]
    
    entries = {}
    ttk.Label(win, text="New Doctor Form", style='Header.TLabel').pack(pady=10)
    
    # Department combobox için veri yükleme
    try:
        conn = connect_to_oracle()
        cursor = conn.cursor()
        cursor.execute("SELECT department_id || ' - ' || department_name FROM Departments")
        departments = [row[0] for row in cursor.fetchall()]
        fields[5] = ("Department", "combo", departments)
    except Exception as e:
        messagebox.showerror("Error", f"Department load failed: {str(e)}")
    finally:
        if conn:
            conn.close()

    for field in fields:
        frame = ttk.Frame(win)
        frame.pack(pady=5, fill='x', padx=20)
        
        ttk.Label(frame, text=field[0]+":", width=15).pack(side='left')
        
        if field[1] == "text":
            entry = ttk.Entry(frame)
            entry.pack(side='left', expand=True, fill='x')
            entries[field[0]] = entry
        elif field[1] == "combo":
            cb = ttk.Combobox(frame, values=field[2], state='readonly')
            cb.pack(side='left', fill='x', expand=True)
            entries[field[0]] = cb

    def submit():
        try:
            dept_id = int(entries['Department'].get().split(" - ")[0])
            data = (
                entries['First Name'].get(),
                entries['Last Name'].get(),
                entries['Specialization'].get(),
                entries['Contact'].get(),
                entries['Email'].get(),
                dept_id
            )
            
            conn = connect_to_oracle()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Doctors (first_name, last_name, specialization, 
                contact_number, email, department_id)
                VALUES (:1, :2, :3, :4, :5, :6)
            """, data)
            conn.commit()
            messagebox.showinfo("Success", "Doctor added successfully!")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if conn:
                conn.close()

    ttk.Button(win, text="Submit", command=submit).pack(pady=10)

# ---------------------- ADD DEPARTMENT FORM ----------------------
def open_add_department():
    win = tk.Toplevel(root)
    win.title("Add Department")
    win.configure(bg='#f0f0f0')
    
    fields = [
        ("Department Name", "text"),
        ("Location", "text")
    ]
    
    entries = {}
    ttk.Label(win, text="New Department Form", style='Header.TLabel').pack(pady=10)
    
    for field in fields:
        frame = ttk.Frame(win)
        frame.pack(pady=5, fill='x', padx=20)
        
        ttk.Label(frame, text=field[0]+":", width=15).pack(side='left')
        
        entry = ttk.Entry(frame)
        entry.pack(side='left', expand=True, fill='x')
        entries[field[0]] = entry

    def submit():
        data = (
            entries['Department Name'].get(),
            entries['Location'].get()
        )
        
        try:
            conn = connect_to_oracle()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Departments (department_name, location)
                VALUES (:1, :2)
            """, data)
            conn.commit()
            messagebox.showinfo("Success", "Department added successfully!")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if conn:
                conn.close()

    ttk.Button(win, text="Submit", command=submit).pack(pady=10)

# ---------------------- COMMON WIDGET STYLING ----------------------
def configure_styles():
    style = ttk.Style()
    style.configure('TFrame', background='#f0f0f0')
    style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
    style.configure('TButton', font=('Arial', 10), padding=5)
    style.configure('Header.TLabel', font=('Arial', 12, 'bold'))

# ---------------------- IMPROVED DATE ENTRY ----------------------
def create_date_entry(parent):
    frame = ttk.Frame(parent)
    frame.pack(pady=5, fill='x')
    
    ttk.Label(frame, text="Date of Birth").pack(side='left')
    cal = DateEntry(
        frame,
        date_pattern='yyyy-mm-dd',
        font=('Arial', 10),
        background='darkblue',
        foreground='white',
        borderwidth=2
    )
    cal.pack(side='left', padx=10)
    return cal

# ---------------------- IMPROVED PATIENT FORM ----------------------
def open_add_patient():
    win = tk.Toplevel(root)
    win.title("Add Patient")
    win.configure(bg='#f0f0f0')
    
    fields = [
        ("First Name", "text"),
        ("Last Name", "text"),
        ("Date of Birth", "date"),
        ("Gender", "combo", ['Male', 'Female', 'Other']),
        ("Contact", "text"),
        ("Address", "text")
    ]
    
    entries = {}
    ttk.Label(win, text="New Patient Form", style='Header.TLabel').pack(pady=10)
    
    for field in fields:
        frame = ttk.Frame(win)
        frame.pack(pady=5, fill='x', padx=20)
        
        ttk.Label(frame, text=field[0]+":", width=15).pack(side='left')
        
        if field[1] == "text":
            entry = ttk.Entry(frame)
            entry.pack(side='left', expand=True, fill='x')
            entries[field[0]] = entry
        elif field[1] == "date":
            entries[field[0]] = create_date_entry(win)
        elif field[1] == "combo":
            cb = ttk.Combobox(frame, values=field[2], state='readonly')
            cb.pack(side='left', fill='x', expand=True)
            entries[field[0]] = cb

    def submit():
        data = {
            'first_name': entries['First Name'].get(),
            'last_name': entries['Last Name'].get(),
            'date_of_birth': entries['Date of Birth'].get(),
            'gender': entries['Gender'].get(),
            'contact_number': entries['Contact'].get(),
            'address': entries['Address'].get()
        }

        try:
            conn = connect_to_oracle()
            cursor = conn.cursor()
            cursor.callproc("Patient_Pkg.Add_Patient", [
    data['first_name'],
    data['last_name'],
    datetime.strptime(data['date_of_birth'], '%Y-%m-%d'),  # string yerine date objesi
    data['gender'],
    data['contact_number'],
    data['address']
])

            conn.commit()
            messagebox.showinfo("Success", "Patient added successfully!")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if conn:
                conn.close()




    ttk.Button(win, text="Submit", command=submit).pack(pady=10)


# ---------------------- UPDATE PATIENT ----------------------
def open_update_patient(patient_id):
    conn = connect_to_oracle()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Patients WHERE patient_id = :1", (patient_id,))
    patient_data = cursor.fetchone()
    conn.close()

    win = tk.Toplevel(root)
    win.title("Update Patient")
    win.configure(bg='#f0f0f0')
    
    fields = [
        ("First Name", "text"),
        ("Last Name", "text"),
        ("Date of Birth", "date"),
        ("Gender", "combo", ['Male', 'Female', 'Other']),
        ("Contact", "text"),
        ("Address", "text")
    ]
    
    entries = {}
    ttk.Label(win, text="Update Patient Form", style='Header.TLabel').pack(pady=10)
    
    # Verileri formda göster
    for i, field in enumerate(fields):
        frame = ttk.Frame(win)
        frame.pack(pady=5, fill='x', padx=20)
        
        ttk.Label(frame, text=field[0]+":", width=15).pack(side='left')
        
        if field[1] == "text":
            entry = ttk.Entry(frame)
            entry.insert(0, patient_data[i+1])  # ID 0. indekste olduğu için +1
            entry.pack(side='left', expand=True, fill='x')
            entries[field[0]] = entry
        elif field[1] == "date":
            cal = create_date_entry(win)
            cal.set_date(patient_data[3])  # date_of_birth 3. indekste
            entries[field[0]] = cal
        elif field[1] == "combo":
            cb = ttk.Combobox(frame, values=field[2], state='readonly')
            cb.set(patient_data[4])  # gender 4. indekste
            cb.pack(side='left', fill='x', expand=True)
            entries[field[0]] = cb

    def submit():
        data = (
            entries['First Name'].get(),
            entries['Last Name'].get(),
            entries['Date of Birth'].get(),
            entries['Gender'].get(),
            entries['Contact'].get(),
            entries['Address'].get(),
            patient_id
        )
        
        try:
            conn = connect_to_oracle()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Patients SET 
                first_name = :1,
                last_name = :2,
                date_of_birth = TO_DATE(:3, 'YYYY-MM-DD'),
                gender = :4,
                contact_number = :5,
                address = :6
                WHERE patient_id = :7
            """, data)
            conn.commit()
            messagebox.showinfo("Success", "Patient updated successfully!")
            win.destroy()
            show_list("Patients")  # Listeyi yenile
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if conn:
                conn.close()

    ttk.Button(win, text="Update", command=submit).pack(pady=10)
    # ---------------------- UPDATE DOCTOR ----------------------
def open_update_doctor(doctor_id):
    conn = connect_to_oracle()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Doctors WHERE doctor_id = :1", (doctor_id,))
    doctor_data = cursor.fetchone()
    cursor.execute("SELECT department_id || ' - ' || department_name FROM Departments")
    departments = [row[0] for row in cursor.fetchall()]
    conn.close()

    win = tk.Toplevel(root)
    win.title("Update Doctor")
    win.configure(bg='#f0f0f0')
    
    fields = [
        ("First Name", "text"),
        ("Last Name", "text"),
        ("Specialization", "text"),
        ("Contact", "text"),
        ("Email", "text"),
        ("Department", "combo", departments)
    ]
    
    entries = {}
    ttk.Label(win, text="Update Doctor Form", style='Header.TLabel').pack(pady=10)
    
    # Verileri formda göster
    for i, field in enumerate(fields):
        frame = ttk.Frame(win)
        frame.pack(pady=5, fill='x', padx=20)
        
        ttk.Label(frame, text=field[0]+":", width=15).pack(side='left')
        
        if field[1] == "text":
            entry = ttk.Entry(frame)
            entry.insert(0, doctor_data[i+1])  # ID 0. indekste
            entry.pack(side='left', expand=True, fill='x')
            entries[field[0]] = entry
        elif field[1] == "combo":
            cb = ttk.Combobox(frame, values=field[2], state='readonly')
            current_dept = f"{doctor_data[6]} - " + next((d.split(' - ')[1] for d in departments if d.startswith(str(doctor_data[6]))))
            cb.set(current_dept)
            cb.pack(side='left', fill='x', expand=True)
            entries[field[0]] = cb

    def submit():
        try:
            dept_id = int(entries['Department'].get().split(" - ")[0])
            data = (
                entries['First Name'].get(),
                entries['Last Name'].get(),
                entries['Specialization'].get(),
                entries['Contact'].get(),
                entries['Email'].get(),
                dept_id,
                doctor_id
            )
            
            conn = connect_to_oracle()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Doctors SET
                first_name = :1,
                last_name = :2,
                specialization = :3,
                contact_number = :4,
                email = :5,
                department_id = :6
                WHERE doctor_id = :7
            """, data)
            conn.commit()
            messagebox.showinfo("Success", "Doctor updated successfully!")
            win.destroy()
            show_list("Doctors")  # Listeyi yenile
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if conn:
                conn.close()

    ttk.Button(win, text="Update", command=submit).pack(pady=10)

# ---------------------- ENHANCED LIST VIEW ----------------------
def show_list(entity):
    win = tk.Toplevel(root)
    win.title(f"{entity} Management")
    win.geometry("1000x600")
    
    # Header
    header_frame = ttk.Frame(win)
    header_frame.pack(fill='x', padx=10, pady=10)
    
    ttk.Label(header_frame, text=f"{entity} List", style='Header.TLabel').pack(side='left')
    
    # Search Panel
    search_frame = ttk.Frame(win)
    search_frame.pack(fill='x', padx=10, pady=5)
    
    ttk.Label(search_frame, text="Search:").pack(side='left')
    search_entry = ttk.Entry(search_frame)
    search_entry.pack(side='left', padx=5)
    
    filter_combo = ttk.Combobox(search_frame, state='readonly')
    filter_combo.pack(side='left', padx=5)
    
    # Set default filters
    filter_map = {
        "Patients": ["first_name", "last_name", "gender", "contact_number"],
        "Doctors": ["first_name", "last_name", "specialization", "department_id"],
        "Departments": ["department_name", "location"]
    }
    filter_combo['values'] = filter_map.get(entity, [])
    filter_combo.current(1 if entity in ["Patients", "Doctors"] else 0)  # Default to last name
    
    action_frame = ttk.Frame(win)
    action_frame.pack(fill='x', padx=10, pady=5)
    
    tree = ttk.Treeview(win)
    tree.pack(fill='both', expand=True, padx=10, pady=10)
    
    # Configure columns
    tree['show'] = 'headings'
    
    # Add Scrollbar
    scrollbar = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
    scrollbar.pack(side='right', fill='y')
    tree.configure(yscrollcommand=scrollbar.set)
    
    def refresh():
        try:
            conn = connect_to_oracle()
            cursor = conn.cursor()
            if entity == "Patients":
                query = """
                    SELECT * FROM Patients
                    WHERE patient_id IN (
                        SELECT patient_id FROM Admissions
                        WHERE discharge_date IS NULL
                    )
                """
            else:
                query = f"SELECT * FROM {entity}"


            params = []
            
            search_term = search_entry.get().strip()
            filter_field = filter_combo.get()
            
            if search_term and filter_field:
                query += f" WHERE LOWER({filter_field}) LIKE LOWER(:1)"
                params.append(f'%{search_term}%')
            
            cursor.execute(query, params)
            
            # Clear tree
            tree.delete(*tree.get_children())
            
            # Configure columns
            columns = [desc[0] for desc in cursor.description]
            tree['columns'] = columns
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100, anchor='w')
            
            # Add data
            for row in cursor.fetchall():
                tree.insert('', 'end', values=row)
                
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if conn:
                conn.close()
    
    # Action Buttons
    ttk.Button(action_frame, text="Search", command=refresh).pack(side='left', padx=5)
    ttk.Button(action_frame, text="Delete", command=lambda: delete_record(entity)).pack(side='left', padx=5)
    ttk.Button(action_frame, text="Update", command=lambda: update_record(entity)).pack(side='left', padx=5)
    ttk.Button(action_frame, text="Refresh", command=refresh).pack(side='right', padx=5)
    
    def delete_record(entity):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a record to delete")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?")
        if not confirm:
            return

        try:
            conn = connect_to_oracle()
            cursor = conn.cursor()
            record_id = tree.item(selected[0])['values'][0]

            if entity == "Doctors":
                # önce medical record'lardaki doctor_id'yi NULL yap
                cursor.execute("UPDATE Medical_Records SET doctor_id = NULL WHERE doctor_id = :1", [record_id])

            cursor.execute(f"DELETE FROM {entity} WHERE {entity[:-1].lower()}_id = :1", (record_id,))
            conn.commit()
            refresh()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if conn:
                conn.close()

    
    def update_record(entity):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a record to update")
            return
        
        record_id = tree.item(selected[0])['values'][0]
        
        if entity == "Patients":
            open_update_patient(record_id)
        # Add similar update functions for Doctors and Departments
    
    refresh()



# ---------------------- ADD PAYMENT ------------------
def open_add_payment():
    win = tk.Toplevel(root)
    win.title("Add Payment")
    win.configure(bg='#f0f0f0')

    ttk.Label(win, text="New Payment", style='Header.TLabel').pack(pady=10)

    entries = {}

    # Hasta seçimi
    patient_frame = ttk.Frame(win)
    patient_frame.pack(pady=5, fill='x', padx=20)
    ttk.Label(patient_frame, text="Patient:", width=15).pack(side='left')

    patient_combo = ttk.Combobox(patient_frame, state='readonly')
    try:
        conn = connect_to_oracle()
        cursor = conn.cursor()
        cursor.execute("""
    SELECT p.patient_id || ' - ' || p.first_name || ' ' || p.last_name
    FROM Patients p
    JOIN Admissions a ON p.patient_id = a.patient_id
    WHERE a.discharge_date IS NULL
""")

        patients = [row[0] for row in cursor.fetchall()]
        patient_combo['values'] = patients
        patient_combo.pack(side='left', fill='x', expand=True)
        entries['Patient'] = patient_combo
    except Exception as e:
        messagebox.showerror("Error", f"Could not load patients: {str(e)}")
    finally:
        if conn:
            conn.close()

    # Tutar
    amount_frame = ttk.Frame(win)
    amount_frame.pack(pady=5, fill='x', padx=20)
    ttk.Label(amount_frame, text="Amount:", width=15).pack(side='left')
    amount_entry = ttk.Entry(amount_frame)
    amount_entry.pack(side='left', expand=True, fill='x')
    entries['Amount'] = amount_entry

    # Tarih (DateEntry)
    date_frame = ttk.Frame(win)
    date_frame.pack(pady=5, fill='x', padx=20)
    ttk.Label(date_frame, text="Due Date:", width=15).pack(side='left')
    due_date = DateEntry(date_frame, date_pattern='yyyy-mm-dd')
    due_date.pack(side='left', fill='x', expand=True)
    entries['Due Date'] = due_date

    def submit():
        try:
            patient_id = int(entries['Patient'].get().split(" - ")[0])
            amount = float(entries['Amount'].get())
            due = entries['Due Date'].get()  # 'yyyy-mm-dd' formatında

            conn = connect_to_oracle()
            cursor = conn.cursor()
            cursor.callproc("Payment_Pkg.Add_Payment", [patient_id, amount, due, ""])
            conn.commit()
            messagebox.showinfo("Success", "Payment added successfully.")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if conn:
                conn.close()

    ttk.Button(win, text="Submit", command=submit).pack(pady=10)

# ---------------------- SHOW PAYMENTS ----------------
def show_payments():
    win = tk.Toplevel(root)
    win.title("Payments")
    win.geometry("900x500")
    
    header_frame = ttk.Frame(win)
    header_frame.pack(fill='x', padx=10, pady=10)
    
    ttk.Label(header_frame, text="Payments List", style='Header.TLabel').pack(side='left')

    # Arama filtresi
    search_frame = ttk.Frame(win)
    search_frame.pack(fill='x', padx=10)
    ttk.Label(search_frame, text="Search by Status:").pack(side='left')
    
    status_filter = ttk.Combobox(search_frame, state='readonly', values=["", "Paid", "Unpaid"])
    status_filter.pack(side='left', padx=5)
    
    tree = ttk.Treeview(win, show='headings')
    tree.pack(fill='both', expand=True, padx=10, pady=10)
    
    scrollbar = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
    scrollbar.pack(side='right', fill='y')
    tree.configure(yscrollcommand=scrollbar.set)

    def refresh():
        try:
            conn = connect_to_oracle()
            cursor = conn.cursor()

            query = """SELECT p.payment_id,
                  pt.first_name || ' ' || pt.last_name AS patient_name,
                  p.amount,
                  TO_CHAR(p.payment_date, 'YYYY-MM-DD') AS payment_date,
                  p.status
           FROM Payments p
           JOIN Patients pt ON p.patient_id = pt.patient_id"""

            params = []
            if status_filter.get():
                query += " WHERE status = :1"
                params.append(status_filter.get())

            cursor.execute(query, params)

            tree.delete(*tree.get_children())
            columns = [desc[0] for desc in cursor.description]
            tree['columns'] = columns
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100)

            for row in cursor.fetchall():
                # row: (payment_id, patient_name, amount, payment_date, status)
                payment_id, patient_name, amount, payment_date, status = row
                formatted_row = (payment_id, patient_name, f"{amount:.2f} TL", payment_date, status)
                tree.insert('', 'end', values=formatted_row)

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if conn:
                conn.close()

    def mark_as_paid():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a payment.")
            return
        payment_id = tree.item(selected[0])['values'][0]
        try:
            conn = connect_to_oracle()
            cursor = conn.cursor()
            cursor.callproc("Payment_Pkg.Mark_As_Paid", [payment_id])
            conn.commit()
            messagebox.showinfo("Success", "Marked as Paid.")
            refresh()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if conn:
                conn.close()

    def delete_payment():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a payment to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this payment?")
        if not confirm:
            return

        payment_id = tree.item(selected[0])['values'][0]

        try:
            conn = connect_to_oracle()
            cursor = conn.cursor()
            cursor.callproc("Payment_Pkg.Delete_Payment", [payment_id])
            conn.commit()
            messagebox.showinfo("Success", "Payment deleted successfully.")
            refresh()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if conn:
                conn.close()


    action_frame = ttk.Frame(win)
    action_frame.pack(fill='x', padx=10, pady=10)

    ttk.Button(action_frame, text="Refresh", command=refresh).pack(side='right', padx=5)
    ttk.Button(action_frame, text="Mark as Paid", command=mark_as_paid).pack(side='left', padx=5)
    ttk.Button(action_frame, text="Delete", command=delete_payment).pack(side='left', padx=5)


    refresh()

# ---------------------- ADD MEDICAL RECORD ----------
def open_add_medical_record():
    win = tk.Toplevel(root)
    win.title("Add Medical Record")
    win.configure(bg='#f0f0f0')

    ttk.Label(win, text="New Medical Record", style='Header.TLabel').pack(pady=10)

    entries = {}

    # Patient selection
    patient_frame = ttk.Frame(win)
    patient_frame.pack(pady=5, fill='x', padx=20)
    ttk.Label(patient_frame, text="Patient:", width=15).pack(side='left')

    patient_combo = ttk.Combobox(patient_frame, state='readonly')
    entries['Patient'] = patient_combo
    patient_combo.pack(side='left', fill='x', expand=True)

    # Doctor selection
    doctor_frame = ttk.Frame(win)
    doctor_frame.pack(pady=5, fill='x', padx=20)
    ttk.Label(doctor_frame, text="Doctor:", width=15).pack(side='left')

    doctor_combo = ttk.Combobox(doctor_frame, state='readonly')
    entries['Doctor'] = doctor_combo
    doctor_combo.pack(side='left', fill='x', expand=True)

    # Diagnosis
    diag_frame = ttk.Frame(win)
    diag_frame.pack(pady=5, fill='x', padx=20)
    ttk.Label(diag_frame, text="Diagnosis:", width=15).pack(side='left')
    diag_entry = ttk.Entry(diag_frame)
    diag_entry.pack(side='left', expand=True, fill='x')
    entries['Diagnosis'] = diag_entry

    # Treatment
    treat_frame = ttk.Frame(win)
    treat_frame.pack(pady=5, fill='x', padx=20)
    ttk.Label(treat_frame, text="Treatment:", width=15).pack(side='left')
    treat_entry = ttk.Entry(treat_frame)
    treat_entry.pack(side='left', expand=True, fill='x')
    entries['Treatment'] = treat_entry

    # Load patient and doctor values
    try:
        conn = connect_to_oracle()
        cursor = conn.cursor()
        cursor.execute("SELECT patient_id || ' - ' || first_name || ' ' || last_name FROM Patients")
        patients = [row[0] for row in cursor.fetchall()]
        patient_combo['values'] = patients

        cursor.execute("SELECT doctor_id || ' - ' || first_name || ' ' || last_name FROM Doctors")
        doctors = [row[0] for row in cursor.fetchall()]
        doctor_combo['values'] = doctors

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load patients or doctors: {str(e)}")
    finally:
        if conn:
            conn.close()

    def submit():
        try:
            patient_id = int(entries['Patient'].get().split(" - ")[0])
            doctor_id = int(entries['Doctor'].get().split(" - ")[0])
            diagnosis = entries['Diagnosis'].get()
            treatment = entries['Treatment'].get()

            conn = connect_to_oracle()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Medical_Records (patient_id, doctor_id, diagnosis, treatment)
                VALUES (:1, :2, :3, :4)
            """, (patient_id, doctor_id, diagnosis, treatment))
            conn.commit()
            messagebox.showinfo("Success", "Medical record added successfully.")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if conn:
                conn.close()

    ttk.Button(win, text="Submit", command=submit).pack(pady=10)
 


# --------------------- SHOW MEDICAL RECORDS ---------
def show_medical_records():
    win = tk.Toplevel(root)
    win.title("Medical Records")
    win.geometry("1000x600")

    ttk.Label(win, text="Medical Records", style='Header.TLabel').pack(pady=10)

    tree = ttk.Treeview(win, show='headings')
    tree.pack(fill='both', expand=True, padx=10, pady=10)

    scrollbar = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
    scrollbar.pack(side='right', fill='y')
    tree.configure(yscrollcommand=scrollbar.set)

# delete medical record
    def delete_record():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a record to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?")
        if not confirm:
            return

        record_id = tree.item(selected[0])['values'][0]

        try:
            conn = connect_to_oracle()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Medical_Records WHERE record_id = :1", [record_id])
            conn.commit()
            messagebox.showinfo("Success", "Record deleted successfully.")
            refresh()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if conn:
                conn.close()



    def refresh():
        try:
            conn = connect_to_oracle()
            cursor = conn.cursor()

            base_query = """
                SELECT 
                    mr.record_id,
                    pt.first_name || ' ' || pt.last_name AS patient_name,
                    d.first_name || ' ' || d.last_name AS doctor_name,
                    mr.diagnosis,
                    mr.treatment,
                    TO_CHAR(mr.record_date, 'YYYY-MM-DD') AS record_date
                FROM Medical_Records mr
                JOIN Patients pt ON mr.patient_id = pt.patient_id
                JOIN Doctors d ON mr.doctor_id = d.doctor_id
                ORDER BY mr.record_date DESC
            """

            print("DEBUG - Executing query:", base_query)
            cursor.execute(base_query)
            rows = cursor.fetchall()
            print(f"DEBUG - {len(rows)} records found")

            tree.delete(*tree.get_children())
            columns = [desc[0] for desc in cursor.description]
            tree['columns'] = columns

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150)

            for row in rows:
                tree.insert('', 'end', values=row)

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if conn:
                conn.close()



    # Butonlar
    action_frame = ttk.Frame(win)
    action_frame.pack(fill='x', padx=10, pady=5)
    ttk.Button(action_frame, text="Refresh", command=refresh).pack(side='left', padx=5)
    ttk.Button(action_frame, text="Delete", command=delete_record).pack(side='left', padx=5)

    refresh()

# --------------------- SHOW ADMISSIONS --------------
def show_admissions():
    win = tk.Toplevel(root)
    win.title("Manage Admissions")
    win.geometry("900x500")

    ttk.Label(win, text="Active Admissions", style='Header.TLabel').pack(pady=10)

    tree = ttk.Treeview(win, show='headings', height=10)
    tree.pack(fill='both', expand=True, padx=10, pady=10)

    scrollbar = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
    scrollbar.pack(side='right', fill='y')
    tree.configure(yscrollcommand=scrollbar.set)

    def refresh():
        try:
            conn = connect_to_oracle()
            cursor = conn.cursor()
            cursor.execute("""
    SELECT 
        a.admission_id,
        p.first_name || ' ' || p.last_name AS patient_name,
        TO_CHAR(a.admission_date, 'YYYY-MM-DD') AS admission_date,
        NVL(TO_CHAR(a.discharge_date, 'YYYY-MM-DD'), '---') AS discharge_date,
        CASE 
            WHEN EXISTS (
                SELECT 1 FROM Payments pay 
                WHERE pay.patient_id = a.patient_id AND pay.status = 'Unpaid'
            ) THEN 'Unpaid'
            ELSE 'Paid'
        END AS payment_status
    FROM Admissions a
    JOIN Patients p ON a.patient_id = p.patient_id
    WHERE a.discharge_date IS NULL
    ORDER BY a.admission_date DESC
""")


            rows = cursor.fetchall()
            print(f"DEBUG - {len(rows)} kayıt bulundu")
            print("DEBUG - Rows:", rows)
            tree.delete(*tree.get_children())

            columns = [desc[0] for desc in cursor.description]
            tree['columns'] = columns
            print("DEBUG - Columns:", columns)
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150)

            for row in rows:
                formatted_row = [str(cell) if cell is not None else '' for cell in row]
                tags = ('unpaid',) if 'Unpaid' in formatted_row else ()
                tree.insert('', 'end', values=formatted_row, tags=tags)

            # Renk ayarı:
            tree.tag_configure('unpaid', background='#ffe5e5')  # açık kırmızı arka plan



        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def discharge_patient():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a record to discharge.")
            return

        admission_id = tree.item(selected[0])['values'][0]

        try:
            conn = connect_to_oracle()
            cursor = conn.cursor()

            # Hasta ID'sini al
            cursor.execute("SELECT patient_id FROM Admissions WHERE admission_id = :1", [admission_id])
            patient_id = cursor.fetchone()[0]

            # Ödenmemiş ödeme kontrolü
            cursor.execute("""
                SELECT COUNT(*) FROM Payments 
                WHERE patient_id = :1 AND status = 'Unpaid'
            """, [patient_id])
            unpaid = cursor.fetchone()[0]

            if unpaid > 0:
                messagebox.showwarning("Ödeme Gerekli", "Henüz hastane ücretleri ödenmedi.")
                return

            # Medical kayıt ilişiğini kopar
            cursor.execute("UPDATE Medical_Records SET patient_id = NULL WHERE patient_id = :1", [patient_id])

            # Admission log sil
            cursor.execute("DELETE FROM Admission_Log WHERE admission_id IN (SELECT admission_id FROM Admissions WHERE patient_id = :1)", [patient_id])

            # Diğer verileri sil
            cursor.execute("DELETE FROM Payments WHERE patient_id = :1", [patient_id])
            cursor.execute("DELETE FROM Admissions WHERE patient_id = :1", [patient_id])
            cursor.execute("DELETE FROM Patients WHERE patient_id = :1", [patient_id])
            conn.commit()

            messagebox.showinfo("Başarılı", "Hasta başarıyla taburcu edildi ve sistemden silindi.")
            refresh()

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if conn:
                conn.close()





    action_frame = ttk.Frame(win)
    action_frame.pack(fill='x', padx=10, pady=10)
    ttk.Button(action_frame, text="Refresh", command=refresh).pack(side='right', padx=5)
    ttk.Button(action_frame, text="Discharge Patient", command=discharge_patient).pack(side='left', padx=5)

    win.after(100, refresh)


# --------------------- OPEN ADD ADMISSION ------------
def open_add_admission():
    win = tk.Toplevel(root)
    win.title("Add Admission")
    win.configure(bg='#f0f0f0')

    ttk.Label(win, text="New Admission Form", style='Header.TLabel').pack(pady=10)

    entries = {}

    # --- Hasta Seçimi ---
    patient_frame = ttk.Frame(win)
    patient_frame.pack(pady=5, fill='x', padx=20)
    ttk.Label(patient_frame, text="Patient:", width=15).pack(side='left')
    patient_cb = ttk.Combobox(patient_frame, state='readonly')
    entries['Patient'] = patient_cb
    patient_cb.pack(side='left', fill='x', expand=True)

    # --- Oda Seçimi ---
    room_frame = ttk.Frame(win)
    room_frame.pack(pady=5, fill='x', padx=20)
    ttk.Label(room_frame, text="Room:", width=15).pack(side='left')
    room_cb = ttk.Combobox(room_frame, state='readonly')
    entries['Room'] = room_cb
    room_cb.pack(side='left', fill='x', expand=True)

    # --- Departman Seçimi ---
    dept_frame = ttk.Frame(win)
    dept_frame.pack(pady=5, fill='x', padx=20)
    ttk.Label(dept_frame, text="Department:", width=15).pack(side='left')
    dept_cb = ttk.Combobox(dept_frame, state='readonly')
    entries['Department'] = dept_cb
    dept_cb.pack(side='left', fill='x', expand=True)

    # --- Doktor Seçimi ---
    doctor_frame = ttk.Frame(win)
    doctor_frame.pack(pady=5, fill='x', padx=20)
    ttk.Label(doctor_frame, text="Doctor:", width=15).pack(side='left')
    doctor_cb = ttk.Combobox(doctor_frame, state='readonly')
    entries['Doctor'] = doctor_cb
    doctor_cb.pack(side='left', fill='x', expand=True)

    try:
        conn = connect_to_oracle()
        cursor = conn.cursor()

        # Hastaları yükle
        cursor.execute("SELECT patient_id || ' - ' || first_name || ' ' || last_name FROM Patients")
        patient_cb['values'] = [row[0] for row in cursor.fetchall()]

        # Odaları yükle
        cursor.execute("SELECT room_id || ' - ' || room_type FROM Rooms")
        room_cb['values'] = [row[0] for row in cursor.fetchall()]

        # Departmanları yükle
        cursor.execute("SELECT department_id || ' - ' || department_name FROM Departments")
        departments = [row[0] for row in cursor.fetchall()]
        dept_cb['values'] = departments

        # Departman seçimi değişince doktorlar dinamik yüklensin
        def update_doctors(event=None):
            try:
                selected_dept = dept_cb.get()
                if not selected_dept:
                    doctor_cb['values'] = []
                    return

                selected_dept_id = int(selected_dept.split(' - ')[0])

                conn = connect_to_oracle()
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT doctor_id || ' - ' || first_name || ' ' || last_name 
                    FROM Doctors WHERE department_id = :1
                """, [selected_dept_id])

                doctors = [row[0] for row in cursor.fetchall()]
                doctor_cb['values'] = doctors

                if doctors:
                    doctor_cb.current(0)

            except Exception as e:
                messagebox.showerror("Error", f"Doctor list could not be loaded: {str(e)}")
                doctor_cb['values'] = []
            finally:
                if 'conn' in locals():
                    conn.close()


        dept_cb.bind("<<ComboboxSelected>>", update_doctors)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load dropdown data: {str(e)}")
    finally:
        if conn:
            conn.close()

    def submit():
        try:
            patient_id = int(entries['Patient'].get().split(" - ")[0])
            room_id = int(entries['Room'].get().split(" - ")[0])
            doctor_id = int(entries['Doctor'].get().split(" - ")[0])

            conn = connect_to_oracle()
            cursor = conn.cursor()

            # 1. Admissions
            cursor.execute("""
                INSERT INTO Admissions (patient_id, room_id, admission_date)
                VALUES (:1, :2, SYSDATE)
            """, (patient_id, room_id))

            # 2. Medical Record
            cursor.execute("""
                INSERT INTO Medical_Records (patient_id, doctor_id, diagnosis, treatment)
                VALUES (:1, :2, 'Initial Evaluation', 'Pending')
            """, (patient_id, doctor_id))

            conn.commit()
            messagebox.showinfo("Success", "Admission and doctor assignment completed.")
            win.destroy()

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if conn:
                conn.close()

    ttk.Button(win, text="Submit", command=submit).pack(pady=10)



# ---------------------- MAIN UI ----------------------
def create_main_ui():
    main_frame = ttk.Frame(root, padding=20)
    main_frame.pack(fill='both', expand=True)

    ttk.Label(
        main_frame,
        text="🏥 Hospital Management System",
        style='Header.TLabel'
    ).pack(pady=(0, 20))

    # === Hasta Kayıt İşlemleri ===
    ttk.Label(main_frame, text="👤 Hasta Kayıt İşlemleri", style='Header.TLabel').pack(pady=(0, 5))

    group1 = ttk.Frame(main_frame)
    group1.pack(pady=5)
    ttk.Button(group1, text="➕ Add Patient", command=open_add_patient, width=30).pack(side='left', padx=10)
    ttk.Button(group1, text="🏥 Add Admission", command=open_add_admission, width=30).pack(side='left', padx=10)

    group2 = ttk.Frame(main_frame)
    group2.pack(pady=5)
    ttk.Button(group2, text="💰 Add Payment", command=open_add_payment, width=30).pack(side='left', padx=10)
    ttk.Button(group2, text="📝 Add Medical Record", command=open_add_medical_record, width=30).pack(side='left', padx=10)

    # === Yönetim İşlemleri ===
    ttk.Label(main_frame, text="🛠️ Yönetim İşlemleri", style='Header.TLabel').pack(pady=(20, 5))

    group3 = ttk.Frame(main_frame)
    group3.pack(pady=5)
    ttk.Button(group3, text="➕ Add Department", command=open_add_department, width=30).pack(side='left', padx=10)
    ttk.Button(group3, text="➕ Add Doctor", command=open_add_doctor, width=30).pack(side='left', padx=10)

    group4 = ttk.Frame(main_frame)
    group4.pack(pady=5)
    ttk.Button(group4, text="📋 Show Patients", command=lambda: show_list("Patients"), width=30).pack(side='left', padx=10)
    ttk.Button(group4, text="📋 Show Doctors", command=lambda: show_list("Doctors"), width=30).pack(side='left', padx=10)

    group5 = ttk.Frame(main_frame)
    group5.pack(pady=5)
    ttk.Button(group5, text="📋 Show Departments", command=lambda: show_list("Departments"), width=30).pack(side='left', padx=10)
    ttk.Button(group5, text="📄 Show Medical Records", command=show_medical_records, width=30).pack(side='left', padx=10)

    # === Taburcu İşlemleri ===
    ttk.Label(main_frame, text="✅ Hasta Taburcu İşlemleri", style='Header.TLabel').pack(pady=(20, 5))

    group6 = ttk.Frame(main_frame)
    group6.pack(pady=5)
    ttk.Button(group6, text="💳 Show Payments", command=show_payments, width=30).pack(side='left', padx=10)
    ttk.Button(group6, text="🏨 Manage Admissions", command=show_admissions, width=30).pack(side='left', padx=10)




# ---------------------- INITIALIZATION ----------------------
if __name__ == "__main__":
    PASSWORD = simpledialog.askstring("Oracle Login", "Enter SYSTEM Password:", show="*")
    if not PASSWORD:
        exit()
    
    root = tk.Tk()
    root.title("Hospital Management System")
    root.geometry("800x600")
    
    configure_styles()
    create_main_ui()
    
    root.mainloop()