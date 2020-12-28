from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from forms import *
from models import *

from time import localtime, strftime

import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import BernoulliNB

# Initiate App
app = Flask(__name__)
app.secret_key = 'REPLACE LATER'

# Setting up SQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://kfhbafarwjdqwa:f0d2463f7c659badd77f5ce43bbbf97c1035ea8c3fe11c54e9b012f45b8f79b6@ec2-54-225-214-37.compute-1.amazonaws.com:5432/da5tto5evlsm28'
db = SQLAlchemy(app)

# Login Manager to handle user handling
login = LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# Web Sockets for messaging
socketio = SocketIO(app)

# Default rooms
ROOMS = ["coding", "memes", "games", "animals"]

@app.route('/', methods=['GET', 'POST'])
def index():
    """Registration Page"""
    reg_form = RegistrationForm()

    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = sha256.hash(reg_form.password.data)

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        flash('Registered succesfully. Please login.', 'success')
        return redirect(url_for('login'))

    return render_template("index.html", form=reg_form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login Page"""
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('chat'))

    return render_template("login.html", form=login_form)

@app.route("/logout", methods=['GET'])
def logout():
    """Logout Page, Redirects to Login"""
    logout_user()
    flash('Logged Out succesfully', 'success')
    return redirect(url_for('login'))

@app.route("/chat", methods=['GET', 'POST'])
def chat():
    """Chat Page"""
    # if user is not authenticated
    if not current_user.is_authenticated:
        flash('Please login', 'danger')
        return redirect(url_for('login'))

    return render_template('chat.html', username=current_user.username, rooms=ROOMS)

@app.errorhandler(404)
def page_not_found(e):
    """If page not found"""
    return render_template('error.html'), 404

@socketio.on('message')
def message(data):
    """Sending Message to Client"""
    msg = data['msg']
    username = data['username']
    room = data['room']
    time_stamp = strftime('%b-%d %I:%M%p', localtime())
    prediction = predict(msg)

    send({'msg': msg, 'username': username, 'time_stamp': time_stamp, 'prediction': prediction}, room=room)

@socketio.on('join')
def join(data):
    """Joining Room"""
    username = data['username']
    room = data['room']
    join_room(room)

    send({"msg": username + " has joined the " + room + " room."}, room=room)

@socketio.on('leave')
def leave(data):
    """Leaving Room"""
    username = data['username']
    room = data['room']
    leave_room(room)

    send({"msg": username + " has left the room"}, room=room)

def predict(text):
    with open('sentiment_prediction_model/vectorizer.pickle', 'rb') as handle:
        vectorizer = pickle.load(handle)

    with open('sentiment_prediction_model/BNBmodel.pickle', 'rb') as handle:
        model = pickle.load(handle)

    preprocessed_text = vectorizer.transform([text])
    sentiment = model.predict_proba(preprocessed_text)[0]

    if sentiment[0] > sentiment[1]:
        return f"-{round(sentiment[0]*100, 2)}"
    return f"{round(sentiment[1]*100, 2)}"

if __name__ == '__main__':
    socketio.run(app, debug=True)
