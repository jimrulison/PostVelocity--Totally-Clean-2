#!/usr/bin/env python3
"""
Focused Backend API Testing for Phase 6 Verification
Tests core functionality to ensure no regressions after UI enhancements
"""

import requests
import json
import sys
from datetime import datetime, timedelta
import uuid

class FocusedAPITester:
    def __init__(self, base_url="https://944873b2-f626-40e9-9438-c3331bff2788.preview.emergentagent.com"):
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

    def make_request(self, method, endpoint, data=None, params=None, timeout=60):
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

    def test_core_endpoints(self):
        """Test core system endpoints"""
        print("🔍 Testing Core System Endpoints")
        print("-" * 40)
        
        # Health check
        response = self.make_request('GET', 'health')
        if response and response.status_code == 200:
            data = response.json()
            success = data.get('status') == 'healthy'
            self.log_test("Health Check", success, f"Status: {data.get('status')}")
        else:
            self.log_test("Health Check", False, "Failed to connect")

        # Debug endpoint
        response = self.make_request('GET', 'debug')
        if response and response.status_code == 200:
            data = response.json()
            claude_key_exists = data.get('claude_api_key_exists', False)
            seo_loaded = data.get('seo_keywords_loaded', False)
            hashtags_loaded = data.get('trending_hashtags_loaded', False)
            self.log_test("Debug Endpoint", True, f"Claude: {claude_key_exists}, SEO: {seo_loaded}, Hashtags: {hashtags_loaded}")
        else:
            self.log_test("Debug Endpoint", False, "Failed to get debug info")

        # Platforms
        response = self.make_request('GET', 'platforms')
        if response and response.status_code == 200:
            data = response.json()
            platforms = data.get('platforms', [])
            expected_platforms = ['instagram', 'tiktok', 'facebook', 'youtube', 'whatsapp', 'snapchat', 'x', 'linkedin']
            success = len(platforms) >= 8 and all(p in platforms for p in expected_platforms)
            self.log_test("Platforms Endpoint", success, f"Found {len(platforms)} platforms")
        else:
            self.log_test("Platforms Endpoint", False, "Failed to get platforms")

    def test_company_management(self):
        """Test company CRUD operations"""
        print("\n📊 Testing Company Management")
        print("-" * 40)
        
        # Create company
        test_company = {
            "name": f"Phase6 Test Company {datetime.now().strftime('%H%M%S')}",
            "industry": "construction",
            "website": "https://phase6test.com",
            "description": "Testing Phase 6 backend functionality",
            "target_audience": "Construction workers, safety managers",
            "brand_voice": "Professional, safety-focused"
        }
        
        response = self.make_request('POST', 'companies', test_company)
        if response and response.status_code == 200:
            data = response.json()
            self.test_company_id = data.get('id')
            success = self.test_company_id is not None
            self.log_test("Create Company", success, f"Created company: {self.test_company_id}")
        else:
            self.log_test("Create Company", False, f"Status: {response.status_code if response else 'No response'}")

        # Get companies
        response = self.make_request('GET', 'companies')
        if response and response.status_code == 200:
            data = response.json()
            success = isinstance(data, list) and len(data) > 0
            self.log_test("Get Companies", success, f"Found {len(data)} companies")
        else:
            self.log_test("Get Companies", False, "Failed to get companies")

        # Get company by ID
        if self.test_company_id:
            response = self.make_request('GET', f'companies/{self.test_company_id}')
            if response and response.status_code == 200:
                data = response.json()
                success = data.get('id') == self.test_company_id
                self.log_test("Get Company by ID", success, f"Retrieved: {data.get('name')}")
            else:
                self.log_test("Get Company by ID", False, "Failed to get company")

        # Update company
        if self.test_company_id:
            update_data = {
                "description": "Updated for Phase 6 testing"
            }
            response = self.make_request('PUT', f'companies/{self.test_company_id}', update_data)
            if response and response.status_code == 200:
                data = response.json()
                success = "Updated" in data.get('description', '')
                self.log_test("Update Company", success, "Company updated successfully")
            else:
                self.log_test("Update Company", False, f"Status: {response.status_code if response else 'No response'}")

    def test_content_generation(self):
        """Test content generation API"""
        print("\n🎨 Testing Content Generation")
        print("-" * 40)
        
        if not self.test_company_id:
            self.log_test("Content Generation", False, "No test company ID available")
            return

        content_request = {
            "company_id": self.test_company_id,
            "topic": "Phase 6 Safety Training Updates",
            "platforms": ["instagram", "facebook", "linkedin"],
            "audience_level": "intermediate",
            "additional_context": "Focus on new safety protocols",
            "generate_blog": False,
            "seo_focus": True,
            "target_keywords": ["safety training", "construction safety"]
        }
        
        response = self.make_request('POST', 'generate-content', content_request, timeout=90)
        if response and response.status_code == 200:
            data = response.json()
            
            # Check basic structure
            has_content = len(data.get('generated_content', [])) > 0
            platforms_generated = [content.get('platform') for content in data.get('generated_content', [])]
            platforms_match = all(p in content_request['platforms'] for p in platforms_generated)
            
            success = has_content and platforms_match
            details = f"Generated content for {len(data.get('generated_content', []))} platforms"
            
            self.log_test("Content Generation", success, details)
        else:
            error_msg = f"Status: {response.status_code if response else 'No response'}"
            if response and response.status_code != 200:
                try:
                    error_data = response.json()
                    error_msg += f", Error: {error_data.get('detail', 'Unknown error')}"
                except:
                    error_msg += f", Response: {response.text[:200]}"
            self.log_test("Content Generation", False, error_msg)

    def test_ai_features(self):
        """Test AI-powered features"""
        print("\n🧠 Testing AI Features")
        print("-" * 40)
        
        # SEO Analysis
        test_content = {
            "content": "Construction safety is crucial for workplace protection. OSHA compliance ensures worker safety through proper training and equipment usage.",
            "target_keywords": ["construction safety", "OSHA compliance"]
        }
        
        response = self.make_request('POST', 'seo/analyze', test_content)
        if response and response.status_code == 200:
            data = response.json()
            has_seo_score = 'seo_score' in data
            has_recommendations = 'recommendations' in data
            success = has_seo_score and has_recommendations
            self.log_test("SEO Analysis", success, f"SEO Score: {data.get('seo_score', 0)}")
        else:
            self.log_test("SEO Analysis", False, f"Status: {response.status_code if response else 'No response'}")

        # Hashtag Analysis
        test_hashtags = {
            "hashtags": ["#BuildSafe", "#ConstructionLife", "#SafetyFirst"],
            "industry": "construction"
        }
        
        response = self.make_request('POST', 'hashtags/analyze', test_hashtags)
        if response and response.status_code == 200:
            data = response.json()
            hashtag_analysis = data.get('hashtag_analysis', [])
            success = len(hashtag_analysis) > 0
            self.log_test("Hashtag Analysis", success, f"Analyzed {len(hashtag_analysis)} hashtags")
        else:
            self.log_test("Hashtag Analysis", False, f"Status: {response.status_code if response else 'No response'}")

        # Trending Hashtags
        response = self.make_request('GET', 'hashtags/trending/construction')
        if response and response.status_code == 200:
            data = response.json()
            has_trending = 'trending_hashtags' in data
            success = has_trending
            self.log_test("Trending Hashtags", success, f"Industry: {data.get('industry')}")
        else:
            self.log_test("Trending Hashtags", False, f"Status: {response.status_code if response else 'No response'}")

    def test_analytics_features(self):
        """Test analytics and ROI features"""
        print("\n📈 Testing Analytics Features")
        print("-" * 40)
        
        if not self.test_company_id:
            self.log_test("ROI Analytics", False, "No test company ID available")
            return

        # ROI Analytics
        response = self.make_request('GET', f'analytics/{self.test_company_id}/roi')
        if response and response.status_code == 200:
            data = response.json()
            expected_fields = ['total_investment', 'leads_generated', 'conversions', 'revenue_attributed', 
                             'cost_per_lead', 'roi_percentage', 'platform_breakdown']
            has_required_fields = all(field in data for field in expected_fields)
            success = has_required_fields
            self.log_test("ROI Analytics", success, f"ROI: {data.get('roi_percentage', 0)}%")
        else:
            self.log_test("ROI Analytics", False, f"Status: {response.status_code if response else 'No response'}")

    def test_media_management(self):
        """Test media management features"""
        print("\n📁 Testing Media Management")
        print("-" * 40)
        
        if not self.test_company_id:
            self.log_test("Media Categories", False, "No test company ID available")
            return

        # Media Categories
        response = self.make_request('GET', f'companies/{self.test_company_id}/media/categories')
        if response and response.status_code == 200:
            data = response.json()
            categories = data.get('categories', [])
            expected_categories = ['training', 'equipment', 'workplace', 'team', 'projects', 'safety', 'certificates', 'events']
            success = len(categories) >= 8 and all(cat in categories for cat in expected_categories)
            self.log_test("Media Categories", success, f"Found {len(categories)} categories")
        else:
            self.log_test("Media Categories", False, f"Status: {response.status_code if response else 'No response'}")

        # Company Media
        response = self.make_request('GET', f'companies/{self.test_company_id}/media')
        if response and response.status_code == 200:
            data = response.json()
            success = isinstance(data, list)
            self.log_test("Get Company Media", success, f"Retrieved {len(data)} media files")
        else:
            self.log_test("Get Company Media", False, f"Status: {response.status_code if response else 'No response'}")

        # Monthly Media Requests
        response = self.make_request('GET', 'media/requests/monthly')
        if response and response.status_code == 200:
            data = response.json()
            requests_list = data.get('requests', [])
            success = isinstance(requests_list, list)
            self.log_test("Monthly Media Requests", success, f"Found {len(requests_list)} companies needing media")
        else:
            self.log_test("Monthly Media Requests", False, f"Status: {response.status_code if response else 'No response'}")

    def test_beta_feedback_system(self):
        """Test Beta Feedback System endpoints"""
        print("\n🧪 Testing Beta Feedback System")
        print("-" * 40)
        
        # Beta Login
        test_beta_data = {
            "beta_id": f"PHASE6{datetime.now().strftime('%H%M%S')}",
            "name": "Phase 6 Tester",
            "email": f"phase6.tester.{datetime.now().strftime('%H%M%S')}@test.com"
        }
        
        response = self.make_request('POST', 'beta/login', test_beta_data)
        if response and response.status_code == 200:
            data = response.json()
            success = data.get('beta_user_id') is not None
            beta_user_id = data.get('beta_user_id')
            self.log_test("Beta Login", success, f"Beta user registered: {beta_user_id}")
            
            if success:
                # Submit Beta Feedback
                feedback_data = {
                    "beta_user_id": beta_user_id,
                    "beta_user_name": "Phase 6 Tester",
                    "beta_user_email": test_beta_data["email"],
                    "feedback_type": "feature_request",
                    "title": "Phase 6 UI Enhancement Feedback",
                    "description": "The new Phase 6 UI enhancements are working great!",
                    "priority": "medium",
                    "category": "ui"
                }
                
                response = self.make_request('POST', 'beta/feedback', feedback_data)
                if response and response.status_code == 200:
                    data = response.json()
                    success = data.get('feedback_id') is not None
                    self.log_test("Submit Beta Feedback", success, f"Feedback submitted: {data.get('feedback_id')}")
                else:
                    self.log_test("Submit Beta Feedback", False, f"Status: {response.status_code if response else 'No response'}")
        else:
            self.log_test("Beta Login", False, f"Status: {response.status_code if response else 'No response'}")

        # Get Beta Feedback
        response = self.make_request('GET', 'beta/feedback')
        if response and response.status_code == 200:
            data = response.json()
            feedback_list = data.get('feedback', [])
            success = isinstance(feedback_list, list)
            self.log_test("Get Beta Feedback", success, f"Retrieved {len(feedback_list)} feedback items")
        else:
            self.log_test("Get Beta Feedback", False, f"Status: {response.status_code if response else 'No response'}")

    def test_seo_addon_system(self):
        """Test SEO Addon System endpoints"""
        print("\n🔍 Testing SEO Addon System")
        print("-" * 40)
        
        if not self.test_company_id:
            self.log_test("SEO Addon Purchase", False, "No test company ID available")
            return

        # Purchase SEO Addon
        addon_data = {
            "company_id": self.test_company_id,
            "website_url": "https://phase6test.com",
            "notification_email": "seo@phase6test.com",
            "plan_type": "standard"
        }
        
        response = self.make_request('POST', 'seo-addon/purchase', addon_data)
        if response and response.status_code == 200:
            data = response.json()
            success = data.get('status') == 'success'
            self.log_test("SEO Addon Purchase", success, f"Addon activated: {data.get('message', '')}")
        else:
            self.log_test("SEO Addon Purchase", False, f"Status: {response.status_code if response else 'No response'}")

        # Get SEO Addon Status
        response = self.make_request('GET', f'seo-addon/{self.test_company_id}/status')
        if response and response.status_code == 200:
            data = response.json()
            expected_fields = ['company_id', 'website_url', 'monitoring_status']
            has_required_fields = all(field in data for field in expected_fields)
            success = has_required_fields
            self.log_test("Get SEO Addon Status", success, f"Status: {data.get('monitoring_status')}")
        else:
            self.log_test("Get SEO Addon Status", False, f"Status: {response.status_code if response else 'No response'}")

    def run_focused_tests(self):
        """Run focused tests for Phase 6 verification"""
        print("🚀 Phase 6 Backend Verification Testing")
        print("=" * 50)
        print("Testing core functionality after UI enhancements")
        print()
        
        self.test_core_endpoints()
        self.test_company_management()
        self.test_content_generation()
        self.test_ai_features()
        self.test_analytics_features()
        self.test_media_management()
        self.test_beta_feedback_system()
        self.test_seo_addon_system()
        
        # Print final results
        print("\n" + "=" * 50)
        print(f"📊 FINAL RESULTS: {self.tests_passed}/{self.tests_run} tests passed")
        
        success_rate = (self.tests_passed / self.tests_run) * 100 if self.tests_run > 0 else 0
        
        if success_rate >= 95:
            print("🎉 EXCELLENT! Backend is working perfectly after Phase 6 enhancements!")
        elif success_rate >= 85:
            print("✅ GOOD! Backend is mostly functional with minor issues.")
        elif success_rate >= 70:
            print("⚠️  MODERATE! Backend has some issues that need attention.")
        else:
            print("❌ CRITICAL! Backend has significant issues that need immediate attention.")
        
        print(f"Success Rate: {success_rate:.1f}%")
        
        return 0 if success_rate >= 85 else 1

def main():
    """Main test execution"""
    print("PostVelocity Backend API Testing - Phase 6 Verification")
    print("Testing against: https://944873b2-f626-40e9-9438-c3331bff2788.preview.emergentagent.com")
    print()
    
    tester = FocusedAPITester()
    return tester.run_focused_tests()

if __name__ == "__main__":
    sys.exit(main())