#!/usr/bin/env python3
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Check if API key is loaded
api_key = os.getenv('POLLINATIONS_API_KEY')
if api_key:
    print("API Key found in .env file")
    print("Key starts with:", api_key[:10] + "...")
    print("Key length:", len(api_key))
else:
    print("NO API Key found in .env file")
    print("Please check your .env file")