#!/usr/bin/env python3
"""
Generate sample text and images using Pollinations AI
"""

import os
import requests
from urllib.parse import quote
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def generate_sample_text():
    """Generate a sample Turkish story about ancient women's history"""
    api_key = os.getenv("POLLINATIONS_API_KEY")
    if not api_key:
        print("ERROR: POLLINATIONS_API_KEY not found in .env file")
        return None

    print("Generating Sample Text (Turkish Story)")
    print("=" * 50)

    # Turkish system prompt for ancient women's history
    system = (
        "Sen antik medeniyetlerde kadınların tarihi konusunda uzmanlaşmış bir tarihçisin. "
        "30 saniye sürecek kısa ve ilginç bir hikaye yaz (80-130 kelime) Türkçe dilinde. "
        "Gerçek tarihi olaylar, yasalar, gelenekler veya adetler hakkında anlat. "
        "Canlı ve ilgi çekici bir üslup kullan. Başlık kullanma."
    )

    prompt = "Konu: Antik Yunan'da kadınların miras hakları. İlginç bir tarihi gerçek anlat."

    url = f"https://gen.pollinations.ai/text/{quote(prompt)}"
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {
        "model": "nova-fast",
        "temperature": 1.0,
        "system": system,
        "json": False
    }

    try:
        r = requests.get(url, headers=headers, params=params, timeout=30)
        r.raise_for_status()

        text = r.text.strip()
        print(f"SUCCESS: Generated Turkish text ({len(text.split())} words)")
        print("Text contains Turkish characters - saved to file (check samples/sample_story.txt)")

        # Save to file
        output_dir = Path("samples")
        output_dir.mkdir(exist_ok=True)
        with open(output_dir / "sample_story.txt", "w", encoding="utf-8") as f:
            f.write(text)

        print(f"Saved to: samples/sample_story.txt")
        return text

    except Exception as e:
        print(f"Error generating text: {e}")
        return None

def generate_sample_images(story_text):
    """Generate sample images based on the story"""
    print("\nGenerating Sample Images")
    print("=" * 50)

    # Extract key scenes from the story (simple approach)
    sentences = story_text.split('.')[:3]  # First 3 sentences
    scenes = [s.strip() for s in sentences if s.strip()][:3]

    if len(scenes) < 3:
        # Fallback scenes if story is short
        scenes = [
            "beautiful ancient Greek woman in traditional clothing",
            "women gathering in ancient marketplace",
            "historical scene from ancient Athens"
        ]

    output_dir = Path("samples")
    output_dir.mkdir(exist_ok=True)

    images = []
    for i, scene in enumerate(scenes):
        print(f"Generating image {i+1}/3...")
        # Don't print the Turkish text to avoid encoding issues

        # Create detailed prompt for image generation
        prompt = f"stunning beautiful woman in ancient Greece, {scene}, photorealistic portrait, elegant ancient Greek clothing, dramatic cinematic lighting, highly detailed face and eyes, historical accuracy, professional photography, 8k quality, masterpiece, beautiful composition, vibrant colors, sharp focus"

        url = f"https://image.pollinations.ai/prompt/{quote(prompt)}"
        params = {
            "width": 1080,
            "height": 1920,  # Vertical for YouTube Shorts
            "model": "flux",
            "seed": 12345 + i  # Different seed for each image
        }

        try:
            r = requests.get(url, params=params, timeout=60)
            r.raise_for_status()

            image_path = output_dir / f"sample_scene_{i+1:02d}.jpg"
            with open(image_path, "wb") as f:
                f.write(r.content)

            print(f"SUCCESS: Saved: {image_path} ({len(r.content)} bytes)")
            images.append(image_path)

        except Exception as e:
            print(f"ERROR: generating image {i+1}: {e}")

    return images

if __name__ == "__main__":
    print("Pollinations AI - Sample Text & Image Generation")
    print("=" * 60)

    # Generate sample text
    story = generate_sample_text()

    if story:
        # Generate sample images based on the story
        images = generate_sample_images(story)

        print("\nSAMPLE GENERATION COMPLETE!")
        print(f"Story: samples/sample_story.txt")
        print(f"Images: {len(images)} generated in samples/ folder")

        if images:
            print("\nSample images:")
            for img in images:
                print(f"  - {img}")

    else:
        print("ERROR: Failed to generate story. Check your API key.")