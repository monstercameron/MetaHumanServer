import os
import imp
from dotenv import load_dotenv

module_name = '7-stablediffusion.index'
module_path = './7-stablediffusion'

module = imp.load_source(module_name, module_path + '/index.py')
generate_image = module.generate_image

# Load the environment variables from the .env file
load_dotenv()

prompt = "a photo of an astronaut riding a horse on mars"
OUTPUT = os.getenv("OUTPUT")
filename = "test.png"

generate_image(prompt, OUTPUT, filename)
