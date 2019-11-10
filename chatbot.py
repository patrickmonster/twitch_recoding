import sys
import websocket
import requests

channel = ''#chat room name
username = '' # bot user name
passwd = '' # oauth: bot passwd
comm = "!" # call bot command

def on_message(ws, message):
    if message == "":# no message
        return
    try:
        data = parse_message(message.replace('\r\n',''))
        if data['command'] == "PRIVMSG":# recive to message
            print(data['user']['display-name']+" :",data['message'])
            if data['message'][0] == comm:
                get_command(ws,data['user'],data['message'][1:])
            else:
                get_message(ws,data['user'],data['message'])
        elif data['command'] == "PING":# sending Ping to pong
            on_send(ws,data['message'],"PONG")
        elif data['command'] == "JOIN":# join to user
            print(data['message'])
    except Exception as e:# non error
        print("Error ",message, e)

def on_error(ws, error):
    print("ERROR", error)#service connect error

def on_close(ws):# server is close
    ws.closed()
    print("### closed ###")

def send_message(ws, message):# send to message
    on_send(ws,channel + " :" +message)

def on_send(ws,message ,option ='PRIVMSG'):# send command
    print("전송 : %s %s" %(option,message))
    ws.send(option + " " + message)

def on_open(ws):# connect twitch server to first sending data
    on_send(ws,"REQ :twitch.tv/tags twitch.tv/commands twitch.tv/membership","CAP")
    on_send(ws,passwd,"PASS")# pw send
    on_send(ws,username,"NICK")# send bot name
    on_send(ws,channel,"JOIN")# send join call

def parse_message(rawMessage):# convert to message
    parseMessage = {'message':'','command':''}
    if (rawMessage[0] == ':'):#command to protocal
        data = rawMessage.split()
        parseMessage['command'] = data[1]
        if (parseMessage['command'] == 'JOIN'):
            parseMessage['message'] = "Join user :" + data[2]
        else :
            parseMessage['message'] = rawMessage
    elif rawMessage[:4] in ["PING"]:# recive to ping protocal
        parseMessage['command'],parseMessage['message'] = rawMessage.split()
    else:# recive data
        data = rawMessage.split(":")
        parseMessage['command'] = data[1].split()[1]
        parseMessage['message'] = ":".join(data[2:])
        data = data[0].split(';')
        parseMessage['user'] = {}
        for i in data:
            item = i.split('=')
            parseMessage['user'][item[0]] = item[1]
    return parseMessage

countl = {}

def get_command(ws,data,message):#command call
    message = message.split()
    if message[0] == "생존":#a live command 
        send_message(ws,"테스트봇 실행중...")
        return
    elif message[0] == "카운트":# count command
        if len(message) <= 1:
            send_message(ws, "명령어 에러! \r\n!카운트 <카운트이름>")
            return
        if message[1] not in countl:
            countl[message[1]] = 0
            send_message(ws, "항목 추가 "+ message[1])
            return
        else:
            send_message(ws,"현재 카운트 :" + str(countl[message[1]]))
            return
    else:
        #send_message(ws,"명령어 추가중..")
        return
def get_message(ws,data,message):#message call
    for i in countl:
        if i in message:
            countl[i] += 1
            break

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://irc-ws.chat.twitch.tv:443/",#subprotocols="irc",
                            on_message = on_message,
                            on_error = on_error,
                            on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
