from flask import Flask, redirect, request, render_template, session, flash

from mysqlconnections import MySQLConnector #imports the msql connection and connector
import re
# # the "re" module will let us perform some regular expression operations

app = Flask(__name__)
app.secret_key='secret'

mysql = MySQLConnector(app, 'registration')
# # create a regular expression object that we can use run operations on
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def index():

    return render_template("index.html")

@app.route('/success',  methods=["POST"])
def success():
    errors = [] #declared the variable here to throw error if condition is not met.
    data = {
        "first_name": request.form["firstname"],
        "last_name": request.form["lastname"],
        "email": request.form["email"],
        "password": request.form["password"],
        "passwordconf": request.form["confirmation"]
        }

    if len(data['first_name']) < 1 or len(data['last_name']) <2:
        errors.append('Invalid name length') #this makes it conditional that first name has to be > than 2

        # flash(errors) # storing into flash what happened in the if statment.

        # return redirect('/')

    if len(data['email']) == 0:
        errors.append('Email cannot be blank')
        # flash(errors)
        # return redirect('/')

    if not EMAIL_REGEX.match(data['email']):
        errors.append('Must be in valid email format')
        # flash(errors)
        # return redirect('/')

    if len(data['password']) < 8:
        errors.append('Invalid password length')
            # flash(errors)
            # return redirect('/')
    if data['passwordconf'] != data['password']:
        errors.append('Passwords do not match')
                # flash(errors)
                # return redirect('/')

    if errors == []:

        query = "INSERT into users(first_name, last_name, email, password, passwordconf, created_at, updated_at) values(:first_name, :last_name, :email, :password, :passwordconf, NOW(), NOW())"

        mysql.query_db(query, data)

        return render_template("success.html")

    for error in errors:
        flash (error)
    return redirect('/')

@app.route('/login', methods=["POST"])
def login():

    errors = []

    data = {
        'email': request.form['email'],
    }

    user_query = 'SELECT * from users where email = :email'

    mysql.query_db(user_query, data)
    print mysql.query_db(user_query, data)

    if 'email' != ":email":
        errors.append('Email does not exist')

    for error in errors:
            flash(error)

    return redirect('/')

app.run(debug=True)
