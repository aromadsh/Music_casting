import json
import subprocess

import keras
import pandas as pd
import numpy as np
from flask import Flask, jsonify
import tensorflow as tf
from keras.models import load_model
import librosa
import librosa.display
import matplotlib.pyplot as plt
import soundfile as sd
from pydub import AudioSegment
import soundfile as sf
import moviepy.editor as moviepy

def convert_webm_to_wav(file):
    command = ['ffmpeg', '-i', file, '-acodec', 'pcm_s16le', '-ac', '1', '-ar', '16000', './voice.wav']
    subprocess.run(command,stdout=subprocess.PIPE,stdin=subprocess.PIPE)

def voice():
    class_names = ['POP', 'R&B_Soul', '랩_힙합', '록_메탈', '발라드', '일렉트로니카']
    # src = "./voice.wav"
    # dst = "./test.wav"
    # audSeg = AudioSegment.from_mp3("./voice.wav")
    # audSeg.export(dst, format="wav")
    # sr= 22050
    # sf.write('test.wav', 'voice.webm', sr, format='WAV', endian='LITTLE', subtype='PCM_16')  # 깨지지 않음

    #채널 : 1채널

    #clip = moviepy.VideoFileClip('voice.webm')
    #clip.audio.write_audiofile("./voice.wav")
    convert_webm_to_wav('voice.webm')

    y, sr = librosa.load('voice.wav')
    # y, sr = sd.read("voice.wav")

    S = librosa.feature.melspectrogram(y, sr=sr)
    S_DB = librosa.amplitude_to_db(S, ref=np.max)
    librosa.display.specshow(S_DB, sr=sr, hop_length=512)
    plt.savefig("t.png")

    img = tf.keras.utils.load_img("t.png", target_size=(653, 979))
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)
    VGGmodel2 = load_model('Music_scketch_final_model.hdf5')
    predictions = VGGmodel2.predict(img_array)
    plt.imshow(img)
    score = tf.nn.softmax(predictions[0])
    genre = class_names[np.argmax(score)]
    return genre


def csv_genre(genre):
    print(genre)
    data = pd.read_csv('music_list.csv')
    df = pd.DataFrame(data)
    genre_df = df.loc[(df['genre'] == genre)]
    # genre_df30 = genre_df[:30]
    genre_df30 = genre_df.sample(n=30)
    s_id = genre_df30[['song_id']]
    json = s_id.to_json(orient='records', force_ascii=False)

    return json
