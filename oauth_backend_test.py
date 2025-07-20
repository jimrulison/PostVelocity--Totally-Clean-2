#!/usr/bin/env python3
"""
OAuth Integration Testing for PostVelocity Social Media Management Platform
Tests OAuth 2.0 authentication system for all 20 supported platforms

TESTING REQUIREMENTS:
1. OAuth Authorization URL Generation for all 20 platforms
2. Platform Support Endpoint verification
3. OAuth Connection Management
4. Token Exchange Endpoint (simulated)
5. Content Publishing Preparation

PLATFORMS TO TEST (20 total):
Instagram, TikTok, Facebook, YouTube, WhatsApp, Snapchat, X, WeChat, Telegram, 
Facebook Messenger, Douyin, Kuaishou, Reddit, Weibo, Pinterest, QQ, LinkedIn, 
Threads, Quora, Tumblr
"""

import requests
import json
import sys
from datetime import datetime
import uuid
import urllib.parse

class OAuthIntegrationTester:
    def __init__(self, base_url="https://012dc20e-6512-4400-8634-45a38109fa3f.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.user_id = "demo-user"
        
        # All 20 platforms to test
        self.platforms = [
            "instagram", "tiktok", "facebook", "youtube", "whatsapp", 
            "snapchat", "x", "wechat", "telegram", "facebook_messenger",
            "douyin", "kuaishou", "reddit", "weibo", "pinterest", 
            "qq", "linkedin", "threads", "quora", "tumblr"
        ]
        
        # Platform-specific parameters to verify
        self.platform_specific_params = {
            "youtube": ["access_type", "prompt"],
            "linkedin": ["response_type"],
            "x": ["code_challenge_method", "code_challenge"]
        }

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

    def make_request(self, method, endpoint, data=None, params=None):
        """Make HTTP request with error handling"""
        url = f"{self.base_url}/api/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=30)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=30)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=30)
            
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request error: {str(e)}")
            return None

    def test_oauth_authorization_url_generation(self):
        """Test OAuth Authorization URL Generation for all 20 platforms"""
        print("\n🔐 TESTING OAUTH AUTHORIZATION URL GENERATION")
        print("=" * 60)
        
        successful_platforms = 0
        failed_platforms = []
        
        for platform in self.platforms:
            try:
                response = self.make_request('GET', f'oauth/url/{platform}', params={'user_id': self.user_id})
                
                if response and response.status_code == 200:
                    data = response.json()
                    
                    # Verify required fields
                    required_fields = ['authorization_url', 'state', 'platform']
                    if all(field in data for field in required_fields):
                        
                        # Verify URL structure
                        auth_url = data['authorization_url']
                        parsed_url = urllib.parse.urlparse(auth_url)
                        query_params = urllib.parse.parse_qs(parsed_url.query)
                        
                        # Check required OAuth parameters
                        required_params = ['response_type', 'client_id', 'redirect_uri', 'state', 'scope']
                        params_present = all(param in query_params for param in required_params)
                        
                        # Check platform-specific parameters
                        platform_params_ok = True
                        if platform in self.platform_specific_params:
                            expected_params = self.platform_specific_params[platform]
                            platform_params_ok = all(param in query_params for param in expected_params)
                        
                        if params_present and platform_params_ok:
                            successful_platforms += 1
                            self.log_test(
                                f"OAuth URL Generation - {platform.upper()}", 
                                True, 
                                f"URL generated with state: {data['state'][:8]}..."
                            )
                        else:
                            failed_platforms.append(platform)
                            missing_params = [p for p in required_params if p not in query_params]
                            self.log_test(
                                f"OAuth URL Generation - {platform.upper()}", 
                                False, 
                                f"Missing parameters: {missing_params}"
                            )
                    else:
                        failed_platforms.append(platform)
                        missing_fields = [f for f in required_fields if f not in data]
                        self.log_test(
                            f"OAuth URL Generation - {platform.upper()}", 
                            False, 
                            f"Missing response fields: {missing_fields}"
                        )
                else:
                    failed_platforms.append(platform)
                    error_msg = f"HTTP {response.status_code}" if response else "No response"
                    self.log_test(
                        f"OAuth URL Generation - {platform.upper()}", 
                        False, 
                        error_msg
                    )
                    
            except Exception as e:
                failed_platforms.append(platform)
                self.log_test(
                    f"OAuth URL Generation - {platform.upper()}", 
                    False, 
                    f"Exception: {str(e)}"
                )
        
        # Summary
        success_rate = (successful_platforms / len(self.platforms)) * 100
        print(f"\n📊 OAuth URL Generation Summary:")
        print(f"   ✅ Successful: {successful_platforms}/{len(self.platforms)} platforms ({success_rate:.1f}%)")
        if failed_platforms:
            print(f"   ❌ Failed: {', '.join(failed_platforms)}")

    def test_platform_support_endpoint(self):
        """Test Platform Support Endpoint"""
        print("\n🌐 TESTING PLATFORM SUPPORT ENDPOINT")
        print("=" * 60)
        
        try:
            response = self.make_request('GET', 'platforms/supported')
            
            if response and response.status_code == 200:
                data = response.json()
                
                # Verify response structure
                if 'platforms' in data and 'total_platforms' in data:
                    platforms = data['platforms']
                    total_platforms = data['total_platforms']
                    
                    # Check if all 20 platforms are returned
                    platform_names = [p['platform'] for p in platforms]
                    missing_platforms = [p for p in self.platforms if p not in platform_names]
                    
                    if len(platforms) >= 20 and not missing_platforms:
                        # Verify platform configuration details
                        required_platform_fields = ['platform', 'name', 'auth_available', 'scopes', 'max_chars']
                        all_platforms_valid = True
                        
                        for platform in platforms:
                            if not all(field in platform for field in required_platform_fields):
                                all_platforms_valid = False
                                break
                        
                        if all_platforms_valid:
                            self.log_test(
                                "Platform Support Endpoint", 
                                True, 
                                f"All {total_platforms} platforms returned with complete configuration"
                            )
                        else:
                            self.log_test(
                                "Platform Support Endpoint", 
                                False, 
                                "Some platforms missing required configuration fields"
                            )
                    else:
                        self.log_test(
                            "Platform Support Endpoint", 
                            False, 
                            f"Expected 20 platforms, got {len(platforms)}. Missing: {missing_platforms}"
                        )
                else:
                    self.log_test(
                        "Platform Support Endpoint", 
                        False, 
                        "Response missing 'platforms' or 'total_platforms' fields"
                    )
            else:
                error_msg = f"HTTP {response.status_code}" if response else "No response"
                self.log_test("Platform Support Endpoint", False, error_msg)
                
        except Exception as e:
            self.log_test("Platform Support Endpoint", False, f"Exception: {str(e)}")

    def test_oauth_connection_management(self):
        """Test OAuth Connection Management endpoints"""
        print("\n🔗 TESTING OAUTH CONNECTION MANAGEMENT")
        print("=" * 60)
        
        # Test 1: Get user connections
        try:
            response = self.make_request('GET', f'oauth/connections/{self.user_id}')
            
            if response and response.status_code == 200:
                data = response.json()
                
                if 'connections' in data and 'total_connected' in data:
                    self.log_test(
                        "Get User Connections", 
                        True, 
                        f"Retrieved {data['total_connected']} connections"
                    )
                else:
                    self.log_test(
                        "Get User Connections", 
                        False, 
                        "Response missing required fields"
                    )
            else:
                error_msg = f"HTTP {response.status_code}" if response else "No response"
                self.log_test("Get User Connections", False, error_msg)
                
        except Exception as e:
            self.log_test("Get User Connections", False, f"Exception: {str(e)}")
        
        # Test 2: Disconnect platform (test with Instagram)
        test_platform = "instagram"
        try:
            response = self.make_request('DELETE', f'oauth/disconnect/{test_platform}', params={'user_id': self.user_id})
            
            if response and response.status_code == 200:
                data = response.json()
                
                if data.get('status') == 'success':
                    self.log_test(
                        f"Disconnect Platform - {test_platform.upper()}", 
                        True, 
                        data.get('message', 'Successfully disconnected')
                    )
                else:
                    self.log_test(
                        f"Disconnect Platform - {test_platform.upper()}", 
                        False, 
                        "Response status not 'success'"
                    )
            else:
                error_msg = f"HTTP {response.status_code}" if response else "No response"
                self.log_test(f"Disconnect Platform - {test_platform.upper()}", False, error_msg)
                
        except Exception as e:
            self.log_test(f"Disconnect Platform - {test_platform.upper()}", False, f"Exception: {str(e)}")
        
        # Test 3: Refresh token (test with Facebook)
        test_platform = "facebook"
        try:
            response = self.make_request('POST', f'oauth/refresh/{test_platform}', data={'user_id': self.user_id})
            
            if response:
                # Both 200 (success) and 400 (no token to refresh) are acceptable for testing
                if response.status_code in [200, 400]:
                    if response.status_code == 200:
                        data = response.json()
                        self.log_test(
                            f"Refresh Token - {test_platform.upper()}", 
                            True, 
                            data.get('message', 'Token refreshed')
                        )
                    else:
                        # 400 is expected when no token exists to refresh
                        self.log_test(
                            f"Refresh Token - {test_platform.upper()}", 
                            True, 
                            "No token to refresh (expected for demo user)"
                        )
                else:
                    error_msg = f"HTTP {response.status_code}"
                    self.log_test(f"Refresh Token - {test_platform.upper()}", False, error_msg)
            else:
                self.log_test(f"Refresh Token - {test_platform.upper()}", False, "No response")
                
        except Exception as e:
            self.log_test(f"Refresh Token - {test_platform.upper()}", False, f"Exception: {str(e)}")

    def test_token_exchange_endpoint(self):
        """Test Token Exchange Endpoint with mock data"""
        print("\n🔄 TESTING TOKEN EXCHANGE ENDPOINT")
        print("=" * 60)
        
        # Test with mock authorization codes for different platforms
        test_cases = [
            {"platform": "instagram", "code": "mock_instagram_code_12345", "state": "mock_state_67890"},
            {"platform": "linkedin", "code": "mock_linkedin_code_abcde", "state": "mock_state_fghij"},
            {"platform": "x", "code": "mock_x_code_klmno", "state": "mock_state_pqrst"}
        ]
        
        successful_tests = 0
        
        for test_case in test_cases:
            try:
                data = {
                    "platform": test_case["platform"],
                    "code": test_case["code"],
                    "state": test_case["state"],
                    "user_id": self.user_id
                }
                
                response = self.make_request('POST', 'oauth/token', data=data)
                
                if response:
                    # We expect this to fail with 400 (invalid code) since we're using mock data
                    # But the endpoint should handle the request properly
                    if response.status_code == 400:
                        # Check if error message indicates invalid code (expected)
                        try:
                            error_data = response.json()
                            if "failed" in error_data.get("detail", "").lower():
                                successful_tests += 1
                                self.log_test(
                                    f"Token Exchange - {test_case['platform'].upper()}", 
                                    True, 
                                    "Properly handled invalid authorization code"
                                )
                            else:
                                self.log_test(
                                    f"Token Exchange - {test_case['platform'].upper()}", 
                                    False, 
                                    f"Unexpected error response: {error_data}"
                                )
                        except:
                            self.log_test(
                                f"Token Exchange - {test_case['platform'].upper()}", 
                                False, 
                                "Invalid JSON error response"
                            )
                    elif response.status_code == 200:
                        # Unexpected success with mock data
                        self.log_test(
                            f"Token Exchange - {test_case['platform'].upper()}", 
                            False, 
                            "Unexpected success with mock authorization code"
                        )
                    else:
                        self.log_test(
                            f"Token Exchange - {test_case['platform'].upper()}", 
                            False, 
                            f"Unexpected HTTP status: {response.status_code}"
                        )
                else:
                    self.log_test(
                        f"Token Exchange - {test_case['platform'].upper()}", 
                        False, 
                        "No response received"
                    )
                    
            except Exception as e:
                self.log_test(
                    f"Token Exchange - {test_case['platform'].upper()}", 
                    False, 
                    f"Exception: {str(e)}"
                )
        
        print(f"\n📊 Token Exchange Summary: {successful_tests}/{len(test_cases)} tests handled correctly")

    def test_content_publishing_preparation(self):
        """Test Content Publishing Preparation for demo mode"""
        print("\n📤 TESTING CONTENT PUBLISHING PREPARATION")
        print("=" * 60)
        
        # Test publishing to different platforms
        test_platforms = ["instagram", "facebook", "linkedin", "x", "youtube"]
        test_content = "This is a test post for PostVelocity social media management platform! 🚀 #SocialMedia #PostVelocity #Testing"
        
        successful_publishes = 0
        
        for platform in test_platforms:
            try:
                data = {
                    "content": test_content,
                    "user_id": self.user_id,
                    "media_urls": ["https://example.com/test-image.jpg"]
                }
                
                response = self.make_request('POST', f'content/publish/{platform}', data=data)
                
                if response and response.status_code == 200:
                    response_data = response.json()
                    
                    # Verify demo mode response
                    required_fields = ['status', 'message', 'platform', 'content_length', 'demo_mode']
                    if all(field in response_data for field in required_fields):
                        if response_data['status'] == 'success' and response_data['demo_mode']:
                            successful_publishes += 1
                            self.log_test(
                                f"Content Publishing - {platform.upper()}", 
                                True, 
                                f"Demo mode response: {response_data['message']}"
                            )
                        else:
                            self.log_test(
                                f"Content Publishing - {platform.upper()}", 
                                False, 
                                "Invalid status or demo_mode not enabled"
                            )
                    else:
                        missing_fields = [f for f in required_fields if f not in response_data]
                        self.log_test(
                            f"Content Publishing - {platform.upper()}", 
                            False, 
                            f"Missing response fields: {missing_fields}"
                        )
                elif response and response.status_code == 401:
                    # Expected for platforms without connected accounts
                    self.log_test(
                        f"Content Publishing - {platform.upper()}", 
                        True, 
                        "Properly requires authentication (401 Unauthorized)"
                    )
                    successful_publishes += 1
                else:
                    error_msg = f"HTTP {response.status_code}" if response else "No response"
                    self.log_test(f"Content Publishing - {platform.upper()}", False, error_msg)
                    
            except Exception as e:
                self.log_test(
                    f"Content Publishing - {platform.upper()}", 
                    False, 
                    f"Exception: {str(e)}"
                )
        
        print(f"\n📊 Content Publishing Summary: {successful_publishes}/{len(test_platforms)} platforms handled correctly")

    def run_comprehensive_oauth_tests(self):
        """Run all OAuth integration tests"""
        print("🚀 STARTING COMPREHENSIVE OAUTH INTEGRATION TESTING")
        print("=" * 80)
        print(f"Testing OAuth integration for PostVelocity Social Media Management Platform")
        print(f"Base URL: {self.base_url}")
        print(f"User ID: {self.user_id}")
        print(f"Platforms to test: {len(self.platforms)}")
        print("=" * 80)
        
        # Run all test suites
        self.test_oauth_authorization_url_generation()
        self.test_platform_support_endpoint()
        self.test_oauth_connection_management()
        self.test_token_exchange_endpoint()
        self.test_content_publishing_preparation()
        
        # Final summary
        print("\n" + "=" * 80)
        print("🎯 FINAL OAUTH INTEGRATION TEST RESULTS")
        print("=" * 80)
        
        success_rate = (self.tests_passed / self.tests_run) * 100 if self.tests_run > 0 else 0
        
        print(f"📊 Overall Results:")
        print(f"   Total Tests: {self.tests_run}")
        print(f"   Passed: {self.tests_passed}")
        print(f"   Failed: {self.tests_run - self.tests_passed}")
        print(f"   Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print(f"✅ EXCELLENT: OAuth integration system is working well!")
        elif success_rate >= 60:
            print(f"⚠️  GOOD: OAuth integration system is mostly functional with minor issues")
        else:
            print(f"❌ NEEDS WORK: OAuth integration system has significant issues")
        
        print("\n🔍 Test Coverage:")
        print("   ✅ OAuth Authorization URL Generation (20 platforms)")
        print("   ✅ Platform Support Endpoint")
        print("   ✅ OAuth Connection Management")
        print("   ✅ Token Exchange Endpoint (simulated)")
        print("   ✅ Content Publishing Preparation")
        
        return success_rate >= 70  # Return True if tests are mostly successful

def main():
    """Main function to run OAuth integration tests"""
    print("PostVelocity OAuth Integration Testing Suite")
    print("=" * 50)
    
    tester = OAuthIntegrationTester()
    success = tester.run_comprehensive_oauth_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()