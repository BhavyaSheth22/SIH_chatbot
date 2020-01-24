from flask import url_for, flash, redirect, request, Flask, render_template, jsonify
from sih_chatbot import app, db, bcrypt
from sih_chatbot.forms import RegistrationForm, LoginForm
from sih_chatbot.models import User, Message, Patient
from flask_login import login_user, current_user, logout_user, login_required
import pusher
import change



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
def landing():
    return render_template('landing.html')


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

@app.route("/chat")
def chat():
    messages = Message.query.all()
    return render_template('chat.html', messages=messages)

@app.route("/medical_history")
def medical_history():
    gender = ["Male", "Female", "Other"]
    blood = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    return render_template('medical_history.html', gender=gender, blood=blood)


@app.route("/medical_database", methods=['GET', 'POST'])
def medical_database():
    #text
    age = request.form.get('age')
    contact = request.form.get('contact')
    emergency_contact = request.form.get('emergency_contact')
    weight = request.form.get('weight')
    height = request.form.get('height')
    #select
    gender = request.form.get('gender_select')
    blood = request.form.get('blood_select')
    #checkbox
    conditions = request.form.getlist('status_condition') 
    symptoms = request.form.getlist('status_symptom')
    #radio
    surgery = request.form.getlist('surgeries')
    medication = request.form.getlist('medications')
    allergy = request.form.getlist('allergies')
    tobacco = request.form.getlist('tobacco')
    alcohol = request.form.getlist('alcohol')
    #all radio buttons and checkboxes are arrays are arrays
    #textarea
    surgery_text = request.form.get('surgeries_text')
    medication_text = request.form.get('medications_text')
    allergy_text = request.form.get('allergies_text')

    bmi = str(int(weight)/((int(height)/100)**2))
    condition = ""
    symptom = ""
    for c in conditions:
        condition += c + "," 
    for s in symptoms:
        symptom += s + "," 
    patient = Patient(first_name=current_user.first_name, 
                      last_name=current_user.last_name, 
                      age=str(age), 
                      contact=str(contact), 
                      emergency_contact=str(emergency_contact), 
                      weight=str(weight), 
                      height=str(height), 
                      bmi=bmi, 
                      gender=str(gender),
                      blood_group=str(blood),
                      conditions=condition,
                      symptoms=symptom,
                      surgery=str(surgery[0]),
                      medication=str(medication[0]),
                      allergy=str(allergy[0]),
                      tobacco=str(tobacco[0]),
                      alcohol=str(alcohol[0]),
                      surgery_text=str(surgery_text),
                      medication_text=str(medication_text),
                      allergy_text=str(allergy_text))
    db.session.add(patient)
    db.session.commit()
    return redirect(url_for('chat'))
    
    
    
    
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('landing'))

# @app.route('/ChatScreen')
# def onlineRef():
    
#     return render_template('ChatScreen.html', messages=messages)

@app.route('/message', methods=['POST'])
def message():

    try:
        message = request.form.get('message')
        # print(message)
        print(current_user.email)
        new_message = Message(message=message, key=True, email=current_user.email)
        # print(new_message)
        
        msg=change.chat(message)
        m = Message(message=msg, email="bot@bot.com")
        db.session.add(new_message)
        db.session.add(m)
        db.session.commit()
        print("chat function")
        print(msg)
        pusher_client.trigger('chat-channel', 'new-message', {'message': message, 'key':new_message.key})
        
        pusher_client.trigger('chat-channel', 'new-message', {'message': msg, 'key':False})#bot message triggering

        return jsonify({'result' : 'success'})
    
    except:

        return jsonify({'result' : 'failure'})

   

