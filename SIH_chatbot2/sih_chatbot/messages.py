# # import pusher
# # from flask import Flask, render_template, jsonify, request
# # # from flask_sqlalchemy import SQLAlchemy 
# # from sih_chatbot import db, app

# # app = Flask(__name__)
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# # pusher_client = pusher.Pusher(
# #   app_id='932401',
# #   key='474991b3a2877f9aa291',
# #   secret='628252859ca348ecb306',
# #   cluster='ap2',
# #   ssl=True
# # )

# # db = SQLAlchemy(app)

# # class Message(db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     # username = db.Column(db.String(50))
# #     message = db.Column(db.String(500))
# #     key = db.Column(db.Boolean(), default=False) # User = true, bot = false

# @app.route('/ChatScreen')
# def onlineRef():

#     messages = Message.query.all()
    
#     return render_template('ChatScreen.html', messages=messages)

# @app.route('/message', methods=['POST'])
# def message():

#     try:
#         message = request.form.get('message')

#         new_message = Message(message=message, key=True)
#         db.session.add(new_message)
#         db.session.commit()

#         pusher_client.trigger('chat-channel', 'new-message', {'message': message})

#         return jsonify({'result' : 'success'})
    
#     except:

#         return jsonify({'result' : 'failure'})

   


# if __name__ == '__main__':
#     app.run(debug=True)