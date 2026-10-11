import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="aswathy__08__",
    database="attendance_db"
)

print("MySQL connected successfully!")

connection.close()