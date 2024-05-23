import pytest
from project import get_university, get_employee, get_student
from helpers import Employee, Student
from faker import Faker
from datetime import datetime, timedelta

def test_get_university():
    assert get_university("small") == 6000
    assert get_university("really small") == 100
    assert get_university("booger") is None

def test_get_employee():
    fake = Faker()

    employee = get_employee(fake_instance=fake, random_value=0.1)
    assert isinstance(employee, Employee)

def test_get_student():
    fake = Faker()
    three_years_ago = datetime.date(datetime.now()) - timedelta(days=3*365)

    custom_date = datetime.date(datetime.now())
    student = get_student(fake_instance=fake, custom_date = custom_date)
    assert isinstance(student, Student)
    assert student.student_status == 'Active'

