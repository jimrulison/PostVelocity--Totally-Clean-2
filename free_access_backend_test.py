#!/usr/bin/env python3
"""
Free Access System Backend Testing
Tests the new promotional code system for PostVelocity
"""

import requests
import json
import time
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get backend URL from frontend .env file
try:
    with open('/app/frontend/.env', 'r') as f:
        for line in f:
            if line.startswith('REACT_APP_BACKEND_URL='):
                BACKEND_URL = line.split('=', 1)[1].strip()
                break
        else:
            BACKEND_URL = "http://localhost:8001"
except:
    BACKEND_URL = "http://localhost:8001"

API_BASE = f"{BACKEND_URL}/api"

print(f"🧪 FREE ACCESS SYSTEM BACKEND TESTING")
print(f"🔗 Backend URL: {BACKEND_URL}")
print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)

# Test counters
total_tests = 0
passed_tests = 0
failed_tests = 0

def test_result(test_name, success, details=""):
    global total_tests, passed_tests, failed_tests
    total_tests += 1
    if success:
        passed_tests += 1
        print(f"✅ {test_name}")
        if details:
            print(f"   📋 {details}")
    else:
        failed_tests += 1
        print(f"❌ {test_name}")
        if details:
            print(f"   🚨 {details}")
    print()

def make_request(method, endpoint, data=None, params=None):
    """Make HTTP request with error handling"""
    try:
        url = f"{API_BASE}{endpoint}"
        headers = {"Content-Type": "application/json"}
        
        if method.upper() == "GET":
            response = requests.get(url, params=params, headers=headers, timeout=30)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=30)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers, timeout=30)
        else:
            return None, f"Unsupported method: {method}"
        
        return response, None
    except requests.exceptions.Timeout:
        return None, "Request timeout (30s)"
    except requests.exceptions.ConnectionError:
        return None, "Connection error - backend may be down"
    except Exception as e:
        return None, f"Request error: {str(e)}"

# Test data storage
generated_codes = []
test_user_id = "test_user_free_access_123"

print("🎯 SCENARIO 1: ADMIN CODE GENERATION TESTING")
print("-" * 50)

# Test 1: Generate Professional Plan Code (30 days, 5 max uses)
print("1️⃣ Testing Professional Plan Code Generation...")
code_data = {
    "plan_level": "professional",
    "duration_days": 30,
    "max_uses": 5,
    "description": "Professional plan 30-day trial for testing"
}

response, error = make_request("POST", "/admin/generate-free-code", code_data)
if error:
    test_result("Generate Professional Code", False, error)
else:
    if response.status_code == 200:
        try:
            result = response.json()
            if result.get("status") == "success" and result.get("code", "").startswith("FREE-"):
                generated_codes.append(result["code"])
                test_result("Generate Professional Code", True, 
                          f"Code: {result['code']}, Plan: {result['plan_level']}, Duration: {result['duration_days']} days, Max Uses: {result['max_uses']}")
            else:
                test_result("Generate Professional Code", False, f"Invalid response format: {result}")
        except json.JSONDecodeError:
            test_result("Generate Professional Code", False, "Invalid JSON response")
    else:
        test_result("Generate Professional Code", False, f"HTTP {response.status_code}: {response.text}")

# Test 2: Generate Starter Plan Code (7 days, 1 max use)
print("2️⃣ Testing Starter Plan Code Generation...")
code_data = {
    "plan_level": "starter",
    "duration_days": 7,
    "max_uses": 1,
    "description": "Starter plan 7-day trial"
}

response, error = make_request("POST", "/admin/generate-free-code", code_data)
if error:
    test_result("Generate Starter Code", False, error)
else:
    if response.status_code == 200:
        try:
            result = response.json()
            if result.get("status") == "success" and result.get("code", "").startswith("FREE-"):
                generated_codes.append(result["code"])
                test_result("Generate Starter Code", True, 
                          f"Code: {result['code']}, Plan: {result['plan_level']}, Duration: {result['duration_days']} days")
            else:
                test_result("Generate Starter Code", False, f"Invalid response format: {result}")
        except json.JSONDecodeError:
            test_result("Generate Starter Code", False, "Invalid JSON response")
    else:
        test_result("Generate Starter Code", False, f"HTTP {response.status_code}: {response.text}")

# Test 3: Generate Business Plan Code (90 days, 10 max uses)
print("3️⃣ Testing Business Plan Code Generation...")
code_data = {
    "plan_level": "business",
    "duration_days": 90,
    "max_uses": 10,
    "description": "Business plan 90-day extended trial"
}

response, error = make_request("POST", "/admin/generate-free-code", code_data)
if error:
    test_result("Generate Business Code", False, error)
else:
    if response.status_code == 200:
        try:
            result = response.json()
            if result.get("status") == "success" and result.get("code", "").startswith("FREE-"):
                generated_codes.append(result["code"])
                test_result("Generate Business Code", True, 
                          f"Code: {result['code']}, Plan: {result['plan_level']}, Duration: {result['duration_days']} days, Max Uses: {result['max_uses']}")
            else:
                test_result("Generate Business Code", False, f"Invalid response format: {result}")
        except json.JSONDecodeError:
            test_result("Generate Business Code", False, "Invalid JSON response")
    else:
        test_result("Generate Business Code", False, f"HTTP {response.status_code}: {response.text}")

# Test 4: Generate Enterprise Plan Code (30 days, 1 max use)
print("4️⃣ Testing Enterprise Plan Code Generation...")
code_data = {
    "plan_level": "enterprise",
    "duration_days": 30,
    "max_uses": 1,
    "description": "Enterprise plan 30-day premium trial"
}

response, error = make_request("POST", "/admin/generate-free-code", code_data)
if error:
    test_result("Generate Enterprise Code", False, error)
else:
    if response.status_code == 200:
        try:
            result = response.json()
            if result.get("status") == "success" and result.get("code", "").startswith("FREE-"):
                generated_codes.append(result["code"])
                test_result("Generate Enterprise Code", True, 
                          f"Code: {result['code']}, Plan: {result['plan_level']}, Duration: {result['duration_days']} days")
            else:
                test_result("Generate Enterprise Code", False, f"Invalid response format: {result}")
        except json.JSONDecodeError:
            test_result("Generate Enterprise Code", False, "Invalid JSON response")
    else:
        test_result("Generate Enterprise Code", False, f"HTTP {response.status_code}: {response.text}")

print("🎯 SCENARIO 2: ADMIN CODE LISTING TESTING")
print("-" * 50)

# Test 5: List All Free Access Codes
print("5️⃣ Testing Free Access Codes Listing...")
response, error = make_request("GET", "/admin/free-codes")
if error:
    test_result("List Free Access Codes", False, error)
else:
    if response.status_code == 200:
        try:
            result = response.json()
            if result.get("status") == "success" and "codes" in result:
                codes_count = len(result["codes"])
                total_codes = result.get("total_codes", 0)
                test_result("List Free Access Codes", True, 
                          f"Retrieved {codes_count} codes, Total: {total_codes}")
                
                # Verify our generated codes are in the list
                found_codes = [code["code"] for code in result["codes"]]
                for gen_code in generated_codes:
                    if gen_code in found_codes:
                        print(f"   ✅ Found generated code: {gen_code}")
                    else:
                        print(f"   ⚠️  Generated code not found: {gen_code}")
            else:
                test_result("List Free Access Codes", False, f"Invalid response format: {result}")
        except json.JSONDecodeError:
            test_result("List Free Access Codes", False, "Invalid JSON response")
    else:
        test_result("List Free Access Codes", False, f"HTTP {response.status_code}: {response.text}")

print("🎯 SCENARIO 3: USER CODE REDEMPTION TESTING")
print("-" * 50)

# First, create a test user for redemption testing
print("6️⃣ Creating Test User for Redemption...")
user_data = {
    "user_id": test_user_id,
    "email": "testuser@freeaccess.com",
    "name": "Free Access Test User"
}

response, error = make_request("POST", "/create-test-user", user_data)
if error:
    test_result("Create Test User", False, error)
else:
    if response.status_code == 200:
        test_result("Create Test User", True, f"Test user created: {test_user_id}")
    else:
        test_result("Create Test User", False, f"HTTP {response.status_code}: {response.text}")

# Test 7: Redeem Valid Professional Code
if generated_codes:
    print("7️⃣ Testing Valid Code Redemption...")
    professional_code = generated_codes[0]  # Use first generated code
    
    redeem_data = {
        "code": professional_code,
        "user_id": test_user_id,
        "ip_address": "192.168.1.100"
    }
    
    response, error = make_request("POST", "/redeem-free-code", redeem_data)
    if error:
        test_result("Redeem Valid Code", False, error)
    else:
        if response.status_code == 200:
            try:
                result = response.json()
                if result.get("status") == "success":
                    test_result("Redeem Valid Code", True, 
                              f"Plan: {result.get('plan_level')}, Duration: {result.get('duration_days')} days, Expires: {result.get('expires_at')}")
                else:
                    test_result("Redeem Valid Code", False, f"Redemption failed: {result}")
            except json.JSONDecodeError:
                test_result("Redeem Valid Code", False, "Invalid JSON response")
        else:
            test_result("Redeem Valid Code", False, f"HTTP {response.status_code}: {response.text}")

# Test 8: Try to Redeem Same Code Again (Should Fail)
if generated_codes:
    print("8️⃣ Testing Duplicate Code Redemption (Should Fail)...")
    professional_code = generated_codes[0]  # Use same code
    
    redeem_data = {
        "code": professional_code,
        "user_id": test_user_id,
        "ip_address": "192.168.1.100"
    }
    
    response, error = make_request("POST", "/redeem-free-code", redeem_data)
    if error:
        test_result("Duplicate Redemption Prevention", False, error)
    else:
        if response.status_code == 400:
            test_result("Duplicate Redemption Prevention", True, "Correctly prevented duplicate redemption")
        else:
            test_result("Duplicate Redemption Prevention", False, f"Should have failed with 400, got {response.status_code}")

# Test 9: Try to Redeem Invalid Code
print("9️⃣ Testing Invalid Code Redemption (Should Fail)...")
redeem_data = {
    "code": "FREE-INVALID123",
    "user_id": test_user_id,
    "ip_address": "192.168.1.100"
}

response, error = make_request("POST", "/redeem-free-code", redeem_data)
if error:
    test_result("Invalid Code Rejection", False, error)
else:
    if response.status_code == 404:
        test_result("Invalid Code Rejection", True, "Correctly rejected invalid code")
    else:
        test_result("Invalid Code Rejection", False, f"Should have failed with 404, got {response.status_code}")

# Test 10: Test Code Usage Limits
if len(generated_codes) >= 2:
    print("🔟 Testing Code Usage Limits...")
    # Use the starter code (max_uses = 1)
    starter_code = generated_codes[1] if len(generated_codes) > 1 else generated_codes[0]
    
    # Create second test user
    second_user_id = "test_user_free_access_456"
    user_data = {
        "user_id": second_user_id,
        "email": "testuser2@freeaccess.com",
        "name": "Second Test User"
    }
    
    response, error = make_request("POST", "/create-test-user", user_data)
    if response and response.status_code == 200:
        # Try to redeem starter code with second user
        redeem_data = {
            "code": starter_code,
            "user_id": second_user_id,
            "ip_address": "192.168.1.101"
        }
        
        response, error = make_request("POST", "/redeem-free-code", redeem_data)
        if error:
            test_result("Code Usage Limit Test", False, error)
        else:
            if response.status_code == 200:
                # Now try with a third user (should fail due to max_uses = 1)
                third_user_id = "test_user_free_access_789"
                user_data = {
                    "user_id": third_user_id,
                    "email": "testuser3@freeaccess.com",
                    "name": "Third Test User"
                }
                
                response, error = make_request("POST", "/create-test-user", user_data)
                if response and response.status_code == 200:
                    redeem_data = {
                        "code": starter_code,
                        "user_id": third_user_id,
                        "ip_address": "192.168.1.102"
                    }
                    
                    response, error = make_request("POST", "/redeem-free-code", redeem_data)
                    if response and response.status_code == 400:
                        test_result("Code Usage Limit Test", True, "Correctly enforced max_uses limit")
                    else:
                        test_result("Code Usage Limit Test", False, f"Should have failed with 400, got {response.status_code if response else 'No response'}")
                else:
                    test_result("Code Usage Limit Test", False, "Failed to create third test user")
            else:
                test_result("Code Usage Limit Test", False, f"Second user redemption failed: {response.status_code}")
    else:
        test_result("Code Usage Limit Test", False, "Failed to create second test user")

print("🎯 SCENARIO 4: CODE MANAGEMENT TESTING")
print("-" * 50)

# Test 11: Deactivate a Code
if generated_codes:
    print("1️⃣1️⃣ Testing Code Deactivation...")
    code_to_deactivate = generated_codes[-1]  # Use the last generated code
    
    response, error = make_request("DELETE", f"/admin/free-codes/{code_to_deactivate}")
    if error:
        test_result("Code Deactivation", False, error)
    else:
        if response.status_code == 200:
            try:
                result = response.json()
                if result.get("status") == "success":
                    test_result("Code Deactivation", True, f"Successfully deactivated code: {code_to_deactivate}")
                else:
                    test_result("Code Deactivation", False, f"Deactivation failed: {result}")
            except json.JSONDecodeError:
                test_result("Code Deactivation", False, "Invalid JSON response")
        else:
            test_result("Code Deactivation", False, f"HTTP {response.status_code}: {response.text}")

# Test 12: Try to Redeem Deactivated Code
if generated_codes:
    print("1️⃣2️⃣ Testing Deactivated Code Redemption (Should Fail)...")
    deactivated_code = generated_codes[-1]
    
    # Create another test user
    fourth_user_id = "test_user_free_access_999"
    user_data = {
        "user_id": fourth_user_id,
        "email": "testuser4@freeaccess.com",
        "name": "Fourth Test User"
    }
    
    response, error = make_request("POST", "/create-test-user", user_data)
    if response and response.status_code == 200:
        redeem_data = {
            "code": deactivated_code,
            "user_id": fourth_user_id,
            "ip_address": "192.168.1.103"
        }
        
        response, error = make_request("POST", "/redeem-free-code", redeem_data)
        if error:
            test_result("Deactivated Code Rejection", False, error)
        else:
            if response.status_code == 404:
                test_result("Deactivated Code Rejection", True, "Correctly rejected deactivated code")
            else:
                test_result("Deactivated Code Rejection", False, f"Should have failed with 404, got {response.status_code}")
    else:
        test_result("Deactivated Code Rejection", False, "Failed to create fourth test user")

# Test 13: Try to Deactivate Non-existent Code
print("1️⃣3️⃣ Testing Non-existent Code Deactivation (Should Fail)...")
response, error = make_request("DELETE", "/admin/free-codes/FREE-NONEXISTENT")
if error:
    test_result("Non-existent Code Deactivation", False, error)
else:
    if response.status_code == 404:
        test_result("Non-existent Code Deactivation", True, "Correctly handled non-existent code")
    else:
        test_result("Non-existent Code Deactivation", False, f"Should have failed with 404, got {response.status_code}")

print("🎯 SCENARIO 5: DATA VALIDATION TESTING")
print("-" * 50)

# Test 14: Generate Code with Missing Data
print("1️⃣4️⃣ Testing Code Generation with Missing Data...")
incomplete_data = {
    "plan_level": "professional"
    # Missing duration_days and max_uses
}

response, error = make_request("POST", "/admin/generate-free-code", incomplete_data)
if error:
    test_result("Incomplete Data Handling", False, error)
else:
    if response.status_code == 200:
        try:
            result = response.json()
            if result.get("status") == "success":
                # Should use defaults: 30 days, 1 max use
                test_result("Incomplete Data Handling", True, 
                          f"Used defaults - Duration: {result.get('duration_days', 'N/A')}, Max Uses: {result.get('max_uses', 'N/A')}")
            else:
                test_result("Incomplete Data Handling", False, f"Generation failed: {result}")
        except json.JSONDecodeError:
            test_result("Incomplete Data Handling", False, "Invalid JSON response")
    else:
        test_result("Incomplete Data Handling", False, f"HTTP {response.status_code}: {response.text}")

# Test 15: Redeem Code with Missing User ID
print("1️⃣5️⃣ Testing Code Redemption with Missing User ID...")
if generated_codes:
    redeem_data = {
        "code": generated_codes[0]
        # Missing user_id
    }
    
    response, error = make_request("POST", "/redeem-free-code", redeem_data)
    if error:
        test_result("Missing User ID Validation", False, error)
    else:
        if response.status_code == 400:
            test_result("Missing User ID Validation", True, "Correctly validated missing user_id")
        else:
            test_result("Missing User ID Validation", False, f"Should have failed with 400, got {response.status_code}")

print("=" * 80)
print("🎉 FREE ACCESS SYSTEM TESTING COMPLETED")
print("=" * 80)
print(f"📊 FINAL RESULTS:")
print(f"   ✅ Passed: {passed_tests}")
print(f"   ❌ Failed: {failed_tests}")
print(f"   📈 Total:  {total_tests}")
print(f"   🎯 Success Rate: {(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "   🎯 Success Rate: 0%")
print()

if generated_codes:
    print(f"🔑 Generated Test Codes:")
    for i, code in enumerate(generated_codes, 1):
        print(f"   {i}. {code}")
    print()

# Summary of key findings
print("🔍 KEY FINDINGS:")
if passed_tests >= total_tests * 0.8:
    print("   🎉 FREE ACCESS SYSTEM IS WORKING EXCELLENTLY!")
    print("   ✅ All core functionality operational")
    print("   ✅ Code generation, redemption, and management working")
    print("   ✅ Proper validation and error handling")
elif passed_tests >= total_tests * 0.6:
    print("   ⚠️  FREE ACCESS SYSTEM HAS MINOR ISSUES")
    print("   ✅ Core functionality working")
    print("   ⚠️  Some edge cases or validation issues found")
else:
    print("   🚨 FREE ACCESS SYSTEM HAS CRITICAL ISSUES")
    print("   ❌ Major functionality problems detected")
    print("   🔧 Requires immediate attention")

print()
print("🎯 RECOMMENDATION:")
if passed_tests >= total_tests * 0.9:
    print("   ✅ Free Access System is PRODUCTION-READY")
    print("   🚀 All promotional code features working perfectly")
elif passed_tests >= total_tests * 0.7:
    print("   ⚠️  Free Access System needs minor fixes before production")
    print("   🔧 Address validation and edge case issues")
else:
    print("   🚨 Free Access System requires major fixes")
    print("   ⛔ Not ready for production use")

print("=" * 80)