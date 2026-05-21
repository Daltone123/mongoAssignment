from flask import Flask, render_template, request, url_for, redirect, session
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
app.secret_key = "testing"

# Connecting Cloud MongoDB Atlas database
def MongoDB():
    connection_string = "mongodb+srv://daltoneotieno123_db_user:fgX2yMG7SptZvho9@daltone123.jvrkgs9.mongodb.net/?retryWrites=true&w=majority"

    
    client = MongoClient(connection_string)
    db = client.get_database('total_records')
    records = db.register
    return records

# Initializing the cloud database connection
records = MongoDB()

# URLs for routes 
@app.route("/", methods=['POST', 'GET'])
def index():
    message = ''
    if "email" in session:
        return redirect(url_for("logged_in"))
        
    if request.method == "POST":
        user = request.form.get("fullname")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        
        user_found = records.find_one({"name": user})
        email_found = records.find_one({"email": email})
        
        if user_found:
            message = 'There already is a user by that name'
            return render_template('index.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('index.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('index.html', message=message)
        else:
            # Hash the password and encode it
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            user_input = {'name': user, 'email': email, 'password': hashed}
            records.insert_one(user_input)
            
            # Start session for the newly registered user
            session["email"] = email
            return redirect(url_for('logged_in'))
            
    return render_template('index.html')

@app.route("/login", methods=["POST", "GET"])
def login():
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("logged_in"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        email_found = records.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect(url_for('logged_in'))
            else:
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login.html', message=message)
            
    return render_template('login.html', message=message)

@app.route('/logged_in')
def logged_in():
    if "email" in session:
        email = session["email"]
        return render_template('logged_in.html', email=email)
    else:
        return redirect(url_for("login"))

@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return render_template("signout.html")
    else:
        return redirect(url_for("index"))

if __name__ == "__main__":
    # Removed host='0.0.0.0' so it runs seamlessly on Windows localhost
    app.run(debug=True, port=5000)
