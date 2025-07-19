#!/usr/bin/env python3
"""
Final corrected test with proper JSON body format for FastAPI individual parameters
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "https://e2e6ef8c-24a4-44d0-94bb-a56227ac3447.preview.emergentagent.com"

def test_endpoint_json(method, endpoint, data=None):
    """Test endpoint with JSON body"""
    url = f"{BASE_URL}/api/{endpoint}"
    headers = {'Content-Type': 'application/json'}
    
    try:
        if method == 'POST':
            response = requests.post(url, json=data, headers=headers, timeout=20)
        elif method == 'PUT':
            response = requests.put(url, json=data, headers=headers, timeout=20)
        
        print(f"\n{method} {endpoint}")
        if data:
            print(f"Data keys: {list(data.keys()) if isinstance(data, dict) else type(data)}")
        print(f"Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"Error Response: {response.text}")
        else:
            try:
                result = response.json()
                if isinstance(result, dict):
                    print(f"Success: {list(result.keys())}")
                    # Show some key values for verification
                    if 'predicted_performance' in result:
                        print(f"  Predicted Performance: {result['predicted_performance']}")
                    if 'variations' in result:
                        print(f"  Variations: {list(result['variations'].keys())}")
                elif isinstance(result, list):
                    print(f"Success: List with {len(result)} items")
                else:
                    print(f"Success: {type(result)}")
            except:
                print(f"Success: {response.text[:100]}...")
        
        return response.status_code == 200
        
    except requests.exceptions.Timeout:
        print(f"\n{method} {endpoint}")
        print("Status: TIMEOUT (>20s)")
        return False
    except Exception as e:
        print(f"\n{method} {endpoint}")
        print(f"Error: {str(e)}")
        return False

def main():
    print("Final Corrected Backend API Test - JSON Body Format")
    print("=" * 60)
    
    # Get existing company for testing
    response = requests.get(f"{BASE_URL}/api/companies", timeout=10)
    companies = response.json()
    test_company_id = companies[0]['id'] if companies else None
    
    if not test_company_id:
        print("No companies found!")
        return
    
    print(f"Using Company ID: {test_company_id}")
    
    print("\n1. Testing Performance Prediction with JSON body...")
    perf_data = {
        "content": "New OSHA safety regulations require updated training protocols. Learn about fall protection standards.",
        "platform": "instagram",
        "hashtags": ["#SafetyFirst", "#OSHA", "#ConstructionSafety"],
        "company_id": test_company_id
    }
    test_endpoint_json('POST', 'predict/performance', perf_data)
    
    print("\n2. Testing Content Repurposing with JSON body...")
    repurpose_data = {
        "content": "Construction safety training is essential for preventing workplace accidents. Our comprehensive OSHA-compliant programs ensure your team stays safe and productive.",
        "platforms": ["instagram", "facebook", "linkedin", "tiktok"]
    }
    test_endpoint_json('POST', 'content/repurpose', repurpose_data)
    
    print("\n3. Testing Quick Content Generation (reduced scope)...")
    content_request = {
        "company_id": test_company_id,
        "topic": "Basic PPE Safety",
        "platforms": ["instagram", "facebook"],
        "audience_level": "general",
        "additional_context": "Focus on basic safety protocols",
        "generate_blog": False,
        "generate_newsletter": False,
        "generate_video_script": False,
        "use_company_media": False,
        "seo_focus": False,
        "repurpose_content": False
    }
    test_endpoint_json('POST', 'generate-content', content_request)
    
    print("\n4. Testing SEO Analysis (should work)...")
    seo_data = {
        "content": "Construction safety is crucial for workplace protection. OSHA compliance ensures worker safety through proper training and equipment usage. Safety protocols must be followed to prevent accidents.",
        "target_keywords": ["construction safety", "OSHA compliance", "workplace protection"]
    }
    test_endpoint_json('POST', 'seo/analyze', seo_data)
    
    print("\n5. Testing Hashtag Analysis (should work)...")
    hashtag_data = {
        "hashtags": ["#BuildSafe", "#ConstructionLife", "#SafetyFirst", "#OSHA"],
        "industry": "construction"
    }
    test_endpoint_json('POST', 'hashtags/analyze', hashtag_data)
    
    print("\n" + "=" * 60)
    print("Final corrected test completed!")

if __name__ == "__main__":
    main()