
# CustomersAndProducts

```sql
CREATE TABLE orders (
    order_id INT,
    cust_id INT,
    prod_id INT,
    store_id INT,
    order_date DATE,
    order_amt INT
)
```


```
 customer_id |   cust_name    |    city    |
-------------+----------------+------------|
        3002 | Nick Rimando   | NY         |
        3007 | Brad Davis     | NY         |
        3005 | Graham Zusi    | TX         |
        3008 | Julian Green   | TX         |
        3004 | Fabian Johnson | TX         |
        3009 | Geoff Cameron  | MA         |
        3003 | Jozy Altidor   | MA         |
        3001 | Brad Guzan     | MA         |
```

```
order_id    order_amt   order_date  customer_id  store_id
----------  ----------  ----------  -----------  -----------
70001       150.5       2012-10-05  3005         5002
70009       270.65      2012-09-10  3001         5005
70002       65.26       2012-10-05  3002         5001
70004       110.5       2012-08-17  3009         5003
70007       948.5       2012-09-10  3005         5002
70005       2400.6      2012-07-27  3007         5001
70008       5760        2012-09-10  3002         5001
70010       1983.43     2012-10-10  3004         5006
70003       2480.4      2012-10-10  3009         5003
70012       250.45      2012-06-27  3008         5002
70011       75.29       2012-08-17  3003         5007
70013       3045.6      2012-04-25  3002         5001
```

NOTE: `order_amt` means "order amount"

## Part A

For each store show the % difference in sales between 2014 and 2015
### Example answer


```sql
select 
    store_id, 
    100 * case (sum(2015_sales) as decimal) - sum(2014_sales) / sum(2014_sales)
from
(
    select 
        store_id, 
        case 
        when extract (year from order_date) = '2014' 
        then sales_amt else 0 end as 2014_sales,
        case 
        when extract (year from order_date) = '2015' 
        then sales_amt else 0 end as 2015_sales
    from orders
) as t1
group by store_id;
```

## Part B

For each store show the % of all customers that have purchases at least 1 product

```sql
WITH cust_orders AS (
    select 
        cust_id, 
        case 
            when o.cust_id IS NULL
            then 0 
            else c.cust_id 
        end as cust_ordered
    from customers c 
    left join orders o on c.cust_id = o.cust_id;
)
select count(distinct cust_ordered) / count(distinct cust_id) * 100


```

## Part C

List all the customers that live in a state, ordered by the number of unique products they bought.

```sql
select * from customers c
left join orders o on c.cust_id = o.cust_id
left join product p on o.prod_id = p.prod_id
where state='UT'
order by count(distinct product_id) desc;
```

## Part D

Find the earliest born and last born customers, by gender, who have bought at least 1 product.


```sql
SELECT
    gender, 
    max(dob), 
    min(dob)
FROM customers 
JOIN orders o on c.cust_id = o.cust_id
WHERE dob IS NOT NULL
GROUP BY gender;
```

## Part E

Get top 3 orders for top 3 customers who have ordered product x but not y


```sql
SELECT cust_id
from(
    select 
        cust_id, 
        prod_id, 
        order_amt,
        count(distinct prod_id) over(partition by cust_id) as cnt, 
        row_number() 
            OVER (PARTITION by cust_id order by order_amt desc) 
            AS rn
    from customers c join orders o
    on c.cust_id = o.cust_id
    where o.prod_id in ('X','Y')
) 
where 
cnt=1 and prod_id='X'
and rn<=3;
```

# NetflixChannel

Identify all accounts that watched only Netflix in a particular month - An account 
can have multiple devices and can watch mutliple channels.

Streaming data
account_id varchar(40),
device_id varchar(40),
channel_name varchar(20),
play_hours FLOAT,
date_key varchar(10)
