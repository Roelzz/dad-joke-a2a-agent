"""
Configuration helper for Dad Joke Agent
Loads BASE_URL from environment and generates endpoint URLs
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
PORT = int(os.getenv("PORT", 2009))
BASE_URL = os.getenv("BASE_URL", f"http://localhost:{PORT}")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def get_endpoint_urls():
    """Generate all endpoint URLs based on BASE_URL"""
    return {
        "base_url": BASE_URL,
        "messaging": f"{BASE_URL}/api/messages",
        "card": f"{BASE_URL}/api/card",
        "manifest": f"{BASE_URL}/api/manifest",
        "declarative": f"{BASE_URL}/api/declarative-agent",
        "discovery": f"{BASE_URL}/api/discovery",
        "well_known_card": f"{BASE_URL}/.well-known/agent-card.json",
        "well_known_discovery": f"{BASE_URL}/.well-known/agent-discovery.json",
        "icon": f"{BASE_URL}/icon.png",
    }


def update_json_urls(json_data: dict) -> dict:
    """
    Replace URL placeholders in JSON with actual BASE_URL
    Useful for dynamically serving manifest files
    """
    import json

    # Convert to string, replace placeholder, convert back
    json_str = json.dumps(json_data)
    json_str = json_str.replace("{BASE_URL}", BASE_URL)
    return json.loads(json_str)
