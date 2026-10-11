from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import config
from attendance_agent import process_question

app = Flask(__name__)

# Secret key for Flask sessions
app.secret_key = "attendify-secret-key"


# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------

def get_db_connection():
    return mysql.connector.connect(
        host=config.MYSQL_HOST,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD,
        database=config.MYSQL_DATABASE
    )


# --------------------------------------------------
# LOGIN
# --------------------------------------------------

@app.route('/')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_user():

    username = request.form.get('username')
    password = request.form.get('password')

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username = %s
        AND password = %s
        """,
        (username, password)
    )

    user = cursor.fetchone()

    cursor.close()
    db.close()

    if user:

        session['user_id'] = user['user_id']
        session['username'] = user['username']
        session['role'] = user['role']

        return redirect(url_for('dashboard'))

    return "Invalid username or password"


# --------------------------------------------------
# LOGOUT
# --------------------------------------------------

@app.route('/logout')
def logout():

    session.clear()

    return redirect(url_for('login'))


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db_connection()
    cursor = db.cursor()

    # Total students
    cursor.execute("""
        SELECT COUNT(*)
        FROM students
    """)

    total_students = cursor.fetchone()[0]

    # Total subjects
    cursor.execute("""
        SELECT COUNT(*)
        FROM subjects
    """)

    total_subjects = cursor.fetchone()[0]

    # Today's attendance
    cursor.execute("""
        SELECT
            COUNT(*) AS total,
            SUM(
                CASE
                    WHEN status = 'Present'
                    THEN 1
                    ELSE 0
                END
            ) AS present
        FROM attendance
        WHERE attendance_date = CURDATE()
    """)

    attendance_data = cursor.fetchone()

    total_attendance = attendance_data[0]
    present_count = attendance_data[1] or 0

    if total_attendance > 0:

        today_attendance = round(
            (present_count / total_attendance) * 100
        )

    else:

        today_attendance = 0

    # Classes today
    cursor.execute("""
        SELECT COUNT(DISTINCT subject_id)
        FROM attendance
        WHERE attendance_date = CURDATE()
    """)

    classes_today = cursor.fetchone()[0]

    cursor.close()
    db.close()

    return render_template(
        'dashboard.html',
        total_students=total_students,
        total_subjects=total_subjects,
        today_attendance=today_attendance,
        classes_today=classes_today
    )


# --------------------------------------------------
# STUDENTS
# --------------------------------------------------

@app.route('/students')
def students():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            student_id,
            roll_no,
            name,
            email,
            department,
            year
        FROM students
        ORDER BY student_id DESC
    """)

    students = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        'students.html',
        students=students
    )


# --------------------------------------------------
# ADD STUDENT
# --------------------------------------------------

@app.route('/students/add', methods=['POST'])
def add_student():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    roll_no = request.form['roll_no']
    name = request.form['name']
    email = request.form['email']
    department = request.form['department']
    year = request.form['year']

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO students
        (roll_no, name, email, department, year)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        roll_no,
        name,
        email,
        department,
        year
    ))

    db.commit()

    cursor.close()
    db.close()

    return redirect(url_for('students'))


# --------------------------------------------------
# DELETE STUDENT
# --------------------------------------------------

@app.route('/students/delete/<int:student_id>')
def delete_student(student_id):

    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute(
        """
        DELETE FROM students
        WHERE student_id = %s
        """,
        (student_id,)
    )

    db.commit()

    cursor.close()
    db.close()

    return redirect(url_for('students'))


# --------------------------------------------------
# EDIT STUDENT
# --------------------------------------------------

@app.route('/students/edit/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):

    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':

        roll_no = request.form['roll_no']
        name = request.form['name']
        email = request.form['email']
        department = request.form['department']
        year = request.form['year']

        cursor.execute("""
            UPDATE students
            SET
                roll_no = %s,
                name = %s,
                email = %s,
                department = %s,
                year = %s
            WHERE student_id = %s
        """, (
            roll_no,
            name,
            email,
            department,
            year,
            student_id
        ))

        db.commit()

        cursor.close()
        db.close()

        return redirect(url_for('students'))

    cursor.execute(
        """
        SELECT *
        FROM students
        WHERE student_id = %s
        """,
        (student_id,)
    )

    student = cursor.fetchone()

    cursor.close()
    db.close()

    return render_template(
        'edit_student.html',
        student=student
    )


# --------------------------------------------------
# SUBJECTS
# --------------------------------------------------

@app.route('/subjects')
def subjects():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            subject_id,
            subject_code,
            subject_name
        FROM subjects
        ORDER BY subject_id DESC
    """)

    subjects = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        'subjects.html',
        subjects=subjects
    )


# --------------------------------------------------
# ADD SUBJECT
# --------------------------------------------------

@app.route('/subjects/add', methods=['POST'])
def add_subject():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    subject_code = request.form['subject_code']
    subject_name = request.form['subject_name']

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO subjects
        (subject_code, subject_name)
        VALUES (%s, %s)
    """, (
        subject_code,
        subject_name
    ))

    db.commit()

    cursor.close()
    db.close()

    return redirect(url_for('subjects'))


# --------------------------------------------------
# DELETE SUBJECT
# --------------------------------------------------

@app.route('/subjects/delete/<int:subject_id>')
def delete_subject(subject_id):

    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute(
        """
        DELETE FROM subjects
        WHERE subject_id = %s
        """,
        (subject_id,)
    )

    db.commit()

    cursor.close()
    db.close()

    return redirect(url_for('subjects'))


# --------------------------------------------------
# EDIT SUBJECT
# --------------------------------------------------

@app.route('/subjects/edit/<int:subject_id>', methods=['GET', 'POST'])
def edit_subject(subject_id):

    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':

        subject_code = request.form['subject_code']
        subject_name = request.form['subject_name']

        cursor.execute("""
            UPDATE subjects
            SET
                subject_code = %s,
                subject_name = %s
            WHERE subject_id = %s
        """, (
            subject_code,
            subject_name,
            subject_id
        ))

        db.commit()

        cursor.close()
        db.close()

        return redirect(url_for('subjects'))

    cursor.execute(
        """
        SELECT *
        FROM subjects
        WHERE subject_id = %s
        """,
        (subject_id,)
    )

    subject = cursor.fetchone()

    cursor.close()
    db.close()

    return render_template(
        'edit_subject.html',
        subject=subject
    )


# --------------------------------------------------
# ATTENDANCE
# --------------------------------------------------

@app.route('/attendance')
def attendance():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            subject_id,
            subject_code,
            subject_name
        FROM subjects
        ORDER BY subject_name
    """)

    subjects = cursor.fetchall()

    cursor.execute("""
        SELECT
            student_id,
            roll_no,
            name
        FROM students
        ORDER BY roll_no
    """)

    students = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        'attendance.html',
        subjects=subjects,
        students=students
    )


# --------------------------------------------------
# SAVE ATTENDANCE
# --------------------------------------------------

@app.route('/attendance/save', methods=['POST'])
def save_attendance():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    attendance_date = request.form['attendance_date']
    subject_id = request.form['subject_id']

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        SELECT student_id
        FROM students
    """)

    students = cursor.fetchall()

    for student in students:

        student_id = student[0]

        status = request.form.get(
            f'status_{student_id}'
        )

        if status:

            cursor.execute("""
                INSERT INTO attendance
                (
                    student_id,
                    subject_id,
                    attendance_date,
                    status
                )
                VALUES (%s, %s, %s, %s)

                ON DUPLICATE KEY UPDATE
                    status = VALUES(status)
            """, (
                student_id,
                subject_id,
                attendance_date,
                status
            ))

    db.commit()

    cursor.close()
    db.close()

    return redirect(url_for('attendance'))


# --------------------------------------------------
# REPORTS
# --------------------------------------------------

@app.route('/reports')
def reports():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    student_id = request.args.get('student_id')
    subject_id = request.args.get('subject_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Students for filter
    cursor.execute("""
        SELECT
            student_id,
            roll_no,
            name
        FROM students
        ORDER BY roll_no
    """)

    students = cursor.fetchall()

    # Subjects for filter
    cursor.execute("""
        SELECT
            subject_id,
            subject_code,
            subject_name
        FROM subjects
        ORDER BY subject_name
    """)

    subjects = cursor.fetchall()

    # Main report query
    query = """
        SELECT

            s.student_id,
            s.roll_no,
            s.name,

            sub.subject_id,
            sub.subject_code,
            sub.subject_name,

            COUNT(a.attendance_id) AS total_classes,

            SUM(
                CASE
                    WHEN a.status = 'Present'
                    THEN 1
                    ELSE 0
                END
            ) AS present_count,

            SUM(
                CASE
                    WHEN a.status = 'Absent'
                    THEN 1
                    ELSE 0
                END
            ) AS absent_count

        FROM attendance a

        JOIN students s
            ON a.student_id = s.student_id

        JOIN subjects sub
            ON a.subject_id = sub.subject_id

        WHERE 1 = 1
    """

    params = []

    # Student filter
    if student_id:

        query += """
            AND s.student_id = %s
        """

        params.append(student_id)

    # Subject filter
    if subject_id:

        query += """
            AND sub.subject_id = %s
        """

        params.append(subject_id)

    # Start date
    if start_date:

        query += """
            AND a.attendance_date >= %s
        """

        params.append(start_date)

    # End date
    if end_date:

        query += """
            AND a.attendance_date <= %s
        """

        params.append(end_date)

    query += """

        GROUP BY

            s.student_id,
            s.roll_no,
            s.name,

            sub.subject_id,
            sub.subject_code,
            sub.subject_name

        ORDER BY

            s.roll_no,
            sub.subject_code
    """

    cursor.execute(
        query,
        params
    )

    reports = cursor.fetchall()

    # Attendance percentage
    for row in reports:

        total = row['total_classes']
        present = row['present_count'] or 0

        if total:

            row['percentage'] = round(
                (present / total) * 100,
                2
            )

        else:

            row['percentage'] = 0

    # Overall statistics
    total_classes = sum(
        row['total_classes'] or 0
        for row in reports
    )

    total_present = sum(
        row['present_count'] or 0
        for row in reports
    )

    total_absent = sum(
        row['absent_count'] or 0
        for row in reports
    )

    if total_classes:

        overall_percentage = round(
            (total_present / total_classes) * 100,
            2
        )

    else:

        overall_percentage = 0

    cursor.close()
    db.close()

    return render_template(
        'reports.html',

        reports=reports,

        students=students,
        subjects=subjects,

        selected_student=student_id,
        selected_subject=subject_id,

        start_date=start_date,
        end_date=end_date,

        total_classes=total_classes,
        total_present=total_present,
        total_absent=total_absent,

        overall_percentage=overall_percentage
    )


# --------------------------------------------------
# AI ATTENDANCE ASSISTANT
# --------------------------------------------------

@app.route('/chatbot')
def chatbot():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Get students for chatbot selection
    cursor.execute("""
        SELECT
            student_id,
            roll_no,
            name
        FROM students
        ORDER BY roll_no
    """)

    students = cursor.fetchall()

    # Get subjects for chatbot selection
    cursor.execute("""
        SELECT
            subject_id,
            subject_code,
            subject_name
        FROM subjects
        ORDER BY subject_name
    """)

    subjects = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        'chatbot.html',
        students=students,
        subjects=subjects
    )


@app.route('/chatbot/ask', methods=['POST'])
def chatbot_ask():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    question = request.form.get('question', '').strip()

    student_id = request.form.get('student_id')
    subject_id = request.form.get('subject_id')

    if not question:
        return redirect(url_for('chatbot'))

    if not student_id or not subject_id:

        return render_template(
            'chatbot.html',
            students=[],
            subjects=[],
            error="Please select a student and subject."
        )

    answer = process_question(
        question,
        int(student_id),
        int(subject_id)
    )

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            student_id,
            roll_no,
            name
        FROM students
        ORDER BY roll_no
    """)

    students = cursor.fetchall()

    cursor.execute("""
        SELECT
            subject_id,
            subject_code,
            subject_name
        FROM subjects
        ORDER BY subject_name
    """)

    subjects = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        'chatbot.html',
        students=students,
        subjects=subjects,
        question=question,
        answer=answer,
        selected_student=student_id,
        selected_subject=subject_id
    )
# --------------------------------------------------
# RUN APPLICATION
# --------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)