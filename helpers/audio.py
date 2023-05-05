import pyaudio
import wave
from playsound import playsound
import sounddevice as sd
import soundfile as sf


def play_audio_file(filename):
    # Load the WAV file
    with wave.open(filename, 'rb') as wave_file:
        # Initialize the PyAudio library
        audio = pyaudio.PyAudio()

        # Open a stream to play the audio
        stream = audio.open(format=audio.get_format_from_width(wave_file.getsampwidth()),
                            channels=wave_file.getnchannels(),
                            rate=wave_file.getframerate(),
                            output=True)

        # Read the audio data and play it in chunks
        chunk_size = 1024
        data = wave_file.readframes(chunk_size)
        while data:
            stream.write(data)
            data = wave_file.readframes(chunk_size)

        # Stop and close the audio stream and PyAudio library
        stream.stop_stream()
        stream.close()
        audio.terminate()


def play_audio_fileV2(filename):
    playsound(filename)


def play_audio_fileV3(filename):
    # read the WAV file
    data, fs = sf.read(filename)

    # play the WAV file
    sd.play(data, fs)

    # wait for the audio to finish playing
    sd.wait()


if __name__ == "__main__":
    play_audio_fileV3('D:/repos/metahumanserver/samples/output.wav')
