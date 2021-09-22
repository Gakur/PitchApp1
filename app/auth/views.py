from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from .form import LoginForm, SignupForm
from .. import db

from app.auth import auth
from app.models import User
from ..email import mail_message


@auth.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user is not None and user.check_password(login_form.password.data):
            login_user(user, login_form.remember.data)
            flash('Invalid username or Password')
            return redirect(url_for('main.index'))       

    title = "pitch login"
    return render_template('auth/login.html', login_form=login_form, title=title)
    


@auth.route("/logout")
# @login_required
def logout():
    logout_user()
    title = "pitch"
    flash('You have been successfully logged out')
    return redirect(url_for("auth.login"))


@auth.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignupForm()
    title = "New Account"
    if form.validate_on_submit():
        user = User(email=form.email.data,username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('auth/signup.html', signup_form=form, title=title)

# @auth.route('/logout')
# def logout():
#     """
#     Function that logs out a user
#     """

#     logout_user()
#     return redirect(url_for('auth.login'))
