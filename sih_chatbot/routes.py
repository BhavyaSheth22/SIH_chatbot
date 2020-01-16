from flask import render_template, url_for, flash, redirect, request
from sih_chatbot import app, db, bcrypt
from sih_chatbot.forms import RegistrationForm, LoginForm
from sih_chatbot.models import User
from flask_login import login_user, current_user, logout_user, login_required


# @app.route("/")
# @app.route("/home")
# def home():
#     return render_template('home.html')


@login_required
@app.route("/chat")
def chat():
    return render_template('chatDemo.html')

@app.route("/")
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('chat'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(first_name=form.first_name.data, last_name=form.last_name.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('chat'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('chat'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


# @app.route("/logout")
# def logout():
#     logout_user()
#     return redirect(url_for('home'))


