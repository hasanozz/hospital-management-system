-- Ad ve Soyad’a göre hasta arama
DECLARE
  v_first_name VARCHAR2(50) := 'Hasan';
  v_last_name  VARCHAR2(50) := 'Kaya';
BEGIN
  FOR rec IN (
    SELECT * FROM Patients
    WHERE first_name = v_first_name AND last_name = v_last_name
  )
  LOOP
    DBMS_OUTPUT.PUT_LINE(rec.patient_id || ' - ' || rec.first_name || ' ' || rec.last_name);
  END LOOP;
END;
/

-- Cinsiyete göre hasta listeleme
DECLARE
  v_gender VARCHAR2(10) := 'Male';
BEGIN
  FOR rec IN (
    SELECT * FROM Patients
    WHERE gender = v_gender
  )
  LOOP
    DBMS_OUTPUT.PUT_LINE(rec.first_name || ' ' || rec.last_name || ' - ' || rec.gender);
  END LOOP;
END;
/

-- Belirli bir tarih aralığında yapılan ödemeleri listeleme
DECLARE
  v_start_date DATE := TO_DATE('2024-01-01', 'YYYY-MM-DD');
  v_end_date   DATE := TO_DATE('2024-12-31', 'YYYY-MM-DD');
BEGIN
  FOR rec IN (
    SELECT * FROM Payments
    WHERE payment_date BETWEEN v_start_date AND v_end_date
  )
  LOOP
    DBMS_OUTPUT.PUT_LINE('Ödeme ID: ' || rec.payment_id || ' - Tutar: ' || rec.amount);
  END LOOP;
END;
/
