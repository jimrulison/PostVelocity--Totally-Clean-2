from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
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

# Platform configurations
PLATFORM_CONFIGS = {
    "instagram": {
        "max_chars": 2200,
        "hashtag_limit": 30,
        "style": "visual, engaging, story-driven",
        "format": "Short paragraphs, emojis, hashtags",
        "optimal_times": ["6:00", "12:00", "19:00"],
        "supports_video": True,
        "media_required": True
    },
    "tiktok": {
        "max_chars": 150,
        "hashtag_limit": 5,
        "style": "trendy, fun, educational",
        "format": "Hook + quick tip + call to action",
        "optimal_times": ["6:00", "10:00", "19:00"],
        "supports_video": True,
        "media_required": True
    },
    "facebook": {
        "max_chars": 63206,
        "hashtag_limit": 10,
        "style": "informative, community-focused",
        "format": "Detailed post with clear value",
        "optimal_times": ["9:00", "15:00", "21:00"],
        "supports_video": True,
        "media_required": False
    },
    "youtube": {
        "max_chars": 5000,
        "hashtag_limit": 15,
        "style": "educational, detailed",
        "format": "Title + Description + Timestamps",
        "optimal_times": ["14:00", "17:00", "20:00"],
        "supports_video": True,
        "media_required": True
    },
    "whatsapp": {
        "max_chars": 65536,
        "hashtag_limit": 5,
        "style": "personal, direct, actionable",
        "format": "Brief message with clear action",
        "optimal_times": ["8:00", "12:00", "18:00"],
        "supports_video": False,
        "media_required": False
    },
    "snapchat": {
        "max_chars": 250,
        "hashtag_limit": 3,
        "style": "casual, behind-the-scenes",
        "format": "Quick tip or insight",
        "optimal_times": ["10:00", "16:00", "22:00"],
        "supports_video": True,
        "media_required": True
    },
    "x": {
        "max_chars": 280,
        "hashtag_limit": 5,
        "style": "concise, impactful",
        "format": "Hook + value + hashtags",
        "optimal_times": ["8:00", "12:00", "17:00"],
        "supports_video": True,
        "media_required": False
    }
}

# Pydantic models
class Company(BaseModel):
    id: Optional[str] = None
    name: str
    industry: str
    website: Optional[str] = None
    description: Optional[str] = None
    target_audience: Optional[str] = None
    brand_voice: Optional[str] = None
    social_accounts: Optional[Dict[str, Dict[str, str]]] = {}
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    last_media_request: Optional[datetime] = None
    media_library_size: Optional[int] = 0

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

class MediaUploadRequest(BaseModel):
    company_id: str
    category: MediaCategory
    description: Optional[str] = None
    tags: Optional[List[str]] = []

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

class BlogPost(BaseModel):
    title: str
    content: str
    excerpt: str
    estimated_read_time: str
    seo_keywords: List[str]
    suggested_media: Optional[List[Dict[str, Any]]] = []
    media_placement_guide: Optional[str] = None

class NewsletterArticle(BaseModel):
    subject: str
    content: str
    sections: List[str]
    call_to_action: str
    target_audience: str
    suggested_media: Optional[List[Dict[str, Any]]] = []
    media_placement_guide: Optional[str] = None

class VideoScript(BaseModel):
    title: str
    script: str
    duration: str
    scenes: List[str]
    equipment_needed: List[str]
    target_platform: str
    required_media: Optional[List[Dict[str, Any]]] = []
    media_timing: Optional[str] = None

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

class MediaRequestPrompt(BaseModel):
    company_id: str
    company_name: str
    month: str
    year: int
    suggested_categories: List[str]
    current_media_count: int
    last_upload_date: Optional[datetime] = None
    recommendation: str

class CalendarEntry(BaseModel):
    date: str
    posts: List[ScheduledPost]
    total_posts: int

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
def create_platform_prompt_with_media(platform: str, company: dict, topic: str, audience_level: str, additional_context: str, available_media: List[dict]):
    config = PLATFORM_CONFIGS[platform]
    
    company_context = f"""
    Company: {company['name']}
    Industry: {company.get('industry', 'Construction and Environmental Training')}
    Target Audience: {company.get('target_audience', 'Construction workers, safety managers, environmental professionals')}
    Brand Voice: {company.get('brand_voice', 'Professional but accessible, safety-focused, educational')}
    Website: {company.get('website', '')}
    """
    
    media_context = ""
    if available_media:
        media_context = f"""
        Available Company Media:
        {chr(10).join([f"- {media['category']}: {media['description']} (Tags: {', '.join(media.get('tags', []))})" for media in available_media[:5]])}
        """
    
    industry_context = """
    Industry Focus: Construction and Environmental Training
    - Focus areas: Asbestos, Lead, Mold, OSHA compliance, Forklift safety
    - Key themes: Safety first, compliance, proper training, workplace protection
    - Tone: Professional but accessible, safety-focused, educational
    """
    
    prompt = f"""
    Create a {platform} post for {company['name']} about "{topic}".

    {company_context}

    {media_context}

    {industry_context}

    Platform Requirements:
    - Maximum {config['max_chars']} characters
    - Style: {config['style']}
    - Format: {config['format']}
    - Use maximum {config['hashtag_limit']} relevant hashtags
    - Audience level: {audience_level}
    - Optimal posting times: {config['optimal_times']}
    - Video support: {config['supports_video']}
    - Media required: {config['media_required']}
    
    Additional Context: {additional_context}

    Guidelines:
    1. Make it engaging and educational
    2. Include safety tips or compliance information when relevant
    3. Use industry-appropriate language
    4. Include a clear call-to-action
    5. For construction/environmental training, emphasize safety and proper procedures
    6. Keep it conversational but informative
    7. Include video suggestions if the platform supports video
    8. Reference available company media when appropriate
    9. Suggest specific media placement and timing
    
    Provide the content in this exact format:
    CONTENT: [the actual post content]
    HASHTAGS: [comma-separated hashtags]
    ENGAGEMENT_TIP: [one sentence tip for maximum engagement]
    POSTING_TIP: [one sentence tip for optimal posting time/strategy]
    VIDEO_SUGGESTION: [brief video idea if platform supports video, otherwise "Not applicable"]
    MEDIA_SUGGESTIONS: [comma-separated list of suggested media types/categories for this post]
    MEDIA_PLACEMENT: [instructions for where and how to place media in the post]
    """
    
    return prompt

def create_blog_prompt_with_media(company: dict, topic: str, additional_context: str, available_media: List[dict]):
    media_context = ""
    if available_media:
        media_context = f"""
        Available Company Media:
        {chr(10).join([f"- {media['category']}: {media['description']} (Tags: {', '.join(media.get('tags', []))})" for media in available_media[:10]])}
        """
    
    prompt = f"""
    Create a comprehensive blog post for {company['name']} about "{topic}".
    
    Company Context: {company.get('description', '')}
    Industry: {company.get('industry', 'Construction and Environmental Training')}
    Target Audience: {company.get('target_audience', 'Construction workers, safety managers, environmental professionals')}
    
    {media_context}
    
    Requirements:
    - 1200-1800 words
    - Professional but accessible tone
    - Include safety protocols and compliance information
    - Add practical tips and best practices
    - Include relevant statistics or regulations when applicable
    - Structure with clear headings and subheadings
    - End with a strong call-to-action
    - Include SEO-optimized keywords
    - Reference available company media where appropriate
    - Suggest specific media placement throughout the article
    
    Additional Context: {additional_context}
    
    Format the response as:
    TITLE: [compelling blog title]
    EXCERPT: [brief 2-sentence excerpt]
    CONTENT: [complete blog post with headings]
    READ_TIME: [estimated reading time]
    SEO_KEYWORDS: [comma-separated SEO keywords]
    MEDIA_SUGGESTIONS: [comma-separated list of suggested media types for this blog post]
    MEDIA_PLACEMENT: [detailed instructions for where to place media throughout the blog post]
    """
    
    return prompt

def create_newsletter_prompt_with_media(company: dict, topic: str, additional_context: str, available_media: List[dict]):
    media_context = ""
    if available_media:
        media_context = f"""
        Available Company Media:
        {chr(10).join([f"- {media['category']}: {media['description']} (Tags: {', '.join(media.get('tags', []))})" for media in available_media[:10]])}
        """
    
    prompt = f"""
    Create a comprehensive newsletter article for {company['name']} about "{topic}".
    
    Company Context: {company.get('description', '')}
    Industry: {company.get('industry', 'Construction and Environmental Training')}
    Target Audience: {company.get('target_audience', 'Construction workers, safety managers, environmental professionals')}
    
    {media_context}
    
    Requirements:
    - 1500-2000 words
    - In-depth analysis and expert insights
    - Include case studies or real-world examples
    - Reference current regulations and industry standards
    - Professional tone with actionable advice
    - Include relevant training opportunities or certifications
    - Add industry news or updates if relevant
    - Clear section structure
    - Incorporate available company media
    - Suggest specific media placement
    
    Additional Context: {additional_context}
    
    Format the response as:
    SUBJECT: [compelling email subject line]
    CONTENT: [complete newsletter article]
    SECTIONS: [comma-separated section titles]
    CALL_TO_ACTION: [specific call-to-action]
    TARGET_AUDIENCE: [specific audience description]
    MEDIA_SUGGESTIONS: [comma-separated list of suggested media types for this newsletter]
    MEDIA_PLACEMENT: [detailed instructions for where to place media throughout the newsletter]
    """
    
    return prompt

def create_video_script_prompt_with_media(company: dict, topic: str, platform: str, additional_context: str, available_media: List[dict]):
    config = PLATFORM_CONFIGS[platform]
    
    media_context = ""
    if available_media:
        media_context = f"""
        Available Company Media:
        {chr(10).join([f"- {media['category']}: {media['description']} (Tags: {', '.join(media.get('tags', []))})" for media in available_media[:10]])}
        """
    
    prompt = f"""
    Create a video script for {company['name']} about "{topic}" for {platform}.
    
    Company Context: {company.get('description', '')}
    Platform: {platform} (Style: {config['style']})
    
    {media_context}
    
    Requirements:
    - Duration: 60-90 seconds for TikTok/Instagram, 3-5 minutes for YouTube
    - Include hook, main content, and call-to-action
    - Visual cues and scene descriptions
    - Equipment recommendations
    - Safety demonstrations if applicable
    - Professional but engaging tone
    - Incorporate available company media
    - Specify when and how to use company media
    
    Additional Context: {additional_context}
    
    Format the response as:
    TITLE: [video title]
    SCRIPT: [complete script with scene descriptions]
    DURATION: [estimated duration]
    SCENES: [comma-separated scene descriptions]
    EQUIPMENT: [comma-separated equipment needed]
    PLATFORM: {platform}
    REQUIRED_MEDIA: [comma-separated list of specific media needed from company library]
    MEDIA_TIMING: [detailed instructions for when to use specific media in the video]
    """
    
    return prompt

async def generate_content_with_claude(prompt: str):
    try:
        response = client.messages.create(
            model="claude-3-5-haiku-latest",
            max_tokens=2000,
            temperature=0.7,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text
    except Exception as e:
        print(f"Claude API error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Claude API error: {str(e)}")

def parse_platform_content_with_media(content: str):
    lines = content.strip().split('\n')
    parsed = {
        'content': '',
        'hashtags': [],
        'engagement_tip': '',
        'posting_tip': '',
        'video_suggestion': '',
        'media_suggestions': [],
        'media_placement': ''
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
            parsed['hashtags'] = [tag.strip() for tag in hashtags_str.split(',') if tag.strip()]
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
        elif current_section and line:
            if current_section == 'content':
                parsed['content'] += ' ' + line
            elif current_section == 'engagement_tip':
                parsed['engagement_tip'] += ' ' + line
            elif current_section == 'posting_tip':
                parsed['posting_tip'] += ' ' + line
            elif current_section == 'video_suggestion':
                parsed['video_suggestion'] += ' ' + line
            elif current_section == 'media_placement':
                parsed['media_placement'] += ' ' + line
    
    return parsed

def parse_blog_content_with_media(content: str):
    lines = content.strip().split('\n')
    parsed = {
        'title': '',
        'excerpt': '',
        'content': '',
        'estimated_read_time': '',
        'seo_keywords': [],
        'media_suggestions': [],
        'media_placement_guide': ''
    }
    
    current_section = None
    for line in lines:
        line = line.strip()
        if line.startswith('TITLE:'):
            current_section = 'title'
            parsed['title'] = line.replace('TITLE:', '').strip()
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
        elif current_section and line:
            if current_section == 'content':
                parsed['content'] += '\n' + line
            elif current_section == 'excerpt':
                parsed['excerpt'] += ' ' + line
            elif current_section == 'title':
                parsed['title'] += ' ' + line
            elif current_section == 'estimated_read_time':
                parsed['estimated_read_time'] += ' ' + line
            elif current_section == 'media_placement_guide':
                parsed['media_placement_guide'] += ' ' + line
    
    # Set defaults if not found
    if not parsed['estimated_read_time']:
        parsed['estimated_read_time'] = '5 minutes'
    if not parsed['excerpt']:
        parsed['excerpt'] = 'A comprehensive guide to the topic.'
    if not parsed['title']:
        parsed['title'] = 'Untitled Post'
    
    return parsed

def parse_newsletter_content_with_media(content: str):
    lines = content.strip().split('\n')
    parsed = {
        'subject': '',
        'content': '',
        'sections': [],
        'call_to_action': '',
        'target_audience': '',
        'media_suggestions': [],
        'media_placement_guide': ''
    }
    
    current_section = None
    for line in lines:
        line = line.strip()
        if line.startswith('SUBJECT:'):
            current_section = 'subject'
            parsed['subject'] = line.replace('SUBJECT:', '').strip()
        elif line.startswith('CONTENT:'):
            current_section = 'content'
            parsed['content'] = line.replace('CONTENT:', '').strip()
        elif line.startswith('SECTIONS:'):
            current_section = 'sections'
            sections_str = line.replace('SECTIONS:', '').strip()
            parsed['sections'] = [s.strip() for s in sections_str.split(',') if s.strip()]
        elif line.startswith('CALL_TO_ACTION:'):
            current_section = 'call_to_action'
            parsed['call_to_action'] = line.replace('CALL_TO_ACTION:', '').strip()
        elif line.startswith('TARGET_AUDIENCE:'):
            current_section = 'target_audience'
            parsed['target_audience'] = line.replace('TARGET_AUDIENCE:', '').strip()
        elif line.startswith('MEDIA_SUGGESTIONS:'):
            current_section = 'media_suggestions'
            suggestions_str = line.replace('MEDIA_SUGGESTIONS:', '').strip()
            parsed['media_suggestions'] = [s.strip() for s in suggestions_str.split(',') if s.strip()]
        elif line.startswith('MEDIA_PLACEMENT:'):
            current_section = 'media_placement_guide'
            parsed['media_placement_guide'] = line.replace('MEDIA_PLACEMENT:', '').strip()
        elif current_section and line:
            if current_section == 'content':
                parsed['content'] += '\n' + line
            elif current_section == 'call_to_action':
                parsed['call_to_action'] += ' ' + line
            elif current_section == 'target_audience':
                parsed['target_audience'] += ' ' + line
            elif current_section == 'media_placement_guide':
                parsed['media_placement_guide'] += ' ' + line
    
    return parsed

def parse_video_script_with_media(content: str):
    lines = content.strip().split('\n')
    parsed = {
        'title': '',
        'script': '',
        'duration': '',
        'scenes': [],
        'equipment': [],
        'platform': '',
        'required_media': [],
        'media_timing': ''
    }
    
    current_section = None
    for line in lines:
        line = line.strip()
        if line.startswith('TITLE:'):
            current_section = 'title'
            parsed['title'] = line.replace('TITLE:', '').strip()
        elif line.startswith('SCRIPT:'):
            current_section = 'script'
            parsed['script'] = line.replace('SCRIPT:', '').strip()
        elif line.startswith('DURATION:'):
            current_section = 'duration'
            parsed['duration'] = line.replace('DURATION:', '').strip()
        elif line.startswith('SCENES:'):
            current_section = 'scenes'
            scenes_str = line.replace('SCENES:', '').strip()
            parsed['scenes'] = [s.strip() for s in scenes_str.split(',') if s.strip()]
        elif line.startswith('EQUIPMENT:'):
            current_section = 'equipment'
            equipment_str = line.replace('EQUIPMENT:', '').strip()
            parsed['equipment'] = [e.strip() for e in equipment_str.split(',') if e.strip()]
        elif line.startswith('PLATFORM:'):
            current_section = 'platform'
            parsed['platform'] = line.replace('PLATFORM:', '').strip()
        elif line.startswith('REQUIRED_MEDIA:'):
            current_section = 'required_media'
            media_str = line.replace('REQUIRED_MEDIA:', '').strip()
            parsed['required_media'] = [m.strip() for m in media_str.split(',') if m.strip()]
        elif line.startswith('MEDIA_TIMING:'):
            current_section = 'media_timing'
            parsed['media_timing'] = line.replace('MEDIA_TIMING:', '').strip()
        elif current_section and line:
            if current_section == 'script':
                parsed['script'] += '\n' + line
            elif current_section == 'title':
                parsed['title'] += ' ' + line
            elif current_section == 'duration':
                parsed['duration'] += ' ' + line
            elif current_section == 'media_timing':
                parsed['media_timing'] += ' ' + line
    
    return parsed

async def check_monthly_media_requests():
    """Check which companies need monthly media requests"""
    try:
        current_date = datetime.utcnow()
        one_month_ago = current_date - timedelta(days=30)
        
        # Find companies that haven't been asked for media in the last month
        companies_to_request = []
        async for company in db.companies.find():
            last_request = company.get('last_media_request')
            if not last_request or last_request < one_month_ago:
                # Count current media files
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
        "upload_dir_exists": UPLOAD_DIR.exists()
    }

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "Enhanced Social Media Content Generator with Media Management API is running"}

@app.get("/api/platforms")
async def get_platforms():
    return {
        "platforms": list(PLATFORM_CONFIGS.keys()),
        "configs": PLATFORM_CONFIGS
    }

# Company Management
@app.post("/api/companies")
async def create_company(company: Company):
    company_dict = company.dict()
    company_dict["created_at"] = datetime.utcnow()
    company_dict["updated_at"] = datetime.utcnow()
    company_dict["last_media_request"] = None
    company_dict["media_library_size"] = 0
    
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

# Media Management
@app.post("/api/companies/{company_id}/media/upload")
async def upload_media(
    company_id: str,
    file: UploadFile = File(...),
    category: MediaCategory = Form(...),
    description: str = Form(""),
    tags: str = Form("")
):
    """Upload media file for a company"""
    try:
        # Validate company exists
        company = await get_company_by_id(company_id)
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        
        # Validate file type
        if not file.content_type.startswith(('image/', 'video/')):
            raise HTTPException(status_code=400, detail="Only image and video files are supported")
        
        # Save file
        file_path, file_size, mime_type = save_uploaded_file(file, company_id, category.value)
        
        # Process image if needed
        metadata = {}
        if mime_type.startswith('image/'):
            metadata = process_image(file_path)
        
        # Create media record
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
            "upload_date": datetime.utcnow(),
            "is_active": True,
            "usage_count": 0,
            "metadata": metadata
        }
        
        result = await db.media_files.insert_one(media_record)
        media_record["id"] = str(result.inserted_id)
        del media_record["_id"]
        
        # Update company media library size
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
        # Get media record
        media = await db.media_files.find_one({"_id": ObjectId(media_id)})
        if not media:
            raise HTTPException(status_code=404, detail="Media file not found")
        
        # Mark as inactive instead of deleting
        await db.media_files.update_one(
            {"_id": ObjectId(media_id)},
            {"$set": {"is_active": False}}
        )
        
        # Update company media library size
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
        
        # Get current media count
        media_count = await db.media_files.count_documents({"company_id": company_id, "is_active": True})
        
        # Get media distribution by category
        pipeline = [
            {"$match": {"company_id": company_id, "is_active": True}},
            {"$group": {"_id": "$category", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        
        category_distribution = {}
        async for result in db.media_files.aggregate(pipeline):
            category_distribution[result["_id"]] = result["count"]
        
        # Suggest categories that are underrepresented
        all_categories = [cat.value for cat in MediaCategory]
        suggested_categories = [cat for cat in all_categories if category_distribution.get(cat, 0) < 3]
        
        current_date = datetime.utcnow()
        
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

# Enhanced Content Generation with Media
@app.post("/api/generate-content", response_model=ContentResponse)
async def generate_content(request: ContentRequest):
    try:
        # Get company information
        company = await get_company_by_id(request.company_id)
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        
        # Get available media if requested
        available_media = []
        if request.use_company_media:
            available_media = await get_company_media(request.company_id, limit=20)
        
        request_id = str(uuid.uuid4())
        generated_content = []
        
        # Generate content for each platform
        for platform in request.platforms:
            if platform not in PLATFORM_CONFIGS:
                raise HTTPException(status_code=400, detail=f"Unsupported platform: {platform}")
            
            prompt = create_platform_prompt_with_media(
                platform, 
                company, 
                request.topic, 
                request.audience_level,
                request.additional_context,
                available_media
            )
            
            raw_content = await generate_content_with_claude(prompt)
            parsed_content = parse_platform_content_with_media(raw_content)
            
            # Select relevant media for this platform
            platform_media = []
            if available_media and parsed_content.get('media_suggestions'):
                # Match media based on suggestions
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
                media_placement=parsed_content.get('media_placement', '')
            )
            
            generated_content.append(content_item)
        
        # Generate blog post if requested
        blog_post = None
        if request.generate_blog or len(request.platforms) > 4:
            blog_prompt = create_blog_prompt_with_media(company, request.topic, request.additional_context, available_media)
            blog_raw = await generate_content_with_claude(blog_prompt)
            blog_parsed = parse_blog_content_with_media(blog_raw)
            
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
                **blog_parsed,
                suggested_media=blog_media
            )
        
        # Generate newsletter article if requested
        newsletter_article = None
        if request.generate_newsletter or len(request.platforms) > 5:
            newsletter_prompt = create_newsletter_prompt_with_media(company, request.topic, request.additional_context, available_media)
            newsletter_raw = await generate_content_with_claude(newsletter_prompt)
            newsletter_parsed = parse_newsletter_content_with_media(newsletter_raw)
            
            # Select media for newsletter
            newsletter_media = []
            if available_media and newsletter_parsed.get('media_suggestions'):
                for suggestion in newsletter_parsed['media_suggestions']:
                    for media in available_media:
                        if any(tag.lower() in suggestion.lower() for tag in media.get('tags', [])) or \
                           media.get('category', '').lower() in suggestion.lower():
                            newsletter_media.append({
                                "id": media["id"],
                                "filename": media["filename"],
                                "file_path": media["file_path"],
                                "media_type": media["media_type"],
                                "category": media["category"],
                                "description": media["description"]
                            })
            
            newsletter_article = NewsletterArticle(
                **newsletter_parsed,
                suggested_media=newsletter_media
            )
        
        # Generate video scripts if requested
        video_scripts = []
        if request.generate_video_script:
            video_platforms = [p for p in request.platforms if PLATFORM_CONFIGS[p]['supports_video']]
            for platform in video_platforms[:3]:  # Limit to 3 video scripts
                video_prompt = create_video_script_prompt_with_media(company, request.topic, platform, request.additional_context, available_media)
                video_raw = await generate_content_with_claude(video_prompt)
                video_parsed = parse_video_script_with_media(video_raw)
                
                # Select media for video script
                video_media = []
                if available_media and video_parsed.get('required_media'):
                    for requirement in video_parsed['required_media']:
                        for media in available_media:
                            if any(tag.lower() in requirement.lower() for tag in media.get('tags', [])) or \
                               media.get('category', '').lower() in requirement.lower():
                                video_media.append({
                                    "id": media["id"],
                                    "filename": media["filename"],
                                    "file_path": media["file_path"],
                                    "media_type": media["media_type"],
                                    "category": media["category"],
                                    "description": media["description"]
                                })
                
                video_script = VideoScript(
                    title=video_parsed['title'],
                    script=video_parsed['script'],
                    duration=video_parsed['duration'],
                    scenes=video_parsed['scenes'],
                    equipment_needed=video_parsed['equipment'],
                    target_platform=video_parsed['platform'],
                    required_media=video_media,
                    media_timing=video_parsed['media_timing']
                )
                video_scripts.append(video_script)
        
        # Update usage count for selected media
        used_media_ids = set()
        for content in generated_content:
            for media in content.suggested_media:
                used_media_ids.add(media["id"])
        
        if blog_post:
            for media in blog_post.suggested_media:
                used_media_ids.add(media["id"])
        
        if newsletter_article:
            for media in newsletter_article.suggested_media:
                used_media_ids.add(media["id"])
        
        for script in video_scripts:
            for media in script.required_media:
                used_media_ids.add(media["id"])
        
        # Update usage count in database
        for media_id in used_media_ids:
            await db.media_files.update_one(
                {"_id": ObjectId(media_id)},
                {"$inc": {"usage_count": 1}, "$set": {"last_used": datetime.utcnow()}}
            )
        
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
        
        # Save content to database
        content_doc = {
            "request_id": request_id,
            "company_id": request.company_id,
            "topic": request.topic,
            "generated_content": [content.dict() for content in generated_content],
            "blog_post": blog_post.dict() if blog_post else None,
            "newsletter_article": newsletter_article.dict() if newsletter_article else None,
            "video_scripts": [script.dict() for script in video_scripts] if video_scripts else None,
            "media_used": list(used_media_ids),
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
            created_at=datetime.utcnow().isoformat()
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating content: {str(e)}")

# Content Scheduling with Media
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
    
    # Group posts by date
    calendar_data = {}
    for post in posts:
        date_str = post["scheduled_time"].strftime("%Y-%m-%d")
        if date_str not in calendar_data:
            calendar_data[date_str] = []
        calendar_data[date_str].append(post)
    
    # Convert to CalendarEntry format
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

# Analytics with Media Performance
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

@app.get("/api/reports/monthly/{company_id}")
async def get_monthly_report(company_id: str, month: int, year: int):
    start_date = datetime(year, month, 1)
    end_date = datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
    
    # Get analytics for the month
    analytics = []
    async for record in db.analytics.find({
        "company_id": company_id,
        "recorded_at": {"$gte": start_date, "$lt": end_date}
    }):
        analytics.append(record)
    
    # Get media performance for the month
    media_performance = {}
    async for media in db.media_files.find({
        "company_id": company_id,
        "last_used": {"$gte": start_date, "$lt": end_date}
    }).sort("usage_count", -1):
        media_performance[media["category"]] = media_performance.get(media["category"], 0) + media.get("usage_count", 0)
    
    # Calculate metrics
    total_posts = len(analytics)
    total_engagement = sum(record.get("likes", 0) + record.get("shares", 0) + record.get("comments", 0) for record in analytics)
    
    # Get top performing posts
    top_posts = sorted(analytics, key=lambda x: x.get("engagement_rate", 0), reverse=True)[:5]
    
    # Platform performance
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
    
    # Calculate averages
    for platform in platform_performance:
        if platform_performance[platform]["total_posts"] > 0:
            platform_performance[platform]["avg_engagement_rate"] = platform_performance[platform]["total_engagement"] / platform_performance[platform]["total_posts"]
    
    # Generate recommendations including media
    recommendations = [
        "Focus on video content for higher engagement",
        "Post during optimal times for your audience",
        "Use trending hashtags relevant to your industry",
        "Engage with comments within first hour of posting",
        "Create more educational content about safety protocols"
    ]
    
    # Add media-specific recommendations
    media_recommendations = []
    if media_performance:
        top_category = max(media_performance, key=media_performance.get)
        media_recommendations.append(f"Your {top_category} images perform best - upload more similar content")
        media_recommendations.append("Consider creating video versions of your most popular images")
    else:
        media_recommendations.append("Start uploading company photos and videos to increase engagement")
        media_recommendations.append("Visual content can increase engagement by up to 80%")
    
    # Identify viral potential posts
    viral_potential = [record.get("post_id", "") for record in analytics if record.get("engagement_rate", 0) > 0.05]
    
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
        media_recommendations=media_recommendations
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
            "Chemical Storage Safety"
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
            "Government"
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
        ]
    }
    return examples

# Background task for posting scheduled content
async def publish_scheduled_posts():
    """Background task to publish scheduled posts"""
    while True:
        try:
            current_time = datetime.utcnow()
            
            # Find posts that should be published
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
            
            # Sleep for 1 minute before checking again
            await asyncio.sleep(60)
            
        except Exception as e:
            print(f"Error in publish_scheduled_posts: {e}")
            await asyncio.sleep(60)

# Background task for monthly media requests
async def send_monthly_media_requests():
    """Background task to send monthly media requests"""
    while True:
        try:
            # Check every day at 9 AM
            current_time = datetime.utcnow()
            if current_time.hour == 9 and current_time.minute < 5:
                requests = await check_monthly_media_requests()
                
                for request in requests:
                    # Mark as sent (in real implementation, you'd send actual emails/notifications)
                    await db.companies.update_one(
                        {"_id": ObjectId(request["company_id"])},
                        {"$set": {"last_media_request": current_time}}
                    )
                    print(f"Sent media request to {request['company_name']}")
            
            # Sleep for 1 hour before checking again
            await asyncio.sleep(3600)
            
        except Exception as e:
            print(f"Error in send_monthly_media_requests: {e}")
            await asyncio.sleep(3600)

# Start background tasks
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(publish_scheduled_posts())
    asyncio.create_task(send_monthly_media_requests())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)