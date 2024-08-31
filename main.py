from flask import Flask, request, render_template, redirect, url_for, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from config import dbconfig
import bcrypt

app = Flask(__name__)
app.secret_key = 'natruyd123_cybersimple'

# Configure MySQL
dbconfig(app)
mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('home.html')

#login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


#register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fname = request.form.get('fname', '').strip()
        lname = request.form.get('lname', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()

        # Validate form data
        if not fname or not lname or not email or not password or not confirm_password:
            flash("All fields are required.")
            return redirect(url_for('register'))

        if password != confirm_password:
            flash("Passwords do not match.")
            return redirect(url_for('register'))

        if len(password) < 8:
            flash("Password must be at least 8 characters long.")
            return redirect(url_for('register'))
       
        # Connect to the database
        cur = mysql.connection.cursor()

        # Check if the user already exists
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        
        if user:
            flash("User already exists.")
            cur.close()
            return redirect(url_for('register'))
      
        # Hash and salt the password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)


        # Insert the new user into the database
        cur.execute("INSERT INTO users (firstName, lastName, email, password) VALUES (%s, %s, %s, %s)",
                    (fname, lname, email, hashed_password))
        mysql.connection.commit()
        cur.close()

        flash("User registered successfully.")
        return redirect(url_for('login'))

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
