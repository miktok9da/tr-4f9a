#!/usr/bin/env python3
"""
Test different approaches for paid image API
"""

import os
import requests
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("POLLINATIONS_API_KEY")
prompt = "beautiful ancient Greek woman"

print("Testing different paid image API approaches...")
print(f"API Key: {api_key[:10]}...")
print()

# Test 1: POST to /v1/images/generations (OpenAI-style)
print("Test 1: OpenAI-style endpoint")
try:
    url = "https://gen.pollinations.ai/v1/images/generations"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "model": "flux",
        "size": "1024x1024",
        "n": 1
    }
    r = requests.post(url, headers=headers, json=data, timeout=30)
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        print("SUCCESS!")
        print(r.json())
    else:
        print(f"Response: {r.text[:200]}")
except Exception as e:
    print(f"Error: {e}")

print()

# Test 2: GET with auth header
print("Test 2: GET with auth header")
try:
    url = f"https://gen.pollinations.ai/image/{quote(prompt)}"
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {"model": "flux", "width": 1024, "height": 1024}
    r = requests.get(url, headers=headers, params=params, timeout=30)
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        print("SUCCESS!")
        print(f"Content-Type: {r.headers.get('content-type')}")
        print(f"Size: {len(r.content)} bytes")
    else:
        print(f"Response: {r.text[:200]}")
except Exception as e:
    print(f"Error: {e}")

print()

# Test 3: GET with key as query param
print("Test 3: GET with key as query param")
try:
    url = f"https://gen.pollinations.ai/image/{quote(prompt)}"
    params = {"model": "flux", "width": 1024, "height": 1024, "key": api_key}
    r = requests.get(url, params=params, timeout=30)
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        print("SUCCESS!")
        print(f"Content-Type: {r.headers.get('content-type')}")
        print(f"Size: {len(r.content)} bytes")
    else:
        print(f"Response: {r.text[:200]}")
except Exception as e:
    print(f"Error: {e}")