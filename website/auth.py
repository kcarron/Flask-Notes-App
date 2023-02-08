from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user

#This is the blueprint for auth. so we can use
# things like auth.login to redirect.
#blueprint is essentially a way to redirect the user
#to a different page that is in another file. 
# so we don't have a lot of routes in one file. 
auth = Blueprint('auth', __name__)
#defines this route and which it has the two methods
@auth.route('/login', methods=['GET', 'POST'])
#This function practically retrieves the data sent from the login
#page and does something with it. 
def login():
    #if the request method is post
    if request.method == 'POST':
        #it gets the email and password
        email = request.form.get('email')
        password = request.form.get('password')
        #tries to find the email field in the User table
        user = User.query.filter_by(email=email).first()
        #if there is any returned data
        if user:
            #hashes the password and logs the user in
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category = 'success')
                #logs user in and remembers it in case they refresh
                #so they don't have to log in again
                login_user(user, remember=True)
                #redirects the logged in user to views.home 
                #where the /home backend is
                return redirect(url_for('views.home'))
            else:
                 flash('Incorrect password, try again', category='error')   
        else:
            flash('Email does not exist', category='error')
    #this renders the login.html page where the user is set 
    # to current_user
    
    return render_template("login.html", user=current_user)

#creates a route named logout
@auth.route('/logout')
@login_required #only can access this if user is logged in
def logout():
    #flash function that logs current_user out
    logout_user()
    #redirected to login page
    return redirect(url_for('auth.login'))
#creates a route called sign-up that has the methods
#post and get
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    #if the request is POST
    if request.method == 'POST':
        #it gets all the fields for the User table in models.py
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        #gets the email
        user = User.query.filter_by(email=email).first()
        #pretty self explanatory
        if user:
            flash('Email already exists', category = 'error')
        elif len(email) < 2:
            flash('Email must be greater than 3 characters', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 characters', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters long', category='error')
            pass
        else:
            #add user to database
            #sends the data to the User table filling in the fields
            #with the data we retrieved
            new_user = User(email=email,first_name=first_name, password=generate_password_hash(password1, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            #This creates localstorage like thing to tell the browser that
            #the user is logged in. So if they refresh, they are stil 
            #logged in
            login_user(user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
    #renders sign-up.html and passes user to it
    return render_template("sign-up.html", user=current_user)

