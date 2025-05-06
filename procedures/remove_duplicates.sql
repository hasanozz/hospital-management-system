-- Aynı isim, soyisim ve doğum tarihine sahip tekrar eden hastaları temizler.
-- En küçük ID’li (ilk girilen) hasta kaydı tutulur.

CREATE OR REPLACE PROCEDURE Remove_Duplicate_Patients AS
BEGIN
  DELETE FROM Patients
  WHERE patient_id NOT IN (
    SELECT MIN(patient_id)
    FROM Patients
    GROUP BY first_name, last_name, date_of_birth
  );
END;
/
