from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO

from forms import *

app = Flask(__name__)
app.secret_key = 'replace later'

socketio = SocketIO(app)

@app.route('/', methods=['GET', 'POST'])
def index():

    reg_form = RegistriationForm()
    if reg_form.validate_on_submit():
        return "Works"

    return render_template("index.html", form=reg_form)


if __name__ == '__main__':
    socketio.run(app, debug=True)
