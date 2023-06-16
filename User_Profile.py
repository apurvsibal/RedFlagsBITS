# User Profile 


from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

DATABASE = 'user_profiles.db'

def create_database():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 fullname TEXT,
                 gender TEXT,
                 age INTEGER,
                 dob TEXT,
                 contactdetails TEXT,
                 emergencycontact TEXT
                 )''')
    c.execute('''CREATE TABLE IF NOT EXISTS medical_records (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 user_id INTEGER,
                 date TEXT,
                 medical_history TEXT,
                 FOREIGN KEY (user_id) REFERENCES users (id)
                 )''')
    conn.commit()
    conn.close()

@app.route('/create_profile', methods=['GET', 'POST'])
def create_profile():
    if request.method == 'POST':
        fullname = request.form['fullname']
        gender = request.form['gender']
        age = request.form['age']
        dob = request.form['dob']
        contactdetails = request.form['contactdetails']
        emergencycontact = request.form['emergencycontact']

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''INSERT INTO users (
                     fullname, gender, age, dob, contactdetails, emergencycontact
                     ) VALUES (?, ?, ?, ?, ?, ?)''',
                  (fullname, gender, age, dob, contactdetails, emergencycontact))
        user_id = c.lastrowid
        conn.commit()
        conn.close()

        return redirect('/profile/{}'.format(user_id))

    return render_template('create_profile.html')

@app.route('/profile/<int:user_id>', methods=['GET', 'POST'])
def view_profile(user_id):
    if request.method == 'POST':
        medical_history = request.form['medical_history']
        current_date = datetime.now().strftime('%Y-%m-%d')

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''INSERT INTO medical_records (
                     user_id, date, medical_history
                     ) VALUES (?, ?, ?)''',
                  (user_id, current_date, medical_history))
        conn.commit()
        conn.close()

        return redirect('/profile/{}'.format(user_id))

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    c.execute('SELECT * FROM medical_records WHERE user_id = ?', (user_id,))
    medical_records = c.fetchall()
    conn.close()

    return render_template('view_profile.html', user=user, medical_records=medical_records)

@app.route('/update_profile/<int:user_id>', methods=['GET', 'POST'])
def update_profile(user_id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        gender = request.form['gender']
        age = request.form['age']
        dob = request.form['dob']
        contactdetails = request.form['contactdetails']
        emergencycontact = request.form['emergencycontact']

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''UPDATE users SET
                     fullname = ?,
                     gender = ?,
                     age = ?,
                     dob = ?,
                     contactdetails = ?,
                     emergencycontact = ?
                     WHERE id = ?''',
                  (fullname, gender, age, dob, contactdetails, emergencycontact, user_id))
        conn.commit()
        conn.close()

        return redirect('/profile/{}'.format(user_id))

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    conn.close()

    return render_template('update_profile.html', user=user)

if __name__ == '__main__':
    create_database()
    app.run(debug=True)
