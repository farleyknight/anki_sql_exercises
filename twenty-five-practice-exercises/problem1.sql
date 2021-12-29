
-- https://towardsdatascience.com/twenty-five-sql-practice-exercises-5fc791e24082
-- From the following table of user IDs, actions, and dates, write a query to return the publication and cancellation rate for each user.

CREATE TABLE users (
  user_id int,
  action varchar(10),
  action_date date
);


INSERT INTO users VALUES 
                    (1,'start', CAST('01-01-20' AS date)), 
                    (1,'cancel', CAST('01-02-20' AS date)), 
                    (2,'start', CAST('01-03-20' AS date)), 
                    (2,'publish', CAST('01-04-20' AS date)), 
                    (3,'start', CAST('01-05-20' AS date)), 
                    (3,'cancel', CAST('01-06-20' AS date)), 
                    (1,'start', CAST('01-07-20' AS date)), 
                    (1,'publish', CAST('01-08-20' AS date)))

