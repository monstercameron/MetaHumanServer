import os
import struct
import pyaudio
import pvporcupine
from dotenv import load_dotenv

load_dotenv()
ACCESS_KEY = os.getenv("ACCESSKEY")
KEYWORDS = ["computer", "porcupine", 'americano']

porcupine = pvporcupine.create(access_key=ACCESS_KEY, keywords=KEYWORDS)
pa = pyaudio.PyAudio()
audio_stream = pa.open(rate=porcupine.sample_rate,
                       channels=1,
                       format=pyaudio.paInt16,
                       input=True,
                       frames_per_buffer=porcupine.frame_length)


def detect_hotword(callback):
    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        keyword_index = porcupine.process(pcm)

        if keyword_index >= 0:
            callback(KEYWORDS[keyword_index])
