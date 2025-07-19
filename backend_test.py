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
    def __init__(self, base_url="https://e2e6ef8c-24a4-44d0-94bb-a56227ac3447.preview.emergentagent.com"):
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

    def test_seo_analysis(self):
        """Test AI-Powered SEO Content Optimization"""
        test_content = {
            "content": "Construction safety is crucial for workplace protection. OSHA compliance ensures worker safety through proper training and equipment usage. Safety protocols must be followed to prevent accidents and maintain a safe work environment.",
            "target_keywords": ["construction safety", "OSHA compliance", "workplace protection"]
        }
        
        response = self.make_request('POST', 'seo/analyze', test_content)
        if response and response.status_code == 200:
            data = response.json()
            
            # Check SEO analysis components
            has_seo_score = 'seo_score' in data and isinstance(data['seo_score'], (int, float))
            has_keyword_density = 'keyword_density' in data and isinstance(data['keyword_density'], dict)
            has_readability = 'readability_score' in data and isinstance(data['readability_score'], (int, float))
            has_meta_description = 'meta_description' in data
            has_recommendations = 'recommendations' in data and isinstance(data['recommendations'], list)
            
            success = all([has_seo_score, has_keyword_density, has_readability, has_meta_description, has_recommendations])
            details = f"SEO Score: {data.get('seo_score', 0)}, Readability: {data.get('readability_score', 0)}, Recommendations: {len(data.get('recommendations', []))}"
            
            self.log_test("SEO Analysis", success, details)
            return success
        else:
            self.log_test("SEO Analysis", False, f"Status: {response.status_code if response else 'No response'}")
            return False

    def test_hashtag_analysis(self):
        """Test Advanced Hashtag & Trend Analysis"""
        test_data = {
            "hashtags": ["#BuildSafe", "#ConstructionLife", "#SafetyFirst", "#OSHA", "#WorkplaceSafety"],
            "industry": "construction"
        }
        
        response = self.make_request('POST', 'hashtags/analyze', test_data)
        if response and response.status_code == 200:
            data = response.json()
            hashtag_analysis = data.get('hashtag_analysis', [])
            
            if hashtag_analysis:
                first_analysis = hashtag_analysis[0]
                has_popularity_score = 'popularity_score' in first_analysis
                has_engagement_rate = 'engagement_rate' in first_analysis
                has_competition_level = 'competition_level' in first_analysis
                has_trend_direction = 'trend_direction' in first_analysis
                has_related_hashtags = 'related_hashtags' in first_analysis
                has_estimated_reach = 'estimated_reach' in first_analysis
                
                success = all([has_popularity_score, has_engagement_rate, has_competition_level, 
                             has_trend_direction, has_related_hashtags, has_estimated_reach])
                details = f"Analyzed {len(hashtag_analysis)} hashtags with trend analysis"
            else:
                success = False
                details = "No hashtag analysis returned"
            
            self.log_test("Hashtag Analysis", success, details)
            return success
        else:
            self.log_test("Hashtag Analysis", False, f"Status: {response.status_code if response else 'No response'}")
            return False

    def test_trending_hashtags(self):
        """Test trending hashtags endpoint"""
        response = self.make_request('GET', 'hashtags/trending/construction')
        if response and response.status_code == 200:
            data = response.json()
            
            has_industry = 'industry' in data
            has_trending = 'trending_hashtags' in data
            trending_data = data.get('trending_hashtags', {})
            has_categories = all(cat in trending_data for cat in ['trending', 'stable', 'declining'])
            
            success = has_industry and has_trending and has_categories
            details = f"Industry: {data.get('industry')}, Categories: {list(trending_data.keys())}"
            
            self.log_test("Trending Hashtags", success, details)
            return success
        else:
            self.log_test("Trending Hashtags", False, f"Status: {response.status_code if response else 'No response'}")
            return False

    def test_performance_prediction(self):
        """Test Content Performance Prediction"""
        if not self.test_company_id:
            self.log_test("Performance Prediction", False, "No test company ID available")
            return False
            
        test_data = {
            "content": "New OSHA safety regulations require updated training protocols. Learn about the latest fall protection standards and how to implement them in your workplace.",
            "platform": "instagram",
            "hashtags": ["#SafetyFirst", "#OSHA", "#ConstructionSafety"],
            "company_id": self.test_company_id
        }
        
        response = self.make_request('POST', 'predict/performance', test_data)
        if response and response.status_code == 200:
            data = response.json()
            
            has_prediction = 'predicted_performance' in data
            has_confidence = 'confidence_level' in data
            has_recommendations = 'recommendations' in data
            has_platform = data.get('platform') == test_data['platform']
            
            success = all([has_prediction, has_confidence, has_recommendations, has_platform])
            details = f"Prediction: {data.get('predicted_performance', 0)}, Confidence: {data.get('confidence_level')}"
            
            self.log_test("Performance Prediction", success, details)
            return success
        else:
            self.log_test("Performance Prediction", False, f"Status: {response.status_code if response else 'No response'}")
            return False

    def test_content_repurposing(self):
        """Test Cross-Platform Content Repurposing"""
        test_data = {
            "content": "Construction safety training is essential for preventing workplace accidents. Our comprehensive OSHA-compliant programs ensure your team stays safe and productive.",
            "platforms": ["instagram", "tiktok", "facebook", "linkedin"]
        }
        
        response = self.make_request('POST', 'content/repurpose', test_data)
        if response and response.status_code == 200:
            data = response.json()
            
            has_original = 'original_content' in data
            has_variations = 'variations' in data
            has_platforms = 'platforms' in data
            
            variations = data.get('variations', {})
            all_platforms_covered = all(platform in variations for platform in test_data['platforms'])
            
            success = has_original and has_variations and has_platforms and all_platforms_covered
            details = f"Repurposed for {len(variations)} platforms: {list(variations.keys())}"
            
            self.log_test("Content Repurposing", success, details)
            return success
        else:
            self.log_test("Content Repurposing", False, f"Status: {response.status_code if response else 'No response'}")
            return False

    def test_roi_analytics(self):
        """Test ROI Analytics & Tracking"""
        if not self.test_company_id:
            self.log_test("ROI Analytics", False, "No test company ID available")
            return False
            
        response = self.make_request('GET', f'analytics/{self.test_company_id}/roi')
        if response and response.status_code == 200:
            data = response.json()
            
            # Check ROI metrics structure
            expected_fields = ['total_investment', 'leads_generated', 'conversions', 'revenue_attributed', 
                             'cost_per_lead', 'roi_percentage', 'platform_breakdown', 'content_type_performance']
            
            has_required_fields = all(field in data for field in expected_fields)
            has_platform_breakdown = isinstance(data.get('platform_breakdown', {}), dict)
            has_content_performance = isinstance(data.get('content_type_performance', {}), dict)
            
            success = has_required_fields and has_platform_breakdown and has_content_performance
            details = f"ROI: {data.get('roi_percentage', 0)}%, Platforms: {len(data.get('platform_breakdown', {}))}"
            
            self.log_test("ROI Analytics", success, details)
            return success
        else:
            self.log_test("ROI Analytics", False, f"Status: {response.status_code if response else 'No response'}")
            return False

    def test_enhanced_content_generation_with_advanced_features(self):
        """Test Enhanced Content Generation with all revolutionary features"""
        if not self.test_company_id:
            self.log_test("Enhanced Content Generation", False, "No test company ID available")
            return False
            
        content_request = {
            "company_id": self.test_company_id,
            "topic": "Advanced PPE Safety Training",
            "platforms": ["instagram", "facebook", "youtube", "linkedin"],
            "audience_level": "intermediate",
            "additional_context": "Focus on new OSHA regulations and proper PPE usage",
            "generate_blog": True,
            "generate_newsletter": True,
            "generate_video_script": True,
            "use_company_media": True,
            "seo_focus": True,
            "target_keywords": ["PPE safety", "OSHA compliance", "safety training"],
            "competitor_analysis": True,
            "repurpose_content": True
        }
        
        response = self.make_request('POST', 'generate-content', content_request)
        if response and response.status_code == 200:
            data = response.json()
            
            # Check revolutionary features
            has_seo_recommendations = data.get('seo_recommendations') is not None
            has_hashtag_strategy = data.get('hashtag_strategy') is not None
            has_performance_forecast = data.get('performance_forecast') is not None
            has_repurposed_content = data.get('repurposed_content') is not None
            
            # Check platform content has advanced features
            platform_content = data.get('generated_content', [])
            has_seo_analysis = any(content.get('seo_analysis') for content in platform_content)
            has_hashtag_analysis = any(content.get('hashtag_analysis') for content in platform_content)
            has_performance_prediction = any(content.get('performance_prediction') for content in platform_content)
            has_repurposed_versions = any(content.get('repurposed_versions') for content in platform_content)
            
            # Check blog post advanced features
            blog_post = data.get('blog_post')
            blog_has_seo = blog_post and blog_post.get('seo_analysis')
            blog_has_schema = blog_post and blog_post.get('schema_markup')
            blog_has_links = blog_post and (blog_post.get('internal_links') or blog_post.get('external_links'))
            
            success = all([
                has_seo_recommendations, has_hashtag_strategy, has_performance_forecast,
                has_seo_analysis, has_hashtag_analysis, has_performance_prediction,
                blog_has_seo, blog_has_schema
            ])
            
            details = f"SEO: {has_seo_recommendations}, Hashtag Strategy: {has_hashtag_strategy}, " \
                     f"Performance Forecast: {has_performance_forecast}, Blog SEO: {blog_has_seo}, " \
                     f"Schema Markup: {blog_has_schema}"
            
            self.log_test("Enhanced Content Generation", success, details)
            return success
        else:
            error_msg = f"Status: {response.status_code if response else 'No response'}"
            if response:
                try:
                    error_data = response.json()
                    error_msg += f", Error: {error_data.get('detail', 'Unknown error')}"
                except:
                    error_msg += f", Response: {response.text[:200]}"
            self.log_test("Enhanced Content Generation", False, error_msg)
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

    # Beta Feedback System Tests
    def test_beta_login(self):
        """Test beta user login/registration"""
        test_beta_data = {
            "beta_id": f"BETA{datetime.now().strftime('%H%M%S')}",
            "name": "John Safety Manager",
            "email": f"beta.tester.{datetime.now().strftime('%H%M%S')}@construction.com"
        }
        
        response = self.make_request('POST', 'beta/login', test_beta_data)
        if response and response.status_code == 200:
            data = response.json()
            success = data.get('beta_user_id') is not None and data.get('status') == 'success'
            self.test_beta_user_id = data.get('beta_user_id')  # Store for other tests
            self.log_test("Beta Login", success, f"Beta user registered: {data.get('beta_user_id')}")
            return success
        else:
            self.log_test("Beta Login", False, f"Status: {response.status_code if response else 'No response'}")
            return False

    def test_submit_beta_feedback(self):
        """Test submitting beta feedback"""
        if not hasattr(self, 'test_beta_user_id') or not self.test_beta_user_id:
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
            "category": "training"
        }
        
        response = self.make_request('POST', 'beta/feedback', feedback_data)
        if response and response.status_code == 200:
            data = response.json()
            success = data.get('feedback_id') is not None and data.get('status') == 'submitted'
            self.test_feedback_id = data.get('feedback_id')  # Store for other tests
            self.log_test("Submit Beta Feedback", success, f"Feedback submitted: {data.get('feedback_id')}")
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
        if not hasattr(self, 'test_feedback_id') or not self.test_feedback_id:
            self.log_test("Update Feedback Status", False, "No feedback ID available")
            return False
            
        update_data = {
            "status": "in_progress",
            "admin_response": "Great suggestion! We're evaluating VR integration options.",
            "implementation_notes": "Researching VR training platforms for Q2 implementation"
        }
        
        response = self.make_request('PUT', f'beta/feedback/{self.test_feedback_id}', update_data)
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
        if not hasattr(self, 'test_feedback_id') or not self.test_feedback_id:
            self.log_test("Vote Feedback", False, "No feedback ID available")
            return False
        if not hasattr(self, 'test_beta_user_id') or not self.test_beta_user_id:
            self.log_test("Vote Feedback", False, "No beta user ID available")
            return False
            
        vote_data = {
            "beta_user_id": self.test_beta_user_id
        }
        
        response = self.make_request('POST', f'beta/feedback/{self.test_feedback_id}/vote', vote_data)
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
        if not hasattr(self, 'test_beta_user_id') or not self.test_beta_user_id:
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

    # SEO Monitoring Add-on Tests
    def test_purchase_seo_addon(self):
        """Test purchasing SEO monitoring add-on"""
        if not self.test_company_id:
            self.log_test("Purchase SEO Addon", False, "No test company ID available")
            return False
            
        addon_data = {
            "company_id": self.test_company_id,
            "website_url": "https://safetyfirstconstruction.com",
            "notification_email": "seo@safetyfirstconstruction.com",
            "plan_type": "standard"
        }
        
        response = self.make_request('POST', 'seo-addon/purchase', addon_data)
        if response and response.status_code == 200:
            data = response.json()
            success = data.get('addon_id') is not None and data.get('status') == 'active'
            self.test_seo_addon_id = data.get('addon_id')  # Store for other tests
            self.log_test("Purchase SEO Addon", success, f"SEO addon purchased: {data.get('addon_id')}")
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
            expected_fields = ['company_id', 'website_url', 'monitoring_status', 'daily_checks_limit', 'daily_checks_used']
            has_required_fields = all(field in data for field in expected_fields)
            success = has_required_fields and data.get('monitoring_status') in ['active', 'paused', 'expired']
            self.log_test("Get SEO Addon Status", success, f"Status: {data.get('monitoring_status')}, Checks: {data.get('daily_checks_used', 0)}/{data.get('daily_checks_limit', 0)}")
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
            
        audit_data = {
            "page_url": "https://safetyfirstconstruction.com/safety-training"
        }
        
        response = self.make_request('POST', f'seo-addon/{self.test_company_id}/audit', audit_data)
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

    def test_competitor_analysis(self):
        """Test new Competitor Analysis endpoint"""
        competitor_request = {
            "website_url": "https://example.com",
            "competitor_name": "Example Company",
            "analysis_type": "comprehensive",
            "social_platforms": ["Instagram", "Facebook"],
            "company_id": "demo-company"
        }
        
        response = self.make_request('POST', 'competitor/analyze', competitor_request)
        if response and response.status_code == 200:
            data = response.json()
            
            # Check basic response structure
            has_status = data.get('status') == 'success'
            has_message = 'message' in data
            has_competitor_name = data.get('competitor_name') == competitor_request['competitor_name']
            has_website_url = data.get('website_url') == competitor_request['website_url']
            has_analysis_type = data.get('analysis_type') == competitor_request['analysis_type']
            has_social_platforms = data.get('social_platforms') == competitor_request['social_platforms']
            has_company_id = data.get('company_id') == competitor_request['company_id']
            
            # Check analysis content structure
            has_website_analysis = 'website_analysis' in data and data['website_analysis']
            has_social_media_analysis = 'social_media_analysis' in data
            has_strengths = 'strengths' in data and isinstance(data['strengths'], list)
            has_weaknesses = 'weaknesses' in data and isinstance(data['weaknesses'], list)
            has_recommendations = 'recommendations' in data and data['recommendations']
            has_opportunities = 'opportunities' in data and data['opportunities']
            has_full_analysis = 'full_analysis' in data and data['full_analysis']
            has_created_at = 'created_at' in data
            has_id = 'id' in data
            
            # Check if analysis was stored in database (has ID)
            stored_in_db = has_id and data['id']
            
            success = all([
                has_status, has_message, has_competitor_name, has_website_url, 
                has_analysis_type, has_social_platforms, has_company_id,
                has_website_analysis, has_strengths, has_weaknesses, 
                has_recommendations, has_opportunities, has_full_analysis,
                has_created_at, stored_in_db
            ])
            
            details = f"Analysis ID: {data.get('id', 'None')}, Strengths: {len(data.get('strengths', []))}, " \
                     f"Weaknesses: {len(data.get('weaknesses', []))}, Stored in DB: {stored_in_db}"
            
            self.log_test("Competitor Analysis", success, details)
            return success
        else:
            error_msg = f"Status: {response.status_code if response else 'No response'}"
            if response:
                try:
                    error_data = response.json()
                    error_msg += f", Error: {error_data.get('detail', 'Unknown error')}"
                except:
                    error_msg += f", Response: {response.text[:200]}"
            self.log_test("Competitor Analysis", False, error_msg)
            return False

    def test_get_competitor_analyses(self):
        """Test getting competitor analyses for a company"""
        company_id = "demo-company"
        
        response = self.make_request('GET', f'competitor/analyses/{company_id}')
        if response and response.status_code == 200:
            data = response.json()
            
            has_status = data.get('status') == 'success'
            has_analyses = 'analyses' in data and isinstance(data['analyses'], list)
            
            analyses = data.get('analyses', [])
            analyses_count = len(analyses)
            
            # If we have analyses, check structure of first one
            structure_valid = True
            if analyses:
                first_analysis = analyses[0]
                required_fields = ['id', 'company_id', 'competitor_name', 'website_url', 
                                 'analysis_type', 'website_analysis', 'strengths', 'weaknesses',
                                 'recommendations', 'opportunities', 'created_at']
                structure_valid = all(field in first_analysis for field in required_fields)
            
            success = has_status and has_analyses and structure_valid
            details = f"Retrieved {analyses_count} analyses, Structure valid: {structure_valid}"
            
            self.log_test("Get Competitor Analyses", success, details)
            return success
        else:
            self.log_test("Get Competitor Analyses", False, f"Status: {response.status_code if response else 'No response'}")
            return False

    def run_all_tests(self):
        """Run all backend API tests including revolutionary AI-powered features and new Beta/SEO features"""
        print("🚀 Starting Comprehensive Backend API Testing - Revolutionary AI Features + New Beta & SEO Features")
        print("=" * 90)
        
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
        
        print("\n🔍 Revolutionary AI-Powered SEO Features")
        print("-" * 40)
        self.test_seo_analysis()
        
        print("\n📈 Advanced Hashtag & Trend Analysis")
        print("-" * 40)
        self.test_hashtag_analysis()
        self.test_trending_hashtags()
        
        print("\n🎯 Content Performance Prediction")
        print("-" * 40)
        self.test_performance_prediction()
        
        print("\n🔄 Cross-Platform Content Repurposing")
        print("-" * 40)
        self.test_content_repurposing()
        
        print("\n💰 ROI Analytics & Tracking")
        print("-" * 40)
        self.test_roi_analytics()
        
        print("\n📁 Enhanced Media Management")
        print("-" * 30)
        self.test_media_categories()
        self.test_get_company_media()
        self.test_monthly_media_requests()
        self.test_media_request_prompt()
        self.test_mark_media_request_sent()
        
        print("\n🎨 Revolutionary Content Generation")
        print("-" * 40)
        self.test_generate_content()
        self.test_enhanced_content_generation_with_advanced_features()
        
        print("\n📅 Scheduling and Calendar Tests")
        print("-" * 30)
        self.test_schedule_post()
        self.test_get_calendar()
        self.test_update_post()
        
        print("\n📈 Analytics Tests")
        print("-" * 30)
        self.test_analytics_endpoints()
        self.test_monthly_report()
        
        print("\n🧪 NEW: Beta Feedback System Tests")
        print("-" * 40)
        self.test_beta_login()
        self.test_submit_beta_feedback()
        self.test_get_beta_feedback()
        self.test_update_feedback_status()
        self.test_vote_feedback()
        self.test_get_beta_user_stats()
        
        print("\n🔍 NEW: SEO Monitoring Add-on Tests")
        print("-" * 40)
        self.test_purchase_seo_addon()
        self.test_get_seo_addon_status()
        self.test_get_latest_seo_parameters()
        self.test_run_website_audit()
        self.test_get_website_audits()
        self.test_run_daily_seo_research()
        
        print("\n🏢 NEW: Competitor Analysis Tests")
        print("-" * 40)
        self.test_competitor_analysis()
        self.test_get_competitor_analyses()
        
        print("\n🗑️ Cleanup Tests")
        print("-" * 30)
        self.test_delete_post()
        
        # Print final results
        print("\n" + "=" * 90)
        print(f"📊 FINAL RESULTS: {self.tests_passed}/{self.tests_run} tests passed")
        
        if self.tests_passed == self.tests_run:
            print("🎉 ALL TESTS PASSED! Revolutionary AI-Powered Social Media Platform with Beta & SEO Features is working correctly!")
            print("✨ Features tested: SEO Analysis, Hashtag Intelligence, Performance Prediction,")
            print("   Content Repurposing, ROI Tracking, Enhanced Media Management,")
            print("   🆕 Beta Feedback System, 🆕 SEO Monitoring Add-on, 🆕 Competitor Analysis")
            return 0
        else:
            print(f"⚠️  {self.tests_run - self.tests_passed} tests failed. Check the issues above.")
            return 1

def main():
    """Main test execution"""
    print("Social Media Management Platform - Backend API Testing")
    print("Testing against: https://e2e6ef8c-24a4-44d0-94bb-a56227ac3447.preview.emergentagent.com")
    print()
    
    tester = SocialMediaAPITester()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())