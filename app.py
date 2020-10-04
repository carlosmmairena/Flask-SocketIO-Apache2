from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send, join_room, leave_room


app = Flask(__name__)
app.config['SECRET_KEY'] = '6A74SD85QWQWQDDFWEW4ERWE23RW5E52WE29++SD+FS-DF-SDFSD54F5EERE1231231EDEEWRWER!'
socketio = SocketIO(app)


@app.route('/', methods=['GET', 'POST'])
def inicio():
    return render_template('prueba.html')


@socketio.on('connect', namespace='/ws')
def connect():
    print('**************** Cliente conectado...')


@socketio.on('proforma', namespace='/ws')
def recibir_proforma(request):
    print(request['data'])
    print('********** Alertando nueva proforma')
    emit('proforma_nueva', broadcast=True)

@socketio.on('disconnect')
def disconnect():
    print('**************** Cliente desconectado')


@socketio.on('message', namespace='/ws')
def handle_message(message):
    print('**************** Mensaje recibido desde el cliente', message['data'])


@socketio.on('join', namespace='/ws')
def on_join(data):
    username = 'se ha unido'
    room = 'proformas'
    join_room(room)
    datos = {'usuario': username, 'sala': room}
    send(datos, room=room)


@socketio.on('leave', namespace='/ws')
def on_leave(data):
    username = 'se ha retirado'
    room = 'proformas'
    leave_room(room)
    datos = {'usuario': username, 'sala': room}
    send(datos, room=room)


if __name__ == '__main__':
    socketio.run(app, debug=True, host='localhost')
