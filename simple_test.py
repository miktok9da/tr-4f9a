#!/usr/bin/env python3
"""
Simple test to generate text and images using Pollinations AI
"""

import os
import requests
from urllib.parse import quote
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_text_generation():
    """Test text generation with Amazon Nova Micro"""
    api_key = os.getenv("POLLINATIONS_API_KEY")
    if not api_key:
        print("ERROR: No API key found")
        return False

    print("Testing text generation...")

    system = "You are a helpful assistant. Write a short story about ancient women."
    prompt = "Tell me about Cleopatra and her role in history"

    url = "https://gen.pollinations.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "openai",
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.8
    }

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        r.raise_for_status()
        
        response_json = r.json()
        response = response_json['choices'][0]['message']['content'].strip()
        print("SUCCESS: Text generated!")
        print(f"Length: {len(response)} characters")
        print("First 200 characters:")
        print(response[:200] + "...")

        # Save to file
        with open("output/story_test.txt", "w", encoding="utf-8") as f:
            f.write(response)
        print("Saved to output/story_test.txt")

        return True

    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_image_generation():
    """Test image generation"""
    api_key = os.getenv("POLLINATIONS_API_KEY")
    if not api_key:
        print("ERROR: No API key found")
        return False

    print("\nTesting image generation...")

    prompt = "beautiful ancient Egyptian woman, Cleopatra, detailed portrait, historical clothing"

    url = f"https://gen.pollinations.ai/image/{quote(prompt)}"
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {
        "width": 1024,
        "height": 1024,
        "model": "flux",
        "seed": 42
    }

    try:
        r = requests.get(url, headers=headers, params=params, timeout=60)
        r.raise_for_status()

        # Save image
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        image_path = output_dir / "test_image.jpg"

        with open(image_path, "wb") as f:
            f.write(r.content)

        print("SUCCESS: Image generated!")
        print(f"Saved to {image_path}")
        print(f"Size: {len(r.content)} bytes")

        return True

    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    print("Testing Pollinations AI Integration")
    print("=" * 40)

    # Create output directory
    Path("output").mkdir(exist_ok=True)

    # Test text generation
    text_ok = test_text_generation()

    # Test image generation
    image_ok = test_image_generation()

    print("\n" + "=" * 40)
    if text_ok and image_ok:
        print("SUCCESS: All tests passed!")
    else:
        print("Some tests failed - check your API key and connection")