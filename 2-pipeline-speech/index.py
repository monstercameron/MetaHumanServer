import speech_recognition as sr
import audioop
import wave

def listen_and_save_audio(file_path=None):
    # create a recognizer instance
    r = sr.Recognizer()

    # use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Say something!")
        r.adjust_for_ambient_noise(source)
        # listen for audio and store it in audio_data variable
        audio_data = r.listen(source)

        # set the volume threshold
        rms_threshold = audioop.rms(
            audio_data.frame_data, audio_data.sample_width) + 100

        # keep listening until the volume falls below the threshold
        while audioop.rms(audio_data.frame_data, audio_data.sample_width) > rms_threshold:
            print("Still listening...")
            audio_data = r.listen(source)

        # save the recorded audio to a WAV file
        if file_path is not None:
            with open(file_path, "wb") as f:
                f.write(audio_data.get_wav_data())
        else:
            audioBytes = audio_data.get_wav_data()
            with wave.open(audioBytes, mode='wb') as wave_file:
                wave_file.setnchannels(1)  # mono
                wave_file.setsampwidth(2)  # 16-bit
                wave_file.setframerate(44100)  # 44.1 kHz
                return wave_file.readframes(wave_file.getnframes())
    # print(f"Audio saved to {file_path}")
