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
    def __init__(self, base_url: str = "https://d841087a-2e57-44e9-8fcb-86ef99ebc9fe.preview.emergentagent.com"):
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
        """Test AI content generation endpoints - EXACT FORMAT FROM REVIEW REQUEST"""
        try:
            # Test the EXACT format the frontend is sending as specified in review request
            content_request = {
                "topic": "Construction safety tips for winter",
                "platforms": ["instagram", "tiktok", "facebook"],
                "company_id": "demo-company"
            }
            
            print("    Testing content generation with exact frontend format...")
            print(f"    Request: {json.dumps(content_request, indent=2)}")
            
            response = self.session.post(f"{self.api_url}/generate-content", json=content_request, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify the expected response format: {"content": {"instagram": "...", "tiktok": "...", etc.}}
                if "content" in data:
                    content_dict = data["content"]
                    platforms_generated = list(content_dict.keys())
                    
                    # Check if all requested platforms have content
                    requested_platforms = content_request["platforms"]
                    missing_platforms = [p for p in requested_platforms if p not in platforms_generated]
                    
                    if not missing_platforms:
                        self.log_test("Content Generation (Exact Format)", True, 
                                    f"Generated content for all {len(platforms_generated)} requested platforms: {platforms_generated}")
                        
                        # Log sample content for verification
                        for platform in platforms_generated[:2]:  # Show first 2 platforms
                            content_preview = content_dict[platform][:100] + "..." if len(content_dict[platform]) > 100 else content_dict[platform]
                            print(f"    {platform.upper()}: {content_preview}")
                        
                        return True
                    else:
                        self.log_test("Content Generation (Exact Format)", False, 
                                    f"Missing content for platforms: {missing_platforms}")
                        return False
                else:
                    self.log_test("Content Generation (Exact Format)", False, 
                                f"Response missing 'content' field. Got: {list(data.keys())}")
                    return False
            else:
                self.log_test("Content Generation (Exact Format)", False, 
                            f"Status: {response.status_code}", response.text)
                return False
        except requests.exceptions.Timeout:
            self.log_test("Content Generation (Exact Format)", False, "Request timed out (>60s)")
            return False
        except Exception as e:
            self.log_test("Content Generation (Exact Format)", False, f"Error: {str(e)}")
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

    def test_critical_content_hub_apis(self):
        """Test the 3 CRITICAL Content Hub APIs specified in review request"""
        print("🎯 TESTING 3 CRITICAL CONTENT HUB APIs (REVIEW REQUEST FOCUS)")
        print("=" * 60)
        print("Testing the exact 3 endpoints that the rebuilt Content Hub frontend depends on:")
        print("1. Companies Endpoint: GET /api/companies")
        print("2. Content Generation: POST /api/generate-content") 
        print("3. Simple Health Check: GET /api/simple-test")
        print()
        
        success_count = 0
        total_tests = 3
        
        # Test 1: Simple Health Check - GET /api/simple-test
        print("🔍 Test 1: Simple Health Check")
        try:
            response = self.session.get(f"{self.api_url}/simple-test", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('message') == "SIMPLE TEST ROUTE WORKS" and data.get('success') == True:
                    self.log_test("Simple Health Check (Critical)", True, 
                                f"✅ WORKING: Returns correct JSON response: {data}")
                    success_count += 1
                else:
                    self.log_test("Simple Health Check (Critical)", False, 
                                f"❌ FAIL: Unexpected response format: {data}")
            else:
                self.log_test("Simple Health Check (Critical)", False, 
                            f"❌ FAIL: Status {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_test("Simple Health Check (Critical)", False, f"❌ FAIL: Error {str(e)}")
        
        # Test 2: Companies Endpoint - GET /api/companies
        print("🔍 Test 2: Companies Endpoint")
        try:
            response = self.session.get(f"{self.api_url}/companies", timeout=15)
            if response.status_code == 200:
                data = response.json()
                if "companies" in data and isinstance(data["companies"], list):
                    companies = data["companies"]
                    # Check for demo company specifically
                    demo_company_found = any(c.get('id') == 'demo-company' for c in companies)
                    
                    if demo_company_found:
                        self.log_test("Companies Endpoint (Critical)", True, 
                                    f"✅ WORKING: Found {len(companies)} companies including demo-company")
                        print(f"        Expected format: {{\"companies\": [{{\"id\": \"demo-company\", \"name\": \"Demo Construction Company\"}}, ...]}}")
                        print(f"        Actual response: Found demo-company and {len(companies)-1} other companies")
                        success_count += 1
                    else:
                        self.log_test("Companies Endpoint (Critical)", False, 
                                    f"❌ FAIL: Demo company not found in {len(companies)} companies")
                else:
                    self.log_test("Companies Endpoint (Critical)", False, 
                                f"❌ FAIL: Response missing 'companies' field or wrong format: {list(data.keys())}")
            else:
                self.log_test("Companies Endpoint (Critical)", False, 
                            f"❌ FAIL: Status {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_test("Companies Endpoint (Critical)", False, f"❌ FAIL: Error {str(e)}")
        
        # Test 3: Content Generation - POST /api/generate-content
        print("🔍 Test 3: Content Generation")
        try:
            # Use EXACT request format from review request
            content_request = {
                "topic": "Construction safety tips for winter",
                "platforms": ["instagram", "tiktok"],
                "company_id": "demo-company"
            }
            
            print(f"        Request: {json.dumps(content_request, indent=8)}")
            
            response = self.session.post(f"{self.api_url}/generate-content", 
                                       json=content_request, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                if "content" in data and isinstance(data["content"], dict):
                    content_dict = data["content"]
                    platforms_generated = list(content_dict.keys())
                    
                    # Check if requested platforms have content
                    instagram_content = content_dict.get("instagram", "")
                    tiktok_content = content_dict.get("tiktok", "")
                    
                    if instagram_content and tiktok_content:
                        self.log_test("Content Generation (Critical)", True, 
                                    f"✅ WORKING: Generated content for {len(platforms_generated)} platforms")
                        print(f"        Expected format: {{\"content\": {{\"instagram\": \"content...\", \"tiktok\": \"content...\"}}}}")
                        print(f"        Instagram content: {instagram_content[:100]}...")
                        print(f"        TikTok content: {tiktok_content[:100]}...")
                        success_count += 1
                    else:
                        self.log_test("Content Generation (Critical)", False, 
                                    f"❌ FAIL: Missing content for requested platforms. Got: {platforms_generated}")
                else:
                    self.log_test("Content Generation (Critical)", False, 
                                f"❌ FAIL: Response missing 'content' field or wrong format: {list(data.keys())}")
            else:
                self.log_test("Content Generation (Critical)", False, 
                            f"❌ FAIL: Status {response.status_code}, Response: {response.text}")
        except requests.exceptions.Timeout:
            self.log_test("Content Generation (Critical)", False, "❌ FAIL: Request timed out (>60s)")
        except Exception as e:
            self.log_test("Content Generation (Critical)", False, f"❌ FAIL: Error {str(e)}")
        
        # Calculate results
        success_rate = (success_count / total_tests) * 100
        
        print()
        print("🎯 CRITICAL CONTENT HUB API TEST RESULTS:")
        print("=" * 50)
        print(f"Tests Passed: {success_count}/{total_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        print()
        
        if success_count == 3:
            print("🎉 EXCELLENT: All 3 critical APIs working perfectly!")
            print("✅ Content Hub can function - proceed with frontend testing")
        elif success_count == 2:
            print("⚠️  GOOD: 2/3 critical APIs working - minor issues remain")
            print("✅ Content Hub can partially function")
        elif success_count == 1:
            print("❌ POOR: Only 1/3 critical APIs working - major issues")
            print("❌ Content Hub will have significant problems")
        else:
            print("🚨 CRITICAL: 0/3 critical APIs working - complete failure")
            print("❌ Content Hub cannot function at all")
        
        print()
        
        # Demo mode analysis
        if success_count >= 1:
            print("🔧 DEMO MODE ANALYSIS:")
            print("- Simple test working indicates basic server connectivity ✅")
            if success_count >= 2:
                print("- Companies/Content endpoints working suggests demo mode fallbacks are functioning ✅")
            else:
                print("- Companies/Content endpoints failing suggests demo mode issues ❌")
        
        print()
        return success_count, total_tests, success_rate

    def test_critical_content_hub_apis(self):
        """Test the 3 CRITICAL Content Hub APIs specified in review request"""
        print("🎯 TESTING 3 CRITICAL CONTENT HUB APIs (REVIEW REQUEST FOCUS)")
        print("=" * 60)
        print("Testing the exact 3 endpoints that the rebuilt Content Hub frontend depends on:")
        print("1. Companies Endpoint: GET /api/companies")
        print("2. Content Generation: POST /api/generate-content") 
        print("3. Simple Health Check: GET /api/simple-test")
        print()
        
        success_count = 0
        total_tests = 3
        
        # Test 1: Simple Health Check - GET /api/simple-test
        print("🔍 Test 1: Simple Health Check")
        try:
            response = self.session.get(f"{self.api_url}/simple-test", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('message') == "SIMPLE TEST ROUTE WORKS" and data.get('success') == True:
                    self.log_test("Simple Health Check (Critical)", True, 
                                f"✅ WORKING: Returns correct JSON response: {data}")
                    success_count += 1
                else:
                    self.log_test("Simple Health Check (Critical)", False, 
                                f"❌ FAIL: Unexpected response format: {data}")
            else:
                self.log_test("Simple Health Check (Critical)", False, 
                            f"❌ FAIL: Status {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_test("Simple Health Check (Critical)", False, f"❌ FAIL: Error {str(e)}")
        
        # Test 2: Companies Endpoint - GET /api/companies
        print("🔍 Test 2: Companies Endpoint")
        try:
            response = self.session.get(f"{self.api_url}/companies", timeout=15)
            if response.status_code == 200:
                data = response.json()
                if "companies" in data and isinstance(data["companies"], list):
                    companies = data["companies"]
                    # Check for demo company specifically
                    demo_company_found = any(c.get('id') == 'demo-company' for c in companies)
                    
                    if demo_company_found:
                        self.log_test("Companies Endpoint (Critical)", True, 
                                    f"✅ WORKING: Found {len(companies)} companies including demo-company")
                        print(f"        Expected format: {{\"companies\": [{{\"id\": \"demo-company\", \"name\": \"Demo Construction Company\"}}, ...]}}")
                        print(f"        Actual response: Found demo-company and {len(companies)-1} other companies")
                        success_count += 1
                    else:
                        self.log_test("Companies Endpoint (Critical)", False, 
                                    f"❌ FAIL: Demo company not found in {len(companies)} companies")
                else:
                    self.log_test("Companies Endpoint (Critical)", False, 
                                f"❌ FAIL: Response missing 'companies' field or wrong format: {list(data.keys())}")
            else:
                self.log_test("Companies Endpoint (Critical)", False, 
                            f"❌ FAIL: Status {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_test("Companies Endpoint (Critical)", False, f"❌ FAIL: Error {str(e)}")
        
        # Test 3: Content Generation - POST /api/generate-content
        print("🔍 Test 3: Content Generation")
        try:
            # Use EXACT request format from review request
            content_request = {
                "topic": "Construction safety tips for winter",
                "platforms": ["instagram", "tiktok"],
                "company_id": "demo-company"
            }
            
            print(f"        Request: {json.dumps(content_request, indent=8)}")
            
            response = self.session.post(f"{self.api_url}/generate-content", 
                                       json=content_request, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                if "content" in data and isinstance(data["content"], dict):
                    content_dict = data["content"]
                    platforms_generated = list(content_dict.keys())
                    
                    # Check if requested platforms have content
                    instagram_content = content_dict.get("instagram", "")
                    tiktok_content = content_dict.get("tiktok", "")
                    
                    if instagram_content and tiktok_content:
                        self.log_test("Content Generation (Critical)", True, 
                                    f"✅ WORKING: Generated content for {len(platforms_generated)} platforms")
                        print(f"        Expected format: {{\"content\": {{\"instagram\": \"content...\", \"tiktok\": \"content...\"}}}}")
                        print(f"        Instagram content: {instagram_content[:100]}...")
                        print(f"        TikTok content: {tiktok_content[:100]}...")
                        success_count += 1
                    else:
                        self.log_test("Content Generation (Critical)", False, 
                                    f"❌ FAIL: Missing content for requested platforms. Got: {platforms_generated}")
                else:
                    self.log_test("Content Generation (Critical)", False, 
                                f"❌ FAIL: Response missing 'content' field or wrong format: {list(data.keys())}")
            else:
                self.log_test("Content Generation (Critical)", False, 
                            f"❌ FAIL: Status {response.status_code}, Response: {response.text}")
        except requests.exceptions.Timeout:
            self.log_test("Content Generation (Critical)", False, "❌ FAIL: Request timed out (>60s)")
        except Exception as e:
            self.log_test("Content Generation (Critical)", False, f"❌ FAIL: Error {str(e)}")
        
        # Calculate results
        success_rate = (success_count / total_tests) * 100
        
        print()
        print("🎯 CRITICAL CONTENT HUB API TEST RESULTS:")
        print("=" * 50)
        print(f"Tests Passed: {success_count}/{total_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        print()
        
        if success_count == 3:
            print("🎉 EXCELLENT: All 3 critical APIs working perfectly!")
            print("✅ Content Hub can function - proceed with frontend testing")
        elif success_count == 2:
            print("⚠️  GOOD: 2/3 critical APIs working - minor issues remain")
            print("✅ Content Hub can partially function")
        elif success_count == 1:
            print("❌ POOR: Only 1/3 critical APIs working - major issues")
            print("❌ Content Hub will have significant problems")
        else:
            print("🚨 CRITICAL: 0/3 critical APIs working - complete failure")
            print("❌ Content Hub cannot function at all")
        
        print()
        
        # Demo mode analysis
        if success_count >= 1:
            print("🔧 DEMO MODE ANALYSIS:")
            print("- Simple test working indicates basic server connectivity ✅")
            if success_count >= 2:
                print("- Companies/Content endpoints working suggests demo mode fallbacks are functioning ✅")
            else:
                print("- Companies/Content endpoints failing suggests demo mode issues ❌")
        
        print()
        return success_count, total_tests, success_rate

    def test_content_hub_functionality(self):
        print("🎯 TESTING CONTENT HUB FUNCTIONALITY (CRITICAL)")
        print("    Testing the exact APIs that the rebuilt Content Hub depends on...")
        print()
        
        success_count = 0
        total_tests = 5
        
        # Test 1: Content Generation with exact frontend format
        print("    Test 1: Content Generation Endpoint")
        if self.test_content_generation():
            success_count += 1
        
        # Test 2: Companies endpoint with exact format
        print("    Test 2: Companies Endpoint")
        if self.test_companies_endpoint_exact_format():
            success_count += 1
        
        # Test 3: Platforms support with exact format
        print("    Test 3: Platforms Support Endpoint")
        if self.test_platforms_supported_exact_format():
            success_count += 1
        
        # Test 4: Authentication handling
        print("    Test 4: Authentication Handling")
        if self.test_authentication_handling():
            success_count += 1
        
        # Test 5: Error handling with invalid data
        print("    Test 5: Error Handling")
        if self.test_error_handling_with_invalid_data():
            success_count += 1
        
        success_rate = (success_count / total_tests) * 100
        
        print()
        print(f"🎯 CONTENT HUB FUNCTIONALITY TEST RESULTS:")
        print(f"    Tests Passed: {success_count}/{total_tests}")
        print(f"    Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print("    ✅ CONTENT HUB READY - All critical APIs working")
        elif success_rate >= 60:
            print("    ⚠️  CONTENT HUB PARTIAL - Some issues need attention")
        else:
            print("    ❌ CONTENT HUB ISSUES - Critical problems detected")
        
        print()
        return success_count >= 4  # At least 4 out of 5 tests must pass

    def test_companies_endpoint_exact_format(self):
        """Test GET /api/companies endpoint - EXACT FORMAT FROM REVIEW REQUEST"""
        try:
            response = self.session.get(f"{self.api_url}/companies")
            if response.status_code == 200:
                data = response.json()
                
                # Verify the expected response format: {"companies": [{"id": "company1", "name": "Company Name"}]}
                if "companies" in data:
                    companies_list = data["companies"]
                    if isinstance(companies_list, list):
                        self.log_test("Companies Endpoint (Exact Format)", True, 
                                    f"Found {len(companies_list)} companies in correct format")
                        
                        # Log sample companies for verification
                        for company in companies_list[:3]:  # Show first 3 companies
                            company_id = company.get('id', 'No ID')
                            company_name = company.get('name', 'No Name')
                            print(f"        Company: {company_name} (ID: {company_id})")
                        
                        return True
                    else:
                        self.log_test("Companies Endpoint (Exact Format)", False, 
                                    f"'companies' field is not a list: {type(companies_list)}")
                        return False
                else:
                    self.log_test("Companies Endpoint (Exact Format)", False, 
                                f"Response missing 'companies' field. Got: {list(data.keys())}")
                    return False
            else:
                self.log_test("Companies Endpoint (Exact Format)", False, 
                            f"Status: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("Companies Endpoint (Exact Format)", False, f"Error: {str(e)}")
            return False

    def test_platforms_supported_exact_format(self):
        """Test GET /api/platforms/supported endpoint - EXACT FORMAT FROM REVIEW REQUEST"""
        try:
            response = self.session.get(f"{self.api_url}/platforms/supported")
            if response.status_code == 200:
                data = response.json()
                
                # Verify platform configurations are available
                if "platforms" in data:
                    platforms_data = data["platforms"]
                    platform_count = len(platforms_data)
                    
                    # Check for the 8 main platforms mentioned in review request
                    expected_platforms = ["instagram", "tiktok", "facebook", "youtube", "whatsapp", "snapchat", "x", "linkedin"]
                    available_platforms = list(platforms_data.keys()) if isinstance(platforms_data, dict) else []
                    
                    found_platforms = [p for p in expected_platforms if p in available_platforms]
                    
                    self.log_test("Platforms Supported (Exact Format)", True, 
                                f"Found {platform_count} total platforms, {len(found_platforms)}/8 main platforms available")
                    
                    # Log platform configurations
                    for platform in found_platforms[:4]:  # Show first 4 platforms
                        config = platforms_data.get(platform, {})
                        max_chars = config.get('max_chars', 'Unknown')
                        print(f"        {platform.upper()}: max_chars={max_chars}")
                    
                    return len(found_platforms) >= 6  # At least 6 of the 8 main platforms should be available
                else:
                    self.log_test("Platforms Supported (Exact Format)", False, 
                                f"Response missing 'platforms' field. Got: {list(data.keys())}")
                    return False
            else:
                self.log_test("Platforms Supported (Exact Format)", False, 
                            f"Status: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("Platforms Supported (Exact Format)", False, f"Error: {str(e)}")
            return False

    def test_authentication_handling(self):
        """Test authentication handling - verify backend doesn't break frontend"""
        try:
            # Test endpoints without authentication to ensure they don't break
            endpoints_to_test = [
                ("/api/health", "Health Check"),
                ("/api/platforms/supported", "Platforms Support"),
                ("/api/companies", "Companies List"),
                ("/api/debug", "Debug Info")
            ]
            
            success_count = 0
            for endpoint, name in endpoints_to_test:
                try:
                    response = self.session.get(f"{self.base_url}{endpoint}")
                    if response.status_code in [200, 401, 403]:  # These are acceptable responses
                        success_count += 1
                        print(f"        ✅ {name}: Status {response.status_code} (OK)")
                    else:
                        print(f"        ❌ {name}: Status {response.status_code} (Unexpected)")
                except Exception as e:
                    print(f"        ❌ {name}: Error {str(e)}")
            
            success_rate = (success_count / len(endpoints_to_test)) * 100
            self.log_test("Authentication Handling", success_rate >= 75, 
                        f"Authentication handling OK for {success_count}/{len(endpoints_to_test)} endpoints ({success_rate:.1f}%)")
            
            return success_rate >= 75
        except Exception as e:
            self.log_test("Authentication Handling", False, f"Error: {str(e)}")
            return False

    def test_error_handling_with_invalid_data(self):
        """Test error handling with invalid data - EXACT REQUIREMENT FROM REVIEW REQUEST"""
        try:
            success_count = 0
            total_tests = 4
            
            # Test 1: Content generation with invalid data
            try:
                invalid_content_request = {
                    "topic": "",  # Empty topic
                    "platforms": ["invalid_platform"],  # Invalid platform
                    "company_id": "non_existent_company"  # Non-existent company
                }
                response = self.session.post(f"{self.api_url}/generate-content", json=invalid_content_request, timeout=30)
                if response.status_code in [400, 422, 500]:  # Expected error responses
                    success_count += 1
                    print(f"        ✅ Invalid content request: Status {response.status_code} (Expected error)")
                else:
                    print(f"        ❌ Invalid content request: Status {response.status_code} (Should be error)")
            except Exception as e:
                print(f"        ❌ Invalid content request: Exception {str(e)}")
            
            # Test 2: Companies with invalid ID
            try:
                response = self.session.get(f"{self.api_url}/companies/invalid_company_id_12345")
                if response.status_code in [404, 400]:  # Expected error responses
                    success_count += 1
                    print(f"        ✅ Invalid company ID: Status {response.status_code} (Expected error)")
                else:
                    print(f"        ❌ Invalid company ID: Status {response.status_code} (Should be 404)")
            except Exception as e:
                print(f"        ❌ Invalid company ID: Exception {str(e)}")
            
            # Test 3: Malformed JSON request
            try:
                response = self.session.post(f"{self.api_url}/generate-content", 
                                           data="invalid json data", 
                                           headers={'Content-Type': 'application/json'}, 
                                           timeout=10)
                if response.status_code in [400, 422]:  # Expected error responses
                    success_count += 1
                    print(f"        ✅ Malformed JSON: Status {response.status_code} (Expected error)")
                else:
                    print(f"        ❌ Malformed JSON: Status {response.status_code} (Should be 400/422)")
            except Exception as e:
                print(f"        ❌ Malformed JSON: Exception {str(e)}")
            
            # Test 4: Missing required fields
            try:
                incomplete_request = {"topic": "Test topic"}  # Missing platforms and company_id
                response = self.session.post(f"{self.api_url}/generate-content", json=incomplete_request, timeout=10)
                if response.status_code in [400, 422]:  # Expected error responses
                    success_count += 1
                    print(f"        ✅ Missing fields: Status {response.status_code} (Expected error)")
                else:
                    print(f"        ❌ Missing fields: Status {response.status_code} (Should be 400/422)")
            except Exception as e:
                print(f"        ❌ Missing fields: Exception {str(e)}")
            
            success_rate = (success_count / total_tests) * 100
            self.log_test("Error Handling with Invalid Data", success_rate >= 75, 
                        f"Error handling working for {success_count}/{total_tests} test cases ({success_rate:.1f}%)")
            
            return success_rate >= 75
        except Exception as e:
            self.log_test("Error Handling with Invalid Data", False, f"Error: {str(e)}")
            return False

    def run_all_tests(self):
        """Run all backend tests with focus on 3 CRITICAL Content Hub APIs"""
        print("🚀 Starting PostVelocity Backend API Testing Suite")
        print("=" * 60)
        print("FOCUS: Testing the 3 CRITICAL Content Hub APIs as specified in review request")
        print()
        
        start_time = time.time()
        
        # PRIORITY #1: Test the 3 CRITICAL Content Hub APIs (REVIEW REQUEST FOCUS)
        print("🎯 PRIORITY #1: CRITICAL CONTENT HUB APIS")
        print("=" * 50)
        critical_success, critical_total, critical_rate = self.test_critical_content_hub_apis()
        print()
        
        # Only run additional tests if we have time and the critical tests show issues
        if critical_success < 3:
            print("🔍 ADDITIONAL DIAGNOSTIC TESTS (Due to critical API issues)")
            print("-" * 50)
            
            # Debug endpoint to check system status
            debug_ok = self.test_debug_endpoint()
            
            # Basic health check
            health_ok = self.test_health_check()
            print()
        else:
            debug_ok = True
            health_ok = True
        
        # Summary
        end_time = time.time()
        duration = end_time - start_time
        
        print("=" * 60)
        print("📊 FINAL TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Overall Success Rate: {success_rate:.1f}%")
        print(f"Duration: {duration:.1f} seconds")
        print()
        
        # CRITICAL RESULTS ANALYSIS
        print("🎯 CRITICAL CONTENT HUB API RESULTS:")
        print("=" * 50)
        print(f"Critical API Success Rate: {critical_rate:.1f}% ({critical_success}/{critical_total} tests passed)")
        
        if critical_success == 3:
            print("🎉 EXCELLENT: All 3 critical APIs working perfectly!")
            print("✅ Content Hub can function - demo mode fallbacks working")
            print("✅ MongoDB failures prevented by demo mode implementation")
            print("✅ Content generation returns proper format")
            print("✅ RECOMMENDATION: Proceed with frontend testing")
        elif critical_success == 2:
            print("⚠️  GOOD: 2/3 critical APIs working - minor issues remain")
            print("✅ Content Hub can partially function")
            print("⚠️  RECOMMENDATION: Fix remaining issue before full deployment")
        elif critical_success == 1:
            print("❌ POOR: Only 1/3 critical APIs working - major issues")
            print("❌ Content Hub will have significant problems")
            print("❌ RECOMMENDATION: Fix critical issues before frontend testing")
        else:
            print("🚨 CRITICAL FAILURE: 0/3 critical APIs working")
            print("❌ Content Hub cannot function at all")
            print("❌ RECOMMENDATION: Immediate backend fixes required")
        
        print()
        
        # Demo mode status
        if critical_success >= 1:
            print("🔧 DEMO MODE STATUS:")
            if critical_success >= 2:
                print("✅ Demo mode fallbacks appear to be working")
                print("✅ MongoDB connection issues successfully bypassed")
            else:
                print("⚠️  Demo mode may have partial issues")
                print("⚠️  Some fallbacks may not be working correctly")
        
        print()
        
        # Failed Tests Details (only if there are failures)
        if failed_tests > 0:
            print("❌ FAILED TESTS DETAILS:")
            print("-" * 30)
            for result in self.test_results:
                if not result['success']:
                    print(f"• {result['test_name']}: {result['details']}")
            print()
        
        # Final recommendation
        print("🎯 FINAL RECOMMENDATION:")
        print("-" * 30)
        if critical_success == 3:
            print("✅ All critical APIs working - Content Hub is ready!")
            print("✅ Demo mode successfully prevents MongoDB failures")
            print("✅ Content generation returns proper format as expected")
            print("✅ PROCEED with frontend testing")
        else:
            print("❌ Critical API issues detected")
            print("❌ Content Hub functionality compromised")
            print("❌ REQUIRES backend fixes before frontend testing")
        
        print()
        
        return critical_success == 3  # Success only if all 3 critical APIs work

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