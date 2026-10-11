# 🎓 Attendify – AI-Powered Attendance Management System

Attendify is a web-based student attendance management system developed using Python, Flask, and MySQL. It provides a centralized platform to manage student records, subjects, daily attendance, and attendance reports through a user-friendly dashboard.

The project also includes an AI attendance assistant that answers natural-language questions by analyzing attendance records stored in the database.

## ✨ Features

### 📊 Dashboard
- View student and subject statistics.
- Get an overview of attendance information.

### 👩‍🎓 Student Management
- Add new students.
- View student records.
- Edit student details.
- Delete student records.

### 📚 Subject Management
- Add and manage subjects.
- Maintain subject codes and names.

### ✅ Attendance Management
- Record attendance for individual students.
- Select subjects and attendance dates.
- Mark students as Present or Absent.
- Update existing attendance records.

### 📈 Reports and Analytics
- Filter attendance reports by student, subject, and date range.
- Calculate attendance percentages.
- View present and absent counts.
- Visualize attendance statistics.

### 🤖 AI Attendance Assistant
Ask questions in natural language, such as:

- How is my attendance?
- How many classes have I attended?
- How many classes did I miss?
- Can I miss tomorrow's class?
- How many classes can I safely miss?
- How many classes do I need to attend to reach 85%?
- How can I improve my attendance?

The assistant retrieves attendance data for the selected student and subject and calculates answers dynamically.

### 🔐 Login System
- Session-based login.
- Protected application pages.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Flask | Web framework |
| MySQL | Database |
| HTML5 | Page structure |
| CSS3 | Styling and layout |
| JavaScript | Frontend interactions |
| Chart.js | Data visualization |
| mysql-connector-python | MySQL connectivity |

## 📁 Project Structure

```text
Attendify/
├── app.py
├── attendance_agent.py
├── database.py
├── config.example.py
├── requirements.txt
├── README.md
├── .gitignore
├── database/
│   └── schema.sql
├── routes/
├── static/
│   ├── css/
│   ├── images/
│   └── js/
└── templates/
```

## 🚀 Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/aswathy08/Attendify.git
cd Attendify
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```cmd
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure MySQL

Make sure MySQL Server is installed and running.

Create the database:

```sql
CREATE DATABASE attendance_db;
```

Create the required tables in `attendance_db`:

- `users`
- `students`
- `subjects`
- `attendance`

The tables must use the columns and relationships expected by the application.

### 5. Configure database credentials

Create your local configuration file by copying the example:

```cmd
copy config.example.py config.py
```

Edit `config.py` and enter your own local MySQL credentials.

**Important:** Never upload `config.py`, database passwords, or other secrets to GitHub.

### 6. Run the application

```bash
python app.py
```

Open your browser and visit:

http://127.0.0.1:5000

Log in using an account configured in your local database.

## 🧮 Attendance Calculation

The assistant calculates attendance using the selected student's records for the selected subject.

**Attendance percentage:**

Attendance (%) = (Classes Attended / Total Classes) × 100

It can also estimate the number of consecutive classes a student needs to attend to reach a specified target, assuming every upcoming class is attended.

The safe-leave and recovery calculations currently use a 75% attendance threshold.

## 🔒 Security Considerations

This project is intended for learning and demonstration.

Before production deployment:

- Hash passwords securely.
- Use a strong secret key stored in environment variables.
- Validate user input.
- Apply role-based access controls.
- Protect student information and database credentials.
- Use secure session and deployment settings.

## 🔮 Future Enhancements

- Student-specific login accounts.
- Automated attendance notifications.
- Exportable PDF and Excel reports.
- Improved natural-language understanding.
- Configurable attendance thresholds.
- More detailed analytics and visualizations.

## 👩‍💻 Author

**Aswathi S**

B.Tech – Artificial Intelligence and Data Science

## 📄 License

This project is available for educational and learning purposes. Add an explicit open-source license if you wish to permit reuse under particular terms.