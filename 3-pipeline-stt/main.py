import whisper
import os
import ffmpeg

file = "C:/Users/Cam_ws_win/Desktop/repos/metahumanserver/samples/output1.wav"

if os.path.exists(file):
    print("File exists")
else:
    print("File does not exist")

# ffmpeg.input(file, threads=0)

model = whisper.load_model("base")
model.encoder.to("cuda:0")
model.decoder.to("cuda:0")

result = model.transcribe("C:/Users/Cam_ws_win/Desktop/repos/metahumanserver/samples/output1.wav")
print(result["text"])