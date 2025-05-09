CREATE OR REPLACE PACKAGE BODY Patient_Pkg AS

  PROCEDURE Add_Patient(
    p_first_name     IN VARCHAR2,
    p_last_name      IN VARCHAR2,
    p_date_of_birth  IN DATE,
    p_gender         IN VARCHAR2,
    p_contact_number IN VARCHAR2,
    p_address        IN VARCHAR2
  ) IS
  BEGIN
    INSERT INTO Patients (
      first_name, last_name, date_of_birth, gender,
      contact_number, address
    ) VALUES (
      p_first_name, p_last_name, p_date_of_birth, p_gender,
      p_contact_number, p_address
    );
  END Add_Patient;

  PROCEDURE Update_Patient(
    p_patient_id     IN NUMBER,
    p_first_name     IN VARCHAR2,
    p_last_name      IN VARCHAR2,
    p_date_of_birth  IN DATE,
    p_gender         IN VARCHAR2,
    p_contact_number IN VARCHAR2,
    p_address        IN VARCHAR2
  ) IS
  BEGIN
    UPDATE Patients
    SET first_name     = p_first_name,
        last_name      = p_last_name,
        date_of_birth  = p_date_of_birth,
        gender         = p_gender,
        contact_number = p_contact_number,
        address        = p_address
    WHERE patient_id = p_patient_id;
  END Update_Patient;

  PROCEDURE Delete_Patient(
    p_patient_id IN NUMBER
  ) IS
  BEGIN
    UPDATE Medical_Records SET patient_id = NULL WHERE patient_id = p_patient_id;
    DELETE FROM Admissions WHERE patient_id = p_patient_id;
    DELETE FROM Payments WHERE patient_id = p_patient_id;
    DELETE FROM Patients WHERE patient_id = p_patient_id;
  END Delete_Patient;

END Patient_Pkg;
/
