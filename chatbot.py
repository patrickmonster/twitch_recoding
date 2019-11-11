#!/usr/bin/env python
import os
import json
import websocket
import requests


channel = '#' # 접속 채팅방 이름 >#userid
username = ''#챗봇 클라이언트 id
passwd = 'oauth:'#리다이렉션 url
comm = "!" #봇 명령 인식 기호

def on_message(ws, message):
    if message == "":
        return
    #try:
    data = parse_message(message.replace('\r\n',''))
    if data['command'] == "PRIVMSG":
        if data['message'][0] == comm:
            get_command(ws,data,data['message'][1:])
        else:
            get_message(ws,data,data['message'])
    elif data['command'] == "PING":
        on_send(ws,data['message'],"PONG")
    elif data['command'] == "JOIN":
        print(data['message'])

def on_error(ws, error):
    print("ERROR", error)

def on_close(ws):
    try:
        ws.closed()
    except:
        pass
    print("### closed ###")

def send_message(ws, message):
    on_send(ws,channel + " :" +str(message))

def on_send(ws,message ,option ='PRIVMSG'):
    #print("전송 : %s %s" %(option,message))
    ws.send(option + " " + message)

def on_open(ws):
    on_send(ws,"REQ :twitch.tv/tags twitch.tv/commands twitch.tv/membership","CAP")
    on_send(ws,passwd,"PASS")
    on_send(ws,username,"NICK")
    on_send(ws,channel,"JOIN")

def parse_message(rawMessage):
    parseMessage = {'message':'','command':''}
    if (rawMessage[0] == ':'):
        data = rawMessage.split()
        parseMessage['command'] = data[1]
        if (parseMessage['command'] == 'JOIN'):
            parseMessage['message'] = "Join user :" + data[2]
        else :
            parseMessage['message'] = rawMessage
    elif rawMessage[:4] in ["PING"]:
        parseMessage['command'],parseMessage['message'] = rawMessage.split()
    else:
        data = rawMessage.split(";")
        for i in data:
            d = i.split("=")
            if i == '' or len(d) < 2:
                continue
            parseMessage[d[0]] = d[1]
        if 'user-type' in parseMessage:
            user_type = parseMessage['user-type'].split()
            if "mod" in user_type[0]: #타 봇/관리자 
                del user_type[0]
            parseMessage['user-connect'] = user_type[0]
            parseMessage['command'] = user_type[1]
            parseMessage['chatroom'] = user_type[2]
            parseMessage['message'] = " ".join(user_type[3:])[1:]
    return parseMessage

countl = {}

def get_command(ws,data,message):
    if len(message) == 0:
        return
    message = message.split()
    #print(message)
    if message[0] == "생존":
        send_message(ws,"Recoding bot 실행중...")
    elif message[0] == "카운트":
        if len(message) <= 1:
            send_message(ws, "명령에러] :!카운트 <카운트이름>")
            return
        if message[1] not in countl:
            countl[message[1]] = 0
            send_message(ws, "항목 추가 "+ message[1])
        else:
            send_message(ws,"현재 카운트 :" + str(countl[message[1]]))
    else:
        #send_message(ws,"명령어 추가중..")
        return
def get_message(ws,data,message):
    print(data['display-name']+" :",data['message'])
    for i in countl:
        if i in message:
            countl[i] += 1
            break

if __name__ == "__main__":
    #websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://irc-ws.chat.twitch.tv:443/",
                            on_open = on_open,
                            on_message = on_message,
                            on_error = on_error,
                            on_close = on_close)
    ws.run_forever()
