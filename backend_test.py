#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for Social Media Management Platform
Tests all CRUD operations, content generation, and integration features
"""

import requests
import json
import sys
from datetime import datetime, timedelta
import uuid

class SocialMediaAPITester:
    def __init__(self, base_url="https://e7906d23-64b5-46c4-8078-8d731321a4b4.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.test_company_id = None
        self.test_post_id = None

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

    def test_health_check(self):
        """Test basic health check endpoint"""
        response = self.make_request('GET', 'health')
        if response and response.status_code == 200:
            data = response.json()
            success = data.get('status') == 'healthy'
            self.log_test("Health Check", success, f"Status: {data.get('status')}")
            return success
        else:
            self.log_test("Health Check", False, f"Failed to connect or bad response")
            return False

    def test_debug_endpoint(self):
        """Test debug endpoint for API key validation"""
        response = self.make_request('GET', 'debug')
        if response and response.status_code == 200:
            data = response.json()
            claude_key_exists = data.get('claude_api_key_exists', False)
            self.log_test("Debug Endpoint", True, f"Claude API Key exists: {claude_key_exists}")
            return True
        else:
            self.log_test("Debug Endpoint", False, "Failed to get debug info")
            return False

    def test_platforms_endpoint(self):
        """Test platforms configuration endpoint"""
        response = self.make_request('GET', 'platforms')
        if response and response.status_code == 200:
            data = response.json()
            platforms = data.get('platforms', [])
            configs = data.get('configs', {})
            expected_platforms = ['instagram', 'tiktok', 'facebook', 'youtube', 'whatsapp', 'snapchat', 'x']
            
            success = len(platforms) >= 7 and all(p in platforms for p in expected_platforms)
            self.log_test("Platforms Endpoint", success, f"Found {len(platforms)} platforms: {platforms}")
            return success
        else:
            self.log_test("Platforms Endpoint", False, "Failed to get platforms")
            return False

    def test_content_examples(self):
        """Test content examples endpoint"""
        response = self.make_request('GET', 'content-examples')
        if response and response.status_code == 200:
            data = response.json()
            topics = data.get('topics', [])
            audience_levels = data.get('audience_levels', [])
            
            success = len(topics) > 0 and len(audience_levels) > 0
            self.log_test("Content Examples", success, f"Found {len(topics)} topics, {len(audience_levels)} audience levels")
            return success
        else:
            self.log_test("Content Examples", False, "Failed to get content examples")
            return False

    def test_create_company(self):
        """Test company creation"""
        test_company = {
            "name": f"Test Company {datetime.now().strftime('%H%M%S')}",
            "industry": "Construction",
            "website": "https://testcompany.com",
            "description": "A test company for API testing",
            "target_audience": "Construction workers, safety managers",
            "brand_voice": "Professional but accessible, safety-focused"
        }
        
        response = self.make_request('POST', 'companies', test_company)
        if response and response.status_code == 200:
            data = response.json()
            self.test_company_id = data.get('id')
            success = self.test_company_id is not None and data.get('name') == test_company['name']
            self.log_test("Create Company", success, f"Created company with ID: {self.test_company_id}")
            return success
        else:
            self.log_test("Create Company", False, f"Status: {response.status_code if response else 'No response'}")
            return False

    def test_get_companies(self):
        """Test getting all companies"""
        response = self.make_request('GET', 'companies')
        if response and response.status_code == 200:
            data = response.json()
            success = isinstance(data, list) and len(data) > 0
            self.log_test("Get Companies", success, f"Found {len(data)} companies")
            return success
        else:
            self.log_test("Get Companies", False, f"Status: {response.status_code if response else 'No response'}")
            return False

    def test_get_company_by_id(self):
        """Test getting specific company by ID"""
        if not self.test_company_id:
            self.log_test("Get Company by ID", False, "No test company ID available")
            return False
            
        response = self.make_request('GET', f'companies/{self.test_company_id}')
        if response and response.status_code == 200:
            data = response.json()
            success = data.get('id') == self.test_company_id
            self.log_test("Get Company by ID", success, f"Retrieved company: {data.get('name')}")
            return success
        else:
            self.log_test("Get Company by ID", False, f"Status: {response.status_code if response else 'No response'}")
            return False

    def test_update_company(self):
        """Test updating company information"""
        if not self.test_company_id:
            self.log_test("Update Company", False, "No test company ID available")
            return False
            
        update_data = {
            "name": f"Updated Test Company {datetime.now().strftime('%H%M%S')}",
            "description": "Updated description for testing"
        }
        
        response = self.make_request('PUT', f'companies/{self.test_company_id}', update_data)
        if response and response.status_code == 200:
            data = response.json()
            success = data.get('name') == update_data['name']
            self.log_test("Update Company", success, f"Updated company name to: {data.get('name')}")
            return success
        else:
            self.log_test("Update Company", False, f"Status: {response.status_code if response else 'No response'}")
            return False

    def test_generate_content(self):
        """Test enhanced content generation with new features"""
        if not self.test_company_id:
            self.log_test("Generate Content", False, "No test company ID available")
            return False
            
        content_request = {
            "company_id": self.test_company_id,
            "topic": "OSHA Fall Protection Standards",
            "platforms": ["instagram", "tiktok", "facebook", "youtube"],
            "audience_level": "intermediate",
            "additional_context": "Focus on recent updates to safety regulations",
            "generate_blog": True,
            "generate_newsletter": True,
            "generate_video_script": True
        }
        
        response = self.make_request('POST', 'generate-content', content_request)
        if response and response.status_code == 200:
            data = response.json()
            
            # Check basic structure
            has_content = len(data.get('generated_content', [])) > 0
            has_blog = data.get('blog_post') is not None
            has_newsletter = data.get('newsletter_article') is not None
            has_video_scripts = data.get('video_scripts') is not None
            
            # Check platform-specific content
            platforms_generated = [content.get('platform') for content in data.get('generated_content', [])]
            platforms_match = all(p in content_request['platforms'] for p in platforms_generated)
            
            # Check video suggestions for video-enabled platforms
            video_suggestions_present = any(
                content.get('video_suggestions') and content.get('video_suggestions') != 'Not applicable'
                for content in data.get('generated_content', [])
                if content.get('platform') in ['instagram', 'tiktok', 'facebook', 'youtube']
            )
            
            success = has_content and has_blog and has_newsletter and has_video_scripts and platforms_match
            details = f"Content: {len(data.get('generated_content', []))} platforms, Blog: {has_blog}, Newsletter: {has_newsletter}, Video Scripts: {len(data.get('video_scripts', []))}, Video suggestions: {video_suggestions_present}"
            
            self.log_test("Generate Content", success, details)
            return success
        else:
            error_msg = f"Status: {response.status_code if response else 'No response'}"
            if response:
                try:
                    error_data = response.json()
                    error_msg += f", Error: {error_data.get('detail', 'Unknown error')}"
                except:
                    error_msg += f", Response: {response.text[:200]}"
            self.log_test("Generate Content", False, error_msg)
            return False

    def test_schedule_post(self):
        """Test post scheduling functionality"""
        if not self.test_company_id:
            self.log_test("Schedule Post", False, "No test company ID available")
            return False
            
        scheduled_time = datetime.utcnow() + timedelta(hours=1)
        post_data = {
            "company_id": self.test_company_id,
            "platform": "instagram",
            "content": "Test post content for scheduling",
            "hashtags": ["test", "safety", "construction"],
            "scheduled_time": scheduled_time.isoformat(),
            "topic": "Test Topic"
        }
        
        response = self.make_request('POST', 'schedule-post', post_data)
        if response and response.status_code == 200:
            data = response.json()
            self.test_post_id = data.get('id')
            success = self.test_post_id is not None and data.get('status') == 'scheduled'
            self.log_test("Schedule Post", success, f"Scheduled post with ID: {self.test_post_id}")
            return success
        else:
            self.log_test("Schedule Post", False, f"Status: {response.status_code if response else 'No response'}")
            return False

    def test_get_calendar(self):
        """Test calendar functionality"""
        if not self.test_company_id:
            self.log_test("Get Calendar", False, "No test company ID available")
            return False
            
        current_date = datetime.now()
        params = {
            "month": current_date.month,
            "year": current_date.year
        }
        
        response = self.make_request('GET', f'calendar/{self.test_company_id}', params=params)
        if response and response.status_code == 200:
            data = response.json()
            success = isinstance(data, list)
            self.log_test("Get Calendar", success, f"Retrieved {len(data)} calendar entries")
            return success
        else:
            self.log_test("Get Calendar", False, f"Status: {response.status_code if response else 'No response'}")
            return False

    def test_update_post(self):
        """Test updating scheduled post"""
        if not self.test_post_id:
            self.log_test("Update Post", False, "No test post ID available")
            return False
            
        update_data = {
            "content": "Updated test post content",
            "status": "draft"
        }
        
        response = self.make_request('PUT', f'posts/{self.test_post_id}', update_data)
        if response and response.status_code == 200:
            data = response.json()
            success = data.get('content') == update_data['content']
            self.log_test("Update Post", success, f"Updated post content")
            return success
        else:
            self.log_test("Update Post", False, f"Status: {response.status_code if response else 'No response'}")
            return False

    def test_analytics_endpoints(self):
        """Test analytics functionality"""
        if not self.test_company_id:
            self.log_test("Analytics Endpoints", False, "No test company ID available")
            return False
            
        # Test saving analytics
        analytics_data = {
            "company_id": self.test_company_id,
            "platform": "instagram",
            "post_id": self.test_post_id or "test_post_id",
            "views": 1000,
            "likes": 50,
            "shares": 10,
            "comments": 5,
            "engagement_rate": 0.065,
            "reach": 800,
            "impressions": 1200,
            "click_through_rate": 0.02
        }
        
        save_response = self.make_request('POST', 'analytics', analytics_data)
        save_success = save_response and save_response.status_code == 200
        
        # Test getting analytics
        get_response = self.make_request('GET', f'analytics/{self.test_company_id}', params={"days": 30})
        get_success = get_response and get_response.status_code == 200
        
        if get_success:
            data = get_response.json()
            get_success = isinstance(data, list)
        
        success = save_success and get_success
        self.log_test("Analytics Endpoints", success, f"Save: {save_success}, Get: {get_success}")
        return success

    def test_monthly_report(self):
        """Test monthly report generation"""
        if not self.test_company_id:
            self.log_test("Monthly Report", False, "No test company ID available")
            return False
            
        current_date = datetime.now()
        params = {
            "month": current_date.month,
            "year": current_date.year
        }
        
        response = self.make_request('GET', f'reports/monthly/{self.test_company_id}', params=params)
        if response and response.status_code == 200:
            data = response.json()
            has_required_fields = all(field in data for field in [
                'company_id', 'month', 'year', 'total_posts', 'total_engagement',
                'top_performing_posts', 'platform_performance', 'recommendations'
            ])
            success = has_required_fields
            self.log_test("Monthly Report", success, f"Report generated with {data.get('total_posts', 0)} posts")
            return success
        else:
            self.log_test("Monthly Report", False, f"Status: {response.status_code if response else 'No response'}")
            return False

    def test_media_categories(self):
        """Test media categories endpoint"""
        if not self.test_company_id:
            self.log_test("Media Categories", False, "No test company ID available")
            return False
            
        response = self.make_request('GET', f'companies/{self.test_company_id}/media/categories')
        if response and response.status_code == 200:
            data = response.json()
            categories = data.get('categories', [])
            descriptions = data.get('descriptions', {})
            
            expected_categories = ['training', 'equipment', 'workplace', 'team', 'projects', 'safety', 'certificates', 'events']
            success = len(categories) >= 8 and all(cat in categories for cat in expected_categories)
            self.log_test("Media Categories", success, f"Found {len(categories)} categories with descriptions")
            return success
        else:
            self.log_test("Media Categories", False, f"Status: {response.status_code if response else 'No response'}")
            return False

    def test_get_company_media(self):
        """Test getting company media files"""
        if not self.test_company_id:
            self.log_test("Get Company Media", False, "No test company ID available")
            return False
            
        response = self.make_request('GET', f'companies/{self.test_company_id}/media')
        if response and response.status_code == 200:
            data = response.json()
            success = isinstance(data, list)
            self.log_test("Get Company Media", success, f"Retrieved {len(data)} media files")
            return success
        else:
            self.log_test("Get Company Media", False, f"Status: {response.status_code if response else 'No response'}")
            return False

    def test_monthly_media_requests(self):
        """Test monthly media requests endpoint"""
        response = self.make_request('GET', 'media/requests/monthly')
        if response and response.status_code == 200:
            data = response.json()
            requests_list = data.get('requests', [])
            total_companies = data.get('total_companies', 0)
            
            success = isinstance(requests_list, list) and isinstance(total_companies, int)
            self.log_test("Monthly Media Requests", success, f"Found {total_companies} companies needing media requests")
            return success
        else:
            self.log_test("Monthly Media Requests", False, f"Status: {response.status_code if response else 'No response'}")
            return False

    def test_media_request_prompt(self):
        """Test individual company media request prompt"""
        if not self.test_company_id:
            self.log_test("Media Request Prompt", False, "No test company ID available")
            return False
            
        response = self.make_request('GET', f'companies/{self.test_company_id}/media/request')
        if response and response.status_code == 200:
            data = response.json()
            required_fields = ['company_id', 'company_name', 'month', 'year', 'suggested_categories', 'current_media_count', 'recommendation']
            has_required_fields = all(field in data for field in required_fields)
            
            success = has_required_fields
            self.log_test("Media Request Prompt", success, f"Generated prompt for {data.get('company_name', 'Unknown')} with {data.get('current_media_count', 0)} media files")
            return success
        else:
            self.log_test("Media Request Prompt", False, f"Status: {response.status_code if response else 'No response'}")
            return False

    def test_mark_media_request_sent(self):
        """Test marking media request as sent"""
        if not self.test_company_id:
            self.log_test("Mark Media Request Sent", False, "No test company ID available")
            return False
            
        response = self.make_request('POST', f'companies/{self.test_company_id}/media/request/sent')
        if response and response.status_code == 200:
            data = response.json()
            success = 'marked as sent' in data.get('message', '')
            self.log_test("Mark Media Request Sent", success, "Media request marked as sent")
            return success
        else:
            self.log_test("Mark Media Request Sent", False, f"Status: {response.status_code if response else 'No response'}")
            return False

    def test_enhanced_content_generation_with_media(self):
        """Test enhanced content generation with media integration features"""
        if not self.test_company_id:
            self.log_test("Enhanced Content Generation with Media", False, "No test company ID available")
            return False
            
        content_request = {
            "company_id": self.test_company_id,
            "topic": "Construction Site Safety Training",
            "platforms": ["instagram", "facebook", "youtube"],
            "audience_level": "intermediate",
            "additional_context": "Focus on new OSHA regulations and proper PPE usage",
            "generate_blog": True,
            "generate_newsletter": True,
            "generate_video_script": True,
            "use_company_media": True,
            "media_preferences": {
                "instagram": "training,safety",
                "facebook": "workplace,team",
                "youtube": "equipment,projects"
            }
        }
        
        response = self.make_request('POST', 'generate-content', content_request)
        if response and response.status_code == 200:
            data = response.json()
            
            # Check enhanced media features
            has_media_suggestions = data.get('media_suggestions') is not None
            has_media_used = data.get('media_used') is not None
            
            # Check platform content has media integration
            platform_content = data.get('generated_content', [])
            has_media_placement = any(
                content.get('media_placement') for content in platform_content
            )
            has_suggested_media = any(
                content.get('suggested_media') for content in platform_content
            )
            
            # Check blog post media integration
            blog_post = data.get('blog_post')
            blog_has_media = blog_post and (
                blog_post.get('suggested_media') or blog_post.get('media_placement_guide')
            )
            
            # Check newsletter media integration
            newsletter = data.get('newsletter_article')
            newsletter_has_media = newsletter and (
                newsletter.get('suggested_media') or newsletter.get('media_placement_guide')
            )
            
            # Check video scripts media integration
            video_scripts = data.get('video_scripts', [])
            video_has_media = any(
                script.get('required_media') or script.get('media_timing')
                for script in video_scripts
            )
            
            success = (has_media_suggestions and has_media_used and has_media_placement and 
                      has_suggested_media and blog_has_media and newsletter_has_media and video_has_media)
            
            details = f"Media suggestions: {has_media_suggestions}, Media used: {has_media_used}, " \
                     f"Media placement: {has_media_placement}, Suggested media: {has_suggested_media}, " \
                     f"Blog media: {blog_has_media}, Newsletter media: {newsletter_has_media}, " \
                     f"Video media: {video_has_media}"
            
            self.log_test("Enhanced Content Generation with Media", success, details)
            return success
        else:
            error_msg = f"Status: {response.status_code if response else 'No response'}"
            if response:
                try:
                    error_data = response.json()
                    error_msg += f", Error: {error_data.get('detail', 'Unknown error')}"
                except:
                    error_msg += f", Response: {response.text[:200]}"
            self.log_test("Enhanced Content Generation with Media", False, error_msg)
            return False

    def test_delete_post(self):
        """Test deleting scheduled post"""
        if not self.test_post_id:
            self.log_test("Delete Post", False, "No test post ID available")
            return False
            
        response = self.make_request('DELETE', f'posts/{self.test_post_id}')
        if response and response.status_code == 200:
            data = response.json()
            success = 'deleted successfully' in data.get('message', '')
            self.log_test("Delete Post", success, "Post deleted successfully")
            return success
        else:
            self.log_test("Delete Post", False, f"Status: {response.status_code if response else 'No response'}")
            return False

    def run_all_tests(self):
        """Run all backend API tests"""
        print("🚀 Starting Comprehensive Backend API Testing")
        print("=" * 60)
        
        # Basic connectivity and configuration tests
        self.test_health_check()
        self.test_debug_endpoint()
        self.test_platforms_endpoint()
        self.test_content_examples()
        
        print("\n📊 Company Management Tests")
        print("-" * 30)
        self.test_create_company()
        self.test_get_companies()
        self.test_get_company_by_id()
        self.test_update_company()
        
        print("\n🎨 Content Generation Tests")
        print("-" * 30)
        self.test_generate_content()
        
        print("\n📅 Scheduling and Calendar Tests")
        print("-" * 30)
        self.test_schedule_post()
        self.test_get_calendar()
        self.test_update_post()
        
        print("\n📈 Analytics Tests")
        print("-" * 30)
        self.test_analytics_endpoints()
        self.test_monthly_report()
        
        print("\n🗑️ Cleanup Tests")
        print("-" * 30)
        self.test_delete_post()
        
        # Print final results
        print("\n" + "=" * 60)
        print(f"📊 FINAL RESULTS: {self.tests_passed}/{self.tests_run} tests passed")
        
        if self.tests_passed == self.tests_run:
            print("🎉 ALL TESTS PASSED! Backend API is working correctly.")
            return 0
        else:
            print(f"⚠️  {self.tests_run - self.tests_passed} tests failed. Check the issues above.")
            return 1

def main():
    """Main test execution"""
    print("Social Media Management Platform - Backend API Testing")
    print("Testing against: https://e7906d23-64b5-46c4-8078-8d731321a4b4.preview.emergentagent.com")
    print()
    
    tester = SocialMediaAPITester()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())