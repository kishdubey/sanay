from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO

app = Flask(__name__)
app.secret_key = 'replace later'

socketio = SocketIO(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/chat')
def chat():
    username = request.args.get('username')
    room = request.args.get('room')

    if username and room:
        return render_template("chat.html", username=username, room=room)
    return redirect(url_for('home'))

if __name__ == '__main__':
    socketio.run(app, debug=True)
