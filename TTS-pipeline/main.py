from TTS.api import TTS
import os

folder = "C:/Users/Cam_ws_win/Desktop/repos/metahumanserver/samples"

if os.access(folder, os.W_OK):
    print("Folder is writable")
else:
    print("Folder is not writable")


# Running a multi-speaker and multi-lingual model
folder = "C:/Users/Cam_ws_win/Desktop/repos/metahumanserver/samples"


# Running a multi-speaker and multi-lingual model

# List available 🐸TTS models and choose the first one
# model_name = TTS.list_models()[0]
# print(TTS.list_models())
# Init TTS
tts = TTS(model_name='tts_models/en/vctk/vits', progress_bar=True, gpu=True)
# Run TTS
# ❗ Since this model is multi-speaker and multi-lingual, we must set the target speaker and the language
# Text to speech with a numpy output
# wav = tts.tts("This is a test! This is also a test!!", speaker=tts.speakers[0], language=tts.languages[0])
# Text to speech to a file
tts.tts_to_file(text="Adolf Hitler, the infamous Nazi leader during World War II, died on April 30, 1945, in his underground bunker in Berlin, Germany. According to historical records, he committed suicide by shooting himself in the head with a pistol. His long-time partner, Eva Braun, took poison and died alongside him. The exact details of Hitler's and Eva Braun's deaths were not widely known until years after the war. It's important to note that Hitler's death is a historical fact, and there are no credible sources that suggest he survived the war and lived a secret life afterward.",
                speaker=tts.speakers[0], file_path=f"{folder}/tts-out.wav")

# Running a single speaker model

# Init TTS with the target model name
# tts = TTS(model_name="tts_models/en/ljspeech/overflow", progress_bar=True, gpu=True)
# # Run TTS
# tts.tts_to_file(text="I used to be an adventurere like you, until I took an arrow to the knee.", file_path='output/output2.wav')
