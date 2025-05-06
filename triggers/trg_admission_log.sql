-- Hasta yatışı yapıldığında Admission_Log tablosuna otomatik log ekleyen trigger

CREATE OR REPLACE TRIGGER trg_admission_insert_log
AFTER INSERT ON Admissions
FOR EACH ROW
BEGIN
  INSERT INTO Admission_Log (
    admission_id,
    log_message,
    log_date
  ) VALUES (
    :NEW.admission_id,
    'Yeni yatış kaydı oluşturuldu.',
    SYSDATE
  );
END;
/
