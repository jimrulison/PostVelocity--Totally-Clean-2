#!/usr/bin/env python3
"""
Focused Testing for New Beta Feedback System and SEO Monitoring Add-on Features
"""

import requests
import json
import sys
from datetime import datetime, timedelta
import uuid

class NewFeaturesTester:
    def __init__(self, base_url="https://c19ec803-cffc-45c2-9889-95091f0edbcb.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.test_company_id = "687a62ec366953326ddff8de"  # Use existing company from previous test
        self.test_beta_user_id = None
        self.test_feedback_id = None
        self.test_seo_addon_id = None
        self.test_audit_id = None

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
                response = requests.get(url, headers=headers, params=params, timeout=15)
            elif method == 'POST':
                if params:  # For endpoints that expect query parameters
                    response = requests.post(url, headers=headers, params=params, timeout=15)
                else:
                    response = requests.post(url, json=data, headers=headers, timeout=15)
            elif method == 'PUT':
                if params:  # For endpoints that expect query parameters
                    response = requests.put(url, headers=headers, params=params, timeout=15)
                else:
                    response = requests.put(url, json=data, headers=headers, timeout=15)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=15)
            
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request error: {str(e)}")
            return None

    # Beta Feedback System Tests
    def test_beta_login(self):
        """Test beta user login/registration"""
        test_beta_params = {
            "beta_id": f"BETA{datetime.now().strftime('%H%M%S')}",
            "name": "John Safety Manager",
            "email": f"beta.tester.{datetime.now().strftime('%H%M%S')}@construction.com"
        }
        
        response = self.make_request('POST', 'beta/login', params=test_beta_params)
        if response and response.status_code == 200:
            data = response.json()
            success = data.get('status') == 'success' and 'user' in data
            self.test_beta_user_id = data.get('user', {}).get('beta_id')  # Store for other tests
            self.log_test("Beta Login", success, f"Beta user registered: {self.test_beta_user_id}")
            return success
        else:
            self.log_test("Beta Login", False, f"Status: {response.status_code if response else 'No response'}")
            return False

    def test_submit_beta_feedback(self):
        """Test submitting beta feedback"""
        if not self.test_beta_user_id:
            self.log_test("Submit Beta Feedback", False, "No beta user ID available")
            return False
            
        feedback_data = {
            "beta_user_id": self.test_beta_user_id,
            "beta_user_name": "John Safety Manager",
            "beta_user_email": "beta.tester@construction.com",
            "feedback_type": "feature_request",
            "title": "Enhanced Safety Training Module",
            "description": "Would love to see more interactive safety training content with VR integration for construction workers.",
            "priority": "medium",
            "status": "open",  # Required field
            "category": "training"
        }
        
        response = self.make_request('POST', 'beta/feedback', data=feedback_data)
        if response and response.status_code == 200:
            data = response.json()
            success = data.get('status') == 'success' and 'feedback' in data
            self.test_feedback_id = data.get('feedback', {}).get('id')  # Store for other tests
            self.log_test("Submit Beta Feedback", success, f"Feedback submitted: {self.test_feedback_id}")
            return success
        else:
            self.log_test("Submit Beta Feedback", False, f"Status: {response.status_code if response else 'No response'}")
            return False

    def test_get_beta_feedback(self):
        """Test getting all beta feedback"""
        response = self.make_request('GET', 'beta/feedback')
        if response and response.status_code == 200:
            data = response.json()
            feedback_list = data.get('feedback', [])
            success = isinstance(feedback_list, list)
            self.log_test("Get Beta Feedback", success, f"Retrieved {len(feedback_list)} feedback items")
            return success
        else:
            self.log_test("Get Beta Feedback", False, f"Status: {response.status_code if response else 'No response'}")
            return False

    def test_update_feedback_status(self):
        """Test updating feedback status (admin function)"""
        if not self.test_feedback_id:
            self.log_test("Update Feedback Status", False, "No feedback ID available")
            return False
            
        update_params = {
            "status": "in_progress",
            "admin_response": "Great suggestion! We're evaluating VR integration options.",
            "implementation_notes": "Researching VR training platforms for Q2 implementation"
        }
        
        response = self.make_request('PUT', f'beta/feedback/{self.test_feedback_id}', params=update_params)
        if response and response.status_code == 200:
            data = response.json()
            success = data.get('status') == 'updated' and data.get('feedback_status') == 'in_progress'
            self.log_test("Update Feedback Status", success, f"Feedback status updated to: {data.get('feedback_status')}")
            return success
        else:
            self.log_test("Update Feedback Status", False, f"Status: {response.status_code if response else 'No response'}")
            return False

    def test_vote_feedback(self):
        """Test voting on feedback"""
        if not self.test_feedback_id or not self.test_beta_user_id:
            self.log_test("Vote Feedback", False, "No feedback ID or beta user ID available")
            return False
            
        vote_params = {
            "beta_user_id": self.test_beta_user_id
        }
        
        response = self.make_request('POST', f'beta/feedback/{self.test_feedback_id}/vote', params=vote_params)
        if response and response.status_code == 200:
            data = response.json()
            success = data.get('status') == 'voted' and 'votes' in data
            self.log_test("Vote Feedback", success, f"Vote recorded, total votes: {data.get('votes', 0)}")
            return success
        else:
            self.log_test("Vote Feedback", False, f"Status: {response.status_code if response else 'No response'}")
            return False

    def test_get_beta_user_stats(self):
        """Test getting beta user statistics"""
        if not self.test_beta_user_id:
            self.log_test("Get Beta User Stats", False, "No beta user ID available")
            return False
            
        response = self.make_request('GET', f'beta/user/{self.test_beta_user_id}/stats')
        if response and response.status_code == 200:
            data = response.json()
            expected_fields = ['beta_user_id', 'name', 'email', 'contribution_score', 'feedback_count', 'status']
            has_required_fields = all(field in data for field in expected_fields)
            success = has_required_fields
            self.log_test("Get Beta User Stats", success, f"Stats: Score {data.get('contribution_score', 0)}, Feedback {data.get('feedback_count', 0)}")
            return success
        else:
            self.log_test("Get Beta User Stats", False, f"Status: {response.status_code if response else 'No response'}")
            return False

    def test_purchase_seo_addon(self):
        """Test purchasing SEO monitoring add-on"""
        if not self.test_company_id:
            self.log_test("Purchase SEO Addon", False, "No test company ID available")
            return False
            
        addon_params = {
            "company_id": self.test_company_id,
            "website_url": "https://safetyfirstconstruction.com",
            "notification_email": "seo@safetyfirstconstruction.com",
            "plan_type": "standard"
        }
        
        response = self.make_request('POST', 'seo-addon/purchase', params=addon_params)
        if response and response.status_code == 200:
            data = response.json()
            # Handle both new purchase and existing addon cases
            if data.get('status') == 'success':
                success = data.get('addon_id') is not None
                self.test_seo_addon_id = data.get('addon_id')
                self.log_test("Purchase SEO Addon", success, f"SEO addon purchased: {self.test_seo_addon_id}")
            elif data.get('status') == 'error' and 'already has' in data.get('message', ''):
                success = True  # Already exists is acceptable
                self.log_test("Purchase SEO Addon", success, "SEO addon already exists for company")
            else:
                success = False
                self.log_test("Purchase SEO Addon", success, f"Unexpected response: {data}")
            return success
        else:
            self.log_test("Purchase SEO Addon", False, f"Status: {response.status_code if response else 'No response'}")
            return False

    def test_get_seo_addon_status(self):
        """Test getting SEO addon status"""
        if not self.test_company_id:
            self.log_test("Get SEO Addon Status", False, "No test company ID available")
            return False
            
        response = self.make_request('GET', f'seo-addon/{self.test_company_id}/status')
        if response and response.status_code == 200:
            data = response.json()
            addon_data = data.get('addon', {})
            expected_fields = ['company_id', 'website_url', 'monitoring_status', 'daily_checks_limit', 'daily_checks_used']
            has_required_fields = all(field in addon_data for field in expected_fields)
            success = has_required_fields and addon_data.get('monitoring_status') in ['active', 'paused', 'expired']
            self.log_test("Get SEO Addon Status", success, f"Status: {addon_data.get('monitoring_status')}, Checks: {addon_data.get('daily_checks_used', 0)}/{addon_data.get('daily_checks_limit', 0)}")
            return success
        else:
            self.log_test("Get SEO Addon Status", False, f"Status: {response.status_code if response else 'No response'}")
            return False

    def test_get_latest_seo_parameters(self):
        """Test getting latest SEO parameters"""
        response = self.make_request('GET', 'seo-addon/parameters/latest')
        if response and response.status_code == 200:
            data = response.json()
            parameters = data.get('parameters', [])
            success = isinstance(parameters, list) and len(parameters) > 0
            if success and parameters:
                first_param = parameters[0]
                has_required_fields = all(field in first_param for field in ['parameter_name', 'parameter_value', 'source', 'importance_score', 'category'])
                success = has_required_fields
            self.log_test("Get Latest SEO Parameters", success, f"Retrieved {len(parameters)} SEO parameters")
            return success
        else:
            self.log_test("Get Latest SEO Parameters", False, f"Status: {response.status_code if response else 'No response'}")
            return False

    def test_run_website_audit(self):
        """Test running website SEO audit"""
        if not self.test_company_id:
            self.log_test("Run Website Audit", False, "No test company ID available")
            return False
            
        audit_params = {
            "page_url": "https://safetyfirstconstruction.com/safety-training"
        }
        
        response = self.make_request('POST', f'seo-addon/{self.test_company_id}/audit', params=audit_params)
        if response and response.status_code == 200:
            data = response.json()
            expected_fields = ['audit_id', 'overall_score', 'issues_found', 'recommendations', 'priority_fixes']
            has_required_fields = all(field in data for field in expected_fields)
            success = has_required_fields and isinstance(data.get('overall_score'), (int, float))
            self.test_audit_id = data.get('audit_id')  # Store for other tests
            self.log_test("Run Website Audit", success, f"Audit completed: Score {data.get('overall_score', 0)}, Issues: {len(data.get('issues_found', []))}")
            return success
        else:
            self.log_test("Run Website Audit", False, f"Status: {response.status_code if response else 'No response'}")
            return False

    def test_get_website_audits(self):
        """Test getting website audit history"""
        if not self.test_company_id:
            self.log_test("Get Website Audits", False, "No test company ID available")
            return False
            
        response = self.make_request('GET', f'seo-addon/{self.test_company_id}/audits', params={"limit": 5})
        if response and response.status_code == 200:
            data = response.json()
            audits = data.get('audits', [])
            success = isinstance(audits, list)
            self.log_test("Get Website Audits", success, f"Retrieved {len(audits)} audit records")
            return success
        else:
            self.log_test("Get Website Audits", False, f"Status: {response.status_code if response else 'No response'}")
            return False

    def test_run_daily_seo_research(self):
        """Test running daily SEO research"""
        response = self.make_request('POST', 'seo-addon/research/daily')
        if response and response.status_code == 200:
            data = response.json()
            success = data.get('status') == 'completed' and 'parameters_discovered' in data
            parameters_count = data.get('parameters_discovered', 0)
            self.log_test("Run Daily SEO Research", success, f"Research completed, discovered {parameters_count} new parameters")
            return success
        else:
            self.log_test("Run Daily SEO Research", False, f"Status: {response.status_code if response else 'No response'}")
            return False

    def run_new_features_tests(self):
        """Run tests for new Beta Feedback System and SEO Monitoring Add-on features"""
        print("🧪 Testing NEW Beta Feedback System and SEO Monitoring Add-on Features")
        print("=" * 80)
        
        print("\n🧪 Beta Feedback System Tests")
        print("-" * 40)
        self.test_beta_login()
        self.test_submit_beta_feedback()
        self.test_get_beta_feedback()
        self.test_update_feedback_status()
        self.test_vote_feedback()
        self.test_get_beta_user_stats()
        
        print("\n🔍 SEO Monitoring Add-on Tests")
        print("-" * 40)
        self.test_purchase_seo_addon()
        self.test_get_seo_addon_status()
        self.test_get_latest_seo_parameters()
        self.test_run_website_audit()
        self.test_get_website_audits()
        self.test_run_daily_seo_research()
        
        # Print final results
        print("\n" + "=" * 80)
        print(f"📊 NEW FEATURES TEST RESULTS: {self.tests_passed}/{self.tests_run} tests passed")
        
        if self.tests_passed == self.tests_run:
            print("🎉 ALL NEW FEATURES TESTS PASSED!")
            print("✨ New features working: Beta Feedback System, SEO Monitoring Add-on")
            return 0
        else:
            print(f"⚠️  {self.tests_run - self.tests_passed} tests failed. Check the issues above.")
            return 1

def main():
    """Main test execution"""
    print("PostVelocity - New Features Testing")
    print("Testing Beta Feedback System and SEO Monitoring Add-on")
    print()
    
    tester = NewFeaturesTester()
    return tester.run_new_features_tests()

if __name__ == "__main__":
    sys.exit(main())