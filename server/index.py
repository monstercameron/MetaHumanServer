from flask import Flask, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
app.message_history = []

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/api/data')
def get_data():
    print('message history:',app.message_history)
    return jsonify(app.message_history)


@socketio.on('connect')
def test_connect():
    print('Client connected')


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
    emit('message', message, broadcast=True)


if __name__ == '__main__':
    app.run(debug=True)
