#!/usr/bin/env python3
"""
Test script for Pollinations AI paid API integration.
Run this locally to test if your API key is working correctly.
"""

import os
import sys
from urllib.parse import quote
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def test_text_generation():
    """Test the text generation API."""
    api_key = os.getenv("POLLINATIONS_API_KEY")
    if not api_key:
        print("ERROR: POLLINATIONS_API_KEY environment variable not set!")
        print("Please set it with: export POLLINATIONS_API_KEY='your_api_key_here'")
        return False

    print("API Key found, testing text generation...")

    # Test prompt
    prompt = "Merhaba, nasılsın?"
    system = "Sen yardımcı bir asistansın. Türkçe cevap ver."

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
        "temperature": 0.7
    }

    try:
        print(f"Sending request to: {url}")
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        r.raise_for_status()

        response_json = r.json()
        response = response_json['choices'][0]['message']['content'].strip()
        print("API Response:")
        print(response)

        # Check if response is different from prompt (indicates actual generation)
        if response != prompt:
            print("SUCCESS: Text generation working! Response is different from prompt.")
            return True
        else:
            print("WARNING: Response is same as prompt - this might indicate an issue.")
            return False

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code}")
        print(f"Response: {e.response.text}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_balance():
    """Test API key balance."""
    api_key = os.getenv("POLLINATIONS_API_KEY")
    if not api_key:
        return False

    print("\nTesting API balance...")

    try:
        url = "https://gen.pollinations.ai/account/balance"
        headers = {"Authorization": f"Bearer {api_key}"}

        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()

        balance = r.json()
        print(f"Current balance: {balance.get('balance', 'Unknown')} pollen")
        return True

    except Exception as e:
        print(f"Balance check failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Pollinations AI Paid API Integration")
    print("=" * 50)

    balance_ok = test_balance()
    text_ok = test_text_generation()

    print("\n" + "=" * 50)
    if balance_ok and text_ok:
        print("SUCCESS: All tests passed! Your API integration is working correctly.")
        sys.exit(0)
    else:
        print("ERROR: Some tests failed. Please check your API key and try again.")
        sys.exit(1)