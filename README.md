# Person Records
#### Video Demo:  https://youtu.be/1o1gsk9R8BM
#### Introduction:
This program asks the user to indicate whether they would like to simulate a 'very small' (111 people) university, or a 'small' (6000 people) university. Based on the user's response, the program creates fake person data and exports three csv files representing the database tables they are named after: students.csv, employees.csv, and person_final.csv. This demonstrates raw student and employee data and how they may be merged together in a final person record table to create a single record for each person affiliated with the unviersity. This final record can be shared with active directory systems to guide permissions for each user.

#### Randomized Data:
Much of the work put into this program is dedicated to the process of creating a randomized dataset to simulate the feel of real, raw person data being pulled into a database from different systems, mainly HCM, ERP, and CRM systems used to house employee and student data. Specifically, there are two tables being populated by the randomized data, students and employees. Each of these tables pull in the same data except for three fields that are specific to either employees or students. Employees recieve randomized 'hire_date', 'termination_date', and 'employee_id' data, while students receive randomized 'prgm_start_date', 'student_status', and 'student_id'. Both tables contain randomized common biographical data like name, address, email, etc.

#### Merging Person Records:
Again, this program demostrates, on a small scale, merging raw student and employee data into a single record. A big challenge is identifying people who are both student AND employees and correctly loading them into the person_final table as a single record. This program looks at only the 'name' field between both tables to identify matches. This is a very simplistic matching mechanism that would not translate to enterprise operations. However, the matching mechanism could be swapped for other data or combinations of data more suitable to matching.

Csv files are generated to verify the program is correctly merging person records. You can download all three files and compare records in each to identify whether records found in both the student and employee table are correctly merged with both student and employee data in the person_final file.

