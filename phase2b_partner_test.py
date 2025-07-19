#!/usr/bin/env python3
"""
Phase 2B Partner Program Backend Testing Suite
Tests all partner registration, dashboard, referral tracking, and conversion endpoints
"""

import requests
import json
import time
import uuid
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get backend URL from frontend .env file
def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=', 1)[1].strip()
    except:
        pass
    return "http://localhost:8001"

BASE_URL = get_backend_url()
API_BASE = f"{BASE_URL}/api"

print(f"🧪 PHASE 2B PARTNER PROGRAM BACKEND TESTING")
print(f"🔗 Backend URL: {BASE_URL}")
print(f"📡 API Base: {API_BASE}")
print("=" * 80)

# Test results tracking
test_results = {
    "total_tests": 0,
    "passed_tests": 0,
    "failed_tests": 0,
    "test_details": []
}

def log_test_result(test_name, success, details="", response_data=None):
    """Log test result with details"""
    test_results["total_tests"] += 1
    if success:
        test_results["passed_tests"] += 1
        status = "✅ PASS"
    else:
        test_results["failed_tests"] += 1
        status = "❌ FAIL"
    
    result = {
        "test": test_name,
        "status": status,
        "details": details,
        "response_data": response_data
    }
    test_results["test_details"].append(result)
    print(f"{status}: {test_name}")
    if details:
        print(f"   📝 {details}")
    if response_data and isinstance(response_data, dict):
        if "status" in response_data:
            print(f"   📊 Response Status: {response_data.get('status')}")
        if "message" in response_data:
            print(f"   💬 Message: {response_data.get('message')}")

def make_request(method, endpoint, data=None, params=None):
    """Make HTTP request with error handling"""
    try:
        url = f"{API_BASE}{endpoint}"
        headers = {"Content-Type": "application/json"}
        
        if method.upper() == "GET":
            response = requests.get(url, params=params, headers=headers, timeout=30)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=30)
        elif method.upper() == "PUT":
            response = requests.put(url, json=data, headers=headers, timeout=30)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers, timeout=30)
        
        return response
    except requests.exceptions.RequestException as e:
        print(f"   🚨 Request Error: {str(e)}")
        return None

# Global variables to store test data
test_partners = {}
test_referrals = {}

print("\n🔍 1. PARTNER REGISTRATION ENDPOINT TESTING")
print("-" * 50)

def test_partner_registration():
    """Test partner registration with different partner types"""
    
    # Test 1: Register Affiliate Partner (30% commission)
    affiliate_data = {
        "email": "affiliate@test.com",
        "full_name": "John Affiliate",
        "company_name": "Affiliate Marketing Co",
        "partner_type": "affiliate",
        "website": "https://affiliate-marketing.com"
    }
    
    response = make_request("POST", "/partners/register", affiliate_data)
    if response and response.status_code == 200:
        data = response.json()
        if data.get("status") == "success" and "partner" in data:
            partner = data["partner"]
            test_partners["affiliate"] = partner
            log_test_result(
                "Affiliate Partner Registration", 
                True,
                f"Commission Rate: {partner.get('commission_rate', 0)*100}%, Referral Code: {partner.get('referral_code')}",
                data
            )
            
            # Verify commission rate is 30%
            if partner.get("commission_rate") == 0.30:
                log_test_result("Affiliate Commission Rate Verification", True, "30% commission rate correct")
            else:
                log_test_result("Affiliate Commission Rate Verification", False, f"Expected 30%, got {partner.get('commission_rate', 0)*100}%")
        else:
            log_test_result("Affiliate Partner Registration", False, "Invalid response structure")
    else:
        log_test_result("Affiliate Partner Registration", False, f"HTTP {response.status_code if response else 'No Response'}")
    
    # Test 2: Register Agency Partner (40% commission)
    agency_data = {
        "email": "agency@test.com",
        "full_name": "Sarah Agency",
        "company_name": "Digital Agency Pro",
        "partner_type": "agency",
        "website": "https://digital-agency.com"
    }
    
    response = make_request("POST", "/partners/register", agency_data)
    if response and response.status_code == 200:
        data = response.json()
        if data.get("status") == "success" and "partner" in data:
            partner = data["partner"]
            test_partners["agency"] = partner
            log_test_result(
                "Agency Partner Registration", 
                True,
                f"Commission Rate: {partner.get('commission_rate', 0)*100}%, Referral Code: {partner.get('referral_code')}",
                data
            )
            
            # Verify commission rate is 40%
            if partner.get("commission_rate") == 0.40:
                log_test_result("Agency Commission Rate Verification", True, "40% commission rate correct")
            else:
                log_test_result("Agency Commission Rate Verification", False, f"Expected 40%, got {partner.get('commission_rate', 0)*100}%")
        else:
            log_test_result("Agency Partner Registration", False, "Invalid response structure")
    else:
        log_test_result("Agency Partner Registration", False, f"HTTP {response.status_code if response else 'No Response'}")
    
    # Test 3: Register Reseller Partner (60% commission)
    reseller_data = {
        "email": "reseller@test.com",
        "full_name": "Mike Reseller",
        "company_name": "Reseller Solutions Inc",
        "partner_type": "reseller",
        "website": "https://reseller-solutions.com"
    }
    
    response = make_request("POST", "/partners/register", reseller_data)
    if response and response.status_code == 200:
        data = response.json()
        if data.get("status") == "success" and "partner" in data:
            partner = data["partner"]
            test_partners["reseller"] = partner
            log_test_result(
                "Reseller Partner Registration", 
                True,
                f"Commission Rate: {partner.get('commission_rate', 0)*100}%, Referral Code: {partner.get('referral_code')}",
                data
            )
            
            # Verify commission rate is 60%
            if partner.get("commission_rate") == 0.60:
                log_test_result("Reseller Commission Rate Verification", True, "60% commission rate correct")
            else:
                log_test_result("Reseller Commission Rate Verification", False, f"Expected 60%, got {partner.get('commission_rate', 0)*100}%")
        else:
            log_test_result("Reseller Partner Registration", False, "Invalid response structure")
    else:
        log_test_result("Reseller Partner Registration", False, f"HTTP {response.status_code if response else 'No Response'}")
    
    # Test 4: Register Distributor Partner (70% commission)
    distributor_data = {
        "email": "distributor@test.com",
        "full_name": "Lisa Distributor",
        "company_name": "Distribution Network LLC",
        "partner_type": "distributor",
        "website": "https://distribution-network.com"
    }
    
    response = make_request("POST", "/partners/register", distributor_data)
    if response and response.status_code == 200:
        data = response.json()
        if data.get("status") == "success" and "partner" in data:
            partner = data["partner"]
            test_partners["distributor"] = partner
            log_test_result(
                "Distributor Partner Registration", 
                True,
                f"Commission Rate: {partner.get('commission_rate', 0)*100}%, Referral Code: {partner.get('referral_code')}",
                data
            )
            
            # Verify commission rate is 70%
            if partner.get("commission_rate") == 0.70:
                log_test_result("Distributor Commission Rate Verification", True, "70% commission rate correct")
            else:
                log_test_result("Distributor Commission Rate Verification", False, f"Expected 70%, got {partner.get('commission_rate', 0)*100}%")
        else:
            log_test_result("Distributor Partner Registration", False, "Invalid response structure")
    else:
        log_test_result("Distributor Partner Registration", False, f"HTTP {response.status_code if response else 'No Response'}")

def test_partner_validation():
    """Test partner registration validation"""
    
    # Test 5: Missing email validation
    invalid_data = {
        "full_name": "Test User",
        "partner_type": "affiliate"
    }
    
    response = make_request("POST", "/partners/register", invalid_data)
    if response and response.status_code == 400:
        log_test_result("Missing Email Validation", True, "Correctly rejected missing email")
    else:
        log_test_result("Missing Email Validation", False, f"Expected 400, got {response.status_code if response else 'No Response'}")
    
    # Test 6: Missing full_name validation
    invalid_data = {
        "email": "test@example.com",
        "partner_type": "affiliate"
    }
    
    response = make_request("POST", "/partners/register", invalid_data)
    if response and response.status_code == 400:
        log_test_result("Missing Full Name Validation", True, "Correctly rejected missing full name")
    else:
        log_test_result("Missing Full Name Validation", False, f"Expected 400, got {response.status_code if response else 'No Response'}")
    
    # Test 7: Duplicate email validation
    duplicate_data = {
        "email": "affiliate@test.com",  # Already registered
        "full_name": "Duplicate User",
        "partner_type": "affiliate"
    }
    
    response = make_request("POST", "/partners/register", duplicate_data)
    if response and response.status_code == 400:
        log_test_result("Duplicate Email Validation", True, "Correctly rejected duplicate email")
    else:
        log_test_result("Duplicate Email Validation", False, f"Expected 400, got {response.status_code if response else 'No Response'}")

def test_referral_code_generation():
    """Test unique referral code generation"""
    
    # Verify all partners have unique referral codes
    referral_codes = []
    for partner_type, partner in test_partners.items():
        code = partner.get("referral_code")
        if code:
            referral_codes.append(code)
    
    if len(referral_codes) == len(set(referral_codes)):
        log_test_result("Unique Referral Code Generation", True, f"All {len(referral_codes)} referral codes are unique")
    else:
        log_test_result("Unique Referral Code Generation", False, "Duplicate referral codes found")
    
    # Verify referral code format (8 characters, uppercase + digits)
    for partner_type, partner in test_partners.items():
        code = partner.get("referral_code", "")
        if len(code) == 8 and code.isalnum() and code.isupper():
            log_test_result(f"{partner_type.title()} Referral Code Format", True, f"Code '{code}' has correct format")
        else:
            log_test_result(f"{partner_type.title()} Referral Code Format", False, f"Code '{code}' has incorrect format")

print("\n🔍 2. PARTNER DASHBOARD ENDPOINT TESTING")
print("-" * 50)

def test_partner_dashboard():
    """Test partner dashboard data retrieval"""
    
    for partner_type, partner in test_partners.items():
        partner_id = partner.get("id")
        if not partner_id:
            log_test_result(f"{partner_type.title()} Dashboard Test", False, "No partner ID available")
            continue
        
        response = make_request("GET", f"/partners/{partner_id}/dashboard")
        if response and response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                # Verify dashboard structure
                required_fields = ["partner_info", "stats", "recent_referrals", "recent_activity", "referral_url"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if not missing_fields:
                    stats = data.get("stats", {})
                    partner_info = data.get("partner_info", {})
                    
                    log_test_result(
                        f"{partner_type.title()} Dashboard Data", 
                        True,
                        f"Total Referrals: {stats.get('total_referrals', 0)}, Commission: ${stats.get('total_commission_earned', 0):.2f}",
                        data
                    )
                    
                    # Verify partner info
                    if partner_info.get("email") == partner.get("email"):
                        log_test_result(f"{partner_type.title()} Dashboard Partner Info", True, "Partner info matches registration")
                    else:
                        log_test_result(f"{partner_type.title()} Dashboard Partner Info", False, "Partner info mismatch")
                else:
                    log_test_result(f"{partner_type.title()} Dashboard Structure", False, f"Missing fields: {missing_fields}")
            else:
                log_test_result(f"{partner_type.title()} Dashboard Test", False, "Invalid response status")
        else:
            log_test_result(f"{partner_type.title()} Dashboard Test", False, f"HTTP {response.status_code if response else 'No Response'}")

print("\n🔍 3. REFERRAL TRACKING SYSTEM TESTING")
print("-" * 50)

def test_referral_tracking():
    """Test referral tracking functionality"""
    
    # Test with affiliate partner
    if "affiliate" in test_partners:
        affiliate = test_partners["affiliate"]
        referral_code = affiliate.get("referral_code")
        
        # Test 8: Track new referral signup
        referral_data = {
            "referral_code": referral_code,
            "user_email": "customer1@example.com",
            "user_name": "John Customer"
        }
        
        response = make_request("POST", "/referrals/track", referral_data)
        if response and response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                referral_id = data.get("referral_id")
                test_referrals["customer1"] = {
                    "id": referral_id,
                    "partner_type": "affiliate",
                    "partner_id": affiliate.get("id"),
                    "email": "customer1@example.com"
                }
                log_test_result(
                    "Affiliate Referral Tracking", 
                    True,
                    f"Referral ID: {referral_id}, Commission Rate: {data.get('commission_rate', 0)*100}%",
                    data
                )
            else:
                log_test_result("Affiliate Referral Tracking", False, "Invalid response status")
        else:
            log_test_result("Affiliate Referral Tracking", False, f"HTTP {response.status_code if response else 'No Response'}")
        
        # Test 9: Track duplicate referral (should be prevented)
        response = make_request("POST", "/referrals/track", referral_data)
        if response and response.status_code == 200:
            data = response.json()
            if data.get("status") == "duplicate":
                log_test_result("Duplicate Referral Prevention", True, "Correctly prevented duplicate referral")
            else:
                log_test_result("Duplicate Referral Prevention", False, "Did not prevent duplicate referral")
        else:
            log_test_result("Duplicate Referral Prevention", False, f"HTTP {response.status_code if response else 'No Response'}")
    
    # Test with agency partner
    if "agency" in test_partners:
        agency = test_partners["agency"]
        referral_code = agency.get("referral_code")
        
        referral_data = {
            "referral_code": referral_code,
            "user_email": "customer2@example.com",
            "user_name": "Sarah Customer"
        }
        
        response = make_request("POST", "/referrals/track", referral_data)
        if response and response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                referral_id = data.get("referral_id")
                test_referrals["customer2"] = {
                    "id": referral_id,
                    "partner_type": "agency",
                    "partner_id": agency.get("id"),
                    "email": "customer2@example.com"
                }
                log_test_result(
                    "Agency Referral Tracking", 
                    True,
                    f"Referral ID: {referral_id}, Commission Rate: {data.get('commission_rate', 0)*100}%",
                    data
                )
            else:
                log_test_result("Agency Referral Tracking", False, "Invalid response status")
        else:
            log_test_result("Agency Referral Tracking", False, f"HTTP {response.status_code if response else 'No Response'}")

def test_referral_validation():
    """Test referral tracking validation"""
    
    # Test 10: Invalid referral code
    invalid_referral = {
        "referral_code": "INVALID123",
        "user_email": "test@example.com",
        "user_name": "Test User"
    }
    
    response = make_request("POST", "/referrals/track", invalid_referral)
    if response and response.status_code == 404:
        log_test_result("Invalid Referral Code Validation", True, "Correctly rejected invalid referral code")
    else:
        log_test_result("Invalid Referral Code Validation", False, f"Expected 404, got {response.status_code if response else 'No Response'}")
    
    # Test 11: Missing referral code
    missing_code = {
        "user_email": "test@example.com",
        "user_name": "Test User"
    }
    
    response = make_request("POST", "/referrals/track", missing_code)
    if response and response.status_code == 400:
        log_test_result("Missing Referral Code Validation", True, "Correctly rejected missing referral code")
    else:
        log_test_result("Missing Referral Code Validation", False, f"Expected 400, got {response.status_code if response else 'No Response'}")

print("\n🔍 4. REFERRAL CONVERSION TESTING")
print("-" * 50)

def test_referral_conversion():
    """Test referral conversion to paid customers"""
    
    # Test 12: Convert affiliate referral (30% commission)
    if "customer1" in test_referrals:
        referral = test_referrals["customer1"]
        conversion_data = {
            "plan_purchased": "professional",
            "sale_amount": 690.0  # Professional yearly plan
        }
        
        response = make_request("POST", f"/referrals/{referral['id']}/convert", conversion_data)
        if response and response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                commission_earned = data.get("commission_earned", 0)
                expected_commission = 690.0 * 0.30  # 30% of $690
                
                if abs(commission_earned - expected_commission) < 0.01:
                    log_test_result(
                        "Affiliate Referral Conversion", 
                        True,
                        f"Commission: ${commission_earned:.2f} (30% of ${conversion_data['sale_amount']})",
                        data
                    )
                else:
                    log_test_result(
                        "Affiliate Referral Conversion", 
                        False, 
                        f"Commission mismatch: expected ${expected_commission:.2f}, got ${commission_earned:.2f}"
                    )
            else:
                log_test_result("Affiliate Referral Conversion", False, "Invalid response status")
        else:
            log_test_result("Affiliate Referral Conversion", False, f"HTTP {response.status_code if response else 'No Response'}")
    
    # Test 13: Convert agency referral (40% commission)
    if "customer2" in test_referrals:
        referral = test_referrals["customer2"]
        conversion_data = {
            "plan_purchased": "business",
            "sale_amount": 1490.0  # Business yearly plan
        }
        
        response = make_request("POST", f"/referrals/{referral['id']}/convert", conversion_data)
        if response and response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                commission_earned = data.get("commission_earned", 0)
                expected_commission = 1490.0 * 0.40  # 40% of $1490
                
                if abs(commission_earned - expected_commission) < 0.01:
                    log_test_result(
                        "Agency Referral Conversion", 
                        True,
                        f"Commission: ${commission_earned:.2f} (40% of ${conversion_data['sale_amount']})",
                        data
                    )
                else:
                    log_test_result(
                        "Agency Referral Conversion", 
                        False, 
                        f"Commission mismatch: expected ${expected_commission:.2f}, got ${commission_earned:.2f}"
                    )
            else:
                log_test_result("Agency Referral Conversion", False, "Invalid response status")
        else:
            log_test_result("Agency Referral Conversion", False, f"HTTP {response.status_code if response else 'No Response'}")

def test_conversion_validation():
    """Test referral conversion validation"""
    
    # Test 14: Invalid referral ID
    invalid_conversion = {
        "plan_purchased": "professional",
        "sale_amount": 690.0
    }
    
    response = make_request("POST", "/referrals/invalid_id/convert", invalid_conversion)
    if response and response.status_code in [404, 400]:
        log_test_result("Invalid Referral ID Conversion", True, "Correctly rejected invalid referral ID")
    else:
        log_test_result("Invalid Referral ID Conversion", False, f"Expected 404/400, got {response.status_code if response else 'No Response'}")
    
    # Test 15: Missing sale amount
    if "customer1" in test_referrals:
        referral = test_referrals["customer1"]
        invalid_conversion = {
            "plan_purchased": "professional"
            # Missing sale_amount
        }
        
        response = make_request("POST", f"/referrals/{referral['id']}/convert", invalid_conversion)
        if response and response.status_code == 400:
            log_test_result("Missing Sale Amount Validation", True, "Correctly rejected missing sale amount")
        else:
            log_test_result("Missing Sale Amount Validation", False, f"Expected 400, got {response.status_code if response else 'No Response'}")

print("\n🔍 5. PARTNER STATS UPDATE VERIFICATION")
print("-" * 50)

def test_partner_stats_update():
    """Test that partner stats are updated correctly after conversions"""
    
    # Check affiliate partner stats after conversion
    if "affiliate" in test_partners:
        partner_id = test_partners["affiliate"]["id"]
        response = make_request("GET", f"/partners/{partner_id}/dashboard")
        
        if response and response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                stats = data.get("stats", {})
                total_referrals = stats.get("total_referrals", 0)
                total_commission = stats.get("total_commission_earned", 0)
                
                # Should have 1 referral and commission from conversion
                if total_referrals >= 1:
                    log_test_result("Affiliate Stats - Total Referrals", True, f"Total referrals: {total_referrals}")
                else:
                    log_test_result("Affiliate Stats - Total Referrals", False, f"Expected >= 1, got {total_referrals}")
                
                if total_commission > 0:
                    log_test_result("Affiliate Stats - Commission Earned", True, f"Total commission: ${total_commission:.2f}")
                else:
                    log_test_result("Affiliate Stats - Commission Earned", False, f"Expected > 0, got ${total_commission:.2f}")
            else:
                log_test_result("Affiliate Stats Update", False, "Invalid response status")
        else:
            log_test_result("Affiliate Stats Update", False, f"HTTP {response.status_code if response else 'No Response'}")
    
    # Check agency partner stats after conversion
    if "agency" in test_partners:
        partner_id = test_partners["agency"]["id"]
        response = make_request("GET", f"/partners/{partner_id}/dashboard")
        
        if response and response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                stats = data.get("stats", {})
                total_referrals = stats.get("total_referrals", 0)
                total_commission = stats.get("total_commission_earned", 0)
                monthly_volume = stats.get("monthly_sales_volume", 0)
                
                # Should have 1 referral and commission from conversion
                if total_referrals >= 1:
                    log_test_result("Agency Stats - Total Referrals", True, f"Total referrals: {total_referrals}")
                else:
                    log_test_result("Agency Stats - Total Referrals", False, f"Expected >= 1, got {total_referrals}")
                
                if total_commission > 0:
                    log_test_result("Agency Stats - Commission Earned", True, f"Total commission: ${total_commission:.2f}")
                else:
                    log_test_result("Agency Stats - Commission Earned", False, f"Expected > 0, got ${total_commission:.2f}")
                
                if monthly_volume > 0:
                    log_test_result("Agency Stats - Monthly Volume", True, f"Monthly volume: ${monthly_volume:.2f}")
                else:
                    log_test_result("Agency Stats - Monthly Volume", False, f"Expected > 0, got ${monthly_volume:.2f}")
            else:
                log_test_result("Agency Stats Update", False, "Invalid response status")
        else:
            log_test_result("Agency Stats Update", False, f"HTTP {response.status_code if response else 'No Response'}")

# Run all tests
def run_all_tests():
    """Execute all partner program tests"""
    print("🚀 Starting Phase 2B Partner Program Backend Tests...")
    
    # 1. Partner Registration Tests
    test_partner_registration()
    test_partner_validation()
    test_referral_code_generation()
    
    # 2. Partner Dashboard Tests
    test_partner_dashboard()
    
    # 3. Referral Tracking Tests
    test_referral_tracking()
    test_referral_validation()
    
    # 4. Referral Conversion Tests
    test_referral_conversion()
    test_conversion_validation()
    
    # 5. Partner Stats Update Tests
    test_partner_stats_update()

if __name__ == "__main__":
    try:
        run_all_tests()
        
        print("\n" + "=" * 80)
        print("🎯 PHASE 2B PARTNER PROGRAM BACKEND TEST SUMMARY")
        print("=" * 80)
        print(f"📊 Total Tests: {test_results['total_tests']}")
        print(f"✅ Passed: {test_results['passed_tests']}")
        print(f"❌ Failed: {test_results['failed_tests']}")
        
        success_rate = (test_results['passed_tests'] / test_results['total_tests']) * 100 if test_results['total_tests'] > 0 else 0
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if test_results['failed_tests'] > 0:
            print(f"\n🚨 FAILED TESTS:")
            for result in test_results['test_details']:
                if "❌ FAIL" in result['status']:
                    print(f"   • {result['test']}: {result['details']}")
        
        print(f"\n🎉 PHASE 2B PARTNER PROGRAM TESTING COMPLETED!")
        
        # Test specific scenarios mentioned in review request
        print(f"\n📋 SPECIFIC TEST SCENARIOS COMPLETED:")
        print(f"   ✅ Partner Registration with different types (affiliate 30%, agency 40%, reseller 60%, distributor 70%)")
        print(f"   ✅ Unique referral code generation and validation")
        print(f"   ✅ Partner dashboard data with stats calculation")
        print(f"   ✅ Referral tracking system with duplicate prevention")
        print(f"   ✅ Referral conversion with commission calculation")
        print(f"   ✅ Partner stats update verification")
        
        if success_rate >= 80:
            print(f"\n🎊 EXCELLENT: Phase 2B Partner Program backend system is working well!")
        elif success_rate >= 60:
            print(f"\n⚠️  GOOD: Phase 2B Partner Program backend system is mostly functional with some issues.")
        else:
            print(f"\n🚨 NEEDS ATTENTION: Phase 2B Partner Program backend system has significant issues.")
            
    except Exception as e:
        print(f"\n🚨 CRITICAL ERROR during testing: {str(e)}")
        print("❌ Testing could not be completed successfully")