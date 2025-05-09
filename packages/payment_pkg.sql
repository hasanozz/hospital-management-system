CREATE OR REPLACE PACKAGE Payment_Pkg AS
  PROCEDURE Add_Payment(
    p_patient_id  IN NUMBER,
    p_amount      IN NUMBER,
    p_due_date    IN VARCHAR2,
    p_description IN VARCHAR2
  );

  PROCEDURE Mark_As_Paid(p_payment_id IN NUMBER);
  PROCEDURE Delete_Payment(p_payment_id IN NUMBER);
END Payment_Pkg;
/

CREATE OR REPLACE PACKAGE BODY Payment_Pkg AS

  PROCEDURE Add_Payment(
    p_patient_id  IN NUMBER,
    p_amount      IN NUMBER,
    p_due_date    IN VARCHAR2,
    p_description IN VARCHAR2
  ) IS
  BEGIN
    INSERT INTO Payments (
      patient_id, amount, payment_date
    ) VALUES (
      p_patient_id, p_amount, TO_DATE(p_due_date, 'YYYY-MM-DD')
    );
  END Add_Payment;

  PROCEDURE Mark_As_Paid(p_payment_id IN NUMBER) IS
  BEGIN
    UPDATE Payments
    SET payment_date = SYSDATE
    WHERE payment_id = p_payment_id;
  END Mark_As_Paid;

  PROCEDURE Delete_Payment(p_payment_id IN NUMBER) IS
  BEGIN
    DELETE FROM Payments
    WHERE payment_id = p_payment_id;
  END Delete_Payment;

END Payment_Pkg;
/
