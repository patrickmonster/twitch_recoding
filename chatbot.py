#!/usr/bin/env python
import os
import json
import websocket
import requests


class TwitchWSS(websocket.WebSocketApp):

    def __init__(self,username,passwd,channel,on_message,on_command=None,command="!",onError=None):
        super().__init__("wss://irc-ws.chat.twitch.tv:443/",on_open=self.onOpen,on_message = self.onMessage,on_error = onError,on_close = self.onClose)
        self.username = username
        self.passwd = passwd
        self.channel = channel

        self._message = on_message
        self.command = command
        self.oncommand = on_command



    def onClose(self,ws):
        try:
            ws.closed()
        except:
            pass
        print("### closed ###")

    def onOpen(self,ws):
        self.onSend(ws,"REQ :twitch.tv/tags twitch.tv/commands twitch.tv/membership","CAP")
        self.onSend(ws,passwd,"PASS")
        self.onSend(ws,username,"NICK")
        self.onSend(ws,channel,"JOIN")
    
    def sendMessage(self,ws, message):
        self.onSend(ws,channel + " :" +str(message))

    def onSend(self,ws,message ,option ='PRIVMSG'):
        ws.send(option + " " + message)

    def onMessage(self,ws, message):
        if message == "":
            return
        data = self.parse_message(message.replace('\r\n',''))
        if data['command'] == "PRIVMSG":
            if data['message'][0] == comm:
                if callable(self.oncommand):
                    self.oncommand(ws,data,data['message'][1:])
            else:
                if callable(self.oncommand):
                    self._message(ws,data,data['message'])
        elif data['command'] == "PING":
            self.onSend(ws,data['message'],"PONG")
        elif data['command'] == "JOIN":
            print(data['message'])

    def run(self):
        super().run_forever()

    def parse_message(self,rawMessage):# 구문분석
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
                if "mod" in user_type[0]:
                    del user_type[0]
                parseMessage['user-connect'] = user_type[0]
                parseMessage['command'] = user_type[1]
                parseMessage['chatroom'] = user_type[2]
                parseMessage['message'] = " ".join(user_type[3:])[1:]
        return parseMessage
