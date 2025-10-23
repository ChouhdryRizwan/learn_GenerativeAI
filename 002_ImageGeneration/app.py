import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from PIL import Image
import io

# Load variables from .env file
load_dotenv()

# Initialize Hugging Face Inference Client
hf_api_token = os.getenv("HUGGINGFACE_API_TOKEN")

client = InferenceClient(api_key=hf_api_token)

# Define the text prompt for image generation
prompt = "A futuristic cityscape at sunset, cyberpunk style, highly detailed"

# Generate image using Stable Diffusion XL
image = client.text_to_image(
    model="stabilityai/stable-diffusion-xl-base-1.0",
    prompt=prompt,
    negative_prompt="blurry, low quality, text, watermark",
    num_inference_steps=30, # Increased for better quality
    guidance_scale=7.5, # Stronger prompt adherence
)

# Save the generated image
image.save("generated_image.png")
print("Image saved as 'generated_image.png'")
    

