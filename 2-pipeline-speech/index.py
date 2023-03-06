import speech_recognition as sr
import audioop


def listen_and_save_audio(file_path):
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
        with open(file_path, "wb") as f:
            f.write(audio_data.get_wav_data())

    # print(f"Audio saved to {file_path}")
