from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def display_data():
    conn = sqlite3.connect('FaceDataBase.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Person')
    data = cursor.fetchall()
    conn.close()
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
