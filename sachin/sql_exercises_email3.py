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
# CustomersAndProducts
################################################################

class CustomersAndProducts:
    def __init__(self):
        pd.read_sql("""
DROP TABLE IF EXISTS customers;
CREATE TABLE customers (
    cust_id INT,
    cust_name VARCHAR,
    state VARCHAR,
    dob DATE,
    gender VARCHAR
);

INSERT INTO customers
VALUES
    (3001, 'Brad Guzan',     'MA', '2001-01-01', 'm'),
    (3002, 'Nick Rimando',   'NY', '1991-01-01', 'm'),
    (3003, 'Jozy Altidor',   'MA', '1998-01-01', 'f'),
    (3004, 'Fabian Johnson', 'CA', '2002-01-01', 'm'),
    (3005, 'Graham Zusi',    'CA', '1990-01-01', 'm'),
    (3007, 'Brad Davis',     'NY', '1993-01-01', 'n'),
    (3008, 'Julian Green',   'CA', '1989-01-01', 'f'),
    (3009, 'Geoff Cameron',  'MA', '1999-01-01', 'n');

DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
    order_id INT,
    order_date DATE,
    order_amount FLOAT,
    cust_id INT,
    prod_id INT,
    store_id INT
);

INSERT INTO orders
    (order_amount, order_date, cust_id, store_id, prod_id)
VALUES
    (150.5,   '2014-10-05', 3005, 5002, 8001),
    (65.26,   '2014-10-05', 3002, 5001, 8002),
    (2480.4,  '2014-10-10', 3009, 5003, 8002),
    (110.5,   '2014-08-17', 3009, 5003, 8001),
    (2400.6,  '2015-07-27', 3007, 5001, 8001),
    (240.6,   '2015-08-07', 3002, 5003, 8001),
    (948.5,   '2015-09-10', 3005, 5002, 8002),
    (5760,    '2014-09-10', 3002, 5001, 8001),
    (270.65,  '2014-09-10', 3001, 5003, 8001),
    (1983.43, '2014-10-10', 3004, 5002, 8002),
    (250.45,  '2015-06-27', 3008, 5001, 8001),
    (75.29,   '2015-08-17', 3003, 5003, 8001),
    (3045.6,  '2015-04-25', 3002, 5001, 8002),
    (150.5,   '2015-10-05', 3005, 5002, 8001),
    (65.26,   '2015-10-05', 3002, 5001, 8002),
    (2480.4,  '2015-10-10', 3009, 5003, 8002),
    (110.5,   '2014-08-17', 3009, 5003, 8001),
    (2400.6,  '2015-07-27', 3007, 5001, 8001),
    (240.6,   '2014-08-07', 3002, 5003, 8001),
    (948.5,   '2015-09-10', 3005, 5002, 8002),
    (5760,    '2015-09-10', 3002, 5001, 8001),
    (270.65,  '2015-09-10', 3001, 5003, 8001),
    (1983.43, '2015-10-10', 3004, 5002, 8002),
    (250.45,  '2014-06-27', 3008, 5001, 8001),
    (75.29,   '2014-08-17', 3003, 5003, 8001),
    (3045.6,  '2014-04-25', 3002, 5001, 8002);

SELECT * FROM orders
        """, engine)

    def part_A_expected(self):
        data = [
            (5001, 53.00),
            (5002, 89.00),
            (5003, -7.00)
        ]

        return pd.DataFrame(data, columns=['store_id', 'percent_change'])

    def part_A(self):
        actual = pd.read_sql("""
WITH sales AS (
    SELECT
        store_id,
        CASE
        WHEN extract (year FROM order_date) = '2014'
        THEN order_amount
        ELSE 0
        END AS sales_2014,
        CASE
        WHEN extract (year FROM order_date) = '2015'
        THEN order_amount
        ELSE 0
        END AS sales_2015
    FROM orders
    ORDER BY store_id
)

SELECT
    store_id,
    100*ROUND(
        CAST(
            (1.0*sum(sales_2015) - sum(sales_2014)) / sum(sales_2014)
            AS decimal),
        2
    ) as percent_change

FROM sales
GROUP BY store_id;
        """, engine)

        test_equal(actual, self.part_A_expected())


    def part_B_expected(self):
        data = [
            (5001, 0.38),
            (5002, 0.25),
            (5003, 0.50)
        ]

        return pd.DataFrame(data, columns=['store_id', 'percent'])

    def part_B(self):
        actual = pd.read_sql("""
SELECT
    store_id,
    ROUND(
        1.0*COUNT(DISTINCT cust_id) / (SELECT COUNT(DISTINCT cust_id) FROM orders),
        2
    ) as percent
FROM orders
GROUP BY store_id
        """, engine)

        test_equal(actual, self.part_B_expected())

    def part_C_expected(self):
        data = [
            (3007, 1),
            (3002, 2)
        ]

        return pd.DataFrame(data, columns=['cust_id', 'uniq_products'])

    def part_C(self):
        actual = pd.read_sql("""
SELECT
    c.cust_id,
    COUNT(DISTINCT o.prod_id) AS uniq_products
FROM customers c
JOIN orders o
ON o.cust_id = c.cust_id
WHERE state = 'NY'
GROUP BY c.cust_id
ORDER BY uniq_products
        """, engine)

        test_equal(actual, self.part_C_expected())

    def part_D_expected(self):
        data = [
            ('n', datetime.date(1999, 1, 1), datetime.date(1993, 1, 1)),
            ('m', datetime.date(2002, 1, 1), datetime.date(1990, 1, 1)),
            ('f', datetime.date(1998, 1, 1), datetime.date(1989, 1, 1))
        ]

        return pd.DataFrame(data, columns=['gender', 'max', 'min'])

    def part_D(self):
        actual = pd.read_sql("""
SELECT
    gender,
    max(dob),
    min(dob)
FROM customers c
JOIN orders o on c.cust_id = o.cust_id
WHERE dob IS NOT NULL
GROUP BY gender;
        """, engine)

        test_equal(actual, self.part_D_expected())

    def part_E_expected(self):
        data = [
            (3002, 1, 1),
            (3002, 1, 2),
            (3002, 1, 3),
            (3007, 2, 1),
            (3007, 2, 2),
            (3001, 3, 1),
            (3001, 3, 2)
        ]

        return pd.DataFrame(data, columns=['cust_id', 'cust_rank', 'order_rank'])

    def part_E(self):
        actual = pd.read_sql("""
WITH order_ranking AS (
    SELECT
        c.cust_id,
        prod_id,
        order_amount,
        row_number()
            OVER (PARTITION by c.cust_id
                  ORDER BY order_amount DESC)
            AS order_rank
    FROM customers c
    JOIN orders o
    ON c.cust_id = o.cust_id
    WHERE prod_id = 8001
),

cust_ranking AS (
    SELECT
        cust_id,
        SUM(order_amount),
        ROW_NUMBER() OVER (ORDER BY SUM(order_amount) DESC) as cust_rank
    FROM order_ranking
    GROUP BY cust_id
)

SELECT
    c.cust_id,
    cust_rank,
    order_rank
FROM order_ranking o
JOIN cust_ranking c
ON c.cust_id = o.cust_id
WHERE cust_rank <= 3
AND order_rank <= 3
ORDER BY cust_rank, order_rank
        """, engine)

        test_equal(actual, self.part_E_expected())


print("*******")
print("CustomersAndProducts")

cap = CustomersAndProducts()

# For each store show the percentage difference in sales between 2014 and 2015.
print("CustomersAndProducts -- Part A")
cap.part_A()

# For each store, show the percentage of all customers that have purchased at least 1 product.
print("CustomersAndProducts -- Part B")
cap.part_B()

# List all the customers that live in NY state, ordered by the number of unique products they bought.
print("CustomersAndProducts -- Part C")
cap.part_C()

# Find the earliest born and last born customers, by gender, who have bought at least 1 product.
print("CustomersAndProducts -- Part D")
cap.part_D()

# Get top 3 orders for top 3 customers who have ordered product `8001` but not `8002`.
print("CustomersAndProducts -- Part E")
cap.part_E()


################################################################
# NetflixChannel
################################################################

class NetflixChannel:
    def __init__(self):
        pd.read_sql("""
DROP TABLE IF EXISTS streaming_data;
CREATE TABLE streaming_data (
    account_id INT,
    device_id INT,
    channel_name VARCHAR,
    play_hours FLOAT,
    watch_date DATE
);

INSERT INTO streaming_data
VALUES
    (1, 1, 'Netflix',         0.5, '2021-01-01'),
    (1, 1, 'Netflix',         0.5, '2021-01-02'),

    (2, 2, 'Hulu',            0.5, '2021-01-02'),
    (2, 3, 'Amazon Prime',    1.5, '2021-01-02'),
    (2, 3, 'Netflix',         1.5, '2021-01-03'),

    (3, 4, 'Disney+',         1.7, '2021-01-03'),
    (3, 4, 'Netflix',         0.5, '2021-01-03'),
    (3, 4, 'Disney+',         1.7, '2021-01-04'),

    (4, 5, 'Netflix',         2.0, '2021-01-03'),
    (4, 6, 'Netflix',         0.5, '2021-01-04'),

    (5, 7, 'Hulu',            0.5, '2021-01-03');

SELECT * FROM streaming_data;
        """, engine)

    def expected(self):
        data = [
            (1, 1.0),
            (4, 2.5)
        ]

        return pd.DataFrame(data, columns=['account_id', 'total_hours'])

    def run(self):
        actual = pd.read_sql("""
WITH only_netflix AS (
    SELECT
        *,
        CASE
        WHEN channel_name = 'Netflix'
        THEN 0
        ELSE 1
        END AS not_netflix
    FROM streaming_data
),

other_than_netflix AS (
    SELECT
        account_id,
        SUM(play_hours) as total_hours,
        SUM(not_netflix) as non_netflix_channels_watched
    FROM
        only_netflix
    GROUP BY account_id
)

SELECT
    account_id, total_hours
FROM other_than_netflix
WHERE non_netflix_channels_watched = 0
ORDER BY account_id
        """, engine)

        test_equal(actual, self.expected())

print("*******")
print("NetflixChannel")

NetflixChannel().run()
