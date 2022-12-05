import base64
from codecs import encode

import audioread
from flask import Flask, render_template, request, send_file, flash,redirect, url_for
import os
import pandas as pd
from scipy.io import wavfile
from werkzeug.utils import secure_filename
from flask_cors import CORS
from to_json import *
import time
import scipy.io.wavfile

app = Flask(__name__)
CORS(app)

@app.route('/', methods = ['GET', 'POST'])
def down_file():
    if request.method == 'POST':
        result = request.form
        query = result['file']

        bytes_mg = encode(query, 'utf-8')
        b = base64.decodebytes(bytes_mg)
        open('voice.webm', 'wb').write(b)

        time.sleep(3)
        genre = voice()
        json = csv_genre(genre)
        time.sleep(1)

        os.remove("voice.webm")
        os.remove("voice.wav")
        os.remove("t.png")
    return json

if __name__ == '__main__':
    app.run(host='192.168.0.71',port=5000)


#set FLASK_APP=MusicSketch
#set FLASK_DEBUG=TRUE
#flask run -h 192.168.0.148 #랜선
#flask run -h 192.168.0.71 #와이파이


#######################################################22222
# result = request.form
#
# query = result['file']
#
# bytes_mg = encode(query, 'utf-8')
# b = base64.decodebytes(bytes_mg)
# with open('test.wav', 'wb') as f:
#     f.write(b)
#     print(f.name) # -> test.wav
#
# print('voice 들어가기전 ')
#
# json = voice()
# print('voice 들어가기후 ')
#######################################################

# result = request.form
#
# query = result['file']
#
# bytes_mg = encode(query, 'utf-8')
# b = base64.decodebytes(bytes_mg)
# open('test.wav', 'wb').write(b)
#
# data = pd.read_csv('music_list.csv')
# df = pd.DataFrame(data)
# genre_df = df.loc[(df['genre'] == 'J-POP')]
# genre_df30 = genre_df.sample(n=30)
# s_id = genre_df30[['song_id']]
# json = s_id.to_json(orient='records', force_ascii=False)
# time.sleep(3)
# os.remove("test.wav")
# print('wav 삭제')
