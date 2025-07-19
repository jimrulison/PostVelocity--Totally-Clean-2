#!/usr/bin/env python3
"""
Corrected test for failing endpoints with proper parameter formats
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "https://944873b2-f626-40e9-9438-c3331bff2788.preview.emergentagent.com"

def test_endpoint_with_params(method, endpoint, params=None, data=None):
    """Test endpoint with query parameters"""
    url = f"{BASE_URL}/api/{endpoint}"
    headers = {'Content-Type': 'application/json'}
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, params=params, timeout=15)
        elif method == 'POST':
            response = requests.post(url, headers=headers, params=params, json=data, timeout=15)
        elif method == 'PUT':
            response = requests.put(url, headers=headers, params=params, json=data, timeout=15)
        
        print(f"\n{method} {endpoint}")
        if params:
            print(f"Params: {params}")
        print(f"Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"Error Response: {response.text}")
        else:
            try:
                result = response.json()
                if isinstance(result, dict):
                    print(f"Success: {list(result.keys())}")
                elif isinstance(result, list):
                    print(f"Success: List with {len(result)} items")
                else:
                    print(f"Success: {type(result)}")
            except:
                print(f"Success: {response.text[:100]}...")
        
        return response.status_code == 200
        
    except requests.exceptions.Timeout:
        print(f"\n{method} {endpoint}")
        print("Status: TIMEOUT (>15s)")
        return False
    except Exception as e:
        print(f"\n{method} {endpoint}")
        print(f"Error: {str(e)}")
        return False

def main():
    print("Corrected Backend API Test - Proper Parameter Formats")
    print("=" * 60)
    
    # Get existing company for testing
    response = requests.get(f"{BASE_URL}/api/companies", timeout=10)
    companies = response.json()
    if not companies:
        print("No companies found. Creating one...")
        test_company = {
            "name": f"Corrected Test Company {datetime.now().strftime('%H%M%S')}",
            "industry": "construction",
            "website": "https://testcompany.com",
            "description": "A test company for API testing",
            "target_audience": "Construction workers, safety managers",
            "brand_voice": "Professional but accessible, safety-focused"
        }
        response = requests.post(f"{BASE_URL}/api/companies", json=test_company, timeout=10)
        test_company_id = response.json()['id']
    else:
        test_company_id = companies[0]['id']
    
    print(f"Using Company ID: {test_company_id}")
    
    print("\n1. Testing Company Update with full Company object...")
    # Get the full company first
    response = requests.get(f"{BASE_URL}/api/companies/{test_company_id}", timeout=10)
    full_company = response.json()
    
    # Update with all required fields
    full_company['name'] = f"Updated Company {datetime.now().strftime('%H%M%S')}"
    full_company['description'] = "Updated description for testing"
    
    success = test_endpoint_with_params('PUT', f'companies/{test_company_id}', data=full_company)
    
    print("\n2. Testing Performance Prediction with query parameters...")
    params = {
        "content": "New OSHA safety regulations require updated training protocols.",
        "platform": "instagram",
        "hashtags": ["#SafetyFirst", "#OSHA", "#ConstructionSafety"],
        "company_id": test_company_id
    }
    test_endpoint_with_params('POST', 'predict/performance', params=params)
    
    print("\n3. Testing Content Repurposing with query parameters...")
    params = {
        "content": "Construction safety training is essential for preventing workplace accidents.",
        "platforms": ["instagram", "facebook", "linkedin"]
    }
    test_endpoint_with_params('POST', 'content/repurpose', params=params)
    
    print("\n4. Testing Quick Content Generation with longer timeout...")
    content_request = {
        "company_id": test_company_id,
        "topic": "Basic Safety Training",
        "platforms": ["instagram", "facebook"],
        "audience_level": "general",
        "additional_context": "Focus on basic safety protocols",
        "generate_blog": False,
        "generate_newsletter": False,
        "generate_video_script": False
    }
    test_endpoint_with_params('POST', 'generate-content', data=content_request)
    
    print("\n5. Testing Media Upload endpoint structure...")
    # Just test if the endpoint exists and what it expects
    try:
        response = requests.post(f"{BASE_URL}/api/companies/{test_company_id}/media/upload", timeout=5)
        print(f"\nPOST companies/{test_company_id}/media/upload")
        print(f"Status: {response.status_code}")
        if response.status_code == 422:
            print("Expected 422 - endpoint exists but needs file upload")
        else:
            print(f"Response: {response.text[:200]}")
    except Exception as e:
        print(f"Media upload test error: {e}")
    
    print("\n" + "=" * 60)
    print("Corrected test completed!")

if __name__ == "__main__":
    main()