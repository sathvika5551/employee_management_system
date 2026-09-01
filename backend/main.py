from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector

app = FastAPI()


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sathvika@2005",
        database="employee_management"
    )


# =========================================================
# EMPLOYEE MODEL
# =========================================================

class Employee(BaseModel):
    name: str
    email: str
    phone: str
    department: str
    designation: str
    salary: float
    joining_date: str


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():
    return {"message": "Employee Management API is running"}


# =========================================================
# GET EMPLOYEES
# =========================================================

@app.get("/employees")
def get_employees():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM employees")

    employees = cursor.fetchall()

    cursor.close()
    conn.close()

    return employees


# =========================================================
# ADD EMPLOYEE
# =========================================================

@app.post("/employees")
def add_employee(employee: Employee):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO employees
    (name, email, phone, department, designation, salary, joining_date)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        employee.name,
        employee.email,
        employee.phone,
        employee.department,
        employee.designation,
        employee.salary,
        employee.joining_date
    )

    try:

        cursor.execute(query, values)
        conn.commit()

    except mysql.connector.Error as e:

        conn.rollback()

        if e.errno == 1062:
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:

        cursor.close()
        conn.close()

    return {"message": "Employee added successfully"}


# =========================================================
# UPDATE EMPLOYEE
# =========================================================

@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, employee: Employee):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE employees
    SET
        name=%s,
        email=%s,
        phone=%s,
        department=%s,
        designation=%s,
        salary=%s,
        joining_date=%s
    WHERE id=%s
    """

    values = (
        employee.name,
        employee.email,
        employee.phone,
        employee.department,
        employee.designation,
        employee.salary,
        employee.joining_date,
        employee_id
    )

    try:

        cursor.execute(query, values)

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Employee not found"
            )

        conn.commit()

    except mysql.connector.Error as e:

        conn.rollback()

        if e.errno == 1062:
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:

        cursor.close()
        conn.close()

    return {"message": "Employee updated successfully"}


# =========================================================
# DELETE EMPLOYEE
# =========================================================

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    query = "DELETE FROM employees WHERE id=%s"

    try:

        cursor.execute(query, (employee_id,))

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Employee not found"
            )

        conn.commit()

    finally:

        cursor.close()
        conn.close()

    return {"message": "Employee deleted successfully"}