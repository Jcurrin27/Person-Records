from faker import Faker
import random
import sqlite3
import csv

from datetime import datetime, timedelta
from helpers import Employee, Student #, get_student, get_employee, get_university

fake = Faker()

def main():
    num_people = get_university()

    conn = sqlite3.connect('clearinghouse.db')
    cursor = conn.cursor()

    # create student table
    for i in range(int(num_people*.7)):
        student = get_student()
        cursor.execute('INSERT INTO students (name, address, personal_email, personal_phone, prgm_start_date, student_status) VALUES (?,?,?,?,?,?)', (student.name, student.address, student.personal_email, student.personal_phone, student.prgm_start_date, student.student_status))
        conn.commit()

    # create employee table
    for i in range(int(num_people*.3)):
        employee = get_employee()
        cursor.execute('INSERT INTO employees (name, address, personal_email, personal_phone, hire_date, termination_date) VALUES (?,?,?,?,?,?)', (employee.name, employee.address, employee.personal_email, employee.personal_phone, employee.hire_date, employee.termination_date))
        conn.commit()

    # copy a few people from the employee table to the student table to make things more challenging/realistic for the steps below.
    student_employees = int((num_people * .1))

    cursor.execute("""INSERT INTO students
    SELECT (SELECT NULL) AS student_id, e.name, e.address, e.personal_email, e.personal_phone, (SELECT NULL) AS prgm_start_date, (SELECT NULL) AS student_status
    FROM employees e
    LIMIT ?;""", (student_employees,)  )

    for i in range(student_employees):
        prgm_start_date = fake.date_between()
        three_years_ago = datetime.date(datetime.now() - timedelta(days=3*365))
        if prgm_start_date >= three_years_ago:
            student_status = 'Active'
        else:
            student_status = 'Inactive'
        cursor.execute('UPDATE students SET prgm_start_date = ?, student_status = ? WHERE prgm_start_date IS NULL LIMIT 1', (prgm_start_date, student_status))

    # create and export student csv
    csvWriter = csv.writer(open("students.csv", "w"))
    csvWriter.writerow(['name', 'address', 'personal_email', 'personal_phone', 'prgm_start_date', 'student_status'])
    for row in cursor.execute('SELECT * FROM students'):
        csvWriter.writerow(row)

    # create and export employee csv
    csvWriter = csv.writer(open("employees.csv", "w"))
    csvWriter.writerow(['name', 'address', 'personal_email', 'personal_phone', 'hire_date', 'termination_date'])
    for row in cursor.execute('SELECT * FROM employees'):
        csvWriter.writerow(row)

    # insert all employee records into person_final
    cursor.execute("""INSERT INTO person_final
                   SELECT (SELECT NULL) AS person_id,
                   (SELECT NULL) AS student_id,
                    e.employee_id,
                   e.name,
                   e.address,
                   e.personal_email,
                   e.personal_phone,
                   (SELECT NULL) AS prgm_start_date,
                   (SELECT NULL) AS student_status,
                   e.hire_date,
                   e.termination_date,
                   replace(e.name || '@u.edu', ' ','') AS employee_email,
                   (SELECT NULL) AS student_email
                   FROM employees e;""")

    # update all records in person_final that EXIST in students table
    cursor.execute("""
    UPDATE person_final

    SET prgm_start_date = (
            SELECT s.prgm_start_date
            FROM students s
            WHERE person_final.name = s.name
        ),
        student_status = (
            SELECT s.student_status
            FROM students s
            WHERE person_final.name = s.name
        ),
        student_id = (
            SELECT s.student_id
            FROM students s
            WHERE person_final.name = s.name
        ),
        student_email = (
            SELECT replace(s.name || '@my.u.edu',' ','')
            FROM students s
            WHERE person_final.name = s.name
        )
    WHERE EXISTS (
        SELECT 1
        FROM students s
        WHERE person_final.name = s.name
    );
    """)

    # insert all student records into person_final that NOT EXIST in person_final
    cursor.execute("""INSERT INTO person_final
                   SELECT (SELECT NULL) AS person_id,
                   s.student_id AS student_id,
                    (SELECT NULL) AS employee_id,
                   s.name,
                   s.address,
                   s.personal_email,
                   s.personal_phone,
                   s.prgm_start_date,
                   s.student_status AS student_status,
                   (SELECT NULL) AS hire_date,
                   (SELECT NULL) AS termination_date,
                   (SELECT NULL)  AS employee_email,
                   replace(s.name || '@my.u.edu', ' ','') AS student_email
                   FROM students s;""")

    # create and export person_final csv
    csvWriter = csv.writer(open("person_final.csv", "w"))
    csvWriter.writerow(['person_id', 'student_id', 'employee_id', 'name', 'address', 'personal_email', 'personal_phone', 'prgm_start_date', 'student_status', 'hire_date', 'termination_date', 'employee_email', 'student_email'])
    for row in cursor.execute('SELECT * FROM person_final'):
        csvWriter.writerow(row)

    cursor.execute('DELETE from employees')
    cursor.execute('DELETE from students')
    cursor.execute('DELETE from person_final')
    conn.commit()

def get_university(user_input=None):
    while True:
        if user_input is None:
            user_input = input("really small or small size university?: ").strip().lower()
        else:
            user_input = user_input.strip().lower()

        if user_input == 'really small':
            return 100
        elif user_input == 'small':
            return 6000
        else:
            print("Invalid input. Please enter either 'really small' or 'small'.")
            if user_input is not None:
                return None
            user_input = None

def get_employee(fake_instance=fake, random_value=None):
    name = fake_instance.name()
    address = fake_instance.address().replace("\n"," ")
    personal_email = fake_instance.email()
    personal_phone = fake_instance.phone_number()
    hire_date = fake_instance.date_between()

    if random_value is None:
        random_value = random.random()

    if random.random() < 0.2:
        termination_date = None
    else:
        termination_date = fake_instance.date_between(start_date = hire_date)

    return Employee(name, address, personal_email, personal_phone, hire_date, termination_date)

def get_student(fake_instance=fake, custom_date=None):
    name = fake_instance.name()
    address = fake_instance.address().replace("\n"," ")
    personal_email = fake_instance.email()
    personal_phone = fake_instance.phone_number()
    if custom_date is None:
        prgm_start_date = fake_instance.date_between()
    else:
        prgm_start_date = custom_date
        
    three_years_ago = datetime.date(datetime.now() - timedelta(days=3*365))
    if prgm_start_date >= three_years_ago:
        student_status = 'Active'
    else:
        student_status = 'Inactive'

    return Student(name, address, personal_email, personal_phone, prgm_start_date, student_status)

if __name__ == "__main__":
    main()


