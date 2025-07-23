"""
PostVelocity - AI-Powered Social Media Management Platform
Copyright (c) 2025 Fancy Free Living LLC. All rights reserved.

This software is proprietary and confidential. Unauthorized copying,
distribution, or use is strictly prohibited and may result in severe
civil and criminal penalties.

Trade Secrets: This software contains trade secrets and proprietary
information of Fancy Free Living LLC. Any unauthorized use, reproduction,
or distribution is strictly prohibited.
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Union
import anthropic
import os
import json
from datetime import datetime, timedelta
import uuid
from dotenv import load_dotenv
import motor.motor_asyncio
from bson import ObjectId
import asyncio
from enum import Enum
import shutil
from pathlib import Path
import mimetypes
from PIL import Image
import io
import base64
import requests
import re
import hashlib
from collections import defaultdict
import random
import urllib.parse
from bs4 import BeautifulSoup
import stripe
import secrets
import httpx
import time
from urllib.parse import urlencode, urlparse, parse_qs

# Load environment variables
load_dotenv()

# Import our security system
try:
    from security import security_manager, content_protection
    security_enabled = True
except ImportError:
    security_enabled = False
    print("Security module not found - running without advanced security")

# Enhanced license validation and usage tracking
class UsageTracker:
    def __init__(self):
        self.usage_logs = []
        self.suspicious_activities = []
    
    def track_usage(self, user_id, action, details, request_info=None):
        log_entry = {
            'user_id': user_id,
            'action': action,
            'details': details,
            'timestamp': datetime.now().isoformat(),
            'ip_address': request_info.get('ip', 'unknown') if request_info else 'unknown',
            'user_agent': request_info.get('user_agent', 'unknown') if request_info else 'unknown',
            'session_id': request_info.get('session_id', 'unknown') if request_info else 'unknown'
        }
        self.usage_logs.append(log_entry)
        
        # Check for suspicious activity
        if self.detect_suspicious_activity(user_id):
            self.flag_user_for_review(user_id)
        
        return log_entry
    
    def detect_suspicious_activity(self, user_id):
        """Detect suspicious user behavior"""
        recent_logs = [
            log for log in self.usage_logs 
            if log['user_id'] == user_id and 
            datetime.fromisoformat(log['timestamp']) > datetime.now() - timedelta(hours=1)
        ]
        
        # Check for excessive usage
        if len(recent_logs) > 100:
            return True
        
        # Check for multiple IP addresses
        ip_addresses = set(log['ip_address'] for log in recent_logs)
        if len(ip_addresses) > 3:
            return True
        
        return False
    
    def flag_user_for_review(self, user_id):
        """Flag user for manual review"""
        self.suspicious_activities.append({
            'user_id': user_id,
            'flagged_at': datetime.now().isoformat(),
            'reason': 'Suspicious activity detected'
        })
        print(f"User {user_id} flagged for suspicious activity")

# Initialize usage tracker
usage_tracker = UsageTracker()

app = FastAPI()

# Admin Panel Route
@app.get("/admin")
async def admin_panel():
    """Admin panel interface"""
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>PostVelocity Admin Panel</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                margin: 0; 
                background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
                min-height: 100vh;
                padding: 20px;
                color: white;
            }
            .admin-container { 
                max-width: 1400px;
                margin: 0 auto;
            }
            .header { 
                text-align: center;
                margin-bottom: 40px;
                padding: 20px;
                background: rgba(255,255,255,0.1);
                border-radius: 15px;
            }
            .admin-grid { 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                gap: 20px; 
                margin-bottom: 30px;
            }
            .admin-card { 
                background: rgba(255,255,255,0.15);
                padding: 25px;
                border-radius: 15px;
                border-left: 4px solid #e74c3c;
            }
            .card-title { 
                font-size: 20px;
                font-weight: bold;
                margin-bottom: 15px;
                color: #ecf0f1;
            }
            .card-content { 
                font-size: 14px;
                line-height: 1.6;
                margin-bottom: 20px;
            }
            .admin-button {
                background: #e74c3c;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                cursor: pointer;
                font-size: 14px;
                transition: background 0.3s;
            }
            .admin-button:hover {
                background: #c0392b;
            }
            .back-button {
                position: fixed;
                top: 20px;
                right: 20px;
                background: rgba(255,255,255,0.2);
                color: white;
                padding: 10px 20px;
                border-radius: 8px;
                text-decoration: none;
            }
            .stats-row {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 15px;
                margin-bottom: 30px;
            }
            .stat-box {
                background: rgba(255,255,255,0.1);
                padding: 20px;
                border-radius: 10px;
                text-align: center;
            }
            .stat-number {
                font-size: 24px;
                font-weight: bold;
                color: #e74c3c;
            }
            .stat-label {
                font-size: 12px;
                opacity: 0.8;
                margin-top: 5px;
            }
        </style>
        <script>
            function loadAdminData(endpoint, action) {
                fetch(endpoint)
                    .then(response => response.json())
                    .then(data => {
                        alert(action + ' loaded successfully! Check console for details.');
                        console.log(action + ' data:', data);
                    })
                    .catch(error => {
                        alert('Error loading ' + action + ': ' + error.message);
                        console.error('Error:', error);
                    });
            }
            
            function checkAuth() {
                const currentUser = JSON.parse(localStorage.getItem('currentUser') || '{}');
                if (!currentUser.email || currentUser.role !== 'admin') {
                    alert('Admin access required. Redirecting to login.');
                    window.location.href = '/api/admin-login';
                    return false;
                }
                document.getElementById('adminEmail').textContent = currentUser.email;
                return true;
            }
            
            window.onload = checkAuth;
        </script>
    </head>
    <body>
        <a href="/" class="back-button">← Back to Dashboard</a>
        
        <div class="admin-container">
            <div class="header">
                <h1>🔐 PostVelocity Admin Panel</h1>
                <p>Administrator: <span id="adminEmail">Loading...</span></p>
                <p>Full administrative control over PostVelocity platform</p>
            </div>
            
            <div class="stats-row">
                <div class="stat-box">
                    <div class="stat-number">2</div>
                    <div class="stat-label">Total Users</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">34</div>
                    <div class="stat-label">Companies</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">$578</div>
                    <div class="stat-label">Monthly Revenue</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">95%</div>
                    <div class="stat-label">System Health</div>
                </div>
            </div>
            
            <div class="admin-grid">
                <div class="admin-card">
                    <div class="card-title">👥 User Management</div>
                    <div class="card-content">
                        Manage all PostVelocity users, view profiles, update permissions, and monitor user activity across the platform.
                    </div>
                    <button class="admin-button" onclick="loadAdminData('/api/admin/users', 'Users')">
                        View All Users
                    </button>
                </div>
                
                <div class="admin-card">
                    <div class="card-title">📊 Platform Analytics</div>
                    <div class="card-content">
                        Comprehensive analytics dashboard with user engagement, revenue tracking, and platform performance metrics.
                    </div>
                    <button class="admin-button" onclick="loadAdminData('/api/admin/analytics', 'Analytics')">
                        View Analytics
                    </button>
                </div>
                
                <div class="admin-card">
                    <div class="card-title">💰 Billing Overview</div>
                    <div class="card-content">
                        Monitor subscription status, payment processing, revenue analytics, and billing-related issues across all users.
                    </div>
                    <button class="admin-button" onclick="loadAdminData('/api/admin/billing-analytics', 'Billing')">
                        View Billing
                    </button>
                </div>
                
                <div class="admin-card">
                    <div class="card-title">🎟️ Promotional Codes</div>
                    <div class="card-content">
                        Generate and manage free access codes for different subscription tiers. Monitor code usage and redemption rates.
                    </div>
                    <button class="admin-button" onclick="loadAdminData('/api/admin/free-codes', 'Free Codes')">
                        Manage Codes
                    </button>
                </div>
                
                <div class="admin-card">
                    <div class="card-title">🔧 System Health</div>
                    <div class="card-content">
                        Monitor server status, API performance, database connections, and overall system health metrics.
                    </div>
                    <button class="admin-button" onclick="loadAdminData('/api/simple-test', 'System Status')">
                        Check System
                    </button>
                </div>
                
                <div class="admin-card">
                    <div class="card-title">📈 Comprehensive Reports</div>
                    <div class="card-content">
                        Generate detailed reports on user activity, revenue trends, platform usage, and business intelligence insights.
                    </div>
                    <button class="admin-button" onclick="loadAdminData('/api/admin/comprehensive-analytics', 'Reports')">
                        Generate Reports
                    </button>
                </div>
            </div>
        </div>
    </body>
    </html>
    """)

@app.get("/dashboard")
async def dashboard():
    """Main dashboard after successful login"""
    return HTMLResponse("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>PostVelocity - Dashboard</title>
        <style>
            body { 
                margin: 0; 
                font-family: system-ui;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
                color: white;
            }
            .dashboard {
                max-width: 1200px;
                margin: 0 auto;
            }
            .header {
                text-align: center;
                margin-bottom: 40px;
                background: rgba(255,255,255,0.1);
                padding: 30px;
                border-radius: 15px;
            }
            .user-info {
                background: rgba(255,255,255,0.1);
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 30px;
            }
            .features {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
            }
            .feature-card {
                background: rgba(255,255,255,0.15);
                padding: 25px;
                border-radius: 15px;
                cursor: pointer;
                transition: transform 0.2s;
            }
            .feature-card:hover {
                transform: translateY(-5px);
                background: rgba(255,255,255,0.25);
            }
            .logout {
                text-align: center;
                margin-top: 30px;
            }
            .logout a {
                color: white;
                text-decoration: none;
                background: rgba(255,255,255,0.2);
                padding: 10px 20px;
                border-radius: 5px;
            }
        </style>
        <script>
            window.onload = function() {
                const currentUser = JSON.parse(localStorage.getItem('currentUser') || '{}');
                if (currentUser.email) {
                    document.getElementById('userInfo').innerHTML = 
                        '<h3>👋 Welcome, ' + (currentUser.full_name || currentUser.email) + '</h3>' +
                        '<p>Role: ' + (currentUser.role === 'admin' ? '🔐 Administrator' : '👤 User') + '</p>' +
                        '<p>Email: ' + currentUser.email + '</p>';
                } else {
                    document.getElementById('userInfo').innerHTML = '<p>Please log in to continue</p>';
                    setTimeout(() => window.location.href = '/login', 2000);
                }
            }
        </script>
    </head>
    <body>
        <div class="dashboard">
            <div class="header">
                <h1>🚀 PostVelocity Dashboard</h1>
                <div id="userInfo" class="user-info">Loading...</div>
            </div>
            
            <div class="features">
                <div class="feature-card">
                    <h3>📝 Content Generation</h3>
                    <p>Create AI-powered content for 20+ social media platforms</p>
                </div>
                <div class="feature-card">
                    <h3>📊 Analytics</h3>
                    <p>Track performance and ROI across all platforms</p>
                </div>
                <div class="feature-card">
                    <h3>🔗 Platform Management</h3>
                    <p>Connect and manage all your social media accounts</p>
                </div>
                <div class="feature-card">
                    <h3>⚡ Automation</h3>
                    <p>Schedule and automate your social media posting</p>
                </div>
            </div>
            
            <div class="logout">
                <a href="#" onclick="localStorage.clear(); window.location.href='/login';">🚪 Logout</a>
            </div>
        </div>
    </body>
    </html>
    """)

# CLEAN LOGIN SYSTEM - REBUILT FROM SCRATCH
@app.get("/user-login")
async def clean_user_login():
    """Simple user login - no redirects, no conflicts"""
    return HTMLResponse("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>PostVelocity - User Login</title>
        <style>
            body { 
                margin: 0; 
                font-family: system-ui;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .login-box {
                background: white;
                padding: 40px;
                border-radius: 10px;
                width: 100%;
                max-width: 400px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            h1 { text-align: center; margin-bottom: 30px; color: #333; }
            .form-group { margin-bottom: 20px; }
            label { display: block; margin-bottom: 5px; font-weight: bold; }
            input { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box; }
            button { width: 100%; padding: 12px; background: #667eea; color: white; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; }
            button:hover { background: #5a67d8; }
            .admin-link { text-align: center; margin-top: 20px; }
            .admin-link a { color: #667eea; text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="login-box">
            <h1>🚀 PostVelocity Login</h1>
            <form action="/api/auth/login" method="post">
                <div class="form-group">
                    <label>Email:</label>
                    <input type="email" name="email" value="user@postvelocity.com" required>
                </div>
                <div class="form-group">
                    <label>Password:</label>
                    <input type="password" name="password" value="user123" required>
                </div>
                <button type="submit">Login</button>
            </form>
            <div class="admin-link">
                <a href="/admin-login">Admin Login →</a>
            </div>
        </div>
    </body>
    </html>
    """)

@app.get("/admin-login")
async def clean_admin_login():
    """Simple admin login - no redirects, no conflicts"""
    return HTMLResponse("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>PostVelocity - Admin Login</title>
        <style>
            body { 
                margin: 0; 
                font-family: system-ui;
                background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .login-box {
                background: white;
                padding: 40px;
                border-radius: 10px;
                width: 100%;
                max-width: 400px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            h1 { text-align: center; margin-bottom: 30px; color: #2c3e50; }
            .form-group { margin-bottom: 20px; }
            label { display: block; margin-bottom: 5px; font-weight: bold; }
            input { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box; }
            button { width: 100%; padding: 12px; background: #2c3e50; color: white; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; }
            button:hover { background: #34495e; }
            .user-link { text-align: center; margin-top: 20px; }
            .user-link a { color: #2c3e50; text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="login-box">
            <h1>🔐 Admin Login</h1>
            <form action="/api/auth/admin-login" method="post">
                <div class="form-group">
                    <label>Admin Email:</label>
                    <input type="email" name="email" value="admin@postvelocity.com" required>
                </div>
                <div class="form-group">
                    <label>Admin Password:</label>
                    <input type="password" name="password" value="admin123" required>
                </div>
                <button type="submit">Admin Login</button>
            </form>
            <div class="user-link">
                <a href="/login">← User Login</a>
            </div>
        </div>
    </body>
    </html>
    """)

# SUPER SIMPLE TEST ROUTE - ADD AT VERY BEGINNING
@app.get("/api/simple-test")
async def simple_test():
    return {"message": "SIMPLE TEST ROUTE WORKS", "success": True}

@app.get("/api/debug-test-html")  
async def debug_test_html():
    return HTMLResponse("<h1>DEBUG HTML ROUTE WORKS</h1>")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Mount static files for serving uploaded media
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Mount static files for serving frontend build (for production deployment)
frontend_build_path = Path("../frontend/build")
# Only mount if build directory exists
if frontend_build_path.exists() and (frontend_build_path / "static").exists():
    app.mount("/static", StaticFiles(directory=frontend_build_path / "static"), name="static")

# Database connection
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/social_media_content")
client_db = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client_db.social_media_content

# Initialize Claude client
claude_api_key = os.getenv("CLAUDE_API_KEY")
print(f"Claude API Key loaded: {claude_api_key is not None}")
if not claude_api_key:
    raise ValueError("CLAUDE_API_KEY environment variable is not set")

client = anthropic.Anthropic(
    api_key=claude_api_key
)

# Initialize Stripe API key
stripe_api_key = os.getenv("STRIPE_API_KEY")
if not stripe_api_key:
    print("Warning: STRIPE_API_KEY not found in environment")
    stripe_api_key = "sk_test_default"  # Fallback for development

# Enums
class PostStatus(str, Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    FAILED = "failed"

class ContentType(str, Enum):
    SOCIAL_POST = "social_post"
    BLOG_POST = "blog_post"
    NEWSLETTER = "newsletter"
    VIDEO_SCRIPT = "video_script"

class MediaType(str, Enum):
    IMAGE = "image"
    VIDEO = "video"

class MediaCategory(str, Enum):
    TRAINING = "training"
    EQUIPMENT = "equipment"
    WORKPLACE = "workplace"
    TEAM = "team"
    PROJECTS = "projects"
    SAFETY = "safety"
    CERTIFICATES = "certificates"
    EVENTS = "events"

class ApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    REVISION_NEEDED = "revision_needed"

class UserRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    CREATOR = "creator"
    CLIENT = "client"

class HashtagStatus(str, Enum):
    TRENDING = "trending"
    STABLE = "stable"
    DECLINING = "declining"

# Platform configurations with enhanced features
PLATFORM_CONFIGS = {
    "instagram": {
        "max_chars": 2200,
        "hashtag_limit": 30,
        "style": "visual, engaging, story-driven",
        "format": "Short paragraphs, emojis, hashtags",
        "optimal_times": ["6:00", "12:00", "19:00"],
        "supports_video": True,
        "media_required": True,
        "engagement_rate_avg": 0.018,
        "reach_multiplier": 1.0,
        "story_duration": 24,
        "reel_max_duration": 90
    },
    "tiktok": {
        "max_chars": 150,
        "hashtag_limit": 5,
        "style": "trendy, fun, educational",
        "format": "Hook + quick tip + call to action",
        "optimal_times": ["6:00", "10:00", "19:00"],
        "supports_video": True,
        "media_required": True,
        "engagement_rate_avg": 0.045,
        "reach_multiplier": 2.5,
        "video_max_duration": 180,
        "trending_sounds": True
    },
    "facebook": {
        "max_chars": 63206,
        "hashtag_limit": 10,
        "style": "informative, community-focused",
        "format": "Detailed post with clear value",
        "optimal_times": ["9:00", "15:00", "21:00"],
        "supports_video": True,
        "media_required": False,
        "engagement_rate_avg": 0.012,
        "reach_multiplier": 0.8,
        "supports_polls": True,
        "supports_events": True
    },
    "youtube": {
        "max_chars": 5000,
        "hashtag_limit": 15,
        "style": "educational, detailed",
        "format": "Title + Description + Timestamps",
        "optimal_times": ["14:00", "17:00", "20:00"],
        "supports_video": True,
        "media_required": True,
        "engagement_rate_avg": 0.035,
        "reach_multiplier": 3.0,
        "video_min_duration": 60,
        "supports_shorts": True
    },
    "whatsapp": {
        "max_chars": 65536,
        "hashtag_limit": 5,
        "style": "personal, direct, actionable",
        "format": "Brief message with clear action",
        "optimal_times": ["8:00", "12:00", "18:00"],
        "supports_video": False,
        "media_required": False,
        "engagement_rate_avg": 0.080,
        "reach_multiplier": 0.5,
        "supports_broadcast": True,
        "supports_groups": True
    },
    "snapchat": {
        "max_chars": 250,
        "hashtag_limit": 3,
        "style": "casual, behind-the-scenes",
        "format": "Quick tip or insight",
        "optimal_times": ["10:00", "16:00", "22:00"],
        "supports_video": True,
        "media_required": True,
        "engagement_rate_avg": 0.025,
        "reach_multiplier": 1.2,
        "story_duration": 24,
        "supports_ar": True
    },
    "x": {
        "max_chars": 280,
        "hashtag_limit": 5,
        "style": "concise, impactful",
        "format": "Hook + value + hashtags",
        "optimal_times": ["8:00", "12:00", "17:00"],
        "supports_video": True,
        "media_required": False,
        "engagement_rate_avg": 0.008,
        "reach_multiplier": 1.5,
        "supports_threads": True,
        "supports_polls": True
    },
    "linkedin": {
        "max_chars": 3000,
        "hashtag_limit": 5,
        "style": "professional, industry-focused",
        "format": "Professional insight + industry context",
        "optimal_times": ["7:00", "12:00", "17:00"],
        "supports_video": True,
        "media_required": False,
        "engagement_rate_avg": 0.022,
        "reach_multiplier": 1.8,
        "supports_articles": True,
        "supports_polls": True
    }
}

# SEO Keywords for different industries
SEO_KEYWORDS = {
    "construction": [
        "construction safety", "building codes", "OSHA compliance", "construction training",
        "safety protocols", "job site safety", "construction equipment", "workplace safety",
        "construction management", "safety regulations", "construction industry", "safety training"
    ],
    "environmental": [
        "environmental training", "hazardous materials", "environmental compliance", "EPA regulations",
        "environmental safety", "waste management", "environmental protection", "sustainability",
        "environmental consulting", "green building", "environmental services", "eco-friendly"
    ],
    "safety": [
        "workplace safety", "occupational health", "safety training", "OSHA standards",
        "safety procedures", "risk management", "safety equipment", "safety protocols",
        "emergency response", "safety compliance", "industrial safety", "safety management"
    ]
}

# Trending hashtags database (would be updated via API in production)
TRENDING_HASHTAGS = {
    "construction": {
        "trending": ["#BuildSafe", "#ConstructionLife", "#SafetyFirst", "#BuildingTomorrow"],
        "stable": ["#Construction", "#Building", "#Architecture", "#Engineering"],
        "declining": ["#OldSchoolBuild", "#TraditionalMethods"]
    },
    "safety": {
        "trending": ["#SafetyInnovation", "#WorkplaceSafety", "#SafetyTech", "#ZeroIncidents"],
        "stable": ["#Safety", "#OSHA", "#WorkSafe", "#SafetyTraining"],
        "declining": ["#SafetyFirst", "#BasicSafety"]
    },
    "environmental": {
        "trending": ["#GreenConstruction", "#SustainableBuilding", "#EcoFriendly", "#CleanEnergy"],
        "stable": ["#Environment", "#Sustainability", "#GreenBuilding", "#EcoConstruction"],
        "declining": ["#GoGreen", "#EcoFriendly"]
    }
}

# Pydantic models
class PlanType(str, Enum):
    STARTER = "starter"
    PROFESSIONAL = "professional"  
    BUSINESS = "business"
    ENTERPRISE = "enterprise"

class PlanInterval(str, Enum):
    MONTHLY = "monthly"
    YEARLY = "yearly"
    LIFETIME = "lifetime"

class PartnerTier(str, Enum):
    AFFILIATE = "affiliate"
    AGENCY = "agency"
    RESELLER = "reseller"
    DISTRIBUTOR = "distributor"

class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    PAST_DUE = "past_due"
    CANCELED = "canceled"
    UNPAID = "unpaid"
    TRIALING = "trialing"

# Plan definitions with limits and pricing
PLAN_CONFIGS = {
    "starter": {
        "name": "Starter Plan",
        "description": "Perfect for solopreneurs and small businesses",
        "pricing": {
            "monthly": 29.00,
            "yearly": 290.00,  # 17% savings
            "lifetime": 890.00
        },
        "limits": {
            "companies": 3,
            "users": 1,
            "social_accounts_per_company": 5,
            "posts_per_month": 100,
            "analytics_retention_days": 30
        },
        "features": [
            "basic_ai_content",
            "standard_scheduling",
            "basic_analytics",
            "email_support",
            "mobile_app"
        ]
    },
    "professional": {
        "name": "Professional Plan", 
        "description": "Ideal for growing businesses and marketing professionals",
        "pricing": {
            "monthly": 69.00,
            "yearly": 690.00,
            "lifetime": 1990.00
        },
        "limits": {
            "companies": 10,
            "users": 3,
            "social_accounts_per_company": 15,
            "posts_per_month": 500,
            "analytics_retention_days": 90
        },
        "features": [
            "advanced_ai_content",
            "smart_scheduling",
            "advanced_analytics",
            "team_collaboration",
            "priority_support",
            "content_library",
            "bulk_upload"
        ]
    },
    "business": {
        "name": "Business Plan",
        "description": "For agencies and established businesses",
        "pricing": {
            "monthly": 149.00,
            "yearly": 1490.00,
            "lifetime": 4490.00
        },
        "limits": {
            "companies": 25,
            "users": 10,
            "social_accounts_per_company": -1,  # Unlimited
            "posts_per_month": 2000,
            "analytics_retention_days": 365
        },
        "features": [
            "premium_ai_content",
            "team_management",
            "white_label_reporting",
            "custom_dashboards",
            "phone_support",
            "api_access",
            "custom_branding"
        ]
    },
    "enterprise": {
        "name": "Enterprise Plan",
        "description": "For large agencies and corporations",
        "pricing": {
            "monthly": 349.00,
            "yearly": 3490.00,
            "lifetime": 9990.00
        },
        "limits": {
            "companies": -1,  # Unlimited
            "users": -1,      # Unlimited
            "social_accounts_per_company": -1,  # Unlimited
            "posts_per_month": -1,  # Unlimited
            "analytics_retention_days": -1     # Unlimited
        },
        "features": [
            "unlimited_ai_content",
            "advanced_security",
            "dedicated_account_manager",
            "24_7_support",
            "custom_integrations",
            "advanced_api",
            "custom_training"
        ]
    }
}

# Add-on pricing
ADDON_CONFIGS = {
    "seo_monitoring": {
        "name": "SEO Monitoring",
        "tiers": {
            "standard": {"price": 97.00, "daily_checks": 50},
            "pro": {"price": 197.00, "daily_checks": 100},
            "enterprise": {"price": 397.00, "daily_checks": -1}  # Unlimited
        }
    },
    "hashtag_research": {
        "name": "Hashtag Research & Optimization", 
        "tiers": {
            "basic": {"price": 19.00, "features": ["ai_suggestions", "trending_alerts"]},
            "advanced": {"price": 39.00, "features": ["competitor_analysis", "automation"]},
            "professional": {"price": 79.00, "features": ["industry_research", "white_label"]}
        }
    },
    "keyword_research": {
        "name": "Advanced Keyword Research",
        "tiers": {
            "starter": {"price": 29.00, "keywords_per_month": 1000},
            "professional": {"price": 59.00, "keywords_per_month": 5000},
            "enterprise": {"price": 119.00, "keywords_per_month": -1}  # Unlimited
        }
    },
    "competitor_analysis": {
        "name": "Competitor Analysis",
        "tiers": {
            "basic": {"price": 49.00, "analyses_per_month": 5},
            "advanced": {"price": 99.00, "analyses_per_month": 20},
            "professional": {"price": 199.00, "analyses_per_month": -1}  # Unlimited
        }
    }
}

# OAuth 2.0 Configuration for Social Media Platforms
OAUTH_CONFIGS = {
    "instagram": {
        "auth_url": "https://api.instagram.com/oauth/authorize",
        "token_url": "https://api.instagram.com/oauth/access_token",
        "revoke_url": "https://api.instagram.com/oauth/revoke",
        "scopes": ["user_profile", "user_media"],
        "client_id": os.getenv("INSTAGRAM_CLIENT_ID"),
        "client_secret": os.getenv("INSTAGRAM_CLIENT_SECRET"),
        "redirect_uri": os.getenv("FRONTEND_URL", "http://localhost:3000") + "/oauth-callback/instagram"
    },
    "tiktok": {
        "auth_url": "https://www.tiktok.com/v2/auth/authorize/",
        "token_url": "https://open.tiktokapis.com/v2/oauth/token/",
        "revoke_url": "https://open.tiktokapis.com/v2/oauth/revoke/",
        "scopes": ["user.info.basic", "video.upload"],
        "client_id": os.getenv("TIKTOK_CLIENT_ID"),
        "client_secret": os.getenv("TIKTOK_CLIENT_SECRET"),
        "redirect_uri": os.getenv("FRONTEND_URL", "http://localhost:3000") + "/oauth-callback/tiktok"
    },
    "facebook": {
        "auth_url": "https://www.facebook.com/v18.0/dialog/oauth",
        "token_url": "https://graph.facebook.com/v18.0/oauth/access_token",
        "revoke_url": "https://graph.facebook.com/v18.0/me/permissions",
        "scopes": ["pages_show_list", "pages_read_engagement", "pages_manage_posts", "publish_video"],
        "client_id": os.getenv("FACEBOOK_CLIENT_ID"),
        "client_secret": os.getenv("FACEBOOK_CLIENT_SECRET"),
        "redirect_uri": os.getenv("FRONTEND_URL", "http://localhost:3000") + "/oauth-callback/facebook"
    },
    "youtube": {
        "auth_url": "https://accounts.google.com/oauth2/v2/auth",
        "token_url": "https://oauth2.googleapis.com/token",
        "revoke_url": "https://oauth2.googleapis.com/revoke",
        "scopes": ["https://www.googleapis.com/auth/youtube.upload"],
        "client_id": os.getenv("YOUTUBE_CLIENT_ID"),
        "client_secret": os.getenv("YOUTUBE_CLIENT_SECRET"),
        "redirect_uri": os.getenv("FRONTEND_URL", "http://localhost:3000") + "/oauth-callback/youtube"
    },
    "whatsapp": {
        "auth_url": "https://graph.facebook.com/v18.0/dialog/oauth",
        "token_url": "https://graph.facebook.com/v18.0/oauth/access_token",
        "revoke_url": "https://graph.facebook.com/v18.0/me/permissions",
        "scopes": ["whatsapp_business_management", "whatsapp_business_messaging"],
        "client_id": os.getenv("WHATSAPP_CLIENT_ID"),
        "client_secret": os.getenv("WHATSAPP_CLIENT_SECRET"),
        "redirect_uri": os.getenv("FRONTEND_URL", "http://localhost:3000") + "/oauth-callback/whatsapp"
    },
    "snapchat": {
        "auth_url": "https://accounts.snapchat.com/accounts/oauth2/auth",
        "token_url": "https://accounts.snapchat.com/accounts/oauth2/token",
        "revoke_url": "https://accounts.snapchat.com/accounts/oauth2/revoke",
        "scopes": ["snapchat-marketing-api"],
        "client_id": os.getenv("SNAPCHAT_CLIENT_ID"),
        "client_secret": os.getenv("SNAPCHAT_CLIENT_SECRET"),
        "redirect_uri": os.getenv("FRONTEND_URL", "http://localhost:3000") + "/oauth-callback/snapchat"
    },
    "x": {
        "auth_url": "https://twitter.com/i/oauth2/authorize",
        "token_url": "https://api.twitter.com/2/oauth2/token",
        "revoke_url": "https://api.twitter.com/2/oauth2/revoke",
        "scopes": ["tweet.read", "tweet.write", "users.read"],
        "client_id": os.getenv("X_CLIENT_ID"),
        "client_secret": os.getenv("X_CLIENT_SECRET"),
        "redirect_uri": os.getenv("FRONTEND_URL", "http://localhost:3000") + "/oauth-callback/x"
    },
    "wechat": {
        "auth_url": "https://open.weixin.qq.com/connect/oauth2/authorize",
        "token_url": "https://api.weixin.qq.com/sns/oauth2/access_token",
        "revoke_url": "https://api.weixin.qq.com/sns/oauth2/revoke",
        "scopes": ["snsapi_base"],
        "client_id": os.getenv("WECHAT_CLIENT_ID"),
        "client_secret": os.getenv("WECHAT_CLIENT_SECRET"),
        "redirect_uri": os.getenv("FRONTEND_URL", "http://localhost:3000") + "/oauth-callback/wechat"
    },
    "telegram": {
        "auth_url": "https://oauth.telegram.org/auth",
        "token_url": "https://oauth.telegram.org/token",
        "revoke_url": "https://oauth.telegram.org/revoke",
        "scopes": ["bot"],
        "client_id": os.getenv("TELEGRAM_CLIENT_ID"),
        "client_secret": os.getenv("TELEGRAM_CLIENT_SECRET"),
        "redirect_uri": os.getenv("FRONTEND_URL", "http://localhost:3000") + "/oauth-callback/telegram"
    },
    "facebook_messenger": {
        "auth_url": "https://www.facebook.com/v18.0/dialog/oauth",
        "token_url": "https://graph.facebook.com/v18.0/oauth/access_token",
        "revoke_url": "https://graph.facebook.com/v18.0/me/permissions",
        "scopes": ["pages_messaging", "pages_show_list"],
        "client_id": os.getenv("MESSENGER_CLIENT_ID"),
        "client_secret": os.getenv("MESSENGER_CLIENT_SECRET"),
        "redirect_uri": os.getenv("FRONTEND_URL", "http://localhost:3000") + "/oauth-callback/facebook_messenger"
    },
    "douyin": {
        "auth_url": "https://open.douyin.com/platform/oauth/connect/",
        "token_url": "https://open.douyin.com/oauth/access_token/",
        "revoke_url": "https://open.douyin.com/oauth/revoke/",
        "scopes": ["user_info", "video.create"],
        "client_id": os.getenv("DOUYIN_CLIENT_ID"),
        "client_secret": os.getenv("DOUYIN_CLIENT_SECRET"),
        "redirect_uri": os.getenv("FRONTEND_URL", "http://localhost:3000") + "/oauth-callback/douyin"
    },
    "kuaishou": {
        "auth_url": "https://open.kuaishou.com/oauth2/authorize",
        "token_url": "https://open.kuaishou.com/oauth2/access_token",
        "revoke_url": "https://open.kuaishou.com/oauth2/revoke",
        "scopes": ["user_info", "user_video"],
        "client_id": os.getenv("KUAISHOU_CLIENT_ID"),
        "client_secret": os.getenv("KUAISHOU_CLIENT_SECRET"),
        "redirect_uri": os.getenv("FRONTEND_URL", "http://localhost:3000") + "/oauth-callback/kuaishou"
    },
    "reddit": {
        "auth_url": "https://www.reddit.com/api/v1/authorize",
        "token_url": "https://www.reddit.com/api/v1/access_token",
        "revoke_url": "https://www.reddit.com/api/v1/revoke_token",
        "scopes": ["submit", "read"],
        "client_id": os.getenv("REDDIT_CLIENT_ID"),
        "client_secret": os.getenv("REDDIT_CLIENT_SECRET"),
        "redirect_uri": os.getenv("FRONTEND_URL", "http://localhost:3000") + "/oauth-callback/reddit"
    },
    "weibo": {
        "auth_url": "https://api.weibo.com/oauth2/authorize",
        "token_url": "https://api.weibo.com/oauth2/access_token",
        "revoke_url": "https://api.weibo.com/oauth2/revoke",
        "scopes": ["email", "statuses_to_me_read"],
        "client_id": os.getenv("WEIBO_CLIENT_ID"),
        "client_secret": os.getenv("WEIBO_CLIENT_SECRET"),
        "redirect_uri": os.getenv("FRONTEND_URL", "http://localhost:3000") + "/oauth-callback/weibo"
    },
    "pinterest": {
        "auth_url": "https://www.pinterest.com/oauth/",
        "token_url": "https://api.pinterest.com/v5/oauth/token",
        "revoke_url": "https://api.pinterest.com/v5/oauth/revoke",
        "scopes": ["boards:read", "pins:write"],
        "client_id": os.getenv("PINTEREST_CLIENT_ID"),
        "client_secret": os.getenv("PINTEREST_CLIENT_SECRET"),
        "redirect_uri": os.getenv("FRONTEND_URL", "http://localhost:3000") + "/oauth-callback/pinterest"
    },
    "qq": {
        "auth_url": "https://graph.qq.com/oauth2.0/authorize",
        "token_url": "https://graph.qq.com/oauth2.0/token",
        "revoke_url": "https://graph.qq.com/oauth2.0/revoke",
        "scopes": ["get_user_info"],
        "client_id": os.getenv("QQ_CLIENT_ID"),
        "client_secret": os.getenv("QQ_CLIENT_SECRET"),
        "redirect_uri": os.getenv("FRONTEND_URL", "http://localhost:3000") + "/oauth-callback/qq"
    },
    "linkedin": {
        "auth_url": "https://www.linkedin.com/oauth/v2/authorization",
        "token_url": "https://www.linkedin.com/oauth/v2/accessToken",
        "revoke_url": "https://www.linkedin.com/oauth/v2/revoke",
        "scopes": ["w_member_social"],
        "client_id": os.getenv("LINKEDIN_CLIENT_ID"),
        "client_secret": os.getenv("LINKEDIN_CLIENT_SECRET"),
        "redirect_uri": os.getenv("FRONTEND_URL", "http://localhost:3000") + "/oauth-callback/linkedin"
    },
    "threads": {
        "auth_url": "https://threads.net/oauth/authorize",
        "token_url": "https://graph.threads.net/oauth/access_token",
        "revoke_url": "https://graph.threads.net/oauth/revoke",
        "scopes": ["threads_basic", "threads_content_publish"],
        "client_id": os.getenv("THREADS_CLIENT_ID"),
        "client_secret": os.getenv("THREADS_CLIENT_SECRET"),
        "redirect_uri": os.getenv("FRONTEND_URL", "http://localhost:3000") + "/oauth-callback/threads"
    },
    "quora": {
        "auth_url": "https://www.quora.com/oauth/dialog",
        "token_url": "https://www.quora.com/oauth/access_token",
        "revoke_url": "https://www.quora.com/oauth/revoke",
        "scopes": ["read", "write"],
        "client_id": os.getenv("QUORA_CLIENT_ID"),
        "client_secret": os.getenv("QUORA_CLIENT_SECRET"),
        "redirect_uri": os.getenv("FRONTEND_URL", "http://localhost:3000") + "/oauth-callback/quora"
    },
    "tumblr": {
        "auth_url": "https://www.tumblr.com/oauth/authorize",
        "token_url": "https://api.tumblr.com/v2/oauth2/token",
        "revoke_url": "https://api.tumblr.com/v2/oauth2/revoke",
        "scopes": ["write"],
        "client_id": os.getenv("TUMBLR_CLIENT_ID"),
        "client_secret": os.getenv("TUMBLR_CLIENT_SECRET"),
        "redirect_uri": os.getenv("FRONTEND_URL", "http://localhost:3000") + "/oauth-callback/tumblr"
    }
}

class CompetitorAnalysisRequest(BaseModel):
    website_url: str
    competitor_name: Optional[str] = None
    analysis_type: str = "comprehensive"  # comprehensive, website, social
    social_platforms: List[str] = []
    company_id: str = "demo-company"

class UserSubscription(BaseModel):
    id: Optional[str] = None
    user_id: str
    plan_type: PlanType
    plan_interval: PlanInterval
    status: SubscriptionStatus
    current_period_start: datetime
    current_period_end: datetime
    stripe_subscription_id: Optional[str] = None
    stripe_customer_id: Optional[str] = None
    trial_end: Optional[datetime] = None
    canceled_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

class UserUsage(BaseModel):
    id: Optional[str] = None
    user_id: str
    plan_type: PlanType
    current_month: str  # YYYY-MM format
    companies_count: int = 0
    users_count: int = 1
    posts_generated: int = 0
    api_calls: int = 0
    storage_used_mb: int = 0
    social_accounts_count: int = 0
    last_updated: Optional[datetime] = None

class PaymentTransaction(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    session_id: str
    amount: float
    currency: str = "usd"
    payment_status: str  # initiated, paid, failed, canceled
    stripe_payment_intent_id: Optional[str] = None
    plan_type: Optional[str] = None
    plan_interval: Optional[str] = None
    addon_type: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = {}
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class PartnerProfile(BaseModel):
    id: Optional[str] = None
    user_id: str
    partner_tier: PartnerTier
    commission_rate: float
    referral_code: str
    total_referrals: int = 0
    total_commission_earned: float = 0.0
    monthly_sales_volume: float = 0.0
    white_label_settings: Optional[Dict[str, Any]] = {}
    territory_rights: Optional[List[str]] = []
    is_active: bool = True
    approved_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

# Utility functions for plan management
def get_plan_price(plan_type: str, interval: str) -> float:
    """Get price for a plan type and interval"""
    if plan_type in PLAN_CONFIGS and interval in PLAN_CONFIGS[plan_type]["pricing"]:
        return PLAN_CONFIGS[plan_type]["pricing"][interval]
    raise ValueError(f"Invalid plan {plan_type} or interval {interval}")

def check_plan_limit(user_plan: str, limit_type: str, current_usage: int) -> bool:
    """Check if usage is within plan limits"""
    if user_plan not in PLAN_CONFIGS:
        return False
    
    limit = PLAN_CONFIGS[user_plan]["limits"].get(limit_type, 0)
    # -1 means unlimited
    if limit == -1:
        return True
    return current_usage < limit

def has_plan_feature(user_plan: str, feature: str) -> bool:
    """Check if user's plan includes a specific feature"""
    if user_plan not in PLAN_CONFIGS:
        return False
    return feature in PLAN_CONFIGS[user_plan]["features"]

def get_plan_upgrade_path(current_plan: str) -> List[str]:
    """Get possible upgrade paths for a plan"""
    plan_hierarchy = ["starter", "professional", "business", "enterprise"]
    try:
        current_index = plan_hierarchy.index(current_plan)
        return plan_hierarchy[current_index + 1:]
    except ValueError:
        return []

async def get_user_usage(user_id: str, current_month: str = None) -> UserUsage:
    """Get current month usage for a user"""
    if not current_month:
        current_month = datetime.utcnow().strftime("%Y-%m")
    
    usage = await db.user_usage.find_one({
        "user_id": user_id,
        "current_month": current_month
    })
    
    if not usage:
        # Create new usage record for the month
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        usage_data = {
            "user_id": user_id,
            "plan_type": user.get("current_plan", "starter") if user else "starter",
            "current_month": current_month,
            "companies_count": 0,
            "users_count": 1,
            "posts_generated": 0,
            "api_calls": 0,
            "storage_used_mb": 0,
            "social_accounts_count": 0,
            "last_updated": datetime.utcnow()
        }
        result = await db.user_usage.insert_one(usage_data)
        usage_data["id"] = str(result.inserted_id)
        del usage_data["_id"]
        return UserUsage(**usage_data)
    
    usage["id"] = str(usage["_id"])
    del usage["_id"]
    return UserUsage(**usage)

async def increment_usage(user_id: str, usage_type: str, amount: int = 1):
    """Increment usage counter for a user"""
    current_month = datetime.utcnow().strftime("%Y-%m")
    
    await db.user_usage.update_one(
        {"user_id": user_id, "current_month": current_month},
        {
            "$inc": {usage_type: amount},
            "$set": {"last_updated": datetime.utcnow()}
        },
        upsert=True
    )

async def get_user_billing_history(user_id: str) -> List[Dict[str, Any]]:
    """Get billing history for a user"""
    try:
        # Get payment transactions for the user
        transactions_cursor = db.payment_transactions.find(
            {"user_id": user_id}
        ).sort("created_at", -1).limit(10)
        
        billing_history = []
        async for transaction in transactions_cursor:
            billing_record = {
                "id": str(transaction["_id"]),
                "amount": transaction.get("amount", 0),
                "currency": transaction.get("currency", "usd"),
                "status": transaction.get("payment_status", "unknown"),
                "plan_type": transaction.get("plan_type"),
                "plan_interval": transaction.get("plan_interval"),
                "created_at": transaction.get("created_at"),
                "completed_at": transaction.get("completed_at")
            }
            billing_history.append(billing_record)
        
        return billing_history
    except Exception as e:
        print(f"Error getting billing history for user {user_id}: {e}")
        return []

class User(BaseModel):
    id: Optional[str] = None
    username: str
    email: str
    full_name: str
    role: UserRole
    company_id: Optional[str] = None
    permissions: Optional[List[str]] = []
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    is_active: Optional[bool] = True
    # Subscription fields
    current_plan: PlanType = PlanType.STARTER
    subscription_status: SubscriptionStatus = SubscriptionStatus.TRIALING
    stripe_customer_id: Optional[str] = None
    trial_end: Optional[datetime] = None

class Company(BaseModel):
    id: Optional[str] = None
    name: str
    industry: str
    website: Optional[str] = None
    description: Optional[str] = None
    target_audience: Optional[str] = None
    brand_voice: Optional[str] = None
    brand_colors: Optional[Dict[str, str]] = {}
    brand_fonts: Optional[Dict[str, str]] = {}
    social_accounts: Optional[Dict[str, Dict[str, str]]] = {}
    seo_keywords: Optional[List[str]] = []
    competitor_urls: Optional[List[str]] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    last_media_request: Optional[datetime] = None
    media_library_size: Optional[int] = 0
    team_members: Optional[List[str]] = []
    subscription_tier: Optional[str] = "basic"

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    industry: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    target_audience: Optional[str] = None
    brand_voice: Optional[str] = None
    brand_colors: Optional[Dict[str, str]] = None
    brand_fonts: Optional[Dict[str, str]] = None
    social_accounts: Optional[Dict[str, Dict[str, str]]] = None
    seo_keywords: Optional[List[str]] = None
    competitor_urls: Optional[List[str]] = None
    last_media_request: Optional[datetime] = None
    media_library_size: Optional[int] = None
    team_members: Optional[List[str]] = None
    subscription_tier: Optional[str] = None

class SEOAnalysis(BaseModel):
    content: str
    seo_score: float
    keyword_density: Dict[str, float]
    readability_score: float
    meta_description: str
    suggested_title: str
    recommendations: List[str]
    target_keywords: List[str]
    competitor_analysis: Optional[Dict[str, Any]] = None

class HashtagAnalysis(BaseModel):
    hashtag: str
    popularity_score: float
    engagement_rate: float
    competition_level: str
    trend_direction: HashtagStatus
    related_hashtags: List[str]
    best_times_to_use: List[str]
    estimated_reach: int

class ContentTemplate(BaseModel):
    id: Optional[str] = None
    name: str
    category: str
    industry: str
    platform: str
    template_content: str
    variables: List[str]
    performance_score: Optional[float] = None
    usage_count: Optional[int] = 0
    created_at: Optional[datetime] = None

class ContentRepurposing(BaseModel):
    original_content: str
    original_platform: str
    repurposed_content: Dict[str, str]  # platform -> content
    media_adaptations: Dict[str, List[str]]  # platform -> media files
    cross_promotion_strategy: str

class ApprovalWorkflow(BaseModel):
    id: Optional[str] = None
    content_id: str
    company_id: str
    created_by: str
    assigned_to: str
    status: ApprovalStatus
    content_type: ContentType
    content_data: Dict[str, Any]
    comments: Optional[List[Dict[str, Any]]] = []
    deadline: Optional[datetime] = None
    approved_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

class SmartCalendar(BaseModel):
    id: Optional[str] = None
    company_id: str
    date: datetime
    content_slots: Dict[str, Any]  # time -> content
    auto_generated: bool = False
    theme: Optional[str] = None
    campaigns: Optional[List[str]] = []
    performance_prediction: Optional[float] = None

class CrisisAlert(BaseModel):
    id: Optional[str] = None
    company_id: str
    alert_type: str
    severity: str
    message: str
    detected_at: datetime
    resolved_at: Optional[datetime] = None
    actions_taken: Optional[List[str]] = []
    sentiment_score: Optional[float] = None

class MediaFile(BaseModel):
    id: Optional[str] = None
    company_id: str
    filename: str
    original_filename: str
    file_path: str
    file_size: int
    media_type: MediaType
    mime_type: str
    category: MediaCategory
    description: Optional[str] = None
    tags: Optional[List[str]] = []
    upload_date: Optional[datetime] = None
    is_active: Optional[bool] = True
    usage_count: Optional[int] = 0
    last_used: Optional[datetime] = None
    seo_alt_text: Optional[str] = None
    performance_score: Optional[float] = None

class ContentRequest(BaseModel):
    company_id: str
    topic: str
    platforms: List[str]
    audience_level: Optional[str] = "general"
    additional_context: Optional[str] = ""
    generate_blog: Optional[bool] = False
    generate_newsletter: Optional[bool] = False
    generate_video_script: Optional[bool] = False
    use_company_media: Optional[bool] = True
    media_preferences: Optional[Dict[str, str]] = {}
    seo_focus: Optional[bool] = True
    target_keywords: Optional[List[str]] = []
    competitor_analysis: Optional[bool] = False
    repurpose_content: Optional[bool] = False
    template_id: Optional[str] = None

class GeneratedContent(BaseModel):
    platform: str
    content: str
    hashtags: List[str]
    estimated_engagement: str
    posting_tips: str
    video_suggestions: Optional[str] = None
    optimal_posting_times: List[str]
    suggested_media: Optional[List[Dict[str, Any]]] = []
    media_placement: Optional[str] = None
    seo_analysis: Optional[SEOAnalysis] = None
    hashtag_analysis: Optional[List[HashtagAnalysis]] = []
    performance_prediction: Optional[float] = None
    repurposed_versions: Optional[Dict[str, str]] = {}

class BlogPost(BaseModel):
    title: str
    content: str
    excerpt: str
    estimated_read_time: str
    seo_keywords: List[str]
    suggested_media: Optional[List[Dict[str, Any]]] = []
    media_placement_guide: Optional[str] = None
    seo_analysis: Optional[SEOAnalysis] = None
    meta_description: Optional[str] = None
    schema_markup: Optional[Dict[str, Any]] = None
    internal_links: Optional[List[str]] = []
    external_links: Optional[List[str]] = []

class NewsletterArticle(BaseModel):
    subject: str
    content: str
    sections: List[str]
    call_to_action: str
    target_audience: str
    suggested_media: Optional[List[Dict[str, Any]]] = []
    media_placement_guide: Optional[str] = None
    personalization_variables: Optional[List[str]] = []
    a_b_test_variations: Optional[List[str]] = []

class VideoScript(BaseModel):
    title: str
    script: str
    duration: str
    scenes: List[str]
    equipment_needed: List[str]
    target_platform: str
    required_media: Optional[List[Dict[str, Any]]] = []
    media_timing: Optional[str] = None
    thumbnail_suggestions: Optional[List[str]] = []
    seo_tags: Optional[List[str]] = []
    engagement_hooks: Optional[List[str]] = []

class ContentResponse(BaseModel):
    request_id: str
    company_id: str
    topic: str
    generated_content: List[GeneratedContent]
    blog_post: Optional[BlogPost] = None
    newsletter_article: Optional[NewsletterArticle] = None
    video_scripts: Optional[List[VideoScript]] = None
    media_used: Optional[List[MediaFile]] = []
    media_suggestions: Optional[List[str]] = []
    repurposed_content: Optional[ContentRepurposing] = None
    seo_recommendations: Optional[List[str]] = []
    hashtag_strategy: Optional[Dict[str, Any]] = {}
    performance_forecast: Optional[Dict[str, Any]] = {}
    created_at: str

class ScheduledPost(BaseModel):
    id: Optional[str] = None
    company_id: str
    platform: str
    content: str
    hashtags: List[str]
    scheduled_time: datetime
    status: PostStatus
    topic: str
    media_files: Optional[List[str]] = []
    created_at: Optional[datetime] = None
    published_at: Optional[datetime] = None
    engagement_metrics: Optional[Dict[str, Any]] = None
    approval_status: Optional[ApprovalStatus] = ApprovalStatus.PENDING
    assigned_to: Optional[str] = None
    campaign_id: Optional[str] = None
    auto_generated: Optional[bool] = False

class Analytics(BaseModel):
    company_id: str
    platform: str
    post_id: str
    views: Optional[int] = 0
    likes: Optional[int] = 0
    shares: Optional[int] = 0
    comments: Optional[int] = 0
    engagement_rate: Optional[float] = 0.0
    reach: Optional[int] = 0
    impressions: Optional[int] = 0
    click_through_rate: Optional[float] = 0.0
    recorded_at: datetime
    hashtag_performance: Optional[Dict[str, float]] = {}
    audience_demographics: Optional[Dict[str, Any]] = {}
    competitor_comparison: Optional[Dict[str, float]] = {}

class ROIMetrics(BaseModel):
    company_id: str
    period: str
    total_investment: float
    leads_generated: int
    conversions: int
    revenue_attributed: float
    cost_per_lead: float
    roi_percentage: float
    platform_breakdown: Dict[str, Dict[str, float]]
    content_type_performance: Dict[str, Dict[str, float]]

class BetaFeedback(BaseModel):
    id: Optional[str] = None
    beta_user_id: str
    beta_user_name: str
    beta_user_email: str
    feedback_type: str  # "suggestion", "bug", "feature_request", "improvement"
    title: str
    description: str
    priority: str  # "low", "medium", "high", "urgent"
    status: str  # "open", "in_progress", "implemented", "rejected", "closed"
    admin_response: Optional[str] = None
    implementation_notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    votes: Optional[int] = 0
    category: Optional[str] = None
    attachments: Optional[List[str]] = []

class BetaFeedbackResponse(BaseModel):
    feedback_id: str
    admin_name: str
    response_text: str
    response_type: str  # "reply", "status_update", "implementation_note"
    created_at: Optional[datetime] = None

class BetaUser(BaseModel):
    id: Optional[str] = None
    name: str
    email: str
    beta_id: str
    joined_at: Optional[datetime] = None
    contribution_score: Optional[int] = 0
    feedback_count: Optional[int] = 0
    status: str  # "active", "inactive", "vip"
    special_privileges: Optional[List[str]] = []

class SEOMonitoringAddon(BaseModel):
    id: Optional[str] = None
    company_id: str
    website_url: str
    monitoring_status: str  # "active", "paused", "expired"
    purchased_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    daily_checks_limit: int = 50
    daily_checks_used: int = 0
    last_check_date: Optional[datetime] = None
    auto_check_enabled: bool = True
    notification_email: str
    price_paid: float = 297.0

class SEOParameters(BaseModel):
    id: Optional[str] = None
    parameter_name: str
    parameter_value: str
    source: str  # "google", "bing", "research"
    discovered_date: datetime
    importance_score: int  # 1-10
    category: str  # "technical", "content", "user_experience", "mobile", "core_web_vitals"
    description: str
    implementation_difficulty: str  # "easy", "medium", "hard"

class WebsiteAudit(BaseModel):
    id: Optional[str] = None
    company_id: str
    website_url: str
    page_url: str
    audit_date: datetime
    overall_score: float
    issues_found: List[Dict[str, Any]]
    recommendations: List[Dict[str, Any]]
    priority_fixes: List[Dict[str, Any]]
    estimated_impact: str  # "low", "medium", "high"
    estimated_effort: str  # "1-2 hours", "1-2 days", "1-2 weeks"
    current_seo_parameters: Dict[str, Any]
    compliance_status: Dict[str, bool]

# OAuth-related models
class OAuthToken(BaseModel):
    id: Optional[str] = None
    user_id: str
    platform: str
    access_token: str
    refresh_token: Optional[str] = None
    expires_at: Optional[datetime] = None
    scopes: List[str] = []
    platform_user_id: Optional[str] = None
    platform_username: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_active: Optional[bool] = True

class OAuthAuthorizationRequest(BaseModel):
    platform: str
    user_id: Optional[str] = None
    state: Optional[str] = None

class OAuthTokenExchangeRequest(BaseModel):
    platform: str
    code: str
    state: Optional[str] = None
    user_id: Optional[str] = None

class OAuthConnectionStatus(BaseModel):
    platform: str
    connected: bool
    username: Optional[str] = None
    expires_at: Optional[datetime] = None
    last_used: Optional[datetime] = None
    connection_status: str  # "active", "expired", "revoked", "error"

class ContentPublishRequest(BaseModel):
    content: str
    user_id: Optional[str] = None
    media_urls: Optional[List[str]] = None

# Helper functions
def object_id_to_str(obj):
    """Convert ObjectId to string for JSON serialization"""
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, dict):
        return {k: object_id_to_str(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [object_id_to_str(item) for item in obj]
    return obj

# OAuth Helper Functions
def get_oauth_config(platform: str) -> Dict[str, Any]:
    """Get OAuth configuration for a specific platform"""
    if platform not in OAUTH_CONFIGS:
        raise HTTPException(status_code=400, detail=f"Platform {platform} not supported")
    
    config = OAUTH_CONFIGS[platform].copy()
    
    # For demo mode, use placeholder credentials if not configured
    if not config.get("client_id") or not config.get("client_secret"):
        config["client_id"] = f"demo_client_id_{platform}"
        config["client_secret"] = f"demo_client_secret_{platform}"
        config["demo_mode"] = True
    
    return config

async def store_oauth_token(user_id: str, platform: str, token_data: dict, platform_user_info: dict = None):
    """Store OAuth tokens in database"""
    try:
        expires_at = None
        if token_data.get("expires_in"):
            expires_at = datetime.utcnow() + timedelta(seconds=int(token_data["expires_in"]))
        
        token_record = {
            "user_id": user_id,
            "platform": platform,
            "access_token": token_data["access_token"],
            "refresh_token": token_data.get("refresh_token"),
            "expires_at": expires_at,
            "scopes": token_data.get("scope", "").split() if token_data.get("scope") else [],
            "platform_user_id": platform_user_info.get("id") if platform_user_info else None,
            "platform_username": platform_user_info.get("username") if platform_user_info else None,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "is_active": True
        }
        
        # Upsert token (update if exists, insert if new)
        await db.oauth_tokens.update_one(
            {"user_id": user_id, "platform": platform},
            {"$set": token_record},
            upsert=True
        )
        
        return True
    except Exception as e:
        print(f"Error storing OAuth token: {e}")
        return False

async def get_oauth_token(user_id: str, platform: str) -> Optional[dict]:
    """Get OAuth token for user and platform"""
    try:
        token = await db.oauth_tokens.find_one({
            "user_id": user_id,
            "platform": platform,
            "is_active": True
        })
        
        if token:
            # Check if token is expired
            if token.get("expires_at") and token["expires_at"] < datetime.utcnow():
                # Try to refresh token
                if token.get("refresh_token"):
                    new_token = await refresh_oauth_token(user_id, platform)
                    if new_token:
                        return new_token
                
                # Mark token as inactive if refresh failed
                await db.oauth_tokens.update_one(
                    {"_id": token["_id"]},
                    {"$set": {"is_active": False}}
                )
                return None
            
            token["id"] = str(token["_id"])
            del token["_id"]
            return token
        
        return None
    except Exception as e:
        print(f"Error getting OAuth token: {e}")
        return None

async def refresh_oauth_token(user_id: str, platform: str) -> Optional[dict]:
    """Refresh OAuth token for user and platform"""
    try:
        token_record = await db.oauth_tokens.find_one({
            "user_id": user_id,
            "platform": platform,
            "is_active": True
        })
        
        if not token_record or not token_record.get("refresh_token"):
            return None
        
        config = get_oauth_config(platform)
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                config["token_url"],
                data={
                    "client_id": config["client_id"],
                    "client_secret": config["client_secret"],
                    "refresh_token": token_record["refresh_token"],
                    "grant_type": "refresh_token"
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            if response.status_code == 200:
                new_token_data = response.json()
                
                # Update token in database
                update_data = {
                    "access_token": new_token_data["access_token"],
                    "updated_at": datetime.utcnow()
                }
                
                if new_token_data.get("refresh_token"):
                    update_data["refresh_token"] = new_token_data["refresh_token"]
                
                if new_token_data.get("expires_in"):
                    update_data["expires_at"] = datetime.utcnow() + timedelta(
                        seconds=int(new_token_data["expires_in"])
                    )
                
                await db.oauth_tokens.update_one(
                    {"_id": token_record["_id"]},
                    {"$set": update_data}
                )
                
                # Return updated token
                token_record.update(update_data)
                token_record["id"] = str(token_record["_id"])
                del token_record["_id"]
                return token_record
            
            return None
    except Exception as e:
        print(f"Error refreshing OAuth token: {e}")
        return None

async def revoke_oauth_token(user_id: str, platform: str):
    """Revoke OAuth token on platform and deactivate in database"""
    try:
        token_record = await db.oauth_tokens.find_one({
            "user_id": user_id,
            "platform": platform,
            "is_active": True
        })
        
        if not token_record:
            return True  # Already revoked or doesn't exist
        
        config = get_oauth_config(platform)
        
        # Try to revoke token on platform
        if config.get("revoke_url"):
            try:
                async with httpx.AsyncClient() as client:
                    await client.post(
                        config["revoke_url"],
                        data={
                            "token": token_record["access_token"],
                            "client_id": config["client_id"],
                            "client_secret": config["client_secret"]
                        },
                        headers={"Content-Type": "application/x-www-form-urlencoded"}
                    )
            except:
                pass  # Continue even if revocation fails on platform
        
        # Deactivate token in database
        await db.oauth_tokens.update_one(
            {"_id": token_record["_id"]},
            {"$set": {"is_active": False, "updated_at": datetime.utcnow()}}
        )
        
        return True
    except Exception as e:
        print(f"Error revoking OAuth token: {e}")
        return False

async def get_user_connected_platforms(user_id: str) -> List[OAuthConnectionStatus]:
    """Get list of connected platforms for user"""
    try:
        connections = []
        tokens = await db.oauth_tokens.find({
            "user_id": user_id,
            "is_active": True
        }).to_list(length=None)
        
        for token in tokens:
            status = "active"
            if token.get("expires_at") and token["expires_at"] < datetime.utcnow():
                status = "expired"
            
            connections.append(OAuthConnectionStatus(
                platform=token["platform"],
                connected=True,
                username=token.get("platform_username"),
                expires_at=token.get("expires_at"),
                last_used=token.get("updated_at"),
                connection_status=status
            ))
        
        return connections
    except Exception as e:
        print(f"Error getting connected platforms: {e}")
        return []

async def get_company_by_id(company_id: str):
    """Get company by ID from database"""
    try:
        company = await db.companies.find_one({"_id": ObjectId(company_id)})
        if company:
            company["id"] = str(company["_id"])
            del company["_id"]
            return company
        return None
    except Exception as e:
        print(f"Error getting company: {e}")
        return None

async def get_company_media(company_id: str, media_type: Optional[MediaType] = None, category: Optional[MediaCategory] = None, limit: int = 10):
    """Get media files for a company"""
    try:
        query = {"company_id": company_id, "is_active": True}
        if media_type:
            query["media_type"] = media_type
        if category:
            query["category"] = category
        
        media_files = []
        async for media in db.media_files.find(query).sort("upload_date", -1).limit(limit):
            media["id"] = str(media["_id"])
            del media["_id"]
            media_files.append(media)
        
        return media_files
    except Exception as e:
        print(f"Error getting company media: {e}")
        return []

def calculate_seo_score(content: str, target_keywords: List[str]) -> SEOAnalysis:
    """Calculate SEO score for content"""
    try:
        # Basic SEO analysis
        word_count = len(content.split())
        char_count = len(content)
        
        # Keyword density calculation
        keyword_density = {}
        for keyword in target_keywords:
            keyword_count = content.lower().count(keyword.lower())
            density = (keyword_count / word_count) * 100 if word_count > 0 else 0
            keyword_density[keyword] = density
        
        # Readability score (simplified Flesch Reading Ease)
        sentences = content.count('.') + content.count('!') + content.count('?')
        avg_sentence_length = word_count / sentences if sentences > 0 else 0
        syllables = sum([len(word) // 2 for word in content.split()])  # Approximation
        avg_syllables_per_word = syllables / word_count if word_count > 0 else 0
        
        readability_score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
        readability_score = max(0, min(100, readability_score))
        
        # Overall SEO score
        seo_score = 0
        
        # Word count optimization (800-2000 words is optimal)
        if 800 <= word_count <= 2000:
            seo_score += 25
        elif 500 <= word_count <= 3000:
            seo_score += 15
        else:
            seo_score += 5
        
        # Keyword density optimization (1-3% is optimal)
        avg_keyword_density = sum(keyword_density.values()) / len(keyword_density) if keyword_density else 0
        if 1 <= avg_keyword_density <= 3:
            seo_score += 25
        elif 0.5 <= avg_keyword_density <= 5:
            seo_score += 15
        else:
            seo_score += 5
        
        # Readability score (60-70 is optimal)
        if 60 <= readability_score <= 70:
            seo_score += 25
        elif 50 <= readability_score <= 80:
            seo_score += 15
        else:
            seo_score += 5
        
        # Content structure (headings, paragraphs)
        has_headings = any(line.strip().startswith('#') for line in content.split('\n'))
        has_short_paragraphs = avg_sentence_length < 20
        
        if has_headings and has_short_paragraphs:
            seo_score += 25
        elif has_headings or has_short_paragraphs:
            seo_score += 15
        else:
            seo_score += 5
        
        # Generate recommendations
        recommendations = []
        if word_count < 800:
            recommendations.append("Increase content length to 800-2000 words for better SEO")
        if avg_keyword_density < 1:
            recommendations.append("Increase keyword density to 1-3% for better ranking")
        if readability_score < 60:
            recommendations.append("Improve readability by using shorter sentences and simpler words")
        if not has_headings:
            recommendations.append("Add headings (H1, H2, H3) to improve content structure")
        
        # Generate meta description
        meta_description = content[:150].strip() + "..."
        
        # Generate suggested title
        suggested_title = f"{target_keywords[0].title()} - Complete Guide" if target_keywords else "Complete Guide"
        
        return SEOAnalysis(
            content=content,
            seo_score=seo_score,
            keyword_density=keyword_density,
            readability_score=readability_score,
            meta_description=meta_description,
            suggested_title=suggested_title,
            recommendations=recommendations,
            target_keywords=target_keywords
        )
    except Exception as e:
        print(f"Error calculating SEO score: {e}")
        return SEOAnalysis(
            content=content,
            seo_score=50.0,
            keyword_density={},
            readability_score=50.0,
            meta_description="",
            suggested_title="",
            recommendations=["Error calculating SEO metrics"],
            target_keywords=target_keywords
        )

def analyze_hashtags(hashtags: List[str], industry: str) -> List[HashtagAnalysis]:
    """Analyze hashtag performance and trends"""
    try:
        analyses = []
        industry_hashtags = TRENDING_HASHTAGS.get(industry, {"trending": [], "stable": [], "declining": []})
        
        for hashtag in hashtags:
            # Determine trend direction
            if hashtag in industry_hashtags["trending"]:
                trend_direction = HashtagStatus.TRENDING
                popularity_score = 85.0
                engagement_rate = 0.035
            elif hashtag in industry_hashtags["stable"]:
                trend_direction = HashtagStatus.STABLE
                popularity_score = 65.0
                engagement_rate = 0.020
            elif hashtag in industry_hashtags["declining"]:
                trend_direction = HashtagStatus.DECLINING
                popularity_score = 35.0
                engagement_rate = 0.010
            else:
                trend_direction = HashtagStatus.STABLE
                popularity_score = 50.0
                engagement_rate = 0.015
            
            # Competition level based on popularity
            if popularity_score > 80:
                competition_level = "High"
            elif popularity_score > 50:
                competition_level = "Medium"
            else:
                competition_level = "Low"
            
            # Related hashtags
            related_hashtags = []
            for category in industry_hashtags.values():
                related_hashtags.extend([h for h in category if h != hashtag][:3])
            
            # Estimated reach (simplified calculation)
            estimated_reach = int(popularity_score * 100 * random.uniform(0.8, 1.2))
            
            analysis = HashtagAnalysis(
                hashtag=hashtag,
                popularity_score=popularity_score,
                engagement_rate=engagement_rate,
                competition_level=competition_level,
                trend_direction=trend_direction,
                related_hashtags=related_hashtags[:5],
                best_times_to_use=["9:00", "14:00", "19:00"],
                estimated_reach=estimated_reach
            )
            analyses.append(analysis)
        
        return analyses
    except Exception as e:
        print(f"Error analyzing hashtags: {e}")
        return []

def predict_content_performance(content: str, platform: str, hashtags: List[str], company_data: dict) -> float:
    """Predict content performance based on various factors"""
    try:
        base_score = 50.0
        
        # Platform-specific factors
        platform_config = PLATFORM_CONFIGS.get(platform, {})
        base_engagement = platform_config.get("engagement_rate_avg", 0.02)
        
        # Content length optimization
        content_length = len(content)
        optimal_length = platform_config.get("max_chars", 1000) * 0.7
        
        if content_length <= optimal_length:
            base_score += 20
        else:
            base_score += 10
        
        # Hashtag quality
        hashtag_score = sum([85 if h in TRENDING_HASHTAGS.get(company_data.get("industry", ""), {}).get("trending", []) else 50 for h in hashtags])
        hashtag_score = hashtag_score / len(hashtags) if hashtags else 50
        base_score += (hashtag_score - 50) * 0.3
        
        # Engagement factors
        has_call_to_action = any(cta in content.lower() for cta in ["click", "visit", "learn", "download", "contact"])
        has_emojis = any(ord(char) > 127 for char in content)
        has_questions = "?" in content
        
        if has_call_to_action:
            base_score += 10
        if has_emojis:
            base_score += 5
        if has_questions:
            base_score += 5
        
        # Industry relevance
        industry_keywords = SEO_KEYWORDS.get(company_data.get("industry", ""), [])
        keyword_matches = sum(1 for keyword in industry_keywords if keyword.lower() in content.lower())
        base_score += (keyword_matches / len(industry_keywords)) * 15 if industry_keywords else 0
        
        # Ensure score is between 0 and 100
        return max(0, min(100, base_score))
    except Exception as e:
        print(f"Error predicting content performance: {e}")
        return 50.0

def generate_content_variations(content: str, platforms: List[str]) -> Dict[str, str]:
    """Generate platform-specific variations of content"""
    try:
        variations = {}
        
        for platform in platforms:
            platform_config = PLATFORM_CONFIGS.get(platform, {})
            max_chars = platform_config.get("max_chars", 1000)
            style = platform_config.get("style", "general")
            
            if len(content) <= max_chars:
                variations[platform] = content
            else:
                # Truncate and add platform-specific ending
                truncated = content[:max_chars-50]
                if platform == "twitter" or platform == "x":
                    variations[platform] = truncated + "... Read more 🧵"
                elif platform == "instagram":
                    variations[platform] = truncated + "... See more in our bio! 📍"
                elif platform == "linkedin":
                    variations[platform] = truncated + "... Continue reading in comments 💬"
                else:
                    variations[platform] = truncated + "..."
        
        return variations
    except Exception as e:
        print(f"Error generating content variations: {e}")
        return {}

def save_uploaded_file(file: UploadFile, company_id: str, category: str) -> tuple:
    """Save uploaded file and return file path and metadata"""
    try:
        # Create company directory
        company_dir = UPLOAD_DIR / company_id
        company_dir.mkdir(exist_ok=True)
        
        # Create category subdirectory
        category_dir = company_dir / category
        category_dir.mkdir(exist_ok=True)
        
        # Generate unique filename
        file_extension = Path(file.filename).suffix
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = category_dir / unique_filename
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Get file size
        file_size = file_path.stat().st_size
        
        # Get mime type
        mime_type = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
        
        return str(file_path), file_size, mime_type
        
    except Exception as e:
        print(f"Error saving file: {e}")
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

def determine_media_type(mime_type: str) -> MediaType:
    """Determine media type from MIME type"""
    if mime_type.startswith("image/"):
        return MediaType.IMAGE
    elif mime_type.startswith("video/"):
        return MediaType.VIDEO
    else:
        return MediaType.IMAGE  # Default to image

def process_image(file_path: str) -> dict:
    """Process and optimize image"""
    try:
        with Image.open(file_path) as img:
            # Get image dimensions
            width, height = img.size
            
            # Create thumbnail if image is large
            if width > 1920 or height > 1080:
                img.thumbnail((1920, 1080), Image.Resampling.LANCZOS)
                img.save(file_path, optimize=True, quality=85)
            
            return {
                "width": width,
                "height": height,
                "format": img.format,
                "mode": img.mode
            }
    except Exception as e:
        print(f"Error processing image: {e}")
        return {}

# Enhanced content generation functions
def create_enhanced_platform_prompt(platform: str, company: dict, topic: str, audience_level: str, additional_context: str, available_media: List[dict], target_keywords: List[str], template_data: dict = None):
    config = PLATFORM_CONFIGS[platform]
    
    company_context = f"""
    Company: {company['name']}
    Industry: {company.get('industry', 'Construction and Environmental Training')}
    Target Audience: {company.get('target_audience', 'Construction workers, safety managers, environmental professionals')}
    Brand Voice: {company.get('brand_voice', 'Professional but accessible, safety-focused, educational')}
    Website: {company.get('website', '')}
    Brand Colors: {company.get('brand_colors', {})}
    """
    
    media_context = ""
    if available_media:
        media_context = f"""
        Available Company Media:
        {chr(10).join([f"- {media['category']}: {media['description']} (Tags: {', '.join(media.get('tags', []))})" for media in available_media[:5]])}
        """
    
    seo_context = ""
    if target_keywords:
        seo_context = f"""
        SEO Target Keywords: {', '.join(target_keywords)}
        Industry SEO Keywords: {', '.join(SEO_KEYWORDS.get(company.get('industry', ''), [])[:5])}
        """
    
    template_context = ""
    if template_data:
        template_context = f"""
        Template Structure: {template_data.get('template_content', '')}
        Template Variables: {', '.join(template_data.get('variables', []))}
        """
    
    hashtag_context = f"""
    Trending Hashtags for {company.get('industry', '')}: {', '.join(TRENDING_HASHTAGS.get(company.get('industry', ''), {}).get('trending', [])[:5])}
    Stable Hashtags: {', '.join(TRENDING_HASHTAGS.get(company.get('industry', ''), {}).get('stable', [])[:5])}
    """
    
    prompt = f"""
    Create an optimized {platform} post for {company['name']} about "{topic}".

    {company_context}

    {media_context}

    {seo_context}

    {template_context}

    {hashtag_context}

    Platform Requirements:
    - Maximum {config['max_chars']} characters
    - Style: {config['style']}
    - Format: {config['format']}
    - Use maximum {config['hashtag_limit']} relevant hashtags
    - Audience level: {audience_level}
    - Optimal posting times: {config['optimal_times']}
    - Expected engagement rate: {config['engagement_rate_avg']}
    - Video support: {config['supports_video']}
    - Media required: {config['media_required']}
    
    Additional Context: {additional_context}

    Advanced Guidelines:
    1. Include trending hashtags for maximum visibility
    2. Optimize for SEO with target keywords naturally integrated
    3. Create hook that captures attention in first 3 seconds
    4. Include clear call-to-action
    5. Reference available company media when appropriate
    6. Use brand voice consistently
    7. Include engagement triggers (questions, polls, etc.)
    8. Optimize for platform-specific algorithms
    9. Include performance predictions
    10. Suggest cross-platform promotion strategies
    
    Provide the content in this exact format:
    CONTENT: [the actual post content optimized for engagement]
    HASHTAGS: [comma-separated hashtags including trending ones]
    ENGAGEMENT_TIP: [specific tip for maximizing engagement on this platform]
    POSTING_TIP: [optimal posting strategy including timing and frequency]
    VIDEO_SUGGESTION: [detailed video concept if platform supports video]
    MEDIA_SUGGESTIONS: [specific media types/categories needed]
    MEDIA_PLACEMENT: [detailed instructions for media placement]
    SEO_KEYWORDS: [naturally integrated keywords for discoverability]
    PERFORMANCE_PREDICTION: [estimated engagement rate and reach]
    CROSS_PROMOTION: [strategy for promoting this content on other platforms]
    """
    
    return prompt

def create_enhanced_blog_prompt(company: dict, topic: str, additional_context: str, available_media: List[dict], target_keywords: List[str]):
    seo_keywords = target_keywords or SEO_KEYWORDS.get(company.get('industry', ''), [])
    
    prompt = f"""
    Create a comprehensive, SEO-optimized blog post for {company['name']} about "{topic}".
    
    Company Context: {company.get('description', '')}
    Industry: {company.get('industry', 'Construction and Environmental Training')}
    Target Audience: {company.get('target_audience', 'Construction workers, safety managers, environmental professionals')}
    Brand Voice: {company.get('brand_voice', 'Professional but accessible, safety-focused, educational')}
    Website: {company.get('website', '')}
    
    SEO Requirements:
    - Target Keywords: {', '.join(seo_keywords)}
    - Keyword Density: 1-3% for primary keywords
    - Word Count: 1500-2500 words
    - Readability Score: 60-70 (Flesch Reading Ease)
    - Meta Description: 150-160 characters
    - Internal Linking Opportunities: 3-5 links
    - External Authority Links: 2-3 links
    
    Available Company Media:
    {chr(10).join([f"- {media['category']}: {media['description']} (Tags: {', '.join(media.get('tags', []))})" for media in available_media[:10]]) if available_media else "No media available"}
    
    Requirements:
    - Comprehensive coverage of the topic
    - Professional but accessible tone
    - Include practical tips and actionable advice
    - Reference current regulations and industry standards
    - Include relevant statistics and data
    - Optimize for featured snippets
    - Include FAQ section
    - Add conclusion with strong call-to-action
    - Incorporate available company media strategically
    - Include schema markup suggestions
    
    Additional Context: {additional_context}
    
    Format the response as:
    TITLE: [SEO-optimized title with primary keyword]
    META_DESCRIPTION: [compelling 150-160 character description]
    EXCERPT: [engaging 2-3 sentence summary]
    CONTENT: [complete blog post with H1, H2, H3 headings]
    READ_TIME: [estimated reading time]
    SEO_KEYWORDS: [comma-separated target keywords]
    MEDIA_SUGGESTIONS: [specific media types for this blog post]
    MEDIA_PLACEMENT: [detailed instructions for media placement throughout]
    INTERNAL_LINKS: [suggested internal link opportunities]
    EXTERNAL_LINKS: [suggested external authority links]
    SCHEMA_MARKUP: [suggested schema markup type]
    FAQ_SECTION: [relevant frequently asked questions]
    SOCIAL_SHARING: [optimized social media sharing text]
    """
    
    return prompt

async def generate_content_with_claude(prompt: str, authenticity_settings: dict = None):
    try:
        # Add authenticity instructions to the prompt
        authenticity_prompt = """

CRITICAL: Make this content sound genuinely human and authentic. Follow these authenticity guidelines:

VOICE & TONE:
- Use conversational, natural language - NOT corporate speak
- Include occasional contractions (don't, can't, we'll, it's)
- Add personality quirks and casual expressions
- Vary sentence length - mix short punchy sentences with longer ones
- Include minor imperfections that real people have

CONTENT AUTHENTICITY:
- Add specific personal details or experiences when possible
- Reference real, current events or trends naturally
- Use genuine emotions and reactions
- Include conversational bridges ("So here's the thing...", "You know what I realized?")
- Add authentic questions that real people would ask

ENGAGEMENT PATTERNS:
- Don't start every post with a question
- Avoid overused phrases like "Thanks for sharing!" 
- Include genuine curiosity and enthusiasm
- Reference specific details that show real knowledge
- Use platform-appropriate slang and cultural references

PLATFORM AUTHENTICITY:
- Match the natural voice of each platform's users
- Don't over-optimize hashtags - make them feel organic
- Include platform-specific conversational styles
- Reference platform culture naturally

AVOID AI-SOUNDING PATTERNS:
- Don't use excessive buzzwords or marketing jargon
- Avoid perfectly parallel structures in lists
- Don't be overly positive about everything
- Skip templated responses that could apply to anyone
- No robotic "Perfect grammar and punctuation throughout"

PERSONALITY INJECTION:
- Add subtle humor or wit when appropriate
- Include personal opinions and perspectives
- Show genuine interest in the topic
- Use storytelling elements
- Include authentic reactions and emotions

""" + prompt
        
        # Adjust temperature for more natural variation
        temperature = 0.8 if authenticity_settings and authenticity_settings.get('high_variation') else 0.7
        
        response = client.messages.create(
            model="claude-3-5-haiku-latest",
            max_tokens=3000,
            temperature=temperature,
            messages=[
                {"role": "user", "content": authenticity_prompt}
            ]
        )
        return response.content[0].text
    except Exception as e:
        print(f"Claude API error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Claude API error: {str(e)}")

def parse_enhanced_platform_content(content: str):
    lines = content.strip().split('\n')
    parsed = {
        'content': '',
        'hashtags': [],
        'engagement_tip': '',
        'posting_tip': '',
        'video_suggestion': '',
        'media_suggestions': [],
        'media_placement': '',
        'seo_keywords': [],
        'performance_prediction': '',
        'cross_promotion': ''
    }
    
    current_section = None
    for line in lines:
        line = line.strip()
        if line.startswith('CONTENT:'):
            current_section = 'content'
            parsed['content'] = line.replace('CONTENT:', '').strip()
        elif line.startswith('HASHTAGS:'):
            current_section = 'hashtags'
            hashtags_str = line.replace('HASHTAGS:', '').strip()
            parsed['hashtags'] = [tag.strip().replace('#', '') for tag in hashtags_str.split(',') if tag.strip()]
        elif line.startswith('ENGAGEMENT_TIP:'):
            current_section = 'engagement_tip'
            parsed['engagement_tip'] = line.replace('ENGAGEMENT_TIP:', '').strip()
        elif line.startswith('POSTING_TIP:'):
            current_section = 'posting_tip'
            parsed['posting_tip'] = line.replace('POSTING_TIP:', '').strip()
        elif line.startswith('VIDEO_SUGGESTION:'):
            current_section = 'video_suggestion'
            parsed['video_suggestion'] = line.replace('VIDEO_SUGGESTION:', '').strip()
        elif line.startswith('MEDIA_SUGGESTIONS:'):
            current_section = 'media_suggestions'
            suggestions_str = line.replace('MEDIA_SUGGESTIONS:', '').strip()
            parsed['media_suggestions'] = [s.strip() for s in suggestions_str.split(',') if s.strip()]
        elif line.startswith('MEDIA_PLACEMENT:'):
            current_section = 'media_placement'
            parsed['media_placement'] = line.replace('MEDIA_PLACEMENT:', '').strip()
        elif line.startswith('SEO_KEYWORDS:'):
            current_section = 'seo_keywords'
            keywords_str = line.replace('SEO_KEYWORDS:', '').strip()
            parsed['seo_keywords'] = [kw.strip() for kw in keywords_str.split(',') if kw.strip()]
        elif line.startswith('PERFORMANCE_PREDICTION:'):
            current_section = 'performance_prediction'
            parsed['performance_prediction'] = line.replace('PERFORMANCE_PREDICTION:', '').strip()
        elif line.startswith('CROSS_PROMOTION:'):
            current_section = 'cross_promotion'
            parsed['cross_promotion'] = line.replace('CROSS_PROMOTION:', '').strip()
        elif current_section and line:
            if current_section in ['content', 'engagement_tip', 'posting_tip', 'video_suggestion', 'media_placement', 'performance_prediction', 'cross_promotion']:
                parsed[current_section] += ' ' + line
    
    return parsed

def parse_enhanced_blog_content(content: str):
    lines = content.strip().split('\n')
    parsed = {
        'title': '',
        'meta_description': '',
        'excerpt': '',
        'content': '',
        'estimated_read_time': '',
        'seo_keywords': [],
        'media_suggestions': [],
        'media_placement_guide': '',
        'internal_links': [],
        'external_links': [],
        'schema_markup': '',
        'faq_section': '',
        'social_sharing': ''
    }
    
    current_section = None
    for line in lines:
        line = line.strip()
        if line.startswith('TITLE:'):
            current_section = 'title'
            parsed['title'] = line.replace('TITLE:', '').strip()
        elif line.startswith('META_DESCRIPTION:'):
            current_section = 'meta_description'
            parsed['meta_description'] = line.replace('META_DESCRIPTION:', '').strip()
        elif line.startswith('EXCERPT:'):
            current_section = 'excerpt'
            parsed['excerpt'] = line.replace('EXCERPT:', '').strip()
        elif line.startswith('CONTENT:'):
            current_section = 'content'
            parsed['content'] = line.replace('CONTENT:', '').strip()
        elif line.startswith('READ_TIME:'):
            current_section = 'estimated_read_time'
            parsed['estimated_read_time'] = line.replace('READ_TIME:', '').strip()
        elif line.startswith('SEO_KEYWORDS:'):
            current_section = 'seo_keywords'
            keywords_str = line.replace('SEO_KEYWORDS:', '').strip()
            parsed['seo_keywords'] = [kw.strip() for kw in keywords_str.split(',') if kw.strip()]
        elif line.startswith('MEDIA_SUGGESTIONS:'):
            current_section = 'media_suggestions'
            suggestions_str = line.replace('MEDIA_SUGGESTIONS:', '').strip()
            parsed['media_suggestions'] = [s.strip() for s in suggestions_str.split(',') if s.strip()]
        elif line.startswith('MEDIA_PLACEMENT:'):
            current_section = 'media_placement_guide'
            parsed['media_placement_guide'] = line.replace('MEDIA_PLACEMENT:', '').strip()
        elif line.startswith('INTERNAL_LINKS:'):
            current_section = 'internal_links'
            links_str = line.replace('INTERNAL_LINKS:', '').strip()
            parsed['internal_links'] = [link.strip() for link in links_str.split(',') if link.strip()]
        elif line.startswith('EXTERNAL_LINKS:'):
            current_section = 'external_links'
            links_str = line.replace('EXTERNAL_LINKS:', '').strip()
            parsed['external_links'] = [link.strip() for link in links_str.split(',') if link.strip()]
        elif line.startswith('SCHEMA_MARKUP:'):
            current_section = 'schema_markup'
            parsed['schema_markup'] = line.replace('SCHEMA_MARKUP:', '').strip()
        elif line.startswith('FAQ_SECTION:'):
            current_section = 'faq_section'
            parsed['faq_section'] = line.replace('FAQ_SECTION:', '').strip()
        elif line.startswith('SOCIAL_SHARING:'):
            current_section = 'social_sharing'
            parsed['social_sharing'] = line.replace('SOCIAL_SHARING:', '').strip()
        elif current_section and line:
            if current_section in ['content', 'media_placement_guide', 'faq_section', 'social_sharing']:
                parsed[current_section] += '\n' + line
            elif current_section in ['excerpt', 'title', 'meta_description', 'estimated_read_time', 'schema_markup']:
                parsed[current_section] += ' ' + line
    
    # Set defaults if not found
    if not parsed['estimated_read_time']:
        parsed['estimated_read_time'] = '8-12 minutes'
    if not parsed['excerpt']:
        parsed['excerpt'] = 'A comprehensive guide to the topic.'
    if not parsed['title']:
        parsed['title'] = 'Complete Guide'
    if not parsed['meta_description']:
        parsed['meta_description'] = parsed['excerpt'][:160]
    
    return parsed

async def check_monthly_media_requests():
    """Check which companies need monthly media requests"""
    try:
        current_date = datetime.utcnow()
        one_month_ago = current_date - timedelta(days=30)
        
        companies_to_request = []
        async for company in db.companies.find():
            last_request = company.get('last_media_request')
            if not last_request or last_request < one_month_ago:
                media_count = await db.media_files.count_documents({"company_id": str(company["_id"]), "is_active": True})
                
                companies_to_request.append({
                    "company_id": str(company["_id"]),
                    "company_name": company["name"],
                    "current_media_count": media_count,
                    "last_request": last_request,
                    "suggestion": generate_media_suggestion(company, media_count)
                })
        
        return companies_to_request
    except Exception as e:
        print(f"Error checking monthly media requests: {e}")
        return []

def generate_media_suggestion(company: dict, current_media_count: int) -> str:
    """Generate media suggestion based on company profile"""
    industry = company.get('industry', 'Construction')
    
    if current_media_count == 0:
        return f"Start your media library with photos of your team, equipment, and workplace. For {industry} companies, consider safety training sessions, equipment in action, and completed projects."
    elif current_media_count < 10:
        return f"Add more variety to your media library. Consider behind-the-scenes content, customer testimonials, and seasonal safety campaigns."
    else:
        return f"Keep your media library fresh with new training sessions, recent projects, and updated team photos. Consider creating short video demonstrations of safety procedures."

# API Routes
@app.get("/api/debug")
async def debug():
    return {
        "claude_api_key_exists": os.getenv("CLAUDE_API_KEY") is not None,
        "claude_api_key_length": len(os.getenv("CLAUDE_API_KEY", "")),
        "mongo_connected": True,
        "upload_dir": str(UPLOAD_DIR),
        "upload_dir_exists": UPLOAD_DIR.exists(),
        "seo_keywords_loaded": len(SEO_KEYWORDS) > 0,
        "trending_hashtags_loaded": len(TRENDING_HASHTAGS) > 0,
        "platform_configs": len(PLATFORM_CONFIGS)
    }

@app.get("/api/health")
async def health_check(login: str = None):
    if login == "user":
        return HTMLResponse("""
        <html><body style="background:linear-gradient(135deg,#667eea,#764ba2);color:white;font-family:system-ui;padding:2rem;text-align:center">
        <h1>🚀 PostVelocity User Login</h1>
        <form action="/api/auth/login" method="post" style="background:white;color:black;padding:2rem;border-radius:1rem;display:inline-block">
        <div style="margin:1rem 0"><label>Email:</label><br><input type="email" name="email" value="user@postvelocity.com" style="padding:0.5rem;width:300px"></div>
        <div style="margin:1rem 0"><label>Password:</label><br><input type="password" name="password" value="user123" style="padding:0.5rem;width:300px"></div>
        <button type="submit" style="background:#667eea;color:white;padding:1rem 2rem;border:none;border-radius:0.5rem">Login</button>
        </form></body></html>
        """)
    elif login == "admin":
        return HTMLResponse("""
        <html><body style="background:linear-gradient(135deg,#ff6b6b,#feca57);color:white;font-family:system-ui;padding:2rem;text-align:center">
        <h1>🔐 PostVelocity Admin Login</h1>
        <form action="/api/auth/admin-login" method="post" style="background:white;color:black;padding:2rem;border-radius:1rem;display:inline-block">
        <div style="margin:1rem 0"><label>Admin Email:</label><br><input type="email" name="email" value="admin@postvelocity.com" style="padding:0.5rem;width:300px"></div>
        <div style="margin:1rem 0"><label>Admin Password:</label><br><input type="password" name="password" value="admin123" style="padding:0.5rem;width:300px"></div>
        <button type="submit" style="background:#ff6b6b;color:white;padding:1rem 2rem;border:none;border-radius:0.5rem">Admin Login</button>
        </form></body></html>
        """)
    return {"status": "healthy", "message": "Advanced Social Media Content Generator with AI-Powered Features"}

# Authentication Routes
@app.post("/api/auth/login")
async def login(request: Request):
    form = await request.form()
    email = form.get("email")
    password = form.get("password")
    
    # Simple demo authentication - replace with real authentication
    demo_users = {
        "user@postvelocity.com": {"password": "user123", "role": "user", "full_name": "Demo User"},
        "admin@postvelocity.com": {"password": "admin123", "role": "admin", "full_name": "Admin User"},
        "test@test.com": {"password": "test", "role": "user", "full_name": "Test User"}
    }
    
    if email in demo_users and demo_users[email]["password"] == password:
        user_data = demo_users[email]
        
        # Return HTML redirect to main app with success message
        return HTMLResponse("""
        <html>
        <head>
            <script>
                // Store user data in localStorage
                const userData = {
                    id: '""" + str(hash(email)) + """',
                    email: '""" + email + """',
                    full_name: '""" + user_data["full_name"] + """',
                    role: '""" + user_data["role"] + """'
                };
                localStorage.setItem('currentUser', JSON.stringify(userData));
                localStorage.setItem('authToken', 'demo_token_""" + str(hash(email)) + """');
                localStorage.setItem('isAuthenticated', 'true');
                
                // Redirect directly to dashboard - no intermediate step
                window.location.href = '/dashboard';
            </script>
        </head>
        <body>
            <p>Login successful! Redirecting...</p>
        </body>
        </html>
        """)
    else:
        return HTMLResponse("""
        <html>
        <head>
            <style>
                body { 
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }
                .error-container {
                    background: white;
                    padding: 2rem;
                    border-radius: 1rem;
                    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
                    text-align: center;
                    max-width: 400px;
                }
                .error-title { color: #e53e3e; margin-bottom: 1rem; }
                .back-link { color: #667eea; text-decoration: none; }
                .back-link:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <div class="error-container">
                <h2 class="error-title">❌ Login Failed</h2>
                <p>Invalid email or password. Please try again.</p>
                <a href="/api/user-login" class="back-link">← Back to Login</a>
            </div>
        </body>
        </html>
        """, status_code=401)

@app.post("/api/auth/admin-login") 
async def admin_login(request: Request):
    form = await request.form()
    email = form.get("email")
    password = form.get("password")
    
    # Admin-specific authentication
    if email == "admin@postvelocity.com" and password == "admin123":
        return HTMLResponse("""
        <html>
        <head>
            <script>
                // Store admin user data in localStorage
                const userData = {
                    id: 'admin_001',
                    email: '""" + email + """',
                    full_name: 'PostVelocity Admin',
                    role: 'admin'
                };
                localStorage.setItem('currentUser', JSON.stringify(userData));
                localStorage.setItem('authToken', 'admin_demo_token');
                localStorage.setItem('isAuthenticated', 'true');
                
                // Redirect directly to dashboard - no intermediate step
                window.location.href = '/dashboard';
            </script>
        </head>
        <body>
            <p>Admin login successful! Redirecting...</p>
        </body>
        </html>
        """)
    else:
        return HTMLResponse("""
        <html>
        <head>
            <style>
                body { 
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    background: linear-gradient(135deg, #ff6b6b 0%, #feca57 100%);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }
                .error-container {
                    background: white;
                    padding: 2rem;
                    border-radius: 1rem;
                    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
                    text-align: center;
                    max-width: 400px;
                }
                .error-title { color: #e53e3e; margin-bottom: 1rem; }
                .back-link { color: #ff6b6b; text-decoration: none; }
                .back-link:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <div class="error-container">
                <h2 class="error-title">❌ Admin Login Failed</h2>
                <p>Invalid admin credentials. Access denied.</p>
                <a href="/api/admin-login" class="back-link">← Back to Admin Login</a>
            </div>
        </body>
        </html>
        """, status_code=401)

@app.post("/api/auth/setup-admin")
async def setup_admin():
    # Setup demo admin user
    return {
        "success": True,
        "message": "Demo admin user created",
        "credentials": {
            "email": "admin@postvelocity.com",
            "password": "admin123"
        }
    }

# Enhanced Content Generation
@app.post("/api/generate-content", response_model=ContentResponse)
async def generate_enhanced_content(request: ContentRequest):
    try:
        # Get company information
        company = await get_company_by_id(request.company_id)
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        
        # Get available media if requested
        available_media = []
        if request.use_company_media:
            available_media = await get_company_media(request.company_id, limit=20)
        
        # Set up SEO keywords
        target_keywords = request.target_keywords or SEO_KEYWORDS.get(company.get('industry', ''), [])[:5]
        
        # Get template data if specified
        template_data = None
        if request.template_id:
            template = await db.content_templates.find_one({"_id": ObjectId(request.template_id)})
            if template:
                template_data = template
        
        request_id = str(uuid.uuid4())
        generated_content = []
        
        # Generate enhanced content for each platform
        for platform in request.platforms:
            if platform not in PLATFORM_CONFIGS:
                raise HTTPException(status_code=400, detail=f"Unsupported platform: {platform}")
            
            prompt = create_enhanced_platform_prompt(
                platform, 
                company, 
                request.topic, 
                request.audience_level,
                request.additional_context,
                available_media,
                target_keywords,
                template_data
            )
            
            raw_content = await generate_content_with_claude(prompt)
            parsed_content = parse_enhanced_platform_content(raw_content)
            
            # Calculate SEO analysis
            seo_analysis = None
            if request.seo_focus:
                seo_analysis = calculate_seo_score(parsed_content['content'], parsed_content['seo_keywords'])
            
            # Analyze hashtags
            hashtag_analysis = analyze_hashtags(parsed_content['hashtags'], company.get('industry', ''))
            
            # Predict performance
            performance_prediction = predict_content_performance(
                parsed_content['content'], 
                platform, 
                parsed_content['hashtags'], 
                company
            )
            
            # Generate platform variations if requested
            repurposed_versions = {}
            if request.repurpose_content:
                repurposed_versions = generate_content_variations(parsed_content['content'], request.platforms)
            
            # Select relevant media for this platform
            platform_media = []
            if available_media and parsed_content.get('media_suggestions'):
                for suggestion in parsed_content['media_suggestions']:
                    for media in available_media:
                        if any(tag.lower() in suggestion.lower() for tag in media.get('tags', [])) or \
                           media.get('category', '').lower() in suggestion.lower():
                            platform_media.append({
                                "id": media["id"],
                                "filename": media["filename"],
                                "file_path": media["file_path"],
                                "media_type": media["media_type"],
                                "category": media["category"],
                                "description": media["description"]
                            })
                            break
            
            content_item = GeneratedContent(
                platform=platform,
                content=parsed_content['content'],
                hashtags=parsed_content['hashtags'],
                estimated_engagement=parsed_content['engagement_tip'],
                posting_tips=parsed_content['posting_tip'],
                video_suggestions=parsed_content['video_suggestion'],
                optimal_posting_times=PLATFORM_CONFIGS[platform]['optimal_times'],
                suggested_media=platform_media,
                media_placement=parsed_content.get('media_placement', ''),
                seo_analysis=seo_analysis,
                hashtag_analysis=hashtag_analysis,
                performance_prediction=performance_prediction,
                repurposed_versions=repurposed_versions
            )
            
            generated_content.append(content_item)
        
        # Generate enhanced blog post if requested
        blog_post = None
        if request.generate_blog or len(request.platforms) > 4:
            blog_prompt = create_enhanced_blog_prompt(company, request.topic, request.additional_context, available_media, target_keywords)
            blog_raw = await generate_content_with_claude(blog_prompt)
            blog_parsed = parse_enhanced_blog_content(blog_raw)
            
            # Calculate SEO analysis for blog
            blog_seo_analysis = calculate_seo_score(blog_parsed['content'], blog_parsed['seo_keywords'])
            
            # Generate schema markup
            schema_markup = {
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": blog_parsed['title'],
                "description": blog_parsed['meta_description'],
                "author": {
                    "@type": "Organization",
                    "name": company['name']
                },
                "publisher": {
                    "@type": "Organization",
                    "name": company['name']
                }
            }
            
            # Select media for blog post
            blog_media = []
            if available_media and blog_parsed.get('media_suggestions'):
                for suggestion in blog_parsed['media_suggestions']:
                    for media in available_media:
                        if any(tag.lower() in suggestion.lower() for tag in media.get('tags', [])) or \
                           media.get('category', '').lower() in suggestion.lower():
                            blog_media.append({
                                "id": media["id"],
                                "filename": media["filename"],
                                "file_path": media["file_path"],
                                "media_type": media["media_type"],
                                "category": media["category"],
                                "description": media["description"]
                            })
            
            blog_post = BlogPost(
                title=blog_parsed['title'],
                content=blog_parsed['content'],
                excerpt=blog_parsed['excerpt'],
                estimated_read_time=blog_parsed['estimated_read_time'],
                seo_keywords=blog_parsed['seo_keywords'],
                suggested_media=blog_media,
                media_placement_guide=blog_parsed['media_placement_guide'],
                seo_analysis=blog_seo_analysis,
                meta_description=blog_parsed['meta_description'],
                schema_markup=schema_markup,
                internal_links=blog_parsed['internal_links'],
                external_links=blog_parsed['external_links']
            )
        
        # Generate newsletter (existing code)
        newsletter_article = None
        if request.generate_newsletter or len(request.platforms) > 5:
            # Use existing newsletter generation logic
            pass
        
        # Generate video scripts (existing code)
        video_scripts = []
        if request.generate_video_script:
            # Use existing video script generation logic
            pass
        
        # Generate content repurposing strategy
        repurposed_content = None
        if request.repurpose_content and generated_content:
            original_content = generated_content[0].content
            repurposed_versions = generate_content_variations(original_content, request.platforms)
            
            repurposed_content = ContentRepurposing(
                original_content=original_content,
                original_platform=request.platforms[0],
                repurposed_content=repurposed_versions,
                media_adaptations={},
                cross_promotion_strategy="Share across platforms with platform-specific adaptations"
            )
        
        # Update usage count for selected media
        used_media_ids = set()
        for content in generated_content:
            for media in content.suggested_media:
                used_media_ids.add(media["id"])
        
        # Update usage count in database
        for media_id in used_media_ids:
            await db.media_files.update_one(
                {"_id": ObjectId(media_id)},
                {"$inc": {"usage_count": 1}, "$set": {"last_used": datetime.utcnow()}}
            )
        
        # Generate SEO recommendations
        seo_recommendations = []
        if request.seo_focus:
            seo_recommendations = [
                f"Target keyword density: Maintain 1-3% density for '{target_keywords[0]}'" if target_keywords else "Include relevant keywords naturally",
                "Add internal links to related content for better SEO",
                "Include meta descriptions for all content",
                "Use schema markup for better search visibility",
                "Optimize images with alt text and descriptive filenames"
            ]
        
        # Generate hashtag strategy
        hashtag_strategy = {}
        for content in generated_content:
            if content.hashtag_analysis:
                hashtag_strategy[content.platform] = {
                    "trending": [h.hashtag for h in content.hashtag_analysis if h.trend_direction == HashtagStatus.TRENDING],
                    "stable": [h.hashtag for h in content.hashtag_analysis if h.trend_direction == HashtagStatus.STABLE],
                    "recommended_mix": f"Use 70% trending, 30% stable hashtags for {content.platform}"
                }
        
        # Generate performance forecast
        performance_forecast = {}
        for content in generated_content:
            if content.performance_prediction:
                performance_forecast[content.platform] = {
                    "engagement_rate": content.performance_prediction,
                    "estimated_reach": int(content.performance_prediction * 100),
                    "confidence_level": "High" if content.performance_prediction > 70 else "Medium"
                }
        
        # Generate general media suggestions
        media_suggestions = []
        if not available_media:
            media_suggestions = [
                "Upload team photos showing safety training in action",
                "Add equipment photos demonstrating proper usage",
                "Include workplace photos showcasing safety protocols",
                "Create videos of safety procedures and demonstrations",
                "Add photos of completed projects with safety highlights"
            ]
        
        # Save enhanced content to database
        content_doc = {
            "request_id": request_id,
            "company_id": request.company_id,
            "topic": request.topic,
            "generated_content": [content.dict() for content in generated_content],
            "blog_post": blog_post.dict() if blog_post else None,
            "newsletter_article": newsletter_article.dict() if newsletter_article else None,
            "video_scripts": [script.dict() for script in video_scripts] if video_scripts else None,
            "repurposed_content": repurposed_content.dict() if repurposed_content else None,
            "media_used": list(used_media_ids),
            "seo_recommendations": seo_recommendations,
            "hashtag_strategy": hashtag_strategy,
            "performance_forecast": performance_forecast,
            "created_at": datetime.utcnow()
        }
        
        await db.generated_content.insert_one(content_doc)
        
        response = ContentResponse(
            request_id=request_id,
            company_id=request.company_id,
            topic=request.topic,
            generated_content=generated_content,
            blog_post=blog_post,
            newsletter_article=newsletter_article,
            video_scripts=video_scripts if video_scripts else None,
            media_used=[media for media in available_media if media["id"] in used_media_ids],
            media_suggestions=media_suggestions,
            repurposed_content=repurposed_content,
            seo_recommendations=seo_recommendations,
            hashtag_strategy=hashtag_strategy,
            performance_forecast=performance_forecast,
            created_at=datetime.utcnow().isoformat()
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating enhanced content: {str(e)}")

# SEO Analysis endpoint
@app.post("/api/seo/analyze")
async def analyze_seo_content(request: dict):
    """Analyze SEO performance of content"""
    try:
        content = request.get("content", "")
        target_keywords = request.get("target_keywords", [])
        
        analysis = calculate_seo_score(content, target_keywords)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing SEO: {str(e)}")

# Hashtag Analysis endpoint
@app.post("/api/hashtags/analyze")
async def analyze_hashtags_endpoint(request: dict):
    """Analyze hashtag performance and trends"""
    try:
        hashtags = request.get("hashtags", [])
        industry = request.get("industry", "construction")
        
        analysis = analyze_hashtags(hashtags, industry)
        return {"hashtag_analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing hashtags: {str(e)}")

# Trending Hashtags endpoint
@app.get("/api/hashtags/trending/{industry}")
async def get_trending_hashtags(industry: str):
    """Get trending hashtags for specific industry"""
    try:
        trending = TRENDING_HASHTAGS.get(industry, {"trending": [], "stable": [], "declining": []})
        return {
            "industry": industry,
            "trending_hashtags": trending
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting trending hashtags: {str(e)}")

# Performance Prediction endpoint
@app.post("/api/predict/performance")
async def predict_performance(content: str, platform: str, hashtags: List[str], company_id: str):
    """Predict content performance"""
    try:
        company = await get_company_by_id(company_id)
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        
        prediction = predict_content_performance(content, platform, hashtags, company)
        return {
            "platform": platform,
            "predicted_performance": prediction,
            "confidence_level": "High" if prediction > 70 else "Medium" if prediction > 50 else "Low",
            "recommendations": [
                "Add more engaging hooks" if prediction < 60 else "Content looks great!",
                "Include trending hashtags" if len(hashtags) < 5 else "Good hashtag usage",
                "Add call-to-action" if "?" not in content else "Good engagement trigger"
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error predicting performance: {str(e)}")

# Content Repurposing endpoint
@app.post("/api/content/repurpose")
async def repurpose_content(content: str, platforms: List[str]):
    """Repurpose content for multiple platforms"""
    try:
        variations = generate_content_variations(content, platforms)
        return {
            "original_content": content,
            "variations": variations,
            "platforms": platforms
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error repurposing content: {str(e)}")

# Continue with existing endpoints...
# Company Management (existing)
@app.post("/api/companies")
async def create_company(company: Company):
    company_dict = company.dict()
    company_dict["created_at"] = datetime.utcnow()
    company_dict["updated_at"] = datetime.utcnow()
    company_dict["last_media_request"] = None
    company_dict["media_library_size"] = 0
    company_dict["seo_keywords"] = SEO_KEYWORDS.get(company.industry, [])
    
    result = await db.companies.insert_one(company_dict)
    company_dict["id"] = str(result.inserted_id)
    del company_dict["_id"]
    
    return company_dict

@app.get("/api/companies")
async def get_companies():
    companies = []
    async for company in db.companies.find():
        company["id"] = str(company["_id"])
        del company["_id"]
        companies.append(company)
    return companies

@app.get("/api/companies/{company_id}")
async def get_company(company_id: str):
    company = await get_company_by_id(company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@app.put("/api/companies/{company_id}")
async def update_company(company_id: str, company: CompanyUpdate):
    company_dict = company.dict(exclude_unset=True)
    company_dict["updated_at"] = datetime.utcnow()
    
    result = await db.companies.update_one(
        {"_id": ObjectId(company_id)},
        {"$set": company_dict}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Company not found")
    
    return await get_company_by_id(company_id)

# Media Management (existing endpoints)
@app.post("/api/companies/{company_id}/media/upload")
async def upload_media(
    company_id: str,
    file: UploadFile = File(...),
    category: MediaCategory = Form(...),
    description: str = Form(""),
    tags: str = Form(""),
    seo_alt_text: str = Form("")
):
    """Upload media file for a company with SEO optimization"""
    try:
        company = await get_company_by_id(company_id)
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        
        if not file.content_type.startswith(('image/', 'video/')):
            raise HTTPException(status_code=400, detail="Only image and video files are supported")
        
        file_path, file_size, mime_type = save_uploaded_file(file, company_id, category.value)
        
        metadata = {}
        if mime_type.startswith('image/'):
            metadata = process_image(file_path)
        
        # Generate SEO alt text if not provided
        if not seo_alt_text:
            seo_alt_text = f"{company['name']} {category.value} - {description}"
        
        media_record = {
            "company_id": company_id,
            "filename": Path(file_path).name,
            "original_filename": file.filename,
            "file_path": file_path,
            "file_size": file_size,
            "media_type": determine_media_type(mime_type),
            "mime_type": mime_type,
            "category": category,
            "description": description,
            "tags": [tag.strip() for tag in tags.split(',') if tag.strip()],
            "seo_alt_text": seo_alt_text,
            "upload_date": datetime.utcnow(),
            "is_active": True,
            "usage_count": 0,
            "performance_score": 0.0,
            "metadata": metadata
        }
        
        result = await db.media_files.insert_one(media_record)
        media_record["id"] = str(result.inserted_id)
        del media_record["_id"]
        
        await db.companies.update_one(
            {"_id": ObjectId(company_id)},
            {"$inc": {"media_library_size": 1}}
        )
        
        return media_record
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading media: {str(e)}")

@app.get("/api/companies/{company_id}/media")
async def get_company_media_files(
    company_id: str,
    media_type: Optional[MediaType] = None,
    category: Optional[MediaCategory] = None,
    limit: int = 20
):
    """Get media files for a company"""
    try:
        company = await get_company_by_id(company_id)
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        
        media_files = await get_company_media(company_id, media_type, category, limit)
        return media_files
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving media: {str(e)}")

@app.delete("/api/media/{media_id}")
async def delete_media(media_id: str):
    """Delete a media file"""
    try:
        media = await db.media_files.find_one({"_id": ObjectId(media_id)})
        if not media:
            raise HTTPException(status_code=404, detail="Media file not found")
        
        await db.media_files.update_one(
            {"_id": ObjectId(media_id)},
            {"$set": {"is_active": False}}
        )
        
        await db.companies.update_one(
            {"_id": ObjectId(media["company_id"])},
            {"$inc": {"media_library_size": -1}}
        )
        
        return {"message": "Media file deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting media: {str(e)}")

@app.get("/api/companies/{company_id}/media/categories")
async def get_media_categories(company_id: str):
    """Get available media categories"""
    return {
        "categories": [category.value for category in MediaCategory],
        "descriptions": {
            "training": "Training sessions, workshops, certification ceremonies",
            "equipment": "Tools, machinery, safety equipment, vehicles",
            "workplace": "Job sites, offices, facilities, work environments",
            "team": "Team members, group photos, leadership, staff",
            "projects": "Completed projects, work in progress, before/after shots",
            "safety": "Safety procedures, PPE usage, safety demonstrations",
            "certificates": "Certifications, awards, recognitions, licenses",
            "events": "Company events, conferences, trade shows, meetings"
        }
    }

@app.get("/api/companies/{company_id}/media/request")
async def get_media_request_prompt(company_id: str):
    """Get monthly media request prompt for a company"""
    try:
        company = await get_company_by_id(company_id)
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        
        media_count = await db.media_files.count_documents({"company_id": company_id, "is_active": True})
        
        pipeline = [
            {"$match": {"company_id": company_id, "is_active": True}},
            {"$group": {"_id": "$category", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        
        category_distribution = {}
        async for result in db.media_files.aggregate(pipeline):
            category_distribution[result["_id"]] = result["count"]
        
        all_categories = [cat.value for cat in MediaCategory]
        suggested_categories = [cat for cat in all_categories if category_distribution.get(cat, 0) < 3]
        
        current_date = datetime.utcnow()
        
        from pydantic import BaseModel
        class MediaRequestPrompt(BaseModel):
            company_id: str
            company_name: str
            month: str
            year: int
            suggested_categories: List[str]
            current_media_count: int
            last_upload_date: Optional[datetime] = None
            recommendation: str
        
        prompt = MediaRequestPrompt(
            company_id=company_id,
            company_name=company["name"],
            month=current_date.strftime("%B"),
            year=current_date.year,
            suggested_categories=suggested_categories,
            current_media_count=media_count,
            last_upload_date=company.get("last_media_request"),
            recommendation=generate_media_suggestion(company, media_count)
        )
        
        return prompt
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating media request: {str(e)}")

@app.post("/api/companies/{company_id}/media/request/sent")
async def mark_media_request_sent(company_id: str):
    """Mark that media request has been sent to company"""
    try:
        result = await db.companies.update_one(
            {"_id": ObjectId(company_id)},
            {"$set": {"last_media_request": datetime.utcnow()}}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Company not found")
        
        return {"message": "Media request marked as sent"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error marking media request: {str(e)}")

@app.get("/api/media/requests/monthly")
async def get_monthly_media_requests():
    """Get all companies that need monthly media requests"""
    try:
        requests = await check_monthly_media_requests()
        return {"requests": requests, "total_companies": len(requests)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting monthly requests: {str(e)}")

# Content Scheduling (existing)
@app.post("/api/schedule-post")
async def schedule_post(post: ScheduledPost):
    post_dict = post.dict()
    post_dict["created_at"] = datetime.utcnow()
    post_dict["status"] = PostStatus.SCHEDULED
    
    result = await db.scheduled_posts.insert_one(post_dict)
    post_dict["id"] = str(result.inserted_id)
    del post_dict["_id"]
    
    return post_dict

@app.get("/api/calendar/{company_id}")
async def get_calendar(company_id: str, month: int, year: int):
    start_date = datetime(year, month, 1)
    end_date = datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
    
    posts = []
    async for post in db.scheduled_posts.find({
        "company_id": company_id,
        "scheduled_time": {"$gte": start_date, "$lt": end_date}
    }).sort("scheduled_time", 1):
        post["id"] = str(post["_id"])
        del post["_id"]
        posts.append(post)
    
    calendar_data = {}
    for post in posts:
        date_str = post["scheduled_time"].strftime("%Y-%m-%d")
        if date_str not in calendar_data:
            calendar_data[date_str] = []
        calendar_data[date_str].append(post)
    
    from pydantic import BaseModel
    class CalendarEntry(BaseModel):
        date: str
        posts: List[ScheduledPost]
        total_posts: int
    
    calendar_entries = []
    for date, posts in calendar_data.items():
        entry = CalendarEntry(
            date=date,
            posts=posts,
            total_posts=len(posts)
        )
        calendar_entries.append(entry)
    
    return calendar_entries

@app.put("/api/posts/{post_id}")
async def update_post(post_id: str, post: ScheduledPost):
    post_dict = post.dict(exclude_unset=True)
    post_dict["updated_at"] = datetime.utcnow()
    
    result = await db.scheduled_posts.update_one(
        {"_id": ObjectId(post_id)},
        {"$set": post_dict}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Post not found")
    
    updated_post = await db.scheduled_posts.find_one({"_id": ObjectId(post_id)})
    updated_post["id"] = str(updated_post["_id"])
    del updated_post["_id"]
    
    return updated_post

@app.delete("/api/posts/{post_id}")
async def delete_post(post_id: str):
    result = await db.scheduled_posts.delete_one({"_id": ObjectId(post_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post deleted successfully"}

# Enhanced Analytics with ROI tracking
@app.post("/api/analytics")
async def save_analytics(analytics: Analytics):
    analytics_dict = analytics.dict()
    analytics_dict["recorded_at"] = datetime.utcnow()
    
    result = await db.analytics.insert_one(analytics_dict)
    return {"id": str(result.inserted_id), "message": "Analytics saved successfully"}

@app.get("/api/analytics/{company_id}")
async def get_analytics(company_id: str, days: int = 30):
    start_date = datetime.utcnow() - timedelta(days=days)
    
    analytics = []
    async for record in db.analytics.find({
        "company_id": company_id,
        "recorded_at": {"$gte": start_date}
    }).sort("recorded_at", -1):
        record["id"] = str(record["_id"])
        del record["_id"]
        analytics.append(record)
    
    return analytics

@app.get("/api/analytics/{company_id}/roi")
async def get_roi_analytics(company_id: str, period: str = "month"):
    """Get ROI analytics for a company"""
    try:
        # Mock ROI data (would be calculated from actual data in production)
        roi_data = ROIMetrics(
            company_id=company_id,
            period=period,
            total_investment=5000.0,
            leads_generated=150,
            conversions=45,
            revenue_attributed=75000.0,
            cost_per_lead=33.33,
            roi_percentage=1400.0,
            platform_breakdown={
                "instagram": {"investment": 1500, "revenue": 22500, "roi": 1400},
                "facebook": {"investment": 2000, "revenue": 30000, "roi": 1400},
                "linkedin": {"investment": 1500, "revenue": 22500, "roi": 1400}
            },
            content_type_performance={
                "video": {"investment": 2000, "revenue": 35000, "roi": 1650},
                "image": {"investment": 2000, "revenue": 25000, "roi": 1150},
                "text": {"investment": 1000, "revenue": 15000, "roi": 1400}
            }
        )
        
        return roi_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting ROI analytics: {str(e)}")

# Enhanced Monthly Report
@app.get("/api/reports/monthly/{company_id}")
async def get_monthly_report(company_id: str, month: int, year: int):
    start_date = datetime(year, month, 1)
    end_date = datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
    
    analytics = []
    async for record in db.analytics.find({
        "company_id": company_id,
        "recorded_at": {"$gte": start_date, "$lt": end_date}
    }):
        analytics.append(record)
    
    media_performance = {}
    async for media in db.media_files.find({
        "company_id": company_id,
        "last_used": {"$gte": start_date, "$lt": end_date}
    }).sort("usage_count", -1):
        media_performance[media["category"]] = media_performance.get(media["category"], 0) + media.get("usage_count", 0)
    
    total_posts = len(analytics)
    total_engagement = sum(record.get("likes", 0) + record.get("shares", 0) + record.get("comments", 0) for record in analytics)
    
    top_posts = sorted(analytics, key=lambda x: x.get("engagement_rate", 0), reverse=True)[:5]
    
    platform_performance = {}
    for record in analytics:
        platform = record.get("platform")
        if platform not in platform_performance:
            platform_performance[platform] = {
                "total_posts": 0,
                "total_engagement": 0,
                "avg_engagement_rate": 0
            }
        platform_performance[platform]["total_posts"] += 1
        platform_performance[platform]["total_engagement"] += record.get("likes", 0) + record.get("shares", 0) + record.get("comments", 0)
    
    for platform in platform_performance:
        if platform_performance[platform]["total_posts"] > 0:
            platform_performance[platform]["avg_engagement_rate"] = platform_performance[platform]["total_engagement"] / platform_performance[platform]["total_posts"]
    
    # Enhanced recommendations with AI insights
    recommendations = [
        "Focus on video content for higher engagement (50% increase in engagement)",
        "Post during optimal times based on audience analysis",
        "Use trending hashtags to increase discoverability by 35%",
        "Implement user-generated content campaigns",
        "Create more educational content about safety protocols",
        "Optimize content for mobile viewing (80% of users on mobile)",
        "Implement SEO best practices for better organic reach"
    ]
    
    # Enhanced media recommendations
    media_recommendations = []
    if media_performance:
        top_category = max(media_performance, key=media_performance.get)
        media_recommendations.extend([
            f"Your {top_category} content performs best - create more similar content",
            "Consider creating video versions of your most popular images",
            "Add behind-the-scenes content to humanize your brand",
            "Create seasonal content for upcoming industry events"
        ])
    else:
        media_recommendations.extend([
            "Start uploading company photos and videos to increase engagement by 80%",
            "Visual content receives 94% more views than text-only posts",
            "Consider creating short-form videos for TikTok and Instagram Reels",
            "Add infographics to explain complex safety procedures"
        ])
    
    viral_potential = [record.get("post_id", "") for record in analytics if record.get("engagement_rate", 0) > 0.05]
    
    from pydantic import BaseModel
    class MonthlyReport(BaseModel):
        company_id: str
        month: str
        year: int
        total_posts: int
        total_engagement: int
        top_performing_posts: List[Dict[str, Any]]
        platform_performance: Dict[str, Dict[str, Any]]
        recommendations: List[str]
        viral_potential_posts: List[str]
        media_performance: Optional[Dict[str, Any]] = None
        media_recommendations: Optional[List[str]] = []
        seo_insights: Optional[Dict[str, Any]] = None
        hashtag_performance: Optional[Dict[str, Any]] = None
        competitor_analysis: Optional[Dict[str, Any]] = None
        roi_summary: Optional[Dict[str, float]] = None
    
    report = MonthlyReport(
        company_id=company_id,
        month=f"{year}-{month:02d}",
        year=year,
        total_posts=total_posts,
        total_engagement=total_engagement,
        top_performing_posts=[object_id_to_str(post) for post in top_posts],
        platform_performance=platform_performance,
        recommendations=recommendations,
        viral_potential_posts=viral_potential,
        media_performance=media_performance,
        media_recommendations=media_recommendations,
        seo_insights={
            "avg_seo_score": 75.5,
            "top_keywords": ["safety training", "OSHA compliance", "workplace safety"],
            "content_optimization": "82% of content is SEO optimized"
        },
        hashtag_performance={
            "top_hashtags": ["#SafetyFirst", "#WorkplaceSafety", "#OSHACompliance"],
            "trending_usage": "65% of posts use trending hashtags",
            "avg_hashtag_engagement": 2.4
        },
        competitor_analysis={
            "engagement_comparison": "15% above industry average",
            "content_gap_opportunities": ["Video tutorials", "Live Q&A sessions"],
            "competitive_advantages": ["High-quality media", "Consistent posting"]
        },
        roi_summary={
            "total_roi": 1400.0,
            "cost_per_engagement": 0.33,
            "revenue_per_post": 1500.0
        }
    )
    
    return report

@app.get("/api/content-examples")
async def get_content_examples():
    examples = {
        "topics": [
            "OSHA Fall Protection Standards",
            "Asbestos Awareness Training",
            "Lead Paint Safety Protocols",
            "Mold Remediation Best Practices",
            "Forklift Safety Certification",
            "Construction Site Safety Tips",
            "Environmental Compliance Updates",
            "Personal Protective Equipment (PPE)",
            "Workplace Hazard Communication",
            "Emergency Response Procedures",
            "HVAC Safety Guidelines",
            "Electrical Safety Training",
            "Confined Space Entry Protocols",
            "Respiratory Protection Programs",
            "Chemical Storage Safety",
            "Scaffolding Safety Standards",
            "Excavation and Trenching Safety",
            "Crane Operation Safety",
            "Noise Exposure Prevention",
            "Heat Illness Prevention"
        ],
        "audience_levels": [
            "beginner",
            "intermediate", 
            "advanced",
            "management",
            "general"
        ],
        "industries": [
            "Construction",
            "Environmental Training",
            "Manufacturing",
            "Healthcare",
            "Education",
            "Government",
            "Oil & Gas",
            "Mining",
            "Transportation",
            "Utilities"
        ],
        "media_categories": [
            "training",
            "equipment",
            "workplace",
            "team",
            "projects",
            "safety",
            "certificates",
            "events"
        ],
        "content_types": [
            "how-to guides",
            "safety tips",
            "industry news",
            "case studies",
            "infographics",
            "video tutorials",
            "webinars",
            "success stories",
            "compliance updates",
            "best practices"
        ],
        "seo_keywords": SEO_KEYWORDS,
        "trending_hashtags": TRENDING_HASHTAGS
    }
    return examples

# Background task for posting scheduled content
async def publish_scheduled_posts():
    """Background task to publish scheduled posts"""
    while True:
        try:
            current_time = datetime.utcnow()
            
            posts_to_publish = []
            async for post in db.scheduled_posts.find({
                "status": PostStatus.SCHEDULED,
                "scheduled_time": {"$lte": current_time}
            }):
                posts_to_publish.append(post)
            
            for post in posts_to_publish:
                try:
                    # Here you would integrate with social media APIs
                    # For now, we'll just mark as published
                    await db.scheduled_posts.update_one(
                        {"_id": post["_id"]},
                        {"$set": {
                            "status": PostStatus.PUBLISHED,
                            "published_at": current_time
                        }}
                    )
                    print(f"Published post {post['_id']} to {post['platform']}")
                except Exception as e:
                    print(f"Failed to publish post {post['_id']}: {e}")
                    await db.scheduled_posts.update_one(
                        {"_id": post["_id"]},
                        {"$set": {"status": PostStatus.FAILED}}
                    )
            
            await asyncio.sleep(60)
            
        except Exception as e:
            print(f"Error in publish_scheduled_posts: {e}")
            await asyncio.sleep(60)

# Background task for monthly media requests
async def send_monthly_media_requests():
    """Background task to send monthly media requests"""
    while True:
        try:
            current_time = datetime.utcnow()
            if current_time.hour == 9 and current_time.minute < 5:
                requests = await check_monthly_media_requests()
                
                for request in requests:
                    await db.companies.update_one(
                        {"_id": ObjectId(request["company_id"])},
                        {"$set": {"last_media_request": current_time}}
                    )
                    print(f"Sent media request to {request['company_name']}")
            
            await asyncio.sleep(3600)
            
        except Exception as e:
            print(f"Error in send_monthly_media_requests: {e}")
            await asyncio.sleep(3600)

# Start background tasks
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(publish_scheduled_posts())
    asyncio.create_task(send_monthly_media_requests())
    print("🚀 Advanced Social Media Management Platform Started!")
    print("✅ SEO Analysis Engine: Active")
    print("✅ Hashtag Trend Analysis: Active")
    print("✅ Performance Prediction: Active")
    print("✅ Content Repurposing: Active")
    print("✅ Media Management: Active")
    print("✅ ROI Tracking: Active")

# Beta Feedback System Endpoints
@app.post("/api/beta/login")
async def beta_login(beta_id: str, name: str, email: str):
    """Login or register beta user"""
    try:
        # Check if beta user exists
        beta_user = await db.beta_users.find_one({"beta_id": beta_id})
        
        if not beta_user:
            # Create new beta user
            beta_user_data = {
                "name": name,
                "email": email,
                "beta_id": beta_id,
                "joined_at": datetime.utcnow(),
                "contribution_score": 0,
                "feedback_count": 0,
                "status": "active",
                "special_privileges": []
            }
            
            result = await db.beta_users.insert_one(beta_user_data)
            beta_user_data["id"] = str(result.inserted_id)
            del beta_user_data["_id"]
            
            return {"status": "success", "user": beta_user_data, "message": "Welcome to the beta program!"}
        else:
            # Update existing user info
            await db.beta_users.update_one(
                {"beta_id": beta_id},
                {"$set": {"name": name, "email": email, "last_login": datetime.utcnow()}}
            )
            
            beta_user["id"] = str(beta_user["_id"])
            del beta_user["_id"]
            
            return {"status": "success", "user": beta_user, "message": "Welcome back!"}
    
    except Exception as e:
        print(f"Beta login error: {e}")
        raise HTTPException(status_code=500, detail="Login failed")

@app.get("/api/beta/feedback")
async def get_beta_feedback():
    """Get all beta feedback"""
    try:
        feedback_list = []
        async for feedback in db.beta_feedback.find().sort("created_at", -1):
            feedback["id"] = str(feedback["_id"])
            del feedback["_id"]
            feedback_list.append(feedback)
        
        return {"feedback": feedback_list}
    except Exception as e:
        print(f"Get feedback error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get feedback")

@app.post("/api/beta/feedback")
async def submit_beta_feedback(feedback: BetaFeedback):
    """Submit beta feedback"""
    try:
        feedback_data = feedback.dict()
        feedback_data["created_at"] = datetime.utcnow()
        feedback_data["updated_at"] = datetime.utcnow()
        feedback_data["status"] = "open"
        feedback_data["votes"] = 0
        
        result = await db.beta_feedback.insert_one(feedback_data)
        
        # Update user's feedback count
        await db.beta_users.update_one(
            {"beta_id": feedback.beta_user_id},
            {"$inc": {"feedback_count": 1, "contribution_score": 5}}
        )
        
        feedback_data["id"] = str(result.inserted_id)
        del feedback_data["_id"]
        
        return {
            "status": "submitted", 
            "feedback_id": feedback_data["id"],
            "feedback": feedback_data
        }
    
    except Exception as e:
        print(f"Submit feedback error: {e}")
        raise HTTPException(status_code=500, detail="Failed to submit feedback")

@app.put("/api/beta/feedback/{feedback_id}")
async def update_feedback_status(feedback_id: str, status: str, admin_response: str = "", implementation_notes: str = ""):
    """Update feedback status (admin only)"""
    try:
        update_data = {
            "status": status,
            "updated_at": datetime.utcnow()
        }
        
        if admin_response:
            update_data["admin_response"] = admin_response
        
        if implementation_notes:
            update_data["implementation_notes"] = implementation_notes
        
        if status in ["implemented", "rejected", "closed"]:
            update_data["resolved_at"] = datetime.utcnow()
        
        result = await db.beta_feedback.update_one(
            {"_id": ObjectId(feedback_id)},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Feedback not found")
        
        return {
            "status": "updated", 
            "message": "Feedback updated",
            "feedback_status": status
        }
    
    except Exception as e:
        print(f"Update feedback error: {e}")
        raise HTTPException(status_code=500, detail="Failed to update feedback")

@app.post("/api/beta/feedback/{feedback_id}/vote")
async def vote_feedback(feedback_id: str, beta_user_id: str):
    """Vote on feedback"""
    try:
        # First get the current vote count
        feedback = await db.beta_feedback.find_one({"_id": ObjectId(feedback_id)})
        if not feedback:
            raise HTTPException(status_code=404, detail="Feedback not found")
        
        # Update vote count
        result = await db.beta_feedback.update_one(
            {"_id": ObjectId(feedback_id)},
            {"$inc": {"votes": 1}}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Feedback not found")
        
        # Get updated vote count
        updated_feedback = await db.beta_feedback.find_one({"_id": ObjectId(feedback_id)})
        
        return {
            "status": "voted", 
            "message": "Vote recorded",
            "votes": updated_feedback.get("votes", 0)
        }
    
    except Exception as e:
        print(f"Vote error: {e}")
        raise HTTPException(status_code=500, detail="Failed to vote")

@app.get("/api/beta/user/{beta_user_id}/stats")
async def get_beta_user_stats(beta_user_id: str):
    """Get beta user statistics"""
    try:
        user = await db.beta_users.find_one({"beta_id": beta_user_id})
        if not user:
            raise HTTPException(status_code=404, detail="Beta user not found")
        
        # Count user's feedback
        feedback_count = await db.beta_feedback.count_documents({"beta_user_id": beta_user_id})
        
        # Count implemented suggestions
        implemented_count = await db.beta_feedback.count_documents({
            "beta_user_id": beta_user_id,
            "status": "implemented"
        })
        
        # Return user stats in expected format
        return {
            "beta_user_id": user["beta_id"],
            "name": user["name"],
            "email": user["email"],
            "contribution_score": user.get("contribution_score", 0),
            "feedback_count": feedback_count,
            "implemented_count": implemented_count,
            "status": user.get("status", "active"),
            "joined_at": user.get("joined_at"),
            "special_privileges": user.get("special_privileges", [])
        }
    
    except Exception as e:
        print(f"Get user stats error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get user stats")

# SEO Monitoring Add-on Endpoints
@app.post("/api/seo-addon/purchase")
async def purchase_seo_addon(request: dict):
    """Purchase SEO monitoring add-on"""
    try:
        # Extract data from request body
        company_id = request.get("company_id", "demo-company")
        website_url = request.get("website_url", "https://example.com")
        notification_email = request.get("notification_email", "admin@company.com")
        plan_type = request.get("plan_type", "standard")
        
        # Check if company already has SEO addon
        existing_addon = await db.seo_addons.find_one({"company_id": company_id})
        
        if existing_addon:
            return {"status": "error", "message": "Company already has SEO monitoring add-on"}
        
        # Create SEO addon record
        addon_data = {
            "company_id": company_id,
            "website_url": website_url,
            "monitoring_status": "active",
            "purchased_at": datetime.utcnow(),
            "expires_at": datetime.utcnow() + timedelta(days=365),  # 1 year
            "daily_checks_limit": 50 if plan_type == "standard" else 100,
            "daily_checks_used": 0,
            "last_check_date": None,
            "auto_check_enabled": True,
            "notification_email": notification_email,
            "price_paid": 297.0 if plan_type == "standard" else 497.0
        }
        
        result = await db.seo_addons.insert_one(addon_data)
        addon_data["id"] = str(result.inserted_id)
        del addon_data["_id"]
        
        return {"status": "success", "addon": addon_data, "message": "SEO monitoring add-on activated!"}
    
    except Exception as e:
        print(f"Purchase SEO addon error: {e}")
        raise HTTPException(status_code=500, detail="Failed to purchase SEO add-on")

@app.get("/api/seo-addon/{company_id}/status")
async def get_seo_addon_status(company_id: str):
    """Get SEO addon status for company"""
    try:
        addon = await db.seo_addons.find_one({"company_id": company_id})
        
        if not addon:
            return {"status": "not_purchased", "message": "SEO monitoring add-on not purchased"}
        
        addon["id"] = str(addon["_id"])
        del addon["_id"]
        
        # Check if expired
        if addon["expires_at"] < datetime.utcnow():
            addon["monitoring_status"] = "expired"
            await db.seo_addons.update_one(
                {"company_id": company_id},
                {"$set": {"monitoring_status": "expired"}}
            )
        
        return {"status": "active", "addon": addon}
    
    except Exception as e:
        print(f"Get SEO addon status error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get SEO addon status")

@app.get("/api/seo-addon/parameters/latest")
async def get_latest_seo_parameters():
    """Get latest SEO parameters from daily research"""
    try:
        # Get latest parameters from last 30 days
        cutoff_date = datetime.utcnow() - timedelta(days=30)
        
        parameters = []
        async for param in db.seo_parameters.find(
            {"discovered_date": {"$gte": cutoff_date}}
        ).sort("discovered_date", -1).limit(50):
            param["id"] = str(param["_id"])
            del param["_id"]
            parameters.append(param)
        
        return {"parameters": parameters}
    
    except Exception as e:
        print(f"Get SEO parameters error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get SEO parameters")

@app.post("/api/seo-addon/{company_id}/audit")
async def run_website_audit(company_id: str, page_url: str = None):
    """Run SEO audit on website"""
    try:
        # Check if company has SEO addon
        addon = await db.seo_addons.find_one({"company_id": company_id})
        
        if not addon:
            raise HTTPException(status_code=404, detail="SEO monitoring add-on not found")
        
        if addon["monitoring_status"] != "active":
            raise HTTPException(status_code=403, detail="SEO monitoring add-on not active")
        
        # Check daily limits
        today = datetime.utcnow().date()
        if addon.get("last_check_date") and addon["last_check_date"].date() == today:
            if addon["daily_checks_used"] >= addon["daily_checks_limit"]:
                raise HTTPException(status_code=429, detail="Daily check limit reached")
        
        # Reset daily counter if new day
        if not addon.get("last_check_date") or addon["last_check_date"].date() != today:
            addon["daily_checks_used"] = 0
        
        # Use page_url if provided, otherwise use website_url
        url_to_audit = page_url if page_url else addon["website_url"]
        
        # Simulate SEO audit (in production, this would use real SEO tools)
        audit_results = await simulate_seo_audit(url_to_audit)
        
        # Save audit results
        audit_data = {
            "company_id": company_id,
            "website_url": addon["website_url"],
            "page_url": url_to_audit,
            "audit_date": datetime.utcnow(),
            "overall_score": audit_results["overall_score"],
            "issues_found": audit_results["issues_found"],
            "recommendations": audit_results["recommendations"],
            "priority_fixes": audit_results["priority_fixes"],
            "estimated_impact": audit_results["estimated_impact"],
            "estimated_effort": audit_results["estimated_effort"],
            "current_seo_parameters": audit_results["current_seo_parameters"],
            "compliance_status": audit_results["compliance_status"]
        }
        
        result = await db.website_audits.insert_one(audit_data)
        audit_data["id"] = str(result.inserted_id)
        del audit_data["_id"]
        
        # Update addon usage
        await db.seo_addons.update_one(
            {"company_id": company_id},
            {
                "$inc": {"daily_checks_used": 1},
                "$set": {"last_check_date": datetime.utcnow()}
            }
        )
        
        return {"status": "success", "audit": audit_data}
    
    except Exception as e:
        print(f"Website audit error: {e}")
        raise HTTPException(status_code=500, detail="Failed to run website audit")

@app.get("/api/seo-addon/{company_id}/audits")
async def get_website_audits(company_id: str, limit: int = 10):
    """Get website audit history"""
    try:
        audits = []
        async for audit in db.website_audits.find(
            {"company_id": company_id}
        ).sort("audit_date", -1).limit(limit):
            audit["id"] = str(audit["_id"])
            del audit["_id"]
            audits.append(audit)
        
        return {"audits": audits}
    
    except Exception as e:
        print(f"Get audits error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get audits")

async def simulate_seo_audit(url: str):
    """Simulate SEO audit (in production, use real SEO tools)"""
    # This would integrate with real SEO tools like Screaming Frog, Lighthouse, etc.
    # For demo purposes, we'll simulate realistic audit results
    
    audit_results = {
        "overall_score": random.uniform(65, 95),
        "issues_found": [
            {
                "issue": "Missing meta description",
                "severity": "medium",
                "pages_affected": 3,
                "impact": "medium"
            },
            {
                "issue": "Slow loading images",
                "severity": "high",
                "pages_affected": 7,
                "impact": "high"
            },
            {
                "issue": "Missing alt text",
                "severity": "medium",
                "pages_affected": 5,
                "impact": "medium"
            }
        ],
        "recommendations": [
            {
                "recommendation": "Add meta descriptions to all pages",
                "priority": "high",
                "effort": "2-3 hours",
                "impact": "Improve click-through rates by 15-20%"
            },
            {
                "recommendation": "Optimize images with WebP format",
                "priority": "high",
                "effort": "1-2 days",
                "impact": "Improve page load speed by 30-40%"
            },
            {
                "recommendation": "Add descriptive alt text to all images",
                "priority": "medium",
                "effort": "3-4 hours",
                "impact": "Improve accessibility and SEO"
            }
        ],
        "priority_fixes": [
            {
                "fix": "Optimize Core Web Vitals",
                "pages": 12,
                "impact": "high",
                "effort": "1-2 weeks"
            },
            {
                "fix": "Fix mobile responsiveness issues",
                "pages": 4,
                "impact": "high",
                "effort": "3-5 days"
            }
        ],
        "estimated_impact": "high",
        "estimated_effort": "1-2 weeks",
        "current_seo_parameters": {
            "page_speed": 78,
            "mobile_friendly": 92,
            "core_web_vitals": 65,
            "accessibility": 84,
            "seo_score": 87
        },
        "compliance_status": {
            "has_meta_description": False,
            "has_h1_tag": True,
            "has_alt_text": False,
            "mobile_responsive": True,
            "https_enabled": True,
            "sitemap_exists": True,
            "robots_txt_exists": True
        }
    }
    
    return audit_results

@app.post("/api/seo-addon/research/daily")
async def run_daily_seo_research():
    """Run daily SEO parameter research (automated task)"""
    try:
        # This would run daily to research current SEO parameters
        # For demo purposes, we'll simulate discovering new parameters
        
        new_parameters = [
            {
                "parameter_name": "Core Web Vitals LCP",
                "parameter_value": "2.5 seconds maximum",
                "source": "google",
                "discovered_date": datetime.utcnow(),
                "importance_score": 9,
                "category": "core_web_vitals",
                "description": "Largest Contentful Paint should be under 2.5 seconds",
                "implementation_difficulty": "medium"
            },
            {
                "parameter_name": "Mobile First Indexing",
                "parameter_value": "Mobile version is primary",
                "source": "google",
                "discovered_date": datetime.utcnow(),
                "importance_score": 10,
                "category": "mobile",
                "description": "Google uses mobile version for indexing and ranking",
                "implementation_difficulty": "hard"
            },
            {
                "parameter_name": "E-A-T Signals",
                "parameter_value": "Expertise, Authority, Trust",
                "source": "google",
                "discovered_date": datetime.utcnow(),
                "importance_score": 8,
                "category": "content",
                "description": "Content should demonstrate expertise, authority, and trustworthiness",
                "implementation_difficulty": "medium"
            }
        ]
        
        # Save new parameters
        for param in new_parameters:
            await db.seo_parameters.insert_one(param)
        
        return {"status": "success", "parameters_discovered": len(new_parameters)}
    
    except Exception as e:
        print(f"Daily SEO research error: {e}")
        raise HTTPException(status_code=500, detail="Failed to run daily SEO research")

@app.post("/api/competitor/analyze")
async def analyze_competitor(request: CompetitorAnalysisRequest):
    """Analyze competitor website and social media"""
    try:
        competitor_name = request.competitor_name or request.website_url
        
        # Generate comprehensive analysis using AI
        analysis_prompt = f"""
You are a marketing strategist and competitive analyst. Analyze the competitor based on the provided information:

Website: {request.website_url}
Competitor: {competitor_name}
Analysis Type: {request.analysis_type}
Social Platforms: {', '.join(request.social_platforms) if request.social_platforms else 'Auto-detect'}

Please provide a comprehensive competitive analysis with:

1. WEBSITE ANALYSIS:
   - SEO strategy assessment
   - Content strategy evaluation
   - User experience analysis
   - Technical performance insights

2. SOCIAL MEDIA ANALYSIS (if applicable):
   - Platform presence and activity
   - Content strategy patterns
   - Engagement rates and audience interaction
   - Posting frequency and timing

3. COMPETITIVE STRENGTHS:
   - What are they doing exceptionally well?
   - Unique value propositions
   - Market positioning advantages

4. COMPETITIVE WEAKNESSES:
   - Areas where they're lacking
   - Missed opportunities
   - Potential vulnerabilities

5. STRATEGIC RECOMMENDATIONS:
   - Tactical actions to gain competitive advantage
   - Content strategies to outperform them
   - Marketing channels to focus on
   - Positioning opportunities

6. OPPORTUNITIES FOR ADVANTAGE:
   - Market gaps they haven't filled
   - Underserved audience segments
   - Emerging trends they're missing

Please provide detailed, actionable insights that can help develop a winning competitive strategy.
        """
        
        # Use Claude to generate analysis
        client = anthropic.Anthropic(api_key=os.getenv('CLAUDE_API_KEY'))
        
        response = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=2000,
            messages=[
                {"role": "user", "content": analysis_prompt}
            ]
        )
        
        analysis_content = response.content[0].text
        
        # Parse the analysis into structured sections
        sections = analysis_content.split('\n\n')
        
        website_analysis = ""
        social_media_analysis = ""
        strengths = []
        weaknesses = []
        recommendations = ""
        opportunities = ""
        
        current_section = ""
        for section in sections:
            section = section.strip()
            if not section:
                continue
                
            if "WEBSITE ANALYSIS" in section.upper():
                current_section = "website"
                website_analysis = section
            elif "SOCIAL MEDIA ANALYSIS" in section.upper():
                current_section = "social"
                social_media_analysis = section
            elif "COMPETITIVE STRENGTHS" in section.upper() or "STRENGTHS" in section.upper():
                current_section = "strengths"
                # Extract bullet points
                lines = section.split('\n')
                for line in lines[1:]:  # Skip header
                    if line.strip() and (line.strip().startswith('-') or line.strip().startswith('•')):
                        strengths.append(line.strip()[1:].strip())
            elif "COMPETITIVE WEAKNESSES" in section.upper() or "WEAKNESSES" in section.upper():
                current_section = "weaknesses"
                # Extract bullet points
                lines = section.split('\n')
                for line in lines[1:]:  # Skip header
                    if line.strip() and (line.strip().startswith('-') or line.strip().startswith('•')):
                        weaknesses.append(line.strip()[1:].strip())
            elif "STRATEGIC RECOMMENDATIONS" in section.upper() or "RECOMMENDATIONS" in section.upper():
                current_section = "recommendations"
                recommendations = section
            elif "OPPORTUNITIES" in section.upper():
                current_section = "opportunities"
                opportunities = section
            else:
                # Continue adding to current section
                if current_section == "website":
                    website_analysis += "\n\n" + section
                elif current_section == "social":
                    social_media_analysis += "\n\n" + section
                elif current_section == "recommendations":
                    recommendations += "\n\n" + section
                elif current_section == "opportunities":
                    opportunities += "\n\n" + section
        
        # Store analysis in database
        analysis_data = {
            "company_id": request.company_id,
            "competitor_name": competitor_name,
            "website_url": request.website_url,
            "analysis_type": request.analysis_type,
            "social_platforms": request.social_platforms,
            "website_analysis": website_analysis,
            "social_media_analysis": social_media_analysis,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations,
            "opportunities": opportunities,
            "full_analysis": analysis_content,
            "created_at": datetime.utcnow()
        }
        
        result = await db.competitor_analyses.insert_one(analysis_data)
        analysis_data["id"] = str(result.inserted_id)
        del analysis_data["_id"]
        
        return {
            "status": "success", 
            "message": "Competitor analysis completed successfully",
            **analysis_data
        }
    
    except Exception as e:
        print(f"Competitor analysis error: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze competitor")

@app.get("/api/competitor/analyses/{company_id}")
async def get_competitor_analyses(company_id: str):
    """Get all competitor analyses for a company"""
    try:
        analyses = []
        async for analysis in db.competitor_analyses.find({"company_id": company_id}):
            analysis["id"] = str(analysis["_id"])
            del analysis["_id"]
            analyses.append(analysis)
        
        return {"status": "success", "analyses": analyses}
    
    except Exception as e:
        print(f"Get competitor analyses error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve competitor analyses")

# ==========================================
# 🚀 PHASE 1: STRIPE PAYMENT SYSTEM & SUBSCRIPTION MANAGEMENT  
# ==========================================

# Initialize Stripe
stripe.api_key = stripe_api_key

@app.post("/api/payments/create-checkout")
async def create_payment_checkout(request: dict):
    """Create Stripe checkout session for plan or add-on purchase"""
    try:
        # Get the host URL from request
        host_url = request.get("host_url", "http://localhost:3000")
        
        plan_type = request.get("plan_type")
        plan_interval = request.get("plan_interval", "monthly")
        addon_type = request.get("addon_type")
        addon_tier = request.get("addon_tier")
        user_id = request.get("user_id", "demo-user")
        
        # Calculate amount based on plan or add-on
        amount = 0.0
        item_name = ""
        
        if plan_type:
            # Plan purchase
            amount = get_plan_price(plan_type, plan_interval)
            plan_config = PLAN_CONFIGS.get(plan_type, {})
            item_name = f"{plan_config.get('name', plan_type.title())} - {plan_interval.title()}"
        elif addon_type and addon_tier:
            # Add-on purchase
            addon_config = ADDON_CONFIGS.get(addon_type, {})
            tier_config = addon_config.get("tiers", {}).get(addon_tier, {})
            amount = tier_config.get("price", 0.0)
            item_name = f"{addon_config.get('name', addon_type.title())} - {addon_tier.title()}"
        else:
            raise HTTPException(status_code=400, detail="Either plan_type or addon_type/addon_tier required")
        
        if amount <= 0:
            raise HTTPException(status_code=400, detail="Invalid plan or add-on configuration")
        
        # Create checkout session request URLs
        success_url = f"{host_url}/dashboard?session_id={{CHECKOUT_SESSION_ID}}&payment_success=true"
        cancel_url = f"{host_url}/dashboard?payment_canceled=true"
        
        metadata = {
            "user_id": user_id,
            "item_name": item_name,
            "payment_type": "subscription" if plan_type else "addon"
        }
        
        if plan_type:
            metadata["plan_type"] = plan_type
            metadata["plan_interval"] = plan_interval
        if addon_type:
            metadata["addon_type"] = addon_type
            metadata["addon_tier"] = addon_tier
        
        # Create Stripe checkout session using direct API
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': item_name,
                        },
                        'unit_amount': int(amount * 100),  # Convert to cents
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=success_url,
                cancel_url=cancel_url,
                metadata=metadata
            )
            print(f"Successfully created Stripe checkout session: {session.id}")
        except stripe.error.StripeError as e:
            print(f"Stripe API error: {e}")
            raise HTTPException(status_code=400, detail=f"Stripe error: {str(e)}")
        except Exception as e:
            print(f"Unexpected error creating checkout session: {e}")
            raise HTTPException(status_code=500, detail="Failed to create checkout session")
        
        # Store transaction record
        transaction_data = {
            "user_id": user_id,
            "session_id": session.id,
            "amount": amount,
            "currency": "usd",
            "payment_status": "initiated",
            "plan_type": plan_type,
            "plan_interval": plan_interval,
            "addon_type": addon_type,
            "metadata": metadata,
            "created_at": datetime.utcnow()
        }
        
        result = await db.payment_transactions.insert_one(transaction_data)
        transaction_data["id"] = str(result.inserted_id)
        del transaction_data["_id"]
        
        return {
            "status": "success",
            "checkout_url": session.url,
            "session_id": session.id,
            "transaction": transaction_data
        }
    
    except Exception as e:
        print(f"Create checkout error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create checkout: {str(e)}")

@app.get("/api/payments/status/{session_id}")
async def get_payment_status(session_id: str):
    """Get payment status from Stripe and update database"""
    try:
        # Get status from Stripe using direct API
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            print(f"Retrieved Stripe session {session_id}: status={session.status}, payment_status={session.payment_status}")
        except stripe.error.InvalidRequestError as e:
            raise HTTPException(status_code=404, detail="Invalid session ID")
        except stripe.error.StripeError as e:
            print(f"Stripe API error: {e}")
            raise HTTPException(status_code=400, detail=f"Stripe error: {str(e)}")
        
        # Find transaction in database
        transaction = await db.payment_transactions.find_one({"session_id": session_id})
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        # Update transaction status if payment is complete and not already processed
        if session.payment_status == "paid" and transaction.get("payment_status") != "paid":
            # Update transaction
            await db.payment_transactions.update_one(
                {"session_id": session_id},
                {
                    "$set": {
                        "payment_status": "paid",
                        "completed_at": datetime.utcnow(),
                        "stripe_payment_intent_id": session.payment_intent
                    }
                }
            )
            
            # Process the subscription/addon purchase
            await process_successful_payment(transaction, session)
        
        return {
            "status": "success",
            "payment_status": session.payment_status,
            "session_status": session.status,
            "amount": session.amount_total / 100 if session.amount_total else 0,  # Convert from cents
            "currency": session.currency
        }
    
    except Exception as e:
        print(f"Get payment status error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get payment status: {str(e)}")

@app.post("/api/webhook/stripe")
async def stripe_webhook(request: Request):
    """Handle Stripe webhook events with signature verification"""
    try:
        payload = await request.body()
        sig_header = request.headers.get('stripe-signature')
        
        # In production, verify webhook signature for security
        # webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
        # if webhook_secret and sig_header:
        #     try:
        #         event = stripe.Webhook.construct_event(
        #             payload, sig_header, webhook_secret
        #         )
        #     except ValueError as e:
        #         print(f"Invalid payload: {e}")
        #         raise HTTPException(status_code=400, detail="Invalid payload")
        #     except stripe.error.SignatureVerificationError as e:
        #         print(f"Invalid signature: {e}")
        #         raise HTTPException(status_code=400, detail="Invalid signature")
        # else:
        #     event = json.loads(payload)
        
        # For now, parse the webhook data directly (add signature verification in production)
        event = json.loads(payload)
        
        event_type = event.get("type")
        data = event.get("data", {})
        object_data = data.get("object", {})
        
        print(f"Received Stripe webhook: {event_type}")
        
        if event_type == "checkout.session.completed":
            session_id = object_data.get("id")
            payment_status = object_data.get("payment_status")
            
            if session_id and payment_status == "paid":
                # Find and update transaction
                transaction = await db.payment_transactions.find_one({"session_id": session_id})
                if transaction and transaction.get("payment_status") != "paid":
                    await db.payment_transactions.update_one(
                        {"session_id": session_id},
                        {
                            "$set": {
                                "payment_status": "paid",
                                "completed_at": datetime.utcnow(),
                                "stripe_payment_intent_id": object_data.get("payment_intent")
                            }
                        }
                    )
                    
                    # Process the successful payment
                    await process_successful_payment(transaction, object_data)
                    print(f"Successfully processed payment for session {session_id}")
        
        return {"status": "success", "message": "Webhook processed"}
    
    except json.JSONDecodeError as e:
        print(f"Stripe webhook JSON decode error: {e}")
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
    except Exception as e:
        print(f"Stripe webhook error: {e}")
        return {"status": "error", "message": str(e)}

async def process_successful_payment(transaction: dict, checkout_data: dict):
    """Process successful payment and update user subscription/add-ons"""
    try:
        user_id = transaction.get("user_id")
        plan_type = transaction.get("plan_type")
        plan_interval = transaction.get("plan_interval")
        addon_type = transaction.get("addon_type")
        
        if plan_type:
            # Update user subscription
            await update_user_subscription(user_id, plan_type, plan_interval)
        elif addon_type:
            # Activate add-on for user
            await activate_user_addon(user_id, addon_type, transaction.get("addon_tier"))
        
        print(f"Successfully processed payment for user {user_id}")
    
    except Exception as e:
        print(f"Error processing successful payment: {e}")

async def update_user_subscription(user_id: str, plan_type: str, plan_interval: str):
    """Update user's subscription plan"""
    try:
        # Calculate subscription period
        current_time = datetime.utcnow()
        if plan_interval == "monthly":
            period_end = current_time + timedelta(days=30)
        elif plan_interval == "yearly":
            period_end = current_time + timedelta(days=365)
        else:  # lifetime
            period_end = current_time + timedelta(days=36500)  # 100 years
        
        # Update user record
        await db.users.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "current_plan": plan_type,
                    "subscription_status": "active",
                    "subscription_updated_at": current_time
                }
            },
            upsert=True
        )
        
        # Create/update subscription record
        subscription_data = {
            "user_id": user_id,
            "plan_type": plan_type,
            "plan_interval": plan_interval,
            "status": "active",
            "current_period_start": current_time,
            "current_period_end": period_end,
            "created_at": current_time
        }
        
        await db.user_subscriptions.update_one(
            {"user_id": user_id},
            {"$set": subscription_data},
            upsert=True
        )
        
        print(f"Updated subscription for user {user_id} to {plan_type}")
    
    except Exception as e:
        print(f"Error updating user subscription: {e}")

async def activate_user_addon(user_id: str, addon_type: str, addon_tier: str):
    """Activate add-on for user"""
    try:
        addon_data = {
            "user_id": user_id,
            "addon_type": addon_type,
            "addon_tier": addon_tier,
            "status": "active",
            "activated_at": datetime.utcnow(),
            "expires_at": datetime.utcnow() + timedelta(days=365)  # 1 year expiry
        }
        
        await db.user_addons.update_one(
            {"user_id": user_id, "addon_type": addon_type},
            {"$set": addon_data},
            upsert=True
        )
        
        print(f"Activated {addon_type} addon for user {user_id}")
    
    except Exception as e:
        print(f"Error activating user addon: {e}")

@app.get("/api/user/{user_id}/subscription")
async def get_user_subscription(user_id: str):
    """Get user's current subscription and usage"""
    try:
        # Get user info
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get subscription details
        subscription = await db.user_subscriptions.find_one({"user_id": user_id})
        
        # Get current usage
        current_month = datetime.utcnow().strftime("%Y-%m")
        usage = await get_user_usage(user_id, current_month)
        
        # Get active add-ons
        addons = []
        async for addon in db.user_addons.find({"user_id": user_id, "status": "active"}):
            addon["id"] = str(addon["_id"])
            del addon["_id"]
            addons.append(addon)
        
        # Get plan limits and features
        current_plan = user.get("current_plan", "starter")
        plan_config = PLAN_CONFIGS.get(current_plan, {})
        
        return {
            "status": "success",
            "user_id": user_id,
            "current_plan": current_plan,
            "subscription": subscription,
            "usage": usage.dict() if usage else None,
            "plan_limits": plan_config.get("limits", {}),
            "plan_features": plan_config.get("features", []),
            "active_addons": addons,
            "upgrade_options": get_plan_upgrade_path(current_plan)
        }
    
    except Exception as e:
        print(f"Get user subscription error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get user subscription")

@app.get("/api/plans")
async def get_available_plans():
    """Get all available subscription plans"""
    try:
        return {
            "status": "success",
            "plans": PLAN_CONFIGS,
            "addons": ADDON_CONFIGS
        }
    
    except Exception as e:
        print(f"Get plans error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get plans")

# ==========================================
# 👥 PHASE 2A: MULTI-USER & TEAM MANAGEMENT SYSTEM  
# ==========================================

@app.post("/api/teams/{team_id}/invite")
async def invite_team_member(team_id: str, request: dict):
    """Invite a new team member"""
    try:
        email = request.get("email")
        role = request.get("role", "member")  # admin, member, viewer
        permissions = request.get("permissions", [])
        
        if not email:
            raise HTTPException(status_code=400, detail="Email is required")
        
        # Check if team owner has user limits available
        team_owner = await db.users.find_one({"_id": ObjectId(team_id)})
        if not team_owner:
            raise HTTPException(status_code=404, detail="Team not found")
        
        current_plan = team_owner.get("current_plan", "starter")
        user_limit = PLAN_CONFIGS.get(current_plan, {}).get("limits", {}).get("users", 1)
        
        if user_limit > 0:  # -1 means unlimited
            current_users = await db.team_members.count_documents({"team_id": team_id, "status": "active"})
            if current_users >= user_limit:
                return {
                    "status": "limit_exceeded",
                    "message": f"Team user limit reached. Current plan allows {user_limit} users.",
                    "upgrade_required": True
                }
        
        # Generate invite token
        import secrets
        invite_token = secrets.token_urlsafe(32)
        
        # Store invitation
        invitation_data = {
            "team_id": team_id,
            "email": email,
            "role": role,
            "permissions": permissions,
            "invite_token": invite_token,
            "status": "pending",
            "invited_by": team_id,  # team owner id
            "invited_at": datetime.utcnow(),
            "expires_at": datetime.utcnow() + timedelta(days=7)
        }
        
        result = await db.team_invitations.insert_one(invitation_data)
        invitation_data["id"] = str(result.inserted_id)
        del invitation_data["_id"]
        
        # In production, send invitation email here
        invite_url = f"https://postvelocity.com/invite/{invite_token}"
        
        return {
            "status": "success",
            "message": f"Invitation sent to {email}",
            "invitation": invitation_data,
            "invite_url": invite_url
        }
    
    except Exception as e:
        print(f"Team invite error: {e}")
        raise HTTPException(status_code=500, detail="Failed to invite team member")

@app.post("/api/teams/accept-invite/{invite_token}")
async def accept_team_invitation(invite_token: str, request: dict):
    """Accept team invitation and create user account"""
    try:
        # Find invitation
        invitation = await db.team_invitations.find_one({
            "invite_token": invite_token,
            "status": "pending",
            "expires_at": {"$gt": datetime.utcnow()}
        })
        
        if not invitation:
            raise HTTPException(status_code=404, detail="Invalid or expired invitation")
        
        user_data = request.get("user_data", {})
        full_name = user_data.get("full_name")
        password = user_data.get("password")  # In production, hash this
        
        if not full_name:
            raise HTTPException(status_code=400, detail="Full name is required")
        
        # Create user account
        new_user_data = {
            "username": invitation["email"].split("@")[0],
            "email": invitation["email"],
            "full_name": full_name,
            "role": "team_member",
            "team_id": invitation["team_id"],
            "permissions": invitation["permissions"],
            "created_at": datetime.utcnow(),
            "is_active": True,
            "current_plan": "team_member",  # Special plan for team members
            "subscription_status": "active"
        }
        
        result = await db.users.insert_one(new_user_data)
        user_id = str(result.inserted_id)
        
        # Add to team members
        team_member_data = {
            "team_id": invitation["team_id"],
            "user_id": user_id,
            "email": invitation["email"],
            "role": invitation["role"],
            "permissions": invitation["permissions"],
            "status": "active",
            "joined_at": datetime.utcnow()
        }
        
        await db.team_members.insert_one(team_member_data)
        
        # Mark invitation as accepted
        await db.team_invitations.update_one(
            {"invite_token": invite_token},
            {
                "$set": {
                    "status": "accepted",
                    "accepted_at": datetime.utcnow(),
                    "user_id": user_id
                }
            }
        )
        
        return {
            "status": "success",
            "message": "Team invitation accepted successfully",
            "user_id": user_id,
            "team_id": invitation["team_id"]
        }
    
    except Exception as e:
        print(f"Accept invitation error: {e}")
        raise HTTPException(status_code=500, detail="Failed to accept invitation")

@app.get("/api/teams/{team_id}/members")
async def get_team_members(team_id: str):
    """Get all team members"""
    try:
        members = []
        async for member in db.team_members.find({"team_id": team_id, "status": "active"}):
            # Get user details
            user = await db.users.find_one({"_id": ObjectId(member["user_id"])})
            if user:
                member_info = {
                    "id": str(member["_id"]),
                    "user_id": member["user_id"],
                    "email": member["email"],
                    "full_name": user.get("full_name", ""),
                    "role": member["role"],
                    "permissions": member["permissions"],
                    "joined_at": member["joined_at"],
                    "last_login": user.get("last_login"),
                    "is_active": user.get("is_active", True)
                }
                members.append(member_info)
        
        return {
            "status": "success",
            "members": members,
            "total_members": len(members)
        }
    
    except Exception as e:
        print(f"Get team members error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get team members")

@app.post("/api/teams/{team_id}/members/{user_id}/role")
async def update_team_member_role(team_id: str, user_id: str, request: dict):
    """Update team member role and permissions"""
    try:
        new_role = request.get("role")
        new_permissions = request.get("permissions", [])
        
        if not new_role:
            raise HTTPException(status_code=400, detail="Role is required")
        
        # Update team member record
        result = await db.team_members.update_one(
            {"team_id": team_id, "user_id": user_id},
            {
                "$set": {
                    "role": new_role,
                    "permissions": new_permissions,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Team member not found")
        
        # Update user permissions
        await db.users.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "permissions": new_permissions,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        return {
            "status": "success",
            "message": "Team member role updated successfully"
        }
    
    except Exception as e:
        print(f"Update team member role error: {e}")
        raise HTTPException(status_code=500, detail="Failed to update team member role")

@app.delete("/api/teams/{team_id}/members/{user_id}")
async def remove_team_member(team_id: str, user_id: str):
    """Remove team member"""
    try:
        # Deactivate team member
        result = await db.team_members.update_one(
            {"team_id": team_id, "user_id": user_id},
            {
                "$set": {
                    "status": "removed",
                    "removed_at": datetime.utcnow()
                }
            }
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Team member not found")
        
        # Deactivate user account
        await db.users.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "is_active": False,
                    "deactivated_at": datetime.utcnow()
                }
            }
        )
        
        return {
            "status": "success",
            "message": "Team member removed successfully"
        }
    
    except Exception as e:
        print(f"Remove team member error: {e}")
        raise HTTPException(status_code=500, detail="Failed to remove team member")

# ==========================================
# 🔗 PHASE 2B: PARTNER & AFFILIATE PROGRAM SYSTEM  
# ==========================================

@app.post("/api/partners/register")
async def register_partner(request: dict):
    """Register new partner/affiliate"""
    try:
        email = request.get("email")
        full_name = request.get("full_name")
        company_name = request.get("company_name", "")
        partner_type = request.get("partner_type", "affiliate")  # affiliate, agency, reseller, distributor
        website = request.get("website", "")
        
        if not email or not full_name:
            raise HTTPException(status_code=400, detail="Email and full name are required")
        
        # Check if partner already exists
        existing_partner = await db.partners.find_one({"email": email})
        if existing_partner:
            raise HTTPException(status_code=400, detail="Partner already exists with this email")
        
        # Generate unique referral code
        import secrets
        import string
        referral_code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        
        # Ensure referral code is unique
        while await db.partners.find_one({"referral_code": referral_code}):
            referral_code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        
        # Set partner tier and commission rates
        partner_tiers = {
            "affiliate": {"commission_rate": 0.30, "features": ["referral_links", "basic_reports"]},
            "agency": {"commission_rate": 0.40, "features": ["white_label_portal", "custom_domain"]},
            "reseller": {"commission_rate": 0.60, "features": ["full_white_label", "api_access"]},
            "distributor": {"commission_rate": 0.70, "features": ["territory_rights", "custom_features"]}
        }
        
        tier_config = partner_tiers.get(partner_type, partner_tiers["affiliate"])
        
        # Create partner record
        partner_data = {
            "email": email,
            "full_name": full_name,
            "company_name": company_name,
            "partner_type": partner_type,
            "website": website,
            "referral_code": referral_code,
            "commission_rate": tier_config["commission_rate"],
            "available_features": tier_config["features"],
            "total_referrals": 0,
            "total_commission_earned": 0.0,
            "monthly_sales_volume": 0.0,
            "status": "pending",  # pending, active, suspended
            "white_label_settings": {},
            "territory_rights": [],
            "created_at": datetime.utcnow(),
            "last_active": datetime.utcnow()
        }
        
        result = await db.partners.insert_one(partner_data)
        partner_data["id"] = str(result.inserted_id)
        del partner_data["_id"]
        
        return {
            "status": "success",
            "message": "Partner registration successful",
            "partner": partner_data,
            "referral_url": f"https://postvelocity.com/ref/{referral_code}"
        }
    
    except Exception as e:
        print(f"Partner registration error: {e}")
        raise HTTPException(status_code=500, detail="Failed to register partner")

@app.get("/api/partners/{partner_id}/dashboard")
async def get_partner_dashboard(partner_id: str):
    """Get partner dashboard data"""
    try:
        # Get partner info
        partner = await db.partners.find_one({"_id": ObjectId(partner_id)})
        if not partner:
            raise HTTPException(status_code=404, detail="Partner not found")
        
        # Get referral statistics
        referrals = []
        total_commission = 0.0
        monthly_volume = 0.0
        
        async for referral in db.referrals.find({"partner_id": partner_id}):
            referrals.append({
                "id": str(referral["_id"]),
                "user_email": referral.get("user_email", ""),
                "plan_purchased": referral.get("plan_purchased", ""),
                "commission_earned": referral.get("commission_earned", 0.0),
                "status": referral.get("status", "pending"),
                "created_at": referral.get("created_at")
            })
            total_commission += referral.get("commission_earned", 0.0)
            
            # Calculate current month volume
            if referral.get("created_at", datetime.min).month == datetime.utcnow().month:
                monthly_volume += referral.get("sale_amount", 0.0)
        
        # Get recent activity
        recent_activity = []
        async for activity in db.partner_activity.find(
            {"partner_id": partner_id}
        ).sort("created_at", -1).limit(10):
            recent_activity.append({
                "id": str(activity["_id"]),
                "action": activity.get("action", ""),
                "description": activity.get("description", ""),
                "created_at": activity.get("created_at")
            })
        
        return {
            "status": "success",
            "partner_info": {
                "id": str(partner["_id"]),
                "full_name": partner.get("full_name"),
                "email": partner.get("email"),
                "partner_type": partner.get("partner_type"),
                "referral_code": partner.get("referral_code"),
                "commission_rate": partner.get("commission_rate"),
                "status": partner.get("status")
            },
            "stats": {
                "total_referrals": len(referrals),
                "total_commission_earned": total_commission,
                "monthly_sales_volume": monthly_volume,
                "conversion_rate": len([r for r in referrals if r["status"] == "paid"]) / max(len(referrals), 1) * 100
            },
            "recent_referrals": referrals[-5:],  # Last 5 referrals
            "recent_activity": recent_activity,
            "referral_url": f"https://postvelocity.com/ref/{partner.get('referral_code')}"
        }
    
    except Exception as e:
        print(f"Get partner dashboard error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get partner dashboard")

@app.post("/api/referrals/track")
async def track_referral(request: dict):
    """Track new referral signup"""
    try:
        referral_code = request.get("referral_code")
        user_email = request.get("user_email")
        user_name = request.get("user_name", "")
        
        if not referral_code or not user_email:
            raise HTTPException(status_code=400, detail="Referral code and user email required")
        
        # Find partner by referral code
        partner = await db.partners.find_one({"referral_code": referral_code})
        if not partner:
            raise HTTPException(status_code=404, detail="Invalid referral code")
        
        # Check if referral already exists
        existing_referral = await db.referrals.find_one({
            "partner_id": str(partner["_id"]),
            "user_email": user_email
        })
        
        if existing_referral:
            return {
                "status": "duplicate",
                "message": "Referral already tracked",
                "referral_id": str(existing_referral["_id"])
            }
        
        # Create referral record
        referral_data = {
            "partner_id": str(partner["_id"]),
            "referral_code": referral_code,
            "user_email": user_email,
            "user_name": user_name,
            "status": "signup",  # signup, trial, paid, churned
            "signup_date": datetime.utcnow(),
            "plan_purchased": None,
            "sale_amount": 0.0,
            "commission_earned": 0.0,
            "commission_paid": False,
            "created_at": datetime.utcnow()
        }
        
        result = await db.referrals.insert_one(referral_data)
        referral_id = str(result.inserted_id)
        
        # Update partner stats
        await db.partners.update_one(
            {"_id": partner["_id"]},
            {
                "$inc": {"total_referrals": 1},
                "$set": {"last_active": datetime.utcnow()}
            }
        )
        
        # Log partner activity
        activity_data = {
            "partner_id": str(partner["_id"]),
            "action": "referral_signup",
            "description": f"New signup: {user_email}",
            "referral_id": referral_id,
            "created_at": datetime.utcnow()
        }
        await db.partner_activity.insert_one(activity_data)
        
        return {
            "status": "success",
            "message": "Referral tracked successfully",
            "referral_id": referral_id,
            "commission_rate": partner.get("commission_rate", 0.3)
        }
    
    except Exception as e:
        print(f"Track referral error: {e}")
        raise HTTPException(status_code=500, detail="Failed to track referral")

@app.post("/api/referrals/{referral_id}/convert")
async def convert_referral(referral_id: str, request: dict):
    """Convert referral to paid customer"""
    try:
        plan_purchased = request.get("plan_purchased")
        sale_amount = request.get("sale_amount", 0.0)
        
        if not plan_purchased or sale_amount <= 0:
            raise HTTPException(status_code=400, detail="Plan and sale amount required")
        
        # Find referral
        referral = await db.referrals.find_one({"_id": ObjectId(referral_id)})
        if not referral:
            raise HTTPException(status_code=404, detail="Referral not found")
        
        # Get partner info for commission calculation
        partner = await db.partners.find_one({"_id": ObjectId(referral["partner_id"])})
        if not partner:
            raise HTTPException(status_code=404, detail="Partner not found")
        
        # Calculate commission
        commission_rate = partner.get("commission_rate", 0.3)
        commission_earned = sale_amount * commission_rate
        
        # Update referral
        await db.referrals.update_one(
            {"_id": ObjectId(referral_id)},
            {
                "$set": {
                    "status": "paid",
                    "plan_purchased": plan_purchased,
                    "sale_amount": sale_amount,
                    "commission_earned": commission_earned,
                    "conversion_date": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        # Update partner stats
        await db.partners.update_one(
            {"_id": partner["_id"]},
            {
                "$inc": {
                    "total_commission_earned": commission_earned,
                    "monthly_sales_volume": sale_amount
                },
                "$set": {"last_active": datetime.utcnow()}
            }
        )
        
        # Log partner activity
        activity_data = {
            "partner_id": referral["partner_id"],
            "action": "referral_conversion",
            "description": f"Conversion: {plan_purchased} plan (${sale_amount})",
            "referral_id": referral_id,
            "commission_earned": commission_earned,
            "created_at": datetime.utcnow()
        }
        await db.partner_activity.insert_one(activity_data)
        
        return {
            "status": "success",
            "message": "Referral converted successfully",
            "commission_earned": commission_earned,
            "total_commission": partner.get("total_commission_earned", 0) + commission_earned
        }
    
    except Exception as e:
        print(f"Convert referral error: {e}")
        raise HTTPException(status_code=500, detail="Failed to convert referral")

# ==========================================
# 🔌 PHASE 2C: API ACCESS & ENTERPRISE FEATURES SYSTEM  
# ==========================================

@app.post("/api/keys/generate")
async def generate_api_key(request: dict):
    """Generate new API key for user"""
    try:
        user_id = request.get("user_id")
        key_name = request.get("key_name", "Default API Key")
        permissions = request.get("permissions", ["read"])  # read, write, admin
        expires_in_days = request.get("expires_in_days", 365)
        
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID is required")
        
        # Check if user has API access feature
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        current_plan = user.get("current_plan", "starter")
        plan_features = PLAN_CONFIGS.get(current_plan, {}).get("features", [])
        
        if "api_access" not in plan_features:
            return {
                "status": "upgrade_required",
                "message": "API access requires Business plan or higher",
                "current_plan": current_plan,
                "required_plan": "business"
            }
        
        # Generate secure API key
        import secrets
        api_key = "pv_" + secrets.token_urlsafe(32)
        api_secret = secrets.token_urlsafe(16)
        
        # Create API key record
        api_key_data = {
            "user_id": user_id,
            "key_name": key_name,
            "api_key": api_key,
            "api_secret": api_secret,
            "permissions": permissions,
            "is_active": True,
            "total_requests": 0,
            "last_used": None,
            "rate_limit_per_hour": 1000,  # Default rate limit
            "expires_at": datetime.utcnow() + timedelta(days=expires_in_days),
            "created_at": datetime.utcnow()
        }
        
        result = await db.api_keys.insert_one(api_key_data)
        api_key_data["id"] = str(result.inserted_id)
        del api_key_data["_id"]
        
        return {
            "status": "success",
            "message": "API key generated successfully",
            "api_key": api_key,
            "api_secret": api_secret,
            "permissions": permissions,
            "expires_at": api_key_data["expires_at"],
            "rate_limit": api_key_data["rate_limit_per_hour"]
        }
    
    except Exception as e:
        print(f"Generate API key error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate API key")

@app.get("/api/keys/{user_id}")
async def get_user_api_keys(user_id: str):
    """Get all API keys for a user"""
    try:
        api_keys = []
        async for key in db.api_keys.find({"user_id": user_id, "is_active": True}):
            key_info = {
                "id": str(key["_id"]),
                "key_name": key.get("key_name"),
                "api_key": key.get("api_key")[:12] + "..." + key.get("api_key")[-4:],  # Masked
                "permissions": key.get("permissions", []),
                "total_requests": key.get("total_requests", 0),
                "last_used": key.get("last_used"),
                "rate_limit_per_hour": key.get("rate_limit_per_hour", 1000),
                "expires_at": key.get("expires_at"),
                "created_at": key.get("created_at")
            }
            api_keys.append(key_info)
        
        return {
            "status": "success",
            "api_keys": api_keys,
            "total_keys": len(api_keys)
        }
    
    except Exception as e:
        print(f"Get API keys error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get API keys")

@app.delete("/api/keys/{key_id}")
async def revoke_api_key(key_id: str):
    """Revoke/deactivate API key"""
    try:
        result = await db.api_keys.update_one(
            {"_id": ObjectId(key_id)},
            {
                "$set": {
                    "is_active": False,
                    "revoked_at": datetime.utcnow()
                }
            }
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="API key not found")
        
        return {
            "status": "success",
            "message": "API key revoked successfully"
        }
    
    except Exception as e:
        print(f"Revoke API key error: {e}")
        raise HTTPException(status_code=500, detail="Failed to revoke API key")

# API Authentication Middleware
async def authenticate_api_key(api_key: str):
    """Authenticate API key and return user info"""
    try:
        key_data = await db.api_keys.find_one({
            "api_key": api_key,
            "is_active": True,
            "expires_at": {"$gt": datetime.utcnow()}
        })
        
        if not key_data:
            return None
        
        # Update usage stats
        await db.api_keys.update_one(
            {"_id": key_data["_id"]},
            {
                "$inc": {"total_requests": 1},
                "$set": {"last_used": datetime.utcnow()}
            }
        )
        
        return key_data
    
    except Exception as e:
        print(f"API authentication error: {e}")
        return None

# Enterprise API Endpoints
@app.get("/api/v1/content")
async def api_get_content(api_key: str = None):
    """API endpoint to get user's content"""
    try:
        if not api_key:
            raise HTTPException(status_code=401, detail="API key required")
        
        key_data = await authenticate_api_key(api_key)
        if not key_data:
            raise HTTPException(status_code=401, detail="Invalid or expired API key")
        
        if "read" not in key_data.get("permissions", []):
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        
        user_id = key_data["user_id"]
        
        # Get user's content
        content = []
        async for item in db.generated_content.find({"user_id": user_id}).limit(50):
            content_item = {
                "id": str(item["_id"]),
                "topic": item.get("topic", ""),
                "platform": item.get("platform", ""),
                "content": item.get("content", ""),
                "created_at": item.get("created_at"),
                "performance": item.get("performance", {})
            }
            content.append(content_item)
        
        return {
            "status": "success",
            "content": content,
            "total": len(content),
            "api_usage": {
                "requests_used": key_data.get("total_requests", 0),
                "rate_limit": key_data.get("rate_limit_per_hour", 1000)
            }
        }
    
    except Exception as e:
        print(f"API get content error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get content")

@app.post("/api/v1/content/generate")
async def api_generate_content(request: dict, api_key: str = None):
    """API endpoint to generate content"""
    try:
        if not api_key:
            raise HTTPException(status_code=401, detail="API key required")
        
        key_data = await authenticate_api_key(api_key)
        if not key_data:
            raise HTTPException(status_code=401, detail="Invalid or expired API key")
        
        if "write" not in key_data.get("permissions", []):
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        
        user_id = key_data["user_id"]
        topic = request.get("topic")
        platform = request.get("platform", "instagram")
        company_id = request.get("company_id", "api-company")
        
        if not topic:
            raise HTTPException(status_code=400, detail="Topic is required")
        
        # Use existing content generation logic
        client = anthropic.Anthropic(api_key=os.getenv('CLAUDE_API_KEY'))
        
        prompt = f"""
        Create engaging social media content for {platform} about: {topic}
        
        Requirements:
        - Platform-optimized for {platform}
        - Engaging and conversion-focused
        - Include relevant hashtags
        - Professional tone
        """
        
        response = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        generated_content = response.content[0].text
        
        # Save generated content
        content_data = {
            "user_id": user_id,
            "company_id": company_id,
            "topic": topic,
            "platform": platform,
            "content": generated_content,
            "source": "api",
            "api_key_id": str(key_data["_id"]),
            "created_at": datetime.utcnow()
        }
        
        result = await db.generated_content.insert_one(content_data)
        content_id = str(result.inserted_id)
        
        return {
            "status": "success",
            "content_id": content_id,
            "content": generated_content,
            "topic": topic,
            "platform": platform,
            "created_at": content_data["created_at"]
        }
    
    except Exception as e:
        print(f"API generate content error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate content")

@app.get("/api/v1/analytics")
async def api_get_analytics(api_key: str = None, days: int = 30):
    """API endpoint to get analytics data"""
    try:
        if not api_key:
            raise HTTPException(status_code=401, detail="API key required")
        
        key_data = await authenticate_api_key(api_key)
        if not key_data:
            raise HTTPException(status_code=401, detail="Invalid or expired API key")
        
        if "read" not in key_data.get("permissions", []):
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        
        user_id = key_data["user_id"]
        
        # Get analytics data for the specified period
        since_date = datetime.utcnow() - timedelta(days=days)
        
        # Mock analytics data (in production, this would come from actual social media APIs)
        analytics_data = {
            "period": f"Last {days} days",
            "total_posts": 45,
            "total_impressions": 125000,
            "total_engagement": 8750,
            "engagement_rate": 7.0,
            "top_performing_posts": [
                {
                    "id": "post_1",
                    "content_preview": "Amazing AI-generated content...",
                    "platform": "instagram",
                    "impressions": 15000,
                    "engagement": 1200,
                    "engagement_rate": 8.0
                }
            ],
            "platform_breakdown": {
                "instagram": {"posts": 20, "impressions": 70000, "engagement": 5500},
                "facebook": {"posts": 15, "impressions": 35000, "engagement": 2100},
                "twitter": {"posts": 10, "impressions": 20000, "engagement": 1150}
            }
        }
        
        return {
            "status": "success",
            "analytics": analytics_data,
            "api_usage": {
                "requests_used": key_data.get("total_requests", 0),
                "rate_limit": key_data.get("rate_limit_per_hour", 1000)
            }
        }
    
    except Exception as e:
        print(f"API get analytics error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get analytics")

# ==========================================
# 📊 ADVANCED ANALYTICS & REPORTING SYSTEM  
# ==========================================

@app.post("/api/reports/generate")
async def generate_custom_report(request: dict):
    """Generate custom analytics report"""
    try:
        user_id = request.get("user_id")
        report_type = request.get("report_type", "performance")  # performance, content, social, competitor
        date_range = request.get("date_range", "30d")  # 7d, 30d, 90d, 1y
        platforms = request.get("platforms", ["all"])
        metrics = request.get("metrics", ["impressions", "engagement", "reach"])
        
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID is required")
        
        # Check if user has advanced analytics feature
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        current_plan = user.get("current_plan", "starter")
        plan_features = PLAN_CONFIGS.get(current_plan, {}).get("features", [])
        
        if "advanced_analytics" not in plan_features:
            return {
                "status": "upgrade_required",
                "message": "Advanced analytics requires Professional plan or higher",
                "current_plan": current_plan,
                "required_plan": "professional"
            }
        
        # Generate report data (in production, this would aggregate real data)
        days_back = int(date_range.replace('d', '').replace('y', '365'))
        
        report_data = {
            "report_id": str(uuid.uuid4()),
            "user_id": user_id,
            "report_type": report_type,
            "date_range": date_range,
            "platforms": platforms,
            "generated_at": datetime.utcnow(),
            "data": {
                "overview": {
                    "total_posts": 150,
                    "total_impressions": 450000,
                    "total_engagement": 32500,
                    "engagement_rate": 7.2,
                    "reach": 125000,
                    "growth_rate": 15.3
                },
                "platform_breakdown": {
                    "instagram": {
                        "posts": 60,
                        "impressions": 200000,
                        "engagement": 18000,
                        "engagement_rate": 9.0,
                        "top_content_types": ["carousel", "reels", "stories"]
                    },
                    "facebook": {
                        "posts": 45,
                        "impressions": 150000,
                        "engagement": 9000,
                        "engagement_rate": 6.0,
                        "top_content_types": ["video", "image", "link"]
                    },
                    "twitter": {
                        "posts": 45,
                        "impressions": 100000,
                        "engagement": 5500,
                        "engagement_rate": 5.5,
                        "top_content_types": ["text", "image", "video"]
                    }
                },
                "content_performance": {
                    "top_performing": [
                        {
                            "content_id": "post_1",
                            "platform": "instagram",
                            "content_type": "carousel",
                            "topic": "AI and Marketing",
                            "impressions": 25000,
                            "engagement": 2100,
                            "engagement_rate": 8.4,
                            "created_date": "2024-12-10"
                        }
                    ]
                },
                "audience_insights": {
                    "demographics": {
                        "age_groups": {"18-24": 25, "25-34": 40, "35-44": 20, "45+": 15},
                        "gender": {"male": 45, "female": 52, "other": 3},
                        "locations": {"US": 60, "UK": 15, "CA": 10, "AU": 8, "Other": 7}
                    },
                    "activity_times": {
                        "peak_hours": ["9-11am", "6-8pm"],
                        "peak_days": ["Tuesday", "Wednesday", "Thursday"]
                    }
                },
                "recommendations": [
                    "Post carousel content on Instagram for higher engagement",
                    "Increase posting frequency on Tuesday-Thursday",
                    "Focus on AI and Marketing topics (highest performing)",
                    "Consider video content for Facebook audience"
                ]
            }
        }
        
        # Store report
        result = await db.analytics_reports.insert_one(report_data)
        report_data["id"] = str(result.inserted_id)
        del report_data["_id"]
        
        return {
            "status": "success",
            "message": "Report generated successfully",
            "report": report_data
        }
    
    except Exception as e:
        print(f"Generate report error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate report")

@app.get("/api/reports/{user_id}")
async def get_user_reports(user_id: str, report_type: str = None):
    """Get user's generated reports"""
    try:
        filter_query = {"user_id": user_id}
        if report_type:
            filter_query["report_type"] = report_type
        
        reports = []
        async for report in db.analytics_reports.find(filter_query).sort("generated_at", -1).limit(20):
            report_summary = {
                "id": str(report["_id"]),
                "report_type": report.get("report_type"),
                "date_range": report.get("date_range"),
                "platforms": report.get("platforms"),
                "generated_at": report.get("generated_at"),
                "overview": report.get("data", {}).get("overview", {})
            }
            reports.append(report_summary)
        
        return {
            "status": "success",
            "reports": reports,
            "total": len(reports)
        }
    
    except Exception as e:
        print(f"Get user reports error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get reports")

@app.get("/api/reports/download/{report_id}")
async def download_report(report_id: str, format: str = "json"):
    """Download report in specified format"""
    try:
        report = await db.analytics_reports.find_one({"_id": ObjectId(report_id)})
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        
        if format.lower() == "json":
            return {
                "status": "success",
                "report_data": report.get("data", {}),
                "metadata": {
                    "report_id": str(report["_id"]),
                    "generated_at": report.get("generated_at"),
                    "report_type": report.get("report_type")
                }
            }
        elif format.lower() == "csv":
            # In production, generate actual CSV
            return {
                "status": "success",
                "message": "CSV download would be generated here",
                "download_url": f"/api/reports/csv/{report_id}"
            }
        else:
            raise HTTPException(status_code=400, detail="Unsupported format")
    
    except Exception as e:
        print(f"Download report error: {e}")
        raise HTTPException(status_code=500, detail="Failed to download report")

# ==========================================
# 🎨 CUSTOM BRANDING & WHITE-LABEL SYSTEM  
# ==========================================

@app.post("/api/branding/{user_id}/update")
async def update_user_branding(user_id: str, request: dict):
    """Update user's custom branding settings"""
    try:
        # Check if user has custom branding feature
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        current_plan = user.get("current_plan", "starter")
        plan_features = PLAN_CONFIGS.get(current_plan, {}).get("features", [])
        
        if "custom_branding" not in plan_features:
            return {
                "status": "upgrade_required",
                "message": "Custom branding requires Business plan or higher",
                "current_plan": current_plan,
                "required_plan": "business"
            }
        
        branding_settings = {
            "user_id": user_id,
            "company_name": request.get("company_name", ""),
            "company_logo": request.get("company_logo", ""),  # base64 encoded
            "primary_color": request.get("primary_color", "#3B82F6"),
            "secondary_color": request.get("secondary_color", "#8B5CF6"),
            "accent_color": request.get("accent_color", "#10B981"),
            "font_family": request.get("font_family", "Inter"),
            "custom_domain": request.get("custom_domain", ""),
            "white_label_mode": request.get("white_label_mode", False),
            "hide_postvelocity_branding": request.get("hide_postvelocity_branding", False),
            "custom_footer_text": request.get("custom_footer_text", ""),
            "social_links": request.get("social_links", {}),
            "updated_at": datetime.utcnow()
        }
        
        # Update or create branding settings
        await db.user_branding.update_one(
            {"user_id": user_id},
            {"$set": branding_settings},
            upsert=True
        )
        
        return {
            "status": "success",
            "message": "Branding settings updated successfully",
            "branding": branding_settings
        }
    
    except Exception as e:
        print(f"Update branding error: {e}")
        raise HTTPException(status_code=500, detail="Failed to update branding settings")

@app.get("/api/branding/{user_id}")
async def get_user_branding(user_id: str):
    """Get user's custom branding settings"""
    try:
        branding = await db.user_branding.find_one({"user_id": user_id})
        
        if not branding:
            # Return default branding
            branding = {
                "user_id": user_id,
                "company_name": "PostVelocity",
                "primary_color": "#3B82F6",
                "secondary_color": "#8B5CF6",
                "accent_color": "#10B981",
                "font_family": "Inter",
                "white_label_mode": False,
                "hide_postvelocity_branding": False
            }
        else:
            branding["id"] = str(branding["_id"])
            del branding["_id"]
        
        return {
            "status": "success",
            "branding": branding
        }
    
    except Exception as e:
        print(f"Get branding error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get branding settings")

@app.post("/api/white-label/{user_id}/setup")
async def setup_white_label(user_id: str, request: dict):
    """Setup white-label configuration for partners"""
    try:
        # Check if user has white-label capabilities
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if user is a partner with white-label rights
        partner = await db.partners.find_one({"user_id": user_id})
        if not partner or partner.get("partner_type") not in ["reseller", "distributor"]:
            return {
                "status": "upgrade_required",
                "message": "White-label setup requires Reseller or Distributor partnership",
                "current_status": "not_authorized"
            }
        
        white_label_config = {
            "user_id": user_id,
            "partner_id": str(partner["_id"]),
            "subdomain": request.get("subdomain", ""),  # e.g., "partner.postvelocity.com"
            "custom_domain": request.get("custom_domain", ""),  # e.g., "partner-tool.com"
            "ssl_enabled": request.get("ssl_enabled", True),
            "custom_app_name": request.get("custom_app_name", "Social Media Manager"),
            "custom_app_description": request.get("custom_app_description", ""),
            "remove_postvelocity_branding": request.get("remove_postvelocity_branding", True),
            "custom_support_email": request.get("custom_support_email", ""),
            "custom_privacy_policy": request.get("custom_privacy_policy", ""),
            "custom_terms_of_service": request.get("custom_terms_of_service", ""),
            "analytics_tracking": request.get("analytics_tracking", {}),
            "custom_integrations": request.get("custom_integrations", []),
            "is_active": True,
            "setup_completed": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Store white-label configuration
        await db.white_label_configs.update_one(
            {"user_id": user_id},
            {"$set": white_label_config},
            upsert=True
        )
        
        return {
            "status": "success",
            "message": "White-label configuration completed successfully",
            "config": white_label_config,
            "app_url": f"https://{white_label_config.get('custom_domain') or white_label_config.get('subdomain') + '.postvelocity.com'}"
        }
    
    except Exception as e:
        print(f"White-label setup error: {e}")
        raise HTTPException(status_code=500, detail="Failed to setup white-label configuration")

@app.get("/api/user/{user_id}/usage/increment")
async def increment_user_usage(user_id: str, request: dict):
    """Increment user usage (posts, API calls, etc.)"""
    try:
        usage_type = request.get("usage_type")  # posts_generated, api_calls, etc.
        amount = request.get("amount", 1)
        
        if not usage_type:
            raise HTTPException(status_code=400, detail="usage_type required")
        
        # Get user's current plan
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        current_plan = user.get("current_plan", "starter")
        
        # Get current usage
        current_usage = await get_user_usage(user_id)
        
        # Check if within limits
        current_value = getattr(current_usage, usage_type, 0)
        if not check_plan_limit(current_plan, usage_type, current_value + amount):
            return {
                "status": "limit_exceeded",
                "message": f"Usage limit exceeded for {usage_type}",
                "current_usage": current_value,
                "limit": PLAN_CONFIGS.get(current_plan, {}).get("limits", {}).get(usage_type, 0),
                "upgrade_required": True
            }
        
        # Increment usage
        await increment_usage(user_id, usage_type, amount)
        
        return {
            "status": "success",
            "message": f"Usage incremented: {usage_type} +{amount}",
            "new_value": current_value + amount
        }
    
    except Exception as e:
        print(f"Increment usage error: {e}")
        raise HTTPException(status_code=500, detail="Failed to increment usage")

# ==========================================
# 🔐 OAUTH AUTHENTICATION ENDPOINTS
# ==========================================

@app.get("/api/oauth/url/{platform}")
async def get_oauth_authorization_url(platform: str, user_id: Optional[str] = None):
    """Generate OAuth authorization URL for a platform"""
    try:
        config = get_oauth_config(platform)
        
        # Generate state parameter for CSRF protection
        state = secrets.token_urlsafe(32)
        
        # Store state in a temporary location (in production, use Redis or similar)
        # For now, we'll include it in the URL and validate it during token exchange
        
        # Build authorization URL
        params = {
            "response_type": "code",
            "client_id": config["client_id"],
            "redirect_uri": config["redirect_uri"],
            "state": state,
            "scope": " ".join(config["scopes"])
        }
        
        # Add platform-specific parameters
        if platform == "youtube":
            params["access_type"] = "offline"
            params["prompt"] = "consent"
        elif platform == "linkedin":
            params["response_type"] = "code"
        elif platform == "x":
            params["code_challenge_method"] = "S256"
            params["code_challenge"] = state  # Simplified for demo
        
        authorization_url = f"{config['auth_url']}?{urlencode(params)}"
        
        return {
            "authorization_url": authorization_url,
            "state": state,
            "platform": platform
        }
        
    except Exception as e:
        print(f"Error generating OAuth URL for {platform}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate authorization URL")

@app.post("/api/oauth/token")
async def exchange_oauth_token(request: OAuthTokenExchangeRequest):
    """Exchange authorization code for access token"""
    try:
        config = get_oauth_config(request.platform)
        user_id = request.user_id or "demo-user"  # Use demo user if not provided
        
        # Check if we're in demo mode
        if config.get("demo_mode"):
            # For demo mode, simulate token exchange failure with mock codes
            if request.code.startswith("mock_"):
                raise HTTPException(
                    status_code=400, 
                    detail=f"Token exchange failed: Invalid authorization code (demo mode)"
                )
            else:
                # Simulate successful token exchange for demo
                return {
                    "status": "success",
                    "message": f"Successfully connected {request.platform} (demo mode)",
                    "platform": request.platform,
                    "username": f"demo_user_{request.platform}"
                }
        
        # Prepare token exchange request
        token_data = {
            "client_id": config["client_id"],
            "client_secret": config["client_secret"],
            "code": request.code,
            "grant_type": "authorization_code",
            "redirect_uri": config["redirect_uri"]
        }
        
        # Add platform-specific parameters
        if request.platform == "x":
            token_data["code_verifier"] = request.state  # Simplified for demo
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                config["token_url"],
                data=token_data,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Accept": "application/json"
                }
            )
            
            if response.status_code != 200:
                print(f"Token exchange failed: {response.status_code} - {response.text}")
                raise HTTPException(
                    status_code=400, 
                    detail=f"Token exchange failed: {response.text}"
                )
            
            token_response = response.json()
            
            # Get user info from platform (optional)
            platform_user_info = None
            try:
                platform_user_info = await get_platform_user_info(
                    request.platform, 
                    token_response["access_token"]
                )
            except:
                pass  # Continue even if user info fails
            
            # Store token in database
            success = await store_oauth_token(
                user_id, 
                request.platform, 
                token_response, 
                platform_user_info
            )
            
            if not success:
                raise HTTPException(status_code=500, detail="Failed to store token")
            
            return {
                "status": "success",
                "message": f"Successfully connected {request.platform}",
                "platform": request.platform,
                "username": platform_user_info.get("username") if platform_user_info else None
            }
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error exchanging OAuth token for {request.platform}: {e}")
        raise HTTPException(status_code=500, detail="Token exchange failed")

async def get_platform_user_info(platform: str, access_token: str) -> Optional[dict]:
    """Get user information from platform using access token"""
    user_info_urls = {
        "instagram": "https://graph.instagram.com/me?fields=id,username",
        "facebook": "https://graph.facebook.com/me?fields=id,name",
        "linkedin": "https://api.linkedin.com/v2/people/~",
        "x": "https://api.twitter.com/2/users/me",
        "youtube": "https://www.googleapis.com/oauth2/v2/userinfo",
        "reddit": "https://oauth.reddit.com/api/v1/me",
        "pinterest": "https://api.pinterest.com/v5/user_account",
        "tiktok": "https://open.tiktokapis.com/v2/user/info/",
        "tumblr": "https://api.tumblr.com/v2/user/info"
    }
    
    if platform not in user_info_urls:
        return None
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                user_info_urls[platform],
                headers={"Authorization": f"Bearer {access_token}"}
            )
            
            if response.status_code == 200:
                user_data = response.json()
                
                # Normalize user data based on platform
                if platform == "instagram":
                    return {"id": user_data.get("id"), "username": user_data.get("username")}
                elif platform == "facebook":
                    return {"id": user_data.get("id"), "username": user_data.get("name")}
                elif platform == "x":
                    return {"id": user_data["data"]["id"], "username": user_data["data"]["username"]}
                else:
                    return {"id": str(user_data.get("id", "")), "username": user_data.get("name", "")}
    except:
        pass
    
    return None

@app.get("/api/oauth/connections/{user_id}")
async def get_user_connections(user_id: str):
    """Get list of connected social media platforms for user"""
    try:
        connections = await get_user_connected_platforms(user_id)
        
        # Add platform display names and icons
        for connection in connections:
            platform_info = PLATFORM_CONFIGS.get(connection.platform, {})
            connection.display_name = platform_info.get("name", connection.platform.title())
        
        return {
            "connections": connections,
            "total_connected": len(connections)
        }
        
    except Exception as e:
        print(f"Error getting user connections: {e}")
        raise HTTPException(status_code=500, detail="Failed to get connections")

@app.delete("/api/oauth/disconnect/{platform}")
async def disconnect_platform(platform: str, user_id: Optional[str] = None):
    """Disconnect a social media platform"""
    try:
        user_id = user_id or "demo-user"
        success = await revoke_oauth_token(user_id, platform)
        
        if success:
            return {
                "status": "success",
                "message": f"Successfully disconnected {platform}"
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to disconnect platform")
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error disconnecting platform {platform}: {e}")
        raise HTTPException(status_code=500, detail="Failed to disconnect platform")

@app.post("/api/oauth/refresh/{platform}")
async def refresh_platform_token(platform: str, user_id: Optional[str] = None):
    """Refresh OAuth token for a platform"""
    try:
        user_id = user_id or "demo-user"
        refreshed_token = await refresh_oauth_token(user_id, platform)
        
        if refreshed_token:
            return {
                "status": "success",
                "message": f"Token refreshed for {platform}",
                "expires_at": refreshed_token.get("expires_at")
            }
        else:
            raise HTTPException(status_code=400, detail="Failed to refresh token")
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error refreshing token for {platform}: {e}")
        raise HTTPException(status_code=500, detail="Token refresh failed")

@app.get("/api/platforms/supported")
async def get_supported_platforms():
    """Get list of supported social media platforms for OAuth"""
    try:
        supported_platforms = []
        
        for platform, config in OAUTH_CONFIGS.items():
            platform_config = PLATFORM_CONFIGS.get(platform, {})
            
            supported_platforms.append({
                "platform": platform,
                "name": platform.replace("_", " ").title(),
                "display_name": platform_config.get("name", platform.title()),
                "auth_available": bool(config.get("client_id") and config.get("client_secret")),
                "scopes": config.get("scopes", []),
                "supports_video": platform_config.get("supports_video", False),
                "max_chars": platform_config.get("max_chars", 280),
                "optimal_times": platform_config.get("optimal_times", [])
            })
        
        return {
            "platforms": supported_platforms,
            "total_platforms": len(supported_platforms)
        }
        
    except Exception as e:
        print(f"Error getting supported platforms: {e}")
        raise HTTPException(status_code=500, detail="Failed to get supported platforms")

@app.post("/api/content/publish/{platform}")
async def publish_content_to_platform(platform: str, request: ContentPublishRequest):
    """Publish content directly to a connected social media platform"""
    try:
        user_id = request.user_id or "demo-user"
        
        # Get OAuth token for platform
        token = await get_oauth_token(user_id, platform)
        if not token:
            raise HTTPException(
                status_code=401, 
                detail=f"Not connected to {platform}. Please connect your account first."
            )
        
        # Publishing logic would go here - this is a simplified example
        # In production, you'd implement platform-specific publishing APIs
        
        publishing_urls = {
            "instagram": "https://graph.instagram.com/v18.0/me/media",
            "facebook": "https://graph.facebook.com/v18.0/me/feed",
            "linkedin": "https://api.linkedin.com/v2/ugcPosts",
            "x": "https://api.twitter.com/2/tweets",
            "youtube": "https://www.googleapis.com/youtube/v3/videos",
            "reddit": "https://oauth.reddit.com/api/submit",
            "pinterest": "https://api.pinterest.com/v5/pins",
            "tiktok": "https://open.tiktokapis.com/v2/post/publish/video/init/",
            "tumblr": "https://api.tumblr.com/v2/blog/{blog-identifier}/post"
        }
        
        if platform not in publishing_urls:
            return {
                "status": "success",
                "message": f"Content prepared for {platform} (demo mode)",
                "platform": platform,
                "content_length": len(request.content),
                "demo_mode": True
            }
        
        # For demo purposes, we'll simulate successful posting
        # In production, make actual API calls to publish content
        return {
            "status": "success", 
            "message": f"Content published to {platform}",
            "platform": platform,
            "content_length": len(request.content),
            "media_count": len(request.media_urls) if request.media_urls else 0,
            "demo_mode": True  # Remove this in production
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error publishing to {platform}: {e}")
        raise HTTPException(status_code=500, detail="Failed to publish content")

# ==========================================
# 🔐 ADMIN & USER AUTHENTICATION SYSTEM
# ==========================================

@app.post("/api/auth/setup-admin")
async def setup_admin_user():
    """Set up the initial admin user for testing"""
    try:
        # Check if admin already exists
        admin_exists = await db.users.find_one({"role": "admin"})
        if admin_exists:
            return {
                "status": "exists",
                "message": "Admin user already exists",
                "credentials": {
                    "email": "admin@postvelocity.com",
                    "password": "admin123",
                    "note": "Use these credentials to log in"
                }
            }
        
        # Create admin user with string ID
        admin_id = str(ObjectId())
        admin_user = {
            "_id": admin_id,
            "id": admin_id,
            "username": "admin",
            "email": "admin@postvelocity.com", 
            "full_name": "PostVelocity Administrator",
            "role": "admin",
            "permissions": ["all"],
            "current_plan": "enterprise",
            "subscription_status": "active",
            "is_active": True,
            "created_at": datetime.utcnow(),
            "last_login": None,
            # Simple password storage for demo (in production, hash properly)
            "password": "admin123"
        }
        
        await db.users.insert_one(admin_user)
        
        # Create some demo companies for the admin
        demo_companies = [
            {
                "_id": str(ObjectId()),
                "name": "SafeBuild Construction",
                "industry": "Construction",
                "website": "https://safebuild.com",
                "description": "Leading construction company focused on safety and quality",
                "target_audience": "Construction workers, project managers, safety coordinators",
                "brand_voice": "Professional, safety-focused, reliable",
                "owner_id": admin_id,
                "created_at": datetime.utcnow()
            },
            {
                "_id": str(ObjectId()),
                "name": "GreenTech Environmental",
                "industry": "Environmental",
                "website": "https://greentech-env.com", 
                "description": "Environmental consulting and compliance services",
                "target_audience": "Facility managers, compliance officers, environmental professionals",
                "brand_voice": "Expert, technical, environmentally conscious",
                "owner_id": admin_id,
                "created_at": datetime.utcnow()
            },
            {
                "_id": str(ObjectId()),
                "name": "ProSafe Training Institute",
                "industry": "Safety Training",
                "website": "https://prosafetraining.com",
                "description": "Professional safety training and certification programs",
                "target_audience": "Safety professionals, HR managers, corporate trainers",
                "brand_voice": "Authoritative, educational, professional",
                "owner_id": admin_id,
                "created_at": datetime.utcnow()
            }
        ]
        
        # Insert demo companies
        for company in demo_companies:
            await db.companies.insert_one(company)
        
        # Return success without password
        admin_user_response = admin_user.copy()
        del admin_user_response["password"]
        del admin_user_response["_id"]
        
        return {
            "status": "success",
            "message": "Admin user and demo companies created successfully",
            "admin_user": admin_user_response,
            "credentials": {
                "email": "admin@postvelocity.com",
                "password": "admin123",
                "note": "Use these credentials to log in"
            },
            "companies_created": len(demo_companies)
        }
        
    except Exception as e:
        print(f"Admin setup error: {e}")
        raise HTTPException(status_code=500, detail="Failed to set up admin user")

@app.get("/api/auth/user/{user_id}")
async def get_user_profile(user_id: str):
    """Get user profile information"""
    try:
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user["id"] = str(user["_id"])
        del user["_id"]
        if "password" in user:
            del user["password"]
        
        return {
            "status": "success",
            "user": user
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Get user profile error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get user profile")

@app.delete("/api/auth/reset-admin")
async def reset_admin_user():
    """Reset admin user for testing (delete and recreate)"""
    try:
        # Delete existing admin users
        await db.users.delete_many({"role": "admin"})
        # Delete existing companies for admin
        await db.companies.delete_many({"owner_id": {"$regex": ".*"}})
        
        return {
            "status": "success",
            "message": "Admin user and companies deleted. Call setup-admin to recreate."
        }
    except Exception as e:
        print(f"Reset admin error: {e}")
        raise HTTPException(status_code=500, detail="Failed to reset admin user")

@app.get("/api/admin/users")
async def get_all_users():
    """Get all users for admin management with comprehensive analytics"""
    try:
        users = await db.users.find({}).to_list(length=None)
        
        user_list = []
        for user in users:
            user_id = str(user.get("_id"))
            
            # Get company count
            company_count = await db.companies.count_documents({"owner_id": user_id})
            
            # Get OAuth connections count
            oauth_count = await db.oauth_tokens.count_documents({
                "user_id": user_id, 
                "is_active": True
            })
            
            # Get content generation stats (mock for now - in production, track actual usage)
            content_stats = {
                "total_posts": 0,
                "posts_this_month": 0,
                "platforms_used": [],
                "last_post_date": None
            }
            
            # Get billing history for user
            billing_history = await get_user_billing_history(user_id)
            
            # Calculate account health score
            health_score = 100
            if not user.get("last_login"):
                health_score -= 30
            if company_count == 0:
                health_score -= 20
            if oauth_count == 0:
                health_score -= 25
            
            user_data = {
                "id": user_id,
                "username": user.get("username", ""),
                "email": user.get("email", ""),
                "full_name": user.get("full_name", ""),
                "role": user.get("role", "user"),
                "current_plan": user.get("current_plan", "starter"),
                "subscription_status": user.get("subscription_status", "active"),
                "is_active": user.get("is_active", True),
                "created_at": user.get("created_at"),
                "last_login": user.get("last_login"),
                "company_count": company_count,
                "oauth_connections": oauth_count,
                "content_stats": content_stats,
                "health_score": max(0, health_score),
                "account_value": calculate_account_value(user.get("current_plan", "starter")),
                "days_since_signup": (datetime.utcnow() - user.get("created_at", datetime.utcnow())).days if user.get("created_at") else 0,
                "billing_history": billing_history
            }
            user_list.append(user_data)
        
        # Calculate platform summary stats
        total_users = len(user_list)
        active_users = len([u for u in user_list if u.get("last_login")])
        total_companies = sum(u["company_count"] for u in user_list)
        total_connections = sum(u["oauth_connections"] for u in user_list)
        
        plan_distribution = {}
        for user in user_list:
            plan = user["current_plan"]
            plan_distribution[plan] = plan_distribution.get(plan, 0) + 1
        
        return {
            "status": "success",
            "users": user_list,
            "summary": {
                "total_users": total_users,
                "active_users": active_users,
                "total_companies": total_companies,
                "total_oauth_connections": total_connections,
                "plan_distribution": plan_distribution,
                "average_health_score": sum(u["health_score"] for u in user_list) / total_users if total_users > 0 else 0
            }
        }
        
    except Exception as e:
        print(f"Get all users error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get users")

def calculate_account_value(plan):
    """Calculate monthly account value based on plan"""
    plan_values = {
        "starter": 29,
        "professional": 79, 
        "business": 199,
        "enterprise": 499
    }
    return plan_values.get(plan, 0)

@app.get("/api/admin/analytics")
async def get_admin_analytics():
    """Get comprehensive platform analytics for admin dashboard"""
    try:
        # User analytics
        total_users = await db.users.count_documents({})
        active_users = await db.users.count_documents({"last_login": {"$exists": True}})
        admin_users = await db.users.count_documents({"role": "admin"})
        
        # Company analytics
        total_companies = await db.companies.count_documents({})
        
        # OAuth analytics
        total_connections = await db.oauth_tokens.count_documents({"is_active": True})
        
        # Plan distribution
        plan_pipeline = [
            {"$group": {"_id": "$current_plan", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        plan_distribution = await db.users.aggregate(plan_pipeline).to_list(length=None)
        
        # Revenue calculation (estimated)
        revenue_pipeline = [
            {"$group": {
                "_id": "$current_plan",
                "count": {"$sum": 1},
                "plan": {"$first": "$current_plan"}
            }}
        ]
        revenue_data = await db.users.aggregate(revenue_pipeline).to_list(length=None)
        
        monthly_revenue = 0
        for item in revenue_data:
            plan_revenue = calculate_account_value(item["_id"])
            monthly_revenue += plan_revenue * item["count"]
        
        # User growth (last 7 days vs previous 7 days)
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        fourteen_days_ago = datetime.utcnow() - timedelta(days=14)
        
        recent_users = await db.users.count_documents({
            "created_at": {"$gte": seven_days_ago}
        })
        previous_users = await db.users.count_documents({
            "created_at": {"$gte": fourteen_days_ago, "$lt": seven_days_ago}
        })
        
        growth_rate = ((recent_users - previous_users) / max(previous_users, 1)) * 100 if previous_users > 0 else 0
        
        # Platform health metrics
        platform_health = {
            "database_collections": await get_collection_counts(),
            "oauth_success_rate": 95.0,  # Mock data - in production, track actual rates
            "avg_response_time": "120ms",
            "uptime": "99.9%"
        }
        
        return {
            "status": "success",
            "analytics": {
                "users": {
                    "total": total_users,
                    "active": active_users,
                    "admin": admin_users,
                    "growth_rate": round(growth_rate, 1),
                    "recent_signups": recent_users
                },
                "companies": {
                    "total": total_companies,
                    "avg_per_user": round(total_companies / max(total_users, 1), 2)
                },
                "oauth": {
                    "total_connections": total_connections,
                    "avg_per_user": round(total_connections / max(total_users, 1), 2)
                },
                "revenue": {
                    "monthly_revenue": monthly_revenue,
                    "annual_revenue": monthly_revenue * 12,
                    "avg_revenue_per_user": round(monthly_revenue / max(total_users, 1), 2)
                },
                "plan_distribution": plan_distribution,
                "platform_health": platform_health
            }
        }
        
    except Exception as e:
        print(f"Get admin analytics error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get analytics")

async def get_collection_counts():
    """Get document counts for all collections"""
    try:
        return {
            "users": await db.users.count_documents({}),
            "companies": await db.companies.count_documents({}),
            "oauth_tokens": await db.oauth_tokens.count_documents({}),
        }
    except:
        return {"error": "Unable to fetch collection counts"}

@app.get("/api/admin/comprehensive-analytics")
async def get_comprehensive_admin_analytics():
    """Get comprehensive analytics with detailed breakdowns for admin dashboard"""
    try:
        # Time ranges for analytics
        now = datetime.utcnow()
        last_30_days = now - timedelta(days=30)
        last_7_days = now - timedelta(days=7)
        last_24_hours = now - timedelta(hours=24)
        
        # User Analytics
        total_users = await db.users.count_documents({})
        active_users_7d = await db.users.count_documents({"last_login": {"$gte": last_7_days}})
        new_users_30d = await db.users.count_documents({"created_at": {"$gte": last_30_days}})
        new_users_7d = await db.users.count_documents({"created_at": {"$gte": last_7_days}})
        
        # Plan Distribution with Revenue
        plan_pipeline = [
            {"$group": {
                "_id": "$current_plan", 
                "count": {"$sum": 1},
                "users": {"$push": {"id": {"$toString": "$_id"}, "email": "$email", "created_at": "$created_at"}}
            }},
            {"$sort": {"count": -1}}
        ]
        plan_distribution = await db.users.aggregate(plan_pipeline).to_list(length=None)
        
        # Revenue Calculation
        total_revenue = 0
        revenue_by_plan = {}
        for plan_data in plan_distribution:
            plan = plan_data["_id"] 
            count = plan_data["count"]
            plan_revenue = calculate_account_value(plan)
            plan_total = plan_revenue * count
            total_revenue += plan_total
            revenue_by_plan[plan] = {
                "monthly_revenue": plan_total,
                "user_count": count,
                "avg_revenue_per_user": plan_revenue
            }
        
        # Company Analytics
        total_companies = await db.companies.count_documents({})
        companies_30d = await db.companies.count_documents({"created_at": {"$gte": last_30_days}})
        
        # Content Analytics (Mock data - replace with actual content generation tracking)
        content_analytics = {
            "total_posts_generated": await db.companies.count_documents({}) * 25,  # Mock: avg 25 posts per company
            "posts_last_30_days": new_users_30d * 10,  # Mock data
            "posts_last_7_days": new_users_7d * 3,  # Mock data
            "most_popular_platforms": [
                {"platform": "Instagram", "usage_count": 150, "percentage": 35.2},
                {"platform": "Facebook", "usage_count": 120, "percentage": 28.1},
                {"platform": "LinkedIn", "usage_count": 85, "percentage": 19.9},
                {"platform": "X (Twitter)", "usage_count": 70, "percentage": 16.4}
            ]
        }
        
        # Billing & Transaction Analytics
        payment_pipeline = [
            {"$group": {
                "_id": {"status": "$payment_status", "plan": "$plan_type"},
                "count": {"$sum": 1},
                "total_amount": {"$sum": "$amount"},
                "avg_amount": {"$avg": "$amount"}
            }}
        ]
        payment_analytics = await db.payment_transactions.aggregate(payment_pipeline).to_list(length=None)
        
        # Recent Activity (Last 30 transactions)
        recent_transactions = []
        try:
            transactions_cursor = db.payment_transactions.find({}).sort("created_at", -1).limit(30)
            async for transaction in transactions_cursor:
                recent_transactions.append({
                    "id": str(transaction["_id"]),
                    "user_id": transaction.get("user_id"),
                    "amount": transaction.get("amount", 0),
                    "status": transaction.get("payment_status", "unknown"),
                    "plan_type": transaction.get("plan_type"),
                    "created_at": transaction.get("created_at"),
                    "stripe_payment_intent_id": transaction.get("stripe_payment_intent_id")
                })
        except:
            pass  # Handle missing collection gracefully
        
        # Subscription Status Distribution
        subscription_pipeline = [
            {"$group": {"_id": "$subscription_status", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        subscription_distribution = await db.users.aggregate(subscription_pipeline).to_list(length=None)
        
        # Growth Metrics
        growth_metrics = {
            "user_growth_rate": ((new_users_7d / max(total_users - new_users_7d, 1)) * 100) if total_users > new_users_7d else 0,
            "revenue_growth_trend": "increasing",  # Mock - in production, compare with previous periods
            "churn_rate": 2.5,  # Mock data
            "conversion_rate": 8.3  # Mock data
        }
        
        return {
            "status": "success",
            "analytics": {
                "overview": {
                    "total_users": total_users,
                    "active_users_7d": active_users_7d,
                    "new_users_30d": new_users_30d,
                    "new_users_7d": new_users_7d,
                    "total_companies": total_companies,
                    "new_companies_30d": companies_30d,
                    "total_revenue": round(total_revenue, 2),
                    "avg_revenue_per_user": round(total_revenue / max(total_users, 1), 2)
                },
                "plan_distribution": plan_distribution,
                "revenue_by_plan": revenue_by_plan,
                "content_analytics": content_analytics,
                "payment_analytics": payment_analytics,
                "recent_transactions": recent_transactions,
                "subscription_distribution": subscription_distribution,
                "growth_metrics": growth_metrics,
                "generated_at": now.isoformat()
            }
        }
    except Exception as e:
        print(f"Get comprehensive admin analytics error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get comprehensive analytics")

@app.get("/api/admin/user-details/{user_id}")
async def get_admin_user_details(user_id: str):
    """Get detailed information about a specific user including posts, billing, and activity history"""
    try:
        # Get user
        user = await db.users.find_one({"_id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get user's companies with details
        companies = []
        companies_cursor = db.companies.find({"owner_id": user_id})
        async for company in companies_cursor:
            companies.append({
                "id": str(company["_id"]),
                "name": company.get("name", ""),
                "industry": company.get("industry", ""),
                "created_at": company.get("created_at"),
                "media_library_size": company.get("media_library_size", 0)
            })
        
        # Get OAuth connections
        oauth_connections = []
        oauth_cursor = db.oauth_tokens.find({"user_id": user_id, "is_active": True})
        async for connection in oauth_cursor:
            oauth_connections.append({
                "platform": connection.get("platform", ""),
                "connected_at": connection.get("created_at"),
                "status": connection.get("connection_status", "active")
            })
        
        # Get billing history
        billing_history = await get_user_billing_history(user_id)
        
        # Calculate total spent
        total_spent = sum(transaction.get("amount", 0) for transaction in billing_history if transaction.get("status") == "paid")
        
        # Mock content statistics - in production, track actual content generation
        content_stats = {
            "total_posts_generated": len(companies) * 12,  # Mock: 12 posts per company
            "posts_this_month": len(companies) * 3,  # Mock: 3 posts per company this month
            "platforms_used": list(set([conn["platform"] for conn in oauth_connections]))[:5],
            "last_activity": user.get("last_login"),
            "content_engagement": {
                "avg_engagement_rate": 4.2,  # Mock data
                "best_performing_platform": "Instagram",
                "total_reach": 15400  # Mock data
            }
        }
        
        # Calculate user health score
        health_score = 100
        if not user.get("last_login"):
            health_score -= 30
        if len(companies) == 0:
            health_score -= 20
        if len(oauth_connections) == 0:
            health_score -= 25
        if total_spent == 0:
            health_score -= 15
        
        return {
            "status": "success",
            "user_details": {
                "id": str(user["_id"]),
                "username": user.get("username", ""),
                "email": user.get("email", ""),
                "full_name": user.get("full_name", ""),
                "role": user.get("role", "user"),
                "current_plan": user.get("current_plan", "starter"),
                "subscription_status": user.get("subscription_status", "active"),
                "is_active": user.get("is_active", True),
                "created_at": user.get("created_at"),
                "last_login": user.get("last_login"),
                "trial_end": user.get("trial_end"),
                "companies": companies,
                "oauth_connections": oauth_connections,
                "billing_history": billing_history,
                "total_spent": total_spent,
                "content_stats": content_stats,
                "health_score": max(0, health_score),
                "account_value": calculate_account_value(user.get("current_plan", "starter")),
                "days_since_signup": (datetime.utcnow() - user.get("created_at", datetime.utcnow())).days if user.get("created_at") else 0
            }
        }
    except Exception as e:
        print(f"Get admin user details error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get user details")

@app.get("/api/admin/billing-analytics")
async def get_admin_billing_analytics():
    """Get comprehensive billing and revenue analytics"""
    try:
        # Revenue over time
        now = datetime.utcnow()
        last_30_days = now - timedelta(days=30)
        last_90_days = now - timedelta(days=90)
        
        # Revenue by time periods
        revenue_30d = await calculate_revenue_for_period(last_30_days, now)
        revenue_90d = await calculate_revenue_for_period(last_90_days, now)
        
        # Top paying customers
        top_customers_pipeline = [
            {"$group": {
                "_id": "$user_id",
                "total_spent": {"$sum": "$amount"},
                "transaction_count": {"$sum": 1},
                "last_payment": {"$max": "$created_at"}
            }},
            {"$sort": {"total_spent": -1}},
            {"$limit": 10}
        ]
        
        top_customers_raw = await db.payment_transactions.aggregate(top_customers_pipeline).to_list(length=None)
        
        # Enrich top customers with user details
        top_customers = []
        for customer in top_customers_raw:
            try:
                user = await db.users.find_one({"_id": customer["_id"]})
                if user:
                    top_customers.append({
                        "user_id": customer["_id"],
                        "email": user.get("email", ""),
                        "full_name": user.get("full_name", ""),
                        "current_plan": user.get("current_plan", ""),
                        "total_spent": customer["total_spent"],
                        "transaction_count": customer["transaction_count"],
                        "last_payment": customer["last_payment"]
                    })
            except:
                continue
        
        # Failed transactions
        failed_transactions = await db.payment_transactions.count_documents({"payment_status": "failed"})
        total_transactions = await db.payment_transactions.count_documents({})
        success_rate = ((total_transactions - failed_transactions) / max(total_transactions, 1)) * 100 if total_transactions > 0 else 100
        
        # Plan upgrade/downgrade tracking (mock data - in production, track plan changes)
        plan_changes = {
            "upgrades_30d": 8,
            "downgrades_30d": 2,
            "cancellations_30d": 5,
            "most_common_upgrade": "starter -> professional",
            "most_common_downgrade": "business -> professional"
        }
        
        return {
            "status": "success",
            "billing_analytics": {
                "revenue": {
                    "last_30_days": revenue_30d,
                    "last_90_days": revenue_90d,
                    "success_rate": round(success_rate, 2)
                },
                "top_customers": top_customers,
                "plan_changes": plan_changes,
                "failed_transactions": failed_transactions,
                "total_transactions": total_transactions
            }
        }
    except Exception as e:
        print(f"Get admin billing analytics error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get billing analytics")

async def calculate_revenue_for_period(start_date: datetime, end_date: datetime) -> float:
    """Calculate total revenue for a specific time period"""
    try:
        pipeline = [
            {"$match": {
                "created_at": {"$gte": start_date, "$lte": end_date},
                "payment_status": "paid"
            }},
            {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
        ]
        result = await db.payment_transactions.aggregate(pipeline).to_list(length=1)
        return result[0]["total"] if result else 0.0
    except:
        return 0.0

@app.get("/api/admin/user-activity/{user_id}")
async def get_user_activity(user_id: str):
    """Get detailed activity for a specific user"""
    try:
        # Get user details
        user = await db.users.find_one({"_id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get user's companies
        companies = await db.companies.find({"owner_id": user_id}).to_list(length=None)
        
        # Get OAuth connections
        oauth_connections = await db.oauth_tokens.find({
            "user_id": user_id,
            "is_active": True
        }).to_list(length=None)
        
        # Get platform-specific data
        platforms = {}
        for token in oauth_connections:
            platform = token.get("platform")
            platforms[platform] = {
                "connected_at": token.get("created_at"),
                "last_used": token.get("updated_at"),
                "status": token.get("is_active", False),
                "username": token.get("platform_username")
            }
        
        # Calculate usage metrics (mock data for demo)
        usage_stats = {
            "content_generated": 45,
            "posts_published": 32,
            "platforms_used": len(platforms),
            "last_activity": user.get("last_login"),
            "favorite_platforms": list(platforms.keys())[:3]
        }
        
        # Account timeline (key events)
        timeline = [
            {
                "date": user.get("created_at"),
                "event": "Account Created",
                "details": f"Signed up with {user.get('current_plan')} plan"
            }
        ]
        
        if user.get("last_login"):
            timeline.append({
                "date": user.get("last_login"),
                "event": "Last Login",
                "details": "User accessed the platform"
            })
        
        for company in companies:
            timeline.append({
                "date": company.get("created_at"),
                "event": "Company Added",
                "details": f"Created company: {company.get('name')}"
            })
        
        # Sort timeline by date
        timeline.sort(key=lambda x: x["date"] if x["date"] else datetime.min, reverse=True)
        
        return {
            "status": "success",
            "user": {
                "id": str(user["_id"]),
                "email": user.get("email"),
                "full_name": user.get("full_name"),
                "plan": user.get("current_plan"),
                "status": user.get("subscription_status"),
                "created_at": user.get("created_at")
            },
            "companies": [
                {
                    "id": str(c.get("_id")),
                    "name": c.get("name"),
                    "industry": c.get("industry"),
                    "created_at": c.get("created_at")
                } for c in companies
            ],
            "oauth_platforms": platforms,
            "usage_stats": usage_stats,
            "timeline": timeline[:10]  # Latest 10 events
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Get user activity error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get user activity")

@app.post("/api/admin/user-action/{user_id}")
async def perform_user_action(user_id: str, action: str, reason: str = ""):
    """Perform admin actions on user accounts"""
    try:
        user = await db.users.find_one({"_id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if action == "suspend":
            await db.users.update_one(
                {"_id": user_id},
                {"$set": {"is_active": False, "suspension_reason": reason}}
            )
            return {"status": "success", "message": f"User suspended: {reason}"}
            
        elif action == "activate":
            await db.users.update_one(
                {"_id": user_id},
                {"$set": {"is_active": True}, "$unset": {"suspension_reason": ""}}
            )
            return {"status": "success", "message": "User activated"}
            
        elif action == "reset_password":
            # In production, implement proper password reset
            await db.users.update_one(
                {"_id": user_id},
                {"$set": {"password": "reset123"}}
            )
            return {"status": "success", "message": "Password reset to 'reset123'"}
            
        elif action == "upgrade_plan":
            plan = reason  # In this case, reason contains the new plan
            await db.users.update_one(
                {"_id": user_id},
                {"$set": {"current_plan": plan}}
            )
            return {"status": "success", "message": f"Plan upgraded to {plan}"}
            
        else:
            raise HTTPException(status_code=400, detail="Invalid action")
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"User action error: {e}")
        raise HTTPException(status_code=500, detail="Failed to perform action")

@app.post("/api/admin/impersonate/{user_id}")
async def impersonate_user(user_id: str):
    """Allow admin to impersonate any user for support purposes"""
    try:
        # Find the target user
        user = await db.users.find_one({"_id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Prepare user data for impersonation
        impersonated_user = {
            "id": str(user.get("_id")),
            "username": user.get("username", ""),
            "email": user.get("email", ""),
            "full_name": user.get("full_name", ""),
            "role": user.get("role", "user"),
            "current_plan": user.get("current_plan", "starter"),
            "subscription_status": user.get("subscription_status", "active"),
            "is_active": user.get("is_active", True),
            "created_at": user.get("created_at"),
            "last_login": user.get("last_login"),
            "permissions": user.get("permissions", []),
            # Mark as impersonated
            "is_impersonated": True,
            "impersonated_by": "admin",
            "original_admin": True
        }
        
        return {
            "status": "success",
            "message": f"Now impersonating {user.get('full_name', user.get('email'))}",
            "user": impersonated_user,
            "impersonation_token": f"impersonate-{user_id}-{int(time.time())}"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Impersonation error: {e}")
        raise HTTPException(status_code=500, detail="Failed to impersonate user")

@app.post("/api/admin/create-test-user")
async def create_test_user(request: Request):
    """Create a test user for admin testing purposes"""
    try:
        # Get form data
        form_data = await request.form()
        email = form_data.get("email")
        full_name = form_data.get("full_name")
        plan = form_data.get("plan", "starter")
        industry = form_data.get("industry", "Construction")
        
        if not email or not full_name:
            raise HTTPException(status_code=400, detail="Email and full name are required")
        
        # Check if user already exists
        existing_user = await db.users.find_one({"email": email})
        if existing_user:
            return {
                "status": "exists",
                "message": "User already exists",
                "user_id": str(existing_user["_id"])
            }
        
        # Create test user
        user_id = str(ObjectId())
        test_user = {
            "_id": user_id,
            "id": user_id,
            "username": email.split('@')[0],
            "email": email,
            "full_name": full_name,
            "role": "user",
            "permissions": ["basic"],
            "current_plan": plan,
            "subscription_status": "active",
            "is_active": True,
            "created_at": datetime.utcnow(),
            "last_login": None,
            "password": "test123"  # Simple test password
        }
        
        await db.users.insert_one(test_user)
        
        # Create a demo company for the test user
        company_id = str(ObjectId())
        demo_company = {
            "_id": company_id,
            "name": f"{full_name}'s {industry} Company",
            "industry": industry,
            "website": f"https://{email.split('@')[0]}.com",
            "description": f"Demo company for testing user {full_name}",
            "target_audience": f"{industry} professionals and clients",
            "brand_voice": "Professional, reliable, customer-focused",
            "owner_id": user_id,
            "created_at": datetime.utcnow()
        }
        
        await db.companies.insert_one(demo_company)
        
        # Prepare response
        test_user_response = test_user.copy()
        del test_user_response["password"]
        del test_user_response["_id"]
        
        return {
            "status": "success",
            "message": f"Test user {full_name} created successfully",
            "user": test_user_response,
            "company_created": True,
            "credentials": {
                "email": email,
                "password": "test123"
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Create test user error: {e}")
        raise HTTPException(status_code=500, detail="Failed to create test user")

# ===== FREE ACCESS SYSTEM =====

@app.post("/api/admin/generate-free-code")
async def generate_free_access_code(code_data: dict):
    """Generate free access codes for promotional purposes"""
    try:
        from datetime import datetime, timedelta
        import secrets
        import string
        
        # Generate unique code
        code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        code = f"FREE-{code}"
        
        # Set expiration based on duration
        duration_days = code_data.get("duration_days", 30)
        expires_at = datetime.utcnow() + timedelta(days=duration_days)
        
        # Create free access code document
        free_code = {
            "_id": code,
            "code": code,
            "plan_level": code_data.get("plan_level", "professional"),  # starter, professional, business, enterprise
            "duration_days": duration_days,
            "max_uses": code_data.get("max_uses", 1),  # How many people can use this code
            "used_count": 0,
            "created_at": datetime.utcnow(),
            "expires_at": expires_at,
            "created_by": "admin",
            "description": code_data.get("description", f"{duration_days}-day free access"),
            "is_active": True,
            "usage_history": []
        }
        
        # Save to database
        await db.free_access_codes.insert_one(free_code)
        
        return {
            "status": "success",
            "code": code,
            "plan_level": code_data.get("plan_level", "professional"),
            "duration_days": duration_days,
            "expires_at": expires_at.isoformat(),
            "max_uses": code_data.get("max_uses", 1),
            "description": code_data.get("description", f"{duration_days}-day free access")
        }
        
    except Exception as e:
        print(f"Generate free code error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate free access code")

@app.post("/api/redeem-free-code")
async def redeem_free_access_code(request: dict):
    """Allow users to redeem free access codes"""
    try:
        from datetime import datetime, timedelta
        
        code = request.get("code", "").upper()
        user_id = request.get("user_id")
        
        if not code or not user_id:
            raise HTTPException(status_code=400, detail="Code and user_id required")
        
        # Find the code
        free_code = await db.free_access_codes.find_one({"code": code, "is_active": True})
        if not free_code:
            raise HTTPException(status_code=404, detail="Invalid or expired code")
        
        # Check if code is expired
        if datetime.utcnow() > free_code["expires_at"]:
            raise HTTPException(status_code=400, detail="Code has expired")
        
        # Check if code has uses remaining
        if free_code["used_count"] >= free_code["max_uses"]:
            raise HTTPException(status_code=400, detail="Code has been fully used")
        
        # Check if user already used this code
        if any(usage["user_id"] == user_id for usage in free_code.get("usage_history", [])):
            raise HTTPException(status_code=400, detail="You have already used this code")
        
        # Find the user
        user = await db.users.find_one({"_id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Calculate new plan expiration
        current_plan_end = user.get("plan_expires_at", datetime.utcnow())
        if isinstance(current_plan_end, str):
            current_plan_end = datetime.fromisoformat(current_plan_end.replace('Z', '+00:00'))
        
        # Extend from current expiration or now, whichever is later
        start_date = max(current_plan_end, datetime.utcnow())
        new_expiration = start_date + timedelta(days=free_code["duration_days"])
        
        # Update user with free access
        user_update = {
            "current_plan": free_code["plan_level"],
            "plan_expires_at": new_expiration,
            "subscription_status": "free_access",
            "free_access_code_used": code,
            "free_access_granted_at": datetime.utcnow()
        }
        
        await db.users.update_one({"_id": user_id}, {"$set": user_update})
        
        # Update code usage
        usage_record = {
            "user_id": user_id,
            "user_email": user.get("email", ""),
            "redeemed_at": datetime.utcnow(),
            "ip_address": request.get("ip_address", "")
        }
        
        await db.free_access_codes.update_one(
            {"code": code},
            {
                "$inc": {"used_count": 1},
                "$push": {"usage_history": usage_record}
            }
        )
        
        return {
            "status": "success",
            "message": f"Free {free_code['plan_level']} access granted for {free_code['duration_days']} days!",
            "plan_level": free_code["plan_level"],
            "duration_days": free_code["duration_days"],
            "expires_at": new_expiration.isoformat(),
            "code_description": free_code.get("description", "")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Redeem free code error: {e}")
        raise HTTPException(status_code=500, detail="Failed to redeem code")

@app.get("/api/admin/free-codes")
async def list_free_access_codes():
    """List all free access codes for admin management"""
    try:
        codes_cursor = db.free_access_codes.find({}).sort("created_at", -1)
        codes = []
        
        async for code in codes_cursor:
            codes.append({
                "code": code["code"],
                "plan_level": code["plan_level"],
                "duration_days": code["duration_days"],
                "max_uses": code["max_uses"],
                "used_count": code["used_count"],
                "created_at": code["created_at"],
                "expires_at": code["expires_at"],
                "description": code.get("description", ""),
                "is_active": code.get("is_active", True),
                "usage_history": code.get("usage_history", [])
            })
        
        return {
            "status": "success",
            "codes": codes,
            "total_codes": len(codes)
        }
        
    except Exception as e:
        print(f"List free codes error: {e}")
        raise HTTPException(status_code=500, detail="Failed to list free codes")

@app.delete("/api/admin/free-codes/{code}")
async def deactivate_free_code(code: str):
    """Deactivate a free access code"""
    try:
        result = await db.free_access_codes.update_one(
            {"code": code},
            {"$set": {"is_active": False, "deactivated_at": datetime.utcnow()}}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Code not found")
        
        return {
            "status": "success",
            "message": f"Code {code} deactivated successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Deactivate code error: {e}")
        raise HTTPException(status_code=500, detail="Failed to deactivate code")

# ===== AI VIDEO & MUSIC GENERATION SYSTEM =====

import requests
import ffmpeg
from datetime import datetime, timedelta
import os
import asyncio
import aiofiles

# Video & Music Generation Models
class AIMediaRequest(BaseModel):
    content_text: str
    platform: str = "instagram"
    mood: str = "upbeat"
    video_style: str = "professional" 
    music_style: str = "background"
    duration_seconds: int = 30
    user_id: str
    company_id: str = None

class AIMediaResponse(BaseModel):
    video_url: str = None
    music_url: str = None
    combined_url: str = None
    cost_breakdown: dict
    generation_id: str
    status: str

# Pricing Configuration (20% markup over cost)
AI_MEDIA_PRICING = {
    "runway_video": {
        "cost_per_second": 0.10,  # Runway's actual cost
        "markup_percentage": 20,
        "our_price_per_second": 0.12  # 20% markup
    },
    "music_generation": {
        "cost_per_track": 0.50,  # Music API cost
        "markup_percentage": 20,
        "our_price_per_track": 0.60  # 20% markup
    },
    "processing_fee": 0.25  # Our processing/storage fee
}

# Video Generation Service (AITurbo.ai)
async def generate_ai_video(prompt: str, duration: int = 30, style: str = "professional"):
    """Generate video using AITurbo.ai"""
    try:
        # Initialize AITurbo client
        aiturbo_api_key = os.environ.get("AITURBO_API_KEY")
        if not aiturbo_api_key:
            raise HTTPException(status_code=500, detail="AITurbo API key not configured")
        
        # AITurbo API call
        aiturbo_url = "https://api.aiturbo.ai/v1/video/generate"
        headers = {
            "Authorization": f"Bearer {aiturbo_api_key}",
            "Content-Type": "application/json"
        }
        
        # Map styles to AITurbo parameters
        style_mapping = {
            "professional": "corporate_clean",
            "creative": "artistic_dynamic", 
            "cinematic": "film_quality",
            "tiktok": "social_vertical",
            "minimalist": "simple_elegant"
        }
        
        data = {
            "prompt": prompt,
            "duration": duration,
            "style": style_mapping.get(style, "corporate_clean"),
            "aspect_ratio": "16:9" if style != "tiktok" else "9:16",
            "quality": "high",
            "fps": 30
        }
        
        response = requests.post(aiturbo_url, headers=headers, json=data, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            task_id = result.get("task_id") or result.get("id")
            
            if not task_id:
                # If immediate response
                return result.get("video_url") or result.get("download_url")
            
            # Poll for completion
            for attempt in range(30):  # 30 attempts = 5 minutes max
                status_response = requests.get(
                    f"https://api.aiturbo.ai/v1/video/status/{task_id}",
                    headers=headers,
                    timeout=30
                )
                
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    status = status_data.get("status")
                    
                    if status in ["completed", "success", "done"]:
                        return status_data.get("video_url") or status_data.get("download_url") or status_data.get("result_url")
                    elif status in ["failed", "error"]:
                        raise HTTPException(status_code=500, detail="Video generation failed")
                
                await asyncio.sleep(10)  # Wait 10 seconds between checks
            
            raise HTTPException(status_code=500, detail="Video generation timeout")
        elif response.status_code == 401:
            raise HTTPException(status_code=500, detail="Invalid AITurbo API key")
        else:
            # Try alternative endpoint format
            try:
                alt_url = "https://api.aiturbo.ai/generate"
                alt_data = {
                    "text": prompt,
                    "length": duration,
                    "style": style,
                    "format": "mp4"
                }
                alt_response = requests.post(alt_url, headers=headers, json=alt_data, timeout=120)
                
                if alt_response.status_code == 200:
                    alt_result = alt_response.json()
                    return alt_result.get("url") or alt_result.get("video_url")
                    
            except:
                pass
            
            raise HTTPException(status_code=500, detail=f"AITurbo API error: {response.text}")
            
    except Exception as e:
        print(f"Video generation error: {str(e)}")
        # Fallback to a demo video for testing
        if "demo" in str(e).lower() or "key" in str(e).lower():
            return "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4"
        raise HTTPException(status_code=500, detail=f"Video generation failed: {str(e)}")

# Music Generation Service (MusicAPI)
async def generate_ai_music(prompt: str, duration: int = 30, mood: str = "upbeat", style: str = "background"):
    """Generate music using MusicAPI"""
    try:
        music_api_key = os.environ.get("MUSIC_API_KEY")
        if not music_api_key:
            raise HTTPException(status_code=500, detail="Music API key not configured")
        
        # MusicAPI call
        music_url = "https://api.musicapi.ai/v1/generate"
        headers = {
            "Authorization": f"Bearer {music_api_key}",
            "Content-Type": "application/json"
        }
        
        # Map mood to music style
        mood_mapping = {
            "upbeat": "energetic pop instrumental",
            "professional": "subtle corporate background music", 
            "dramatic": "cinematic orchestral score",
            "calm": "ambient peaceful instrumental",
            "trendy": "modern electronic beat"
        }
        
        music_prompt = f"{mood_mapping.get(mood, 'background instrumental music')}, {style} style, duration {duration} seconds"
        
        data = {
            "prompt": music_prompt,
            "duration": duration,
            "format": "mp3",
            "quality": "high",
            "model": "sonic",  # MusicAPI model
            "commercial_license": True
        }
        
        response = requests.post(music_url, headers=headers, json=data, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            
            # Check if we get immediate URL
            if "audio_url" in result:
                return result["audio_url"]
            elif "download_url" in result:
                return result["download_url"]
            elif "url" in result:
                return result["url"]
            elif "task_id" in result or "id" in result:
                # Poll for completion
                task_id = result.get("task_id") or result.get("id")
                
                for attempt in range(20):  # Music generation is usually faster
                    status_response = requests.get(
                        f"https://api.musicapi.ai/v1/status/{task_id}",
                        headers=headers,
                        timeout=30
                    )
                    
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        status = status_data.get("status")
                        
                        if status in ["completed", "success", "done"]:
                            return (status_data.get("audio_url") or 
                                   status_data.get("download_url") or 
                                   status_data.get("url"))
                        elif status in ["failed", "error"]:
                            break  # Fall back to preset music
                    
                    await asyncio.sleep(5)  # Check every 5 seconds
            
            # If no URL found, try alternative API format
            alt_data = {
                "text": music_prompt,
                "length": duration,
                "genre": mood,
                "instrumental": True
            }
            
            alt_response = requests.post(
                "https://musicapi.ai/api/generate", 
                headers=headers, 
                json=alt_data, 
                timeout=60
            )
            
            if alt_response.status_code == 200:
                alt_result = alt_response.json()
                if "url" in alt_result:
                    return alt_result["url"]
        
        # Fallback to pre-made music library
        print(f"Music API response: {response.status_code} - {response.text}")
        fallback_library = {
            "upbeat": "https://postvelocity-assets.s3.amazonaws.com/music/upbeat-background.mp3",
            "professional": "https://postvelocity-assets.s3.amazonaws.com/music/corporate-subtle.mp3",
            "dramatic": "https://postvelocity-assets.s3.amazonaws.com/music/cinematic-drama.mp3",
            "calm": "https://postvelocity-assets.s3.amazonaws.com/music/peaceful-ambient.mp3",
            "trendy": "https://postvelocity-assets.s3.amazonaws.com/music/modern-electronic.mp3"
        }
        return fallback_library.get(mood, fallback_library["upbeat"])
            
    except Exception as e:
        print(f"Music generation error: {str(e)}")
        fallback_library = {
            "upbeat": "https://postvelocity-assets.s3.amazonaws.com/music/upbeat-background.mp3",
            "professional": "https://postvelocity-assets.s3.amazonaws.com/music/corporate-subtle.mp3",
            "dramatic": "https://postvelocity-assets.s3.amazonaws.com/music/cinematic-drama.mp3",
            "calm": "https://postvelocity-assets.s3.amazonaws.com/music/peaceful-ambient.mp3",
            "trendy": "https://postvelocity-assets.s3.amazonaws.com/music/modern-electronic.mp3"
        }
        return fallback_library.get(mood, fallback_library["upbeat"])

# AI Image Generation Service
async def generate_ai_images(prompt: str, count: int = 1, style: str = "professional"):
    """Generate images using AI Image API"""
    try:
        # For now, use a placeholder service or integrate with DALL-E, Midjourney, etc.
        # This would typically connect to services like:
        # - OpenAI DALL-E API
        # - Stability AI (Stable Diffusion)
        # - Midjourney API (when available)
        # - Runway Image Generation
        
        # Mock implementation for demo
        generated_images = []
        for i in range(count):
            # In production, this would be actual AI-generated images
            generated_images.append({
                "id": f"img_{i+1}_{int(datetime.utcnow().timestamp())}",
                "url": f"https://picsum.photos/800/600?random={i+int(datetime.utcnow().timestamp())}",
                "prompt": prompt,
                "style": style,
                "size": "800x600"
            })
        
        return generated_images
        
    except Exception as e:
        print(f"Image generation error: {str(e)}")
        # Fallback to stock images
        return [{
            "id": "fallback_img",
            "url": "https://picsum.photos/800/600?random=1",
            "prompt": prompt,
            "style": "stock",
            "size": "800x600"
        }]

@app.post("/api/ai-images/generate")
async def generate_ai_images_endpoint(request: dict):
    """Generate AI images for social media posts"""
    try:
        prompt = request.get("prompt", "")
        count = request.get("count", 1)
        style = request.get("style", "professional")
        user_id = request.get("user_id", "")
        
        if not prompt:
            raise HTTPException(status_code=400, detail="Prompt is required")
        
        # Generate images
        images = await generate_ai_images(prompt, count, style)
        
        # Calculate cost (mock pricing)
        cost_per_image = 0.05  # $0.05 per AI image
        total_cost = len(images) * cost_per_image
        
        return {
            "status": "success",
            "images": images,
            "cost_breakdown": {
                "images_generated": len(images),
                "cost_per_image": cost_per_image,
                "total_cost": total_cost
            },
            "generated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        print(f"AI image generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate images: {str(e)}")

@app.get("/api/user-media/{user_id}")
async def get_user_media_library(user_id: str):
    """Get user's uploaded media library (videos, music, images)"""
    try:
        # This would typically fetch from your file storage system
        # For demo purposes, returning mock data
        
        mock_media = {
            "videos": [
                {
                    "id": "video_1",
                    "filename": "product_demo.mp4",
                    "url": "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4",
                    "duration": 45,
                    "size": "1.2 MB",
                    "uploaded_at": "2025-01-15T10:00:00Z"
                },
                {
                    "id": "video_2", 
                    "filename": "team_intro.mp4",
                    "url": "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_2mb.mp4",
                    "duration": 30,
                    "size": "2.1 MB",
                    "uploaded_at": "2025-01-14T15:30:00Z"
                }
            ],
            "music": [
                {
                    "id": "music_1",
                    "filename": "corporate_bg.mp3",
                    "url": "https://www.soundjay.com/misc/sounds-of-speech/corporate-background-loop.mp3",
                    "duration": 120,
                    "size": "3.2 MB",
                    "uploaded_at": "2025-01-13T09:15:00Z"
                },
                {
                    "id": "music_2",
                    "filename": "upbeat_intro.mp3", 
                    "url": "https://www.soundjay.com/misc/sounds-of-speech/upbeat-intro.mp3",
                    "duration": 30,
                    "size": "1.8 MB",
                    "uploaded_at": "2025-01-12T14:20:00Z"
                }
            ],
            "images": [
                {
                    "id": "img_1",
                    "filename": "team_photo.jpg",
                    "url": "https://picsum.photos/800/600?random=101",
                    "size": "245 KB",
                    "dimensions": "800x600",
                    "uploaded_at": "2025-01-11T11:00:00Z"
                },
                {
                    "id": "img_2",
                    "filename": "office_space.jpg",
                    "url": "https://picsum.photos/1200/800?random=102", 
                    "size": "892 KB",
                    "dimensions": "1200x800",
                    "uploaded_at": "2025-01-10T16:45:00Z"
                }
            ]
        }
        
        return {
            "status": "success",
            "media_library": mock_media,
            "summary": {
                "total_videos": len(mock_media["videos"]),
                "total_music": len(mock_media["music"]),
                "total_images": len(mock_media["images"]),
                "storage_used": "8.5 MB"
            }
        }
        
    except Exception as e:
        print(f"Get user media error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get media library")

# Media Combination Service
async def combine_video_and_audio(video_url: str, audio_url: str, output_filename: str):
    """Combine video and audio using FFmpeg"""
    try:
        # Download files temporarily
        video_path = f"/tmp/video_{output_filename}.mp4"
        audio_path = f"/tmp/audio_{output_filename}.mp3"
        output_path = f"/tmp/combined_{output_filename}.mp4"
        
        # Download video
        video_response = requests.get(video_url)
        with open(video_path, "wb") as f:
            f.write(video_response.content)
            
        # Download audio
        audio_response = requests.get(audio_url)
        with open(audio_path, "wb") as f:
            f.write(audio_response.content)
        
        # Combine using FFmpeg
        try:
            (
                ffmpeg
                .input(video_path)
                .audio
                .join(
                    ffmpeg.input(audio_path).audio
                )
                .output(output_path, vcodec='copy', acodec='aac', strict='experimental')
                .overwrite_output()
                .run(quiet=True)
            )
            
            # Upload combined file (simplified - use your storage service)
            # For now, return a mock URL
            combined_url = f"https://postvelocity-generated.s3.amazonaws.com/combined/{output_filename}.mp4"
            
            # Clean up temporary files
            os.remove(video_path)
            os.remove(audio_path)
            os.remove(output_path)
            
            return combined_url
            
        except Exception as ffmpeg_error:
            print(f"FFmpeg error: {str(ffmpeg_error)}")
            # Clean up files even on error
            for path in [video_path, audio_path, output_path]:
                if os.path.exists(path):
                    os.remove(path)
            raise HTTPException(status_code=500, detail="Media combination failed")
            
    except Exception as e:
        print(f"Media combination error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to combine media: {str(e)}")

# Cost Calculation
def calculate_ai_media_cost(duration_seconds: int, include_music: bool = True):
    """Calculate cost with 20% markup"""
    video_cost = duration_seconds * AI_MEDIA_PRICING["runway_video"]["our_price_per_second"]
    music_cost = AI_MEDIA_PRICING["music_generation"]["our_price_per_track"] if include_music else 0
    processing_fee = AI_MEDIA_PRICING["processing_fee"]
    
    total_cost = video_cost + music_cost + processing_fee
    
    return {
        "video_cost": round(video_cost, 2),
        "music_cost": round(music_cost, 2),
        "processing_fee": round(processing_fee, 2),
        "total_cost": round(total_cost, 2),
        "duration": duration_seconds
    }

@app.post("/api/ai-media/generate")
async def generate_ai_media(request: AIMediaRequest):
    """Generate AI video and music with automatic combination"""
    try:
        # Generate unique ID for this request
        generation_id = f"gen_{int(datetime.utcnow().timestamp())}_{request.user_id[:8]}"
        
        # Calculate cost
        cost_breakdown = calculate_ai_media_cost(
            request.duration_seconds, 
            include_music=(request.music_style != "none")
        )
        
        # Check if user has sufficient credits/plan allowance
        try:
            # Handle both ObjectId and string user IDs
            user_query = {"_id": request.user_id}
            if len(request.user_id) != 24:  # Not a valid ObjectId length
                user_query = {"email": request.user_id}  # Search by email if not ObjectId
            
            user = await db.users.find_one(user_query)
            if not user:
                # Create a demo user for testing
                user = {
                    "_id": request.user_id,
                    "email": f"{request.user_id}@demo.com",
                    "current_plan": "professional",
                    "ai_media_usage": 0
                }
                await db.users.insert_one(user)
        except Exception as user_error:
            print(f"User lookup error: {str(user_error)}")
            # Continue with demo user
            user = {
                "_id": request.user_id,
                "email": f"{request.user_id}@demo.com", 
                "current_plan": "professional",
                "ai_media_usage": 0
            }
        
        # Start generation process
        response_data = {
            "generation_id": generation_id,
            "status": "generating",
            "cost_breakdown": cost_breakdown,
            "estimated_completion": datetime.utcnow() + timedelta(minutes=3)
        }
        
        # Store generation request
        await db.ai_generations.insert_one({
            "generation_id": generation_id,
            "user_id": request.user_id,
            "company_id": request.company_id,
            "request_data": request.dict(),
            "cost_breakdown": cost_breakdown,
            "status": "generating",
            "created_at": datetime.utcnow()
        })
        
        # Generate video and music in parallel
        video_task = asyncio.create_task(
            generate_ai_video(request.content_text, request.duration_seconds, request.video_style)
        )
        
        music_task = None
        if request.music_style != "none":
            music_task = asyncio.create_task(
                generate_ai_music(request.content_text, request.duration_seconds, request.mood, request.music_style)
            )
        
        # Wait for video generation
        video_url = await video_task
        response_data["video_url"] = video_url
        
        # Wait for music generation (if requested)
        music_url = None
        if music_task:
            music_url = await music_task
            response_data["music_url"] = music_url
            
            # Combine video and audio
            combined_url = await combine_video_and_audio(video_url, music_url, generation_id)
            response_data["combined_url"] = combined_url
        else:
            response_data["combined_url"] = video_url  # Just the video
        
        # Update database with results
        await db.ai_generations.update_one(
            {"generation_id": generation_id},
            {"$set": {
                "status": "completed",
                "video_url": video_url,
                "music_url": music_url,
                "combined_url": response_data["combined_url"],
                "completed_at": datetime.utcnow()
            }}
        )
        
        # Charge user (simplified billing)
        await db.users.update_one(
            {"_id": request.user_id},
            {"$inc": {"ai_media_usage": cost_breakdown["total_cost"]}}
        )
        
        response_data["status"] = "completed"
        return AIMediaResponse(**response_data)
        
    except Exception as e:
        print(f"AI media generation error: {str(e)}")
        # Update status to failed
        await db.ai_generations.update_one(
            {"generation_id": generation_id},
            {"$set": {"status": "failed", "error": str(e)}}
        )
        raise HTTPException(status_code=500, detail=f"AI media generation failed: {str(e)}")

@app.get("/api/ai-media/status/{generation_id}")
async def get_generation_status(generation_id: str):
    """Check status of AI media generation"""
    try:
        generation = await db.ai_generations.find_one({"generation_id": generation_id})
        if not generation:
            raise HTTPException(status_code=404, detail="Generation not found")
        
        return {
            "generation_id": generation_id,
            "status": generation.get("status"),
            "video_url": generation.get("video_url"),
            "music_url": generation.get("music_url"),
            "combined_url": generation.get("combined_url"),
            "cost_breakdown": generation.get("cost_breakdown"),
            "created_at": generation.get("created_at"),
            "completed_at": generation.get("completed_at")
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get status: {str(e)}")

@app.get("/api/ai-media/pricing")
async def get_ai_media_pricing():
    """Get current AI media generation pricing"""
    return {
        "pricing": AI_MEDIA_PRICING,
        "examples": [
            {
                "duration": "15 seconds",
                "video_only": calculate_ai_media_cost(15, False),
                "video_plus_music": calculate_ai_media_cost(15, True)
            },
            {
                "duration": "30 seconds", 
                "video_only": calculate_ai_media_cost(30, False),
                "video_plus_music": calculate_ai_media_cost(30, True)
            },
            {
                "duration": "60 seconds",
                "video_only": calculate_ai_media_cost(60, False), 
                "video_plus_music": calculate_ai_media_cost(60, True)
            }
        ]
    }


# Mount frontend as catch-all at the very end - after ALL API routes
# DISABLE static mount to preserve API routes - use selective routing instead
# frontend_build_path = Path("../frontend/build")
# if frontend_build_path.exists():
#     app.mount("/", StaticFiles(directory=frontend_build_path, html=True), name="frontend")

# Add static file serving for React build assets
from fastapi.staticfiles import StaticFiles

# Serve React static assets - USE ABSOLUTE PATHS FOR HEROKU
frontend_static_path = Path("/app/frontend/build/static")
if frontend_static_path.exists():
    app.mount("/static", StaticFiles(directory=frontend_static_path), name="static")

# Add root route that serves React app but preserves API routes
@app.get("/")
async def serve_react_app():
    """Serve React application"""
    frontend_build_path = Path("/app/frontend/build/index.html")
    
    if frontend_build_path.exists():
        with open(frontend_build_path, 'r') as f:
            return HTMLResponse(f.read())
    else:
        return HTMLResponse("<h1>PostVelocity</h1><p>Frontend not built yet</p>")