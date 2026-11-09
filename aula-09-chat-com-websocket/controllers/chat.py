from flask import request
from flask_socketio import emit

def init_app(socketio):
    #eventos a serem disparados pelo servidor
    
    #usuario se conectou
    @socketio.on("connect")
    def handle_connect():
        print(f"O usuário com a ID: {request.sid} se conectou.")
    #usuario se desconectou
    @socketio.on("disconnect")
    def handle_disconnect():
        print(f"O usuário com a ID: {request.sid} se desconectou.")
        
    #eventos globais
    @socketio.on("join")
    def handle_join(data):
        print(f"O usuário {data['nickname']} entrou no chat.")
        emit("join", data, broadcast=True)

    #usuario enviou uma mensagem
    @socketio.on("msg")
    def handle_msg(data):
        print(data)
        emit("showmsg", data, broadcast=True)