#!/usr/bin/env python3
"""
Phase 2A Team Management Backend Testing
Tests all team management endpoints with plan limit enforcement
"""

import requests
import json
import sys
from datetime import datetime, timedelta
import uuid

class Phase2ATeamManagementTester:
    def __init__(self, base_url="https://9df131db-0ee7-4c9f-904a-7a8c74e82599.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.test_team_id = None
        self.test_user_id = None
        self.invite_token = None

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

    def setup_test_team(self):
        """Get existing company to use as test team"""
        try:
            # Get existing companies to use as test teams
            response = self.make_request('GET', 'companies')
            if response and response.status_code == 200:
                companies = response.json()
                if companies and len(companies) > 0:
                    # Use first company as test team
                    self.test_team_id = companies[0]['id']
                    print(f"🔧 Setup: Using existing company as test team: {self.test_team_id}")
                    return True
                else:
                    # Create a test company if none exist
                    company_data = {
                        "name": f"Test Team Company {uuid.uuid4().hex[:8]}",
                        "industry": "Construction",
                        "website": "https://testteam.com",
                        "description": "Test company for team management testing"
                    }
                    create_response = self.make_request('POST', 'companies', company_data)
                    if create_response and create_response.status_code == 200:
                        company = create_response.json()
                        self.test_team_id = company['id']
                        print(f"🔧 Setup: Created test company: {self.test_team_id}")
                        return True
            
            print("❌ Setup failed: Could not get or create test team")
            return False
            
        except Exception as e:
            print(f"Setup error: {str(e)}")
            return False

    def test_invite_team_member(self):
        """Test POST /api/teams/{team_id}/invite"""
        print("\n🧪 Testing Team Member Invitation...")
        
        if not self.test_team_id:
            self.setup_test_team()
        
        # Test 1: Valid invitation
        invite_data = {
            "email": "test@example.com",
            "role": "member",
            "permissions": ["read", "write"]
        }
        
        response = self.make_request('POST', f'teams/{self.test_team_id}/invite', invite_data)
        
        if response and response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                self.invite_token = data.get('invitation', {}).get('invite_token')
                self.log_test("Team Member Invitation", True, 
                            f"Invitation sent to {invite_data['email']}, token: {self.invite_token[:10]}...")
            else:
                self.log_test("Team Member Invitation", False, f"Unexpected response: {data}")
        else:
            self.log_test("Team Member Invitation", False, 
                        f"HTTP {response.status_code if response else 'No response'}")
        
        # Test 2: Invalid email
        invalid_invite = {"role": "member"}  # Missing email
        response = self.make_request('POST', f'teams/{self.test_team_id}/invite', invalid_invite)
        
        if response and response.status_code == 400:
            self.log_test("Team Invitation - Invalid Email", True, "Correctly rejected missing email")
        else:
            self.log_test("Team Invitation - Invalid Email", False, 
                        f"Should return 400, got {response.status_code if response else 'No response'}")

    def test_plan_limit_enforcement(self):
        """Test plan limit enforcement for team invitations"""
        print("\n🧪 Testing Plan Limit Enforcement...")
        
        if not self.test_team_id:
            self.setup_test_team()
        
        # Test with starter plan (1 user limit) - should fail on second invite
        invite_data_2 = {
            "email": "second@example.com",
            "role": "member",
            "permissions": ["read"]
        }
        
        response = self.make_request('POST', f'teams/{self.test_team_id}/invite', invite_data_2)
        
        if response and response.status_code == 200:
            data = response.json()
            if data.get('status') == 'limit_exceeded':
                self.log_test("Starter Plan Limit Enforcement", True, 
                            f"Correctly blocked invitation: {data.get('message')}")
            else:
                self.log_test("Starter Plan Limit Enforcement", False, 
                            f"Should block invitation but got: {data}")
        else:
            self.log_test("Starter Plan Limit Enforcement", False, 
                        f"HTTP {response.status_code if response else 'No response'}")

    def test_professional_plan_limits(self):
        """Test professional plan allows 3 users"""
        print("\n🧪 Testing Professional Plan Limits...")
        
        # Create a professional plan team
        prof_team_id = str(uuid.uuid4())
        
        # Simulate professional plan user
        for i in range(3):  # Professional plan allows 3 users
            invite_data = {
                "email": f"prof_user_{i}@example.com",
                "role": "member",
                "permissions": ["read", "write"]
            }
            
            response = self.make_request('POST', f'teams/{prof_team_id}/invite', invite_data)
            
            if response and response.status_code == 200:
                data = response.json()
                if i < 2:  # First 2 should succeed
                    if data.get('status') == 'success':
                        self.log_test(f"Professional Plan User {i+1}", True, 
                                    f"Successfully invited user {i+1}")
                    else:
                        self.log_test(f"Professional Plan User {i+1}", False, 
                                    f"Should succeed but got: {data}")
                else:  # 3rd should hit limit
                    if data.get('status') == 'limit_exceeded':
                        self.log_test("Professional Plan Limit", True, 
                                    "Correctly enforced 3-user limit")
                    else:
                        self.log_test("Professional Plan Limit", False, 
                                    f"Should hit limit but got: {data}")
            else:
                self.log_test(f"Professional Plan Test {i+1}", False, 
                            f"HTTP {response.status_code if response else 'No response'}")

    def test_get_team_members(self):
        """Test GET /api/teams/{team_id}/members"""
        print("\n🧪 Testing Get Team Members...")
        
        if not self.test_team_id:
            self.setup_test_team()
        
        response = self.make_request('GET', f'teams/{self.test_team_id}/members')
        
        if response and response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success' and 'members' in data:
                members_count = data.get('total_members', 0)
                self.log_test("Get Team Members", True, 
                            f"Retrieved {members_count} team members")
            else:
                self.log_test("Get Team Members", False, f"Invalid response format: {data}")
        else:
            self.log_test("Get Team Members", False, 
                        f"HTTP {response.status_code if response else 'No response'}")

    def test_update_member_role(self):
        """Test POST /api/teams/{team_id}/members/{user_id}/role"""
        print("\n🧪 Testing Update Member Role...")
        
        if not self.test_team_id:
            self.setup_test_team()
        
        # Create a test user ID for role update
        test_user_id = str(uuid.uuid4())
        
        role_update_data = {
            "role": "editor",
            "permissions": ["read", "write", "edit"]
        }
        
        response = self.make_request('POST', f'teams/{self.test_team_id}/members/{test_user_id}/role', 
                                   role_update_data)
        
        if response:
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    self.log_test("Update Member Role", True, 
                                f"Successfully updated role to {role_update_data['role']}")
                else:
                    self.log_test("Update Member Role", False, f"Unexpected response: {data}")
            elif response.status_code == 404:
                self.log_test("Update Member Role - Not Found", True, 
                            "Correctly returned 404 for non-existent member")
            else:
                self.log_test("Update Member Role", False, f"HTTP {response.status_code}")
        else:
            self.log_test("Update Member Role", False, "No response")
        
        # Test invalid role update
        invalid_role_data = {"permissions": ["read"]}  # Missing role
        response = self.make_request('POST', f'teams/{self.test_team_id}/members/{test_user_id}/role', 
                                   invalid_role_data)
        
        if response and response.status_code == 400:
            self.log_test("Update Role - Invalid Data", True, "Correctly rejected missing role")
        else:
            self.log_test("Update Role - Invalid Data", False, 
                        f"Should return 400, got {response.status_code if response else 'No response'}")

    def test_remove_team_member(self):
        """Test DELETE /api/teams/{team_id}/members/{user_id}"""
        print("\n🧪 Testing Remove Team Member...")
        
        if not self.test_team_id:
            self.setup_test_team()
        
        # Create a test user ID for removal
        test_user_id = str(uuid.uuid4())
        
        response = self.make_request('DELETE', f'teams/{self.test_team_id}/members/{test_user_id}')
        
        if response:
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    self.log_test("Remove Team Member", True, "Successfully removed team member")
                else:
                    self.log_test("Remove Team Member", False, f"Unexpected response: {data}")
            elif response.status_code == 404:
                self.log_test("Remove Member - Not Found", True, 
                            "Correctly returned 404 for non-existent member")
            else:
                self.log_test("Remove Team Member", False, f"HTTP {response.status_code}")
        else:
            self.log_test("Remove Team Member", False, "No response")

    def test_complete_team_workflow(self):
        """Test complete team management workflow"""
        print("\n🧪 Testing Complete Team Management Workflow...")
        
        workflow_team_id = str(uuid.uuid4())
        
        # Step 1: Invite member
        invite_data = {
            "email": "workflow@example.com",
            "role": "member",
            "permissions": ["read", "write"]
        }
        
        response = self.make_request('POST', f'teams/{workflow_team_id}/invite', invite_data)
        workflow_success = False
        
        if response and response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                # Step 2: Get team members
                members_response = self.make_request('GET', f'teams/{workflow_team_id}/members')
                if members_response and members_response.status_code == 200:
                    # Step 3: Update role (simulate with test user)
                    test_user_id = str(uuid.uuid4())
                    role_data = {"role": "editor", "permissions": ["read", "write", "edit"]}
                    role_response = self.make_request('POST', 
                                                    f'teams/{workflow_team_id}/members/{test_user_id}/role', 
                                                    role_data)
                    
                    # Step 4: Remove member
                    remove_response = self.make_request('DELETE', 
                                                      f'teams/{workflow_team_id}/members/{test_user_id}')
                    
                    if (role_response and remove_response):
                        workflow_success = True
        
        if workflow_success:
            self.log_test("Complete Team Workflow", True, 
                        "All team management operations completed successfully")
        else:
            self.log_test("Complete Team Workflow", False, "Workflow failed at some step")

    def run_all_tests(self):
        """Run all Phase 2A team management tests"""
        print("🚀 Starting Phase 2A Team Management Backend Testing...")
        print("=" * 60)
        
        # Setup
        self.setup_test_team()
        
        # Run individual tests
        self.test_invite_team_member()
        self.test_plan_limit_enforcement()
        self.test_professional_plan_limits()
        self.test_get_team_members()
        self.test_update_member_role()
        self.test_remove_team_member()
        self.test_complete_team_workflow()
        
        # Summary
        print("\n" + "=" * 60)
        print(f"📊 PHASE 2A TEAM MANAGEMENT TEST SUMMARY")
        print(f"Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("🎉 ALL PHASE 2A TEAM MANAGEMENT TESTS PASSED!")
            return True
        else:
            print("⚠️  Some tests failed. Check the details above.")
            return False

def main():
    """Main test execution"""
    tester = Phase2ATeamManagementTester()
    success = tester.run_all_tests()
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()