#!/usr/bin/env python3
"""
Phase 2C API Access System Backend Testing
Tests all API key management and enterprise API endpoints
"""

import requests
import json
import time
import uuid
from datetime import datetime
import os

# Get backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://012dc20e-6512-4400-8634-45a38109fa3f.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class Phase2CAPITester:
    def __init__(self):
        self.test_results = []
        self.api_keys = {}  # Store generated API keys for testing
        self.test_user_ids = {}  # Store test user IDs
        
    def log_result(self, test_name, success, details="", response_data=None):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
        if details:
            print(f"   Details: {details}")
        if not success and response_data:
            print(f"   Response: {response_data}")
        print()

    def make_request(self, method, endpoint, data=None, headers=None, params=None):
        """Make HTTP request with error handling"""
        try:
            url = f"{API_BASE}{endpoint}"
            if headers is None:
                headers = {"Content-Type": "application/json"}
            
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, params=params, timeout=30)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, headers=headers, timeout=30)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=headers, timeout=30)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None

    def setup_test_users(self):
        """Create test users with different plan types"""
        print("🔧 Setting up test users...")
        
        # First, let's create a company to get a valid company_id
        test_company = {
            "name": f"API Test Company {datetime.now().strftime('%H%M%S')}",
            "industry": "Construction",
            "website": "https://apitestcompany.com",
            "description": "A test company for API testing",
            "target_audience": "Construction workers, safety managers",
            "brand_voice": "Professional but accessible, safety-focused"
        }
        
        company_response = self.make_request("POST", "/companies", test_company)
        if company_response and company_response.status_code == 200:
            company_data = company_response.json()
            self.test_company_id = company_data.get("id")
            print(f"✅ Test company created: {self.test_company_id}")
        else:
            self.test_company_id = "507f1f77bcf86cd799439013"
            print(f"⚠️  Using fallback company ID: {self.test_company_id}")
        
        # For testing purposes, we'll use valid ObjectId format user IDs
        # These represent users with different plan types
        self.test_user_ids["business"] = "507f1f77bcf86cd799439011"  # Business plan user
        self.test_user_ids["starter"] = "507f1f77bcf86cd799439012"   # Starter plan user
        
        print(f"✅ Test users setup complete")
        print(f"   Business User ID: {self.test_user_ids['business']}")
        print(f"   Starter User ID: {self.test_user_ids['starter']}")
        print()

    def test_api_key_generation_business_user(self):
        """Test API key generation for business plan user"""
        test_name = "API Key Generation - Business Plan User"
        
        request_data = {
            "user_id": self.test_user_ids["business"],
            "key_name": "Test Business API Key",
            "permissions": ["read", "write"],
            "expires_in_days": 365
        }
        
        response = self.make_request("POST", "/keys/generate", request_data)
        
        if response and response.status_code == 200:
            data = response.json()
            if data.get("status") == "success" and data.get("api_key", "").startswith("pv_"):
                self.api_keys["business_read_write"] = data.get("api_key")
                self.log_result(test_name, True, 
                    f"API key generated successfully: {data.get('api_key')[:12]}..., Permissions: {data.get('permissions')}")
            else:
                self.log_result(test_name, False, "Invalid response format", data)
        else:
            self.log_result(test_name, False, 
                f"Request failed with status: {response.status_code if response else 'No response'}", 
                response.json() if response else None)

    def test_api_key_generation_different_permissions(self):
        """Test API key generation with different permission levels"""
        permissions_tests = [
            (["read"], "read_only"),
            (["write"], "write_only"), 
            (["admin"], "admin_only"),
            (["read", "write", "admin"], "full_access")
        ]
        
        for permissions, key_type in permissions_tests:
            test_name = f"API Key Generation - {key_type.replace('_', ' ').title()} Permissions"
            
            request_data = {
                "user_id": self.test_user_ids["business"],
                "key_name": f"Test {key_type} Key",
                "permissions": permissions,
                "expires_in_days": 30
            }
            
            response = self.make_request("POST", "/keys/generate", request_data)
            
            if response and response.status_code == 200:
                data = response.json()
                if data.get("status") == "success" and set(data.get("permissions", [])) == set(permissions):
                    self.api_keys[key_type] = data.get("api_key")
                    self.log_result(test_name, True, 
                        f"API key with {permissions} permissions generated successfully")
                else:
                    self.log_result(test_name, False, "Permissions mismatch", data)
            else:
                self.log_result(test_name, False, 
                    f"Request failed with status: {response.status_code if response else 'No response'}")

    def test_api_key_generation_starter_user(self):
        """Test API key generation for starter plan user (should fail)"""
        test_name = "API Key Generation - Starter Plan User (Should Require Upgrade)"
        
        request_data = {
            "user_id": self.test_user_ids["starter"],
            "key_name": "Test Starter API Key",
            "permissions": ["read"],
            "expires_in_days": 30
        }
        
        response = self.make_request("POST", "/keys/generate", request_data)
        
        if response and response.status_code == 200:
            data = response.json()
            if data.get("status") == "upgrade_required":
                self.log_result(test_name, True, 
                    f"Correctly requires upgrade: {data.get('message')}, Required plan: {data.get('required_plan')}")
            else:
                self.log_result(test_name, False, "Should require upgrade but didn't", data)
        else:
            self.log_result(test_name, False, 
                f"Request failed with status: {response.status_code if response else 'No response'}")

    def test_list_user_api_keys(self):
        """Test listing user's API keys"""
        test_name = "List User API Keys"
        
        user_id = self.test_user_ids["business"]
        response = self.make_request("GET", f"/keys/{user_id}")
        
        if response and response.status_code == 200:
            data = response.json()
            if data.get("status") == "success" and isinstance(data.get("api_keys"), list):
                api_keys = data.get("api_keys", [])
                masked_keys = [key for key in api_keys if "..." in key.get("api_key", "")]
                self.log_result(test_name, True, 
                    f"Retrieved {len(api_keys)} API keys, all properly masked: {len(masked_keys) == len(api_keys)}")
            else:
                self.log_result(test_name, False, "Invalid response format", data)
        else:
            self.log_result(test_name, False, 
                f"Request failed with status: {response.status_code if response else 'No response'}")

    def test_revoke_api_key(self):
        """Test revoking an API key"""
        test_name = "Revoke API Key"
        
        # First, get the list of keys to find one to revoke
        user_id = self.test_user_ids["business"]
        response = self.make_request("GET", f"/keys/{user_id}")
        
        if response and response.status_code == 200:
            data = response.json()
            api_keys = data.get("api_keys", [])
            
            if api_keys:
                key_to_revoke = api_keys[0]["id"]
                
                # Now revoke the key
                revoke_response = self.make_request("DELETE", f"/keys/{key_to_revoke}")
                
                if revoke_response and revoke_response.status_code == 200:
                    revoke_data = revoke_response.json()
                    if revoke_data.get("status") == "success":
                        self.log_result(test_name, True, 
                            f"API key revoked successfully: {revoke_data.get('message')}")
                    else:
                        self.log_result(test_name, False, "Revocation failed", revoke_data)
                else:
                    self.log_result(test_name, False, 
                        f"Revoke request failed with status: {revoke_response.status_code if revoke_response else 'No response'}")
            else:
                self.log_result(test_name, False, "No API keys found to revoke")
        else:
            self.log_result(test_name, False, "Could not retrieve API keys for revocation test")

    def test_api_authentication_valid_key(self):
        """Test API authentication with valid key"""
        test_name = "API Authentication - Valid Key"
        
        if "business_read_write" not in self.api_keys:
            self.log_result(test_name, False, "No valid API key available for testing")
            return
        
        api_key = self.api_keys["business_read_write"]
        response = self.make_request("GET", "/v1/content", params={"api_key": api_key})
        
        if response and response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                self.log_result(test_name, True, 
                    f"Authentication successful, retrieved {len(data.get('content', []))} content items")
            else:
                self.log_result(test_name, False, "Authentication failed", data)
        else:
            self.log_result(test_name, False, 
                f"Request failed with status: {response.status_code if response else 'No response'}")

    def test_api_authentication_invalid_key(self):
        """Test API authentication with invalid key"""
        test_name = "API Authentication - Invalid Key"
        
        invalid_key = "pv_invalid_key_12345"
        response = self.make_request("GET", "/v1/content", params={"api_key": invalid_key})
        
        if response and response.status_code == 401:
            self.log_result(test_name, True, "Correctly rejected invalid API key")
        else:
            self.log_result(test_name, False, 
                f"Should return 401 for invalid key, got: {response.status_code if response else 'No response'}")

    def test_api_permissions_read_only(self):
        """Test API permissions with read-only key"""
        test_name = "API Permissions - Read Only Key"
        
        if "read_only" not in self.api_keys:
            self.log_result(test_name, False, "No read-only API key available for testing")
            return
        
        api_key = self.api_keys["read_only"]
        
        # Test read access (should work)
        read_response = self.make_request("GET", "/v1/content", params={"api_key": api_key})
        read_success = read_response and read_response.status_code == 200
        
        # Test write access (should fail)
        write_data = {
            "topic": "Test Content Generation",
            "platform": "instagram",
            "company_id": "test-company"
        }
        write_response = self.make_request("POST", "/v1/content/generate", 
                                         write_data, params={"api_key": api_key})
        write_failed = write_response and write_response.status_code == 403
        
        if read_success and write_failed:
            self.log_result(test_name, True, "Read-only permissions working correctly")
        else:
            self.log_result(test_name, False, 
                f"Permission test failed - Read: {read_success}, Write blocked: {write_failed}")

    def test_enterprise_api_content_retrieval(self):
        """Test enterprise API content retrieval"""
        test_name = "Enterprise API - Content Retrieval"
        
        if "business_read_write" not in self.api_keys:
            self.log_result(test_name, False, "No valid API key available for testing")
            return
        
        api_key = self.api_keys["business_read_write"]
        response = self.make_request("GET", "/v1/content", params={"api_key": api_key})
        
        if response and response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                content = data.get("content", [])
                api_usage = data.get("api_usage", {})
                self.log_result(test_name, True, 
                    f"Retrieved {len(content)} content items, API usage: {api_usage.get('requests_used', 0)}/{api_usage.get('rate_limit', 1000)}")
            else:
                self.log_result(test_name, False, "Invalid response format", data)
        else:
            self.log_result(test_name, False, 
                f"Request failed with status: {response.status_code if response else 'No response'}")

    def test_enterprise_api_content_generation(self):
        """Test enterprise API content generation"""
        test_name = "Enterprise API - Content Generation"
        
        if "business_read_write" not in self.api_keys:
            self.log_result(test_name, False, "No valid API key available for testing")
            return
        
        api_key = self.api_keys["business_read_write"]
        request_data = {
            "topic": "Construction Safety Best Practices",
            "platform": "linkedin",
            "company_id": "api-test-company"
        }
        
        response = self.make_request("POST", "/v1/content/generate", 
                                   request_data, params={"api_key": api_key})
        
        if response and response.status_code == 200:
            data = response.json()
            if data.get("status") == "success" and data.get("content"):
                self.log_result(test_name, True, 
                    f"Content generated successfully: {len(data.get('content', ''))} characters, Platform: {data.get('platform')}")
            else:
                self.log_result(test_name, False, "Content generation failed", data)
        else:
            self.log_result(test_name, False, 
                f"Request failed with status: {response.status_code if response else 'No response'}")

    def test_enterprise_api_analytics(self):
        """Test enterprise API analytics retrieval"""
        test_name = "Enterprise API - Analytics Retrieval"
        
        if "business_read_write" not in self.api_keys:
            self.log_result(test_name, False, "No valid API key available for testing")
            return
        
        api_key = self.api_keys["business_read_write"]
        response = self.make_request("GET", "/v1/analytics", params={"api_key": api_key, "days": 30})
        
        if response and response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                analytics = data.get("analytics", {})
                platform_breakdown = analytics.get("platform_breakdown", {})
                self.log_result(test_name, True, 
                    f"Analytics retrieved: {analytics.get('total_posts', 0)} posts, {len(platform_breakdown)} platforms, Engagement rate: {analytics.get('engagement_rate', 0)}%")
            else:
                self.log_result(test_name, False, "Analytics retrieval failed", data)
        else:
            self.log_result(test_name, False, 
                f"Request failed with status: {response.status_code if response else 'No response'}")

    def test_rate_limiting_and_usage_tracking(self):
        """Test rate limiting and usage tracking"""
        test_name = "Rate Limiting and Usage Tracking"
        
        if "business_read_write" not in self.api_keys:
            self.log_result(test_name, False, "No valid API key available for testing")
            return
        
        api_key = self.api_keys["business_read_write"]
        
        # Make multiple requests to test usage tracking
        initial_response = self.make_request("GET", "/v1/content", params={"api_key": api_key})
        if not initial_response or initial_response.status_code != 200:
            self.log_result(test_name, False, "Initial request failed")
            return
        
        initial_usage = initial_response.json().get("api_usage", {}).get("requests_used", 0)
        
        # Make another request
        second_response = self.make_request("GET", "/v1/content", params={"api_key": api_key})
        if not second_response or second_response.status_code != 200:
            self.log_result(test_name, False, "Second request failed")
            return
        
        second_usage = second_response.json().get("api_usage", {}).get("requests_used", 0)
        
        if second_usage > initial_usage:
            self.log_result(test_name, True, 
                f"Usage tracking working: {initial_usage} → {second_usage} requests")
        else:
            self.log_result(test_name, False, 
                f"Usage not incrementing: {initial_usage} → {second_usage}")

    def test_api_key_format_validation(self):
        """Test API key format validation"""
        test_name = "API Key Format Validation"
        
        # Check if generated keys follow pv_* format
        valid_format_count = 0
        total_keys = 0
        
        for key_type, api_key in self.api_keys.items():
            total_keys += 1
            if api_key and api_key.startswith("pv_") and len(api_key) > 10:
                valid_format_count += 1
        
        if total_keys > 0 and valid_format_count == total_keys:
            self.log_result(test_name, True, 
                f"All {total_keys} generated API keys follow pv_* format")
        else:
            self.log_result(test_name, False, 
                f"Format validation failed: {valid_format_count}/{total_keys} keys valid")

    def run_all_tests(self):
        """Run all Phase 2C API Access System tests"""
        print("🚀 Starting Phase 2C API Access System Backend Testing")
        print("=" * 60)
        
        # Setup
        self.setup_test_users()
        
        # API Key Management Tests
        print("📋 Testing API Key Management...")
        self.test_api_key_generation_business_user()
        self.test_api_key_generation_different_permissions()
        self.test_api_key_generation_starter_user()
        self.test_list_user_api_keys()
        self.test_revoke_api_key()
        
        # API Authentication Tests
        print("🔐 Testing API Authentication...")
        self.test_api_authentication_valid_key()
        self.test_api_authentication_invalid_key()
        self.test_api_permissions_read_only()
        
        # Enterprise API Tests
        print("🏢 Testing Enterprise API Endpoints...")
        self.test_enterprise_api_content_retrieval()
        self.test_enterprise_api_content_generation()
        self.test_enterprise_api_analytics()
        
        # Advanced Features Tests
        print("⚡ Testing Advanced Features...")
        self.test_rate_limiting_and_usage_tracking()
        self.test_api_key_format_validation()
        
        # Summary
        self.print_summary()

    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📊 PHASE 2C API ACCESS SYSTEM TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"   • {result['test']}: {result['details']}")
        
        print("\n🔑 GENERATED API KEYS:")
        for key_type, api_key in self.api_keys.items():
            if api_key:
                print(f"   • {key_type}: {api_key[:12]}...{api_key[-4:]}")
        
        # Overall assessment
        if success_rate >= 90:
            print(f"\n🎉 EXCELLENT: Phase 2C API Access System is {success_rate:.1f}% functional!")
        elif success_rate >= 75:
            print(f"\n✅ GOOD: Phase 2C API Access System is {success_rate:.1f}% functional with minor issues.")
        elif success_rate >= 50:
            print(f"\n⚠️  MODERATE: Phase 2C API Access System is {success_rate:.1f}% functional with some issues.")
        else:
            print(f"\n❌ CRITICAL: Phase 2C API Access System has major issues ({success_rate:.1f}% functional).")

if __name__ == "__main__":
    tester = Phase2CAPITester()
    tester.run_all_tests()