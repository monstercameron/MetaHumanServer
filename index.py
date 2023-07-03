import os
from dotenv import load_dotenv
from helpers.audio import AudioPlayer
from step_1_wakeword.index import detect_hotword
from step_2_audio_recording.index import listen_and_save_audio
from step_3_stt.index import transcribe, load_model as load_model_stt
from step_4_chatbot.index import ChatGPT
from step_5_tts_fast.index import generate_audio, load_model as load_model_tts
from step_7_image_generation.index import generate_image
from helpers.system import insert_app

load_dotenv()


class ChatApp:
    def __init__(self):
        self.OUTPUT = os.getenv("OUTPUT")
        self.model = os.getenv("MODEL")
        self.aiRole = os.getenv("AIROLE")
        self.userRole = os.getenv("USERROLE")
        self.initialize_app()

    def initialize_app(self):
        device = os.getenv("STTDEVICE")
        self.stt = load_model_stt(device)
        device = os.getenv("TTSDEVICE")
        self.tts = load_model_tts(device)
        self.audio_player = AudioPlayer()
        self.chat = ChatGPT(self.model, self.aiRole, self.userRole)

    def process_context(self):
        if self.context == "porcupine":
            print("Resetting ChatGPT History")
            self.chat.reset_history()
            return False
        elif self.context == "americano":
            return False
        else:
            self.audio_player.play_audio_file_sync("resources/notif1.wav")
            return True

    def record_audio(self):
        file_path = f"{self.OUTPUT}/recording.wav"
        listen_and_save_audio(file_path)
        return file_path

    def convert_audio_to_text(self, file_path):
        return transcribe(file_path=file_path, model=self.stt)

    def get_chat_response(self, prompt):
        print(f'{self.chat.user_role}:{prompt}')
        response = self.chat.next(prompt)
        print(f'{self.chat.ai_role}: {response}')
        return response

    def play_audio_response(self, response):
        filePath = generate_audio(
            prompt=response, output_path=self.OUTPUT, model=self.tts)
        self.player = self.audio_player.play_audio_file_async(filePath)

    def main(self, context):
        self.context = context

        if not self.process_context():
            self.chatInProgress = False
            return

        file_path = self.record_audio()
        prompt = self.convert_audio_to_text(file_path)
        response = self.get_chat_response(prompt)
        self.play_audio_response(response)

    def listen_for_wake_word(self):
        print("Computer is listening, try 'Computer' to make a prompt or 'porcupine' to start a new conversation")
        detect_hotword(self.main)

    def run(self):
        self.listen_for_wake_word()


if __name__ == "__main__":
    app = ChatApp()
    app.run()
