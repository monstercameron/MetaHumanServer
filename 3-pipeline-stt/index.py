import os
import ffmpeg
import whisper


def transcribe(file_path):
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

    # Transcribe the audio file using the Whisper library
    result = model.transcribe(file_path)

    # Return the transcribed text
    return result["text"]
