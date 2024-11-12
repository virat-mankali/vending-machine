from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
vending_db = client['vending']
users = vending_db['users']

# Root route for signup
@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data
        first_name = request.form['firstname']
        second_name = request.form['secondname']
        email = request.form['email']
        password = request.form['password']

        # Check if user already exists
        existing_user = users.find_one({'email': email})
        if existing_user:
            flash('Email already registered. Please log in.', 'danger')
            return redirect(url_for('login'))

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Insert new user into MongoDB
        users.insert_one({
            'full name': first_name + " " + second_name,
            'email': email,
            'password': hashed_password
        })

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Fetch user from MongoDB
        user = users.find_one({'email': email})

        # Check user and password
        if user and check_password_hash(user['password'], password):
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Check your email and password.', 'danger')

    return render_template('login.html')

# Home route after login
@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True, port=5432)
