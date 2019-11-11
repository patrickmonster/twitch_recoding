#!/usr/bin/env python
import os
import json
import websocket
import requests

'''
project by Soungjin
make 2019.11.02
'''

class TwitchWSS(websocket.WebSocketApp):

    def __init__(self,username,passwd,channel,on_message,on_command=None,command="!",onError=None):
        super().__init__("wss://irc-ws.chat.twitch.tv:443/",on_open=self.onOpen,on_message = self.onMessage,on_error = onError,on_close = self.onClose)
        self.username = username
        self.passwd = passwd
        self.channel = channel

        self._message = on_message
        self.command = command
        self.oncommand = on_command

    def onError(self,message):
        print("Error",message)

    def onClose(self):
        try:
            self.closed()
        except:
            pass
        print("### closed ###")

    def onOpen(self):
        print("Connect to " + self.channel)
        self.onSend("REQ :twitch.tv/tags twitch.tv/commands twitch.tv/membership","CAP")
        self.onSend(self.passwd,"PASS")
        self.onSend(self.username,"NICK")
        self.onSend(self.channel,"JOIN")
    
    def sendMessage(self, message):
        self.onSend(self.channel + " :" +str(message))

    def onSend(self,message ,option ='PRIVMSG'):
        self.send(option + " " + message)

    def onMessage(self, message):
        if message == "":
            return
        data = self.parse_message(message.replace('\r\n',''))
        if data['command'] == "PRIVMSG":
            if data['message'][0] == self.command:
                if self.oncommand:
                    self.oncommand(self,data,data['message'][1:])
            else:
                if self._message:
                    self._message(self,data,data['message'])
        elif data['command'] == "PING":
            self.onSend(data['message'],"PONG")
        elif data['command'] == "JOIN":
            print(data['message'])

    def run(self):
        print("run")
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
