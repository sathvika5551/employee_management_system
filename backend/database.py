import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sathvika@5551",
    database="employee_management"
)

print("Database connected successfully")