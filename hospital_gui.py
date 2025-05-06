import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import cx_Oracle
from datetime import datetime
from tkcalendar import DateEntry

# ---------------------- ORACLE CONNECTION ----------------------
def connect_to_oracle():
    global PASSWORD
    dsn = cx_Oracle.makedsn("localhost", 1521, service_name="XE")
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
            cursor.execute("""
                INSERT INTO Patients (first_name, last_name, date_of_birth, gender, contact_number, address)
                VALUES (:1, :2, TO_DATE(:3, 'YYYY-MM-DD'), :4, :5, :6)
            """, list(data.values()))
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

# ---------------------- MAIN UI ----------------------
def create_main_ui():
    main_frame = ttk.Frame(root)
    main_frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    ttk.Label(main_frame, text="Hospital Management System", 
             style='Header.TLabel').grid(row=0, column=0, columnspan=2, pady=20)
    
    buttons = [
        ("ADD Patients", open_add_patient),
        ("ADD Doctors", open_add_doctor),
        ("ADD Departments", open_add_department),
        ("Show Patients", lambda: show_list("Patients")),
        ("Show Doctors", lambda: show_list("Doctors")),
        ("Show Departments", lambda: show_list("Departments"))
    ]
    
    for i, (text, command) in enumerate(buttons, start=1):
        ttk.Button(main_frame, text=text, command=command, width=20).grid(
            row=i, column=0, pady=5, padx=10, sticky='ew')
    
    main_frame.columnconfigure(0, weight=1)

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