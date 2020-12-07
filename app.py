from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

from forms import *
from models import *

app = Flask(__name__)
app.secret_key = 'replace later'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://kfhbafarwjdqwa:f0d2463f7c659badd77f5ce43bbbf97c1035ea8c3fe11c54e9b012f45b8f79b6@ec2-54-225-214-37.compute-1.amazonaws.com:5432/da5tto5evlsm28'
db = SQLAlchemy(app)

login = LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/', methods=['GET', 'POST'])
def index():

    reg_form = RegistrationForm()

    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = sha256.hash(reg_form.password.data)

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

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

@app.route("/chat", methods=['GET', 'POST'])
def chat():
    if not current_user.is_authenticated:
        return "Please login before chatting"
    return "chat"

@app.route("/logout", methods=['GET'])
def logout():
    logout_user()
    return "Logged out"

if __name__ == '__main__':
    app.run(debug=True)
