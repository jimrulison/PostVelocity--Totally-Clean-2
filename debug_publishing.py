#!/usr/bin/env python3
"""
Simple OAuth Publishing Test Debug
"""

import requests
import json

def test_publishing_debug():
    base_url = "https://3c895907-57fe-4e13-8514-beec8ca83a66.preview.emergentagent.com"
    user_id = "60d5ec49f1b2c8e1a4567890"
    
    platforms = ["instagram", "facebook", "linkedin", "x"]
    
    for platform in platforms:
        print(f"\nTesting {platform}...")
        
        url = f"{base_url}/api/content/publish/{platform}"
        data = {
            "content": "Test post for OAuth integration testing",
            "user_id": user_id,
            "media_urls": ["https://example.com/test-image.jpg"]
        }
        headers = {'Content-Type': 'application/json'}
        
        try:
            response = requests.post(url, json=data, headers=headers, timeout=30)
            print(f"  Status Code: {response.status_code}")
            print(f"  Response: {response.text}")
            
            if response.status_code == 401:
                print(f"  ✅ {platform.upper()} - Authentication required (as expected)")
            elif response.status_code == 200:
                print(f"  ✅ {platform.upper()} - Success response")
            else:
                print(f"  ❌ {platform.upper()} - Unexpected status: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ {platform.upper()} - Error: {e}")

if __name__ == "__main__":
    test_publishing_debug()