
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO,emit,send
import socket

import eventlet
eventlet.monkey_patch()

import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

# Create :-)
cur = conn.cursor()
DBC = 'CREATE TABLE IF NOT EXISTS log (id serial,msg text);'
cur.execute(DBC)
conn.commit()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
sio = SocketIO(app) # , message_queue='redis://')

th = None

HOST = '192.168.2.123'  # The server's hostname or IP address
PORT = 4532        # The port used by the server

def worker():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            s.sendall(b"f\n")
            data = s.recv(1024)
            #print('Received', str(data)) #repr(data))
            sio.emit("chat message","Freq is: %s" % data.decode("utf-8"))
            eventlet.sleep(0.5)

@app.route('/')
def index():
    """Serve the client-side application."""
    return render_template('index.html')

@sio.on('connect')
def connect():
    cur = conn.cursor()
    cur.execute('select msg from log order by id')
    for msg in cur.fetchall():
        emit('chat message',"replay: %s" % msg[0])
    #emit('chat message',DATABASE_URL)
    #global th
    #print('connect (%s)' % request.sid)
    #print('connect')
    #if not th:
        #th = eventlet.spawn(worker)
        #print(th)

@sio.on('chat message')
def chat_message(data):
    #print('chat message ', data)
    cur = conn.cursor()
    cur.execute('INSERT INTO log (msg) values (%(msg)s)',{ 'msg': data })
    conn.commit()
    emit('chat message',"OK")
    sio.emit('chat message', "[%s] %s" % (request.sid,data))

@sio.on('disconnect')
def disconnect():
    pass
    #global th
    #print('disconnect ')
    #th.kill()
    #th = None

if __name__ == '__main__':
    sio.run(app)
