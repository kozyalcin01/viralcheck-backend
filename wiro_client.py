# wiro_client.py
import requests
import time
import hashlib
import hmac
import json
from dotenv import load_dotenv
import os

# .env dosyasını yükle
load_dotenv()

API_KEY = os.getenv("WIRO_API_KEY")
API_SECRET = os.getenv("WIRO_API_SECRET")
API_URL = "https://api.wiro.ai/v1/Run/wiro/ask-video"


def _generate_headers():
    nonce = str(int(time.time()))
    signature = hmac.new(
        API_KEY.encode(),
        f"{API_SECRET}{nonce}".encode(),
        hashlib.sha256
    ).hexdigest()
    return {
        "x-api-key": API_KEY,
        "x-nonce": nonce,
        "x-signature": signature,
        "Content-Type": "application/json",
    }


def analyze_video(video_url: str):
    """Wiro Ask-Video API üzerinden video analizi"""
    payload = {
        "input-video-url": video_url,
        "prompt": "Describe this video in detail."
    }

    headers = _generate_headers()
    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))

    if response.status_code != 200:
        return {"error": f"Request failed: {response.status_code}", "details": response.text}

    return response.json()
