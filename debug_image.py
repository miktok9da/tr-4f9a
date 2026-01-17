#!/usr/bin/env python3
import requests
from urllib.parse import quote
from pathlib import Path

print("Testing image generation...")

prompt = "beautiful ancient Egyptian woman, Cleopatra, detailed portrait, historical clothing"

url = f"https://image.pollinations.ai/prompt/{quote(prompt)}"
params = {
    "width": 1024,
    "height": 1024,
    "model": "flux",
    "seed": 42
}

print(f"URL: {url}")
print(f"Params: {params}")

try:
    r = requests.get(url, params=params, timeout=60)
    print(f"Status code: {r.status_code}")
    print(f"Response headers: {dict(r.headers)}")

    if r.status_code == 200:
        # Save image
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        image_path = output_dir / "test_image.jpg"

        print(f"Saving to: {image_path.absolute()}")

        with open(image_path, "wb") as f:
            f.write(r.content)

        print(f"SUCCESS: Image saved! Size: {len(r.content)} bytes")
        print(f"File exists: {image_path.exists()}")

    else:
        print(f"ERROR: HTTP {r.status_code}")
        print(f"Response: {r.text[:200]}")

except Exception as e:
    print(f"ERROR: {e}")