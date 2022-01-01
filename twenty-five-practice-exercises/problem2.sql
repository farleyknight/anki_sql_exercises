-- PROBLEM 2:
-- Changes in net worth

-- https://towardsdatascience.com/twenty-five-sql-practice-exercises-5fc791e24082

-- From the following table of transactions between two users, write a query to return the change in net worth for each user, ordered by decreasing net change.


CREATE TABLE transactions (
  sender INT,
  receiver INT,
  amount INT,
  transaction_date DATE
);


INSERT INTO transactions
VALUES
  (5, 2, 10, '2-12-20'),
  (1, 3, 15, '2-13-20'),
  (2, 1, 20, '2-13-20'),
  (2, 3, 25, '2-14-20'),
  (3, 1, 20, '2-15-20'),
  (3, 2, 15, '2-15-20'),
  (1, 4, 5,  '2-16-20');

