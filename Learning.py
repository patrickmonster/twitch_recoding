
import os
import json


class SaveList:
    def __init__(self,filename):
        self.data = {}
        self._size = 0
        self.filename = filename
        if os.path.isfile(self.filename):
            with open(self.filename, 'r') as f:
                self.data = json.load(f)

    def save(self):
        with open(self.filename, 'w') as f:
            f.write(json.dumps(self.data))
        print(self.filename ,"데이터 수집....저장")

class n_gram(SaveList):

    def __init__(self,filename='text.json'):
        super().__init__(filename)
        self._size = 3

    def add(self,message):
        data = list(zip(*[message[i:] for i in range(self._size)]))
        for i in data:
            s = "".join(i)
            if s not in self.data:
                self.data[s] = 1
            else:
                self.data[s] += 1

class times(SaveList):

    def __init__(self,filename='time.json'):
        super().__init__(filename)
        self._size = 9# 10번째 1초     // 10ms 단위로 기록

    def add(self,message):
        t = message[:self._size]
        print("["+t,end="]")
        if t not in self.data:
            self.data[t] = 1 
        else :
            self.data[t] += 1
