# twitch_recoding

install
===
사용전, 필수 설치 패키지 

```
python -m pip install websocket requests
```

트위치용 체팅을 관리하는 봇 제작(python) 

Sample
=====
```
from chatbot import TwitchWSS

def callback_message(ws,data,msg):
    print(data['display-name'],":"+msg)

def callback_command(ws,data,message):
    msg = message.split()
    print("COMMAND",msg)
    if msg[0] == "업타임": # !uptime
        ws.sendMessage("방송시간:" + ws.get_stream_running_s())
tw = chatbot.TwitchWSS('username','oauth:pw','#channel',callback_message,on_command=callback_command)
tw.run()
```



연결 인자
=====

### 필수 ###
username #유저id

passwd #유저 url (pw)

channel #접속할 채널

on_message #수신한 메세지를 리턴 할 메서드   callboack(TwitchWSS,data,message)

### 선택 ###
on_command=None # 커맨드 호출시에 콜백되는 함수 callboack(TwitchWSS,data,message)

command="!" # 커맨드로 입력받을 문자

onError=None # 에러처리

