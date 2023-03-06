import os
from TTS.api import TTS
from dotenv import load_dotenv

load_dotenv()
OUTPUT = os.getenv("OUTPUT")


def generate_audio(prompt):
    # Running a multi-speaker and multi-lingual model
    tts = TTS(model_name='tts_models/en/vctk/vits',
              progress_bar=True, gpu=True)

    # Text to speech to a file
    tts.tts_to_file(text=prompt,
                    speaker=tts.speakers[0], file_path=f"{OUTPUT}/output.wav")
    return f"{OUTPUT}/output.wav"
