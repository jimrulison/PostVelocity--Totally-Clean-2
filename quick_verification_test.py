#!/usr/bin/env python3
"""
Quick Verification Test for PostVelocity Backend
Testing company-specific calendar and media upload functionality
"""

import requests
import json
import sys
from datetime import datetime
import uuid
import io

class QuickVerificationTester:
    def __init__(self, base_url="https://f172fa13-34dd-4e25-a49a-5e4342ce5451.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.test_company_id = None

    def log_test(self, name, success, details=""):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name} - PASSED")
        else:
            print(f"❌ {name} - FAILED: {details}")
        
        if details and success:
            print(f"   Details: {details}")

    def make_request(self, method, endpoint, data=None, params=None, files=None):
        """Make HTTP request with error handling"""
        url = f"{self.base_url}/api/{endpoint}"
        
        try:
            if method == 'GET':
                response = requests.get(url, params=params, timeout=30)
            elif method == 'POST':
                if files:
                    response = requests.post(url, data=data, files=files, timeout=30)
                else:
                    headers = {'Content-Type': 'application/json'}
                    response = requests.post(url, json=data, headers=headers, timeout=30)
            elif method == 'PUT':
                headers = {'Content-Type': 'application/json'}
                response = requests.put(url, json=data, headers=headers, timeout=30)
            elif method == 'DELETE':
                response = requests.delete(url, timeout=30)
            
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request error: {str(e)}")
            return None

    def test_health_check(self):
        """Test GET /api/health to verify backend is running"""
        response = self.make_request('GET', 'health')
        if response and response.status_code == 200:
            data = response.json()
            success = data.get('status') == 'healthy'
            self.log_test("Health Check", success, f"Status: {data.get('status')}")
            return success
        else:
            self.log_test("Health Check", False, f"Failed to connect or bad response")
            return False

    def test_debug_endpoint(self):
        """Test GET /api/debug to verify all systems operational"""
        response = self.make_request('GET', 'debug')
        if response and response.status_code == 200:
            data = response.json()
            claude_key_exists = data.get('claude_api_key_exists', False)
            seo_keywords_loaded = data.get('seo_keywords_loaded', False)
            trending_hashtags_loaded = data.get('trending_hashtags_loaded', False)
            
            success = claude_key_exists and seo_keywords_loaded and trending_hashtags_loaded
            details = f"Claude API: {claude_key_exists}, SEO Keywords: {seo_keywords_loaded}, Trending Hashtags: {trending_hashtags_loaded}"
            self.log_test("Debug Endpoint", success, details)
            return success
        else:
            self.log_test("Debug Endpoint", False, "Failed to get debug info")
            return False

    def test_get_companies(self):
        """Test GET /api/companies to verify company retrieval"""
        response = self.make_request('GET', 'companies')
        if response and response.status_code == 200:
            data = response.json()
            success = isinstance(data, list)
            companies_count = len(data) if success else 0
            self.log_test("Get Companies", success, f"Found {companies_count} companies")
            
            # Store first company ID for media upload test
            if success and companies_count > 0:
                self.test_company_id = data[0].get('id')
            
            return success
        else:
            self.log_test("Get Companies", False, f"Status: {response.status_code if response else 'No response'}")
            return False

    def test_create_company(self):
        """Test POST /api/companies to verify company creation still works"""
        test_company = {
            "name": f"Quick Test Company {datetime.now().strftime('%H%M%S')}",
            "industry": "Construction",
            "website": "https://quicktest.com",
            "description": "Quick verification test company",
            "target_audience": "Construction professionals",
            "brand_voice": "Professional and safety-focused"
        }
        
        response = self.make_request('POST', 'companies', test_company)
        if response and response.status_code == 200:
            data = response.json()
            company_id = data.get('id')
            success = company_id is not None and data.get('name') == test_company['name']
            self.log_test("Create Company", success, f"Created company with ID: {company_id}")
            
            # Use this company for media upload test if we don't have one
            if success and not self.test_company_id:
                self.test_company_id = company_id
            
            return success
        else:
            self.log_test("Create Company", False, f"Status: {response.status_code if response else 'No response'}")
            return False

    def test_media_upload_with_company_selection(self):
        """Test POST /api/companies/{company_id}/media/upload functionality"""
        if not self.test_company_id:
            self.log_test("Media Upload with Company Selection", False, "No test company ID available")
            return False

        # Create a simple test image file in memory
        test_image_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\nIDATx\x9cc\xf8\x00\x00\x00\x01\x00\x01\x00\x00\x00\x00IEND\xaeB`\x82'
        
        # Test media upload
        files = {
            'file': ('test_image.png', io.BytesIO(test_image_content), 'image/png')
        }
        
        data = {
            'category': 'training',
            'description': 'Quick verification test image',
            'tags': 'test,verification'
        }
        
        response = self.make_request('POST', f'companies/{self.test_company_id}/media/upload', data=data, files=files)
        
        if response and response.status_code == 200:
            response_data = response.json()
            success = response_data.get('id') is not None and response_data.get('company_id') == self.test_company_id
            details = f"Uploaded media ID: {response_data.get('id')}, Company: {response_data.get('company_id')}"
            self.log_test("Media Upload with Company Selection", success, details)
            return success
        else:
            error_msg = f"Status: {response.status_code if response else 'No response'}"
            if response:
                try:
                    error_data = response.json()
                    error_msg += f", Error: {error_data.get('detail', 'Unknown error')}"
                except:
                    error_msg += f", Response: {response.text[:200]}"
            self.log_test("Media Upload with Company Selection", False, error_msg)
            return False

    def test_company_media_isolation(self):
        """Verify company-specific media isolation"""
        if not self.test_company_id:
            self.log_test("Company Media Isolation", False, "No test company ID available")
            return False
            
        response = self.make_request('GET', f'companies/{self.test_company_id}/media')
        if response and response.status_code == 200:
            data = response.json()
            success = isinstance(data, list)
            
            # Check that all media belongs to the correct company
            if success and data:
                all_correct_company = all(media.get('company_id') == self.test_company_id for media in data)
                success = all_correct_company
                details = f"Retrieved {len(data)} media files, all belong to company {self.test_company_id}: {all_correct_company}"
            else:
                details = f"Retrieved {len(data) if success else 0} media files for company {self.test_company_id}"
            
            self.log_test("Company Media Isolation", success, details)
            return success
        else:
            self.log_test("Company Media Isolation", False, f"Status: {response.status_code if response else 'No response'}")
            return False

    def test_calendar_functionality(self):
        """Test calendar-related endpoints if they exist"""
        if not self.test_company_id:
            self.log_test("Calendar Functionality", False, "No test company ID available")
            return False
            
        current_date = datetime.now()
        params = {
            "month": current_date.month,
            "year": current_date.year
        }
        
        response = self.make_request('GET', f'calendar/{self.test_company_id}', params=params)
        if response and response.status_code == 200:
            data = response.json()
            success = isinstance(data, list)
            details = f"Retrieved {len(data)} calendar entries for {current_date.month}/{current_date.year}"
            self.log_test("Calendar Functionality", success, details)
            return success
        else:
            # Calendar endpoint might not exist or might be different
            # Try alternative calendar endpoint
            response = self.make_request('GET', f'companies/{self.test_company_id}/calendar', params=params)
            if response and response.status_code == 200:
                data = response.json()
                success = isinstance(data, list)
                details = f"Retrieved {len(data)} calendar entries via alternative endpoint"
                self.log_test("Calendar Functionality", success, details)
                return success
            else:
                self.log_test("Calendar Functionality", False, f"Calendar endpoints not available or not working")
                return False

    def run_quick_verification(self):
        """Run quick verification tests as specified in review request"""
        print("🚀 PostVelocity Backend Quick Verification Test")
        print("Testing company-specific calendar and media upload functionality")
        print("=" * 70)
        
        print("\n1. Basic Health Check")
        print("-" * 20)
        self.test_health_check()
        self.test_debug_endpoint()
        
        print("\n2. Company Management")
        print("-" * 20)
        self.test_get_companies()
        self.test_create_company()
        
        print("\n3. Media Upload with Company Selection")
        print("-" * 40)
        self.test_media_upload_with_company_selection()
        self.test_company_media_isolation()
        
        print("\n4. Calendar Functionality")
        print("-" * 25)
        self.test_calendar_functionality()
        
        # Print final results
        print("\n" + "=" * 70)
        print(f"📊 VERIFICATION RESULTS: {self.tests_passed}/{self.tests_run} tests passed")
        
        if self.tests_passed == self.tests_run:
            print("🎉 ALL VERIFICATION TESTS PASSED!")
            print("✅ Backend is stable after recent frontend enhancements")
            print("✅ Company-specific functionality working correctly")
            print("✅ Media upload with company isolation verified")
            return 0
        else:
            print(f"⚠️  {self.tests_run - self.tests_passed} tests failed.")
            print("❌ Some issues found that need attention")
            return 1

def main():
    """Main test execution"""
    print("PostVelocity Backend - Quick Verification Test")
    print("Testing against: https://f172fa13-34dd-4e25-a49a-5e4342ce5451.preview.emergentagent.com")
    print()
    
    tester = QuickVerificationTester()
    return tester.run_quick_verification()

if __name__ == "__main__":
    sys.exit(main())