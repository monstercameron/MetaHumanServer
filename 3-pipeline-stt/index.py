import os
import ffmpeg
import whisper


def transcribe(file_path=None, wav_data=None):
    # Check if the specified file exists
    # if os.path.exists(file_path):
    #     print("File exists")
    # else:
    #     print("File does not exist")
    #     return ""

    # Load the Whisper model and move it to the GPU
    model = whisper.load_model("base")
    model.encoder.to("cuda:0")
    model.decoder.to("cuda:0")

    result = None

    # Transcribe the audio file using the Whisper library
    if file_path is not None:
        result = model.transcribe(file_path)

    if wav_data is not None:
        result = model.transcribe(wav_data)

    # Return the transcribed text
    return result["text"]
