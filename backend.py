from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/api/students')
def get_students():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Students")
    students = cursor.fetchall()
    conn.close()
    return jsonify(students)

if __name__ == '__main__':
    app.run(debug=True)
