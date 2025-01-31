import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
DB_FILE = 'database.db'


def create_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS Employees")
    cursor.execute("DROP TABLE IF EXISTS Departments")

    cursor.execute('''
        CREATE TABLE Departments (
            ID INTEGER PRIMARY KEY,
            Name TEXT UNIQUE NOT NULL,
            Manager TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE Employees (
            ID INTEGER PRIMARY KEY,
            Name TEXT NOT NULL,
            Department INTEGER,
            Salary INTEGER,
            Hire_Date DATE,
            FOREIGN KEY (Department) REFERENCES Departments(ID) ON DELETE CASCADE
        )
    ''')

    cursor.execute("INSERT INTO Departments VALUES (1, 'sales', 'Alice')")
    cursor.execute("INSERT INTO Departments VALUES (2, 'engineering', 'Bob')")
    cursor.execute(
        "INSERT INTO Departments VALUES (3, 'marketing', 'Charlie')")
    cursor.execute("INSERT INTO Departments VALUES (4, 'hr', 'David')")
    cursor.execute("INSERT INTO Departments VALUES (5, 'finance', 'Eve')")

    cursor.execute(
        "INSERT INTO Employees VALUES (1, 'Alice', 1, 50000, '2021-01-15')")
    cursor.execute(
        "INSERT INTO Employees VALUES (2, 'Bob', 2, 70000, '2020-06-10')")
    cursor.execute(
        "INSERT INTO Employees VALUES (3, 'Charlie', 3, 60000, '2022-03-20')")
    cursor.execute(
        "INSERT INTO Employees VALUES (4, 'David', 4, 65000, '2019-08-25')")
    cursor.execute(
        "INSERT INTO Employees VALUES (5, 'Eve', 5, 72000, '2018-11-30')")
    cursor.execute(
        "INSERT INTO Employees VALUES (6, 'Frank', 1, 55000, '2022-05-12')")
    cursor.execute(
        "INSERT INTO Employees VALUES (7, 'Grace', 2, 73000, '2020-02-17')")

    conn.commit()
    conn.close()


@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Backend of Chat Assistant."})


@app.route('/query', methods=['POST'])
def query_database():
    user_query = request.json.get('query', '').lower()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        if "show me all employees in" in user_query:
            dept = user_query.split(" in ")[1].split(" department")[0].strip()
            cursor.execute("SELECT Employees.ID, Employees.Name, Departments.Name, Employees.Salary, Employees.Hire_Date FROM Employees JOIN Departments ON Employees.Department = Departments.ID WHERE Departments.Name = ?", (dept,))
            results = cursor.fetchall()
            response = [dict(ID=row[0], Name=row[1], Department=row[2],
                             Salary=row[3], Hire_Date=row[4]) for row in results]
            return jsonify(response if response else {"message": "No employees found in this department."})

        elif "who is the manager of" in user_query:
            dept = user_query.split(" of ")[1].split(" department")[0].strip()
            cursor.execute(
                "SELECT Manager FROM Departments WHERE Name = ?", (dept,))
            result = cursor.fetchone()
            return jsonify({"Manager": result[0]} if result else {"message": "Department not found."})

        elif "list all employees hired after" in user_query:
            date = user_query.split(" after ")[1].strip()
            cursor.execute(
                "SELECT * FROM Employees WHERE Hire_Date > ?", (date,))
            results = cursor.fetchall()
            response = [dict(ID=row[0], Name=row[1], Department=row[2],
                             Salary=row[3], Hire_Date=row[4]) for row in results]
            return jsonify(response if response else {"message": "No employees found hired after this date."})

        elif "what is the total salary expense for" in user_query:
            dept = user_query.split(" for ")[1].split(" department")[0].strip()
            cursor.execute(
                "SELECT SUM(Employees.Salary) FROM Employees JOIN Departments ON Employees.Department = Departments.ID WHERE Departments.Name = ?", (dept,))
            result = cursor.fetchone()
            return jsonify({"Total Salary Expense": result[0]} if result and result[0] else {"message": "Department not found or no employees."})

        else:
            return jsonify({"message": "Unsupported query. Please try again."})

    except Exception as e:
        return jsonify({"error": str(e)})

    finally:
        conn.close()


if __name__ == '__main__':
    create_database()
    app.run(host='0.0.0.0', port=3000, debug=True)
