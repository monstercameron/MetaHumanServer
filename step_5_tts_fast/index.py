import os
import torch
from TTS.api import TTS
from helpers.system import track_time


@track_time
def load_model(cuda_device):
    """
    Load the TTS model on the specified CUDA device.

    Args:
        cuda_device (str): The CUDA device to use.

    Returns:
        TTS: Loaded TTS model.
    """
    # Set the CUDA visible device
    torch.cuda.set_device(cuda_device)

    # Running a multi-speaker and multi-lingual model
    tts = TTS(model_name='tts_models/en/vctk/vits',
              progress_bar=False, gpu=True, )
    return tts


def generate_audio(prompt, output_path, model):
    """
    Generate audio file from the given text prompt using the provided TTS model.

    Args:
        prompt (str): Text prompt for generating audio.
        output_path (str): Path to save the generated audio file.
        model (TTS): Loaded TTS model.

    Returns:
        str: File path of the generated audio file.
    """
    file_path = os.path.join(output_path, "output.wav")
    # Text to speech to a file
    model.tts_to_file(text=prompt,
                      speaker=model.speakers[0], file_path=file_path)
    return file_path
