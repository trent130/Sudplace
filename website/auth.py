from flask import Blueprint, render_template, request, flash, redirect, url_for
from.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db 
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method =='POST':
        email = request.form.get('email')
        password = request.form.get('password1')  # Use 'password1' instead of 'Password1'

        user = User.query.filter_by(email=email).first()
        if user:
            if password and check_password_hash(user.password, password):  # Check if password is not None
                flash('Logged in successfull!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist',  category='error')
    return render_template("login.html", user= current_user)
    

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('Password1')
        password2 = request.form.get('Password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists!', category='error')
        elif len(email) <= 6:
            flash('Email must be provided and more than 6 characters', category='error')

        elif len(first_name) <= 6:
            flash('First name must be provided and more than 6 characters', category='error')

        elif not password1 or len(password1) < 10:
            flash('Password must be provided and more than 10 characters', category='error')

        elif not(password1 and password2 and password1 == password2 ):
            flash('Passwords do not match', category='error')

        else:
            # Add user to the database
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)  # Login the new_user instead of user
            flash('Registration successful!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign-up.html", user= current_user)

