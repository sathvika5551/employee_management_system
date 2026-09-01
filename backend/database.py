import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sathvika@2005",
    database="employee_management"
)

print("Database connected successfully")