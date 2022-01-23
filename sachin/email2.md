# Triangles

Write a query that checks the lengths of three sides, and determines if the triangle is isosceles, equilateral, scalene, or not a triangle.

Triangle_id  A   B    C
1            20  20  23
2            20  20  20
3            20  21  22
4            13  14  30

## Expected output

1  isosceles
2  equilateral
3  scalene
4  not a triangle

## Example answer

```sql
SELECT
    CASE 
        WHEN A+B < C THEN 'not a triangle' 
        WHEN A  = B AND B  = C THEN 'equilateral'
        WHEN A  = B AND B != C THEN 'isosceles'
        WHEN A != B AND B != C THEN 'scalene'
        ELSE NULL
    END AS triangle_type
FROM TRIANGLES
```

# StudentData

Show subject scores for each student.


## Sample Data

```sql
CREATE TABLE student_data (
  id      INTEGER,
  subject varchar(10),
  marks   integer
)

insert into student_data values (1,'English',60) ;
insert into student_data values (1,'Maths',70);
insert into student_data values (1,'Science',75);

insert into student_data values (2,'English',62);
insert into student_data values (2,'Maths',72);
insert into student_data values (2,'Science',85);
```

## Expected output

 StudentID Maths English Science 
 --------- ----- ------- -------
  1         70     60      75
  2         72     62      85


## Example answer

```sql
WITH subject_scores AS (
    SELECT 
        student_id,
        CASE
            WHEN subject = 'Maths' 
            THEN marks 
            ELSE 0 
        END as maths,
        CASE
            WHEN subject = 'English' 
            THEN marks
            ELSE 0 
        END as english,
        CASE
            WHEN subject = 'Science' 
            THEN marks 
            ELSE 0 
        END as science
    FROM student_data
)

SELECT 
    student_id,
    SUM(case when subject = ‘Maths’  then Marks else 0 end) as Maths ,sum(case when subject = ‘English’ then Marks else 0 ) as English ,,sum(case when subject = ‘Science’ then Marks else 0 ) as Science
GROUP BY id
```


# EmployeeDepartment

A table schema with tables like employee, department, employee_to_projects, projects

```sql
CREATE TABLE employees (
    employee_id  int
    name varchar
    title varchar
    last_name varchar
    start_date date
    salary int
    end_date date
    department_id int
    budget int
)
```

```sql
CREATE TABLE projects (
    id int
    project id int
    name varchar
    employee_id int
)
```

```sql
CREATE TABLE dept (
    id INT
    name varchar
)
```


## Part A

Show the Dept which works the highest paid employee win the company with their names and salary

## Part B

Determine which projects that have employees from more than one department.

## Part C

Select employee from departments where max salary of the department is 40k

## Part D

Select employee assigned to projects

## Part E

Select employee which have the max salary in a given department

## Part F

Select employee with second highest salary
