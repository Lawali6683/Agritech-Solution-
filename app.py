from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MongoDB connection
try:
    client = MongoClient('mongodb+srv://username:password@cluster0.mongodb.net/myVirtualDatabase?retryWrites=true&w=majority')
    db = client['myVirtualDatabase']
    collection = db['users']
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

@app.route('/')
@app.route('/index.html')
def index():
    return render_template


('index.html')

@app.route('/login.html')
def login_page():
    return render_template('login.html')

@app.route('/dashboard.html')
def dashboard():
    return render_template('dashboard.html')

@app.route('/register', methods=['POST'])
def register():
    first_name = request.form['first-name']
    surname = request.form['surname']
    age = request.form['age']
    farmer = request.form['farmer']
    country = request.form['country']
    state = request.form['state']
    lg = request.form['lg']
    address = request.form['address']
    gender = request.form['gender']
    contact = request.form['contact']
    password = request.form['password']
    confirm_password = request.form['confirm-password']

    # Check if user exists
    if collection.find_one({"contact": contact}):
        flash("You are using this email or phone number")
        return redirect(url_for('index'))

    # Insert new user
    if password == confirm_password:
        hashed_password = generate_password_hash(password)
        user_data = {
            "first_name": first_name,
            "surname": surname,
            "age": age,
            "farmer": farmer,
            "country": country,
            "state": state,
            "lg": lg,
            "address": address,
            "gender": gender,
            "contact": contact,
            "password": hashed_password
        }
        collection.insert_one(user_data)
        return redirect(url_for('dashboard'))
    else:
        flash("Passwords do not match")
        return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    contact = request.form['contact']
    password = request.form['password']
    
    user = collection.find_one({"contact": contact})
    if user and check_password_hash(user['password'], password):
        return redirect(url_for('dashboard'))
    else:
        flash("Invalid credentials")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
