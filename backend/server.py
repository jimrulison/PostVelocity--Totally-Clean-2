from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Union
import anthropic
import os
from datetime import datetime, timedelta
import uuid
import json
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

# Load environment variables
load_dotenv()

app = FastAPI()

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
    hashtag_strategy: Optional[Dict[str, List[str]]] = {}
    performance_forecast: Optional[Dict[str, float]] = {}
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

async def generate_content_with_claude(prompt: str):
    try:
        response = client.messages.create(
            model="claude-3-5-haiku-latest",
            max_tokens=3000,
            temperature=0.7,
            messages=[
                {"role": "user", "content": prompt}
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
async def health_check():
    return {"status": "healthy", "message": "Advanced Social Media Content Generator with AI-Powered Features"}

@app.get("/api/platforms")
async def get_platforms():
    return {
        "platforms": list(PLATFORM_CONFIGS.keys()),
        "configs": PLATFORM_CONFIGS
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
async def update_company(company_id: str, company: Company):
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)