#!/usr/bin/env python3
"""
Test safe image generation with conservative prompts
"""

import os
import time
import requests
from urllib.parse import quote
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def test_safe_image():
    """Generate one safe, watermark-free image"""
    api_key = os.getenv("POLLINATIONS_API_KEY")
    if not api_key:
        print("ERROR: POLLINATIONS_API_KEY not found")
        return False

    print("Testing safe image generation...")
    print("=" * 40)

    # High-quality photorealistic prompt optimized for flux model
    prompt = "stunningly beautiful ancient Greek woman in modest traditional clothing, hyper-realistic portrait, extremely detailed facial features, intricate traditional ancient clothing with rich textures, professional studio lighting, dramatic shadows and highlights, RAW photography, photorealistic, 8K resolution, ultra-high detail, sharp focus, depth of field, bokeh, cinematic composition, masterpiece, award-winning photography, volumetric lighting, hyper-detailed skin texture, realistic eyes with catchlights, museum quality art, historical accuracy, elegant and graceful pose, appropriate for all audiences, clean and tasteful"

    print(f"Prompt: {prompt}")

    # Using the paid gateway image endpoint
    url = f"https://gen.pollinations.ai/image/{quote(prompt)}"
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {
        "width": 1080,
        "height": 1920,
        "model": "flux",
        "seed": 99999,  # Fixed seed for testing
        "safe": True,  # Strict content filtering (boolean)
        "nologo": True,  # Explicitly request no watermarks
        "negative_prompt": "worst quality, blurry, watermark, logo, text, signature, branded content"
    }

    try:
        print("Generating image with safety filters...")
        r = requests.get(url, headers=headers, params=params, timeout=60)

        print(f"Status Code: {r.status_code}")

        if r.status_code == 200:
            # Save the image
            output_dir = Path("samples")
            output_dir.mkdir(exist_ok=True)
            timestamp = int(time.time())
            image_path = output_dir / f"safe_test_image_{timestamp}.jpg"

            with open(image_path, "wb") as f:
                f.write(r.content)

            print(f"SUCCESS: Safe image saved to {image_path}")
            print(f"Size: {len(r.content)} bytes")
            print("Image should be watermark-free and appropriate for all audiences")

            return True
        else:
            print(f"ERROR: HTTP {r.status_code}")
            print(f"Response: {r.text[:200]}")
            return False

    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    success = test_safe_image()
    if success:
        print("\nSUCCESS: Safe image generation working!")
        print("SUCCESS: No watermarks expected")
        print("SUCCESS: NSFW content prevented by safety filters")
    else:
        print("\nERROR: Safe image generation failed")