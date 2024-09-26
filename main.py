from flask import Flask, request, render_template, redirect, session, url_for, flash
from flask_mysqldb import MySQL
from db.config import dbconfig

app = Flask(__name__)
app.secret_key = 'natruyd123_pysimple'

# Configure MySQL
dbconfig(app)
mysql = MySQL(app)


# Home Route
@app.route('/home')
def home():
    if 'email' not in session:  
        flash("You need to log in first.", 'warning')
        return redirect(url_for('login'))  
    
    email = session.get('email') 
    return render_template('home.html', email=email)


# Login Route
@app.route('/', methods=['GET', 'POST'])
def login():
    if 'email' in session: 
        flash("You are already logged in.", 'info')
        return redirect(url_for('home')) 
    
    if request.method == 'POST':
        email = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not email or not password:
            flash("Email and password are required.", 'danger')
            return redirect(url_for('login'))

        # Fetch the user's password from the database
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()

        if user and user[0] == password:  
            session['email'] = email
            # flash("Login successful!", 'success')
            return redirect(url_for('home'))
        else:
            flash("Invalid email or password.", 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')


# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'email' in session: 
        flash("You are already registered in if you want to register again please log out your account first.", 'info')
        return redirect(url_for('home')) 
    
    if request.method == 'POST':
        fname = request.form.get('fname', '').strip()
        lname = request.form.get('lname', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()

        # Validate form data
        if not fname or not lname or not email or not password or not confirm_password:
            flash("All fields are required.", 'danger')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash("Passwords do not match.", 'danger')
            return redirect(url_for('register'))

        if len(password) < 8:
            flash("Password must be at least 8 characters long.", 'danger')
            return redirect(url_for('register'))

        # Connect to the database
        cur = mysql.connection.cursor()

        # Check if the user already exists
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        
        if user:
            flash("User already exists.", 'danger')
            cur.close()
            return redirect(url_for('register'))
        
        
        # Insert the new user into the database
        cur.execute("INSERT INTO users (firstName, lastName, email, password) VALUES (%s, %s, %s, %s)",
                    (fname, lname, email, password))
        mysql.connection.commit()
        cur.close()
        
        session['email'] = email
        # flash("User registered successfully.")
        return redirect(url_for('home'))

    return render_template('register.html')

# Logout Route 
@app.route('/logout')
def logout():
    session.pop('email', None) 
    # flash("You have been logged out.", 'info')  
    return redirect(url_for('login'))  

if __name__ == '__main__':
    app.run(debug=True)
