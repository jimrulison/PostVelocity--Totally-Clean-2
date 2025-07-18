#!/usr/bin/env python3
"""
Beta Feedback System Testing - Focused Testing for 6 Beta Endpoints
Tests all beta feedback functionality with proper response format validation
"""

import requests
import json
import sys
from datetime import datetime
import uuid

class BetaFeedbackTester:
    def __init__(self, base_url="https://c19ec803-cffc-45c2-9889-95091f0edbcb.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.test_beta_user_id = None
        self.test_feedback_id = None

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
                if data:
                    response = requests.post(url, json=data, headers=headers, params=params, timeout=30)
                else:
                    response = requests.post(url, headers=headers, params=params, timeout=30)
            elif method == 'PUT':
                if data:
                    response = requests.put(url, json=data, headers=headers, params=params, timeout=30)
                else:
                    response = requests.put(url, headers=headers, params=params, timeout=30)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=30)
            
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request error: {str(e)}")
            return None

    def make_request_form(self, method, endpoint, data=None, params=None):
        """Make HTTP request with form data"""
        url = f"{self.base_url}/api/{endpoint}"
        
        try:
            if method == 'POST':
                response = requests.post(url, data=data, timeout=30)
            elif method == 'PUT':
                response = requests.put(url, data=data, timeout=30)
            else:
                # Fallback to regular request
                return self.make_request(method, endpoint, data, params)
            
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request error: {str(e)}")
            return None

    def test_beta_login(self):
        """Test 1: POST /api/beta/login - Beta user login/registration"""
        test_beta_data = {
            "beta_id": f"BETA{datetime.now().strftime('%H%M%S')}",
            "name": "Sarah Construction Manager",
            "email": f"sarah.manager.{datetime.now().strftime('%H%M%S')}@safetyfirst.com"
        }
        
        # Send as query parameters
        response = self.make_request('POST', 'beta/login', params=test_beta_data)
        if response and response.status_code == 200:
            data = response.json()
            
            # Check response format
            has_status = data.get('status') == 'success'
            has_user = 'user' in data and isinstance(data['user'], dict)
            has_message = 'message' in data
            
            if has_user:
                user = data['user']
                has_user_id = 'id' in user
                has_beta_id = user.get('beta_id') == test_beta_data['beta_id']
                has_name = user.get('name') == test_beta_data['name']
                has_email = user.get('email') == test_beta_data['email']
                
                user_valid = has_user_id and has_beta_id and has_name and has_email
                self.test_beta_user_id = user.get('beta_id')  # Store for other tests
            else:
                user_valid = False
            
            success = has_status and has_user and has_message and user_valid
            details = f"Status: {data.get('status')}, User ID: {self.test_beta_user_id}, Message: {data.get('message')}"
            
            self.log_test("Beta Login/Registration", success, details)
            return success
        else:
            error_msg = f"Status: {response.status_code if response else 'No response'}"
            if response:
                try:
                    error_data = response.json()
                    error_msg += f", Error: {error_data.get('detail', 'Unknown error')}"
                except:
                    error_msg += f", Response: {response.text[:200]}"
            self.log_test("Beta Login/Registration", False, error_msg)
            return False

    def test_submit_beta_feedback(self):
        """Test 2: POST /api/beta/feedback - Submit new feedback"""
        if not self.test_beta_user_id:
            self.log_test("Submit Beta Feedback", False, "No beta user ID available")
            return False
            
        feedback_data = {
            "beta_user_id": self.test_beta_user_id,
            "beta_user_name": "Sarah Construction Manager",
            "beta_user_email": "sarah.manager@safetyfirst.com",
            "feedback_type": "feature_request",
            "title": "Advanced Safety Analytics Dashboard",
            "description": "Would love to see real-time safety incident tracking with predictive analytics to prevent accidents before they happen. Integration with wearable safety devices would be amazing.",
            "priority": "high",
            "status": "open",  # Required field
            "category": "safety_analytics"
        }
        
        response = self.make_request('POST', 'beta/feedback', feedback_data)
        if response and response.status_code == 200:
            data = response.json()
            
            # Check expected response format: {"status": "submitted", "feedback_id": "...", "feedback": {...}}
            has_status = data.get('status') == 'submitted'
            has_feedback_id = 'feedback_id' in data and data['feedback_id']
            has_feedback = 'feedback' in data and isinstance(data['feedback'], dict)
            
            if has_feedback:
                feedback = data['feedback']
                has_title = feedback.get('title') == feedback_data['title']
                has_description = feedback.get('description') == feedback_data['description']
                has_user_id = feedback.get('beta_user_id') == feedback_data['beta_user_id']
                has_created_at = 'created_at' in feedback
                has_votes = 'votes' in feedback and feedback['votes'] == 0
                has_open_status = feedback.get('status') == 'open'
                
                feedback_valid = all([has_title, has_description, has_user_id, has_created_at, has_votes, has_open_status])
                self.test_feedback_id = data.get('feedback_id')  # Store for other tests
            else:
                feedback_valid = False
            
            success = has_status and has_feedback_id and has_feedback and feedback_valid
            details = f"Status: {data.get('status')}, Feedback ID: {self.test_feedback_id}, Title: {feedback.get('title') if has_feedback else 'N/A'}"
            
            self.log_test("Submit Beta Feedback", success, details)
            return success
        else:
            error_msg = f"Status: {response.status_code if response else 'No response'}"
            if response:
                try:
                    error_data = response.json()
                    error_msg += f", Error: {error_data.get('detail', 'Unknown error')}"
                except:
                    error_msg += f", Response: {response.text[:200]}"
            self.log_test("Submit Beta Feedback", False, error_msg)
            return False

    def test_get_beta_feedback(self):
        """Test 3: GET /api/beta/feedback - Get all beta feedback"""
        response = self.make_request('GET', 'beta/feedback')
        if response and response.status_code == 200:
            data = response.json()
            
            # Check response format
            has_feedback_list = 'feedback' in data and isinstance(data['feedback'], list)
            
            if has_feedback_list:
                feedback_list = data['feedback']
                list_not_empty = len(feedback_list) > 0
                
                if list_not_empty:
                    # Check first feedback item structure
                    first_feedback = feedback_list[0]
                    has_required_fields = all(field in first_feedback for field in [
                        'id', 'beta_user_id', 'beta_user_name', 'beta_user_email',
                        'feedback_type', 'title', 'description', 'priority', 'status'
                    ])
                    
                    # Check if our submitted feedback is in the list
                    our_feedback_found = any(f.get('id') == self.test_feedback_id for f in feedback_list) if self.test_feedback_id else False
                    
                    structure_valid = has_required_fields
                else:
                    structure_valid = True  # Empty list is valid
                    our_feedback_found = False
            else:
                structure_valid = False
                list_not_empty = False
                our_feedback_found = False
            
            success = has_feedback_list and structure_valid
            details = f"Retrieved {len(feedback_list) if has_feedback_list else 0} feedback items, Our feedback found: {our_feedback_found}"
            
            self.log_test("Get All Beta Feedback", success, details)
            return success
        else:
            error_msg = f"Status: {response.status_code if response else 'No response'}"
            if response:
                try:
                    error_data = response.json()
                    error_msg += f", Error: {error_data.get('detail', 'Unknown error')}"
                except:
                    error_msg += f", Response: {response.text[:200]}"
            self.log_test("Get All Beta Feedback", False, error_msg)
            return False

    def test_update_feedback_status(self):
        """Test 4: PUT /api/beta/feedback/{feedback_id} - Update feedback status (admin function)"""
        if not self.test_feedback_id:
            self.log_test("Update Feedback Status", False, "No feedback ID available")
            return False
            
        update_params = {
            "status": "in_progress",
            "admin_response": "Excellent suggestion! We're actively researching predictive safety analytics and wearable device integration for Q2 2025 implementation.",
            "implementation_notes": "Phase 1: Research wearable device APIs, Phase 2: Develop predictive models, Phase 3: Dashboard integration"
        }
        
        # Send as query parameters
        response = self.make_request('PUT', f'beta/feedback/{self.test_feedback_id}', params=update_params)
        if response and response.status_code == 200:
            data = response.json()
            
            # Check expected response format: {"status": "updated", "message": "Feedback updated", "feedback_status": "..."}
            has_status = data.get('status') == 'updated'
            has_message = data.get('message') == 'Feedback updated'
            has_feedback_status = data.get('feedback_status') == update_params['status']
            
            success = has_status and has_message and has_feedback_status
            details = f"Status: {data.get('status')}, Message: {data.get('message')}, Feedback Status: {data.get('feedback_status')}"
            
            self.log_test("Update Feedback Status", success, details)
            return success
        else:
            error_msg = f"Status: {response.status_code if response else 'No response'}"
            if response:
                try:
                    error_data = response.json()
                    error_msg += f", Error: {error_data.get('detail', 'Unknown error')}"
                except:
                    error_msg += f", Response: {response.text[:200]}"
            self.log_test("Update Feedback Status", False, error_msg)
            return False

    def test_vote_feedback(self):
        """Test 5: POST /api/beta/feedback/{feedback_id}/vote - Vote on feedback"""
        if not self.test_feedback_id:
            self.log_test("Vote on Feedback", False, "No feedback ID available")
            return False
        if not self.test_beta_user_id:
            self.log_test("Vote on Feedback", False, "No beta user ID available")
            return False
            
        vote_params = {
            "beta_user_id": self.test_beta_user_id
        }
        
        # Send as query parameters
        response = self.make_request('POST', f'beta/feedback/{self.test_feedback_id}/vote', params=vote_params)
        if response and response.status_code == 200:
            data = response.json()
            
            # Check expected response format: {"status": "voted", "message": "Vote recorded", "votes": X}
            has_status = data.get('status') == 'voted'
            has_message = data.get('message') == 'Vote recorded'
            has_votes = 'votes' in data and isinstance(data['votes'], int) and data['votes'] > 0
            
            success = has_status and has_message and has_votes
            details = f"Status: {data.get('status')}, Message: {data.get('message')}, Total Votes: {data.get('votes', 0)}"
            
            self.log_test("Vote on Feedback", success, details)
            return success
        else:
            error_msg = f"Status: {response.status_code if response else 'No response'}"
            if response:
                try:
                    error_data = response.json()
                    error_msg += f", Error: {error_data.get('detail', 'Unknown error')}"
                except:
                    error_msg += f", Response: {response.text[:200]}"
            self.log_test("Vote on Feedback", False, error_msg)
            return False

    def test_get_beta_user_stats(self):
        """Test 6: GET /api/beta/user/{beta_user_id}/stats - Get user statistics"""
        if not self.test_beta_user_id:
            self.log_test("Get Beta User Stats", False, "No beta user ID available")
            return False
            
        response = self.make_request('GET', f'beta/user/{self.test_beta_user_id}/stats')
        if response and response.status_code == 200:
            data = response.json()
            
            # Check expected response format with proper field mapping
            expected_fields = ['beta_user_id', 'name', 'email', 'contribution_score', 'feedback_count', 'status']
            has_required_fields = all(field in data for field in expected_fields)
            
            # Validate field values
            has_correct_user_id = data.get('beta_user_id') == self.test_beta_user_id
            has_valid_contribution_score = isinstance(data.get('contribution_score'), int) and data.get('contribution_score') >= 0
            has_valid_feedback_count = isinstance(data.get('feedback_count'), int) and data.get('feedback_count') >= 1  # Should be at least 1 from our submission
            has_valid_status = data.get('status') in ['active', 'inactive', 'vip']
            has_name = data.get('name') and isinstance(data.get('name'), str)
            has_email = data.get('email') and isinstance(data.get('email'), str)
            
            # Check optional fields
            has_implemented_count = 'implemented_count' in data
            has_joined_at = 'joined_at' in data
            has_special_privileges = 'special_privileges' in data
            
            field_validation = all([
                has_correct_user_id, has_valid_contribution_score, has_valid_feedback_count,
                has_valid_status, has_name, has_email
            ])
            
            success = has_required_fields and field_validation
            details = f"User: {data.get('name')}, Score: {data.get('contribution_score', 0)}, Feedback: {data.get('feedback_count', 0)}, Status: {data.get('status')}"
            
            self.log_test("Get Beta User Stats", success, details)
            return success
        else:
            error_msg = f"Status: {response.status_code if response else 'No response'}"
            if response:
                try:
                    error_data = response.json()
                    error_msg += f", Error: {error_data.get('detail', 'Unknown error')}"
                except:
                    error_msg += f", Response: {response.text[:200]}"
            self.log_test("Get Beta User Stats", False, error_msg)
            return False

    def run_beta_feedback_tests(self):
        """Run all Beta Feedback System tests in proper workflow order"""
        print("🧪 BETA FEEDBACK SYSTEM TESTING - 6 Endpoints")
        print("=" * 60)
        print("Testing workflow: Register → Submit → Get All → Update → Vote → Stats")
        print()
        
        # Test workflow in proper order
        print("1️⃣ Testing Beta User Registration/Login")
        test1_success = self.test_beta_login()
        
        print("\n2️⃣ Testing Feedback Submission")
        test2_success = self.test_submit_beta_feedback()
        
        print("\n3️⃣ Testing Get All Feedback")
        test3_success = self.test_get_beta_feedback()
        
        print("\n4️⃣ Testing Update Feedback Status (Admin)")
        test4_success = self.test_update_feedback_status()
        
        print("\n5️⃣ Testing Vote on Feedback")
        test5_success = self.test_vote_feedback()
        
        print("\n6️⃣ Testing Get User Statistics")
        test6_success = self.test_get_beta_user_stats()
        
        # Print final results
        print("\n" + "=" * 60)
        print(f"📊 BETA FEEDBACK SYSTEM RESULTS: {self.tests_passed}/{self.tests_run} tests passed")
        
        if self.tests_passed == self.tests_run:
            print("🎉 ALL BETA FEEDBACK TESTS PASSED!")
            print("✅ All 6 endpoints working correctly with proper response formats")
            print("✅ Full workflow completed successfully")
            print("✅ Data persistence verified")
            print("✅ Response format validation passed")
            return 0
        else:
            print(f"⚠️  {self.tests_run - self.tests_passed} tests failed. Check the issues above.")
            
            # Provide specific failure analysis
            failed_tests = []
            if not test1_success:
                failed_tests.append("Beta Login/Registration")
            if not test2_success:
                failed_tests.append("Submit Feedback")
            if not test3_success:
                failed_tests.append("Get All Feedback")
            if not test4_success:
                failed_tests.append("Update Feedback Status")
            if not test5_success:
                failed_tests.append("Vote on Feedback")
            if not test6_success:
                failed_tests.append("Get User Statistics")
            
            print(f"❌ Failed tests: {', '.join(failed_tests)}")
            return 1

def main():
    """Main test execution"""
    print("PostVelocity - Beta Feedback System Testing")
    print("Testing against: https://c19ec803-cffc-45c2-9889-95091f0edbcb.preview.emergentagent.com")
    print()
    
    tester = BetaFeedbackTester()
    return tester.run_beta_feedback_tests()

if __name__ == "__main__":
    sys.exit(main())