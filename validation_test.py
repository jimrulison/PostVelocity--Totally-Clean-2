#!/usr/bin/env python3
"""
Quick test to check the specific error details for file validation
"""

import requests
import io

def test_file_validation_details():
    base_url = "https://9b531162-6bde-47f4-84ae-bcc0317537cc.preview.emergentagent.com"
    
    # Test invalid file type
    print("Testing invalid file type...")
    invalid_file = io.BytesIO(b"This is not an image file")
    files = {'file': ("invalid_test.txt", invalid_file, 'text/plain')}
    data = {'category': 'training', 'description': 'Invalid file test'}
    
    # Use a demo company ID that should exist
    company_id = "demo-company"
    
    response = requests.post(f"{base_url}/api/companies/{company_id}/media/upload", 
                           data=data, files=files, timeout=30)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    # Test non-existent company
    print("\nTesting non-existent company...")
    test_file = io.BytesIO(b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x01\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00\xaa\xff\xd9')
    files = {'file': ("test.jpg", test_file, 'image/jpeg')}
    data = {'category': 'training', 'description': 'Non-existent company test'}
    
    fake_company_id = "507f1f77bcf86cd799439011"  # Valid ObjectId format but non-existent
    response = requests.post(f"{base_url}/api/companies/{fake_company_id}/media/upload", 
                           data=data, files=files, timeout=30)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

if __name__ == "__main__":
    test_file_validation_details()