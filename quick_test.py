#!/usr/bin/env python3
"""
Quick targeted test for specific failing endpoints
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "https://c19ec803-cffc-45c2-9889-95091f0edbcb.preview.emergentagent.com"

def test_endpoint(method, endpoint, data=None, params=None):
    """Test a specific endpoint and return detailed results"""
    url = f"{BASE_URL}/api/{endpoint}"
    headers = {'Content-Type': 'application/json'}
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, params=params, timeout=10)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=headers, timeout=10)
        elif method == 'PUT':
            response = requests.put(url, json=data, headers=headers, timeout=10)
        
        print(f"\n{method} {endpoint}")
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
        print("Status: TIMEOUT (>10s)")
        return False
    except Exception as e:
        print(f"\n{method} {endpoint}")
        print(f"Error: {str(e)}")
        return False

def main():
    print("Quick Backend API Test - Focusing on Failing Endpoints")
    print("=" * 60)
    
    # First create a test company
    test_company = {
        "name": f"Quick Test Company {datetime.now().strftime('%H%M%S')}",
        "industry": "construction",
        "website": "https://testcompany.com",
        "description": "A test company for API testing",
        "target_audience": "Construction workers, safety managers",
        "brand_voice": "Professional but accessible, safety-focused"
    }
    
    print("\n1. Testing Company Creation...")
    success = test_endpoint('POST', 'companies', test_company)
    
    if success:
        # Get the company ID from the companies list
        response = requests.get(f"{BASE_URL}/api/companies", timeout=10)
        companies = response.json()
        test_company_id = companies[-1]['id']  # Get the last created company
        print(f"Test Company ID: {test_company_id}")
        
        print("\n2. Testing Company Update (422 error)...")
        update_data = {
            "name": f"Updated Quick Test Company {datetime.now().strftime('%H%M%S')}",
            "description": "Updated description for testing"
        }
        test_endpoint('PUT', f'companies/{test_company_id}', update_data)
        
        print("\n3. Testing Performance Prediction (422 error)...")
        perf_data = {
            "content": "New OSHA safety regulations require updated training protocols.",
            "platform": "instagram", 
            "hashtags": ["#SafetyFirst", "#OSHA"],
            "company_id": test_company_id
        }
        test_endpoint('POST', 'predict/performance', perf_data)
        
        print("\n4. Testing Content Repurposing (422 error)...")
        repurpose_data = {
            "content": "Construction safety training is essential for preventing workplace accidents.",
            "platforms": ["instagram", "facebook"]
        }
        test_endpoint('POST', 'content/repurpose', repurpose_data)
        
        print("\n5. Testing Quick Content Generation (timeout issue)...")
        content_request = {
            "company_id": test_company_id,
            "topic": "Basic Safety Training",
            "platforms": ["instagram", "facebook"],
            "audience_level": "general",
            "additional_context": "Focus on basic safety protocols"
        }
        test_endpoint('POST', 'generate-content', content_request)
        
        print("\n6. Testing Schedule Post (422 error)...")
        scheduled_time = datetime.utcnow() + timedelta(hours=1)
        post_data = {
            "company_id": test_company_id,
            "platform": "instagram",
            "content": "Test post content for scheduling",
            "hashtags": ["test", "safety"],
            "scheduled_time": scheduled_time.isoformat(),
            "topic": "Test Topic"
        }
        test_endpoint('POST', 'schedule-post', post_data)
    
    print("\n" + "=" * 60)
    print("Quick test completed!")

if __name__ == "__main__":
    main()