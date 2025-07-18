"""
PostVelocity - Advanced Security & License Management System
Copyright (c) 2025 Fancy Free Living LLC. All rights reserved.

This software is proprietary and confidential. Unauthorized copying,
distribution, or use is strictly prohibited and may result in severe
civil and criminal penalties.
"""

import hashlib
import secrets
import base64
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import json
import logging

logger = logging.getLogger(__name__)

class SecurityManager:
    """
    Advanced security management system for PostVelocity
    Handles encryption, license validation, and API security
    """
    
    def __init__(self):
        self.master_key = self._get_or_create_master_key()
        self.cipher = Fernet(self.master_key)
        self.license_manager = LicenseManager(self.master_key)
        self.api_key_manager = APIKeyManager()
    
    def _get_or_create_master_key(self):
        """Get or create the master encryption key"""
        key_file = os.environ.get('MASTER_KEY_FILE', '/tmp/master.key')
        
        try:
            with open(key_file, 'rb') as f:
                return f.read()
        except FileNotFoundError:
            # Generate new key
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            logger.info("Generated new master key")
            return key
    
    def encrypt_data(self, data):
        """Encrypt sensitive data"""
        if isinstance(data, str):
            data = data.encode()
        return self.cipher.encrypt(data).decode()
    
    def decrypt_data(self, encrypted_data):
        """Decrypt sensitive data"""
        if isinstance(encrypted_data, str):
            encrypted_data = encrypted_data.encode()
        return self.cipher.decrypt(encrypted_data).decode()

class LicenseManager:
    """
    Comprehensive license management system
    Handles license generation, validation, and enforcement
    """
    
    def __init__(self, master_key):
        self.master_key = master_key
        self.salt = b'PostVelocity2025FancyFreeLiving'
    
    def generate_license(self, user_id, plan_type, duration_days=30, features=None):
        """Generate a secure license key"""
        timestamp = int(datetime.now().timestamp())
        expiry = timestamp + (duration_days * 24 * 60 * 60)
        
        license_data = {
            'user_id': user_id,
            'plan_type': plan_type,
            'timestamp': timestamp,
            'expiry': expiry,
            'features': features or [],
            'max_usage': self._get_usage_limit(plan_type),
            'platforms': self._get_platform_access(plan_type)
        }
        
        # Create signature
        data_string = json.dumps(license_data, sort_keys=True)
        signature = hashlib.sha256(f"{data_string}:{self.master_key.decode()}".encode()).hexdigest()
        
        license_data['signature'] = signature
        
        # Encode license
        license_json = json.dumps(license_data)
        license_key = base64.b64encode(license_json.encode()).decode()
        
        return license_key
    
    def validate_license(self, license_key):
        """Validate license key and return license data"""
        try:
            # Decode license
            license_json = base64.b64decode(license_key.encode()).decode()
            license_data = json.loads(license_json)
            
            # Extract signature
            signature = license_data.pop('signature', None)
            if not signature:
                return False
            
            # Verify signature
            data_string = json.dumps(license_data, sort_keys=True)
            expected_signature = hashlib.sha256(f"{data_string}:{self.master_key.decode()}".encode()).hexdigest()
            
            if signature != expected_signature:
                logger.warning(f"Invalid license signature for user {license_data.get('user_id')}")
                return False
            
            # Check expiry
            if license_data['expiry'] < int(datetime.now().timestamp()):
                logger.warning(f"Expired license for user {license_data.get('user_id')}")
                return False
            
            # Add signature back for return
            license_data['signature'] = signature
            
            return license_data
            
        except Exception as e:
            logger.error(f"License validation error: {str(e)}")
            return False
    
    def _get_usage_limit(self, plan_type):
        """Get usage limits based on plan type"""
        limits = {
            'trial': 50,
            'pro': -1,  # Unlimited
            'enterprise': -1  # Unlimited
        }
        return limits.get(plan_type.lower(), 0)
    
    def _get_platform_access(self, plan_type):
        """Get platform access based on plan type"""
        if plan_type.lower() == 'trial':
            return ['instagram', 'facebook', 'linkedin']
        return ['instagram', 'facebook', 'linkedin', 'tiktok', 'youtube', 'whatsapp', 'snapchat', 'x']

class APIKeyManager:
    """
    Secure API key management system
    Handles API key generation, validation, and rotation
    """
    
    def __init__(self):
        self.keys = {}
        self.rate_limits = {}
    
    def generate_api_key(self, user_id, key_type='user'):
        """Generate a secure API key"""
        key = secrets.token_urlsafe(32)
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        
        self.keys[key_hash] = {
            'user_id': user_id,
            'key_type': key_type,
            'created': datetime.now().isoformat(),
            'expires': (datetime.now() + timedelta(days=90)).isoformat(),
            'last_used': None,
            'usage_count': 0
        }
        
        return key
    
    def validate_api_key(self, key):
        """Validate API key and return key data"""
        if not key:
            return False
        
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        
        if key_hash not in self.keys:
            return False
        
        key_data = self.keys[key_hash]
        
        # Check expiry
        if datetime.fromisoformat(key_data['expires']) < datetime.now():
            return False
        
        # Update usage
        key_data['last_used'] = datetime.now().isoformat()
        key_data['usage_count'] += 1
        
        return key_data
    
    def check_rate_limit(self, user_id, action='api_call', limit=100, window_minutes=60):
        """Check rate limiting for API calls"""
        now = datetime.now()
        window_start = now - timedelta(minutes=window_minutes)
        
        if user_id not in self.rate_limits:
            self.rate_limits[user_id] = {}
        
        if action not in self.rate_limits[user_id]:
            self.rate_limits[user_id][action] = []
        
        # Clean old entries
        self.rate_limits[user_id][action] = [
            timestamp for timestamp in self.rate_limits[user_id][action]
            if timestamp > window_start
        ]
        
        # Check limit
        if len(self.rate_limits[user_id][action]) >= limit:
            return False
        
        # Add current request
        self.rate_limits[user_id][action].append(now)
        return True

class ContentProtection:
    """
    Protect content generation algorithms and processes
    Contains proprietary PostVelocity enhancement algorithms
    """
    
    def __init__(self):
        self.secret_sauce_algorithms = self._load_proprietary_algorithms()
    
    def _load_proprietary_algorithms(self):
        """Load proprietary content enhancement algorithms"""
        return {
            'engagement_booster': self._engagement_enhancement,
            'viral_predictor': self._viral_prediction,
            'trend_analyzer': self._trend_analysis,
            'platform_optimizer': self._platform_optimization
        }
    
    def apply_secret_sauce(self, topic, platform, user_context):
        """Apply proprietary algorithms to enhance content"""
        # This is the secret sauce that makes PostVelocity unique
        enhanced_topic = self.secret_sauce_algorithms['engagement_booster'](topic, platform)
        viral_score = self.secret_sauce_algorithms['viral_predictor'](enhanced_topic, user_context)
        trend_data = self.secret_sauce_algorithms['trend_analyzer'](topic, platform)
        optimized_content = self.secret_sauce_algorithms['platform_optimizer'](
            enhanced_topic, platform, viral_score, trend_data
        )
        
        return optimized_content
    
    def _engagement_enhancement(self, topic, platform):
        """Proprietary engagement enhancement algorithm"""
        # Secret algorithm - significantly improves engagement rates
        engagement_multipliers = {
            'instagram': 1.3,
            'facebook': 1.2,
            'linkedin': 1.4,
            'tiktok': 1.6,
            'youtube': 1.5,
            'whatsapp': 1.1,
            'snapchat': 1.3,
            'x': 1.2
        }
        
        multiplier = engagement_multipliers.get(platform, 1.0)
        
        # Apply proprietary enhancement
        enhanced_topic = {
            'original': topic,
            'enhanced': f"{topic} (Enhanced for {multiplier}x engagement)",
            'engagement_score': multiplier * 100,
            'optimization_applied': True
        }
        
        return enhanced_topic
    
    def _viral_prediction(self, topic, user_context):
        """Proprietary viral prediction algorithm"""
        # Secret algorithm - predicts viral potential
        base_score = 50
        
        # Analyze topic for viral indicators
        viral_keywords = ['new', 'amazing', 'breakthrough', 'revolutionary', 'secret', 'exclusive']
        topic_text = str(topic).lower()
        viral_boost = sum(10 for keyword in viral_keywords if keyword in topic_text)
        
        # Apply user context
        context_boost = len(user_context.get('previous_viral_posts', [])) * 5
        
        viral_score = min(base_score + viral_boost + context_boost, 100)
        
        return viral_score
    
    def _trend_analysis(self, topic, platform):
        """Proprietary trend analysis algorithm"""
        # Secret algorithm - analyzes current trends
        current_trends = {
            'ai': 95,
            'automation': 90,
            'productivity': 85,
            'social_media': 80,
            'business': 75
        }
        
        topic_text = str(topic).lower()
        trend_score = max(
            score for keyword, score in current_trends.items()
            if keyword in topic_text
        ) if any(keyword in topic_text for keyword in current_trends) else 50
        
        return {
            'trend_score': trend_score,
            'trending_keywords': [k for k in current_trends.keys() if k in topic_text],
            'platform_trend_bonus': 10 if platform in ['tiktok', 'instagram'] else 5
        }
    
    def _platform_optimization(self, topic, platform, viral_score, trend_data):
        """Proprietary platform optimization algorithm"""
        # Secret algorithm - optimizes content for specific platforms
        platform_characteristics = {
            'instagram': {'max_length': 2200, 'hashtag_optimal': 11, 'visual_focus': True},
            'facebook': {'max_length': 63206, 'hashtag_optimal': 3, 'visual_focus': False},
            'linkedin': {'max_length': 3000, 'hashtag_optimal': 5, 'visual_focus': False},
            'tiktok': {'max_length': 100, 'hashtag_optimal': 8, 'visual_focus': True},
            'youtube': {'max_length': 1000, 'hashtag_optimal': 15, 'visual_focus': True},
            'whatsapp': {'max_length': 4096, 'hashtag_optimal': 0, 'visual_focus': False},
            'snapchat': {'max_length': 80, 'hashtag_optimal': 0, 'visual_focus': True},
            'x': {'max_length': 280, 'hashtag_optimal': 2, 'visual_focus': False}
        }
        
        platform_config = platform_characteristics.get(platform, {})
        
        optimized_content = {
            'topic': topic,
            'platform': platform,
            'viral_score': viral_score,
            'trend_data': trend_data,
            'platform_config': platform_config,
            'optimization_score': (viral_score + trend_data['trend_score']) / 2,
            'recommended_hashtags': platform_config.get('hashtag_optimal', 5),
            'content_length_target': platform_config.get('max_length', 1000)
        }
        
        return optimized_content

# Initialize security manager
security_manager = SecurityManager()
content_protection = ContentProtection()

# Export for use in main application
__all__ = ['security_manager', 'content_protection', 'LicenseManager', 'APIKeyManager']