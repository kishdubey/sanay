from flask import Flask, render_template, request, redirect, url_for
from forms import *

app = Flask(__name__)
app.secret_key = 'replace later'

@app.route('/', methods=['GET', 'POST'])
def index():

    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        return "Works"

    return render_template("index.html", form=reg_form)


if __name__ == '__main__':
    app.run(debug=True)
