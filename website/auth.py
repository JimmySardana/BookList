from flask import Blueprint, render_template, request, url_for, redirect
from werkzeug.utils import redirect
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.top_books'))
    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                return render_template("login.html", email_value=email, valid_email=True, user=current_user)
        else:
            return render_template("login.html", valid_pass=True, user=current_user)
                


    return render_template("login.html", valid_email=True, valid_pass=True, user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('views.top_books'))

    validity = {
        "email": True,
        "username": True,
        "password": True,
        "confirm_password": True
    }

    error_msg = {
        "email": "",
        "username": "",
        "password": "",
    }

    values = {
        "email": "",
        "username": ""
    }

    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')

        values["email"] = email
        values["username"] = username

        if len(email) == 0:
            validity['email'] = False
            error_msg['email'] = "Email cannot be empty"
        else:
            user = User.query.filter_by(email=email).first()
            if user:
                validity['email'] = False
                error_msg['email'] = "Email already exists"
        if len(username) == 0:
            validity['username'] = False
            error_msg['username'] = "Username cannot be empty"
        else:
            user = User.query.filter_by(username=username).first()
            if user:
                validity['username'] = False
                error_msg['username'] = "Username already exists"
        if len(password) == 0:
            validity['password'] = False
            error_msg['password'] = "Password cannot be empty"
        if password != confirm_password:
            validity['password'] = False
            validity['confirm_password'] = False
            error_msg['password'] = "Password doesn't match"

        
        for value in validity.values():
            if not value:
                return render_template("sign_up.html", validity=validity, error_msg=error_msg, values=values, user=current_user)

        values["username"] = ""
        values["email"] = ""

        new_user = User(email = email, username=username, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))

    return render_template("sign_up.html", validity=validity, error_msg=error_msg, values=values, user=current_user)

