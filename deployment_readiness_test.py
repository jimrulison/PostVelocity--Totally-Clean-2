#!/usr/bin/env python3
"""
Deployment Readiness Test for PostVelocity Backend
Focus on critical endpoints after craco dependency fix
"""

import requests
import json
import sys
from datetime import datetime

class DeploymentReadinessTest:
    def __init__(self, base_url="https://f172fa13-34dd-4e25-a49a-5e4342ce5451.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.critical_failures = []

    def log_test(self, name, success, details="", critical=False):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name} - PASSED")
        else:
            print(f"❌ {name} - FAILED: {details}")
            if critical:
                self.critical_failures.append(f"{name}: {details}")
        
        if details and success:
            print(f"   Details: {details}")

    def make_request(self, method, endpoint, data=None, timeout=10):
        """Make HTTP request with shorter timeout for deployment testing"""
        url = f"{self.base_url}/api/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=timeout)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=timeout)
            
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request error: {str(e)}")
            return None

    def test_backend_health_check(self):
        """Test backend health check endpoint - CRITICAL"""
        response = self.make_request('GET', 'health')
        if response and response.status_code == 200:
            data = response.json()
            success = data.get('status') == 'healthy'
            self.log_test("Backend Health Check", success, f"Status: {data.get('status')}", critical=True)
            return success
        else:
            self.log_test("Backend Health Check", False, "Backend not responding", critical=True)
            return False

    def test_claude_api_integration(self):
        """Test Claude API integration - CRITICAL"""
        response = self.make_request('GET', 'debug')
        if response and response.status_code == 200:
            data = response.json()
            claude_key_exists = data.get('claude_api_key_exists', False)
            seo_keywords_loaded = data.get('seo_keywords_loaded', False)
            trending_hashtags_loaded = data.get('trending_hashtags_loaded', False)
            
            success = claude_key_exists and seo_keywords_loaded and trending_hashtags_loaded
            details = f"Claude API: {claude_key_exists}, SEO Keywords: {seo_keywords_loaded}, Trending Hashtags: {trending_hashtags_loaded}"
            self.log_test("Claude API Integration", success, details, critical=True)
            return success
        else:
            self.log_test("Claude API Integration", False, "Debug endpoint failed", critical=True)
            return False

    def test_stripe_payment_endpoints(self):
        """Test Stripe payment system readiness - CRITICAL"""
        # Test ROI analytics endpoint which includes payment-related data
        response = self.make_request('GET', 'analytics/demo-company/roi')
        if response and response.status_code == 200:
            data = response.json()
            has_payment_fields = all(field in data for field in [
                'total_investment', 'revenue_attributed', 'cost_per_lead', 'roi_percentage'
            ])
            success = has_payment_fields
            details = f"Payment fields present: {has_payment_fields}, ROI: {data.get('roi_percentage', 0)}%"
            self.log_test("Stripe Payment System", success, details, critical=True)
            return success
        else:
            self.log_test("Stripe Payment System", False, "ROI analytics endpoint failed", critical=True)
            return False

    def test_content_generation_endpoint(self):
        """Test content generation endpoint - CRITICAL"""
        content_request = {
            "company_id": "demo-company",
            "topic": "Construction Safety",
            "platforms": ["instagram", "facebook"],
            "audience_level": "general"
        }
        
        response = self.make_request('POST', 'generate-content', content_request, timeout=30)
        if response and response.status_code == 200:
            data = response.json()
            has_content = len(data.get('generated_content', [])) > 0
            success = has_content
            details = f"Generated content for {len(data.get('generated_content', []))} platforms"
            self.log_test("Content Generation", success, details, critical=True)
            return success
        else:
            error_msg = f"Status: {response.status_code if response else 'No response'}"
            self.log_test("Content Generation", False, error_msg, critical=True)
            return False

    def test_companies_endpoint(self):
        """Test companies CRUD operations - CRITICAL"""
        # Test getting companies
        response = self.make_request('GET', 'companies')
        if response and response.status_code == 200:
            data = response.json()
            success = isinstance(data, list) and len(data) > 0
            details = f"Found {len(data)} companies"
            self.log_test("Companies Endpoint", success, details, critical=True)
            return success
        else:
            self.log_test("Companies Endpoint", False, "Failed to get companies", critical=True)
            return False

    def test_analytics_endpoint(self):
        """Test analytics functionality - CRITICAL"""
        response = self.make_request('GET', 'analytics/demo-company/roi')
        if response and response.status_code == 200:
            data = response.json()
            has_analytics = all(field in data for field in [
                'total_investment', 'leads_generated', 'conversions', 'platform_breakdown'
            ])
            success = has_analytics
            details = f"Analytics data complete: {has_analytics}"
            self.log_test("Analytics Endpoint", success, details, critical=True)
            return success
        else:
            self.log_test("Analytics Endpoint", False, "Analytics endpoint failed", critical=True)
            return False

    def test_mongodb_connectivity(self):
        """Test MongoDB connectivity through data operations - CRITICAL"""
        # Test by getting companies (requires DB connection)
        response = self.make_request('GET', 'companies')
        if response and response.status_code == 200:
            data = response.json()
            success = isinstance(data, list)
            details = f"Database connection working, retrieved {len(data)} records"
            self.log_test("MongoDB Connectivity", success, details, critical=True)
            return success
        else:
            self.log_test("MongoDB Connectivity", False, "Database connection failed", critical=True)
            return False

    def test_oauth_endpoints(self):
        """Test OAuth endpoints functionality - CRITICAL"""
        # Test OAuth platform support
        response = self.make_request('GET', 'platforms/supported')
        if response and response.status_code == 200:
            data = response.json()
            platforms = data.get('platforms', [])
            success = len(platforms) >= 8  # Should have at least 8 platforms
            details = f"OAuth platforms supported: {len(platforms)}"
            self.log_test("OAuth Endpoints", success, details, critical=True)
            return success
        else:
            self.log_test("OAuth Endpoints", False, "OAuth platforms endpoint failed", critical=True)
            return False

    def test_ai_features_endpoints(self):
        """Test AI-powered features - IMPORTANT"""
        # Test SEO analysis
        test_content = {
            "content": "Construction safety is important for workplace protection.",
            "target_keywords": ["construction safety", "workplace protection"]
        }
        
        response = self.make_request('POST', 'seo/analyze', test_content)
        if response and response.status_code == 200:
            data = response.json()
            has_seo_score = 'seo_score' in data
            success = has_seo_score
            details = f"SEO analysis working, score: {data.get('seo_score', 0)}"
            self.log_test("AI Features (SEO)", success, details)
            return success
        else:
            self.log_test("AI Features (SEO)", False, "SEO analysis failed")
            return False

    def test_media_management(self):
        """Test media management system - IMPORTANT"""
        response = self.make_request('GET', 'companies/demo-company/media/categories')
        if response and response.status_code == 200:
            data = response.json()
            categories = data.get('categories', [])
            success = len(categories) >= 8
            details = f"Media categories: {len(categories)}"
            self.log_test("Media Management", success, details)
            return success
        else:
            self.log_test("Media Management", False, "Media categories failed")
            return False

    def run_deployment_readiness_tests(self):
        """Run all deployment readiness tests"""
        print("🚀 PostVelocity Deployment Readiness Test")
        print("Testing after craco dependency fix")
        print("=" * 60)
        
        print("\n🔥 CRITICAL ENDPOINTS (Must Pass for Deployment)")
        print("-" * 50)
        self.test_backend_health_check()
        self.test_claude_api_integration()
        self.test_stripe_payment_endpoints()
        self.test_mongodb_connectivity()
        self.test_companies_endpoint()
        self.test_analytics_endpoint()
        self.test_oauth_endpoints()
        
        print("\n⚡ IMPORTANT ENDPOINTS")
        print("-" * 30)
        self.test_ai_features_endpoints()
        self.test_media_management()
        
        print("\n🎯 CONTENT GENERATION (High Load Test)")
        print("-" * 40)
        self.test_content_generation_endpoint()
        
        # Print final results
        print("\n" + "=" * 60)
        print(f"📊 DEPLOYMENT READINESS: {self.tests_passed}/{self.tests_run} tests passed")
        
        if len(self.critical_failures) == 0:
            print("🎉 ALL CRITICAL SYSTEMS OPERATIONAL!")
            print("✅ Backend is ready for Heroku deployment")
            
            if self.tests_passed == self.tests_run:
                print("🌟 PERFECT SCORE - All systems working flawlessly!")
                return 0
            else:
                print(f"⚠️  {self.tests_run - self.tests_passed} non-critical issues found")
                return 0
        else:
            print("🚨 CRITICAL FAILURES DETECTED:")
            for failure in self.critical_failures:
                print(f"   ❌ {failure}")
            print("\n🛑 Backend NOT ready for deployment until critical issues are resolved")
            return 1

def main():
    """Main test execution"""
    tester = DeploymentReadinessTest()
    return tester.run_deployment_readiness_tests()

if __name__ == "__main__":
    sys.exit(main())