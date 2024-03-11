from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__, template_folder='/Users/yousiftriki/project_directory/templates')

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
    query = f"SELECT * FROM users WHERE username=? AND password=?"
    c.execute(query, (username, password))
    user = c.fetchone()
    conn.close()

    if user:
        # Redirect to the comment page upon successful login
        return redirect(url_for('comment'))
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

@app.route('/comment')
def comment():
    return render_template('comment.html')

@app.route('/post_comment', methods=['POST'])
def post_comment():
    if request.method == 'POST':
        comment = request.form.get('comment')
        # Process and store the comment in the database or perform other actions as needed
        return redirect(url_for('comment'))  # Redirect back to the comment page
    else:
        return render_template('comment.html')

if __name__ == '__main__':
    app.run(debug=True)
