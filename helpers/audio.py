import wave
import sounddevice as sd
import soundfile as sf
import threading


class AudioPlayer:
    def __init__(self):
        self.stop_flag = False
        self.playback_thread = None

    def play_audio_file_sync(self, filename):
        # Read the WAV file
        data, fs = sf.read(filename)

        # Play the WAV file synchronously
        sd.play(data, fs)
        sd.wait()

    def play_audio_file_async(self, filename):
        self.stop_flag = False

        # Read the WAV file
        data, fs = sf.read(filename)

        # Play the WAV file in a separate thread
        def play_thread():
            sd.play(data, fs)
            sd.wait()
            self.stop_flag = True

        # Start the playback thread
        self.playback_thread = threading.Thread(target=play_thread)
        self.playback_thread.start()

    def stop_playback(self):
        self.stop_flag = True
        if self.playback_thread:
            self.playback_thread.join()
            self.playback_thread = None

    def __del__(self):
        self.stop_playback()


if __name__ == "__main__":
    filename = 'D:/repos/metahumanserver/samples/output.wav'

    # Create an instance of AudioPlayer
    player = AudioPlayer()

    # Synchronous playback
    player.play_audio_file_sync(filename)

    # Asynchronous playback
    player.play_audio_file_async(filename)

    # Stop the playback
    player.stop_playback()
