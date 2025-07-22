#!/usr/bin/env python3
"""
PostVelocity Backend API Testing Suite
Tests all major backend endpoints to ensure functionality after frontend fixes
"""

import requests
import json
import time
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional

class PostVelocityBackendTester:
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        self.test_results = []
        self.demo_company_id = "demo-company"
        
    def log_test(self, test_name: str, success: bool, details: str = "", response_data: Any = None):
        """Log test results"""
        result = {
            'test_name': test_name,
            'success': success,
            'details': details,
            'timestamp': datetime.now().isoformat(),
            'response_data': response_data
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"    {details}")
        if not success and response_data:
            print(f"    Response: {response_data}")
        print()

    def test_health_check(self):
        """Test basic API health check"""
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                self.log_test("Health Check", True, f"Status: {response.status_code}")
                return True
            else:
                self.log_test("Health Check", False, f"Status: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("Health Check", False, f"Connection error: {str(e)}")
            return False

    def test_debug_endpoint(self):
        """Test debug endpoint to verify system status"""
        try:
            response = self.session.get(f"{self.api_url}/debug")
            if response.status_code == 200:
                data = response.json()
                details = f"Claude API: {'✓' if data.get('claude_api_available') else '✗'}, "
                details += f"SEO Keywords: {len(data.get('seo_keywords', {}))}, "
                details += f"Trending Hashtags: {len(data.get('trending_hashtags', {}))}"
                self.log_test("Debug Endpoint", True, details, data)
                return True
            else:
                self.log_test("Debug Endpoint", False, f"Status: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("Debug Endpoint", False, f"Error: {str(e)}")
            return False

    def test_platforms_endpoint(self):
        """Test platforms configuration endpoint"""
        try:
            response = self.session.get(f"{self.api_url}/platforms")
            if response.status_code == 200:
                data = response.json()
                platform_count = len(data.get('platforms', {}))
                self.log_test("Platforms Endpoint", True, f"Platforms available: {platform_count}", data)
                return True
            else:
                self.log_test("Platforms Endpoint", False, f"Status: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("Platforms Endpoint", False, f"Error: {str(e)}")
            return False

    def test_company_management(self):
        """Test company CRUD operations"""
        success_count = 0
        total_tests = 4
        
        # Test 1: Create Company
        try:
            company_data = {
                "name": "Test Construction Company",
                "industry": "construction",
                "website": "https://testconstruction.com",
                "description": "A test construction company for API testing",
                "target_audience": "Construction professionals and contractors",
                "brand_voice": "Professional and trustworthy"
            }
            response = self.session.post(f"{self.api_url}/companies", json=company_data)
            if response.status_code == 200:
                created_company = response.json()
                test_company_id = created_company.get('id')
                self.log_test("Create Company", True, f"Company created with ID: {test_company_id}")
                success_count += 1
            else:
                self.log_test("Create Company", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Create Company", False, f"Error: {str(e)}")

        # Test 2: Get Companies
        try:
            response = self.session.get(f"{self.api_url}/companies")
            if response.status_code == 200:
                companies = response.json()
                company_count = len(companies)
                self.log_test("Get Companies", True, f"Found {company_count} companies")
                success_count += 1
            else:
                self.log_test("Get Companies", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Get Companies", False, f"Error: {str(e)}")

        # Test 3: Get Company by ID (using demo company)
        try:
            response = self.session.get(f"{self.api_url}/companies/{self.demo_company_id}")
            if response.status_code == 200:
                company = response.json()
                self.log_test("Get Company by ID", True, f"Retrieved company: {company.get('name', 'Unknown')}")
                success_count += 1
            else:
                self.log_test("Get Company by ID", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Get Company by ID", False, f"Error: {str(e)}")

        # Test 4: Update Company
        try:
            update_data = {
                "description": "Updated description for testing purposes",
                "target_audience": "Updated target audience"
            }
            response = self.session.put(f"{self.api_url}/companies/{self.demo_company_id}", json=update_data)
            if response.status_code == 200:
                self.log_test("Update Company", True, "Company updated successfully")
                success_count += 1
            else:
                self.log_test("Update Company", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Update Company", False, f"Error: {str(e)}")

        return success_count == total_tests

    def test_content_generation(self):
        """Test AI content generation endpoints"""
        try:
            content_request = {
                "company_id": self.demo_company_id,
                "topic": "Construction Safety Best Practices",
                "platforms": ["instagram", "linkedin", "facebook"],
                "audience_level": "professional",
                "additional_context": "Focus on workplace safety and OSHA compliance",
                "seo_focus": True,
                "target_keywords": ["construction safety", "workplace safety", "OSHA compliance"]
            }
            
            print("    Generating content (this may take 20-30 seconds)...")
            response = self.session.post(f"{self.api_url}/content/generate", json=content_request, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                content_count = len(data.get('generated_content', []))
                self.log_test("Content Generation", True, f"Generated content for {content_count} platforms")
                return True
            else:
                self.log_test("Content Generation", False, f"Status: {response.status_code}", response.text)
                return False
        except requests.exceptions.Timeout:
            self.log_test("Content Generation", False, "Request timed out (>60s)")
            return False
        except Exception as e:
            self.log_test("Content Generation", False, f"Error: {str(e)}")
            return False

    def test_ai_features(self):
        """Test advanced AI features"""
        success_count = 0
        total_tests = 4
        
        # Test 1: SEO Analysis
        try:
            seo_request = {
                "content": "Construction safety is paramount in any building project. Proper safety protocols, OSHA compliance, and regular training ensure worker protection and project success.",
                "target_keywords": ["construction safety", "OSHA compliance", "worker protection"]
            }
            response = self.session.post(f"{self.api_url}/seo/analyze", json=seo_request)
            if response.status_code == 200:
                data = response.json()
                seo_score = data.get('seo_score', 0)
                recommendations = len(data.get('recommendations', []))
                self.log_test("SEO Analysis", True, f"SEO Score: {seo_score}, Recommendations: {recommendations}")
                success_count += 1
            else:
                self.log_test("SEO Analysis", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("SEO Analysis", False, f"Error: {str(e)}")

        # Test 2: Hashtag Analysis
        try:
            hashtag_request = {
                "hashtags": ["#ConstructionSafety", "#BuildSafe", "#OSHACompliance"],
                "industry": "construction"
            }
            response = self.session.post(f"{self.api_url}/hashtags/analyze", json=hashtag_request)
            if response.status_code == 200:
                data = response.json()
                analyses = data.get('analyses', [])
                self.log_test("Hashtag Analysis", True, f"Analyzed {len(analyses)} hashtags")
                success_count += 1
            else:
                self.log_test("Hashtag Analysis", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Hashtag Analysis", False, f"Error: {str(e)}")

        # Test 3: Trending Hashtags
        try:
            response = self.session.get(f"{self.api_url}/hashtags/trending/construction")
            if response.status_code == 200:
                data = response.json()
                trending_count = len(data.get('trending', []))
                self.log_test("Trending Hashtags", True, f"Found {trending_count} trending hashtags for construction")
                success_count += 1
            else:
                self.log_test("Trending Hashtags", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Trending Hashtags", False, f"Error: {str(e)}")

        # Test 4: ROI Analytics
        try:
            response = self.session.get(f"{self.api_url}/analytics/roi/{self.demo_company_id}")
            if response.status_code == 200:
                data = response.json()
                roi_percentage = data.get('roi_percentage', 0)
                platforms = len(data.get('platform_breakdown', {}))
                self.log_test("ROI Analytics", True, f"ROI: {roi_percentage}%, Platforms: {platforms}")
                success_count += 1
            else:
                self.log_test("ROI Analytics", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("ROI Analytics", False, f"Error: {str(e)}")

        return success_count == total_tests

    def test_media_management(self):
        """Test media management endpoints"""
        success_count = 0
        total_tests = 5
        
        # Test 1: Media Categories
        try:
            response = self.session.get(f"{self.api_url}/media/categories")
            if response.status_code == 200:
                data = response.json()
                categories = data.get('categories', [])
                self.log_test("Media Categories", True, f"Available categories: {len(categories)}")
                success_count += 1
            else:
                self.log_test("Media Categories", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Media Categories", False, f"Error: {str(e)}")

        # Test 2: Get Company Media
        try:
            response = self.session.get(f"{self.api_url}/companies/{self.demo_company_id}/media")
            if response.status_code == 200:
                data = response.json()
                media_count = len(data.get('media_files', []))
                self.log_test("Get Company Media", True, f"Found {media_count} media files")
                success_count += 1
            else:
                self.log_test("Get Company Media", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Get Company Media", False, f"Error: {str(e)}")

        # Test 3: Monthly Media Requests
        try:
            response = self.session.get(f"{self.api_url}/media/monthly-requests")
            if response.status_code == 200:
                data = response.json()
                companies_needing_media = len(data.get('companies_needing_media', []))
                self.log_test("Monthly Media Requests", True, f"Companies needing media: {companies_needing_media}")
                success_count += 1
            else:
                self.log_test("Monthly Media Requests", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Monthly Media Requests", False, f"Error: {str(e)}")

        # Test 4: Media Request Prompt
        try:
            response = self.session.get(f"{self.api_url}/media/request-prompt/{self.demo_company_id}")
            if response.status_code == 200:
                data = response.json()
                self.log_test("Media Request Prompt", True, "Media request prompt generated")
                success_count += 1
            else:
                self.log_test("Media Request Prompt", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Media Request Prompt", False, f"Error: {str(e)}")

        # Test 5: Mark Media Request Sent
        try:
            response = self.session.post(f"{self.api_url}/media/mark-sent/{self.demo_company_id}")
            if response.status_code == 200:
                self.log_test("Mark Media Request Sent", True, "Media request marked as sent")
                success_count += 1
            else:
                self.log_test("Mark Media Request Sent", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Mark Media Request Sent", False, f"Error: {str(e)}")

        return success_count == total_tests

    def test_beta_feedback_system(self):
        """Test beta feedback system endpoints"""
        success_count = 0
        total_tests = 6
        
        # Test 1: Beta Login/Registration
        try:
            beta_user_data = {
                "name": "Test Beta User",
                "email": "testbeta@example.com"
            }
            response = self.session.post(f"{self.api_url}/beta/login", json=beta_user_data)
            if response.status_code == 200:
                data = response.json()
                beta_user_id = data.get('beta_user_id')
                self.log_test("Beta Login", True, f"Beta user registered: {beta_user_id}")
                success_count += 1
            else:
                self.log_test("Beta Login", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Beta Login", False, f"Error: {str(e)}")

        # Test 2: Submit Feedback
        try:
            feedback_data = {
                "beta_user_id": "test-beta-user",
                "beta_user_name": "Test Beta User",
                "beta_user_email": "testbeta@example.com",
                "feedback_type": "suggestion",
                "title": "Test Feedback Submission",
                "description": "This is a test feedback submission for API testing",
                "priority": "medium",
                "category": "ui"
            }
            response = self.session.post(f"{self.api_url}/beta/feedback", json=feedback_data)
            if response.status_code == 200:
                data = response.json()
                feedback_id = data.get('feedback_id')
                self.log_test("Submit Feedback", True, f"Feedback submitted: {feedback_id}")
                success_count += 1
            else:
                self.log_test("Submit Feedback", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Submit Feedback", False, f"Error: {str(e)}")

        # Test 3: Get All Feedback
        try:
            response = self.session.get(f"{self.api_url}/beta/feedback")
            if response.status_code == 200:
                data = response.json()
                feedback_count = len(data.get('feedback', []))
                self.log_test("Get All Feedback", True, f"Retrieved {feedback_count} feedback items")
                success_count += 1
            else:
                self.log_test("Get All Feedback", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Get All Feedback", False, f"Error: {str(e)}")

        # Test 4: Update Feedback Status (Admin function)
        try:
            feedback_id = "test-feedback-id"
            update_data = {
                "status": "in_progress",
                "admin_response": "We are working on this feedback"
            }
            response = self.session.put(f"{self.api_url}/beta/feedback/{feedback_id}", json=update_data)
            if response.status_code == 200:
                self.log_test("Update Feedback Status", True, "Feedback status updated")
                success_count += 1
            else:
                self.log_test("Update Feedback Status", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Update Feedback Status", False, f"Error: {str(e)}")

        # Test 5: Vote on Feedback
        try:
            feedback_id = "test-feedback-id"
            vote_data = {
                "beta_user_id": "test-beta-user",
                "vote_type": "upvote"
            }
            response = self.session.post(f"{self.api_url}/beta/feedback/{feedback_id}/vote", json=vote_data)
            if response.status_code == 200:
                data = response.json()
                votes = data.get('votes', 0)
                self.log_test("Vote on Feedback", True, f"Vote recorded, total votes: {votes}")
                success_count += 1
            else:
                self.log_test("Vote on Feedback", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Vote on Feedback", False, f"Error: {str(e)}")

        # Test 6: Get User Statistics
        try:
            beta_user_id = "test-beta-user"
            response = self.session.get(f"{self.api_url}/beta/user/{beta_user_id}/stats")
            if response.status_code == 200:
                data = response.json()
                feedback_count = data.get('feedback_count', 0)
                self.log_test("Get User Statistics", True, f"User has {feedback_count} feedback submissions")
                success_count += 1
            else:
                self.log_test("Get User Statistics", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Get User Statistics", False, f"Error: {str(e)}")

        return success_count == total_tests

    def test_routing_fix_verification(self):
        """Test the critical routing fix - all routes should have /api/ prefix"""
        success_count = 0
        total_tests = 9
        
        print("🔧 TESTING ROUTING FIX VERIFICATION")
        print("    Testing newly fixed routes with /api/ prefix...")
        
        # Test 1: Simple Test Route
        try:
            response = self.session.get(f"{self.api_url}/simple-test")
            if response.status_code == 200:
                data = response.json()
                if data.get('message') == "SIMPLE TEST ROUTE WORKS" and data.get('success') == True:
                    self.log_test("Simple Test Route", True, "Route works with /api/ prefix")
                    success_count += 1
                else:
                    self.log_test("Simple Test Route", False, f"Unexpected response: {data}")
            else:
                self.log_test("Simple Test Route", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Simple Test Route", False, f"Error: {str(e)}")

        # Test 2: Debug Test HTML Route
        try:
            response = self.session.get(f"{self.api_url}/debug-test-html")
            if response.status_code == 200:
                if "DEBUG HTML ROUTE WORKS" in response.text:
                    self.log_test("Debug Test HTML Route", True, "HTML route works with /api/ prefix")
                    success_count += 1
                else:
                    self.log_test("Debug Test HTML Route", False, f"Unexpected HTML content")
            else:
                self.log_test("Debug Test HTML Route", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Debug Test HTML Route", False, f"Error: {str(e)}")

        # Test 3: User Login Route
        try:
            response = self.session.get(f"{self.api_url}/login")
            if response.status_code == 200:
                if "login" in response.text.lower():
                    self.log_test("User Login Route", True, "Login page accessible with /api/ prefix")
                    success_count += 1
                else:
                    self.log_test("User Login Route", False, "Login page content not found")
            else:
                self.log_test("User Login Route", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("User Login Route", False, f"Error: {str(e)}")

        # Test 4: Admin Login Route
        try:
            response = self.session.get(f"{self.api_url}/admin-login")
            if response.status_code == 200:
                if "admin" in response.text.lower() or "login" in response.text.lower():
                    self.log_test("Admin Login Route", True, "Admin login page accessible with /api/ prefix")
                    success_count += 1
                else:
                    self.log_test("Admin Login Route", False, "Admin login page content not found")
            else:
                self.log_test("Admin Login Route", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Admin Login Route", False, f"Error: {str(e)}")

        # Test 5: Backend Login Route
        try:
            response = self.session.get(f"{self.api_url}/backend-login")
            if response.status_code == 200:
                if "login" in response.text.lower():
                    self.log_test("Backend Login Route", True, "Backend login page accessible with /api/ prefix")
                    success_count += 1
                else:
                    self.log_test("Backend Login Route", False, "Backend login page content not found")
            else:
                self.log_test("Backend Login Route", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Backend Login Route", False, f"Error: {str(e)}")

        # Test 6: Backend Admin Login Route
        try:
            response = self.session.get(f"{self.api_url}/backend-admin-login")
            if response.status_code == 200:
                if "admin" in response.text.lower() or "login" in response.text.lower():
                    self.log_test("Backend Admin Login Route", True, "Backend admin login page accessible with /api/ prefix")
                    success_count += 1
                else:
                    self.log_test("Backend Admin Login Route", False, "Backend admin login page content not found")
            else:
                self.log_test("Backend Admin Login Route", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Backend Admin Login Route", False, f"Error: {str(e)}")

        # Test 7: Health Check (existing working route)
        try:
            response = self.session.get(f"{self.api_url}/health")
            if response.status_code == 200:
                self.log_test("Health Check Route", True, "Existing health route still works")
                success_count += 1
            else:
                self.log_test("Health Check Route", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Health Check Route", False, f"Error: {str(e)}")

        # Test 8: Platforms Supported (existing working route)
        try:
            response = self.session.get(f"{self.api_url}/platforms/supported")
            if response.status_code == 200:
                data = response.json()
                platforms = data.get('platforms', [])
                self.log_test("Platforms Supported Route", True, f"Existing platforms route works ({len(platforms)} platforms)")
                success_count += 1
            else:
                self.log_test("Platforms Supported Route", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Platforms Supported Route", False, f"Error: {str(e)}")

        # Test 9: Debug Route (existing working route)
        try:
            response = self.session.get(f"{self.api_url}/debug")
            if response.status_code == 200:
                data = response.json()
                claude_api = data.get('claude_api_available', False)
                self.log_test("Debug Route", True, f"Existing debug route works (Claude API: {claude_api})")
                success_count += 1
            else:
                self.log_test("Debug Route", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Debug Route", False, f"Error: {str(e)}")

        return success_count == total_tests

    def test_oauth_integration(self):
        """Test OAuth integration endpoints"""
        success_count = 0
        total_tests = 5
        
        # Test 1: Get Supported Platforms
        try:
            response = self.session.get(f"{self.api_url}/platforms/supported")
            if response.status_code == 200:
                data = response.json()
                platforms = data.get('platforms', [])
                self.log_test("OAuth Supported Platforms", True, f"Supported platforms: {len(platforms)}")
                success_count += 1
            else:
                self.log_test("OAuth Supported Platforms", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("OAuth Supported Platforms", False, f"Error: {str(e)}")

        # Test 2: Generate OAuth Authorization URL
        try:
            oauth_request = {
                "platform": "instagram",
                "user_id": "test-user"
            }
            response = self.session.post(f"{self.api_url}/oauth/authorize", json=oauth_request)
            if response.status_code == 200:
                data = response.json()
                auth_url = data.get('authorization_url', '')
                self.log_test("OAuth Authorization URL", True, f"Generated auth URL for Instagram")
                success_count += 1
            else:
                self.log_test("OAuth Authorization URL", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("OAuth Authorization URL", False, f"Error: {str(e)}")

        # Test 3: Token Exchange (Demo Mode)
        try:
            token_request = {
                "platform": "instagram",
                "code": "demo_auth_code",
                "user_id": "test-user"
            }
            response = self.session.post(f"{self.api_url}/oauth/token", json=token_request)
            if response.status_code == 200:
                data = response.json()
                self.log_test("OAuth Token Exchange", True, "Token exchange successful (demo mode)")
                success_count += 1
            else:
                self.log_test("OAuth Token Exchange", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("OAuth Token Exchange", False, f"Error: {str(e)}")

        # Test 4: Get User Connections
        try:
            user_id = "test-user"
            response = self.session.get(f"{self.api_url}/oauth/connections/{user_id}")
            if response.status_code == 200:
                data = response.json()
                connections = data.get('connections', [])
                self.log_test("Get User Connections", True, f"User has {len(connections)} connections")
                success_count += 1
            else:
                self.log_test("Get User Connections", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Get User Connections", False, f"Error: {str(e)}")

        # Test 5: Disconnect Platform
        try:
            platform = "instagram"
            disconnect_request = {
                "user_id": "test-user"
            }
            response = self.session.delete(f"{self.api_url}/oauth/disconnect/{platform}", json=disconnect_request)
            if response.status_code == 200:
                self.log_test("Disconnect Platform", True, f"Successfully disconnected {platform}")
                success_count += 1
            else:
                self.log_test("Disconnect Platform", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Disconnect Platform", False, f"Error: {str(e)}")

        return success_count == total_tests

    def test_seo_addon_system(self):
        """Test SEO addon purchase and management"""
        success_count = 0
        total_tests = 2
        
        # Test 1: SEO Addon Purchase
        try:
            purchase_request = {
                "company_id": self.demo_company_id,
                "website_url": "https://example.com",
                "notification_email": "admin@company.com",
                "plan_type": "standard"
            }
            response = self.session.post(f"{self.api_url}/seo-addon/purchase", json=purchase_request)
            if response.status_code == 200:
                data = response.json()
                status = data.get('status')
                self.log_test("SEO Addon Purchase", True, f"Purchase status: {status}")
                success_count += 1
            else:
                self.log_test("SEO Addon Purchase", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("SEO Addon Purchase", False, f"Error: {str(e)}")

        # Test 2: Get SEO Addon Status
        try:
            response = self.session.get(f"{self.api_url}/seo-addon/{self.demo_company_id}/status")
            if response.status_code == 200:
                data = response.json()
                monitoring_status = data.get('monitoring_status', 'inactive')
                self.log_test("SEO Addon Status", True, f"Monitoring status: {monitoring_status}")
                success_count += 1
            else:
                self.log_test("SEO Addon Status", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("SEO Addon Status", False, f"Error: {str(e)}")

        return success_count == total_tests

    def run_all_tests(self):
        """Run all backend tests"""
        print("🚀 Starting PostVelocity Backend API Testing Suite")
        print("=" * 60)
        print()
        
        start_time = time.time()
        
        # CRITICAL: Routing Fix Verification Tests (Priority #1)
        print("🔧 ROUTING FIX VERIFICATION TESTS (CRITICAL)")
        print("-" * 50)
        routing_fix_ok = self.test_routing_fix_verification()
        print()
        
        # Core System Tests
        print("📋 CORE SYSTEM TESTS")
        print("-" * 30)
        health_ok = self.test_health_check()
        debug_ok = self.test_debug_endpoint()
        platforms_ok = self.test_platforms_endpoint()
        print()
        
        # Company Management Tests
        print("🏢 COMPANY MANAGEMENT TESTS")
        print("-" * 30)
        company_ok = self.test_company_management()
        print()
        
        # Content Generation Tests
        print("🤖 AI CONTENT GENERATION TESTS")
        print("-" * 30)
        content_ok = self.test_content_generation()
        print()
        
        # AI Features Tests
        print("🧠 ADVANCED AI FEATURES TESTS")
        print("-" * 30)
        ai_features_ok = self.test_ai_features()
        print()
        
        # Media Management Tests
        print("📸 MEDIA MANAGEMENT TESTS")
        print("-" * 30)
        media_ok = self.test_media_management()
        print()
        
        # Beta Feedback System Tests
        print("💬 BETA FEEDBACK SYSTEM TESTS")
        print("-" * 30)
        beta_ok = self.test_beta_feedback_system()
        print()
        
        # OAuth Integration Tests
        print("🔗 OAUTH INTEGRATION TESTS")
        print("-" * 30)
        oauth_ok = self.test_oauth_integration()
        print()
        
        # SEO Addon Tests
        print("🔍 SEO ADDON SYSTEM TESTS")
        print("-" * 30)
        seo_addon_ok = self.test_seo_addon_system()
        print()
        
        # Summary
        end_time = time.time()
        duration = end_time - start_time
        
        print("=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {success_rate:.1f}%")
        print(f"Duration: {duration:.1f} seconds")
        print()
        
        # CRITICAL: Routing Fix Status
        print("🔧 ROUTING FIX VERIFICATION STATUS:")
        print("-" * 40)
        if routing_fix_ok:
            print("✅ ROUTING FIX SUCCESSFUL - All routes working with /api/ prefix")
        else:
            print("❌ ROUTING FIX ISSUES DETECTED - Some routes not working properly")
        print()
        
        # System Status
        core_systems = [health_ok, debug_ok, platforms_ok]
        critical_features = [company_ok, content_ok, ai_features_ok]
        
        if routing_fix_ok and all(core_systems) and all(critical_features):
            print("🎉 OVERALL STATUS: EXCELLENT - Routing fix successful, all critical systems operational")
        elif routing_fix_ok and all(core_systems) and any(critical_features):
            print("✅ OVERALL STATUS: GOOD - Routing fix successful, core systems working, some features need attention")
        elif routing_fix_ok and any(core_systems):
            print("⚠️  OVERALL STATUS: PARTIAL - Routing fix successful but some core systems need attention")
        elif not routing_fix_ok:
            print("❌ OVERALL STATUS: CRITICAL - Routing fix verification failed")
        else:
            print("❌ OVERALL STATUS: CRITICAL - Core systems not responding")
        
        print()
        
        # Failed Tests Details
        if failed_tests > 0:
            print("❌ FAILED TESTS DETAILS:")
            print("-" * 30)
            for result in self.test_results:
                if not result['success']:
                    print(f"• {result['test_name']}: {result['details']}")
            print()
        
        return success_rate >= 70 and routing_fix_ok  # Routing fix must pass

def main():
    """Main function to run the tests"""
    # Check if custom URL provided
    base_url = "http://localhost:8001"
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    
    print(f"Testing PostVelocity Backend at: {base_url}")
    print()
    
    tester = PostVelocityBackendTester(base_url)
    success = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()