
from flask import Flask, render_template, session, request, send_from_directory
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
DBC = '''
CREATE TABLE IF NOT EXISTS votes (
    id      text not null,
    name    text not null,
    votes   integer[] not null
)
'''
cur.execute(DBC)
conn.commit()

FETCH_ALL_VOTES = '''
SELECT v.id, a.number, a.value 
FROM   votes AS v
LEFT   JOIN LATERAL unnest(v.votes)
                    WITH ORDINALITY AS a(value, number) ON TRUE
WHERE value IS NOT NULL and value > -9999
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
sio = SocketIO(app) # , message_queue='redis://')

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")

# serve application
@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
    return send_from_directory(root, path)

@app.route('/', methods=['GET'])
def redirect_to_index():
    return send_from_directory(root, 'index.html')

@sio.on('connect')
def connect():
    print("Connect: %s" % (request.sid))
    cur = conn.cursor()
    cur.execute('select id,name from votes')
    for msg in cur.fetchall():
        emit('register',{ 'id': msg[0], 'name': msg[1]})
    cur.execute(FETCH_ALL_VOTES)
    for msg in cur.fetchall():
        print("%s => %s = %s" % (msg[0],msg[1],msg[2]))
        emit('vote',{'id':msg[0],'number':msg[1]-1,'value': msg[2]})

@sio.on('disconnect')
def disconnect():
    print("Disconnect: %s" % (request.sid))

@sio.on('register')
def on_register(id,name):
    cur = conn.cursor()
    cur.execute("INSERT INTO votes values(%(id)s,%(name)s,'{-9999}')",{ 'id': id, 'name': name })
    conn.commit()
    sio.emit('register', {'id': id, 'name': name})

@sio.on('vote')
def vote(id,number,value):
    if number < 0:
        return
    cur = conn.cursor()
    cur.execute('UPDATE votes set votes[%(number)s] = %(value)s WHERE id = %(id)s',{ 'value': value, 'number': number+1, 'id': id })
    conn.commit()
    sio.emit('vote',{'id':id,'number':number,'value': value})
    print("Vote: %s[%d]=%d" % (id,number,value))

@sio.on('disconnect')
def disconnect():
    print("Disconnect: %s" % (request.sid));

if __name__ == '__main__':
    sio.run(app)
