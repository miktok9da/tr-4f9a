#!/usr/bin/env python3
"""
Generate sample images for demonstration using paid Pollinations API
"""

import os
import time
import requests
from urllib.parse import quote
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def generate_sample_images():
    """Generate 3 sample images of ancient women using paid Pollinations API"""
    api_key = os.getenv("POLLINATIONS_API_KEY")
    if not api_key:
        print("ERROR: POLLINATIONS_API_KEY not found in .env file")
        return []

    print("Generating Sample Images (Paid API)")
    print("=" * 40)

    # Simple prompts for images
    prompts = [
        "beautiful ancient Greek woman in traditional clothing, detailed portrait",
        "stunning ancient Egyptian woman, Cleopatra style, elegant",
        "beautiful ancient Roman woman, historical clothing, portrait"
    ]

    output_dir = Path("samples")
    output_dir.mkdir(exist_ok=True)

    # Add timestamp to make filenames unique for each run
    timestamp = int(time.time())

    images = []
    for i, prompt in enumerate(prompts):
        print(f"Generating image {i+1}/3...")

        # High-quality photorealistic prompt optimized for flux model
        full_prompt = f"{prompt}, hyper-realistic portrait, extremely detailed facial features, intricate traditional ancient clothing with rich textures, professional studio lighting, dramatic shadows and highlights, RAW photography, photorealistic, 8K resolution, ultra-high detail, sharp focus, depth of field, bokeh, cinematic composition, masterpiece, award-winning photography, volumetric lighting, hyper-detailed skin texture, realistic eyes with catchlights, museum quality art, historical accuracy, elegant and graceful pose, appropriate for all audiences, clean and tasteful"

        # Using the working configuration - check if images have watermarks
        url = f"https://image.pollinations.ai/prompt/{quote(full_prompt)}"
        headers = {"Authorization": f"Bearer {api_key}"}  # Add auth header
        params = {
            "width": 1080,
            "height": 1920,  # Vertical for YouTube Shorts
            "model": "flux",  # Use flux model
            "seed": 12345 + i,
            "safe": True,  # Enable content filtering to prevent NSFW (boolean)
            "nologo": True,  # Explicitly request no watermarks
            "negative_prompt": "worst quality, blurry, watermark, logo, text, signature, branded content"
        }

        try:
            r = requests.get(url, headers=headers, params=params, timeout=60)
            r.raise_for_status()

            image_path = output_dir / f"sample_image_paid_{timestamp}_{i+1:02d}.jpg"
            with open(image_path, "wb") as f:
                f.write(r.content)

            print(f"SUCCESS: Saved {image_path} ({len(r.content)} bytes)")
            images.append(image_path)

        except Exception as e:
            print(f"ERROR generating image {i+1}: {e}")

    return images

if __name__ == "__main__":
    images = generate_sample_images()

    print("\nCOMPLETE!")
    print(f"Generated {len(images)} sample images in samples/ folder")

    for img in images:
        print(f"  - {img}")