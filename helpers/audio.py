import pyaudio
import wave


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
