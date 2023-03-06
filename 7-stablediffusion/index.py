import os
import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler

def generate_image(prompt, output_path, filename):
    model_id = "stabilityai/stable-diffusion-2-1"

    # Use the DPMSolverMultistepScheduler (DPM-Solver++) scheduler here instead
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    if not pipe:
        raise ValueError(f"Failed to load model {model_id}")
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    pipe = pipe.to("cuda")

    image = pipe(prompt).images[0]
    if not image:
        raise ValueError("Failed to generate image")

    if not os.path.exists(output_path):
        os.makedirs(output_path)
    image_path = os.path.join(output_path, filename)
    image.save(image_path)