#!/usr/bin/env python3
"""
Media Upload Functionality Testing for PostVelocity
Tests media upload with company selection, file validation, and multi-company isolation
"""

import requests
import json
import sys
import io
import os
from datetime import datetime
from pathlib import Path

class MediaUploadTester:
    def __init__(self, base_url="https://9b531162-6bde-47f4-84ae-bcc0317537cc.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.test_companies = []
        self.uploaded_media = []

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

    def make_request(self, method, endpoint, data=None, params=None, files=None):
        """Make HTTP request with error handling"""
        url = f"{self.base_url}/api/{endpoint}"
        headers = {}
        
        # Don't set Content-Type for file uploads
        if not files:
            headers['Content-Type'] = 'application/json'
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params, timeout=30)
            elif method == 'POST':
                if files:
                    response = requests.post(url, data=data, files=files, timeout=30)
                else:
                    response = requests.post(url, json=data, headers=headers, timeout=30)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=30)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=30)
            
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request error: {str(e)}")
            return None

    def create_test_companies(self):
        """Create multiple test companies for isolation testing"""
        companies_data = [
            {
                "name": f"Construction Corp {datetime.now().strftime('%H%M%S')}",
                "industry": "construction",
                "website": "https://constructioncorp.com",
                "description": "Construction company for media testing",
                "target_audience": "Construction workers, safety managers"
            },
            {
                "name": f"Safety Solutions {datetime.now().strftime('%H%M%S')}",
                "industry": "safety",
                "website": "https://safetysolutions.com", 
                "description": "Safety consulting company for media testing",
                "target_audience": "Safety professionals, compliance officers"
            },
            {
                "name": f"Environmental Services {datetime.now().strftime('%H%M%S')}",
                "industry": "environmental",
                "website": "https://enviroservices.com",
                "description": "Environmental services company for media testing",
                "target_audience": "Environmental engineers, facility managers"
            }
        ]
        
        for company_data in companies_data:
            response = self.make_request('POST', 'companies', company_data)
            if response and response.status_code == 200:
                data = response.json()
                company_id = data.get('id')
                if company_id:
                    self.test_companies.append({
                        'id': company_id,
                        'name': data.get('name'),
                        'industry': company_data['industry']
                    })
        
        success = len(self.test_companies) == 3
        self.log_test("Create Test Companies", success, 
                     f"Created {len(self.test_companies)} companies: {[c['name'] for c in self.test_companies]}")
        return success

    def create_test_image_file(self, filename="test_image.jpg"):
        """Create a simple test image file in memory"""
        # Create a simple 1x1 pixel JPEG image
        jpeg_data = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x01\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00\xaa\xff\xd9'
        return io.BytesIO(jpeg_data)

    def test_media_categories_endpoint(self):
        """Test media categories endpoint for existing companies"""
        if not self.test_companies:
            self.log_test("Media Categories Endpoint", False, "No test companies available")
            return False
        
        company = self.test_companies[0]
        response = self.make_request('GET', f'companies/{company["id"]}/media/categories')
        
        if response and response.status_code == 200:
            data = response.json()
            categories = data.get('categories', [])
            descriptions = data.get('descriptions', {})
            
            # Check for required categories from the review request
            required_categories = ['training', 'workplace', 'equipment', 'team', 'events', 'safety']
            has_required = all(cat in categories for cat in required_categories)
            has_descriptions = all(cat in descriptions for cat in required_categories)
            
            success = has_required and has_descriptions and len(categories) >= 6
            self.log_test("Media Categories Endpoint", success, 
                         f"Found {len(categories)} categories: {categories}")
            return success
        else:
            self.log_test("Media Categories Endpoint", False, 
                         f"Status: {response.status_code if response else 'No response'}")
            return False

    def test_media_upload_for_company(self, company, category="training", description="Test media upload"):
        """Test media upload for a specific company"""
        # Create test image file
        test_file = self.create_test_image_file(f"test_{company['name'].replace(' ', '_')}.jpg")
        
        # Prepare form data
        files = {
            'file': (f"test_{category}.jpg", test_file, 'image/jpeg')
        }
        data = {
            'category': category,
            'description': description,
            'tags': f"test,{category},{company['industry']}",
            'seo_alt_text': f"{company['name']} {category} image"
        }
        
        response = self.make_request('POST', f'companies/{company["id"]}/media/upload', 
                                   data=data, files=files)
        
        if response and response.status_code == 200:
            media_data = response.json()
            media_id = media_data.get('id')
            
            # Verify response structure
            required_fields = ['id', 'company_id', 'filename', 'category', 'description', 'file_size']
            has_required_fields = all(field in media_data for field in required_fields)
            
            # Verify company association
            correct_company = media_data.get('company_id') == company['id']
            correct_category = media_data.get('category') == category
            
            if media_id and has_required_fields and correct_company and correct_category:
                self.uploaded_media.append({
                    'id': media_id,
                    'company_id': company['id'],
                    'company_name': company['name'],
                    'category': category,
                    'filename': media_data.get('filename')
                })
                
                success = True
                details = f"Uploaded {media_data.get('filename')} ({media_data.get('file_size')} bytes) to {company['name']}"
            else:
                success = False
                details = f"Missing fields or incorrect association: company_id={media_data.get('company_id')}, category={media_data.get('category')}"
            
            self.log_test(f"Media Upload - {company['name']}", success, details)
            return success
        else:
            error_msg = f"Status: {response.status_code if response else 'No response'}"
            if response:
                try:
                    error_data = response.json()
                    error_msg += f", Error: {error_data.get('detail', 'Unknown error')}"
                except:
                    error_msg += f", Response: {response.text[:200]}"
            
            self.log_test(f"Media Upload - {company['name']}", False, error_msg)
            return False

    def test_media_upload_different_categories(self):
        """Test uploading media with different categories"""
        if not self.test_companies:
            self.log_test("Media Upload Different Categories", False, "No test companies available")
            return False
        
        categories_to_test = ['training', 'equipment', 'workplace', 'team', 'events', 'safety']
        company = self.test_companies[0]
        successful_uploads = 0
        
        for category in categories_to_test:
            if self.test_media_upload_for_company(company, category, f"Test {category} media"):
                successful_uploads += 1
        
        success = successful_uploads == len(categories_to_test)
        self.log_test("Media Upload Different Categories", success, 
                     f"Successfully uploaded {successful_uploads}/{len(categories_to_test)} categories")
        return success

    def test_company_media_retrieval(self):
        """Test retrieving media for specific companies"""
        if not self.test_companies:
            self.log_test("Company Media Retrieval", False, "No test companies available")
            return False
        
        all_retrievals_successful = True
        
        for company in self.test_companies:
            response = self.make_request('GET', f'companies/{company["id"]}/media')
            
            if response and response.status_code == 200:
                media_files = response.json()
                
                # Check that all media belongs to this company
                company_media = [m for m in self.uploaded_media if m['company_id'] == company['id']]
                expected_count = len(company_media)
                actual_count = len(media_files)
                
                # Verify company association
                correct_association = all(
                    media.get('company_id') == company['id'] 
                    for media in media_files
                )
                
                if correct_association and actual_count >= expected_count:
                    self.log_test(f"Media Retrieval - {company['name']}", True, 
                                 f"Retrieved {actual_count} media files (expected >= {expected_count})")
                else:
                    self.log_test(f"Media Retrieval - {company['name']}", False, 
                                 f"Retrieved {actual_count} files, expected >= {expected_count}, correct association: {correct_association}")
                    all_retrievals_successful = False
            else:
                self.log_test(f"Media Retrieval - {company['name']}", False, 
                             f"Status: {response.status_code if response else 'No response'}")
                all_retrievals_successful = False
        
        return all_retrievals_successful

    def test_media_filtering_by_category(self):
        """Test filtering media by category"""
        if not self.test_companies or not self.uploaded_media:
            self.log_test("Media Filtering by Category", False, "No test data available")
            return False
        
        company = self.test_companies[0]
        test_category = 'training'
        
        # Get media filtered by category
        params = {'category': test_category}
        response = self.make_request('GET', f'companies/{company["id"]}/media', params=params)
        
        if response and response.status_code == 200:
            filtered_media = response.json()
            
            # Verify all returned media has the correct category
            correct_category = all(
                media.get('category') == test_category 
                for media in filtered_media
            )
            
            # Verify all media belongs to the correct company
            correct_company = all(
                media.get('company_id') == company['id']
                for media in filtered_media
            )
            
            success = correct_category and correct_company and len(filtered_media) > 0
            self.log_test("Media Filtering by Category", success, 
                         f"Retrieved {len(filtered_media)} {test_category} media files")
            return success
        else:
            self.log_test("Media Filtering by Category", False, 
                         f"Status: {response.status_code if response else 'No response'}")
            return False

    def test_multi_company_media_isolation(self):
        """Test that companies only see their own media"""
        if len(self.test_companies) < 2:
            self.log_test("Multi-Company Media Isolation", False, "Need at least 2 companies")
            return False
        
        # Upload media to different companies
        company1 = self.test_companies[0]
        company2 = self.test_companies[1]
        
        # Upload to company1
        self.test_media_upload_for_company(company1, "safety", "Company 1 safety media")
        
        # Upload to company2  
        self.test_media_upload_for_company(company2, "safety", "Company 2 safety media")
        
        # Check company1 media
        response1 = self.make_request('GET', f'companies/{company1["id"]}/media')
        # Check company2 media
        response2 = self.make_request('GET', f'companies/{company2["id"]}/media')
        
        if response1 and response1.status_code == 200 and response2 and response2.status_code == 200:
            media1 = response1.json()
            media2 = response2.json()
            
            # Verify isolation - company1 media should only belong to company1
            company1_isolation = all(m.get('company_id') == company1['id'] for m in media1)
            # Verify isolation - company2 media should only belong to company2
            company2_isolation = all(m.get('company_id') == company2['id'] for m in media2)
            
            # Verify no cross-contamination
            company1_ids = {m.get('id') for m in media1}
            company2_ids = {m.get('id') for m in media2}
            no_overlap = len(company1_ids.intersection(company2_ids)) == 0
            
            success = company1_isolation and company2_isolation and no_overlap
            self.log_test("Multi-Company Media Isolation", success, 
                         f"Company1: {len(media1)} files, Company2: {len(media2)} files, No overlap: {no_overlap}")
            return success
        else:
            self.log_test("Multi-Company Media Isolation", False, "Failed to retrieve media for comparison")
            return False

    def test_file_upload_validation(self):
        """Test file upload validation (file types, etc.)"""
        if not self.test_companies:
            self.log_test("File Upload Validation", False, "No test companies available")
            return False
        
        company = self.test_companies[0]
        
        # Test 1: Valid image file (should succeed)
        test_file = self.create_test_image_file("valid_test.jpg")
        files = {'file': ("valid_test.jpg", test_file, 'image/jpeg')}
        data = {'category': 'training', 'description': 'Valid image test'}
        
        response = self.make_request('POST', f'companies/{company["id"]}/media/upload', 
                                   data=data, files=files)
        valid_upload = response and response.status_code == 200
        
        # Test 2: Invalid file type (should fail)
        invalid_file = io.BytesIO(b"This is not an image file")
        files = {'file': ("invalid_test.txt", invalid_file, 'text/plain')}
        data = {'category': 'training', 'description': 'Invalid file test'}
        
        response = self.make_request('POST', f'companies/{company["id"]}/media/upload', 
                                   data=data, files=files)
        invalid_rejected = response and response.status_code == 400
        
        # Test 3: Non-existent company (should fail)
        test_file = self.create_test_image_file("nonexistent_company_test.jpg")
        files = {'file': ("test.jpg", test_file, 'image/jpeg')}
        data = {'category': 'training', 'description': 'Non-existent company test'}
        
        fake_company_id = "507f1f77bcf86cd799439011"  # Valid ObjectId format but non-existent
        response = self.make_request('POST', f'companies/{fake_company_id}/media/upload', 
                                   data=data, files=files)
        nonexistent_rejected = response and response.status_code == 404
        
        success = valid_upload and invalid_rejected and nonexistent_rejected
        self.log_test("File Upload Validation", success, 
                     f"Valid upload: {valid_upload}, Invalid rejected: {invalid_rejected}, Non-existent company rejected: {nonexistent_rejected}")
        return success

    def test_media_metadata_handling(self):
        """Test metadata handling (categories, descriptions, tags)"""
        if not self.test_companies:
            self.log_test("Media Metadata Handling", False, "No test companies available")
            return False
        
        company = self.test_companies[0]
        
        # Upload with comprehensive metadata
        test_file = self.create_test_image_file("metadata_test.jpg")
        files = {'file': ("metadata_test.jpg", test_file, 'image/jpeg')}
        data = {
            'category': 'equipment',
            'description': 'Heavy machinery safety demonstration',
            'tags': 'safety,equipment,machinery,demonstration,training',
            'seo_alt_text': 'Construction workers using heavy machinery with proper safety equipment'
        }
        
        response = self.make_request('POST', f'companies/{company["id"]}/media/upload', 
                                   data=data, files=files)
        
        if response and response.status_code == 200:
            media_data = response.json()
            
            # Verify metadata preservation
            correct_category = media_data.get('category') == 'equipment'
            correct_description = media_data.get('description') == data['description']
            correct_seo_alt = media_data.get('seo_alt_text') == data['seo_alt_text']
            
            # Verify tags are properly parsed
            expected_tags = ['safety', 'equipment', 'machinery', 'demonstration', 'training']
            actual_tags = media_data.get('tags', [])
            correct_tags = set(expected_tags) == set(actual_tags)
            
            # Verify additional fields
            has_upload_date = 'upload_date' in media_data
            has_file_size = 'file_size' in media_data and media_data['file_size'] > 0
            
            success = all([correct_category, correct_description, correct_seo_alt, 
                          correct_tags, has_upload_date, has_file_size])
            
            details = f"Category: {correct_category}, Description: {correct_description}, SEO Alt: {correct_seo_alt}, Tags: {correct_tags}, Upload Date: {has_upload_date}, File Size: {has_file_size}"
            self.log_test("Media Metadata Handling", success, details)
            return success
        else:
            self.log_test("Media Metadata Handling", False, 
                         f"Status: {response.status_code if response else 'No response'}")
            return False

    def run_all_tests(self):
        """Run all media upload tests"""
        print("🎬 Starting Media Upload Functionality Testing for PostVelocity")
        print("=" * 70)
        
        # Setup
        if not self.create_test_companies():
            print("❌ Failed to create test companies. Aborting tests.")
            return False
        
        # Core functionality tests
        self.test_media_categories_endpoint()
        self.test_media_upload_different_categories()
        self.test_company_media_retrieval()
        self.test_media_filtering_by_category()
        self.test_multi_company_media_isolation()
        self.test_file_upload_validation()
        self.test_media_metadata_handling()
        
        # Summary
        print("\n" + "=" * 70)
        print(f"📊 MEDIA UPLOAD TESTING SUMMARY")
        print(f"Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("🎉 ALL MEDIA UPLOAD TESTS PASSED!")
            return True
        else:
            print(f"⚠️  {self.tests_run - self.tests_passed} tests failed")
            return False

if __name__ == "__main__":
    tester = MediaUploadTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)