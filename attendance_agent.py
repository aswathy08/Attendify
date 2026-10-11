import mysql.connector
import config


def get_db_connection():
    return mysql.connector.connect(
        host=config.MYSQL_HOST,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD,
        database=config.MYSQL_DATABASE
    )


def get_attendance(student_id, subject_id):

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            COUNT(*) AS total_classes,
            SUM(status = 'Present') AS present_classes
        FROM attendance
        WHERE student_id = %s
        AND subject_id = %s
    """

    cursor.execute(
        query,
        (student_id, subject_id)
    )

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    total_classes = result[0] or 0
    present_classes = result[1] or 0

    return total_classes, present_classes


def get_attendance_percentage(student_id, subject_id):

    total_classes, present_classes = get_attendance(
        student_id,
        subject_id
    )

    if total_classes == 0:
        return 0

    return (present_classes / total_classes) * 100


def show_attendance(student_id, subject_id):

    total_classes, present_classes = get_attendance(
        student_id,
        subject_id
    )

    if total_classes == 0:
        return "No attendance records found for this student and subject."

    percentage = (present_classes / total_classes) * 100

    return (
        f"Your current attendance is {percentage:.2f}%. "
        f"You attended {present_classes} out of "
        f"{total_classes} classes."
    )


def check_leave(student_id, subject_id):

    total_classes, present_classes = get_attendance(
        student_id,
        subject_id
    )

    if total_classes == 0:
        return "No attendance records found."

    current_percentage = (
        present_classes / total_classes
    ) * 100

    new_total = total_classes + 1

    new_percentage = (
        present_classes / new_total
    ) * 100

    response = (
        f"Your current attendance is "
        f"{current_percentage:.2f}%. "
        f"If you miss the next class, it will become "
        f"{new_percentage:.2f}%."
    )

    if new_percentage < 75:

        response += (
            " ⚠️ Your attendance would fall below "
            "75%, so you should avoid taking that leave."
        )

    else:

        response += (
            " ✅ Your attendance would remain at or "
            "above 75%."
        )

    return response


def create_recovery_plan(student_id, subject_id):

    total_classes, present_classes = get_attendance(
        student_id,
        subject_id
    )

    if total_classes == 0:
        return "No attendance records found."

    current_percentage = (
        present_classes / total_classes
    ) * 100

    if current_percentage >= 75:

        return (
            f"Your current attendance is "
            f"{current_percentage:.2f}%. "
            "Your attendance is already above 75%. "
            "No recovery plan is needed."
        )

    classes_needed = 0

    while True:

        classes_needed += 1

        new_total = (
            total_classes + classes_needed
        )

        new_present = (
            present_classes + classes_needed
        )

        new_percentage = (
            new_present / new_total
        ) * 100

        if new_percentage >= 75:
            break

    return (
        f"Your current attendance is "
        f"{current_percentage:.2f}%. "
        f"Attend the next {classes_needed} classes "
        f"without absence to reach approximately "
        f"{new_percentage:.2f}%."
    )


def classes_needed_for_target(
    student_id,
    subject_id,
    target_percentage
):

    total_classes, present_classes = get_attendance(
        student_id,
        subject_id
    )

    if total_classes == 0:
        return "No attendance records found."

    current_percentage = (
        present_classes / total_classes
    ) * 100

    if current_percentage >= target_percentage:

        return (
            f"Your current attendance is "
            f"{current_percentage:.2f}%, which is already "
            f"above your target of {target_percentage:.0f}%."
        )

    classes_needed = 0

    while True:

        classes_needed += 1

        new_total = (
            total_classes + classes_needed
        )

        new_present = (
            present_classes + classes_needed
        )

        new_percentage = (
            new_present / new_total
        ) * 100

        if new_percentage >= target_percentage:
            break

    return (
        f"Your current attendance is "
        f"{current_percentage:.2f}%. "
        f"You need to attend the next "
        f"{classes_needed} classes continuously "
        f"to reach approximately "
        f"{new_percentage:.2f}%."
    )


def process_question(
    question,
    student_id,
    subject_id
):

    command = question.lower().strip()

    # Target percentage questions
    import re

    target_match = re.search(
        r'(\d+)\s*%',
        command
    )

    if (
        "reach" in command
        or "target" in command
        or "get to" in command
    ) and target_match:

        target = int(
            target_match.group(1)
        )

        return classes_needed_for_target(
            student_id,
            subject_id,
            target
        )

    # Attendance questions
    if (
        "attendance" in command
        or "percentage" in command
        or "how am i doing" in command
    ):

        return show_attendance(
            student_id,
            subject_id
        )

    # Leave questions
    if (
        "leave" in command
        or "miss" in command
        or "absent" in command
        or "skip" in command
    ):

        return check_leave(
            student_id,
            subject_id
        )

    # Recovery questions
    if (
        "improve" in command
        or "recover" in command
        or "increase" in command
        or "below 75" in command
    ):

        return create_recovery_plan(
            student_id,
            subject_id
        )

    return (
        "I can help with attendance questions 🤖 "
        "Try asking: "
        "\"How is my attendance?\", "
        "\"Can I miss the next class?\", or "
        "\"How many classes do I need to attend "
        "to reach 85%?\""
    )