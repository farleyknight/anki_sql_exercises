# BusesAndPassengers

NOTE: The code for this is in the `jupyter` directory, called `BusesAndPassengers`.


# PatientProblem

NOTE: The code for this is in the `jupyter` directory, called `PatientProblem`.


# CandidateJoining

NOTE: The code for this is in the `jupyter` directory, called `CandidateJoining`.


# GoldRate

NOTE: The code for this is in the `jupyter` directory, called `GoldRate`.

# AverageStepTime

TODO: This question does not yet have a complete entry under the `jupyter` directory.

Find the average step time without using `LEAD/LAG`.

```sql
create table steps (
    session_id int,
    step_no int, 
    end_secs int
)

insert into steps values(1,1,10);
insert into steps values(1,2,25);
insert into steps values(1,3,45);
insert into steps values(1,4,60);
insert into steps values(2,1,15);
insert into steps values(2,2,20);
insert into steps values(2,3,40);
insert into steps values(2,4,60);
insert into steps values(3,1,10);
insert into steps values(3,2,22);
insert into steps values(3,3,42);
insert into steps values(3,4,50);
insert into steps values(4,1,5);
insert into steps values(4,2,12);
insert into steps values(4,3,24);
insert into steps values(4,4,36);
```

select * From steps_fb order by 1,2

## Example answer

```sql
select 
    a.sessionid,
    a.stepno,
    a.endsecs,
    b.endsecs 
from steps_fb a
left join steps_fb b
on a.stepno+1 = b.stepno
and a.sessionid = b.sessionid
order by 1,2
```

# MinutesStreamed

```
time_minute         | streamer_username | category      | concurrent_viewers
----------------------------------------------------------------------------
2020-03-18 12:00:00 | alex              | Fortnite      |                1Q25
2020-03-18 12:01:00 | alex              | Fortnite      |                130
2020-03-19 15:30:00 | jamie             | Just Chatting |                 13
2020-03-19 15:31:00 | jamie             | Food & Drink  |                 15
2020-03-18 12:00:00 | alex              | Fortnite      |                1Q25
2020-03-18 12:01:00 | alex              | Fortnite      |                130
2020-03-18 12:02:00 | alex              | Fortnite      |                130
```

## Q1) Write a query that returns total monthly hours streamed for each month, in order by month.


SELECT EXTRACT(YEAR from time_minute) ,EXTRACT(month from time_minute) ,cast(count(*)  as float) / 60 as hours  --0.5

from 

minute_streamed

group by 1 ,2


2018,3 , 1000

1019,3, 1500 MIM

2018-03-01

2019-03 - 30 minuites


## Q2) Write a query that returns a row for each streamer with columns for their total hours streamed (in any category) and percentage of hours streamed in a Call of Duty game category. 

Examples of Call of Duty games include:

* Call of Duty: Black Ops
* Call of Duty: Modern Warfare
* Call of Duty: Advanced Warfare


SELECT streamer_username,(count(*)  as float) / 60 as TOTALhours  , SUM(CASE WHEN CATEGORY LIKE '%Call of Duty% THEN 1 ELSE 0 ) CALLOFDUTYHRS, (CAST(CALLOFDUTYHRS AS FLOAT)/TOTALhours) * 100

from 

minute_streamed

group by 1
 

-----

## Q3) For each calendar s, output the list of streamers who increased their hours streamed from the previous calendar month.


select year, month, streamer_username from 

(

Select EXTRACT(YEAR from time_minute) YEAR ,EXTRACT(month from time_minute) MNTH,streamer_username, cast(count(*)  as float) / 60 as hours ,LAG(hours,1) OVER (PARTITION BY USERNAME ORDER BY YEAR,MNTH) previous_mnth_hours , hours - previous_mnth_hours  diff

FROM minute_streamed

GROUP BY 1,2

) streamer_Data

where diff > 0 



SELECT YEAR,MONTH ,HOURS,LAG (HOURS,1) 

FROM 



(SELECT CM.YEAR,CM.MONTH, STREAMER , CASE WHEN streamer_Data.YEAR IS NULL THEN 0 ELSE hours



FROM 



(SELECT YEAR,MONTH,STREAMER  FROM CALENDAR 

WHERE YEAR BETWEEN 2018 AND 2019) CM 



LEFT OUTER JOIN 



(

Select EXTRACT(YEAR from time_minute) YEAR ,EXTRACT(month from time_minute) MNTH,streamer_username, cast(count(*)  as float) / 60 as hours 

FROM minute_streamed

GROUP BY 1,2

) SM



ON SM.YEAR  = CM.YEAR

AND SM.MNTH = CM.MONTH

AND SM.STREAMER = CM.STREAMER 

) FD







(SELECT YEAR,MONTH  FROM CALENDAR 

WHERE YEAR BETWEEN 2018 AND 2019) CM 



(SELECT streamer_username FROM  SM





2018,03 - alex

2018,04 - 0 



2018,03  - alex 

2018,03 -- sam

2018,05  - alex 

2018,05 -- sam

.

.

2018,12 - alex





2019,03 - sam

2019,04 

.

2019,06   sam  0 

2019,12   0 



---



2018,03 - alex - 50 null 

2018,04 - alex - 60 ,50

2018,05 -alex - 90  ,60



2019,03 - sam - 50 

2019,04 - sam - 40 ,50

2019,05 -sam - 100  ,40

2019,06 -> not streamed

2019,07 -> 120 , 90 , --->  



2019,07, sam 




## Q4) Write a query that returns a row for each streamer with columns for their average concurrent viewers in 2019 and their total minutes viewed from viewers in Japan (JP) in 2019.



minute_viewed 



time_minute         | viewer_username | viewer_country | streamer_username

--------------------------------------------------------------------------

2020-03-18 12:00:00 | taylor          | US             | alex

2020-03-18 12:01:00 | taylor          | US             | alex

2020-03-18 12:00:00 | charlie         | JP             | alex

2020-03-18 12:01:00 | charlie         | JP             | alex



Alex  HOURS

WHERE viewer_Country = JP





minute_streamed



time_minute         | streamer_username | category      | concurrent_viewers

----------------------------------------------------------------------------

2020-03-18 12:00:00 | alex              | Fortnite      |                125

2020-03-18 12:01:00 | alex              | Fortnite      |                130

2020-03-19 15:30:00 | jamie             | Just Chatting |                 13

2020-03-19 15:31:00 | jamie             | Food & Drink  |                 15



ALEX AVG(VIEWERS)




SELECT AC.streamer_username ,AVGCV ,COALESCE(TOTJPMIN ,0) 

FROM 



( 

SELECT streamer_username , AVG(concurrent_viewers)  AVGCV

WHERE EXTRACT(YEAR FROM time_minute) = 2019

GROUP BY 1 ) AC



LEFT JOIN 

(

SELECT STREAMER_USERNAME , COUNT(*) TOTJPMIN

WHERE viewer_country = 'JP'

AND EXTRACT(YEAR FROM time_minute) = 2019 ) MV



ON AC.streamer_username = MV.STREAMER_USERNAME
