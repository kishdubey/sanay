from flask import Flask, render_template, request, redirect, url_for
from forms import *
from models import *

app = Flask(__name__)
app.secret_key = 'replace later'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://kfhbafarwjdqwa:f0d2463f7c659badd77f5ce43bbbf97c1035ea8c3fe11c54e9b012f45b8f79b6@ec2-54-225-214-37.compute-1.amazonaws.com:5432/da5tto5evlsm28'
db = SQLAlchemy(app)

@app.route('/', methods=['GET', 'POST'])
def index():

    reg_form = RegistrationForm()

    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        # check username duplicate
        user_object = User.query.filter_by(username=username).first()
        if user_object:
            return "Someone else has this username"


        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return "Inserted!"

    return render_template("index.html", form=reg_form)

if __name__ == '__main__':
    app.run(debug=True)
