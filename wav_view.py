#! /usr/bin/python
## 참고 https://nachwon.github.io/faster-waveform/

import os,sys
import subprocess
import audioop, numpy as np

import matplotlib.pyplot as plt
import matplotlib.animation as animation

from PIL import Image, ImageDraw

if len(sys.argv) < 2:# arg 필요
    print("args error!")
    exit()

def calculate_peaks(audio_data,bar_count = 1000):
    chunk_length = int(len(audio_data)/2 / bar_count)
    out = []
    for i in range(0,len(audio_data),2):
        out.append(int.from_bytes(audio_data[i:i+2],"little")-32768)
    loudness_of_chunks = [
        sum(out[i * chunk_length: (i + 1) * chunk_length])/chunk_length
        for i in range(bar_count)]

    max_rms = max(loudness_of_chunks) * 1.00

    return [int((loudness / max_rms) * 100)
            for loudness in loudness_of_chunks]
url = "a.mp3"
cmd = "ffmpeg -i "+ url +" -vn -f u16le -ar 16000 -threads 1 -"# convert pcm file
ps = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print ("started %s" % cmd)

def animate(i):# 애니메이트를 통한 데이터 갱신
    data = ps.stdout.read(16000 * 2 * 2)
    data = calculate_peaks(data)
    plt.clf()
    plt.ylim(-100,100)# 평준화
    return plt.plot(range(len(data)),data)

fig = plt.figure()
ani = animation.FuncAnimation(fig, animate, interval=500)
plt.show()

ps.kill()
print("END ")
