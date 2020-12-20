from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from forms import *
from models import *

from time import localtime, strftime

import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

app = Flask(__name__)
app.secret_key = 'replace later'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://kfhbafarwjdqwa:f0d2463f7c659badd77f5ce43bbbf97c1035ea8c3fe11c54e9b012f45b8f79b6@ec2-54-225-214-37.compute-1.amazonaws.com:5432/da5tto5evlsm28'
db = SQLAlchemy(app)

login = LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

socketio = SocketIO(app)
ROOMS = ["coding", "memes", "games", "animals"]

@app.route('/', methods=['GET', 'POST'])
def index():
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
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('chat'))

    return render_template("login.html", form=login_form)

@app.route("/logout", methods=['GET'])
def logout():
    logout_user()
    flash('Logged Out succesfully', 'success')
    return redirect(url_for('login'))

@app.route("/chat", methods=['GET', 'POST'])
def chat():
    if not current_user.is_authenticated:
        flash('Please login', 'danger')
        return redirect(url_for('login'))

    return render_template('chat.html', username=current_user.username, rooms=ROOMS)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

@socketio.on('message')
def message(data):
    msg = data['msg']
    username = data['username']
    room = data['room']
    time_stamp = strftime('%b-%d %I:%M%p', localtime())
    prediction = predict(msg)
    
    send({'msg': msg, 'username': username, 'time_stamp': time_stamp, 'prediction': prediction}, room=room)

@socketio.on('join')
def join(data):
    username = data['username']
    room = data['room']
    join_room(room)

    send({"msg": username + " has joined the " + room + " room."}, room=room)

@socketio.on('leave')
def leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)

    send({"msg": username + " has left the room"}, room=room)

def predict(message):
    model=load_model('keras_model/model.h5')
    with open('keras_model/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    x_1 = tokenizer.texts_to_sequences([message])
    x_1 = pad_sequences(x_1, maxlen=300)
    prediction = model.predict(x_1)[0][0]

    if prediction >= 0.6:
        return round(prediction*100, 2)

    elif prediction <= 0.4:
        return -(100-round(prediction*100, 2))

    return 0

if __name__ == '__main__':
    socketio.run(app, debug=True)
