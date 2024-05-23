from faker import Faker
import random
import sqlite3
from datetime import datetime, timedelta

# could possibly improve by creating a Person class and students and employees a subset of the Person class #
fake = Faker()

class Employee:
    def __init__(self, name, address, personal_email, personal_phone, hire_date, termination_date):
        self.name = name
        self.address = address
        self.personal_email = personal_email
        self.personal_phone = personal_phone
        self.hire_date = hire_date
        self.termination_date = termination_date

class Student:
    def __init__(self, name, address, personal_email, personal_phone, prgm_start_date, student_status):
        self.name = name
        self.address = address
        self.personal_email = personal_email
        self.personal_phone = personal_phone
        self.prgm_start_date = prgm_start_date
        self.student_status = student_status





