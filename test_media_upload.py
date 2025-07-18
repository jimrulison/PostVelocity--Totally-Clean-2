#!/usr/bin/env python3
"""
Test script to demonstrate media upload functionality
"""

import requests
import json
from PIL import Image
import io
import os

def create_test_image():
    """Create a simple test image"""
    img = Image.new('RGB', (800, 600), color='blue')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes

def test_media_upload():
    """Test media upload functionality"""
    base_url = "http://localhost:8001"
    company_id = "6879923419b52b3e5b36c36f"  # SafetyFirst Environmental Training
    
    # Create a test image
    test_image = create_test_image()
    
    # Upload media file
    files = {
        'file': ('safety_training.png', test_image, 'image/png')
    }
    
    data = {
        'category': 'training',
        'description': 'Safety training demonstration photo',
        'tags': 'safety, training, PPE, demonstration'
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/companies/{company_id}/media/upload",
            files=files,
            data=data
        )
        
        if response.status_code == 200:
            print("✅ Media upload successful!")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ Media upload failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error during upload: {e}")
        return False

def test_media_retrieval():
    """Test media retrieval"""
    base_url = "http://localhost:8001"
    company_id = "6879923419b52b3e5b36c36f"
    
    try:
        response = requests.get(f"{base_url}/api/companies/{company_id}/media")
        
        if response.status_code == 200:
            media_files = response.json()
            print(f"✅ Retrieved {len(media_files)} media files")
            for media in media_files:
                print(f"  - {media['filename']} ({media['category']}) - {media['description']}")
            return True
        else:
            print(f"❌ Media retrieval failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error during retrieval: {e}")
        return False

def test_content_generation_with_media():
    """Test content generation with media"""
    base_url = "http://localhost:8001"
    company_id = "6879923419b52b3e5b36c36f"
    
    content_request = {
        "company_id": company_id,
        "topic": "Safety Equipment Training",
        "platforms": ["instagram", "facebook"],
        "audience_level": "general",
        "additional_context": "Focus on proper PPE usage and training",
        "use_company_media": True
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/generate-content",
            json=content_request
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Content generation with media successful!")
            print(f"Generated content for {len(result['generated_content'])} platforms")
            print(f"Media used: {len(result['media_used'])} files")
            print(f"Media suggestions: {len(result['media_suggestions'])} suggestions")
            
            # Show media suggestions
            if result['media_suggestions']:
                print("\nMedia Suggestions:")
                for suggestion in result['media_suggestions']:
                    print(f"  - {suggestion}")
            
            return True
        else:
            print(f"❌ Content generation failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error during content generation: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Testing Media Management System")
    print("=" * 50)
    
    # Test 1: Upload media
    print("\n1. Testing Media Upload...")
    upload_success = test_media_upload()
    
    # Test 2: Retrieve media
    print("\n2. Testing Media Retrieval...")
    retrieval_success = test_media_retrieval()
    
    # Test 3: Content generation with media
    print("\n3. Testing Content Generation with Media...")
    content_success = test_content_generation_with_media()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print(f"Media Upload: {'✅ PASSED' if upload_success else '❌ FAILED'}")
    print(f"Media Retrieval: {'✅ PASSED' if retrieval_success else '❌ FAILED'}")
    print(f"Content Generation: {'✅ PASSED' if content_success else '❌ FAILED'}")
    
    if upload_success and retrieval_success and content_success:
        print("\n🎉 ALL TESTS PASSED! Media Management System is working perfectly!")
    else:
        print("\n⚠️  Some tests failed. Please check the logs above.")

if __name__ == "__main__":
    main()