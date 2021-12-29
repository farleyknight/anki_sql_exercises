-- PROBLEM:
-- https://msbiskills.com/2015/03/23/473/

-- T-SQL Query | [ The Patient Puzzle ]
-- In this puzzle we have to group data based on Patients admission date and discharge date.
-- If any Patients discharge date + 1 = admission date then we have group both rows into one row and sum costs from both the rows.
-- Please check out the sample input and expected output for details.

-- The solution should be should use “SELECT” statement or “CTE”.

-- Create Table

CREATE TABLE PatientProblem
  (
    PatientID INT,
    AdmissionDate DATETIME,
    DischargeDate DATETIME,
    Cost MONEY
  );

-- Insert Data
INSERT INTO PatientProblem
            (
              PatientID,
              AdmissionDate,
              DischargeDate,
              Cost
            )
VALUES
  (1009,'2014-07-27','2014-07-31',1050.00),
  (1009,'2014-08-01','2014-08-23',1070.00),
  (1009,'2014-08-31','2014-08-31',1900.00),
  (1009,'2014-09-01','2014-09-14',1260.00),
  (1009,'2014-12-01','2014-12-31',2090.00),
  (1024,'2014-06-07','2014-06-28',1900.00),
  (1024,'2014-06-29','2014-07-31',2900.00),
  (1024,'2014-08-01','2014-08-02',1800.00);

-- Verify Data
SELECT PatientID, AdmissionDate, DischargeDate, Cost
  FROM PatientProblem;
