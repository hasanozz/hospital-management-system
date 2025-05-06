-- Foreign key (yabancı anahtar) ilişkileri

-- Doctors → Departments
ALTER TABLE Doctors
ADD CONSTRAINT fk_doctor_dept
FOREIGN KEY (department_id)
REFERENCES Departments(department_id);

-- Appointments → Patients & Doctors
ALTER TABLE Appointments
ADD CONSTRAINT fk_appt_patient
FOREIGN KEY (patient_id)
REFERENCES Patients(patient_id);

ALTER TABLE Appointments
ADD CONSTRAINT fk_appt_doctor
FOREIGN KEY (doctor_id)
REFERENCES Doctors(doctor_id);

-- Prescriptions → Appointments & Doctors
ALTER TABLE Prescriptions
ADD CONSTRAINT fk_presc_appt
FOREIGN KEY (appointment_id)
REFERENCES Appointments(appointment_id);

ALTER TABLE Prescriptions
ADD CONSTRAINT fk_presc_doc
FOREIGN KEY (doctor_id)
REFERENCES Doctors(doctor_id);

-- Prescription_Details → Prescriptions & Medications
ALTER TABLE Prescription_Details
ADD CONSTRAINT fk_presc_detail_presc
FOREIGN KEY (prescription_id)
REFERENCES Prescriptions(prescription_id);

ALTER TABLE Prescription_Details
ADD CONSTRAINT fk_presc_detail_med
FOREIGN KEY (medication_id)
REFERENCES Medications(medication_id);

-- Medical_Records → Patients & Doctors
ALTER TABLE Medical_Records
ADD CONSTRAINT fk_record_patient
FOREIGN KEY (patient_id)
REFERENCES Patients(patient_id);

ALTER TABLE Medical_Records
ADD CONSTRAINT fk_record_doctor
FOREIGN KEY (doctor_id)
REFERENCES Doctors(doctor_id);

-- Admissions → Patients & Rooms
ALTER TABLE Admissions
ADD CONSTRAINT fk_admission_patient
FOREIGN KEY (patient_id)
REFERENCES Patients(patient_id);

ALTER TABLE Admissions
ADD CONSTRAINT fk_admission_room
FOREIGN KEY (room_id)
REFERENCES Rooms(room_id);

-- Admission_Log → Admissions
ALTER TABLE Admission_Log
ADD CONSTRAINT fk_log_admission
FOREIGN KEY (admission_id)
REFERENCES Admissions(admission_id);

-- Payments → Patients
ALTER TABLE Payments
ADD CONSTRAINT fk_payment_patient
FOREIGN KEY (patient_id)
REFERENCES Patients(patient_id);
