import mysql.connector
from mysql.connector import Error

from db_config import DB_CONFIG


def get_connection(database=None):
    config = DB_CONFIG.copy()
    if database:
        config["database"] = database
    else:
        config.pop("database", None)
    return mysql.connector.connect(**config)


def create_database():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS employee_management")
        cursor.close()
        conn.close()

        conn = get_connection(database="employee_management")
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS employees (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                department VARCHAR(100),
                position VARCHAR(100),
                salary DECIMAL(10,2),
                email VARCHAR(100),
                phone VARCHAR(20),
                doj DATE
            )
            """
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Error as err:
        print(f"Database error: {err}")
        return False


def add_employee(name, department, position, salary, email, phone, doj):
    try:
        conn = get_connection(database="employee_management")
        cursor = conn.cursor()
        query = """
            INSERT INTO employees (name, department, position, salary, email, phone, doj)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (name, department, position, salary, email, phone, doj))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Error as err:
        print(f"Error adding employee: {err}")
        return False


def get_all_employees():
    try:
        conn = get_connection(database="employee_management")
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM employees ORDER BY id")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Error as err:
        print(f"Error fetching employees: {err}")
        return []


def get_employee_by_id(employee_id):
    try:
        conn = get_connection(database="employee_management")
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM employees WHERE id = %s", (employee_id,))
        employee = cursor.fetchone()
        cursor.close()
        conn.close()
        return employee
    except Error as err:
        print(f"Error fetching employee: {err}")
        return None


def update_employee(employee_id, name, department, position, salary, email, phone, doj):
    try:
        conn = get_connection(database="employee_management")
        cursor = conn.cursor()
        query = """
            UPDATE employees
            SET name = %s,
                department = %s,
                position = %s,
                salary = %s,
                email = %s,
                phone = %s,
                doj = %s
            WHERE id = %s
        """
        cursor.execute(query, (name, department, position, salary, email, phone, doj, employee_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Error as err:
        print(f"Error updating employee: {err}")
        return False


def delete_employee(employee_id):
    try:
        conn = get_connection(database="employee_management")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employees WHERE id = %s", (employee_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Error as err:
        print(f"Error deleting employee: {err}")
        return False


def search_employee(keyword):
    try:
        conn = get_connection(database="employee_management")
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT * FROM employees
            WHERE name LIKE %s OR department LIKE %s OR position LIKE %s OR email LIKE %s OR phone LIKE %s
            ORDER BY id
        """
        search_term = f"%{keyword}%"
        cursor.execute(query, (search_term, search_term, search_term, search_term, search_term))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Error as err:
        print(f"Error searching employees: {err}")
        return []


if __name__ == "__main__":
    create_database()
    print("Database ready.")
