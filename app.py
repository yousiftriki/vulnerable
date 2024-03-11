from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# SQLite database initialization
conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
             (username TEXT NOT NULL, password TEXT NOT NULL)''')
c.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin')")
conn.commit()
conn.close()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_check():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Vulnerable SQL query susceptible to SQL injection
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    c.execute(query)
    user = c.fetchone()
    conn.close()

    if user:
        return f"Welcome, {username}!"
    else:
        return "Invalid username or password."

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        # Check if username already exists
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = c.fetchone()

        if existing_user:
            return "Username already exists. Please choose a different username."
        else:
            # Insert new user into the database
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))  # Redirect to the login page after successful registration

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
