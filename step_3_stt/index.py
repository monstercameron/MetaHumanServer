import os
import ffmpeg
import whisper
from helpers.system import track_time


import os
import time
import whisper
from dotenv import load_dotenv

load_dotenv()


@track_time
def load_model(cuda_device):
    """
    Load the Whisper model and move it to the specified CUDA device.

    Args:
        cuda_device (str): The CUDA device to use.

    Returns:
        model: Loaded Whisper model.
    """
    start_time = time.time()

    model = whisper.load_model("base")
    model.encoder.to(cuda_device)
    model.decoder.to(cuda_device)

    return model


def transcribe(file_path=None, wav_data=None, model=None):
    """
    Transcribe audio using the provided Whisper model.

    Args:
        file_path (str): Path to the audio file.
        wav_data (str): Audio data in WAV format.
        model: Loaded Whisper model.

    Returns:
        str: Transcribed text.
    """
    result = None

    # Transcribe the audio file using the provided model reference
    if file_path is not None:
        result = model.transcribe(file_path)

    if wav_data is not None:
        result = model.transcribe(wav_data)

    # Return the transcribed text
    return result["text"]
