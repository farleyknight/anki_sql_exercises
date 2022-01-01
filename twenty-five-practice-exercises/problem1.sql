-- PROBLEM 1:
-- Cancellation rates

-- https://towardsdatascience.com/twenty-five-sql-practice-exercises-5fc791e24082

-- From the following table of user IDs, actions, and dates, write a query to return the publication and cancellation rate for each user.

CREATE TABLE users (
  user_id INT,
  action VARCHAR(10),
  action_date DATE
);

INSERT INTO users
VALUES
  (1,'start',   '01-01-20'),
  (1,'cancel',  '01-02-20'),
  (2,'start',   '01-03-20'),
  (2,'publish', '01-04-20'),
  (3,'start',   '01-05-20'),
  (3,'cancel',  '01-06-20'),
  (1,'start',   '01-07-20'),
  (1,'publish', '01-08-20');


-- SOLUTION
/*

  */
