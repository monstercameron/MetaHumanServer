from step_7_image_generation.index import generate_image
from step_5_tts_slow.index import generate_audio as generate_audio_v2
from step_5_tts_fast.index import generate_audio, load_model as load_model_tts
from step_4_chatbot.index import ChatGPT
from step_3_stt.index import transcribe, load_model as load_model_stt
from step_2_audio_recording.index import listen_and_save_audio
from step_1_wakeword.index import detect_hotword
from importlib.machinery import SourceFileLoader
import os
import threading
import importlib.machinery
import time
from dotenv import load_dotenv
from helpers.audio import play_audio_file, play_audio_fileV3
# from server.index import app

# Load the environment variables from the .env file
load_dotenv()

OUTPUT = os.getenv("OUTPUT")
model = os.getenv("MODEL")
aiRole = os.getenv("AIROLE")
userRole = os.getenv("USERROLE")

# Create ChatGPT instance
chatGPT = ChatGPT(model, aiRole, userRole)

# Models
models = {}

chatInProgress = False


def load_models():
    device = os.getenv("STTDEVICE")
    models['stt'] = load_model_stt(device)
    device = os.getenv("TTSDEVICE")
    models['tts'] = load_model_tts(device)


# main function
def main(context):
    # getting the context of the wake word
    # prevent running simultaneously
    global chatInProgress
    if chatInProgress:
        return
    else:
        chatInProgress = True

    # needs custom models for other non-standard wake words
    if context == "porcupine":
        print("Resetting ChatGPT History")
        chatGPT.reset_history()
    elif context == "americano":
        pass
    else:
        # play audio buzz to show that the computer is listening after wakeword
        play_audio_file("resources/notif1.wav")

        # step 2 record audio and end when stop speaking
        file_path = f"{OUTPUT}/recording.wav"
        listen_and_save_audio(file_path)
        # audio = listen_and_save_audio()

        # step 3 speech to text
        prompt = transcribe(file_path=file_path, model=models['stt'])
        # prompt = transcribe(wav_data=audio)
        # global app
        # app.message_history = chatGPT.history
        message_history = chatGPT.history

        # step 4 prompt chatGPT
        print(f'{chatGPT.user_role}:{prompt}')
        response = chatGPT.next(prompt)
        print(f'{chatGPT.ai_role}: {response}')
        # app.message_history = chatGPT.history

        # step 5 generate speech to text
        filePath = generate_audio(
            prompt=response, output_path=OUTPUT, model=models["tts"])
        # filePath = generate_audio_v2(response, cuda_device=2)
        # play_audio_file(filePath)
        play_audio_fileV3(filePath)

        # allow new prompts
        chatInProgress = False

    # play audio buzz to show that the computer is ready to start listening
    play_audio_file("resources/notif2.wav")

    # step 7
    # prompt = "a photo of an astronaut riding a horse on mars"
    # filename = "test.png"
    # generate_image(prompt, OUTPUT, filename)


def listenForWakeWord():
    # Perform other tasks in the main thread
    print("Computer is listening, try 'Computer' to make a prompt or 'porcupine' to start a new conversation")
    detect_hotword(main)


if __name__ == "__main__":
    # Start Flask app in a new thread
    # wakeWord = threading.Thread(target=listenForWakeWord)
    # wakeWord.start()
    # main('')
    load_models()
    listenForWakeWord()

    # app.run(debug=True)
