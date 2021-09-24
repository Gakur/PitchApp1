from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from .form import LoginForm, SignupForm
from .. import db

from app.auth import auth
from app.models import User
from ..email import mail_message


@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user is None:
            error = 'A user with that email  does not exist'
            return render_template('auth/login.html', error=error)
        # is_correct_password = user.check_password(login_form.password.data)
        # print(is_correct_password)
        # if not is_correct_password:
        #     error = 'A user with that password does not exist'
        #     return render_template('auth/login.html', error=error)
        login_user(user, login_form.remember.data)
        return redirect('/')
    title = 'PitchApp Login Page'    
    return render_template('auth/login.html' , login_form=login_form, title=title)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    title = "Signup Page"
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('auth/signup.html', signup_form = form, title=title)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
