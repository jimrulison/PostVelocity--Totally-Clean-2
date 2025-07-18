from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
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

# Platform configurations
PLATFORM_CONFIGS = {
    "instagram": {
        "max_chars": 2200,
        "hashtag_limit": 30,
        "style": "visual, engaging, story-driven",
        "format": "Short paragraphs, emojis, hashtags",
        "optimal_times": ["6:00", "12:00", "19:00"],
        "supports_video": True
    },
    "tiktok": {
        "max_chars": 150,
        "hashtag_limit": 5,
        "style": "trendy, fun, educational",
        "format": "Hook + quick tip + call to action",
        "optimal_times": ["6:00", "10:00", "19:00"],
        "supports_video": True
    },
    "facebook": {
        "max_chars": 63206,
        "hashtag_limit": 10,
        "style": "informative, community-focused",
        "format": "Detailed post with clear value",
        "optimal_times": ["9:00", "15:00", "21:00"],
        "supports_video": True
    },
    "youtube": {
        "max_chars": 5000,
        "hashtag_limit": 15,
        "style": "educational, detailed",
        "format": "Title + Description + Timestamps",
        "optimal_times": ["14:00", "17:00", "20:00"],
        "supports_video": True
    },
    "whatsapp": {
        "max_chars": 65536,
        "hashtag_limit": 5,
        "style": "personal, direct, actionable",
        "format": "Brief message with clear action",
        "optimal_times": ["8:00", "12:00", "18:00"],
        "supports_video": False
    },
    "snapchat": {
        "max_chars": 250,
        "hashtag_limit": 3,
        "style": "casual, behind-the-scenes",
        "format": "Quick tip or insight",
        "optimal_times": ["10:00", "16:00", "22:00"],
        "supports_video": True
    },
    "x": {
        "max_chars": 280,
        "hashtag_limit": 5,
        "style": "concise, impactful",
        "format": "Hook + value + hashtags",
        "optimal_times": ["8:00", "12:00", "17:00"],
        "supports_video": True
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

class ContentRequest(BaseModel):
    company_id: str
    topic: str
    platforms: List[str]
    audience_level: Optional[str] = "general"
    additional_context: Optional[str] = ""
    generate_blog: Optional[bool] = False
    generate_newsletter: Optional[bool] = False
    generate_video_script: Optional[bool] = False

class GeneratedContent(BaseModel):
    platform: str
    content: str
    hashtags: List[str]
    estimated_engagement: str
    posting_tips: str
    video_suggestions: Optional[str] = None
    optimal_posting_times: List[str]

class BlogPost(BaseModel):
    title: str
    content: str
    excerpt: str
    estimated_read_time: str
    seo_keywords: List[str]

class NewsletterArticle(BaseModel):
    subject: str
    content: str
    sections: List[str]
    call_to_action: str
    target_audience: str

class VideoScript(BaseModel):
    title: str
    script: str
    duration: str
    scenes: List[str]
    equipment_needed: List[str]
    target_platform: str

class ContentResponse(BaseModel):
    request_id: str
    company_id: str
    topic: str
    generated_content: List[GeneratedContent]
    blog_post: Optional[BlogPost] = None
    newsletter_article: Optional[NewsletterArticle] = None
    video_scripts: Optional[List[VideoScript]] = None
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
    created_at: Optional[datetime] = None
    published_at: Optional[datetime] = None
    engagement_metrics: Optional[Dict[str, Any]] = None

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

# Content generation functions
def create_platform_prompt(platform: str, company: dict, topic: str, audience_level: str, additional_context: str):
    config = PLATFORM_CONFIGS[platform]
    
    company_context = f"""
    Company: {company['name']}
    Industry: {company.get('industry', 'Construction and Environmental Training')}
    Target Audience: {company.get('target_audience', 'Construction workers, safety managers, environmental professionals')}
    Brand Voice: {company.get('brand_voice', 'Professional but accessible, safety-focused, educational')}
    Website: {company.get('website', '')}
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

    {industry_context}

    Platform Requirements:
    - Maximum {config['max_chars']} characters
    - Style: {config['style']}
    - Format: {config['format']}
    - Use maximum {config['hashtag_limit']} relevant hashtags
    - Audience level: {audience_level}
    - Optimal posting times: {config['optimal_times']}
    - Video support: {config['supports_video']}
    
    Additional Context: {additional_context}

    Guidelines:
    1. Make it engaging and educational
    2. Include safety tips or compliance information when relevant
    3. Use industry-appropriate language
    4. Include a clear call-to-action
    5. For construction/environmental training, emphasize safety and proper procedures
    6. Keep it conversational but informative
    7. Include video suggestions if the platform supports video
    
    Provide the content in this exact format:
    CONTENT: [the actual post content]
    HASHTAGS: [comma-separated hashtags]
    ENGAGEMENT_TIP: [one sentence tip for maximum engagement]
    POSTING_TIP: [one sentence tip for optimal posting time/strategy]
    VIDEO_SUGGESTION: [brief video idea if platform supports video, otherwise "Not applicable"]
    """
    
    return prompt

def create_blog_prompt(company: dict, topic: str, additional_context: str):
    prompt = f"""
    Create a comprehensive blog post for {company['name']} about "{topic}".
    
    Company Context: {company.get('description', '')}
    Industry: {company.get('industry', 'Construction and Environmental Training')}
    Target Audience: {company.get('target_audience', 'Construction workers, safety managers, environmental professionals')}
    
    Requirements:
    - 1200-1800 words
    - Professional but accessible tone
    - Include safety protocols and compliance information
    - Add practical tips and best practices
    - Include relevant statistics or regulations when applicable
    - Structure with clear headings and subheadings
    - End with a strong call-to-action
    - Include SEO-optimized keywords
    
    Additional Context: {additional_context}
    
    Format the response as:
    TITLE: [compelling blog title]
    EXCERPT: [brief 2-sentence excerpt]
    CONTENT: [complete blog post with headings]
    READ_TIME: [estimated reading time]
    SEO_KEYWORDS: [comma-separated SEO keywords]
    """
    
    return prompt

def create_newsletter_prompt(company: dict, topic: str, additional_context: str):
    prompt = f"""
    Create a comprehensive newsletter article for {company['name']} about "{topic}".
    
    Company Context: {company.get('description', '')}
    Industry: {company.get('industry', 'Construction and Environmental Training')}
    Target Audience: {company.get('target_audience', 'Construction workers, safety managers, environmental professionals')}
    
    Requirements:
    - 1500-2000 words
    - In-depth analysis and expert insights
    - Include case studies or real-world examples
    - Reference current regulations and industry standards
    - Professional tone with actionable advice
    - Include relevant training opportunities or certifications
    - Add industry news or updates if relevant
    - Clear section structure
    
    Additional Context: {additional_context}
    
    Format the response as:
    SUBJECT: [compelling email subject line]
    CONTENT: [complete newsletter article]
    SECTIONS: [comma-separated section titles]
    CALL_TO_ACTION: [specific call-to-action]
    TARGET_AUDIENCE: [specific audience description]
    """
    
    return prompt

def create_video_script_prompt(company: dict, topic: str, platform: str, additional_context: str):
    config = PLATFORM_CONFIGS[platform]
    
    prompt = f"""
    Create a video script for {company['name']} about "{topic}" for {platform}.
    
    Company Context: {company.get('description', '')}
    Platform: {platform} (Style: {config['style']})
    
    Requirements:
    - Duration: 60-90 seconds for TikTok/Instagram, 3-5 minutes for YouTube
    - Include hook, main content, and call-to-action
    - Visual cues and scene descriptions
    - Equipment recommendations
    - Safety demonstrations if applicable
    - Professional but engaging tone
    
    Additional Context: {additional_context}
    
    Format the response as:
    TITLE: [video title]
    SCRIPT: [complete script with scene descriptions]
    DURATION: [estimated duration]
    SCENES: [comma-separated scene descriptions]
    EQUIPMENT: [comma-separated equipment needed]
    PLATFORM: {platform}
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

def parse_platform_content(content: str):
    lines = content.strip().split('\n')
    parsed = {
        'content': '',
        'hashtags': [],
        'engagement_tip': '',
        'posting_tip': '',
        'video_suggestion': ''
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
        elif current_section and line:
            if current_section == 'content':
                parsed['content'] += ' ' + line
            elif current_section == 'engagement_tip':
                parsed['engagement_tip'] += ' ' + line
            elif current_section == 'posting_tip':
                parsed['posting_tip'] += ' ' + line
            elif current_section == 'video_suggestion':
                parsed['video_suggestion'] += ' ' + line
    
    return parsed

def parse_blog_content(content: str):
    lines = content.strip().split('\n')
    parsed = {
        'title': '',
        'excerpt': '',
        'content': '',
        'read_time': '',
        'seo_keywords': []
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
            current_section = 'read_time'
            parsed['read_time'] = line.replace('READ_TIME:', '').strip()
        elif line.startswith('SEO_KEYWORDS:'):
            current_section = 'seo_keywords'
            keywords_str = line.replace('SEO_KEYWORDS:', '').strip()
            parsed['seo_keywords'] = [kw.strip() for kw in keywords_str.split(',') if kw.strip()]
        elif current_section and line:
            if current_section == 'content':
                parsed['content'] += '\n' + line
            elif current_section == 'excerpt':
                parsed['excerpt'] += ' ' + line
            elif current_section == 'title':
                parsed['title'] += ' ' + line
            elif current_section == 'read_time':
                parsed['read_time'] += ' ' + line
    
    return parsed

def parse_newsletter_content(content: str):
    lines = content.strip().split('\n')
    parsed = {
        'subject': '',
        'content': '',
        'sections': [],
        'call_to_action': '',
        'target_audience': ''
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
        elif current_section and line:
            if current_section == 'content':
                parsed['content'] += '\n' + line
            elif current_section == 'call_to_action':
                parsed['call_to_action'] += ' ' + line
            elif current_section == 'target_audience':
                parsed['target_audience'] += ' ' + line
    
    return parsed

def parse_video_script(content: str):
    lines = content.strip().split('\n')
    parsed = {
        'title': '',
        'script': '',
        'duration': '',
        'scenes': [],
        'equipment': [],
        'platform': ''
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
        elif current_section and line:
            if current_section == 'script':
                parsed['script'] += '\n' + line
            elif current_section == 'title':
                parsed['title'] += ' ' + line
            elif current_section == 'duration':
                parsed['duration'] += ' ' + line
    
    return parsed

# API Routes
@app.get("/api/debug")
async def debug():
    return {
        "claude_api_key_exists": os.getenv("CLAUDE_API_KEY") is not None,
        "claude_api_key_length": len(os.getenv("CLAUDE_API_KEY", "")),
        "mongo_connected": True
    }

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "Enhanced Social Media Content Generator API is running"}

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

# Enhanced Content Generation
@app.post("/api/generate-content", response_model=ContentResponse)
async def generate_content(request: ContentRequest):
    try:
        # Get company information
        company = await get_company_by_id(request.company_id)
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        
        request_id = str(uuid.uuid4())
        generated_content = []
        
        # Generate content for each platform
        for platform in request.platforms:
            if platform not in PLATFORM_CONFIGS:
                raise HTTPException(status_code=400, detail=f"Unsupported platform: {platform}")
            
            prompt = create_platform_prompt(
                platform, 
                company, 
                request.topic, 
                request.audience_level,
                request.additional_context
            )
            
            raw_content = await generate_content_with_claude(prompt)
            parsed_content = parse_platform_content(raw_content)
            
            content_item = GeneratedContent(
                platform=platform,
                content=parsed_content['content'],
                hashtags=parsed_content['hashtags'],
                estimated_engagement=parsed_content['engagement_tip'],
                posting_tips=parsed_content['posting_tip'],
                video_suggestions=parsed_content['video_suggestion'],
                optimal_posting_times=PLATFORM_CONFIGS[platform]['optimal_times']
            )
            
            generated_content.append(content_item)
        
        # Generate blog post if requested
        blog_post = None
        if request.generate_blog or len(request.platforms) > 4:
            blog_prompt = create_blog_prompt(company, request.topic, request.additional_context)
            blog_raw = await generate_content_with_claude(blog_prompt)
            blog_parsed = parse_blog_content(blog_raw)
            blog_post = BlogPost(**blog_parsed)
        
        # Generate newsletter article if requested
        newsletter_article = None
        if request.generate_newsletter or len(request.platforms) > 5:
            newsletter_prompt = create_newsletter_prompt(company, request.topic, request.additional_context)
            newsletter_raw = await generate_content_with_claude(newsletter_prompt)
            newsletter_parsed = parse_newsletter_content(newsletter_raw)
            newsletter_article = NewsletterArticle(**newsletter_parsed)
        
        # Generate video scripts if requested
        video_scripts = []
        if request.generate_video_script:
            video_platforms = [p for p in request.platforms if PLATFORM_CONFIGS[p]['supports_video']]
            for platform in video_platforms[:3]:  # Limit to 3 video scripts
                video_prompt = create_video_script_prompt(company, request.topic, platform, request.additional_context)
                video_raw = await generate_content_with_claude(video_prompt)
                video_parsed = parse_video_script(video_raw)
                video_script = VideoScript(**video_parsed)
                video_scripts.append(video_script)
        
        # Save content to database
        content_doc = {
            "request_id": request_id,
            "company_id": request.company_id,
            "topic": request.topic,
            "generated_content": [content.dict() for content in generated_content],
            "blog_post": blog_post.dict() if blog_post else None,
            "newsletter_article": newsletter_article.dict() if newsletter_article else None,
            "video_scripts": [script.dict() for script in video_scripts] if video_scripts else None,
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
            created_at=datetime.utcnow().isoformat()
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating content: {str(e)}")

# Content Scheduling
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

# Analytics
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
    
    # Generate recommendations
    recommendations = [
        "Focus on video content for higher engagement",
        "Post during optimal times for your audience",
        "Use trending hashtags relevant to your industry",
        "Engage with comments within first hour of posting",
        "Create more educational content about safety protocols"
    ]
    
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
        viral_potential_posts=viral_potential
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

# Start background task
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(publish_scheduled_posts())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)