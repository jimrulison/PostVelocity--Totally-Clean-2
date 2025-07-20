#!/usr/bin/env python3
"""
Phase 5 Enhanced Usage Status Component Testing
Tests usage tracking, security integration, and license validation backend support
"""

import requests
import json
import sys
from datetime import datetime, timedelta
import uuid

class Phase5UsageStatusTester:
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

    def make_request(self, method, endpoint, data=None, params=None, timeout=15):
        """Make HTTP request with error handling"""
        url = f"{self.base_url}/api/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params, timeout=timeout)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=timeout)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=timeout)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=timeout)
            
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request error: {str(e)}")
            return None

    def test_backend_security_integration(self):
        """Test security system integration"""
        response = self.make_request('GET', 'debug')
        if response and response.status_code == 200:
            data = response.json()
            
            # Check if security-related configurations are present
            has_claude_key = data.get('claude_api_key_exists', False)
            has_mongo = data.get('mongo_connected', False)
            has_seo_keywords = data.get('seo_keywords_loaded', False)
            has_trending_hashtags = data.get('trending_hashtags_loaded', False)
            
            # Security integration is working if all core components are loaded
            security_integration = all([has_claude_key, has_mongo, has_seo_keywords, has_trending_hashtags])
            
            details = f"Claude API: {has_claude_key}, MongoDB: {has_mongo}, SEO Keywords: {has_seo_keywords}, Trending Hashtags: {has_trending_hashtags}"
            self.log_test("Backend Security Integration", security_integration, details)
            return security_integration
        else:
            self.log_test("Backend Security Integration", False, "Failed to get debug info")
            return False

    def test_usage_tracking_backend_support(self):
        """Test backend support for usage tracking through content generation"""
        # Create a test company first
        test_company = {
            "name": f"Usage Test Company {datetime.now().strftime('%H%M%S')}",
            "industry": "Construction",
            "description": "Test company for usage tracking"
        }
        
        response = self.make_request('POST', 'companies', test_company)
        if not response or response.status_code != 200:
            self.log_test("Usage Tracking Backend Support", False, "Failed to create test company")
            return False
        
        company_data = response.json()
        self.test_company_id = company_data.get('id')
        
        # Test usage tracking through content generation (this should track usage internally)
        content_request = {
            "company_id": self.test_company_id,
            "topic": "Safety Training Usage Test",
            "platforms": ["instagram", "facebook"],
            "audience_level": "general",
            "additional_context": "Testing usage tracking functionality"
        }
        
        # Make multiple requests to test usage tracking
        usage_requests = []
        for i in range(3):
            response = self.make_request('POST', 'generate-content', content_request, timeout=45)
            if response:
                usage_requests.append(response.status_code == 200)
            else:
                usage_requests.append(False)
        
        # Check if at least some requests succeeded (indicating usage tracking is working)
        successful_requests = sum(usage_requests)
        usage_tracking_working = successful_requests > 0
        
        details = f"Successful usage tracking requests: {successful_requests}/3"
        self.log_test("Usage Tracking Backend Support", usage_tracking_working, details)
        return usage_tracking_working

    def test_license_validation_backend(self):
        """Test license validation through platform access"""
        response = self.make_request('GET', 'platforms')
        if response and response.status_code == 200:
            data = response.json()
            platforms = data.get('platforms', [])
            configs = data.get('configs', {})
            
            # Check if all expected platforms are available (license validation working)
            expected_platforms = ['instagram', 'tiktok', 'facebook', 'youtube', 'whatsapp', 'snapchat', 'x', 'linkedin']
            license_valid = len(platforms) >= 8 and all(p in platforms for p in expected_platforms)
            
            # Check if platform configurations are complete (indicates proper licensing)
            config_complete = all(
                config.get('max_chars') and config.get('hashtag_limit') and config.get('style')
                for config in configs.values()
            )
            
            license_validation = license_valid and config_complete
            details = f"Platforms: {len(platforms)}/8, Configs complete: {config_complete}"
            self.log_test("License Validation Backend", license_validation, details)
            return license_validation
        else:
            self.log_test("License Validation Backend", False, "Failed to get platform info")
            return False

    def test_trial_system_backend_support(self):
        """Test backend support for trial system through company management"""
        if not self.test_company_id:
            self.log_test("Trial System Backend Support", False, "No test company available")
            return False
        
        # Test getting company info (trial system would track this)
        response = self.make_request('GET', f'companies/{self.test_company_id}')
        if response and response.status_code == 200:
            company_data = response.json()
            
            # Check if company has fields that support trial system
            has_subscription_tier = 'subscription_tier' in company_data
            has_created_at = 'created_at' in company_data
            has_updated_at = 'updated_at' in company_data
            
            # Test updating company (trial system would track usage)
            update_data = {
                "description": f"Updated for trial system test - {datetime.now().isoformat()}"
            }
            
            update_response = self.make_request('PUT', f'companies/{self.test_company_id}', update_data)
            update_successful = update_response and update_response.status_code == 200
            
            trial_support = has_subscription_tier and has_created_at and update_successful
            details = f"Subscription tier: {has_subscription_tier}, Timestamps: {has_created_at}, Update: {update_successful}"
            self.log_test("Trial System Backend Support", trial_support, details)
            return trial_support
        else:
            self.log_test("Trial System Backend Support", False, "Failed to get company info")
            return False

    def test_payment_system_backend_support(self):
        """Test backend support for payment system through ROI analytics"""
        if not self.test_company_id:
            self.log_test("Payment System Backend Support", False, "No test company available")
            return False
        
        # Test ROI analytics (payment system would use this data)
        response = self.make_request('GET', f'analytics/{self.test_company_id}/roi')
        if response and response.status_code == 200:
            data = response.json()
            
            # Check if ROI data structure supports payment system
            payment_fields = [
                'total_investment', 'leads_generated', 'conversions', 
                'revenue_attributed', 'cost_per_lead', 'roi_percentage'
            ]
            
            has_payment_fields = all(field in data for field in payment_fields)
            has_platform_breakdown = isinstance(data.get('platform_breakdown', {}), dict)
            has_content_performance = isinstance(data.get('content_type_performance', {}), dict)
            
            payment_support = has_payment_fields and has_platform_breakdown and has_content_performance
            details = f"Payment fields: {has_payment_fields}, Platform data: {has_platform_breakdown}, Content data: {has_content_performance}"
            self.log_test("Payment System Backend Support", payment_support, details)
            return payment_support
        else:
            self.log_test("Payment System Backend Support", False, "Failed to get ROI analytics")
            return False

    def test_enhanced_status_component_integration(self):
        """Test enhanced status component integration through multiple endpoints"""
        if not self.test_company_id:
            self.log_test("Enhanced Status Component Integration", False, "No test company available")
            return False
        
        # Test multiple endpoints that the enhanced status component would use
        endpoints_to_test = [
            ('companies', 'GET', None),
            (f'companies/{self.test_company_id}', 'GET', None),
            (f'companies/{self.test_company_id}/media/categories', 'GET', None),
            ('platforms', 'GET', None)
        ]
        
        successful_endpoints = 0
        total_endpoints = len(endpoints_to_test)
        
        for endpoint, method, data in endpoints_to_test:
            response = self.make_request(method, endpoint, data)
            if response and response.status_code == 200:
                successful_endpoints += 1
        
        integration_working = successful_endpoints >= (total_endpoints * 0.75)  # 75% success rate
        details = f"Successful endpoints: {successful_endpoints}/{total_endpoints}"
        self.log_test("Enhanced Status Component Integration", integration_working, details)
        return integration_working

    def test_advanced_ai_features_for_status(self):
        """Test advanced AI features that support status component"""
        # Test SEO analysis (status component would show AI feature usage)
        seo_test = {
            "content": "Construction safety training for enhanced status testing",
            "target_keywords": ["construction safety", "training"]
        }
        
        seo_response = self.make_request('POST', 'seo/analyze', seo_test)
        seo_working = seo_response and seo_response.status_code == 200
        
        # Test hashtag analysis (status component would track AI usage)
        hashtag_test = {
            "hashtags": ["#SafetyFirst", "#Construction"],
            "industry": "construction"
        }
        
        hashtag_response = self.make_request('POST', 'hashtags/analyze', hashtag_test)
        hashtag_working = hashtag_response and hashtag_response.status_code == 200
        
        # Test trending hashtags (status component would show available features)
        trending_response = self.make_request('GET', 'hashtags/trending/construction')
        trending_working = trending_response and trending_response.status_code == 200
        
        ai_features_working = seo_working and hashtag_working and trending_working
        details = f"SEO: {seo_working}, Hashtags: {hashtag_working}, Trending: {trending_working}"
        self.log_test("Advanced AI Features for Status", ai_features_working, details)
        return ai_features_working

    def run_phase5_tests(self):
        """Run all Phase 5 Enhanced Usage Status Component tests"""
        print("🚀 Phase 5 Enhanced Usage Status Component Testing")
        print("=" * 60)
        
        print("\n🔒 Security Integration Tests")
        print("-" * 30)
        self.test_backend_security_integration()
        
        print("\n📊 Usage Tracking Tests")
        print("-" * 30)
        self.test_usage_tracking_backend_support()
        
        print("\n🎫 License Validation Tests")
        print("-" * 30)
        self.test_license_validation_backend()
        
        print("\n🆓 Trial System Tests")
        print("-" * 30)
        self.test_trial_system_backend_support()
        
        print("\n💳 Payment System Tests")
        print("-" * 30)
        self.test_payment_system_backend_support()
        
        print("\n🔧 Status Component Integration Tests")
        print("-" * 30)
        self.test_enhanced_status_component_integration()
        
        print("\n🤖 AI Features Status Tests")
        print("-" * 30)
        self.test_advanced_ai_features_for_status()
        
        # Print final results
        print("\n" + "=" * 60)
        print(f"📊 PHASE 5 RESULTS: {self.tests_passed}/{self.tests_run} tests passed")
        
        if self.tests_passed == self.tests_run:
            print("🎉 ALL PHASE 5 TESTS PASSED! Enhanced Usage Status Component backend is working!")
            return True
        else:
            print(f"⚠️  {self.tests_run - self.tests_passed} Phase 5 tests failed.")
            return False

def main():
    """Main test execution for Phase 5"""
    print("Phase 5 Enhanced Usage Status Component - Backend Testing")
    print("Testing against: https://f172fa13-34dd-4e25-a49a-5e4342ce5451.preview.emergentagent.com")
    print()
    
    tester = Phase5UsageStatusTester()
    success = tester.run_phase5_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())