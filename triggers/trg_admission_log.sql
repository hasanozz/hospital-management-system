DROP TRIGGER TRG_ADMISSION_INSERT_LOG;

CREATE OR REPLACE TRIGGER TRG_ADMISSION_INSERT_LOG
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
