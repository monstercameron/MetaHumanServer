import os
import importlib.machinery
from dotenv import load_dotenv
from helpers.audio import play_audio_file

# Step 1: Listen for wake word
from importlib.machinery import SourceFileLoader

wake_word_module = '1-pipeline-wakeword.index'
wake_word_path = './1-pipeline-wakeword'
wake_word = SourceFileLoader(
    wake_word_module, wake_word_path + '/index.py').load_module()
detect_hotword = wake_word.detect_hotword

# Step 2: Listen and save audio
speech_module = '2-pipeline-speech.index'
speech_path = './2-pipeline-speech'
speech = SourceFileLoader(
    speech_module, speech_path + '/index.py').load_module()
listen_and_save_audio = speech.listen_and_save_audio

# Step 3: Transcribe audio to text
stt_module = '3-pipeline-stt.index'
stt_path = './3-pipeline-stt'
stt = SourceFileLoader(stt_module, stt_path + '/index.py').load_module()
transcribe = stt.transcribe

# Step 4: Prompt ChatGPT
chatgpt_module = '4-pipeline-chatGPT.index'
chatgpt_path = './4-pipeline-chatGPT'
chatgpt = SourceFileLoader(
    chatgpt_module, chatgpt_path + '/index.py').load_module()

# step 5 prompt to speech
tts_module = '5-pipeline-tts.index'
tts_path = './5-pipeline-tts'
tts_loader = SourceFileLoader(tts_module, tts_path + '/index.py')
tts = tts_loader.load_module()
generate_audio = tts.generate_audio

# Step 7: Generate image
stable_diffusion_module = '7-stablediffusion.index'
stable_diffusion_path = './7-stablediffusion'
stable_diffusion = SourceFileLoader(
    stable_diffusion_module, stable_diffusion_path + '/index.py').load_module()
generate_image = stable_diffusion.generate_image

# Load the environment variables from the .env file
load_dotenv()
OUTPUT = os.getenv("OUTPUT")

model = "gpt-3.5-turbo"
aiRole = "assistant"
userRole = "user"
chatGPT = chatgpt.ChatGPT(model, aiRole, userRole)
print('Initializing chatGPT')
print("Setting up AI personality")


# main function
def main(context):
    # getting the context of the wake word
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

        # step 3 speech to text
        prompt = transcribe(file_path)

        # step 4 prompt chatGPT
        print(f'{chatGPT.user_role}:{prompt}')
        response = chatGPT.next(prompt)
        print(f'{chatGPT.ai_role}: {response}')

        # step 5 generate speech to text
        filePath = generate_audio(response)
        play_audio_file(filePath)

    # play audio buzz to show that the computer is ready to start listening
    play_audio_file("resources/notif2.wav")

    # step 7
    # prompt = "a photo of an astronaut riding a horse on mars"
    # filename = "test.png"
    # generate_image(prompt, OUTPUT, filename)


if __name__ == "__main__":
    # step 1 listen for wake word
    print("Computer is listening, try 'Computer' to make a prompt or 'porcupine' to start a new conversation")
    detect_hotword(main)
