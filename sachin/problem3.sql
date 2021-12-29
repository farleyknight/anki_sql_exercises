-- PROBLEM
-- https://msbiskills.com/2015/03/23/t-sql-query-the-candidate-joining-puzzle/

-- Create Table
CREATE TABLE Holidays
  (
    ID INT,
    HolidayDate DATETIME
  );

-- Insert Data
INSERT INTO Holidays(ID,HolidayDate)
VALUES
  (101,'01/10/2015'),
  (102,'01/09/2015'),
  (103,'02/19/2015'),
  (104,'03/11/2015'),
  (105,'04/11/2015');

-- Verify Data
SELECT ID,HolidayDate FROM Holidays;

-- Create Table
CREATE TABLE CandidateJoining
  (
    CId VARCHAR(17),
    CJoiningDate DATETIME
  );

-- Insert Data
INSERT INTO CandidateJoining(CId, CJoiningDate)
VALUES
  ('CJ10101','01/10/2015'),
  ('CJ10104','01/10/2015'),
  ('CJ10105','02/18/2015'),
  ('CJ10121','03/11/2015'),
  ('CJ10198','04/11/2015');

-- Verify Data

SELECT CId, CJoiningDate FROM CandidateJoining;
