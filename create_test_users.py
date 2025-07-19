#!/usr/bin/env python3
"""
Create test users for Phase 2C API testing
"""

import asyncio
import motor.motor_asyncio
from datetime import datetime
from bson import ObjectId
import os

# Database connection
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/social_media_content")

async def create_test_users():
    """Create test users with different plan types"""
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
    db = client.social_media_content
    
    # Business plan user (should have API access)
    business_user = {
        "_id": ObjectId("507f1f77bcf86cd799439011"),
        "username": "business_api_user",
        "email": "business@apitest.com",
        "full_name": "Business API User",
        "role": "admin",
        "current_plan": "business",
        "subscription_status": "active",
        "created_at": datetime.utcnow(),
        "is_active": True
    }
    
    # Starter plan user (should NOT have API access)
    starter_user = {
        "_id": ObjectId("507f1f77bcf86cd799439012"),
        "username": "starter_api_user",
        "email": "starter@apitest.com",
        "full_name": "Starter API User",
        "role": "admin",
        "current_plan": "starter",
        "subscription_status": "active",
        "created_at": datetime.utcnow(),
        "is_active": True
    }
    
    try:
        # Insert or update business user
        await db.users.replace_one(
            {"_id": business_user["_id"]},
            business_user,
            upsert=True
        )
        print(f"✅ Business user created/updated: {business_user['_id']}")
        
        # Insert or update starter user
        await db.users.replace_one(
            {"_id": starter_user["_id"]},
            starter_user,
            upsert=True
        )
        print(f"✅ Starter user created/updated: {starter_user['_id']}")
        
        print("✅ Test users setup complete!")
        
    except Exception as e:
        print(f"❌ Error creating test users: {e}")
    
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(create_test_users())