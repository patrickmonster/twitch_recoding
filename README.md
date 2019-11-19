# twitch_recoding



트위치용 체팅을 관리하는 봇 제작(python) 

Sample
=====

import chatbot.TwitchWSS

def callback_message(ws,data,msg):
    print(data['display-name'],":"+msg)
    
tw = chatbot.TwitchWSS('username','oauth:pw','#channel',callback_message)
tw.run()




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

### 연락처 ###

Soungjin Ryu 
rsj1120@dongguk.ac.kr
