\# Attendify – AI-Powered Attendance Management System



Attendify is a web-based attendance management system built using Python, Flask, and MySQL. It helps manage student records, subjects, attendance, and attendance reports through a user-friendly dashboard.



It also includes a rule-based AI attendance assistant that retrieves attendance data from MySQL and answers questions using dynamic calculations.



\## Features



\- \*\*Dashboard:\*\* View student and subject statistics.

\- \*\*Student Management:\*\* Add, view, edit, and delete student records.

\- \*\*Subject Management:\*\* Manage subjects and subject codes.

\- \*\*Attendance Management:\*\* Record attendance by student, subject, and date.

\- \*\*Reports \& Analytics:\*\* Filter attendance reports and view attendance percentages.

\- \*\*AI Attendance Assistant:\*\* Ask questions about attendance, absences, leave, and target percentages.

\- \*\*Login System:\*\* Session-based access to the application.



\## Technology Stack



\- Python

\- Flask

\- MySQL

\- HTML

\- CSS

\- JavaScript

\- Chart.js

\- mysql-connector-python



\## Project Structure



```text

attendance\_app/

├── app.py

├── attendance\_agent.py

├── config.example.py

├── database.py

├── .gitignore

├── README.md

├── static/

└── templates/

```



\## Setup Instructions



\### 1. Clone the repository



```bash

git clone YOUR\_GITHUB\_REPOSITORY\_URL

cd attendance\_app

```



\### 2. Create a virtual environment



```bash

python -m venv venv

```



Activate it on Windows:



```cmd

venv\\Scripts\\activate

```



\### 3. Install dependencies



```bash

pip install Flask mysql-connector-python

```



\### 4. Configure MySQL



Create a MySQL database named `attendance\_db` and create the required tables: `users`, `students`, `subjects`, and `attendance`.



Copy the example configuration:



```cmd

copy config.example.py config.py

```



Edit `config.py` with your own local MySQL credentials.



Create an admin account in the `users` table using credentials appropriate for your local setup.



\### 5. Run the application



```bash

python app.py

```



Open `http://127.0.0.1:5000` in your browser.



\## AI Attendance Assistant



The assistant supports questions such as:



\- How is my attendance?

\- How many classes have I attended?

\- How many classes did I miss?

\- Can I miss the next class?

\- How many classes can I safely miss?

\- How many classes do I need to attend to reach 85%?



Answers are calculated using the selected student's attendance records for the selected subject.



\## Note



This is an educational project. Before production deployment, add secure password hashing, stronger session-secret management, input validation, and appropriate access controls.



\## Author



Aswathi S  

B.Tech – Artificial Intelligence and Data Science

