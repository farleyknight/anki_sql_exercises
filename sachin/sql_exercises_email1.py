import datetime
import pandas as pd
from sqlalchemy import create_engine

# NOTE: This will need to be changed based on the local environment
engine = create_engine("postgresql://fknight:@localhost/postgres")

def parse_date(string):
    return datetime.datetime.strptime(string, '%Y-%m-%d').date()

def test_equal(actual, expected):
    if actual.equals(expected):
        print("Success!")
    else:
        print("Fail! The expected was different from the actual")
        print(actual.compare(expected))

################################################################
# BusesAndPassengers
################################################################

class BusesAndPassengers:
    def __init__(self):
        pd.read_sql("""
DROP TABLE IF EXISTS buses;
CREATE TABLE buses (
  id INT,
  origin VARCHAR(20),
  destination VARCHAR(20),
  time TIME
);

INSERT INTO buses
VALUES
    (10, 'Warsaw', 'Berlin', '10:55'),
    (20, 'Berlin', 'Paris',  '06:20'),
    (21, 'Berlin', 'Paris',  '14:00'),
    (22, 'Berlin', 'Paris',  '21:40'),
    (30, 'Paris',  'Madrid', '13:30');
SELECT * FROM buses;
        """, engine)

    def expected(self):
        return pd.DataFrame({
            'id':                  [10, 20, 21, 22, 30],
            'passengers_on_board': [ 0,  1,  3,  1,  1]
        })

    def run(self):
        ####################
        # SQL answer below #
        ####################

        actual = pd.read_sql("""
WITH b as (
    select *, lag(time) over (partition by origin, destination order by time) as prev_time
    from buses
)

SELECT b.id, count(p.id) as passengers_on_board
FROM b left join
     passengers p
     ON p.origin = b.origin AND
        p.destination = b.destination AND
        (p.time > b.prev_time or b.prev_time is null) AND
        (p.time <= b.time)
GROUP BY b.id
ORDER BY b.id;
        """, engine)

        test_equal(actual, self.expected())

print("*********")
print("BusesAndPassengers")

# Find passengers on board for each bus.

BusesAndPassengers().run()

################################################################
# PatientProblem
################################################################


class PatientProblem:
    def __init__(self):
        pd.read_sql("""
DROP TABLE IF EXISTS patients;
CREATE TABLE patients (
    PatientID INT,
    AdmissionDate DATE,
    DischargeDate DATE,
    Cost MONEY
);

-- Insert Data
INSERT INTO patients
VALUES
    (1009, '2014-07-27', '2014-07-31', 1050.00),
    (1009, '2014-08-01', '2014-08-23', 1070.00),
    (1009, '2014-08-31', '2014-08-31', 1900.00),
    (1009, '2014-09-01', '2014-09-14', 1260.00),
    (1009, '2014-12-01', '2014-12-31', 2090.00),
    (1024, '2014-06-07', '2014-06-28', 1900.00),
    (1024, '2014-06-29', '2014-07-31', 2900.00),
    (1024, '2014-08-01', '2014-08-02', 1800.00);

SELECT * FROM patients;
        """, engine)

    def expected(self):
        return pd.DataFrame({
            'patientid': [1009, 1009, 1009, 1024],
            'admissiondate': [
                parse_date('2014-07-27'),
                parse_date('2014-08-31'),
                parse_date('2014-12-01'),
                parse_date('2014-06-07')
            ],
            'dischargedate': [
                parse_date('2014-08-23'),
                parse_date('2014-09-14'),
                parse_date('2014-12-31'),
                parse_date('2014-08-02')
            ],
            'cost': [
                '$2,120.00',
                '$3,160.00',
                '$2,090.00',
                '$6,600.00'
            ]
        })

    def run(self):
        ####################
        # SQL answer below #
        ####################

        actual = pd.read_sql("""
WITH seq AS (
    SELECT
        *,
        CASE
        WHEN (AdmissionDate - interval '1 day') = LAG(DischargeDate, 1)
            OVER (ORDER BY PatientID, AdmissionDate)
        THEN 0
        ELSE 1
        END as start_of_seq
    FROM
        patients
),

ranks AS (
    SELECT
        *,
        SUM(start_of_seq)
            OVER (ORDER BY PatientID, AdmissionDate)
            AS date_rank
    FROM seq
)

SELECT
    patientid,
    min(admissiondate) as admissiondate,
    max(dischargedate) as dischargedate,
    sum(cost) as cost
FROM ranks
GROUP BY PatientID, date_rank
ORDER BY PatientID, AdmissionDate;
        """, engine)

        test_equal(actual, self.expected())

print("*********")
print("PatientProblem")

# In this puzzle we have to group data based on Patients admission date and discharge date. If any Patients discharge date + 1 = admission date then we have group both rows into one row and sum costs from both the rows. Please check out the sample input and expected output for details.

PatientProblem().run()

################################################################
# CandidateJoining
################################################################

class CandidateJoining:
    def __init__(self):
        pd.read_sql("""
DROP TABLE IF EXISTS holidays;
CREATE TABLE holidays(
    ID          INTEGER  NOT NULL PRIMARY KEY,
    HolidayDate DATE  NOT NULL
);

INSERT INTO holidays
VALUES
    (101, to_date('10-01-2015', 'DD-MM-YYYY')),
    (102, to_date('09-01-2015', 'DD-MM-YYYY')),
    (103, to_date('19-02-2015', 'DD-MM-YYYY')),
    (104, to_date('11-03-2015', 'DD-MM-YYYY')),
    (105, to_date('11-04-2015', 'DD-MM-YYYY'));

DROP TABLE IF EXISTS candidate_joining;
CREATE TABLE candidate_joining (
    CId          VARCHAR(7) NOT NULL PRIMARY KEY,
    CJoiningDate DATE  NOT NULL
);

INSERT INTO candidate_joining
VALUES
    ('CJ10101', to_date('10-01-2015', 'DD-MM-YYYY')),
    ('CJ10104', to_date('10-01-2015', 'DD-MM-YYYY')),
    ('CJ10105', to_date('18-02-2015', 'DD-MM-YYYY')),
    ('CJ10121', to_date('11-03-2015', 'DD-MM-YYYY')),
    ('CJ10198', to_date('11-04-2015', 'DD-MM-YYYY'));

SELECT * FROM candidate_joining;
        """, engine)

    def expected(self):
        data = [
           ('CJ10101',
            parse_date('2015-01-10'),
            parse_date('2015-01-08')),

           ('CJ10104',
            parse_date('2015-01-10'),
            parse_date('2015-01-08')),

           ('CJ10105',
            parse_date('2015-02-18'),
            parse_date('2015-02-18')),

           ('CJ10121',
            parse_date('2015-03-11'),
            parse_date('2015-03-10')),

           ('CJ10198',
            parse_date('2015-04-11'),
            parse_date('2015-04-10'))
        ]

        return pd.DataFrame(data, columns=['cid', 'cjoiningdate', 'valid_join_date'])

    def run(self):
        ####################
        # SQL answer below #
        ####################
        actual = pd.read_sql("""
WITH seq AS (
    SELECT
        ID,
        HolidayDate,
        CASE
        WHEN HolidayDate = LAG(HolidayDate, 1)
            OVER (ORDER BY HolidayDate) + 1
        THEN 0
        ELSE 1
        END AS start_of_seq
    FROM Holidays
),

ranks AS (
    SELECT
        ID,
        HolidayDate,
        start_of_seq,
        SUM(start_of_seq) OVER (ORDER BY HolidayDate) AS holiday_rank
    FROM seq
),

min_max AS (
    SELECT
        MIN(HolidayDate) AS min_date,
        MAX(HolidayDate) AS max_date
    FROM ranks
    GROUP BY holiday_rank
)

SELECT
    CId,
    CJoiningDate,
    CASE
    WHEN Min_Date IS NULL
    THEN CJoiningDate ELSE Min_Date - 1
    END as Valid_Join_Date
FROM candidate_joining j
LEFT JOIN min_max c
ON j.CJoiningDate
    BETWEEN c.Min_Date AND c.Max_Date
        """, engine)

        test_equal(actual, self.expected())


print("*********")
print("CandidateJoining")

# In this puzzle we have to find out the valid candidate joining date for each candidate. E.g if you check for CID the joining date is 10-01-2015 and as per the company’s holiday table they have holiday. So in this case we have to prepone the joining by one day. Hence for CJ10101 the valid joining date would be 08-01-2015 as they have holiday on 09-01-2015 also. Please check out the sample input and expected output for details.

CandidateJoining().run()


################################################################
# GoldRate
################################################################

class GoldRate:
    def __init__(self):
        pd.read_sql("""
DROP TABLE IF EXISTS rates;
CREATE TABLE rates (
    dt   DATE  NOT NULL PRIMARY KEY,
    rate INT  NOT NULL
);

INSERT INTO rates
VALUES
    (to_date('18-09-2014', 'DD-MM-YYYY'), 27000),
    (to_date('19-09-2014', 'DD-MM-YYYY'), 27000),
    (to_date('20-09-2014', 'DD-MM-YYYY'), 31000),
    (to_date('21-09-2014', 'DD-MM-YYYY'), 31000),
    (to_date('22-09-2014', 'DD-MM-YYYY'), 31000),
    (to_date('23-09-2014', 'DD-MM-YYYY'), 32000),
    (to_date('24-09-2014', 'DD-MM-YYYY'), 31000),
    (to_date('25-09-2014', 'DD-MM-YYYY'), 32000),
    (to_date('26-09-2014', 'DD-MM-YYYY'), 27000);

SELECT * FROM rates;
        """, engine)

    def expected(self):
        data = [
            (datetime.date(2014, 9, 18), datetime.date(2014, 9, 19), 27000),
            (datetime.date(2014, 9, 20), datetime.date(2014, 9, 22), 31000),
            (datetime.date(2014, 9, 23), datetime.date(2014, 9, 23), 32000),
            (datetime.date(2014, 9, 24), datetime.date(2014, 9, 24), 31000),
            (datetime.date(2014, 9, 25), datetime.date(2014, 9, 25), 32000),
            (datetime.date(2014, 9, 26), datetime.date(2014, 9, 26), 27000)
        ]

        return pd.DataFrame(data, columns=['startdate', 'enddate', 'rate'])

    def run(self):
        ####################
        # SQL answer below #
        ####################
        actual = pd.read_sql("""
WITH binary_seq AS (
    SELECT
        *,
        CASE
        WHEN rate = LAG(rate, 1)
            OVER (ORDER BY dt)
        THEN 0
        ELSE 1
        END as start_of_seq
    FROM rates
),

ranks AS (
    SELECT
        *,
        SUM(start_of_seq) OVER (ORDER BY dt) AS date_rank
    FROM binary_seq
)

SELECT
    MIN(dt) as StartDate,
    MAX(dt) as EndDate,
    MAX(Rate) as Rate
FROM ranks
GROUP BY date_rank
ORDER BY StartDate;
        """, engine)

        test_equal(actual, self.expected())

print("*********")
print("GoldRate")

# In the puzzle we have gold rate changing all the time. We have to find the start date, end Date and the gold rate at that duration. If the gold rate is changed then only we have create a new row. Please check the sample input and the expected output.

GoldRate().run()


################################################################
# AverageStepTime
################################################################

class AverageStepTime:
    def __init__(self):
        pd.read_sql("""
DROP TABLE IF EXISTS steps;
CREATE TABLE steps (
    session_id int,
    step_no int,
    end_secs int
);

INSERT INTO steps
VALUES
    (1,1,10),
    (1,2,25),
    (1,3,45),
    (1,4,60),
    (2,1,15),
    (2,2,20),
    (2,3,40),
    (2,4,60),
    (3,1,10),
    (3,2,22),
    (3,3,42),
    (3,4,50),
    (4,1,5),
    (4,2,12),
    (4,3,24),
    (4,4,36);

SELECT * FROM steps;
        """, engine)

    def expected(self):
        data = [(1, 9.75), (2, 18.0), (3, 13.75)]
        return pd.DataFrame(data, columns=['step_no', 'avg'])

    def run(self):
        ####################
        # SQL answer below #
        ####################
        actual = pd.read_sql("""
WITH step_times AS (
    SELECT
        a.session_id,
        a.step_no,
        a.end_secs,
        b.end_secs,
        (b.end_secs - a.end_secs) AS total_step_time
    FROM steps a
    JOIN steps b
    ON a.step_no + 1 = b.step_no
    AND a.session_id = b.session_id
    ORDER BY 1, 2
)

SELECT
    step_no,
    CAST(AVG(total_step_time) AS float)
FROM step_times
GROUP BY step_no
ORDER BY step_no
        """, engine)

        test_equal(actual, self.expected())

print("*********")
print("AverageStepTime")

# Given below is a table showing when a session started on a step. For each step, determine the average step time, without using `LEAD` or `LAG`.

AverageStepTime().run()


################################################################
# MinutesStreamed
################################################################

class MinutesStreamed:
    def __init__(self):
        pd.read_sql("""
DROP TABLE IF EXISTS minute_streamed;

CREATE TABLE minute_streamed (
    time_minute timestamp,
    username varchar(50),
    category varchar(50),
    concurrent_viewers int
);

INSERT INTO minute_streamed
VALUES
    ('2020-03-18 12:00:00', 'alex',  'Fornite',                      125),
    ('2020-03-18 12:01:00', 'alex',  'Fornite',                      130),
    ('2020-03-19 15:30:00', 'jamie', 'Just Chatting',                 13),
    ('2020-03-19 15:31:00', 'jamie', 'Food & Drink',                  15),
    ('2020-03-20 10:30:00', 'rick',  'Call of Duty: Black Ops',      150),
    ('2020-03-20 10:31:00', 'rick',  'Call of Duty: Modern Warfare', 120),
    ('2020-04-21 09:30:00', 'rick',  'Fornite',                      120),
    ('2020-04-20 10:31:00', 'rick',  'Call of Duty: Modern Warfare', 120),
    ('2020-04-21 09:30:00', 'rick',  'Fornite',                      120),
    ('2020-04-20 10:31:00', 'jamie', 'Call of Duty: Modern Warfare', 120),
    ('2020-04-21 09:30:00', 'jamie', 'Fornite',                      120),
    ('2020-04-18 12:00:00', 'alex',  'Fornite',                      125),
    ('2020-04-18 12:01:00', 'alex',  'Fornite',                      130),
    ('2020-06-18 14:00:00', 'alex',  'Fornite',                      120);

SELECT * FROM minute_streamed;
        """, engine)

    def part_A_expected(self):
        data = [
            (2020, 3, 0.10000),
            (2020, 4, 0.11667),
            (2020, 6, 0.01667)
        ]

        return pd.DataFrame(data, columns=['year', 'month', 'hours'])

    def part_A_actual(self):
        return pd.read_sql("""
SELECT
    CAST(EXTRACT(year from time_minute) AS int) AS year,
    CAST(EXTRACT(month from time_minute) as int) AS month,
    ROUND(cast(1.0*count(*) / 60 as decimal), 5) as hours
FROM minute_streamed
GROUP BY year, month
ORDER BY year, month
        """, engine)

    def part_A(self):
        actual = self.part_A_actual()
        test_equal(actual, self.part_A_expected())

    def part_B_expected(self):
        data = [
            ('jamie', 0.0167, 0.25),
            ('rick',  0.0500, 0.6),
            ('alex',  0.0000, 0.0)
        ]

        return pd.DataFrame(data, columns=['username', 'cod_hours', 'cod_percent'])

    def part_B_actual(self):
        return pd.read_sql("""
WITH is_cods AS (
    SELECT
        *,
        CASE
            WHEN CATEGORY LIKE '%%Call of Duty%%'
            THEN 1
            ELSE 0
        END AS is_cod
    FROM
        minute_streamed
)

SELECT
    username,
    ROUND(1.0*SUM(is_cod) / 60, 4) AS cod_hours,
    CAST(SUM(is_cod)/(1.0*count(*)) AS float) AS cod_percent
FROM
    is_cods
GROUP BY username
        """, engine)

    def part_B(self):
        actual = self.part_B_actual()
        test_equal(actual, self.part_B_expected())

    def part_C_expected(self):
        data = [
            ('alex',  2020, 3, 2.0, 0.0, 2.0),
            ('jamie', 2020, 3, 2.0, 0.0, 2.0),
            ('rick',  2020, 3, 2.0, 0.0, 2.0),
            ('rick',  2020, 4, 3.0, 2.0, 1.0)
        ]

        columns = [
            'username',
            'year',
            'month',
            'minutes',
            'previous_month_minutes',
            'diff'
        ]

        return pd.DataFrame(data, columns=columns)

    def part_C_actual(self):
        return pd.read_sql("""
WITH streamer_minutes AS (
    SELECT
        username,
        CAST(EXTRACT(YEAR from time_minute) as int) AS year,
        CAST(EXTRACT(month from time_minute) as int) AS month,
        1.0*COUNT(*) AS minutes
    FROM minute_streamed
    GROUP BY year, month, username
),

prev_month_minutes AS (
    SELECT
        *,
        COALESCE(
            LAG(minutes, 1)
                OVER
                (PARTITION BY username
                 ORDER BY year, month),
            0
        ) AS previous_month_minutes
    FROM streamer_minutes
),

diffs AS (
    SELECT
        *,
        minutes - previous_month_minutes AS diff
    FROM prev_month_minutes
)

SELECT
    *
FROM diffs
WHERE diff > 0
        """, engine)

    def part_C(self):
        actual = self.part_C_actual()
        test_equal(actual, self.part_C_expected())

print("*********")
print("MinutesStreamed")

# This table is a "heartbeat" tracking event where one row is generated each minute for each streamer while that streamer is live. If a streamer is live for 60 minutes, 60 rows would be generated in this table.

ms = MinutesStreamed()

# Write a query that returns total monthly hours streamed for each month, in order by month.
print("MinutesStreamed -- Part A")
ms.part_A()

print("MinutesStreamed -- Part B")
ms.part_B()

print("MinutesStreamed -- Part C")
ms.part_C()
