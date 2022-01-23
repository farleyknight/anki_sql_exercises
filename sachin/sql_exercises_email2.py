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
# Triangles
################################################################

class Triangles:
    def __init__(self):
        pd.read_sql("""
DROP TABLE IF EXISTS triangles;

CREATE TABLE triangles (
    id INT,
    a INT,
    b INT,
    c INT
);

INSERT INTO triangles
VALUES
    (1, 20, 20, 23),
    (2, 20, 20, 20),
    (3, 20, 21, 22),
    (4, 13, 14, 30);

SELECT * FROM triangles;
        """, engine)

    def expected(self):
        data = [
            (1, 'isosceles'),
            (2, 'equilateral'),
            (3, 'scalene'),
            (4, 'not a triangle')
        ]

        return pd.DataFrame(data, columns=['id', 'triangle_type'])

    def run(self):
        actual = pd.read_sql("""
SELECT
    id,
    CASE
        WHEN A+B < C THEN 'not a triangle'
        WHEN A  = B AND B  = C THEN 'equilateral'
        WHEN A  = B AND B != C THEN 'isosceles'
        WHEN A != B AND B != C THEN 'scalene'
        ELSE NULL
    END AS triangle_type
FROM triangles
        """, engine)

        test_equal(actual, self.expected())


# Write a query that checks the lengths of three sides, and determines if the triangle is isosceles, equilateral, scalene, or not a triangle.

print("*********")
print("Triangles")

Triangles().run()

################################################################
# StudentData
################################################################

class StudentData:
    def __init__(self):
        pd.read_sql("""
DROP TABLE IF EXISTS student_data;
CREATE TABLE student_data (
  id      INTEGER,
  subject varchar(10),
  marks   integer
);

INSERT INTO student_data
VALUES
    (1, 'English', 60),
    (1, 'Maths',   70),
    (1, 'Science', 75),
    (2, 'English', 62),
    (2, 'Maths',   72),
    (2, 'Science', 85);

SELECT * FROM student_data;
        """, engine)

    def expected(self):
        data = [
            (1, 70, 60, 75),
            (2, 72, 62, 85)
        ]

        return pd.DataFrame(data, columns=['id', 'maths', 'english', 'science'])
        pass

    def run(self):
        actual = pd.read_sql("""
WITH subject_scores AS (
    SELECT
        id,
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
    id,
    SUM(maths) as maths,
    SUM(english) as english,
    SUM(science) as science
FROM subject_scores
GROUP BY id
ORDER BY id
        """, engine)

        test_equal(actual, self.expected())

# Show subject scores for each student.

print("*********")
print("StudentData")

StudentData().run()


################################################################
# EmployeeDepartment
################################################################

class EmployeeDepartment:
    def __init__(self):
        pd.read_sql("""
DROP TABLE IF EXISTS projects;
CREATE TABLE projects (
    id SERIAL PRIMARY KEY
);

INSERT INTO projects
VALUES
    (1),
    (2),
    (3);

DROP TABLE IF EXISTS employee_to_projects;
CREATE TABLE employee_to_projects (
    employee_id INT,
    project_id INT
);

INSERT INTO employee_to_projects
VALUES
    (1, 1),
    (2, 2),
    (4, 3),
    (5, 2);

DROP TABLE IF EXISTS employees;
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name varchar,
    salary int,
    dept_id int
);

INSERT INTO employees
    (name, salary, dept_id)
VALUES
    ('John',   20000, 1),
    ('Ava',    10000, 5),
    ('Cailin', 30000, 2),
    ('Mike',   20000, 2),
    ('Ian',    80000, 2),
    ('John',   50000, 3);

SELECT * FROM employees;
        """, engine)

    def part_A_expected(self):
        data = [
            (1, 'John', 20000, 1),
            (2, 'Ava', 10000, 5)
        ]

        return pd.DataFrame(data, columns=['id', 'name', 'salary', 'dept_id'])

    def part_A(self):
        actual = pd.read_sql("""
SELECT * FROM employees
WHERE dept_id IN (
    SELECT
        dept_id
    FROM employees
    GROUP BY dept_id
    HAVING max(salary) <= 40000
)
        """, engine)

        test_equal(actual, self.part_A_expected())

    def part_B_expected(self):
        data = [
            (1, 'John', 20000, 1),
            (2, 'Ava', 10000, 5),
            (4, 'Mike', 20000, 2),
            (5, 'Ian', 80000, 2)
        ]

        return pd.DataFrame(data, columns=['id', 'name', 'salary', 'dept_id'])

    def part_B(self):
        actual = pd.read_sql("""
SELECT
    *
FROM employees
WHERE id IN (
    SELECT
        DISTINCT employee_id
    FROM employee_to_projects
)
        """, engine)

        test_equal(actual, self.part_B_expected())

    def part_C_expected(self):
        data = [
            (1, 'John', 20000, 1),
            (2, 'Ava', 10000, 5),
            (5, 'Ian', 80000, 2),
            (6, 'John', 50000, 3)
        ]

        return pd.DataFrame(data, columns=['id', 'name', 'salary', 'dept_id'])

    def part_C(self):
        actual = pd.read_sql("""
WITH max_salaries AS (
    SELECT
        dept_id,
        max(salary) AS max_salary
    FROM employees
    GROUP BY dept_id
)

SELECT
    id, name, salary, e.dept_id
FROM employees e
JOIN max_salaries s
ON e.dept_id = s.dept_id
AND e.salary = s.max_salary
        """, engine)

        test_equal(actual, self.part_C_expected())

    def part_D_expected(self):
        data = [
            (6, 'John', 50000, 3, 2)
        ]

        return pd.DataFrame(data, columns=['id', 'name', 'salary', 'dept_id', 'row_no'])

    def part_D(self):
        actual = pd.read_sql("""
WITH salary_rank AS (
    SELECT
        *,
        row_number() OVER (ORDER BY salary DESC) as row_no
    FROM employees
    ORDER BY salary DESC
)

SELECT
    *
FROM salary_rank
WHERE row_no = 2
        """, engine)

        test_equal(actual, self.part_D_expected())

print("*********")
print("EmployeeDepartment")

ed = EmployeeDepartment()

# Select employee from departments where max salary of the department is 40k
print("EmployeeDepartment -- Part A")
ed.part_A()

# Select all employee who are assigned to projects.
print("EmployeeDepartment -- Part B")
ed.part_B()

# Select all employees which have the max salary in a given department.
print("EmployeeDepartment -- Part C")
ed.part_C()

# Select the employee with second highest salary.
print("EmployeeDepartment -- Part D")
ed.part_D()
