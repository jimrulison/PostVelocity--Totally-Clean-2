from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import anthropic
import os
from datetime import datetime
import uuid
import json
from dotenv import load_dotenv

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

# Initialize Claude client
claude_api_key = os.getenv("CLAUDE_API_KEY")
print(f"Claude API Key loaded: {claude_api_key is not None}")
if not claude_api_key:
    raise ValueError("CLAUDE_API_KEY environment variable is not set")

client = anthropic.Anthropic(
    api_key=claude_api_key
)

# Platform configurations
PLATFORM_CONFIGS = {
    "instagram": {
        "max_chars": 2200,
        "hashtag_limit": 30,
        "style": "visual, engaging, story-driven",
        "format": "Short paragraphs, emojis, hashtags"
    },
    "tiktok": {
        "max_chars": 150,
        "hashtag_limit": 5,
        "style": "trendy, fun, educational",
        "format": "Hook + quick tip + call to action"
    },
    "facebook": {
        "max_chars": 63206,
        "hashtag_limit": 10,
        "style": "informative, community-focused",
        "format": "Detailed post with clear value"
    },
    "youtube": {
        "max_chars": 5000,
        "hashtag_limit": 15,
        "style": "educational, detailed",
        "format": "Title + Description + Timestamps"
    },
    "whatsapp": {
        "max_chars": 65536,
        "hashtag_limit": 5,
        "style": "personal, direct, actionable",
        "format": "Brief message with clear action"
    },
    "snapchat": {
        "max_chars": 250,
        "hashtag_limit": 3,
        "style": "casual, behind-the-scenes",
        "format": "Quick tip or insight"
    },
    "x": {
        "max_chars": 280,
        "hashtag_limit": 5,
        "style": "concise, impactful",
        "format": "Hook + value + hashtags"
    }
}

class ContentRequest(BaseModel):
    company_name: str
    topic: str
    platforms: List[str]
    audience_level: Optional[str] = "general"
    additional_context: Optional[str] = ""

class GeneratedContent(BaseModel):
    platform: str
    content: str
    hashtags: List[str]
    estimated_engagement: str
    posting_tips: str

class ContentResponse(BaseModel):
    request_id: str
    company_name: str
    topic: str
    generated_content: List[GeneratedContent]
    blog_post: Optional[str] = None
    newsletter_article: Optional[str] = None
    created_at: str

def create_platform_prompt(platform: str, company_name: str, topic: str, audience_level: str, additional_context: str):
    config = PLATFORM_CONFIGS[platform]
    
    industry_context = """
    Industry Context: Construction and Environmental Training
    - Focus areas: Asbestos, Lead, Mold, OSHA compliance, Forklift safety
    - Target audience: Construction workers, safety managers, environmental professionals
    - Tone: Professional but accessible, safety-focused, educational
    - Key themes: Safety first, compliance, proper training, workplace protection
    """
    
    prompt = f"""
    Create a {platform} post for {company_name} about "{topic}".

    {industry_context}

    Platform Requirements:
    - Maximum {config['max_chars']} characters
    - Style: {config['style']}
    - Format: {config['format']}
    - Use maximum {config['hashtag_limit']} relevant hashtags
    - Audience level: {audience_level}
    
    Additional Context: {additional_context}

    Guidelines:
    1. Make it engaging and educational
    2. Include safety tips or compliance information when relevant
    3. Use industry-appropriate language
    4. Include a clear call-to-action
    5. For construction/environmental training, emphasize safety and proper procedures
    6. Keep it conversational but informative
    
    Provide the content in this exact format:
    CONTENT: [the actual post content]
    HASHTAGS: [comma-separated hashtags]
    ENGAGEMENT_TIP: [one sentence tip for maximum engagement]
    POSTING_TIP: [one sentence tip for optimal posting time/strategy]
    """
    
    return prompt

def create_blog_prompt(company_name: str, topic: str, additional_context: str):
    prompt = f"""
    Create a comprehensive blog post for {company_name} about "{topic}".
    
    Industry Context: Construction and Environmental Training
    - Focus areas: Asbestos, Lead, Mold, OSHA compliance, Forklift safety
    - Target audience: Construction workers, safety managers, environmental professionals
    
    Requirements:
    - 800-1200 words
    - Professional but accessible tone
    - Include safety protocols and compliance information
    - Add practical tips and best practices
    - Include relevant statistics or regulations when applicable
    - Structure with clear headings and subheadings
    - End with a strong call-to-action
    
    Additional Context: {additional_context}
    
    Format as a complete blog post with title, introduction, main content sections, and conclusion.
    """
    
    return prompt

def create_newsletter_prompt(company_name: str, topic: str, additional_context: str):
    prompt = f"""
    Create a newsletter article for {company_name} about "{topic}".
    
    Industry Context: Construction and Environmental Training
    - Focus areas: Asbestos, Lead, Mold, OSHA compliance, Forklift safety
    - Target audience: Construction workers, safety managers, environmental professionals
    
    Requirements:
    - 1200-1500 words
    - In-depth analysis and expert insights
    - Include case studies or real-world examples
    - Reference current regulations and industry standards
    - Professional tone with actionable advice
    - Include relevant training opportunities or certifications
    - Add industry news or updates if relevant
    
    Additional Context: {additional_context}
    
    Format as a complete newsletter article with compelling headline, executive summary, detailed content sections, and conclusion with next steps.
    """
    
    return prompt

async def generate_content_with_claude(prompt: str):
    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
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
        'posting_tip': ''
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
        elif current_section and line:
            if current_section == 'content':
                parsed['content'] += ' ' + line
            elif current_section == 'engagement_tip':
                parsed['engagement_tip'] += ' ' + line
            elif current_section == 'posting_tip':
                parsed['posting_tip'] += ' ' + line
    
    return parsed

@app.get("/api/debug")
async def debug():
    return {
        "claude_api_key_exists": os.getenv("CLAUDE_API_KEY") is not None,
        "claude_api_key_length": len(os.getenv("CLAUDE_API_KEY", "")),
        "env_vars": list(os.environ.keys())
    }

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "Social Media Content Generator API is running"}

@app.get("/api/platforms")
async def get_platforms():
    return {
        "platforms": list(PLATFORM_CONFIGS.keys()),
        "configs": PLATFORM_CONFIGS
    }

@app.post("/api/generate-content", response_model=ContentResponse)
async def generate_content(request: ContentRequest):
    try:
        request_id = str(uuid.uuid4())
        generated_content = []
        
        # Generate content for each platform
        for platform in request.platforms:
            if platform not in PLATFORM_CONFIGS:
                raise HTTPException(status_code=400, detail=f"Unsupported platform: {platform}")
            
            prompt = create_platform_prompt(
                platform, 
                request.company_name, 
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
                posting_tips=parsed_content['posting_tip']
            )
            
            generated_content.append(content_item)
        
        # Generate blog post if requested
        blog_post = None
        if len(request.platforms) > 3:  # Generate blog for comprehensive requests
            blog_prompt = create_blog_prompt(request.company_name, request.topic, request.additional_context)
            blog_post = await generate_content_with_claude(blog_prompt)
        
        # Generate newsletter article if requested
        newsletter_article = None
        if len(request.platforms) > 5:  # Generate newsletter for extensive requests
            newsletter_prompt = create_newsletter_prompt(request.company_name, request.topic, request.additional_context)
            newsletter_article = await generate_content_with_claude(newsletter_prompt)
        
        response = ContentResponse(
            request_id=request_id,
            company_name=request.company_name,
            topic=request.topic,
            generated_content=generated_content,
            blog_post=blog_post,
            newsletter_article=newsletter_article,
            created_at=datetime.now().isoformat()
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating content: {str(e)}")

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
            "Emergency Response Procedures"
        ],
        "audience_levels": [
            "beginner",
            "intermediate", 
            "advanced",
            "management",
            "general"
        ]
    }
    return examples

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)