from picovoice import Picovoice


def wake_word_callback():
    # wake word detected
    print("test")
    pass


def inference_callback(inference):
    if inference.is_understood:
        intent = inference.intent
        slots = inference.slots
        # take action based on intent and slot values
    else:
        # unsupported command
        pass


handle = Picovoice(
    access_key=${ACCESS_KEY},
    keyword_path=${KEYWORD_FILE_PATH},
    wake_word_callback=wake_word_callback,
    context_path=${CONTEXT_FILE_PATH},
    inference_callback=inference_callback)


def get_next_audio_frame():
    pass


while True:
    audio_frame = get_next_audio_frame()
    handle.process(audio_frame)

handle.delete()
