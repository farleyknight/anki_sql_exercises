-- PROBLEM : Determine the number of passengers on each bus

DROP TABLE IF EXISTS buses;
CREATE TABLE buses (
  id int,
  origin varchar(20),
  destination varchar(20),
  tmofday time
);

INSERT INTO buses VALUES (10, 'Warsaw', 'Berlin', '10:55');
INSERT INTO buses VALUES (20, 'Berlin', 'Paris',  '06:20');
INSERT INTO buses VALUES (21, 'Berlin', 'Paris',  '14:00');
INSERT INTO buses VALUES (22, 'Berlin', 'Paris',  '21:40');
INSERT INTO buses VALUES (30, 'Paris',  'Madrid', '13:30');

DROP TABLE IF EXISTS passengers;
CREATE TABLE passengers (
  id int,
  origin varchar(20),
  destination varchar(20),
  tmofday time
);

INSERT INTO passengers VALUES ( 1, 'Paris',  'Madrid', '13:30');
INSERT INTO passengers VALUES ( 2, 'Paris',  'Madrid', '13:31') ;
INSERT INTO passengers VALUES (10, 'Warsaw', 'Paris',  '10:00');
INSERT INTO passengers VALUES (11, 'Warsaw', 'Berlin', '22:31');
INSERT INTO passengers VALUES (40, 'Berlin', 'Paris',  '06:15');
INSERT INTO passengers VALUES (41, 'Berlin', 'Paris',  '06:50');
INSERT INTO passengers VALUES (42, 'Berlin', 'Paris',  '07:12');
INSERT INTO passengers VALUES (43, 'Berlin', 'Paris',  '12:03');
INSERT INTO passengers VALUES (44, 'Berlin', 'Paris',  '20:0');

-- SOLUTION
-- NOTE: I didn't come up with this on my own, but I did adapt it from an existing solution:
-- https://stackoverflow.com/a/68885782/47535

DROP TABLE IF EXISTS bus_schedule;

CREATE TABLE bus_schedule AS
  (
	  SELECT id,
	         origin,
	         destination,
	         LAG(time_of_day)
             OVER (partition by origin, destination order by tmofday)
             AS arrival_time,
	         time_of_day
	         	 AS departure_time
	    FROM buses
  );

SELECT
	bs.id,
	bs.origin,
	bs.destination,
	bs.arrival_time,
	COUNT(p.id) AS num_of_passengers
  FROM bus_schedule bs
	     LEFT JOIN passengers p
	         ON
		               p.origin = bs.origin AND
		               p.destination = bs.destination AND
		               (p.time_of_day >= bs.arrival_time OR bs.arrival_time IS NULL) AND
		               (p.time_of_day <= bs.departure_time)
 GROUP BY bs.id, bs.origin, bs.destination, bs.arrival_time
 ORDER BY bs.id;
