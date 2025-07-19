#!/usr/bin/env python3
"""
Focused Competitor Analysis Backend Testing
Tests the new competitor analysis endpoint specifically
"""

import requests
import json
import sys
from datetime import datetime

class CompetitorAnalysisTester:
    def __init__(self, base_url="https://e2e6ef8c-24a4-44d0-94bb-a56227ac3447.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0

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
                response = requests.get(url, headers=headers, params=params, timeout=60)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=60)
            
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

    def test_competitor_analysis(self):
        """Test new Competitor Analysis endpoint"""
        competitor_request = {
            "website_url": "https://example.com",
            "competitor_name": "Example Company",
            "analysis_type": "comprehensive",
            "social_platforms": ["Instagram", "Facebook"],
            "company_id": "demo-company"
        }
        
        print(f"🔍 Testing competitor analysis with request: {json.dumps(competitor_request, indent=2)}")
        
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
            
            print(f"📊 Response validation:")
            print(f"   Status: {has_status} ({data.get('status')})")
            print(f"   Message: {has_message} ({data.get('message', 'N/A')[:50]}...)")
            print(f"   Competitor Name: {has_competitor_name} ({data.get('competitor_name')})")
            print(f"   Website URL: {has_website_url} ({data.get('website_url')})")
            print(f"   Analysis Type: {has_analysis_type} ({data.get('analysis_type')})")
            print(f"   Social Platforms: {has_social_platforms} ({data.get('social_platforms')})")
            print(f"   Company ID: {has_company_id} ({data.get('company_id')})")
            print(f"   Website Analysis: {has_website_analysis} ({len(data.get('website_analysis', '')) if data.get('website_analysis') else 0} chars)")
            print(f"   Social Media Analysis: {has_social_media_analysis} ({len(data.get('social_media_analysis', '')) if data.get('social_media_analysis') else 0} chars)")
            print(f"   Strengths: {has_strengths} ({len(data.get('strengths', []))} items)")
            print(f"   Weaknesses: {has_weaknesses} ({len(data.get('weaknesses', []))} items)")
            print(f"   Recommendations: {has_recommendations} ({len(data.get('recommendations', '')) if data.get('recommendations') else 0} chars)")
            print(f"   Opportunities: {has_opportunities} ({len(data.get('opportunities', '')) if data.get('opportunities') else 0} chars)")
            print(f"   Full Analysis: {has_full_analysis} ({len(data.get('full_analysis', '')) if data.get('full_analysis') else 0} chars)")
            print(f"   Created At: {has_created_at} ({data.get('created_at')})")
            print(f"   Database ID: {stored_in_db} ({data.get('id')})")
            
            if data.get('strengths'):
                print(f"   Sample Strengths: {data['strengths'][:3]}")
            if data.get('weaknesses'):
                print(f"   Sample Weaknesses: {data['weaknesses'][:3]}")
            
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
                    print(f"❌ Error response: {json.dumps(error_data, indent=2)}")
                except:
                    error_msg += f", Response: {response.text[:200]}"
                    print(f"❌ Raw response: {response.text[:500]}")
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
            
            print(f"📊 Retrieved {analyses_count} competitor analyses")
            
            # If we have analyses, check structure of first one
            structure_valid = True
            if analyses:
                first_analysis = analyses[0]
                required_fields = ['id', 'company_id', 'competitor_name', 'website_url', 
                                 'analysis_type', 'website_analysis', 'strengths', 'weaknesses',
                                 'recommendations', 'opportunities', 'created_at']
                structure_valid = all(field in first_analysis for field in required_fields)
                
                print(f"   First analysis: {first_analysis.get('competitor_name')} ({first_analysis.get('website_url')})")
                print(f"   Analysis type: {first_analysis.get('analysis_type')}")
                print(f"   Strengths: {len(first_analysis.get('strengths', []))}")
                print(f"   Weaknesses: {len(first_analysis.get('weaknesses', []))}")
                print(f"   Created: {first_analysis.get('created_at')}")
            
            success = has_status and has_analyses and structure_valid
            details = f"Retrieved {analyses_count} analyses, Structure valid: {structure_valid}"
            
            self.log_test("Get Competitor Analyses", success, details)
            return success
        else:
            self.log_test("Get Competitor Analyses", False, f"Status: {response.status_code if response else 'No response'}")
            return False

    def run_competitor_tests(self):
        """Run competitor analysis specific tests"""
        print("🏢 Starting Competitor Analysis Backend Testing")
        print("=" * 60)
        
        # Basic connectivity test
        self.test_health_check()
        
        print("\n🏢 Competitor Analysis Tests")
        print("-" * 40)
        self.test_competitor_analysis()
        self.test_get_competitor_analyses()
        
        # Print final results
        print("\n" + "=" * 60)
        print(f"📊 FINAL RESULTS: {self.tests_passed}/{self.tests_run} tests passed")
        
        if self.tests_passed == self.tests_run:
            print("🎉 ALL COMPETITOR ANALYSIS TESTS PASSED!")
            print("✨ Competitor Analysis endpoint is working correctly!")
            return 0
        else:
            print(f"⚠️  {self.tests_run - self.tests_passed} tests failed. Check the issues above.")
            return 1

def main():
    """Main test execution"""
    print("Competitor Analysis Backend Testing")
    print("Testing against: https://e2e6ef8c-24a4-44d0-94bb-a56227ac3447.preview.emergentagent.com")
    print()
    
    tester = CompetitorAnalysisTester()
    return tester.run_competitor_tests()

if __name__ == "__main__":
    sys.exit(main())