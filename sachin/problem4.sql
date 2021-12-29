-- PROBLEM
-- https://msbiskills.com/2015/03/22/t-sql-query-gold-rate-puzzle/


--Create table

CREATE TABLE [dbo].[testGoldRateChange]
  (
    [dt] [datetime] NULL,
    [Rate] [int] NULL
  );

--Insert Data
INSERT INTO [dbo].[testGoldRateChange](dt,Rate)
VALUES
  ('2014-09-18 06:25:19.897', 27000),
  ('2014-09-19 06:25:19.897', 27000),
  ('2014-09-20 06:25:19.897', 31000),
  ('2014-09-21 06:25:19.897', 31000),
  ('2014-09-22 06:25:19.897', 31000),
  ('2014-09-23 06:25:19.897', 32000),
  ('2014-09-24 06:25:19.897', 31000),
  ('2014-09-25 06:25:19.897', 32000),
  ('2014-09-26 06:25:19.897', 27000);

--Check data
SELECT dt,Rate FROM [dbo].[testGoldRateChange];


