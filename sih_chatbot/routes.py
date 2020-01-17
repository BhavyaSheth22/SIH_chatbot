from flask import url_for, flash, redirect, request, Flask, render_template, jsonify
from sih_chatbot import app, db, bcrypt
from sih_chatbot.forms import RegistrationForm, LoginForm
from sih_chatbot.models import User, Message
from flask_login import login_user, current_user, logout_user, login_required
import pusher




# @app.route("/")
# @app.route("/home")
# def home():
#     return render_template('home.html')


pusher_client = pusher.Pusher(
  app_id='932401',
  key='474991b3a2877f9aa291',
  secret='628252859ca348ecb306',
  cluster='ap2',
  ssl=True
)

@login_required
@app.route("/")
@app.route("/home")
def home():
    return redirect(url_for('register'))
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
    messages = Message.query.all()
    return render_template('login.html', title='Login', form=form, messages=messages)

@app.route("/chat")
def chat():
    return render_template('ChatScreen.html')

# @app.route("/logout")
# def logout():
#     logout_user()
#     return redirect(url_for('home'))

# @app.route('/ChatScreen')
# def onlineRef():
    
#     return render_template('ChatScreen.html', messages=messages)

@app.route('/message', methods=['POST'])
def message():

    try:
        message = request.form.get('message')
        print(message)
        new_message = Message(message=message, key=True)
        db.session.add(new_message)
        db.session.commit()
        print(new_message.key)
        pusher_client.trigger('chat-channel', 'new-message', {'message': message, 'key':new_message.key})
        pusher_client.trigger('chat-channel', 'new-message', {'message': "hi", 'key':False})#bot message triggering

        return jsonify({'result' : 'success'})
    
    except:

        return jsonify({'result' : 'failure'})

   

