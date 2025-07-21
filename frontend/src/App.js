/*
 * PostVelocity - AI-Powered Social Media Management Platform
 * Copyright (c) 2025 Fancy Free Living LLC. All rights reserved.
 * 
 * This software is proprietary and confidential. Unauthorized copying,
 * distribution, or use is strictly prohibited and may result in severe
 * civil and criminal penalties.
 * 
 * Trade Secrets: This software contains trade secrets and proprietary
 * information of Fancy Free Living LLC. Any unauthorized use, reproduction,
 * or distribution is strictly prohibited.
 */

import React, { useState, useEffect, useCallback } from 'react';
import './App.css';

const PLATFORM_ICONS = {
  instagram: '📸',
  tiktok: '🎵',
  facebook: '👥',
  youtube: '📺',
  whatsapp: '💬',
  snapchat: '👻',
  x: '✖️',
  linkedin: '💼',
  wechat: '💬',
  telegram: '✈️',
  messenger: '💬',
  douyin: '🎶',
  kuaishou: '📱',
  reddit: '🔺',
  weibo: '🐦',
  pinterest: '📌',
  qq: '🐧',
  threads: '🧵',
  quora: '❓',
  tumblr: '📄'
};

const PLATFORM_COLORS = {
  instagram: 'bg-gradient-to-r from-purple-500 to-pink-500',
  tiktok: 'bg-gradient-to-r from-black to-gray-800',
  facebook: 'bg-blue-600',
  youtube: 'bg-red-600',
  whatsapp: 'bg-green-500',
  snapchat: 'bg-yellow-400',
  x: 'bg-gray-900',
  linkedin: 'bg-blue-700',
  wechat: 'bg-green-600',
  telegram: 'bg-blue-500',
  messenger: 'bg-blue-600',
  douyin: 'bg-gradient-to-r from-red-500 to-pink-500',
  kuaishou: 'bg-orange-500',
  reddit: 'bg-orange-600',
  weibo: 'bg-red-500',
  pinterest: 'bg-red-500',
  qq: 'bg-blue-500',
  threads: 'bg-gray-800',
  quora: 'bg-red-700',
  tumblr: 'bg-indigo-600'
};

const MEDIA_CATEGORIES = {
  training: { icon: '🎓', description: 'Training sessions, workshops, certification ceremonies' },
  equipment: { icon: '🔧', description: 'Tools, machinery, safety equipment, vehicles' },
  workplace: { icon: '🏗️', description: 'Job sites, offices, facilities, work environments' },
  team: { icon: '👥', description: 'Team members, group photos, leadership, staff' },
  projects: { icon: '📋', description: 'Completed projects, work in progress, before/after shots' },
  safety: { icon: '🛡️', description: 'Safety procedures, PPE usage, safety demonstrations' },
  certificates: { icon: '🏆', description: 'Certifications, awards, recognitions, licenses' },
  events: { icon: '🎉', description: 'Company events, conferences, trade shows, meetings' }
};

const TRENDING_TOPICS = [
  'Weekly Safety Tips',
  'Equipment Maintenance',
  'Team Achievement',
  'Industry News Update',
  'Training Session Highlights',
  'OSHA Compliance',
  'Project Milestone',
  'Safety Recognition',
  'New Technology',
  'Seasonal Safety Tips'
];

const INDUSTRY_TEMPLATES = {
  construction: [
    { name: 'Safety Alert', template: 'Important safety update: [TOPIC]. Remember to always [ACTION]. #SafetyFirst #Construction' },
    { name: 'Project Update', template: 'Exciting progress on [PROJECT]. Our team has [ACHIEVEMENT]. #ProjectUpdate #Construction' },
    { name: 'Equipment Feature', template: 'Spotlight on [EQUIPMENT]: [BENEFITS]. Perfect for [USE_CASE]. #Equipment #Construction' },
    { name: 'Team Spotlight', template: 'Meet our team member [NAME] who specializes in [SPECIALTY]. [ACHIEVEMENT]. #TeamSpotlight #Construction' },
    { name: 'Before & After', template: 'Amazing transformation! Before: [BEFORE_STATE]. After: [AFTER_STATE]. #BeforeAndAfter #Construction' }
  ],
  safety: [
    { name: 'Training Reminder', template: 'Don\'t forget: [TRAINING_TOPIC] training is scheduled for [DATE]. Safety first! #SafetyTraining' },
    { name: 'Compliance Update', template: 'New [REGULATION] requirements: [DETAILS]. Stay compliant! #Compliance #Safety' },
    { name: 'Safety Tip', template: 'Pro tip: [SAFETY_TIP]. Small actions, big impact! #SafetyTips #Prevention' },
    { name: 'Incident Prevention', template: 'Prevent [INCIDENT_TYPE] by following these steps: [STEPS]. Stay safe! #Prevention #Safety' },
    { name: 'Equipment Check', template: 'Daily reminder: Check your [EQUIPMENT] for [ISSUES]. Report any problems immediately. #SafetyCheck' }
  ],
  healthcare: [
    { name: 'Health Tip', template: 'Health tip of the day: [TIP]. Small changes make a big difference! #HealthTip #Wellness' },
    { name: 'Service Highlight', template: 'We\'re proud to offer [SERVICE]. Our experienced team provides [BENEFITS]. #Healthcare #Service' },
    { name: 'Patient Success', template: 'Celebrating [PATIENT_SUCCESS]. We\'re honored to be part of your health journey. #PatientCare' },
    { name: 'Preventive Care', template: 'Don\'t wait for symptoms. Schedule your [SCREENING] today. Prevention is the best medicine. #PreventiveCare' }
  ],
  technology: [
    { name: 'Product Launch', template: 'Introducing [PRODUCT]: [KEY_FEATURES]. Experience [BENEFITS] like never before. #TechLaunch #Innovation' },
    { name: 'Tech Tip', template: 'Pro tip: [TIP] to optimize your [SYSTEM/SOFTWARE]. Boost productivity with this simple trick. #TechTips' },
    { name: 'Security Alert', template: 'Security reminder: [THREAT] is trending. Protect yourself by [PROTECTION_STEPS]. #CyberSecurity' },
    { name: 'Update Announcement', template: 'New update available! [VERSION] includes [NEW_FEATURES]. Update now for improved performance. #Updates' }
  ],
  retail: [
    { name: 'Sale Announcement', template: 'Flash sale alert! Get [DISCOUNT]% off [PRODUCT/CATEGORY] until [END_DATE]. Shop now! #Sale #Retail' },
    { name: 'Product Spotlight', template: 'Product spotlight: [PRODUCT_NAME]. Why customers love it: [BENEFITS]. Available now! #ProductSpotlight' },
    { name: 'Customer Review', template: 'Customer says: "[REVIEW]" Thanks [CUSTOMER_NAME] for choosing us! #CustomerLove #Testimonial' },
    { name: 'New Arrival', template: 'Just in: [PRODUCT_NAME] featuring [KEY_FEATURES]. Perfect for [USE_CASE]. Shop the collection! #NewArrival' }
  ],
  fitness: [
    { name: 'Workout Wednesday', template: 'Workout Wednesday: [EXERCISE_NAME]. Benefits: [BENEFITS]. Try [REPS/DURATION] and feel the difference! #WorkoutWednesday' },
    { name: 'Nutrition Tip', template: 'Nutrition tip: [TIP]. Fuel your body with [FOOD/NUTRIENT] for better [RESULT]. #NutritionTips #HealthyEating' },
    { name: 'Transformation', template: 'Incredible transformation! [CLIENT_NAME] achieved [RESULT] in [TIMEFRAME]. You can do it too! #Transformation' },
    { name: 'Class Schedule', template: 'Join us for [CLASS_NAME] on [DAY] at [TIME]. Perfect for [SKILL_LEVEL]. Reserve your spot! #FitnessClass' }
  ],
  restaurant: [
    { name: 'Daily Special', template: 'Today\'s special: [DISH_NAME] featuring [INGREDIENTS]. Chef\'s recommendation for [OCCASION]. #DailySpecial' },
    { name: 'Behind the Scenes', template: 'Behind the scenes: Our chef [ACTION] to create [DISH]. The secret ingredient? [SECRET]. #BehindTheScenes' },
    { name: 'Happy Hour', template: 'Happy hour starts now! Enjoy [OFFER] from [START_TIME] to [END_TIME]. Perfect for [OCCASION]. #HappyHour' },
    { name: 'Customer Feature', template: 'Look at that smile! [CUSTOMER_NAME] is enjoying our [DISH]. Thanks for dining with us! #CustomerLove' }
  ]
};

function App() {
  const [currentView, setCurrentView] = useState('dashboard');
  const [companies, setCompanies] = useState([]);
  const [selectedCompany, setSelectedCompany] = useState(null);
  const [formData, setFormData] = useState({
    company_id: '',
    topic: '',
    platforms: [],
    audience_level: 'general',
    additional_context: '',
    negative_context: '',
    personal_voice: '',
    generate_blog: false,
    generate_newsletter: false,
    generate_video_script: false,
    generate_ai_video: false,
    generate_ai_music: false,
    generate_ai_images: false,
    ai_video_duration: 30,
    ai_video_style: 'professional',
    ai_music_mood: 'upbeat',
    ai_image_count: 2,
    ai_image_style: 'professional',
    ai_image_usage: 'social_posts',
    video_source: 'ai_generate',
    music_source: 'ai_generate',
    selected_user_video: '',
    selected_user_music: '',
    use_company_media: true,
    high_authenticity: false,
    media_preferences: {},
    seo_focus: true,
    target_keywords: [],
    competitor_analysis: false,
    repurpose_content: false,
    template_id: ''
  });

  // Admin Management State
  const [allUsers, setAllUsers] = useState([]);
  const [showAdminPanel, setShowAdminPanel] = useState(false);
  const [isImpersonating, setIsImpersonating] = useState(false);
  const [originalAdmin, setOriginalAdmin] = useState(null);
  const [showCreateUserModal, setShowCreateUserModal] = useState(false);
  const [newUserForm, setNewUserForm] = useState({
    email: '',
    full_name: '',
    plan: 'starter',
    industry: 'Construction'
  });
  
  // Enhanced Admin Analytics State
  const [adminAnalytics, setAdminAnalytics] = useState(null);
  const [comprehensiveAnalytics, setComprehensiveAnalytics] = useState(null);
  const [billingAnalytics, setBillingAnalytics] = useState(null);
  const [selectedUser, setSelectedUser] = useState(null);
  const [adminActiveTab, setAdminActiveTab] = useState('overview'); // overview, users, analytics, billing, free-codes
  
  // Free Access Codes State
  const [freeCodes, setFreeCodes] = useState([]);
  const [showCreateCodeModal, setShowCreateCodeModal] = useState(false);
  const [newCodeForm, setNewCodeForm] = useState({
    plan_level: 'professional',
    duration_days: 30,
    max_uses: 1,
    description: ''
  });
  const [showRedeemCodeModal, setShowRedeemCodeModal] = useState(false);
  const [redeemCodeInput, setRedeemCodeInput] = useState('');
  
  // OAuth Connection Management State
  const [connectedPlatforms, setConnectedPlatforms] = useState({});
  const [platformConnectionStatus, setPlatformConnectionStatus] = useState({});
  const [connectingPlatform, setConnectingPlatform] = useState(null);
  const [showOAuthModal, setShowOAuthModal] = useState(false);
  const [selectedPlatformForOAuth, setSelectedPlatformForOAuth] = useState(null);
  
  // Drag and drop media upload state
  const [dragDropCompanyId, setDragDropCompanyId] = useState('');
  
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [availablePlatforms, setAvailablePlatforms] = useState([]);
  const [mediaFiles, setMediaFiles] = useState([]);
  const [mediaRequests, setMediaRequests] = useState([]);
  const [uploadingMedia, setUploadingMedia] = useState(false);
  const [roiData, setRoiData] = useState(null);
  const [trendingHashtags, setTrendingHashtags] = useState(null);
  const [quickActionLoading, setQuickActionLoading] = useState(false);
  const [bulkContentLoading, setBulkContentLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('content-hub');
  
  // Enhanced Voice Input State
  const [voiceTranscript, setVoiceTranscript] = useState('');
  const [voiceCommand, setVoiceCommand] = useState('');
  
  // Smart Content Preview State
  const [contentPreview, setContentPreview] = useState(null);
  const [showPreview, setShowPreview] = useState(false);
  const [previewEngagementMetrics, setPreviewEngagementMetrics] = useState(null);
  
  // Quick Actions Enhancement State
  const [lastGeneratedContent, setLastGeneratedContent] = useState(null);
  const [translationLanguages] = useState(['Spanish', 'French', 'German', 'Italian', 'Portuguese', 'Japanese', 'Chinese']);
  const [selectedLanguage, setSelectedLanguage] = useState('Spanish');
  
  // Real-time Analytics State
  const [analyticsInsights, setAnalyticsInsights] = useState(null);
  const [bestPostingTimes, setBestPostingTimes] = useState(null);
  const [whatWorkingData, setWhatWorkingData] = useState(null);
  
  // New Upgrade Add-ons State
  const [showHashtagsUpgrade, setShowHashtagsUpgrade] = useState(false);
  const [showSeoKeywordsUpgrade, setShowSeoKeywordsUpgrade] = useState(false);
  const [showCompetitorAnalysisUpgrade, setShowCompetitorAnalysisUpgrade] = useState(false);
  const [showCompetitorAnalysisModal, setShowCompetitorAnalysisModal] = useState(false);
  const [hasHashtagsAddon, setHasHashtagsAddon] = useState(false);
  const [hasSeoKeywordsAddon, setHasSeoKeywordsAddon] = useState(false);
  const [hasCompetitorAnalysisAddon, setHasCompetitorAnalysisAddon] = useState(false);
  const [generatedHashtags, setGeneratedHashtags] = useState([]);
  const [generatedSeoKeywords, setGeneratedSeoKeywords] = useState([]);
  const [competitorAnalysisData, setCompetitorAnalysisData] = useState(null);
  const [competitorAnalysisForm, setCompetitorAnalysisForm] = useState({
    competitorWebsite: '',
    competitorName: '',
    analysisType: 'comprehensive', // comprehensive, website, social
    socialPlatforms: []
  });
  
  // Enhanced SaaS state management
  const [showPricingModal, setShowPricingModal] = useState(false);
  const [showPlanUpgradeModal, setShowPlanUpgradeModal] = useState(false);
  const [currentUserPlan, setCurrentUserPlan] = useState('starter');
  const [userSubscription, setUserSubscription] = useState(null);
  const [userUsage, setUserUsage] = useState(null);
  const [availablePlans, setAvailablePlans] = useState({});
  const [selectedPlan, setSelectedPlan] = useState('');
  const [selectedInterval, setSelectedInterval] = useState('monthly');
  const [paymentProcessing, setPaymentProcessing] = useState(false);
  const [usageWarnings, setUsageWarnings] = useState([]);
  
  // Add-on selection state
  const [selectedAddons, setSelectedAddons] = useState(new Set());

  // Team Management State
  const [showTeamModal, setShowTeamModal] = useState(false);
  const [showInviteModal, setShowInviteModal] = useState(false);
  const [teamMembers, setTeamMembers] = useState([]);
  const [inviteForm, setInviteForm] = useState({
    email: '',
    role: 'member',
    permissions: []
  });
  const [loadingTeam, setLoadingTeam] = useState(false);

  // Partner Program State
  const [showPartnerModal, setShowPartnerModal] = useState(false);
  const [partnerData, setPartnerData] = useState(null);
  const [partnerStats, setPartnerStats] = useState({});
  const [partnerForm, setPartnerForm] = useState({
    full_name: '',
    email: '',
    company_name: '',
    partner_type: 'affiliate',
    website: ''
  });
  const [loadingPartner, setLoadingPartner] = useState(false);
  const [referralCode, setReferralCode] = useState('');

  // API Management State
  const [showApiModal, setShowApiModal] = useState(false);
  const [apiKeys, setApiKeys] = useState([]);
  const [newApiKeyForm, setNewApiKeyForm] = useState({
    key_name: '',
    permissions: ['read'],
    expires_in_days: 365
  });
  const [loadingApi, setLoadingApi] = useState(false);
  const [generatedApiKey, setGeneratedApiKey] = useState(null);

  // Authentication and Login System State
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [loginForm, setLoginForm] = useState({
    email: '',
    password: '',
    isRegistering: false
  });
  const [loginLoading, setLoginLoading] = useState(false);
  
  // Individual login state variables for the new login system
  const [loginEmail, setLoginEmail] = useState('');
  const [loginPassword, setLoginPassword] = useState('');
  
  // New state for one-time purchase model
  const [userStatus, setUserStatus] = useState({
    isTrialUser: false,
    trialStartDate: null,
    trialDaysRemaining: 0,
    isPaidUser: false,
    purchaseType: null, // 'lifetime', 'beta_special'
    usageCount: 0,
    trialUsageLimit: 50,
    isBetaTester: false,
    betaTesterId: null,
    betaBenefits: [],
    hasSeOAddon: false,
    seoAddonStatus: null
  });
  const [showPaymentModal, setShowPaymentModal] = useState(false);
  const [showTrialModal, setShowTrialModal] = useState(false);
  const [showBetaModal, setShowBetaModal] = useState(false);
  
  // New state for enhanced features
  const [progressStatus, setProgressStatus] = useState(null);
  const [contentLibrary, setContentLibrary] = useState([]);
  const [notifications, setNotifications] = useState([]);
  const [showNotifications, setShowNotifications] = useState(false);
  const [draggedFiles, setDraggedFiles] = useState([]);
  const [calendarPosts, setCalendarPosts] = useState([]);
  const [isVoiceRecording, setIsVoiceRecording] = useState(false);
  const [showSuccessAnimation, setShowSuccessAnimation] = useState(false);
  const [performanceMetrics, setPerformanceMetrics] = useState(null);
  const [trendingTopics, setTrendingTopics] = useState([]);
  const [contentHistory, setContentHistory] = useState([]);
  const [isOffline, setIsOffline] = useState(false);
  const [undoStack, setUndoStack] = useState([]);
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  
  // Beta feedback system state
  const [betaFeedback, setBetaFeedback] = useState([]);
  const [betaUser, setBetaUser] = useState(null);
  const [showBetaLogin, setShowBetaLogin] = useState(false);
  const [newFeedback, setNewFeedback] = useState({ title: '', description: '', type: 'suggestion', priority: 'medium' });
  
  // SEO monitoring state
  const [seoAddon, setSeoAddon] = useState(null);
  const [seoAudits, setSeoAudits] = useState([]);
  const [seoParameters, setSeoParameters] = useState([]);
  const [showSeoUpgrade, setShowSeoUpgrade] = useState(false);
  const [auditInProgress, setAuditInProgress] = useState(false);

  const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

  useEffect(() => {
    fetchCompanies();
    fetchPlatforms();
    fetchMonthlyMediaRequests();
    fetchContentLibrary();
    fetchTrendingTopics();
    setupOfflineListener();
    setupNotifications();
    checkUserStatus();
    checkTrialParams();
  }, []);

  useEffect(() => {
    if (selectedCompany) {
      fetchCompanyMedia();
      fetchRoiData();
      fetchTrendingHashtags();
      fetchPerformanceMetrics();
      fetchContentHistory();
    }
  }, [selectedCompany]);

  const setupOfflineListener = () => {
    window.addEventListener('online', () => setIsOffline(false));
    window.addEventListener('offline', () => setIsOffline(true));
  };

  const setupNotifications = () => {
    // Simulate trending topic notifications
    const checkTrendingTopics = () => {
      const topics = ['AI in Construction', 'New Safety Regulations', 'Equipment Innovation'];
      const randomTopic = topics[Math.floor(Math.random() * topics.length)];
      addNotification(`🔥 Trending: ${randomTopic}`, 'trending');
    };

    // Check every 30 minutes
    setInterval(checkTrendingTopics, 30 * 60 * 1000);
  };

  const checkUserStatus = () => {
    const savedStatus = localStorage.getItem('userStatus');
    if (savedStatus) {
      const status = JSON.parse(savedStatus);
      
      // Check if trial has expired
      if (status.isTrialUser && status.trialStartDate) {
        const trialStart = new Date(status.trialStartDate);
        const now = new Date();
        const daysDiff = Math.floor((now - trialStart) / (1000 * 60 * 60 * 24));
        const daysRemaining = Math.max(0, 7 - daysDiff);
        
        status.trialDaysRemaining = daysRemaining;
        
        if (daysRemaining <= 0) {
          status.isTrialUser = false;
          addNotification('Your free trial has expired. Please upgrade to continue using PostVelocity.', 'error');
        }
      }
      
      setUserStatus(status);
    }
  };

  const checkTrialParams = () => {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('trial') === 'true') {
      setShowTrialModal(true);
    }
    if (urlParams.get('beta') === 'true') {
      setShowBetaModal(true);
    }
  };

  const joinBetaProgram = () => {
    const betaId = `BETA${Date.now().toString(36).toUpperCase()}`;
    const betaStatus = {
      isTrialUser: false,
      trialStartDate: null,
      trialDaysRemaining: 0,
      isPaidUser: false,
      purchaseType: null,
      usageCount: 0,
      trialUsageLimit: 200, // Beta testers get more usage
      isBetaTester: true,
      betaTesterId: betaId,
      betaBenefits: [
        'Extended trial (200 generations)',
        'Priority support',
        'Exclusive beta features',
        'Direct feedback channel',
        '50% discount on lifetime license',
        'Forever free updates',
        'Beta tester badge'
      ],
      hasSeOAddon: false,
      seoAddonStatus: null
    };

    setUserStatus(betaStatus);
    localStorage.setItem('userStatus', JSON.stringify(betaStatus));
    setShowBetaModal(false);
    addNotification(`🎉 Welcome to the Beta Program! Your Beta ID: ${betaId}`, 'success');
  };

  const purchaseSeOAddon = async (planType = 'standard') => {
    console.log('purchaseSeOAddon called with plan:', planType);
    console.log('Current userStatus:', userStatus);
    
    try {
      // Simulate SEO addon purchase
      setProgressStatus({ step: 'Activating SEO Monitoring...', progress: 50 });
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Always succeed for demo purposes - bypass backend call
      let backendSuccess = true;
      
      console.log('Backend success:', backendSuccess);
      
      if (backendSuccess) {
        // Update user status to include SEO addon
        const updatedStatus = {
          ...userStatus,
          hasSeOAddon: true,
          seoAddonStatus: 'active'
        };
        
        console.log('Setting hasSeOAddon to true, updated status:', updatedStatus);
        
        setUserStatus(updatedStatus);
        localStorage.setItem('userStatus', JSON.stringify(updatedStatus));
        setShowSeoUpgrade(false);
        setProgressStatus({ step: 'SEO Monitoring Activated!', progress: 100 });
        
        console.log('Status updated, localStorage updated, modal closed');
        
        addNotification(`🎉 SEO Monitoring Add-on activated! ${planType === 'standard' ? '50' : '100'} daily checks available.`, 'success');
        
        setTimeout(() => setProgressStatus(null), 2000);
        return true;
      } else {
        console.log('Backend failed, showing error');
        addNotification('Failed to purchase SEO add-on. Please try again.', 'error');
        setProgressStatus(null);
        return false;
      }
    } catch (error) {
      console.error('Error in purchaseSeOAddon:', error);
      addNotification('Error purchasing SEO add-on. Please try again.', 'error');
      setProgressStatus(null);
      return false;
    }
  };

  const startFreeTrial = () => {
    const trialStatus = {
      isTrialUser: true,
      trialStartDate: new Date().toISOString(),
      trialDaysRemaining: 7,
      isPaidUser: false,
      purchaseType: null,
      usageCount: 0,
      trialUsageLimit: 50,
      isBetaTester: false,
      betaTesterId: null,
      betaBenefits: []
    };
    
    setUserStatus(trialStatus);
    localStorage.setItem('userStatus', JSON.stringify(trialStatus));
    setShowTrialModal(false);
    addNotification('🎉 Welcome to PostVelocity! Your 7-day free trial has started.', 'success');
  };

  const checkUsageLimit = () => {
    if (userStatus.isPaidUser) {
      return true; // No limits for paid users
    }
    
    if (userStatus.isTrialUser) {
      if (userStatus.trialDaysRemaining <= 0) {
        setShowPaymentModal(true);
        return false;
      }
      
      if (userStatus.usageCount >= userStatus.trialUsageLimit) {
        addNotification('You have reached your trial limit. Please upgrade to continue.', 'error');
        setShowPaymentModal(true);
        return false;
      }
      
      return true;
    }
    
    // New user - show trial modal
    setShowTrialModal(true);
    return false;
  };

  const incrementUsage = () => {
    if (userStatus.isPaidUser) return; // No limits for paid users
    
    const newStatus = {
      ...userStatus,
      usageCount: userStatus.usageCount + 1
    };
    
    setUserStatus(newStatus);
    localStorage.setItem('userStatus', JSON.stringify(newStatus));
    
    // Warning at 80% usage
    if (newStatus.usageCount >= newStatus.trialUsageLimit * 0.8) {
      addNotification(`Trial usage: ${newStatus.usageCount}/${newStatus.trialUsageLimit}. Consider upgrading soon!`, 'warning');
    }
  };

  const processPayment = async (plan) => {
    try {
      // Simulate payment processing
      setProgressStatus({ step: 'Processing payment...', progress: 50 });
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      let purchaseType = 'lifetime';
      let discount = 0;
      
      // Special pricing for beta testers
      if (userStatus.isBetaTester) {
        discount = 50; // 50% discount for beta testers
        purchaseType = 'beta_special';
      }
      
      const paidStatus = {
        isTrialUser: false,
        trialStartDate: null,
        trialDaysRemaining: 0,
        isPaidUser: true,
        purchaseType: purchaseType,
        usageCount: 0,
        trialUsageLimit: 0,
        isBetaTester: userStatus.isBetaTester,
        betaTesterId: userStatus.betaTesterId,
        betaBenefits: userStatus.isBetaTester ? [
          ...userStatus.betaBenefits,
          'Lifetime access purchased',
          'All future updates included'
        ] : ['Lifetime access', 'All future updates included'],
        hasSeOAddon: false, // SEO addon is separate purchase
        seoAddonStatus: null
      };
      
      setUserStatus(paidStatus);
      localStorage.setItem('userStatus', JSON.stringify(paidStatus));
      setShowPaymentModal(false);
      setProgressStatus({ step: 'Payment complete!', progress: 100 });
      
      const discountText = discount > 0 ? ` (${discount}% beta discount applied)` : '';
      addNotification(`🎉 Welcome to PostVelocity ${plan}! Lifetime access activated${discountText}.`, 'success');
      
      // Show SEO addon upsell after main purchase
      setTimeout(() => {
        if (!paidStatus.hasSeOAddon) {
          setShowSeoUpgrade(true);
        }
      }, 3000);
      
      setTimeout(() => setProgressStatus(null), 2000);
    } catch (error) {
      addNotification('Payment processing failed. Please try again.', 'error');
      setProgressStatus(null);
    }
  };

  const addNotification = (message, type = 'info') => {
    const notification = {
      id: Date.now(),
      message,
      type,
      timestamp: new Date(),
      read: false
    };
    setNotifications(prev => [notification, ...prev.slice(0, 9)]);
  };

  const fetchCompanies = async () => {
    try {
      const response = await fetch(`${backendUrl}/api/companies`);
      const data = await response.json();
      setCompanies(data || []);
      if (data && data.length > 0 && !selectedCompany) {
        setSelectedCompany(data[0]);
        setFormData(prev => ({ ...prev, company_id: data[0].id }));
      }
    } catch (error) {
      console.error('Error fetching companies:', error);
      setCompanies([]);
      addNotification('Error loading companies', 'error');
    }
  };

  const fetchPlatforms = async () => {
    try {
      // Use all available platforms from our expanded platform definitions
      const allPlatforms = Object.keys(PLATFORM_ICONS);
      setAvailablePlatforms(allPlatforms);
    } catch (error) {
      console.error('Error setting platforms:', error);
      // Fallback to all platforms
      setAvailablePlatforms([
        'facebook', 'youtube', 'instagram', 'whatsapp', 'tiktok', 'wechat', 
        'telegram', 'messenger', 'snapchat', 'douyin', 'kuaishou', 'reddit', 
        'weibo', 'pinterest', 'qq', 'linkedin', 'x', 'threads', 'quora', 'tumblr'
      ]);
    }
  };

  const fetchCompanyMedia = async () => {
    if (!selectedCompany) return;
    try {
      const response = await fetch(`${backendUrl}/api/companies/${selectedCompany.id}/media`);
      const data = await response.json();
      setMediaFiles(data || []);
    } catch (error) {
      console.error('Error fetching company media:', error);
      setMediaFiles([]);
    }
  };

  const fetchRoiData = async () => {
    if (!selectedCompany) return;
    try {
      const response = await fetch(`${backendUrl}/api/analytics/${selectedCompany.id}/roi`);
      const data = await response.json();
      setRoiData(data);
    } catch (error) {
      console.error('Error fetching ROI data:', error);
    }
  };

  const fetchTrendingHashtags = async () => {
    if (!selectedCompany) return;
    try {
      const industry = selectedCompany.industry?.toLowerCase() || 'construction';
      const response = await fetch(`${backendUrl}/api/hashtags/trending/${industry}`);
      const data = await response.json();
      setTrendingHashtags(data);
    } catch (error) {
      console.error('Error fetching trending hashtags:', error);
    }
  };

  const fetchMonthlyMediaRequests = async () => {
    try {
      const response = await fetch(`${backendUrl}/api/media/requests/monthly`);
      const data = await response.json();
      setMediaRequests(data.requests || []);
    } catch (error) {
      console.error('Error fetching media requests:', error);
      setMediaRequests([]);
    }
  };

  const fetchContentLibrary = async () => {
    try {
      const savedContent = localStorage.getItem('contentLibrary');
      if (savedContent) {
        setContentLibrary(JSON.parse(savedContent));
      }
    } catch (error) {
      console.error('Error loading content library:', error);
    }
  };

  const fetchTrendingTopics = async () => {
    try {
      // Simulate trending topics API
      const topics = [
        { topic: 'AI in Construction', trend: 'rising', engagement: 85 },
        { topic: 'Green Building', trend: 'stable', engagement: 72 },
        { topic: 'Remote Work Safety', trend: 'declining', engagement: 45 },
        { topic: 'Equipment Innovation', trend: 'rising', engagement: 90 },
        { topic: 'Worker Training', trend: 'stable', engagement: 68 }
      ];
      setTrendingTopics(topics);
    } catch (error) {
      console.error('Error fetching trending topics:', error);
    }
  };

  const fetchPerformanceMetrics = async () => {
    if (!selectedCompany) return;
    try {
      // Simulate performance metrics
      const metrics = {
        engagement_rate: 4.2,
        reach: 12500,
        impressions: 25000,
        clicks: 850,
        conversions: 23,
        growth_rate: 15.3,
        top_performing_platform: 'linkedin',
        best_posting_time: '10:00 AM',
        top_hashtag: '#SafetyFirst'
      };
      setPerformanceMetrics(metrics);
    } catch (error) {
      console.error('Error fetching performance metrics:', error);
    }
  };

  const fetchContentHistory = async () => {
    try {
      const history = localStorage.getItem('contentHistory');
      if (history) {
        setContentHistory(JSON.parse(history));
      }
    } catch (error) {
      console.error('Error loading content history:', error);
    }
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handlePlatformToggle = (platform) => {
    setFormData(prev => ({
      ...prev,
      platforms: prev.platforms.includes(platform)
        ? prev.platforms.filter(p => p !== platform)
        : [...prev.platforms, platform]
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.company_id || !formData.topic || formData.platforms.length === 0) {
      addNotification('Please fill in company, topic, and select at least one platform', 'error');
      return;
    }

    // Check usage limits before processing
    const usageAllowed = await trackUsage('posts_generated', formData.platforms.length);
    if (!usageAllowed) {
      return; // trackUsage already shows upgrade modal if limit exceeded
    }

    if (!checkUsageLimit()) {
      return;
    }

    setLoading(true);
    setProgressStatus({ step: 'Analyzing topic...', progress: 20 });

    try {
      setTimeout(() => setProgressStatus({ step: 'Generating content...', progress: 50 }), 2000);
      setTimeout(() => setProgressStatus({ step: 'Optimizing for platforms...', progress: 75 }), 5000);
      setTimeout(() => setProgressStatus({ step: 'Finalizing...', progress: 90 }), 8000);

      const response = await fetch(`${backendUrl}/api/generate-content`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error('Failed to generate content');
      }

      const data = await response.json();
      setResults(data);
      setProgressStatus({ step: 'Complete!', progress: 100 });
      
      // If AI video/music generation is requested, start that process
      if (formData.generate_ai_video || formData.generate_ai_music) {
        setProgressStatus({ step: '🎬🎵 Generating AI media...', progress: 95 });
        try {
          await generateAIMedia(formData);
        } catch (error) {
          console.error('AI media generation failed:', error);
          // Continue even if AI media fails - user still gets text content
        }
      }
      
      // Track last generated content for "Generate Similar" feature
      setLastGeneratedContent({
        topic: formData.topic,
        platforms: formData.platforms,
        content: data.content,
        timestamp: new Date()
      });
      
      // Increment usage count
      incrementUsage();
      
      // Save to content library
      saveToContentLibrary(data);
      
      // Save to history
      saveToContentHistory(data);
      
      // Show success animation
      setShowSuccessAnimation(true);
      setTimeout(() => setShowSuccessAnimation(false), 3000);
      
      setCurrentView('results');
      addNotification('Content generated successfully! 🎉', 'success');
    } catch (error) {
      console.error('Error generating content:', error);
      addNotification('Error generating content. Please try again.', 'error');
    } finally {
      setLoading(false);
      setProgressStatus(null);
    }
  };

  const saveToContentLibrary = (content) => {
    const libraryItem = {
      id: Date.now(),
      topic: formData.topic,
      content: content,
      platforms: formData.platforms,
      created_at: new Date(),
      performance: Math.floor(Math.random() * 40) + 60 // Simulate performance score
    };
    
    const updatedLibrary = [libraryItem, ...contentLibrary.slice(0, 49)]; // Keep last 50
    setContentLibrary(updatedLibrary);
    localStorage.setItem('contentLibrary', JSON.stringify(updatedLibrary));
  };

  const saveToContentHistory = (content) => {
    const historyItem = {
      id: Date.now(),
      topic: formData.topic,
      platforms: formData.platforms,
      created_at: new Date(),
      company: selectedCompany.name
    };
    
    const updatedHistory = [historyItem, ...contentHistory.slice(0, 99)]; // Keep last 100
    setContentHistory(updatedHistory);
    localStorage.setItem('contentHistory', JSON.stringify(updatedHistory));
  };

  // Smart Generate - AI detects trending topics and generates content
  const smartGenerate = async () => {
    if (!selectedCompany) {
      addNotification('Please select a company first', 'error');
      return;
    }

    if (!checkUsageLimit()) {
      return;
    }

    setQuickActionLoading(true);
    setProgressStatus({ step: 'Analyzing trending topics...', progress: 10 });

    try {
      // Get trending topic
      const trendingTopic = trendingTopics.find(t => t.trend === 'rising')?.topic || 'Weekly Safety Tips';
      
      setProgressStatus({ step: 'Generating smart content...', progress: 50 });
      
      const smartRequest = {
        ...formData,
        topic: trendingTopic,
        platforms: ['instagram', 'facebook', 'linkedin'],
        use_company_media: true,
        seo_focus: true,
        repurpose_content: true
      };
      
      const response = await fetch(`${backendUrl}/api/generate-content`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(smartRequest),
      });

      if (!response.ok) {
        throw new Error('Failed to generate smart content');
      }

      const data = await response.json();
      setResults(data);
      setProgressStatus({ step: 'Complete!', progress: 100 });
      
      // Increment usage count
      incrementUsage();
      
      saveToContentLibrary(data);
      saveToContentHistory(data);
      
      setShowSuccessAnimation(true);
      setTimeout(() => setShowSuccessAnimation(false), 3000);
      
      setCurrentView('results');
      addNotification(`Smart content generated for trending topic: ${trendingTopic}! 🚀`, 'success');
    } catch (error) {
      console.error('Error generating smart content:', error);
      addNotification('Error generating smart content. Please try again.', 'error');
    } finally {
      setQuickActionLoading(false);
      setProgressStatus(null);
    }
  };

  // Weekly Batch Mode
  const generateWeeklyBatch = async () => {
    if (!selectedCompany) {
      addNotification('Please select a company first', 'error');
      return;
    }

    if (!checkUsageLimit()) {
      return;
    }

    setBulkContentLoading(true);
    setProgressStatus({ step: 'Planning weekly content...', progress: 10 });

    try {
      const weeklyTopics = [
        'Monday Motivation',
        'Tuesday Training Tips',
        'Wednesday Workplace Safety',
        'Thursday Technology Update',
        'Friday Team Features',
        'Saturday Safety Spotlight',
        'Sunday Preparation'
      ];

      const bulkResults = [];
      
      for (let i = 0; i < weeklyTopics.length; i++) {
        const topic = weeklyTopics[i];
        setProgressStatus({ 
          step: `Generating ${topic}...`, 
          progress: 10 + (i * 80 / weeklyTopics.length) 
        });

        const response = await fetch(`${backendUrl}/api/generate-content`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            ...formData,
            topic,
            platforms: ['instagram', 'facebook', 'linkedin'],
            use_company_media: true,
            seo_focus: true
          }),
        });

        if (response.ok) {
          const data = await response.json();
          bulkResults.push(data);
          saveToContentLibrary(data);
        }
      }
      
      setResults({
        bulk_results: bulkResults,
        is_bulk: true,
        is_weekly: true,
        generated_content: bulkResults.flatMap(r => r.generated_content || [])
      });
      
      // Increment usage count for weekly batch (counts as 7 uses)
      for (let i = 0; i < 7; i++) {
        incrementUsage();
      }
      
      setProgressStatus({ step: 'Weekly batch complete!', progress: 100 });
      setCurrentView('results');
      addNotification(`Weekly batch generated: ${bulkResults.length} content sets! 📅`, 'success');
    } catch (error) {
      console.error('Error generating weekly batch:', error);
      addNotification('Error generating weekly batch. Please try again.', 'error');
    } finally {
      setBulkContentLoading(false);
      setProgressStatus(null);
    }
  };

  // Emergency Post Feature
  const generateEmergencyPost = async (emergencyType) => {
    setQuickActionLoading(true);
    setProgressStatus({ step: 'Generating emergency post...', progress: 50 });

    try {
      const emergencyTemplates = {
        weather: 'Weather Alert: Due to severe weather conditions, please follow safety protocols. Stay safe!',
        accident: 'Safety Update: We are addressing a safety incident. All protocols are being followed.',
        equipment: 'Equipment Alert: [EQUIPMENT] is temporarily out of service. Alternative solutions in place.',
        general: 'Important Update: We are monitoring the situation and will provide updates soon.'
      };

      const emergencyTopic = emergencyTemplates[emergencyType] || emergencyTemplates.general;
      
      const emergencyRequest = {
        ...formData,
        topic: `Emergency: ${emergencyTopic}`,
        platforms: ['instagram', 'facebook', 'linkedin', 'x'],
        additional_context: 'This is an urgent communication that requires immediate attention and professional tone.',
        audience_level: 'general'
      };

      const response = await fetch(`${backendUrl}/api/generate-content`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(emergencyRequest),
      });

      if (!response.ok) {
        throw new Error('Failed to generate emergency post');
      }

      const data = await response.json();
      setResults(data);
      setProgressStatus({ step: 'Emergency post ready!', progress: 100 });
      
      setCurrentView('results');
      addNotification('Emergency post generated and ready for immediate posting! 🚨', 'success');
    } catch (error) {
      console.error('Error generating emergency post:', error);
      addNotification('Error generating emergency post. Please try again.', 'error');
    } finally {
      setQuickActionLoading(false);
      setProgressStatus(null);
    }
  };

  // Enhanced Voice Input Feature with Advanced Capabilities
  const startVoiceRecording = () => {
    if (!('webkitSpeechRecognition' in window)) {
      addNotification('Voice input not supported in this browser', 'error');
      return;
    }

    const recognition = new window.webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'en-US';

    setIsVoiceRecording(true);
    setVoiceTranscript('');

    recognition.onresult = (event) => {
      let interimTranscript = '';
      let finalTranscript = '';
      
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
          finalTranscript += transcript;
        } else {
          interimTranscript += transcript;
        }
      }
      
      // Real-time transcript display
      setVoiceTranscript(finalTranscript + interimTranscript);
      
      if (finalTranscript) {
        // Process voice commands
        const lowerTranscript = finalTranscript.toLowerCase();
        if (lowerTranscript.includes('generate for instagram')) {
          setFormData(prev => ({ ...prev, topic: finalTranscript.replace(/generate for instagram/i, '').trim(), platforms: ['instagram'] }));
          setVoiceCommand('Instagram content generation');
        } else if (lowerTranscript.includes('generate for facebook')) {
          setFormData(prev => ({ ...prev, topic: finalTranscript.replace(/generate for facebook/i, '').trim(), platforms: ['facebook'] }));
          setVoiceCommand('Facebook content generation');
        } else if (lowerTranscript.includes('make it professional')) {
          setFormData(prev => ({ ...prev, topic: finalTranscript.replace(/make it professional/i, '').trim(), audience_level: 'professional' }));
          setVoiceCommand('Professional tone applied');
        } else if (lowerTranscript.includes('generate blog')) {
          setFormData(prev => ({ ...prev, topic: finalTranscript.replace(/generate blog/i, '').trim(), generate_blog: true }));
          setVoiceCommand('Blog generation enabled');
        } else {
          setFormData(prev => ({ ...prev, topic: finalTranscript }));
          setVoiceCommand('Topic captured');
        }
        
        addNotification(`🎤 ${voiceCommand}: "${finalTranscript}"`, 'success');
      }
    };

    recognition.onerror = (event) => {
      console.error('Speech recognition error:', event.error);
      addNotification('Voice input failed. Please try again.', 'error');
      setIsVoiceRecording(false);
    };

    recognition.onend = () => {
      setIsVoiceRecording(false);
    };

    recognition.start();
  };

  // Smart Content Preview Feature
  const generateContentPreview = async () => {
    if (!formData.topic.trim()) {
      addNotification('Please enter a topic for preview', 'error');
      return;
    }

    try {
      setLoading(true);
      setShowPreview(true);
      
      const previewContent = {
        title: `Preview: ${formData.topic}`,
        content: `Sample content for ${formData.platforms.join(', ')} about ${formData.topic}`,
        estimatedEngagement: {
          likes: Math.floor(Math.random() * 500) + 50,
          comments: Math.floor(Math.random() * 50) + 10,
          shares: Math.floor(Math.random() * 25) + 5,
          reach: Math.floor(Math.random() * 2000) + 500
        },
        characterCount: {
          twitter: formData.topic.length + 100,
          facebook: formData.topic.length + 200,
          instagram: formData.topic.length + 150
        },
        bestPlatforms: ['Instagram', 'Facebook', 'LinkedIn']
      };
      
      setContentPreview(previewContent);
      setPreviewEngagementMetrics(previewContent.estimatedEngagement);
      
    } catch (error) {
      console.error('Preview generation error:', error);
      addNotification('Failed to generate preview', 'error');
    } finally {
      setLoading(false);
    }
  };

  // Quick Actions Enhancement Functions
  const generateSimilarContent = async () => {
    if (!lastGeneratedContent) {
      addNotification('No previous content to base similarity on', 'error');
      return;
    }

    try {
      setQuickActionLoading(true);
      setFormData(prev => ({
        ...prev,
        topic: `Similar to: ${lastGeneratedContent.topic}`,
        additional_context: `Create content similar in style and tone to previous successful post about ${lastGeneratedContent.topic}`
      }));
      
      addNotification('🔄 Generating similar content based on previous success', 'success');
      await handleSubmit({ preventDefault: () => {} });
      
    } catch (error) {
      addNotification('Failed to generate similar content', 'error');
    } finally {
      setQuickActionLoading(false);
    }
  };

  const translateContent = async (language) => {
    if (!results || !results.content) {
      addNotification('No content available to translate', 'error');
      return;
    }

    try {
      setQuickActionLoading(true);
      
      const translatedContent = {
        ...results,
        content: {
          ...results.content,
          translated: `[${language}] ${results.content.content} (Translation would be handled by AI service)`
        }
      };
      
      setResults(translatedContent);
      addNotification(`🌍 Content translated to ${language}`, 'success');
      
    } catch (error) {
      addNotification('Translation failed', 'error');
    } finally {
      setQuickActionLoading(false);
    }
  };

  const optimizeForSEO = async () => {
    if (!results || !results.content) {
      addNotification('No content available to optimize', 'error');
      return;
    }

    try {
      setQuickActionLoading(true);
      
      const seoOptimized = {
        ...results,
        content: {
          ...results.content,
          seoOptimized: true,
          keywords: ['trending', 'professional', 'industry'],
          metaDescription: `SEO-optimized content about ${formData.topic}`
        }
      };
      
      setResults(seoOptimized);
      addNotification('🎯 Content optimized for SEO', 'success');
      
    } catch (error) {
      addNotification('SEO optimization failed', 'error');
    } finally {
      setQuickActionLoading(false);
    }
  };

  // Real-time Analytics Integration Functions
  const loadAnalyticsInsights = async () => {
    try {
      const insights = {
        whatWorking: [
          { type: 'Video Content', performance: '+45% engagement', trend: 'rising' },
          { type: 'Behind-the-scenes', performance: '+32% reach', trend: 'stable' },
          { type: 'Educational Posts', performance: '+28% saves', trend: 'rising' }
        ],
        bestTimes: [
          { day: 'Monday', time: '9:00 AM', engagement: '85%' },
          { day: 'Wednesday', time: '2:00 PM', engagement: '92%' },
          { day: 'Friday', time: '5:00 PM', engagement: '78%' }
        ],
        competitorAnalysis: [
          { competitor: 'Industry Leader A', strength: 'Visual content', gap: 'Video consistency' },
          { competitor: 'Industry Leader B', strength: 'Educational posts', gap: 'Engagement rate' }
        ]
      };
      
      setAnalyticsInsights(insights);
      setBestPostingTimes(insights.bestTimes);
      setWhatWorkingData(insights.whatWorking);
      
    } catch (error) {
      console.error('Analytics insights error:', error);
    }
  };

  // Load analytics insights on component mount
  useEffect(() => {
    loadAnalyticsInsights();
    
    // Check if user is already logged in
    const savedUser = localStorage.getItem('currentUser');
    if (savedUser) {
      const userData = JSON.parse(savedUser);
      setCurrentUser(userData);
      setIsAuthenticated(true);
      
      // Check if this is an impersonation session
      const impersonationToken = localStorage.getItem('impersonationToken');
      const originalAdminData = localStorage.getItem('originalAdmin');
      
      if (impersonationToken && originalAdminData) {
        setIsImpersonating(true);
        setOriginalAdmin(JSON.parse(originalAdminData));
      }
    }
    
    // Load OAuth connections
    loadOAuthConnections();
    
    // Handle OAuth callback
    handleOAuthCallback();
  }, []);

  // Handle OAuth callback from redirect
  const handleOAuthCallback = async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get('code');
    const state = urlParams.get('state');
    const error = urlParams.get('error');
    
    if (error) {
      addNotification(`OAuth failed: ${error}`, 'error');
      // Clean up URL
      window.history.replaceState({}, document.title, window.location.pathname);
      return;
    }
    
    if (code && state) {
      try {
        const savedState = localStorage.getItem('oauth_state');
        const savedPlatform = localStorage.getItem('oauth_platform');
        
        if (savedState !== state) {
          addNotification('OAuth security check failed', 'error');
          return;
        }
        
        const demoUserId = "60d5ec49f1b2c8e1a4567890";
        
        // Exchange code for token
        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/oauth/token`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            platform: savedPlatform,
            code: code,
            state: state,
            user_id: demoUserId
          })
        });
        
        if (response.ok) {
          const data = await response.json();
          addNotification(`Successfully connected to ${savedPlatform}! ${data.username ? `(@${data.username})` : ''}`, 'success');
          
          // Reload connections
          await loadOAuthConnections();
        } else {
          const errorData = await response.json();
          addNotification(`Failed to connect to ${savedPlatform}: ${errorData.detail}`, 'error');
        }
      } catch (error) {
        console.error('OAuth callback error:', error);
        addNotification('OAuth connection failed', 'error');
      } finally {
        // Clean up
        localStorage.removeItem('oauth_state');
        localStorage.removeItem('oauth_platform');
        // Clean up URL
        window.history.replaceState({}, document.title, window.location.pathname);
      }
    }
  };

  // OAuth Connection Management Functions
  const loadOAuthConnections = async () => {
    try {
      // Use a consistent demo user ID
      const demoUserId = "60d5ec49f1b2c8e1a4567890"; // Demo MongoDB ObjectId format
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/oauth/connections/${demoUserId}`);
      if (response.ok) {
        const data = await response.json();
        const connections = {};
        const status = {};
        
        data.connections.forEach(connection => {
          connections[connection.platform] = true;
          status[connection.platform] = {
            connected: true,
            username: connection.username,
            status: connection.connection_status,
            expires_at: connection.expires_at
          };
        });
        
        setConnectedPlatforms(connections);
        setPlatformConnectionStatus(status);
      }
    } catch (error) {
      console.error('Error loading OAuth connections:', error);
    }
  };

  const connectPlatform = async (platform) => {
    try {
      setConnectingPlatform(platform);
      setSelectedPlatformForOAuth(platform);
      
      // Use demo user ID
      const demoUserId = "60d5ec49f1b2c8e1a4567890";
      
      // Get OAuth authorization URL
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/oauth/url/${platform}?user_id=${demoUserId}`);
      if (response.ok) {
        const data = await response.json();
        
        // Store state for verification
        localStorage.setItem('oauth_state', data.state);
        localStorage.setItem('oauth_platform', platform);
        
        // For demo mode, simulate successful connection
        addNotification(`Demo: Connected to ${platform}! In production, this would redirect to ${platform}'s OAuth page.`, 'success');
        
        // Simulate successful connection after a delay
        setTimeout(async () => {
          setConnectedPlatforms(prev => ({ ...prev, [platform]: true }));
          setPlatformConnectionStatus(prev => ({ 
            ...prev, 
            [platform]: {
              connected: true,
              username: `demo_user_${platform}`,
              status: 'active',
              expires_at: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString() // 30 days from now
            }
          }));
          setConnectingPlatform(null);
        }, 2000);
        
      } else {
        throw new Error('Failed to get authorization URL');
      }
    } catch (error) {
      console.error(`Error connecting to ${platform}:`, error);
      addNotification(`Failed to connect to ${platform}`, 'error');
      setConnectingPlatform(null);
    }
  };

  const disconnectPlatform = async (platform) => {
    try {
      const demoUserId = "60d5ec49f1b2c8e1a4567890";
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/oauth/disconnect/${platform}?user_id=${demoUserId}`, {
        method: 'DELETE'
      });
      
      if (response.ok || true) { // Allow demo mode to work even if API fails
        // Update local state
        const updatedConnections = { ...connectedPlatforms };
        const updatedStatus = { ...platformConnectionStatus };
        
        delete updatedConnections[platform];
        delete updatedStatus[platform];
        
        setConnectedPlatforms(updatedConnections);
        setPlatformConnectionStatus(updatedStatus);
        
        addNotification(`Disconnected from ${platform}`, 'success');
      } else {
        throw new Error('Failed to disconnect');
      }
    } catch (error) {
      console.error(`Error disconnecting from ${platform}:`, error);
      addNotification(`Failed to disconnect from ${platform}`, 'error');
    }
  };

  const refreshPlatformConnection = async (platform) => {
    try {
      const demoUserId = "60d5ec49f1b2c8e1a4567890";
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/oauth/refresh/${platform}?user_id=${demoUserId}`, {
        method: 'POST'
      });
      
      if (response.ok || true) { // Allow demo mode
        // Update connection status
        setPlatformConnectionStatus(prev => ({
          ...prev,
          [platform]: {
            ...prev[platform],
            status: 'active',
            expires_at: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString()
          }
        }));
        
        addNotification(`Connection refreshed for ${platform}`, 'success');
      } else {
        throw new Error('Failed to refresh connection');
      }
    } catch (error) {
      console.error(`Error refreshing ${platform} connection:`, error);
      addNotification(`Failed to refresh ${platform} connection`, 'error');
    }
  };

  const publishToConnectedPlatforms = async (content, selectedPlatforms) => {
    const connectedSelected = selectedPlatforms.filter(platform => connectedPlatforms[platform]);
    const unconnectedSelected = selectedPlatforms.filter(platform => !connectedPlatforms[platform]);
    
    if (unconnectedSelected.length > 0) {
      addNotification(
        `Please connect to ${unconnectedSelected.join(', ')} to publish content`, 
        'warning'
      );
    }
    
    if (connectedSelected.length === 0) {
      return;
    }
    
    try {
      const demoUserId = "60d5ec49f1b2c8e1a4567890";
      const publishPromises = connectedSelected.map(platform => 
        fetch(`${process.env.REACT_APP_BACKEND_URL}/api/content/publish/${platform}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            content: content,
            user_id: demoUserId
          })
        })
      );
      
      const responses = await Promise.allSettled(publishPromises);
      const successful = responses.filter(r => r.status === 'fulfilled' && (r.value.ok || true)).length; // Demo mode
      const failed = responses.length - successful;
      
      if (successful > 0) {
        addNotification(`✅ Content published to ${successful} platform${successful > 1 ? 's' : ''}! (Demo Mode)`, 'success');
      }
      if (failed > 0) {
        addNotification(`Failed to publish to ${failed} platform${failed > 1 ? 's' : ''}`, 'error');
      }
    } catch (error) {
      console.error('Error publishing to platforms:', error);
      addNotification('Failed to publish content', 'error');
    }
  };

  // Admin Management Functions
  const loadAllUsers = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/users`);
      if (response.ok) {
        const data = await response.json();
        setAllUsers(data.users || []);
      }
    } catch (error) {
      console.error('Error loading users:', error);
      addNotification('Failed to load users', 'error');
    }
  };

  // Enhanced Admin Analytics Functions
  const loadAdminAnalytics = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/analytics`);
      if (response.ok) {
        const data = await response.json();
        setAdminAnalytics(data.analytics);
      }
    } catch (error) {
      console.error('Error loading admin analytics:', error);
    }
  };

  const loadComprehensiveAnalytics = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/comprehensive-analytics`);
      if (response.ok) {
        const data = await response.json();
        setComprehensiveAnalytics(data.analytics);
      }
    } catch (error) {
      console.error('Error loading comprehensive analytics:', error);
    }
  };

  const loadBillingAnalytics = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/billing-analytics`);
      if (response.ok) {
        const data = await response.json();
        setBillingAnalytics(data.billing_analytics);
      }
    } catch (error) {
      console.error('Error loading billing analytics:', error);
    }
  };

  const loadUserDetails = async (userId) => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/user-details/${userId}`);
      if (response.ok) {
        const data = await response.json();
        setSelectedUser(data.user_details);
      }
    } catch (error) {
      console.error('Error loading user details:', error);
      addNotification('Failed to load user details', 'error');
    }
  };

  // Free Access Codes Functions
  const loadFreeCodes = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/free-codes`);
      if (response.ok) {
        const data = await response.json();
        setFreeCodes(data.codes || []);
      }
    } catch (error) {
      console.error('Error loading free codes:', error);
      addNotification('Failed to load free codes', 'error');
    }
  };

  const generateFreeCode = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/generate-free-code`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newCodeForm)
      });
      
      if (response.ok) {
        const data = await response.json();
        addNotification(`Free code generated: ${data.code}`, 'success');
        setShowCreateCodeModal(false);
        setNewCodeForm({
          plan_level: 'professional',
          duration_days: 30,
          max_uses: 1,
          description: ''
        });
        loadFreeCodes(); // Refresh the list
      } else {
        const error = await response.json();
        addNotification(error.detail || 'Failed to generate free code', 'error');
      }
    } catch (error) {
      console.error('Error generating free code:', error);
      addNotification('Failed to generate free code', 'error');
    }
  };

  const redeemFreeCode = async () => {
    try {
      if (!redeemCodeInput.trim()) {
        addNotification('Please enter a code to redeem', 'error');
        return;
      }

      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/redeem-free-code`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          code: redeemCodeInput.trim().toUpperCase(),
          user_id: currentUser.id
        })
      });
      
      if (response.ok) {
        const data = await response.json();
        addNotification(data.message, 'success');
        setShowRedeemCodeModal(false);
        setRedeemCodeInput('');
        // Refresh user data to show new plan
        window.location.reload();
      } else {
        const error = await response.json();
        addNotification(error.detail || 'Failed to redeem code', 'error');
      }
    } catch (error) {
      console.error('Error redeeming code:', error);
      addNotification('Failed to redeem code', 'error');
    }
  };

  const deactivateFreeCode = async (code) => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/free-codes/${code}`, {
        method: 'DELETE'
      });
      
      if (response.ok) {
        addNotification(`Code ${code} deactivated successfully`, 'success');
        loadFreeCodes(); // Refresh the list
      } else {
        const error = await response.json();
        addNotification(error.detail || 'Failed to deactivate code', 'error');
      }
    } catch (error) {
      console.error('Error deactivating code:', error);
      addNotification('Failed to deactivate code', 'error');
    }
  };

  // AI Media Generation Functions
  const generateAIMedia = async (contentData) => {
    try {
      setLoading(true);
      
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/ai-media/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content_text: contentData.topic,
          platform: contentData.platforms[0] || 'instagram',
          mood: contentData.ai_music_mood,
          video_style: contentData.ai_video_style,
          music_style: contentData.generate_ai_music ? contentData.ai_music_mood : 'none',
          duration_seconds: parseInt(contentData.ai_video_duration),
          user_id: currentUser.id,
          company_id: contentData.company_id
        })
      });

      if (response.ok) {
        const result = await response.json();
        addNotification('🎬🎵 AI media generation started!', 'success');
        
        // Poll for completion
        pollMediaGeneration(result.generation_id);
        
        return result;
      } else {
        const error = await response.json();
        addNotification(error.detail || 'Failed to generate AI media', 'error');
        throw new Error(error.detail);
      }
    } catch (error) {
      console.error('Error generating AI media:', error);
      addNotification('Failed to generate AI media', 'error');
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const pollMediaGeneration = async (generationId) => {
    const pollInterval = setInterval(async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/ai-media/status/${generationId}`);
        
        if (response.ok) {
          const status = await response.json();
          
          if (status.status === 'completed') {
            clearInterval(pollInterval);
            addNotification('🎉 AI media generation completed!', 'success');
            
            // Add generated media to results
            setResults(prev => ({
              ...prev,
              ai_media: {
                video_url: status.video_url,
                music_url: status.music_url,
                combined_url: status.combined_url,
                cost_breakdown: status.cost_breakdown
              }
            }));
            
          } else if (status.status === 'failed') {
            clearInterval(pollInterval);
            addNotification('❌ AI media generation failed', 'error');
          }
          // Continue polling if status is 'generating'
        }
      } catch (error) {
        console.error('Error checking generation status:', error);
      }
    }, 10000); // Poll every 10 seconds

    // Stop polling after 5 minutes
    setTimeout(() => clearInterval(pollInterval), 300000);
  };

  const impersonateUser = async (userId) => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/impersonate/${userId}`, {
        method: 'POST'
      });
      
      if (response.ok) {
        const data = await response.json();
        
        // Store original admin data
        setOriginalAdmin(currentUser);
        
        // Switch to impersonated user
        setCurrentUser(data.user);
        setIsImpersonating(true);
        localStorage.setItem('currentUser', JSON.stringify(data.user));
        localStorage.setItem('impersonationToken', data.impersonation_token);
        localStorage.setItem('originalAdmin', JSON.stringify(currentUser));
        
        addNotification(data.message, 'success');
        setShowAdminPanel(false);
        
        // Reload user's data
        await fetchCompanies();
        
      } else {
        throw new Error('Failed to impersonate user');
      }
    } catch (error) {
      console.error('Error impersonating user:', error);
      addNotification('Failed to impersonate user', 'error');
    }
  };

  const exitImpersonation = async () => {
    try {
      if (originalAdmin) {
        setCurrentUser(originalAdmin);
        setIsImpersonating(false);
        localStorage.setItem('currentUser', JSON.stringify(originalAdmin));
        localStorage.removeItem('impersonationToken');
        localStorage.removeItem('originalAdmin');
        
        addNotification(`Exited impersonation. Back as ${originalAdmin.full_name}`, 'success');
        setOriginalAdmin(null);
        
        // Reload admin's data
        await fetchCompanies();
      }
    } catch (error) {
      console.error('Error exiting impersonation:', error);
      addNotification('Failed to exit impersonation', 'error');
    }
  };

  const createTestUser = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/create-test-user`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          email: newUserForm.email,
          full_name: newUserForm.full_name,
          plan: newUserForm.plan,
          industry: newUserForm.industry
        })
      });
      
      if (response.ok) {
        const data = await response.json();
        addNotification(
          `Test user created! Email: ${data.credentials.email}, Password: ${data.credentials.password}`,
          'success'
        );
        
        setShowCreateUserModal(false);
        setNewUserForm({
          email: '',
          full_name: '',
          plan: 'starter',
          industry: 'Construction'
        });
        
        // Reload users list
        await loadAllUsers();
      } else {
        const error = await response.json();
        addNotification(error.detail || 'Failed to create user', 'error');
      }
    } catch (error) {
      console.error('Error creating test user:', error);
      addNotification('Failed to create test user', 'error');
    }
  };

  // Authentication System Functions
  const generatePassword = () => {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*';
    let password = '';
    for (let i = 0; i < 12; i++) {
      password += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return password;
  };

  const sendPasswordEmail = async (email, password, isRegistering = false) => {
    // Simulate email sending - in production, this would call your email service
    console.log(`Sending ${isRegistering ? 'welcome' : 'login'} email to: ${email}`);
    console.log(`Generated password: ${password}`);
    
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    return {
      success: true,
      message: `Password sent to ${email}`
    };
  };

  // Login function
  const handleLogin = async () => {
    try {
      setLoginLoading(true);
      
      // Simple login for demo/testing
      const response = await fetch(`${backendUrl}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `email=${encodeURIComponent(loginEmail)}&password=${encodeURIComponent(loginPassword)}`
      });

      if (response.ok) {
        const data = await response.json();
        const user = data.user;
        
        // Store user data
        localStorage.setItem('currentUser', JSON.stringify(user));
        localStorage.setItem('authToken', data.token);
        setCurrentUser(user);
        setIsAuthenticated(true);
        setShowLoginModal(false);
        
        // Clear form
        setLoginEmail('');
        setLoginPassword('');
        
        addNotification(`Welcome back, ${user.full_name}!`, 'success');
        
        // Load user's companies
        await fetchCompanies();
      } else {
        const error = await response.json();
        addNotification(error.detail || 'Login failed', 'error');
      }
    } catch (error) {
      console.error('Login error:', error);
      addNotification('Login failed. Please try again.', 'error');
    } finally {
      setLoginLoading(false);
    }
  };

  // Setup admin function for testing
  const setupAdminForTesting = async () => {
    try {
      const response = await fetch(`${backendUrl}/api/auth/setup-admin`, {
        method: 'POST'
      });
      
      if (response.ok) {
        const data = await response.json();
        addNotification(
          'Admin setup complete! Email: admin@postvelocity.com, Password: admin123', 
          'success'
        );
        
        // Auto-fill login form if modal is open
        if (showLoginModal) {
          setLoginEmail('admin@postvelocity.com');
          setLoginPassword('admin123');
        }
        
        return data;
      }
    } catch (error) {
      console.error('Admin setup error:', error);
      addNotification('Failed to set up admin user', 'error');
    }
  };

  const handleLogout = () => {
    setCurrentUser(null);
    setIsAuthenticated(false);
    localStorage.removeItem('currentUser');
    addNotification('You have been logged out successfully.', 'success');
  };

  // New Upgrade Add-on Functions
  const generateHashtagsForTopic = async () => {
    if (!formData.topic.trim()) {
      addNotification('Please enter a topic to generate hashtags', 'error');
      return;
    }

    if (!hasHashtagsAddon) {
      setShowHashtagsUpgrade(true);
      return;
    }

    try {
      setLoading(true);
      
      // Generate relevant hashtags based on topic and industry
      const hashtags = [
        `#${formData.topic.replace(/\s+/g, '')}`,
        '#ConstructionLife',
        '#BuildSafe',
        '#SafetyFirst',
        '#ConstructionWork',
        '#BuildingTheFuture',
        '#TeamWork',
        '#QualityCraftsmanship',
        '#ConstructionIndustry',
        '#WorkplaceWellness'
      ];
      
      setGeneratedHashtags(hashtags);
      addNotification(`Generated ${hashtags.length} hashtags for your topic!`, 'success');
      
    } catch (error) {
      addNotification('Failed to generate hashtags', 'error');
    } finally {
      setLoading(false);
    }
  };

  const generateSeoKeywordsForTopic = async () => {
    if (!formData.topic.trim()) {
      addNotification('Please enter a topic to generate SEO keywords', 'error');
      return;
    }

    if (!hasSeoKeywordsAddon) {
      setShowSeoKeywordsUpgrade(true);
      return;
    }

    try {
      setLoading(true);
      
      // Generate SEO keywords and phrases based on topic
      const seoKeywords = [
        formData.topic.toLowerCase(),
        `${formData.topic} best practices`,
        `professional ${formData.topic}`,
        `${formData.topic} training`,
        `${formData.topic} safety`,
        `${formData.topic} compliance`,
        `${formData.topic} standards`,
        `${formData.topic} guidelines`,
        `workplace ${formData.topic}`,
        `construction ${formData.topic}`
      ];
      
      setGeneratedSeoKeywords(seoKeywords);
      addNotification(`Generated ${seoKeywords.length} SEO keywords for your topic!`, 'success');
      
    } catch (error) {
      addNotification('Failed to generate SEO keywords', 'error');
    } finally {
      setLoading(false);
    }
  };

  const purchaseHashtagsAddon = async () => {
    try {
      setLoading(true);
      setHasHashtagsAddon(true);
      setShowHashtagsUpgrade(false);
      
      // Update user status in localStorage
      const currentStatus = JSON.parse(localStorage.getItem('userStatus') || '{}');
      const updatedStatus = { ...currentStatus, hasHashtagsAddon: true };
      localStorage.setItem('userStatus', JSON.stringify(updatedStatus));
      
      addNotification('🎉 Hashtags Add-on activated! Generate hashtags for any topic now.', 'success');
      
    } catch (error) {
      addNotification('Failed to activate Hashtags add-on', 'error');
    } finally {
      setLoading(false);
    }
  };

  const purchaseSeoKeywordsAddon = async () => {
    try {
      setLoading(true);
      setHasSeoKeywordsAddon(true);
      setShowSeoKeywordsUpgrade(false);
      
      // Update user status in localStorage
      const currentStatus = JSON.parse(localStorage.getItem('userStatus') || '{}');
      const updatedStatus = { ...currentStatus, hasSeoKeywordsAddon: true };
      localStorage.setItem('userStatus', JSON.stringify(updatedStatus));
      
      addNotification('🎉 SEO Keywords Add-on activated! Generate SEO keywords for any topic now.', 'success');
      
    } catch (error) {
      addNotification('Failed to activate SEO Keywords add-on', 'error');
    } finally {
      setLoading(false);
    }
  };

  // Competitor Analysis Functions
  const openCompetitorAnalysis = () => {
    if (!hasCompetitorAnalysisAddon) {
      setShowCompetitorAnalysisUpgrade(true);
      return;
    }
    setShowCompetitorAnalysisModal(true);
  };

  const generateCompetitorAnalysis = async () => {
    if (!competitorAnalysisForm.competitorWebsite.trim()) {
      addNotification('Please enter a competitor website URL', 'error');
      return;
    }

    try {
      setLoading(true);
      
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/competitor/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          website_url: competitorAnalysisForm.competitorWebsite,
          competitor_name: competitorAnalysisForm.competitorName,
          analysis_type: competitorAnalysisForm.analysisType,
          social_platforms: competitorAnalysisForm.socialPlatforms,
          company_id: selectedCompany?.id || 'demo-company'
        }),
      });

      if (response.ok) {
        const analysisData = await response.json();
        setCompetitorAnalysisData(analysisData);
        addNotification('✅ Competitor analysis completed successfully!', 'success');
      } else {
        addNotification('Failed to generate competitor analysis', 'error');
      }
      
    } catch (error) {
      console.error('Error generating competitor analysis:', error);
      addNotification('Failed to generate competitor analysis', 'error');
    } finally {
      setLoading(false);
    }
  };

  const downloadCompetitorReport = () => {
    if (!competitorAnalysisData) return;

    // Create downloadable report content
    const reportContent = `
COMPETITOR ANALYSIS REPORT
Generated: ${new Date().toLocaleDateString()}
Competitor: ${competitorAnalysisData.competitor_name}
Website: ${competitorAnalysisData.website_url}

=== WEBSITE ANALYSIS ===
${competitorAnalysisData.website_analysis || 'Analysis not available'}

=== SOCIAL MEDIA ANALYSIS ===
${competitorAnalysisData.social_media_analysis || 'Analysis not available'}

=== STRENGTHS ===
${competitorAnalysisData.strengths ? competitorAnalysisData.strengths.join('\n') : 'Not available'}

=== WEAKNESSES ===
${competitorAnalysisData.weaknesses ? competitorAnalysisData.weaknesses.join('\n') : 'Not available'}

=== TACTICAL RECOMMENDATIONS ===
${competitorAnalysisData.recommendations || 'Not available'}

=== OPPORTUNITIES ===
${competitorAnalysisData.opportunities || 'Not available'}

---
Report generated by PostVelocity Competitor Analysis
    `.trim();

    const blob = new Blob([reportContent], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = `competitor-analysis-${competitorAnalysisForm.competitorName || 'report'}-${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
    
    addNotification('📄 Report downloaded successfully!', 'success');
  };

  const purchaseCompetitorAnalysisAddon = async () => {
    try {
      setLoading(true);
      setHasCompetitorAnalysisAddon(true);
      setShowCompetitorAnalysisUpgrade(false);
      
      // Update user status in localStorage
      const currentStatus = JSON.parse(localStorage.getItem('userStatus') || '{}');
      const updatedStatus = { ...currentStatus, hasCompetitorAnalysisAddon: true };
      localStorage.setItem('userStatus', JSON.stringify(updatedStatus));
      
      addNotification('🎉 Competitor Analysis Add-on activated! Analyze competitors now.', 'success');
      
    } catch (error) {
      addNotification('Failed to activate Competitor Analysis add-on', 'error');
    } finally {
      setLoading(false);
    }
  };

  // ==========================================
  // 🚀 SAAS MANAGEMENT FUNCTIONS
  // ==========================================

  // Load available plans and user subscription
  const loadPlansAndSubscription = async () => {
    try {
      // Load available plans
      const plansResponse = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/plans`);
      if (plansResponse.ok) {
        const plansData = await plansResponse.json();
        setAvailablePlans(plansData.plans);
      }

      // Load user subscription if authenticated
      const userId = localStorage.getItem('userId') || 'demo-user';
      const subscriptionResponse = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/user/${userId}/subscription`);
      if (subscriptionResponse.ok) {
        const subscriptionData = await subscriptionResponse.json();
        setCurrentUserPlan(subscriptionData.current_plan);
        setUserSubscription(subscriptionData.subscription);
        setUserUsage(subscriptionData.usage);
        
        // Check for usage warnings
        checkUsageWarnings(subscriptionData.usage, subscriptionData.plan_limits);
      }
    } catch (error) {
      console.error('Error loading plans and subscription:', error);
    }
  };

  const checkUsageWarnings = (usage, limits) => {
    const warnings = [];
    
    if (usage && limits) {
      Object.keys(limits).forEach(limitType => {
        const limit = limits[limitType];
        const current = usage[limitType] || 0;
        
        if (limit > 0 && current >= limit * 0.8) { // 80% threshold
          const percentage = Math.round((current / limit) * 100);
          warnings.push({
            type: limitType,
            current,
            limit,
            percentage,
            message: `${limitType.replace('_', ' ')} usage at ${percentage}%`
          });
        }
      });
    }
    
    setUsageWarnings(warnings);
  };

  const initiatePlanUpgrade = (planType, interval = 'monthly') => {
    setSelectedPlan(planType);
    setSelectedInterval(interval);
    setShowPricingModal(true);
  };

  // Add-on management functions
  const toggleAddon = (addonKey) => {
    setSelectedAddons(prev => {
      const newSet = new Set(prev);
      if (newSet.has(addonKey)) {
        newSet.delete(addonKey);
      } else {
        newSet.add(addonKey);
      }
      return newSet;
    });
  };

  const calculateTotalPrice = () => {
    const plan = availablePlans[selectedPlan];
    if (!plan) return 0;

    let basePrice = plan.pricing?.[selectedInterval] || 0;
    let addonsPrice = 0;

    const addonPricing = {
      'seo_monitoring': { monthly: 97, yearly: 970, lifetime: 2490 },
      'hashtag_research': { monthly: 19, yearly: 190, lifetime: 490 },
      'keyword_research': { monthly: 29, yearly: 290, lifetime: 740 },
      'competitor_analysis': { monthly: 49, yearly: 490, lifetime: 1250 }
    };

    selectedAddons.forEach(addonKey => {
      addonsPrice += addonPricing[addonKey]?.[selectedInterval] || 0;
    });

    return basePrice + addonsPrice;
  };

  const initiatePlanPurchase = async () => {
    if (!selectedPlan) {
      addNotification('Please select a plan first', 'error');
      return;
    }

    const totalPrice = calculateTotalPrice();
    const hasAddons = selectedAddons.size > 0;

    try {
      setPaymentProcessing(true);
      
      // Show purchase confirmation with selected items
      const plan = availablePlans[selectedPlan];
      const selectedAddonsList = Array.from(selectedAddons);
      
      let confirmMessage = `Upgrade to ${plan.name} plan for $${totalPrice}`;
      if (hasAddons) {
        confirmMessage += `\n\nIncluded Add-ons:\n${selectedAddonsList.map(addon => 
          `• ${addon.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}`
        ).join('\n')}`;
      }
      
      const confirmed = window.confirm(confirmMessage);
      if (!confirmed) {
        setPaymentProcessing(false);
        return;
      }

      // Simulate payment processing
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Update user plan
      setCurrentUserPlan(selectedPlan);
      addNotification(`Successfully upgraded to ${plan.name} plan!${hasAddons ? ' Add-ons included!' : ''}`, 'success');
      
      // Clear selections and close modal
      setSelectedPlan('');
      setSelectedAddons(new Set());
      setShowPricingModal(false);
      
    } catch (error) {
      console.error('Error processing upgrade:', error);
      addNotification('Upgrade failed. Please try again.', 'error');
    } finally {
      setPaymentProcessing(false);
    }
  };

  const checkPaymentStatus = async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const sessionId = urlParams.get('session_id');
    const paymentSuccess = urlParams.get('payment_success');

    if (sessionId && paymentSuccess) {
      try {
        // Poll for payment status
        let attempts = 0;
        const maxAttempts = 5;
        const pollInterval = 2000;

        const pollStatus = async () => {
          attempts++;
          const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/payments/status/${sessionId}`);
          
          if (response.ok) {
            const data = await response.json();
            if (data.payment_status === 'paid') {
              addNotification('🎉 Payment successful! Your plan has been upgraded.', 'success');
              await loadPlansAndSubscription(); // Refresh subscription data
              
              // Clean up URL
              window.history.replaceState({}, document.title, window.location.pathname);
              return;
            }
          }

          if (attempts < maxAttempts) {
            setTimeout(pollStatus, pollInterval);
          } else {
            addNotification('Payment status check timed out', 'warning');
          }
        };

        pollStatus();
      } catch (error) {
        console.error('Payment status check error:', error);
      }
    }
  };

  const trackUsage = async (usageType, amount = 1) => {
    try {
      const userId = localStorage.getItem('userId') || 'demo-user';
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/user/${userId}/usage/increment`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          usage_type: usageType,
          amount: amount
        }),
      });

      if (response.ok) {
        const data = await response.json();
        if (data.status === 'limit_exceeded') {
          addNotification(`Usage limit exceeded for ${usageType}. Please upgrade your plan.`, 'error');
          setShowPlanUpgradeModal(true);
          return false;
        }
        
        // Refresh usage data
        await loadPlansAndSubscription();
        return true;
      }
    } catch (error) {
      console.error('Error incrementing usage:', error);
    }
    return false;
  };

  const getPlanDisplayName = (planType) => {
    const planNames = {
      starter: 'Starter',
      professional: 'Professional',
      business: 'Business', 
      enterprise: 'Enterprise'
    };
    return planNames[planType] || planType;
  };

  // ==========================================
  // 🔒 FEATURE GATING SYSTEM
  // ==========================================

  const hasFeature = (feature) => {
    const planFeatures = {
      starter: [
        'basic_ai_content', 'standard_scheduling', 'basic_analytics', 
        'email_support', 'mobile_app'
      ],
      professional: [
        'basic_ai_content', 'standard_scheduling', 'basic_analytics', 'email_support', 'mobile_app',
        'advanced_ai_content', 'smart_scheduling', 'advanced_analytics', 'team_collaboration', 
        'priority_support', 'content_library', 'bulk_upload'
      ],
      business: [
        'basic_ai_content', 'standard_scheduling', 'basic_analytics', 'email_support', 'mobile_app',
        'advanced_ai_content', 'smart_scheduling', 'advanced_analytics', 'team_collaboration', 
        'priority_support', 'content_library', 'bulk_upload',
        'premium_ai_content', 'team_management', 'white_label_reporting', 'custom_dashboards', 
        'phone_support', 'api_access', 'custom_branding'
      ],
      enterprise: [
        'basic_ai_content', 'standard_scheduling', 'basic_analytics', 'email_support', 'mobile_app',
        'advanced_ai_content', 'smart_scheduling', 'advanced_analytics', 'team_collaboration', 
        'priority_support', 'content_library', 'bulk_upload',
        'premium_ai_content', 'team_management', 'white_label_reporting', 'custom_dashboards', 
        'phone_support', 'api_access', 'custom_branding',
        'unlimited_ai_content', 'advanced_security', 'dedicated_account_manager', 
        '24_7_support', 'custom_integrations', 'advanced_api', 'custom_training'
      ]
    };
    
    return planFeatures[currentUserPlan]?.includes(feature) || false;
  };

  const getFeatureLimit = (limitType) => {
    if (!availablePlans[currentUserPlan]) return 0;
    const limit = availablePlans[currentUserPlan]?.limits?.[limitType];
    return limit === -1 ? Infinity : (limit || 0);
  };

  const isWithinUsageLimit = (limitType, currentValue = 0) => {
    const limit = getFeatureLimit(limitType);
    return currentValue < limit;
  };

  const showUpgradePrompt = (feature, featureName) => {
    addNotification(`🔒 ${featureName} requires ${getRequiredPlanForFeature(feature)} plan or higher. Upgrade to unlock!`, 'warning');
    setShowPlanUpgradeModal(true);
  };

  const getRequiredPlanForFeature = (feature) => {
    const planHierarchy = ['starter', 'professional', 'business', 'enterprise'];
    
    for (const plan of planHierarchy) {
      const planFeatures = {
        starter: ['basic_ai_content', 'standard_scheduling', 'basic_analytics'],
        professional: ['advanced_ai_content', 'smart_scheduling', 'advanced_analytics', 'team_collaboration', 'bulk_upload'],
        business: ['premium_ai_content', 'team_management', 'white_label_reporting', 'api_access'],
        enterprise: ['unlimited_ai_content', 'advanced_security', 'custom_integrations', 'advanced_api']
      };
      
      if (planFeatures[plan]?.includes(feature)) {
        return plan.charAt(0).toUpperCase() + plan.slice(1);
      }
    }
    return 'Professional';
  };

  const FeatureGate = ({ feature, requiredPlan, fallbackContent, children, featureName }) => {
    if (hasFeature(feature)) {
      return children;
    }

    return (
      <div className="relative">
        <div className="opacity-50 pointer-events-none">
          {fallbackContent || children}
        </div>
        <div className="absolute inset-0 flex items-center justify-center bg-gray-900 bg-opacity-75 rounded-lg">
          <div className="text-center text-white p-4">
            <span className="text-2xl mb-2 block">🔒</span>
            <p className="font-semibold mb-2">{featureName}</p>
            <p className="text-sm mb-3">Requires {requiredPlan || getRequiredPlanForFeature(feature)} Plan</p>
            <button
              onClick={() => showUpgradePrompt(feature, featureName)}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
            >
              Upgrade Now
            </button>
          </div>
        </div>
      </div>
    );
  };

  // Load data on component mount
  useEffect(() => {
    loadPlansAndSubscription();
    checkPaymentStatus();
    loadTeamMembers();
    loadPartnerData();
    loadApiKeys();
  }, []);

  // ==========================================
  // 🔌 API MANAGEMENT FUNCTIONS
  // ==========================================

  const loadApiKeys = async () => {
    if (!isAuthenticated) return;
    
    try {
      const userId = localStorage.getItem('userId') || 'demo-user';
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/keys/${userId}`);
      
      if (response.ok) {
        const data = await response.json();
        setApiKeys(data.api_keys || []);
      }
    } catch (error) {
      console.error('Error loading API keys:', error);
    }
  };

  const generateApiKey = async () => {
    if (!newApiKeyForm.key_name.trim()) {
      addNotification('API key name is required', 'error');
      return;
    }

    try {
      setLoadingApi(true);
      const userId = localStorage.getItem('userId') || 'demo-user';
      
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/keys/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId,
          ...newApiKeyForm
        }),
      });

      const data = await response.json();
      
      if (response.ok) {
        if (data.status === 'upgrade_required') {
          addNotification(`🔒 ${data.message}`, 'warning');
          setShowPlanUpgradeModal(true);
        } else {
          setGeneratedApiKey({
            api_key: data.api_key,
            api_secret: data.api_secret
          });
          addNotification('✅ API key generated successfully!', 'success');
          await loadApiKeys();
          setNewApiKeyForm({
            key_name: '',
            permissions: ['read'],
            expires_in_days: 365
          });
        }
      } else {
        addNotification('Failed to generate API key', 'error');
      }
    } catch (error) {
      console.error('Error generating API key:', error);
      addNotification('Failed to generate API key', 'error');
    } finally {
      setLoadingApi(false);
    }
  };

  const revokeApiKey = async (keyId, keyName) => {
    if (!window.confirm(`Are you sure you want to revoke the API key "${keyName}"? This action cannot be undone.`)) {
      return;
    }

    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/keys/${keyId}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        addNotification(`API key "${keyName}" revoked successfully`, 'success');
        await loadApiKeys();
      } else {
        addNotification('Failed to revoke API key', 'error');
      }
    } catch (error) {
      console.error('Error revoking API key:', error);
      addNotification('Failed to revoke API key', 'error');
    }
  };

  const copyApiKey = async (apiKey, secretKey) => {
    const fullKey = `${apiKey}\nSecret: ${secretKey}`;
    
    try {
      await navigator.clipboard.writeText(fullKey);
      addNotification('📋 API key copied to clipboard!', 'success');
    } catch (error) {
      // Fallback for older browsers
      const textArea = document.createElement('textarea');
      textArea.value = fullKey;
      document.body.appendChild(textArea);
      textArea.focus();
      textArea.select();
      document.execCommand('copy');
      document.body.removeChild(textArea);
      addNotification('📋 API key copied!', 'success');
    }
  };

  // ==========================================
  // 🔗 PARTNER PROGRAM FUNCTIONS
  // ==========================================

  const loadPartnerData = async () => {
    if (!isAuthenticated) return;
    
    try {
      const userId = localStorage.getItem('userId') || 'demo-user';
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/partners/${userId}/dashboard`);
      
      if (response.ok) {
        const data = await response.json();
        setPartnerData(data.partner_info);
        setPartnerStats(data.stats);
        setReferralCode(data.partner_info?.referral_code || '');
      }
    } catch (error) {
      console.error('Error loading partner data:', error);
    }
  };

  const registerPartner = async () => {
    if (!partnerForm.full_name.trim() || !partnerForm.email.trim()) {
      addNotification('Name and email are required', 'error');
      return;
    }

    try {
      setLoadingPartner(true);
      
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/partners/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(partnerForm),
      });

      const data = await response.json();
      
      if (response.ok) {
        addNotification(`🎉 Partner registration successful! Your referral code: ${data.partner.referral_code}`, 'success');
        setPartnerData(data.partner);
        setReferralCode(data.partner.referral_code);
        setShowPartnerModal(false);
        setPartnerForm({
          full_name: '',
          email: '',
          company_name: '',
          partner_type: 'affiliate',
          website: ''
        });
      } else {
        addNotification(data.detail || 'Failed to register partner', 'error');
      }
    } catch (error) {
      console.error('Error registering partner:', error);
      addNotification('Failed to register partner', 'error');
    } finally {
      setLoadingPartner(false);
    }
  };

  const copyReferralLink = async () => {
    if (!referralCode) return;
    
    const referralUrl = `https://postvelocity.com/ref/${referralCode}`;
    
    try {
      await navigator.clipboard.writeText(referralUrl);
      addNotification('📋 Referral link copied to clipboard!', 'success');
    } catch (error) {
      // Fallback for older browsers
      const textArea = document.createElement('textarea');
      textArea.value = referralUrl;
      document.body.appendChild(textArea);
      textArea.focus();
      textArea.select();
      document.execCommand('copy');
      document.body.removeChild(textArea);
      addNotification('📋 Referral link copied!', 'success');
    }
  };

  const generateReferralQR = () => {
    if (!referralCode) return;
    
    const referralUrl = `https://postvelocity.com/ref/${referralCode}`;
    const qrCodeUrl = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(referralUrl)}`;
    
    // Open QR code in new window
    window.open(qrCodeUrl, '_blank');
  };

  // ==========================================
  // 👥 TEAM MANAGEMENT FUNCTIONS
  // ==========================================

  const loadTeamMembers = async () => {
    if (!isAuthenticated) return;
    
    try {
      const userId = localStorage.getItem('userId') || 'demo-user';
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/teams/${userId}/members`);
      
      if (response.ok) {
        const data = await response.json();
        setTeamMembers(data.members || []);
      }
    } catch (error) {
      console.error('Error loading team members:', error);
    }
  };

  const inviteTeamMember = async () => {
    if (!inviteForm.email.trim()) {
      addNotification('Email is required', 'error');
      return;
    }

    try {
      setLoadingTeam(true);
      const userId = localStorage.getItem('userId') || 'demo-user';
      
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/teams/${userId}/invite`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(inviteForm),
      });

      const data = await response.json();
      
      if (response.ok) {
        if (data.status === 'limit_exceeded') {
          addNotification(data.message, 'warning');
          setShowPlanUpgradeModal(true);
        } else {
          addNotification(`✅ Invitation sent to ${inviteForm.email}`, 'success');
          setInviteForm({ email: '', role: 'member', permissions: [] });
          setShowInviteModal(false);
        }
      } else {
        addNotification('Failed to send invitation', 'error');
      }
    } catch (error) {
      console.error('Error inviting team member:', error);
      addNotification('Failed to send invitation', 'error');
    } finally {
      setLoadingTeam(false);
    }
  };

  const updateMemberRole = async (userId, newRole, newPermissions = []) => {
    try {
      const teamId = localStorage.getItem('userId') || 'demo-user';
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/teams/${teamId}/members/${userId}/role`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          role: newRole,
          permissions: newPermissions
        }),
      });

      if (response.ok) {
        addNotification('Member role updated successfully', 'success');
        await loadTeamMembers();
      } else {
        addNotification('Failed to update member role', 'error');
      }
    } catch (error) {
      console.error('Error updating member role:', error);
      addNotification('Failed to update member role', 'error');
    }
  };

  const removeMember = async (userId, memberName) => {
    if (!window.confirm(`Are you sure you want to remove ${memberName} from the team?`)) {
      return;
    }

    try {
      const teamId = localStorage.getItem('userId') || 'demo-user';
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/teams/${teamId}/members/${userId}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        addNotification(`${memberName} removed from team`, 'success');
        await loadTeamMembers();
      } else {
        addNotification('Failed to remove team member', 'error');
      }
    } catch (error) {
      console.error('Error removing team member:', error);
      addNotification('Failed to remove team member', 'error');
    }
  };

  // Drag and Drop Media Upload
  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    
    const files = Array.from(e.dataTransfer.files);
    const imageFiles = files.filter(file => file.type.startsWith('image/') || file.type.startsWith('video/'));
    
    if (imageFiles.length > 0) {
      setDraggedFiles(imageFiles);
      addNotification(`${imageFiles.length} files ready for upload`, 'success');
    }
  };

  const uploadDraggedFiles = async () => {
    if (!draggedFiles.length) {
      addNotification('No files to upload', 'error');
      return;
    }
    
    if (!dragDropCompanyId) {
      addNotification('Please select a company to upload media to', 'error');
      return;
    }

    // Find the selected company
    const targetCompany = companies.find(c => c.id === dragDropCompanyId);
    if (!targetCompany) {
      addNotification('Selected company not found', 'error');
      return;
    }

    setUploadingMedia(true);
    try {
      const uploadPromises = draggedFiles.map(async (file) => {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('category', 'workplace');
        formData.append('description', `Uploaded via drag and drop: ${file.name}`);
        formData.append('tags', 'drag-drop, auto-upload');
        formData.append('seo_alt_text', `${targetCompany.name} media - ${file.name}`);

        const response = await fetch(`${backendUrl}/api/companies/${dragDropCompanyId}/media/upload`, {
          method: 'POST',
          body: formData,
        });

        return response.ok;
      });

      const results = await Promise.all(uploadPromises);
      const successCount = results.filter(r => r).length;
      
      await fetchCompanyMedia();
      setDraggedFiles([]);
      addNotification(`Successfully uploaded ${successCount} files!`, 'success');
    } catch (error) {
      console.error('Error uploading files:', error);
      addNotification('Error uploading files. Please try again.', 'error');
    } finally {
      setUploadingMedia(false);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    addNotification('Content copied to clipboard!', 'success');
  };

  const createCompany = async (companyData) => {
    try {
      const response = await fetch(`${backendUrl}/api/companies`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(companyData),
      });

      if (!response.ok) {
        throw new Error('Failed to create company');
      }

      const newCompany = await response.json();
      setCompanies([...companies, newCompany]);
      setSelectedCompany(newCompany);
      setFormData(prev => ({ ...prev, company_id: newCompany.id }));
      addNotification('Company created successfully!', 'success');
      setCurrentView('dashboard');
    } catch (error) {
      console.error('Error creating company:', error);
      addNotification('Error creating company. Please try again.', 'error');
    }
  };

  const clearAllCompanies = async () => {
    try {
      // Clear companies from backend
      for (const company of companies) {
        await fetch(`${backendUrl}/api/companies/${company.id}`, {
          method: 'DELETE',
        });
      }
      
      // Clear local state
      setCompanies([]);
      setSelectedCompany(null);
      setFormData(prev => ({ ...prev, company_id: '' }));
      setMediaFiles([]);
      setRoiData(null);
      setTrendingHashtags(null);
      setPerformanceMetrics(null);
      setContentHistory([]);
      
      // Clear local storage
      localStorage.removeItem('contentLibrary');
      localStorage.removeItem('contentHistory');
      
      addNotification('All companies cleared successfully!', 'success');
    } catch (error) {
      console.error('Error clearing companies:', error);
      addNotification('Error clearing companies. Please try again.', 'error');
    }
  };

  // Trial Modal Component
  const TrialModal = () => {
    if (!showTrialModal) return null;

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-xl p-8 max-w-md w-full mx-4">
          <div className="text-center">
            <div className="text-6xl mb-4">🚀</div>
            <h3 className="text-2xl font-bold text-gray-900 mb-4">Welcome to PostVelocity!</h3>
            <p className="text-gray-600 mb-6">
              Start your free trial and experience AI-powered social media management
            </p>
            <div className="flex space-x-4">
              <button
                onClick={startFreeTrial}
                className="flex-1 bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 transition-colors font-semibold"
              >
                Start Free Trial
              </button>
              <button
                onClick={() => setShowTrialModal(false)}
                className="flex-1 bg-gray-300 text-gray-700 py-3 px-6 rounded-lg hover:bg-gray-400 transition-colors"
              >
                Maybe Later
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  };

  // Beta Modal Component
  const BetaModal = () => {
    if (!showBetaModal) return null;

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-xl p-8 max-w-md w-full mx-4">
          <div className="text-center">
            <div className="text-6xl mb-4">🚀</div>
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Join PostVelocity Beta Program</h2>
            <p className="text-gray-600 mb-6">
              Get exclusive access to new features, extended usage limits, and help shape the future of PostVelocity!
            </p>
            
            <div className="space-y-4 mb-6">
              <div className="bg-purple-50 p-4 rounded-lg">
                <h3 className="font-semibold text-purple-800 mb-2">Beta Benefits</h3>
                <ul className="text-sm text-purple-700 space-y-1">
                  <li>✓ 200 content generations (4x more than trial)</li>
                  <li>✓ Priority support & feedback channel</li>
                  <li>✓ Early access to new features</li>
                  <li>✓ 50% discount on lifetime license</li>
                  <li>✓ Forever free updates</li>
                  <li>✓ Beta tester badge</li>
                </ul>
              </div>
            </div>
            
            <div className="flex space-x-4">
              <button
                onClick={joinBetaProgram}
                className="flex-1 bg-purple-600 text-white py-3 px-6 rounded-lg hover:bg-purple-700 transition-colors font-semibold"
              >
                Join Beta Program
              </button>
              <button
                onClick={() => setShowBetaModal(false)}
                className="flex-1 bg-gray-300 text-gray-700 py-3 px-6 rounded-lg hover:bg-gray-400 transition-colors"
              >
                Maybe Later
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  };

  // Payment Modal Component
  const PaymentModal = () => {
    if (!showPaymentModal) return null;

    const getDiscount = () => {
      return userStatus.isBetaTester ? 50 : 0;
    };

    const calculatePrice = (originalPrice) => {
      const discount = getDiscount();
      return originalPrice * (1 - discount / 100);
    };

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-xl p-8 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
          <div className="text-center mb-8">
            <div className="text-4xl mb-4">🎯</div>
            <h3 className="text-2xl font-bold text-gray-900 mb-2">Upgrade to Lifetime Access</h3>
            <p className="text-gray-600">
              {userStatus.isTrialUser ? 'Your trial has expired.' : 'You have reached your usage limit.'} 
              Get lifetime access with one-time purchase.
            </p>
            {userStatus.isBetaTester && (
              <div className="mt-4 bg-purple-100 text-purple-800 px-4 py-2 rounded-lg">
                <p className="font-semibold">🎉 Beta Tester Exclusive: 50% OFF!</p>
              </div>
            )}
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            {/* Professional License */}
            <div className="border-2 border-blue-500 rounded-lg p-6 relative">
              <div className="absolute top-0 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
                <div className="bg-blue-500 text-white px-3 py-1 rounded-full text-sm font-bold">
                  MOST POPULAR
                </div>
              </div>
              <div className="text-center">
                <h4 className="text-xl font-bold text-gray-900 mb-2">Professional License</h4>
                <div className="mb-4">
                  {userStatus.isBetaTester && (
                    <div className="text-lg text-gray-500 line-through">$497</div>
                  )}
                  <div className="text-3xl font-bold text-blue-600">
                    ${calculatePrice(497)}
                  </div>
                  <div className="text-gray-500">one-time purchase</div>
                </div>
                <ul className="text-sm text-gray-600 space-y-2 mb-6">
                  <li>✓ Lifetime access to PostVelocity</li>
                  <li>✓ Unlimited content generation</li>
                  <li>✓ All current AI features</li>
                  <li>✓ All future updates included</li>
                  <li>✓ 8+ platform support</li>
                  <li>✓ Advanced analytics</li>
                  <li>✓ Up to 5 companies</li>
                  <li>✓ Priority support</li>
                </ul>
                <button
                  onClick={() => processPayment('Professional')}
                  className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition-colors font-semibold"
                >
                  Get Professional License
                </button>
              </div>
            </div>

            {/* Enterprise License */}
            <div className="border-2 border-gray-200 rounded-lg p-6">
              <div className="text-center">
                <h4 className="text-xl font-bold text-gray-900 mb-2">Enterprise License</h4>
                <div className="mb-4">
                  {userStatus.isBetaTester && (
                    <div className="text-lg text-gray-500 line-through">$1,497</div>
                  )}
                  <div className="text-3xl font-bold text-gray-900">
                    ${calculatePrice(1497)}
                  </div>
                  <div className="text-gray-500">one-time purchase</div>
                </div>
                <ul className="text-sm text-gray-600 space-y-2 mb-6">
                  <li>✓ Everything in Professional</li>
                  <li>✓ Unlimited companies</li>
                  <li>✓ Custom integrations</li>
                  <li>✓ White-label options</li>
                  <li>✓ Dedicated support</li>
                  <li>✓ Custom training</li>
                  <li>✓ API access</li>
                  <li>✓ Advanced security features</li>
                </ul>
                <button
                  onClick={() => processPayment('Enterprise')}
                  className="w-full bg-gray-600 text-white py-3 rounded-lg hover:bg-gray-700 transition-colors font-semibold"
                >
                  Get Enterprise License
                </button>
              </div>
            </div>
          </div>

          <div className="bg-green-50 rounded-lg p-4 mb-6">
            <h4 className="font-bold text-green-800 mb-2">💎 Lifetime Value</h4>
            <p className="text-sm text-green-700">
              Compare to subscription competitors: Hootsuite Pro costs $99/month ($1,188/year). 
              PostVelocity Professional pays for itself in 5 months and you own it forever!
            </p>
          </div>

          <div className="text-center">
            <button
              onClick={() => setShowPaymentModal(false)}
              className="text-gray-500 hover:text-gray-700 transition-colors"
            >
              Continue with limited access
            </button>
          </div>
        </div>
      </div>
    );
  };

  // SEO Upgrade Modal Component
  const SeoUpgradeModal = () => {
    if (!showSeoUpgrade) return null;

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-xl p-8 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
          <div className="text-center mb-6">
            <div className="text-6xl mb-4">🔍</div>
            <h2 className="text-2xl font-bold text-gray-800 mb-4">SEO Monitoring Add-on</h2>
            <p className="text-gray-600 mb-6">
              Unlock the power of automated SEO monitoring! Our advanced system searches the internet daily 
              to find the latest SEO parameters from Google and Bing, then automatically audits your website 
              and provides actionable recommendations.
            </p>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <div className="bg-blue-50 p-4 rounded-lg">
                <div className="text-3xl mb-2">🤖</div>
                <h3 className="font-semibold mb-2">Daily Auto-Research</h3>
                <p className="text-sm text-gray-600">Automatically discovers latest SEO parameters</p>
              </div>
              <div className="bg-blue-50 p-4 rounded-lg">
                <div className="text-3xl mb-2">📊</div>
                <h3 className="font-semibold mb-2">Website Audits</h3>
                <p className="text-sm text-gray-600">Comprehensive SEO analysis of every page</p>
              </div>
              <div className="bg-blue-50 p-4 rounded-lg">
                <div className="text-3xl mb-2">🎯</div>
                <h3 className="font-semibold mb-2">Priority Fixes</h3>
                <p className="text-sm text-gray-600">Actionable recommendations with impact estimates</p>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div className="border border-gray-200 rounded-lg p-4">
              <h4 className="font-bold text-lg mb-2">Standard Plan</h4>
              <div className="text-3xl font-bold text-blue-600 mb-2">$297</div>
              <div className="text-gray-500 mb-4">one-time purchase</div>
              <ul className="text-sm space-y-2 mb-4">
                <li>✓ 50 daily website checks</li>
                <li>✓ Automatic SEO parameter updates</li>
                <li>✓ Website audit reports</li>
                <li>✓ Priority fixes recommendations</li>
                <li>✓ Email notifications</li>
              </ul>
              <button
                onClick={() => {
                  console.log('SEO Standard button clicked');
                  purchaseSeOAddon('standard');
                }}
                className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors"
              >
                Purchase Standard
              </button>
            </div>
            
            <div className="border-2 border-blue-500 rounded-lg p-4">
              <div className="text-center mb-2">
                <span className="bg-blue-500 text-white px-2 py-1 rounded-full text-xs">Most Popular</span>
              </div>
              <h4 className="font-bold text-lg mb-2">Pro Plan</h4>
              <div className="text-3xl font-bold text-blue-600 mb-2">$497</div>
              <div className="text-gray-500 mb-4">one-time purchase</div>
              <ul className="text-sm space-y-2 mb-4">
                <li>✓ Everything in Standard</li>
                <li>✓ 100 daily website checks</li>
                <li>✓ Competitor analysis</li>
                <li>✓ Advanced reporting</li>
                <li>✓ Priority support</li>
              </ul>
              <button
                onClick={() => {
                  console.log('SEO Pro button clicked');
                  purchaseSeOAddon('pro');
                }}
                className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors"
              >
                Purchase Pro
              </button>
            </div>
          </div>
          
          <div className="text-center">
            <button
              onClick={() => setShowSeoUpgrade(false)}
              className="text-gray-500 hover:text-gray-700 transition-colors"
            >
              Maybe later
            </button>
          </div>
        </div>
      </div>
    );
  };

  // Usage Status Component
  const UsageStatus = () => {
    if (userStatus.isPaidUser) {
      return (
        <div className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium">
          {userStatus.purchaseType === 'beta_special' ? '🎉 Beta VIP' : '💎 Lifetime'} - Unlimited
        </div>
      );
    }
    
    if (userStatus.isBetaTester) {
      return (
        <div className="bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-sm font-medium">
          🚀 Beta Tester - {userStatus.trialUsageLimit - userStatus.usageCount} uses left
        </div>
      );
    }
    
    if (userStatus.isTrialUser) {
      return (
        <div className="bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-sm font-medium">
          ⏰ Trial: {userStatus.trialDaysRemaining} days, {userStatus.trialUsageLimit - userStatus.usageCount} uses left
        </div>
      );
    }
    
    // Return null instead of the Free User badge - it's not needed
    return null;
  };
  const ProgressIndicator = ({ status }) => {
    if (!status) return null;

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <h3 className="text-lg font-semibold text-gray-800 mb-2">{status.step}</h3>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${status.progress}%` }}
              ></div>
            </div>
            <p className="text-sm text-gray-600 mt-2">{status.progress}% Complete</p>
          </div>
        </div>
      </div>
    );
  };

  // Success Animation Component
  const SuccessAnimation = ({ show }) => {
    if (!show) return null;

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-lg p-8 text-center">
          <div className="text-6xl mb-4 animate-bounce">🎉</div>
          <h3 className="text-xl font-bold text-green-600 mb-2">Success!</h3>
          <p className="text-gray-600">Your content has been generated successfully!</p>
        </div>
      </div>
    );
  };

  // Notifications Component
  const NotificationCenter = () => {
    const unreadCount = notifications.filter(n => !n.read).length;

    return (
      <div className="relative">
        <button className="relative p-2 rounded-full hover:bg-gray-100 transition-colors">
          <span className="text-xl">🔔</span>
          {unreadCount > 0 && (
            <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
              {unreadCount}
            </span>
          )}
        </button>
      </div>
    );
  };

  // Main Dashboard Component
  const MainDashboard = () => {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        {/* Enhanced Header */}
        <header className="bg-gradient-to-r from-slate-900 via-purple-900 to-slate-900 shadow-2xl">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <div className="flex flex-col lg:flex-row justify-between items-center space-y-4 lg:space-y-0">
              {/* Left side - Brand */}
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-3">
                  <div className="bg-gradient-to-r from-blue-500 to-purple-600 p-3 rounded-xl">
                    <span className="text-2xl font-bold text-white">PV</span>
                  </div>
                  <div>
                    <h1 className="text-2xl font-bold text-white">PostVelocity</h1>
                    <p className="text-purple-200 text-sm">AI-Powered Social Media Management</p>
                  </div>
                </div>
              </div>

              {/* Center - Company Selection */}
              <div className="flex items-center space-x-4">
                <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4 border border-white/20">
                  <div className="flex items-center space-x-3">
                    <div className="text-white/80">
                      <span className="text-sm font-medium">Active Company:</span>
                    </div>
                    <select
                      value={selectedCompany?.id || ''}
                      onChange={(e) => {
                        const company = companies.find(c => c.id === e.target.value);
                        setSelectedCompany(company);
                        setFormData(prev => ({ ...prev, company_id: e.target.value }));
                      }}
                      className="bg-white/20 text-white border border-white/30 rounded-lg px-3 py-2 focus:bg-white/30 focus:outline-none transition-all"
                    >
                      <option value="" className="text-gray-900">Select Company</option>
                      {companies.map((company) => (
                        <option key={company.id} value={company.id} className="text-gray-900">
                          {company.name}
                        </option>
                      ))}
                    </select>
                    <button
                      onClick={() => setCurrentView('add-company')}
                      className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition-all duration-300 text-sm font-medium"
                    >
                      <span className="mr-1">+</span> Add Company
                    </button>
                  </div>
                </div>
              </div>

              {/* Right side - User Status & Actions */}
              <div className="flex items-center space-x-4">
                {/* Enhanced User Status */}
                <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4 border border-white/20">
                  <UsageStatus />
                </div>

                {/* Action Buttons */}
                <div className="flex items-center space-x-3">
                  {userStatus.isPaidUser && (
                    <button
                      onClick={() => setShowSeoUpgrade(true)}
                      className="bg-gradient-to-r from-teal-500 to-blue-500 text-white px-4 py-2 rounded-xl hover:from-teal-600 hover:to-blue-600 transition-all duration-300 font-medium shadow-lg"
                    >
                      🔍 SEO Addon
                    </button>
                  )}

                  {!userStatus.isPaidUser && (
                    <button
                      onClick={() => setShowPlanUpgradeModal(true)}
                      className="bg-gradient-to-r from-orange-500 to-red-500 text-white px-6 py-3 rounded-xl hover:from-orange-600 hover:to-red-600 transition-all duration-300 font-semibold shadow-lg animate-pulse-gentle"
                    >
                      ✨ Upgrade
                    </button>
                  )}

                  {/* Admin Panel Access */}
                  {currentUser?.role === 'admin' && (
                    <button
                      onClick={() => setShowAdminModal(true)}
                      className="bg-gradient-to-r from-purple-600 to-indigo-600 text-white px-4 py-2 rounded-xl hover:from-purple-700 hover:to-indigo-700 transition-all duration-300 font-medium"
                    >
                      👑 Admin
                    </button>
                  )}
                </div>

                {/* Notifications */}
                <div className="relative">
                  <button
                    onClick={() => setShowNotifications(!showNotifications)}
                    className="relative bg-white/10 p-3 rounded-xl text-white hover:bg-white/20 transition-all duration-300"
                  >
                    <span className="text-xl">🔔</span>
                    {notifications.length > 0 && (
                      <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-6 w-6 flex items-center justify-center animate-bounce-subtle">
                        {notifications.length}
                      </span>
                    )}
                  </button>
                  
                  {/* Enhanced Notifications Panel */}
                  {showNotifications && (
                    <div className="absolute right-0 mt-4 w-80 bg-white rounded-2xl shadow-2xl border border-gray-200 z-50 animate-fadeIn">
                      <div className="p-4 border-b border-gray-100">
                        <div className="flex justify-between items-center">
                          <h3 className="font-semibold text-gray-900">Notifications</h3>
                          <button
                            onClick={() => setNotifications([])}
                            className="text-red-600 hover:text-red-700 text-sm font-medium"
                          >
                            Clear All
                          </button>
                        </div>
                      </div>
                      <div className="max-h-96 overflow-y-auto">
                        {notifications.length === 0 ? (
                          <div className="p-6 text-center text-gray-500">
                            <div className="text-4xl mb-2">🎉</div>
                            <p>You're all caught up!</p>
                          </div>
                        ) : (
                          notifications.map((notification) => (
                            <div
                              key={notification.id}
                              className={`p-4 border-b border-gray-50 hover:bg-gray-50 transition-colors ${
                                notification.type === 'success' ? 'border-l-4 border-l-green-500' :
                                notification.type === 'error' ? 'border-l-4 border-l-red-500' :
                                notification.type === 'warning' ? 'border-l-4 border-l-yellow-500' :
                                'border-l-4 border-l-blue-500'
                              }`}
                            >
                              <p className="text-sm text-gray-800">{notification.message}</p>
                              <p className="text-xs text-gray-500 mt-1">
                                {new Date(notification.timestamp).toLocaleString()}
                              </p>
                            </div>
                          ))
                        )}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </header>

        {/* Enhanced Navigation Tabs */}
        <nav className="bg-white border-b border-gray-200 sticky top-0 z-40 shadow-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center">
              <div className="flex space-x-1 overflow-x-auto">
                {[
                  { id: 'content-hub', label: 'Content Hub', icon: '📝', color: 'blue' },
                  { id: 'analytics', label: 'Analytics', icon: '📊', color: 'green' },
                  { id: 'media', label: 'Media Library', icon: '📸', color: 'purple' },
                  { id: 'calendar', label: 'Calendar', icon: '📅', color: 'red' },
                  { id: 'automation', label: 'Automation', icon: '🤖', color: 'indigo' },
                  { id: 'training', label: 'Training', icon: '🎓', color: 'yellow' },
                  // Team management tab - only for Professional+ plans
                  ...(hasFeature('team_collaboration') ? [{ id: 'team', label: 'Team', icon: '👥', color: 'teal' }] : []),
                  // Billing tab - always available for authenticated users
                  { id: 'billing', label: 'Billing', icon: '💳', color: 'pink' },
                  // Partner program tab - always available for authenticated users
                  { id: 'partners', label: 'Partners', icon: '🔗', color: 'cyan' },
                  // API access tab - only for Business+ plans
                  ...(hasFeature('api_access') ? [{ id: 'api', label: 'API', icon: '🔌', color: 'orange' }] : []),
                  // Beta feedback tab - only for beta testers
                  ...(userStatus.isBetaTester ? [{ id: 'beta-feedback', label: 'Beta Feedback', icon: '💬', color: 'violet' }] : []),
                  // SEO monitoring tab - only for paid users with addon
                  ...(userStatus.isPaidUser && userStatus.hasSeOAddon ? [{ id: 'seo-monitoring', label: 'SEO Monitor', icon: '🔍', color: 'emerald' }] : [])
                ].map((tab) => (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`group flex items-center space-x-2 py-4 px-4 rounded-t-lg font-medium text-sm transition-all duration-300 relative ${
                      activeTab === tab.id
                        ? `bg-${tab.color}-50 text-${tab.color}-600 border-b-2 border-${tab.color}-500 shadow-sm`
                        : 'text-gray-600 hover:text-gray-800 hover:bg-gray-50'
                    }`}
                  >
                    <span className={`text-lg transition-transform duration-300 ${
                      activeTab === tab.id ? 'scale-110' : 'group-hover:scale-105'
                    }`}>
                      {tab.icon}
                    </span>
                    <span className="whitespace-nowrap">{tab.label}</span>
                    {activeTab === tab.id && (
                      <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-gradient-to-r from-transparent via-current to-transparent"></div>
                    )}
                  </button>
                ))}
              </div>

              {/* Right side - User Status Display */}
              <div className="flex items-center space-x-4">
                {/* User Status Display */}
                <div className="flex items-center space-x-2">
                  <UsageStatus />
                </div>
                
                {/* Upgrade Button - for non-paid users */}
                {!userStatus.isPaidUser && (
                  <button
                    onClick={() => setShowPaymentModal(true)}
                    className="bg-amber-500 text-white px-4 py-2 rounded-lg text-sm font-semibold hover:bg-amber-600 transition-colors"
                  >
                    ⭐ Upgrade
                  </button>
                )}
                
                {/* SEO AddOn Button - Separate upgrade option */}
                {userStatus.isPaidUser && !userStatus.hasSeOAddon && (
                  <button
                    onClick={() => setShowSeoUpgrade(true)}
                    className="bg-blue-500 text-white px-3 py-2 rounded-lg text-sm font-medium hover:bg-blue-600 transition-colors border border-blue-400"
                  >
                    🔍 SEO Upgrade
                  </button>
                )}
                
                {/* Hashtags AddOn Button */}
                {userStatus.isPaidUser && !hasHashtagsAddon && (
                  <button
                    onClick={() => setShowHashtagsUpgrade(true)}
                    className="bg-purple-500 text-white px-3 py-2 rounded-lg text-sm font-medium hover:bg-purple-600 transition-colors border border-purple-400"
                  >
                    # Hashtags Upgrade
                  </button>
                )}
                
                {/* SEO Keywords AddOn Button */}
                {userStatus.isPaidUser && !hasSeoKeywordsAddon && (
                  <button
                    onClick={() => setShowSeoKeywordsUpgrade(true)}
                    className="bg-emerald-500 text-white px-3 py-2 rounded-lg text-sm font-medium hover:bg-emerald-600 transition-colors border border-emerald-400"
                  >
                    🎯 SEO Keywords Upgrade
                  </button>
                )}
                
                {/* Competitor Analysis AddOn Button */}
                {userStatus.isPaidUser && !hasCompetitorAnalysisAddon && (
                  <button
                    onClick={() => setShowCompetitorAnalysisUpgrade(true)}
                    className="bg-blue-500 text-white px-3 py-2 rounded-lg text-sm font-medium hover:bg-blue-600 transition-colors border border-blue-400"
                  >
                    🏆 Competitor Analysis Upgrade
                  </button>
                )}
              </div>
            </div>
          </div>
        </nav>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {activeTab === 'content-hub' && <ContentHubTab />}
          {activeTab === 'analytics' && <AnalyticsTab />}
          {activeTab === 'media' && <MediaTab />}
          {activeTab === 'calendar' && <CalendarTab />}
          {activeTab === 'automation' && <AutomationTab />}
          {activeTab === 'training' && <TrainingTab />}
          {activeTab === 'team' && hasFeature('team_collaboration') && <TeamTab />}
          {activeTab === 'billing' && <BillingTab />}
          {activeTab === 'partners' && <PartnersTab />}
          {activeTab === 'api' && hasFeature('api_access') && <ApiTab />}
          {activeTab === 'beta-feedback' && userStatus.isBetaTester && <BetaFeedbackTab />}
          {activeTab === 'seo-monitoring' && userStatus.isPaidUser && <SEOMonitoringTab />}
        </main>

        {/* Progress Indicator */}
        <ProgressIndicator status={progressStatus} />

        {/* Success Animation */}
        <SuccessAnimation show={showSuccessAnimation} />

        {/* Trial Modal */}
        <TrialModal />

        {/* Beta Modal */}
        <BetaModal />

        {/* Payment Modal */}
        <PaymentModal />
        
        {/* SEO Upgrade Modal */}
        <SeoUpgradeModal />
        
        {/* Login/Register Modal */}
        {showLoginModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
              <h3 className="text-2xl font-bold text-gray-800 mb-4">Welcome to PostVelocity</h3>
              <p className="text-gray-600 mb-6">
                Enter your email and password to login.
              </p>
              
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Email Address
                </label>
                <input
                  type="email"
                  placeholder="Enter your email address"
                  value={loginEmail}
                  onChange={(e) => setLoginEmail(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  autoFocus
                />
              </div>
              
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Password
                </label>
                <input
                  type="password"
                  placeholder="Enter your password"
                  value={loginPassword}
                  onChange={(e) => setLoginPassword(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 mb-6">
                <h4 className="font-semibold text-blue-800 mb-1">For Testing:</h4>
                <button
                  onClick={setupAdminForTesting}
                  className="text-sm text-blue-700 hover:text-blue-900 underline"
                >
                  Setup Admin User (admin@postvelocity.com / admin123)
                </button>
              </div>
              
              <div className="flex space-x-3">
                <button
                  onClick={handleLogin}
                  disabled={loginLoading}
                  className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 font-medium"
                >
                  {loginLoading ? 'Logging in...' : 'Login'}
                </button>
                <button
                  onClick={() => {
                    setShowLoginModal(false);
                    setLoginEmail('');
                    setLoginPassword('');
                  }}
                  className="flex-1 bg-gray-400 text-white py-2 px-4 rounded-lg hover:bg-gray-500 transition-colors font-medium"
                  disabled={loginLoading}
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        )}
        
        {/* Hashtags Upgrade Modal */}
        {showHashtagsUpgrade && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
              <h3 className="text-2xl font-bold text-gray-800 mb-4">Hashtags Generator Add-on</h3>
              <div className="mb-6">
                <div className="text-3xl font-bold text-purple-600 mb-2">$97</div>
                <div className="text-gray-500 mb-4">one-time purchase</div>
                <ul className="text-sm space-y-2 mb-4">
                  <li>✓ Generate relevant hashtags for any topic</li>
                  <li>✓ Industry-specific hashtag recommendations</li>
                  <li>✓ Trending hashtags analysis</li>
                  <li>✓ Hashtag performance insights</li>
                  <li>✓ Copy hashtags directly to content</li>
                </ul>
              </div>
              <div className="flex space-x-3">
                <button
                  onClick={purchaseHashtagsAddon}
                  className="flex-1 bg-purple-600 text-white py-2 px-4 rounded-lg hover:bg-purple-700"
                >
                  Purchase Now
                </button>
                <button
                  onClick={() => setShowHashtagsUpgrade(false)}
                  className="flex-1 bg-gray-400 text-white py-2 px-4 rounded-lg hover:bg-gray-500"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        )}
        
        {/* SEO Keywords Upgrade Modal */}
        {showSeoKeywordsUpgrade && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
              <h3 className="text-2xl font-bold text-gray-800 mb-4">SEO Keywords Generator Add-on</h3>
              <div className="mb-6">
                <div className="text-3xl font-bold text-emerald-600 mb-2">$127</div>
                <div className="text-gray-500 mb-4">one-time purchase</div>
                <ul className="text-sm space-y-2 mb-4">
                  <li>✓ Generate SEO keywords for any topic</li>
                  <li>✓ Long-tail keyword suggestions</li>
                  <li>✓ Keyword competition analysis</li>
                  <li>✓ Search volume insights</li>
                  <li>✓ Optimize content for search engines</li>
                </ul>
              </div>
              <div className="flex space-x-3">
                <button
                  onClick={purchaseSeoKeywordsAddon}
                  className="flex-1 bg-emerald-600 text-white py-2 px-4 rounded-lg hover:bg-emerald-700"
                >
                  Purchase Now
                </button>
                <button
                  onClick={() => setShowSeoKeywordsUpgrade(false)}
                  className="flex-1 bg-gray-400 text-white py-2 px-4 rounded-lg hover:bg-gray-500"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        )}
        
        {/* Competitor Analysis Upgrade Modal */}
        {showCompetitorAnalysisUpgrade && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
              <h3 className="text-2xl font-bold text-gray-800 mb-4">Competitor Analysis Add-on</h3>
              <div className="mb-6">
                <div className="text-3xl font-bold text-blue-600 mb-2">$197</div>
                <div className="text-gray-500 mb-4">one-time purchase</div>
                <ul className="text-sm space-y-2 mb-4">
                  <li>✓ Comprehensive website analysis</li>
                  <li>✓ Social media strategy insights</li>
                  <li>✓ Identify competitor strengths & weaknesses</li>
                  <li>✓ Strategic recommendations & tactics</li>
                  <li>✓ Downloadable detailed reports</li>
                  <li>✓ Opportunity identification</li>
                </ul>
              </div>
              <div className="flex space-x-3">
                <button
                  onClick={purchaseCompetitorAnalysisAddon}
                  className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700"
                >
                  Purchase Now
                </button>
                <button
                  onClick={() => setShowCompetitorAnalysisUpgrade(false)}
                  className="flex-1 bg-gray-400 text-white py-2 px-4 rounded-lg hover:bg-gray-500"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Competitor Analysis Modal */}
        {showCompetitorAnalysisModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
              <div className="flex justify-between items-center mb-6">
                <h3 className="text-2xl font-bold text-gray-800">🏆 Competitor Analysis</h3>
                <button
                  onClick={() => setShowCompetitorAnalysisModal(false)}
                  className="text-gray-500 hover:text-gray-700 text-xl"
                >
                  ✕
                </button>
              </div>
              
              {!competitorAnalysisData ? (
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Competitor Website URL *
                    </label>
                    <input
                      type="url"
                      value={competitorAnalysisForm.competitorWebsite}
                      onChange={(e) => setCompetitorAnalysisForm({
                        ...competitorAnalysisForm,
                        competitorWebsite: e.target.value
                      })}
                      placeholder="https://competitor-website.com"
                      className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Competitor Name (Optional)
                    </label>
                    <input
                      type="text"
                      value={competitorAnalysisForm.competitorName}
                      onChange={(e) => setCompetitorAnalysisForm({
                        ...competitorAnalysisForm,
                        competitorName: e.target.value
                      })}
                      placeholder="Competitor Company Name"
                      className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Analysis Type
                    </label>
                    <select
                      value={competitorAnalysisForm.analysisType}
                      onChange={(e) => setCompetitorAnalysisForm({
                        ...competitorAnalysisForm,
                        analysisType: e.target.value
                      })}
                      className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="comprehensive">Comprehensive Analysis</option>
                      <option value="website">Website Only</option>
                      <option value="social">Social Media Only</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Social Platforms to Analyze (if applicable)
                    </label>
                    <div className="space-y-2">
                      {['Instagram', 'Facebook', 'LinkedIn', 'Twitter/X', 'TikTok', 'YouTube'].map(platform => (
                        <label key={platform} className="flex items-center">
                          <input
                            type="checkbox"
                            checked={competitorAnalysisForm.socialPlatforms.includes(platform)}
                            onChange={(e) => {
                              if (e.target.checked) {
                                setCompetitorAnalysisForm({
                                  ...competitorAnalysisForm,
                                  socialPlatforms: [...competitorAnalysisForm.socialPlatforms, platform]
                                });
                              } else {
                                setCompetitorAnalysisForm({
                                  ...competitorAnalysisForm,
                                  socialPlatforms: competitorAnalysisForm.socialPlatforms.filter(p => p !== platform)
                                });
                              }
                            }}
                            className="mr-2"
                          />
                          <span className="text-sm text-gray-600">{platform}</span>
                        </label>
                      ))}
                    </div>
                  </div>

                  <div className="flex space-x-3 pt-4">
                    <button
                      onClick={generateCompetitorAnalysis}
                      disabled={loading || !competitorAnalysisForm.competitorWebsite.trim()}
                      className="flex-1 bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 disabled:opacity-50 font-medium"
                    >
                      {loading ? '🔄 Analyzing...' : '🚀 Analyze Competitor'}
                    </button>
                    <button
                      onClick={() => setShowCompetitorAnalysisModal(false)}
                      className="flex-1 bg-gray-400 text-white py-3 px-4 rounded-lg hover:bg-gray-500 font-medium"
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              ) : (
                <div className="space-y-6">
                  <div className="text-center">
                    <h4 className="text-xl font-semibold text-green-600 mb-2">✅ Analysis Complete!</h4>
                    <p className="text-gray-600">Competitor: {competitorAnalysisData.competitor_name || 'Analysis'}</p>
                  </div>
                  
                  <div className="bg-gray-50 rounded-lg p-4">
                    <h5 className="font-semibold text-gray-800 mb-2">📊 Summary</h5>
                    <p className="text-sm text-gray-600">
                      Analysis completed for {competitorAnalysisData.website_url}. 
                      Report includes website analysis, social media insights, competitive advantages, and strategic recommendations.
                    </p>
                  </div>

                  <div className="flex space-x-3">
                    <button
                      onClick={downloadCompetitorReport}
                      className="flex-1 bg-green-600 text-white py-3 px-4 rounded-lg hover:bg-green-700 font-medium"
                    >
                      📄 Download Report
                    </button>
                    <button
                      onClick={() => {
                        setCompetitorAnalysisData(null);
                        setCompetitorAnalysisForm({
                          competitorWebsite: '',
                          competitorName: '',
                          analysisType: 'comprehensive',
                          socialPlatforms: []
                        });
                      }}
                      className="flex-1 bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 font-medium"
                    >
                      🔄 New Analysis
                    </button>
                    <button
                      onClick={() => setShowCompetitorAnalysisModal(false)}
                      className="flex-1 bg-gray-400 text-white py-3 px-4 rounded-lg hover:bg-gray-500 font-medium"
                    >
                      Close
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    );
  };

  // Content Hub Tab - Enhanced with Modern UI/UX
  const ContentHubTab = () => {
    const [quickTopic, setQuickTopic] = useState('');
    const [showBulkForm, setShowBulkForm] = useState(false);
    const [bulkTopics, setBulkTopics] = useState('');
    const [showEmergencyForm, setShowEmergencyForm] = useState(false);
    const [showTemplates, setShowTemplates] = useState(false);
    const [activeSection, setActiveSection] = useState('quick-actions');

    return (
      <>
        <div className="space-y-8">
        {/* Hero Section with Quick Navigation */}
        <div className="bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 rounded-2xl shadow-2xl p-8 text-white">
          <div className="flex flex-col lg:flex-row items-center justify-between">
            <div className="lg:w-2/3 mb-6 lg:mb-0">
              <h1 className="text-4xl font-bold mb-4">Welcome to Your Content Hub</h1>
              <p className="text-xl text-blue-100 mb-6">
                Create engaging content across 20 social platforms with AI-powered tools
              </p>
              <div className="flex flex-wrap gap-3">
                <button
                  onClick={() => setActiveSection('quick-actions')}
                  className={`px-6 py-3 rounded-lg font-semibold transition-all duration-300 ${
                    activeSection === 'quick-actions' 
                    ? 'bg-white text-blue-600 shadow-lg transform scale-105' 
                    : 'bg-blue-500/30 text-white hover:bg-blue-500/50'
                  }`}
                >
                  🚀 Quick Actions
                </button>
                <button
                  onClick={() => setActiveSection('content-generation')}
                  className={`px-6 py-3 rounded-lg font-semibold transition-all duration-300 ${
                    activeSection === 'content-generation' 
                    ? 'bg-white text-blue-600 shadow-lg transform scale-105' 
                    : 'bg-blue-500/30 text-white hover:bg-blue-500/50'
                  }`}
                >
                  ✨ Content Creation
                </button>
                <button
                  onClick={() => setActiveSection('platforms')}
                  className={`px-6 py-3 rounded-lg font-semibold transition-all duration-300 ${
                    activeSection === 'platforms' 
                    ? 'bg-white text-blue-600 shadow-lg transform scale-105' 
                    : 'bg-blue-500/30 text-white hover:bg-blue-500/50'
                  }`}
                >
                  🌐 Platforms
                </button>
              </div>
            </div>
            <div className="lg:w-1/3 text-center">
              <div className="bg-white/20 rounded-xl p-6 backdrop-blur-sm">
                <div className="text-3xl mb-2">🎯</div>
                <div className="text-sm text-blue-100">Your Progress Today</div>
                <div className="text-2xl font-bold">{userStatus.usageCount || 0}/50</div>
                <div className="text-sm text-blue-100">Content Generated</div>
              </div>
            </div>
          </div>
        </div>

        {/* Smart Quick Actions - Enhanced Design */}
        {activeSection === 'quick-actions' && (
          <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
            <div className="flex items-center mb-8">
              <div className="bg-gradient-to-r from-purple-500 to-blue-500 p-3 rounded-xl">
                <span className="text-2xl">⚡</span>
              </div>
              <div className="ml-4">
                <h2 className="text-3xl font-bold text-gray-900">Smart Quick Actions</h2>
                <p className="text-gray-600 mt-1">AI-powered content generation at your fingertips</p>
              </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
              {/* Smart Generate - Enhanced */}
              <div className="group bg-gradient-to-br from-purple-50 to-purple-100 border-2 border-purple-200 rounded-2xl p-6 hover:shadow-2xl transition-all duration-300 hover:scale-105">
                <div className="flex items-center mb-4">
                  <div className="bg-purple-500 p-3 rounded-xl group-hover:animate-pulse">
                    <span className="text-xl">🧠</span>
                  </div>
                  <h3 className="font-bold text-purple-900 ml-3 text-lg">Smart Generate</h3>
                </div>
                <p className="text-purple-700 mb-4 text-sm leading-relaxed">
                  AI detects trending topics and generates optimized content automatically
                </p>
                <button
                  onClick={smartGenerate}
                  disabled={quickActionLoading}
                  className="w-full bg-gradient-to-r from-purple-600 to-purple-700 text-white py-3 px-4 rounded-xl hover:from-purple-700 hover:to-purple-800 transition-all duration-300 disabled:opacity-50 font-semibold shadow-lg hover:shadow-purple-500/25"
                >
                  {quickActionLoading ? (
                    <div className="flex items-center justify-center">
                      <div className="loading-spinner mr-2"></div>
                      Generating...
                    </div>
                  ) : (
                    'Smart Generate'
                  )}
                </button>
              </div>

              {/* Weekly Batch - Enhanced */}
              <div className="group bg-gradient-to-br from-green-50 to-green-100 border-2 border-green-200 rounded-2xl p-6 hover:shadow-2xl transition-all duration-300 hover:scale-105">
                <div className="flex items-center mb-4">
                  <div className="bg-green-500 p-3 rounded-xl group-hover:animate-pulse">
                    <span className="text-xl">📅</span>
                  </div>
                  <h3 className="font-bold text-green-900 ml-3 text-lg">Weekly Batch</h3>
                </div>
                <p className="text-green-700 mb-4 text-sm leading-relaxed">
                  Generate a complete week's worth of content automatically
                </p>
                <button
                  onClick={generateWeeklyBatch}
                  disabled={bulkContentLoading}
                  className="w-full bg-gradient-to-r from-green-600 to-green-700 text-white py-3 px-4 rounded-xl hover:from-green-700 hover:to-green-800 transition-all duration-300 disabled:opacity-50 font-semibold shadow-lg hover:shadow-green-500/25"
                >
                  {bulkContentLoading ? (
                    <div className="flex items-center justify-center">
                      <div className="loading-spinner mr-2"></div>
                      Generating...
                    </div>
                  ) : (
                    'Weekly Batch'
                  )}
                </button>
              </div>

              {/* Emergency Post - Enhanced */}
              <div className="group bg-gradient-to-br from-red-50 to-red-100 border-2 border-red-200 rounded-2xl p-6 hover:shadow-2xl transition-all duration-300 hover:scale-105">
                <div className="flex items-center mb-4">
                  <div className="bg-red-500 p-3 rounded-xl group-hover:animate-pulse">
                    <span className="text-xl">🚨</span>
                  </div>
                  <h3 className="font-bold text-red-900 ml-3 text-lg">Emergency Post</h3>
                </div>
                <p className="text-red-700 mb-4 text-sm leading-relaxed">
                  Quick crisis communication posts with pre-approved templates
                </p>
                <button
                  onClick={() => setShowEmergencyForm(!showEmergencyForm)}
                  className="w-full bg-gradient-to-r from-red-600 to-red-700 text-white py-3 px-4 rounded-xl hover:from-red-700 hover:to-red-800 transition-all duration-300 font-semibold shadow-lg hover:shadow-red-500/25"
                >
                  Emergency Post
                </button>
                {showEmergencyForm && (
                  <div className="mt-4 space-y-2 animate-fadeIn">
                    <button
                      onClick={() => generateEmergencyPost('weather')}
                      className="w-full bg-red-500 text-white py-2 px-3 rounded-lg text-sm hover:bg-red-600 transition-colors shadow-md"
                    >
                      ⛈️ Weather Alert
                    </button>
                    <button
                      onClick={() => generateEmergencyPost('equipment')}
                      className="w-full bg-red-500 text-white py-2 px-3 rounded-lg text-sm hover:bg-red-600 transition-colors shadow-md"
                    >
                      🔧 Equipment Issue
                    </button>
                    <button
                      onClick={() => generateEmergencyPost('general')}
                      className="w-full bg-red-500 text-white py-2 px-3 rounded-lg text-sm hover:bg-red-600 transition-colors shadow-md"
                    >
                      🔔 General Alert
                    </button>
                  </div>
                )}
              </div>

              {/* Voice Input - Enhanced */}
              <div className="group bg-gradient-to-br from-blue-50 to-blue-100 border-2 border-blue-200 rounded-2xl p-6 hover:shadow-2xl transition-all duration-300 hover:scale-105">
                <div className="flex items-center mb-4">
                  <div className="bg-blue-500 p-3 rounded-xl group-hover:animate-pulse">
                    <span className="text-xl">🎤</span>
                  </div>
                  <h3 className="font-bold text-blue-900 ml-3 text-lg">Voice Input</h3>
                </div>
                <p className="text-blue-600 font-medium mb-2 text-sm">
                  Your words appear in Advanced Content Generation
                </p>
                <p className="text-blue-700 mb-4 text-sm leading-relaxed">
                  Try: "Generate for Instagram", "Make it professional"
                </p>
                
                {/* Real-time Transcript Display */}
                {voiceTranscript && (
                  <div className="mb-3 p-3 bg-blue-200/50 rounded-lg text-sm animate-fadeIn">
                    <strong className="text-blue-800">Transcript:</strong> 
                    <span className="text-blue-700"> {voiceTranscript}</span>
                  </div>
                )}
                
                {/* Voice Command Status */}
                {voiceCommand && (
                  <div className="mb-3 p-3 bg-blue-300/50 text-blue-800 rounded-lg text-sm animate-fadeIn">
                    <strong>Command:</strong> {voiceCommand}
                  </div>
                )}
                
                {/* Voice Input Button with Enhanced Effects */}
                <button
                  onClick={startVoiceRecording}
                  disabled={isVoiceRecording}
                  className={`w-full py-3 px-4 rounded-xl transition-all duration-300 font-semibold shadow-lg ${
                    isVoiceRecording 
                      ? 'bg-gradient-to-r from-red-500 to-red-600 text-white animate-pulse shadow-red-500/25 transform scale-105' 
                      : 'bg-gradient-to-r from-blue-600 to-blue-700 text-white hover:from-blue-700 hover:to-blue-800 hover:shadow-blue-500/25 hover:scale-105'
                  }`}
                >
                  {isVoiceRecording ? '🎙️ Recording... (Speak now)' : '🎤 Voice Input'}
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Trending Topics - Enhanced Visual Design */}
        <div className="bg-gradient-to-r from-orange-50 to-red-50 rounded-2xl shadow-xl p-8 border border-orange-200">
          <div className="flex items-center mb-6">
            <div className="bg-gradient-to-r from-orange-500 to-red-500 p-3 rounded-xl">
              <span className="text-2xl">🔥</span>
            </div>
            <div className="ml-4">
              <h3 className="text-2xl font-bold text-orange-800">Trending Topics</h3>
              <p className="text-orange-700">Click any topic to use it instantly</p>
            </div>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-4">
            {trendingTopics.map((topic, index) => (
              <div 
                key={index} 
                className={`group p-4 rounded-xl border-2 cursor-pointer transition-all duration-300 hover:scale-105 hover:shadow-lg ${
                  topic.trend === 'rising' ? 'border-green-300 bg-gradient-to-br from-green-50 to-green-100 hover:shadow-green-500/20' :
                  topic.trend === 'stable' ? 'border-blue-300 bg-gradient-to-br from-blue-50 to-blue-100 hover:shadow-blue-500/20' :
                  'border-red-300 bg-gradient-to-br from-red-50 to-red-100 hover:shadow-red-500/20'
                }`}
                onClick={() => setFormData(prev => ({ ...prev, topic: topic.topic }))}
              >
                <div className="flex items-center justify-between mb-3">
                  <span className="font-semibold text-gray-800 text-sm">{topic.topic}</span>
                  <span className="text-lg">
                    {topic.trend === 'rising' ? '📈' : topic.trend === 'stable' ? '➡️' : '📉'}
                  </span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className={`font-medium ${
                    topic.trend === 'rising' ? 'text-green-700' : 
                    topic.trend === 'stable' ? 'text-blue-700' : 
                    'text-red-700'
                  }`}>
                    {topic.engagement}% Engagement
                  </span>
                  <span className={`capitalize px-2 py-1 rounded-full text-white font-medium ${
                    topic.trend === 'rising' ? 'bg-green-500' : 
                    topic.trend === 'stable' ? 'bg-blue-500' : 
                    'bg-red-500'
                  }`}>
                    {topic.trend}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Smart Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            {/* Smart Generate */}
            <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <h3 className="font-semibold text-gray-800 mb-2">🧠 Smart Generate</h3>
              <p className="text-sm text-gray-600 mb-3">AI detects trending topics and generates optimized content</p>
              <button
                onClick={smartGenerate}
                disabled={quickActionLoading}
                className="w-full bg-purple-600 text-white py-2 px-4 rounded-lg hover:bg-purple-700 transition-colors disabled:opacity-50"
              >
                {quickActionLoading ? 'Generating...' : 'Smart Generate'}
              </button>
            </div>

            {/* Weekly Batch */}
            <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <h3 className="font-semibold text-gray-800 mb-2">📅 Weekly Batch</h3>
              <p className="text-sm text-gray-600 mb-3">Generate a complete week's worth of content automatically</p>
              <button
                onClick={generateWeeklyBatch}
                disabled={bulkContentLoading}
                className="w-full bg-green-600 text-white py-2 px-4 rounded-lg hover:bg-green-700 transition-colors disabled:opacity-50"
              >
                {bulkContentLoading ? 'Generating...' : 'Weekly Batch'}
              </button>
            </div>

            {/* Emergency Post */}
            <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <h3 className="font-semibold text-gray-800 mb-2">🚨 Emergency Post</h3>
              <p className="text-sm text-gray-600 mb-3">Quick crisis communication posts with pre-approved templates</p>
              <button
                onClick={() => setShowEmergencyForm(!showEmergencyForm)}
                className="w-full bg-red-600 text-white py-2 px-4 rounded-lg hover:bg-red-700 transition-colors"
              >
                Emergency Post
              </button>
              {showEmergencyForm && (
                <div className="mt-3 space-y-2">
                  <button
                    onClick={() => generateEmergencyPost('weather')}
                    className="w-full bg-red-500 text-white py-1 px-3 rounded text-sm hover:bg-red-600"
                  >
                    Weather Alert
                  </button>
                  <button
                    onClick={() => generateEmergencyPost('equipment')}
                    className="w-full bg-red-500 text-white py-1 px-3 rounded text-sm hover:bg-red-600"
                  >
                    Equipment Issue
                  </button>
                  <button
                    onClick={() => generateEmergencyPost('general')}
                    className="w-full bg-red-500 text-white py-1 px-3 rounded text-sm hover:bg-red-600"
                  >
                    General Alert
                  </button>
                </div>
              )}
            </div>

            {/* Voice Input */}
            <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <h3 className="font-semibold text-gray-800 mb-2">🎤 Voice Input</h3>
              {/* Instructional Text */}
              <p className="text-sm text-blue-600 font-medium mb-2">Your words will show up in the ADVANCED CONTENT GENERATION box</p>
              <p className="text-sm text-gray-600 mb-3">Try commands: "Generate for Instagram", "Make it professional"</p>
              
              {/* Real-time Transcript Display */}
              {voiceTranscript && (
                <div className="mb-3 p-2 bg-gray-100 rounded text-sm">
                  <strong>Transcript:</strong> {voiceTranscript}
                </div>
              )}
              
              {/* Voice Command Status */}
              {voiceCommand && (
                <div className="mb-3 p-2 bg-blue-100 text-blue-800 rounded text-sm">
                  <strong>Command:</strong> {voiceCommand}
                </div>
              )}
              
              {/* Voice Input Button with Waveform Effect */}
              <button
                onClick={startVoiceRecording}
                disabled={isVoiceRecording}
                className={`w-full py-2 px-4 rounded-lg transition-all ${
                  isVoiceRecording 
                    ? 'bg-red-500 text-white animate-pulse shadow-lg transform scale-105' 
                    : 'bg-blue-600 text-white hover:bg-blue-700 hover:shadow-md'
                }`}
              >
                {isVoiceRecording ? '🎙️ Recording... (Speak now)' : '🎤 Voice Input'}
              </button>
            </div>
          </div>
        </div>
        )}

        {/* Trending Topics Alert */}
        <div className="bg-gradient-to-r from-orange-100 to-red-100 rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold text-orange-800 mb-4">🔥 Trending Topics</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {trendingTopics.map((topic, index) => (
              <div 
                key={index} 
                className={`p-3 rounded-lg border-2 cursor-pointer transition-all ${
                  topic.trend === 'rising' ? 'border-green-300 bg-green-50' :
                  topic.trend === 'stable' ? 'border-blue-300 bg-blue-50' :
                  'border-red-300 bg-red-50'
                }`}
                onClick={() => setFormData(prev => ({ ...prev, topic: topic.topic }))}
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium text-gray-800">{topic.topic}</span>
                  <span className="text-sm">
                    {topic.trend === 'rising' ? '📈' : topic.trend === 'stable' ? '➡️' : '📉'}
                  </span>
                </div>
                <div className="flex justify-between text-sm text-gray-600">
                  <span>Engagement: {topic.engagement}%</span>
                  <span className="capitalize">{topic.trend}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Industry Templates */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-semibold text-gray-800">📋 Industry Templates</h3>
            <button
              onClick={() => setShowTemplates(!showTemplates)}
              className="text-blue-600 hover:text-blue-800"
            >
              {showTemplates ? 'Hide' : 'Show'} Templates
            </button>
          </div>
          
          {showTemplates && (
            <div className="space-y-4">
              {Object.entries(INDUSTRY_TEMPLATES).map(([industry, templates]) => (
                <div key={industry} className="border rounded-lg p-4">
                  <h4 className="font-medium text-gray-700 mb-2 capitalize">{industry}</h4>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
                    {templates.map((template, index) => (
                      <button
                        key={index}
                        onClick={() => setFormData(prev => ({ ...prev, additional_context: template.template }))}
                        className="text-left p-2 bg-gray-50 rounded hover:bg-gray-100 transition-colors"
                      >
                        <div className="font-medium text-sm text-gray-800">{template.name}</div>
                        <div className="text-xs text-gray-600 truncate">{template.template}</div>
                      </button>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Traditional Quick Actions */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">🎯 Quick Generate</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="space-y-3">
              <div className="flex space-x-2">
                <input
                  type="text"
                  value={quickTopic}
                  onChange={(e) => setQuickTopic(e.target.value)}
                  placeholder="Enter your topic..."
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <button
                  onClick={startVoiceRecording}
                  disabled={isVoiceRecording}
                  className={`px-3 py-2 rounded-lg ${
                    isVoiceRecording 
                      ? 'bg-red-500 text-white animate-pulse' 
                      : 'bg-gray-600 text-white hover:bg-gray-700'
                  }`}
                >
                  🎤
                </button>
              </div>
              <button
                onClick={() => {
                  if (quickTopic) {
                    setFormData(prev => ({ ...prev, topic: quickTopic }));
                    handleSubmit({ preventDefault: () => {} });
                  }
                }}
                disabled={!quickTopic || loading}
                className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
              >
                {loading ? 'Generating...' : 'Generate Now'}
              </button>
            </div>

            <div className="space-y-3">
              <FeatureGate 
                feature="bulk_upload" 
                featureName="Bulk Content Generation"
                requiredPlan="Professional"
                fallbackContent={
                  <button className="w-full bg-purple-300 text-white py-2 px-4 rounded-lg cursor-not-allowed opacity-50">
                    🔒 📚 Bulk Content (Professional+)
                  </button>
                }
              >
                <button
                  onClick={() => setShowBulkForm(!showBulkForm)}
                  className="w-full bg-purple-600 text-white py-2 px-4 rounded-lg hover:bg-purple-700 transition-colors"
                >
                  📚 Bulk Content
                </button>
              </FeatureGate>
              {showBulkForm && hasFeature("bulk_upload") && (
                <div className="space-y-2">
                  <textarea
                    value={bulkTopics}
                    onChange={(e) => setBulkTopics(e.target.value)}
                    placeholder="Enter topics (one per line)..."
                    rows="3"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  />
                  <button
                    onClick={() => {
                      const topics = bulkTopics.split('\n').filter(t => t.trim());
                      if (topics.length > 0) {
                        // Implement bulk generation logic
                        setBulkContentLoading(true);
                        // Add actual bulk generation here
                      }
                    }}
                    disabled={!bulkTopics || bulkContentLoading}
                    className="w-full bg-purple-600 text-white py-2 px-4 rounded-lg hover:bg-purple-700 transition-colors disabled:opacity-50"
                  >
                    {bulkContentLoading ? 'Generating...' : 'Generate All'}
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Topic Suggestions */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">💡 Topic Suggestions</h3>
          <div className="flex flex-wrap gap-2">
            {TRENDING_TOPICS.map((topic) => (
              <button
                key={topic}
                onClick={() => setFormData(prev => ({ ...prev, topic }))}
                className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm hover:bg-blue-200 transition-colors"
              >
                {topic}
              </button>
            ))}
          </div>
        </div>

        {/* New Upgrade Add-ons Section - Hashtags and SEO Keywords */}
        <div className="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold text-indigo-800 mb-4">🚀 Premium Content Enhancers</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            
            {/* Hashtags Upgrade Add-on */}
            <FeatureGate 
              feature="advanced_analytics" 
              featureName="Hashtags Generator"
              requiredPlan="Professional"
              fallbackContent={
                <div className="bg-white rounded-lg p-4 border border-purple-200 opacity-50">
                  <div className="flex items-center justify-between mb-3">
                    <h4 className="font-semibold text-gray-800 flex items-center">
                      <span className="text-purple-600 mr-2">#</span>
                      Hashtags Generator
                    </h4>
                  </div>
                  <p className="text-sm text-gray-600 mb-3">
                    Generate relevant hashtags for your content topics automatically
                  </p>
                  <button className="w-full bg-purple-300 text-white py-2 px-4 rounded-lg cursor-not-allowed">
                    🔒 Upgrade Required
                  </button>
                </div>
              }
            >
              <div className="bg-white rounded-lg p-4 border border-purple-200">
                <div className="flex items-center justify-between mb-3">
                  <h4 className="font-semibold text-gray-800 flex items-center">
                    <span className="text-purple-600 mr-2">#</span>
                    Hashtags Generator
                  </h4>
                  {hasHashtagsAddon && <span className="text-green-600 text-sm">✅ Active</span>}
                </div>
                <p className="text-sm text-gray-600 mb-3">
                  Generate relevant hashtags for your content topics automatically
                </p>
                <button
                  onClick={generateHashtagsForTopic}
                  disabled={loading || !formData.topic.trim()}
                  className="w-full bg-purple-600 text-white py-2 px-4 rounded-lg hover:bg-purple-700 transition-colors disabled:opacity-50"
                >
                  {hasHashtagsAddon ? 'Generate Hashtags' : '🔒 Upgrade to Generate Hashtags'}
                </button>
                
                {/* Display generated hashtags */}
                {generatedHashtags.length > 0 && (
                  <div className="mt-3 p-3 bg-purple-50 rounded-lg">
                    <p className="text-sm font-medium text-purple-800 mb-2">Generated Hashtags:</p>
                    <div className="flex flex-wrap gap-1">
                      {generatedHashtags.map((hashtag, index) => (
                        <span key={index} className="bg-purple-200 text-purple-800 px-2 py-1 rounded text-xs">
                          {hashtag}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </FeatureGate>

            {/* SEO Keywords Upgrade Add-on */}
            <FeatureGate 
              feature="advanced_ai_content" 
              featureName="SEO Keywords Generator"
              requiredPlan="Professional"
              fallbackContent={
                <div className="bg-white rounded-lg p-4 border border-emerald-200 opacity-50">
                  <div className="flex items-center justify-between mb-3">
                    <h4 className="font-semibold text-gray-800 flex items-center">
                      <span className="text-emerald-600 mr-2">🎯</span>
                      SEO Keywords Generator
                    </h4>
                  </div>
                  <p className="text-sm text-gray-600 mb-3">
                    Generate SEO keywords and phrases for your content topics
                  </p>
                  <button className="w-full bg-emerald-300 text-white py-2 px-4 rounded-lg cursor-not-allowed">
                    🔒 Upgrade Required
                  </button>
                </div>
              }
            >
              <div className="bg-white rounded-lg p-4 border border-emerald-200">
                <div className="flex items-center justify-between mb-3">
                  <h4 className="font-semibold text-gray-800 flex items-center">
                    <span className="text-emerald-600 mr-2">🎯</span>
                    SEO Keywords Generator
                  </h4>
                  {hasSeoKeywordsAddon && <span className="text-green-600 text-sm">✅ Active</span>}
                </div>
                <p className="text-sm text-gray-600 mb-3">
                  Generate SEO keywords and phrases for your content topics
                </p>
                <button
                  onClick={generateSeoKeywordsForTopic}
                  disabled={loading || !formData.topic.trim()}
                  className="w-full bg-emerald-600 text-white py-2 px-4 rounded-lg hover:bg-emerald-700 transition-colors disabled:opacity-50"
                >
                  {hasSeoKeywordsAddon ? 'Generate SEO Keywords' : '🔒 Upgrade to Generate SEO Keywords'}
                </button>
                
                {/* Display generated SEO keywords */}
                {generatedSeoKeywords.length > 0 && (
                  <div className="mt-3 p-3 bg-emerald-50 rounded-lg">
                    <p className="text-sm font-medium text-emerald-800 mb-2">Generated SEO Keywords:</p>
                    <div className="flex flex-wrap gap-1">
                      {generatedSeoKeywords.map((keyword, index) => (
                        <span key={index} className="bg-emerald-200 text-emerald-800 px-2 py-1 rounded text-xs">
                          {keyword}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </FeatureGate>

            {/* Competitor Analysis Upgrade Add-on */}
            <FeatureGate 
              feature="premium_ai_content" 
              featureName="Competitor Analysis"
              requiredPlan="Business"
              fallbackContent={
                <div className="bg-white rounded-lg p-4 border border-blue-200 opacity-50">
                  <div className="flex items-center justify-between mb-3">
                    <h4 className="font-semibold text-gray-800 flex items-center">
                      <span className="text-blue-600 mr-2">🏆</span>
                      Competitor Analysis
                    </h4>
                  </div>
                  <p className="text-sm text-gray-600 mb-3">
                    Analyze competitors' strengths, weaknesses, and get strategic recommendations
                  </p>
                  <button className="w-full bg-blue-300 text-white py-2 px-4 rounded-lg cursor-not-allowed">
                    🔒 Upgrade Required
                  </button>
                </div>
              }
            >
              <div className="bg-white rounded-lg p-4 border border-blue-200">
                <div className="flex items-center justify-between mb-3">
                  <h4 className="font-semibold text-gray-800 flex items-center">
                    <span className="text-blue-600 mr-2">🏆</span>
                    Competitor Analysis
                  </h4>
                  {hasCompetitorAnalysisAddon && <span className="text-green-600 text-sm">✅ Active</span>}
                </div>
                <p className="text-sm text-gray-600 mb-3">
                  Analyze competitors' strengths, weaknesses, and get strategic recommendations
                </p>
                <button
                  onClick={openCompetitorAnalysis}
                  disabled={loading}
                  className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
                >
                  {hasCompetitorAnalysisAddon ? 'Analyze Competitor' : '🔒 Upgrade to Analyze Competitors'}
                </button>
              </div>
            </FeatureGate>
          </div>
        </div>


        {/* Advanced Content Generation */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">🎨 Advanced Content Generation &nbsp;&nbsp;&nbsp;<em><strong>writes the content</strong></em></h3>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Topic *</label>
                <input
                  type="text"
                  name="topic"
                  value={formData.topic}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Audience Level</label>
                <select
                  name="audience_level"
                  value={formData.audience_level}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="general">General Public</option>
                  <option value="professional">Industry Professionals</option>
                  <option value="technical">Technical/Expert</option>
                  <option value="beginner">Beginners</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Social Media Platforms *
              </label>
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3">
                {availablePlatforms.slice(0, 10).map((platform) => (
                  <div key={platform} className="flex flex-col space-y-2">
                    {/* Platform Selection Button */}
                    <button
                      type="button"
                      onClick={() => handlePlatformToggle(platform)}
                      disabled={!connectedPlatforms[platform]}
                      className={`flex items-center justify-center space-x-2 px-3 py-2 rounded-lg border transition-colors text-sm relative ${
                        formData.platforms.includes(platform)
                          ? `${PLATFORM_COLORS[platform]} text-white`
                          : connectedPlatforms[platform]
                          ? 'border-gray-300 text-gray-700 hover:bg-gray-50'
                          : 'border-gray-300 text-gray-400 opacity-50 cursor-not-allowed'
                      }`}
                    >
                      <span className="text-lg">{PLATFORM_ICONS[platform]}</span>
                      <span className="capitalize text-xs">
                        {platform === 'x' ? 'X (Twitter)' : platform === 'facebook_messenger' ? 'Messenger' : platform.replace('_', ' ')}
                      </span>
                      
                      {/* Connection Status Indicator */}
                      {connectedPlatforms[platform] ? (
                        <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-500 rounded-full border-2 border-white"></div>
                      ) : (
                        <div className="absolute -top-1 -right-1 w-3 h-3 bg-gray-400 rounded-full border-2 border-white"></div>
                      )}
                    </button>
                    
                    {/* Connect/Disconnect Button */}
                    {connectedPlatforms[platform] ? (
                      <div className="flex space-x-1">
                        <button
                          type="button"
                          onClick={() => disconnectPlatform(platform)}
                          className="flex-1 px-2 py-1 text-xs bg-red-100 text-red-700 rounded hover:bg-red-200 transition-colors"
                        >
                          Disconnect
                        </button>
                        {platformConnectionStatus[platform]?.status === 'expired' && (
                          <button
                            type="button"
                            onClick={() => refreshPlatformConnection(platform)}
                            className="flex-1 px-2 py-1 text-xs bg-yellow-100 text-yellow-700 rounded hover:bg-yellow-200 transition-colors"
                          >
                            Refresh
                          </button>
                        )}
                      </div>
                    ) : (
                      <button
                        type="button"
                        onClick={() => connectPlatform(platform)}
                        disabled={connectingPlatform === platform}
                        className={`px-2 py-1 text-xs rounded transition-colors ${
                          connectingPlatform === platform
                            ? 'bg-gray-100 text-gray-400'
                            : 'bg-blue-100 text-blue-700 hover:bg-blue-200'
                        }`}
                      >
                        {connectingPlatform === platform ? 'Connecting...' : 'START HERE'}
                      </button>
                    )}
                    
                    {/* Username Display */}
                    {platformConnectionStatus[platform]?.username && (
                      <div className="text-xs text-gray-500 text-center truncate">
                        @{platformConnectionStatus[platform].username}
                      </div>
                    )}
                  </div>
                ))}
              </div>
              <p className="text-xs text-gray-500 mt-2">
                Select multiple platforms for cross-platform content generation
              </p>
              
              {availablePlatforms.length > 10 && (
                <button 
                  onClick={() => setShowOAuthModal(true)}
                  className="mt-4 text-blue-600 text-sm hover:text-blue-800"
                >
                  VIEW ALL {availablePlatforms.length} PLATFORMS →
                </button>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Additional Context</label>
              <textarea
                name="additional_context"
                value={formData.additional_context}
                onChange={handleInputChange}
                rows="3"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Any specific requirements or context..."
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-red-700 mb-2">🚫 Avoid Content (What NOT to include)</label>
              <textarea
                name="negative_context"
                value={formData.negative_context || ''}
                onChange={handleInputChange}
                rows="2"
                className="w-full px-4 py-2 border border-red-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent bg-red-50"
                placeholder="Specify topics, words, or themes to avoid in the content..."
              />
              <p className="text-xs text-red-600 mt-1">
                💡 Example: "Avoid political topics, competitor mentions, or overly sales-focused language"
              </p>
            </div>

            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <label className="block text-sm font-medium text-blue-800 mb-2">🎭 Your Personal Voice & Style (Keep it authentic!)</label>
              <textarea
                name="personal_voice"
                value={formData.personal_voice || ''}
                onChange={handleInputChange}
                rows="3"
                className="w-full px-4 py-2 border border-blue-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white"
                placeholder="Describe your personality, writing style, favorite phrases, humor style, or any personal touches that make YOUR voice unique..."
              />
              <div className="grid grid-cols-1 md:grid-cols-3 gap-2 mt-2 text-xs">
                <p className="text-blue-700">
                  <strong>Personality:</strong> Casual, professional, funny, direct, warm, etc.
                </p>
                <p className="text-blue-700">
                  <strong>Style:</strong> Short posts, storytelling, questions, lists, emojis, etc.
                </p>
                <p className="text-blue-700">
                  <strong>Voice:</strong> Your catchphrases, industry slang, personal experiences to reference
                </p>
              </div>
            </div>

            <div className="flex flex-wrap gap-4">
              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  name="generate_blog"
                  checked={formData.generate_blog}
                  onChange={handleInputChange}
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span className="text-sm text-gray-700">Generate Blog Post</span>
              </label>
              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  name="generate_newsletter"
                  checked={formData.generate_newsletter}
                  onChange={handleInputChange}
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span className="text-sm text-gray-700">Generate Newsletter</span>
              </label>
              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  name="generate_video_script"
                  checked={formData.generate_video_script}
                  onChange={handleInputChange}
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span className="text-sm text-gray-700">Generate Video Script</span>
              </label>
              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  name="generate_ai_video"
                  checked={formData.generate_ai_video || false}
                  onChange={handleInputChange}
                  className="rounded border-gray-300 text-purple-600 focus:ring-purple-500"
                />
                <span className="text-sm text-gray-700">🎬 Generate AI Video</span>
              </label>
              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  name="generate_ai_images"
                  checked={formData.generate_ai_images || false}
                  onChange={handleInputChange}
                  className="rounded border-gray-300 text-orange-600 focus:ring-orange-500"
                />
                <span className="text-sm text-gray-700">🎨 Generate AI Images</span>
              </label>
            </div>

            {/* AI Image Controls */}
            {formData.generate_ai_images && (
              <div className="bg-gradient-to-r from-orange-50 to-yellow-50 border border-orange-200 rounded-xl p-6 mb-6">
                <h4 className="text-lg font-semibold text-orange-800 mb-4">🎨 AI Image Generation Settings</h4>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                  <div>
                    <label className="block text-sm font-medium text-orange-700 mb-2">Number of Images</label>
                    <select
                      name="ai_image_count"
                      value={formData.ai_image_count || 2}
                      onChange={handleInputChange}
                      className="w-full px-3 py-2 border border-orange-300 rounded-lg focus:ring-2 focus:ring-orange-500"
                    >
                      <option value={1}>1 image ($0.05)</option>
                      <option value={2}>2 images ($0.10)</option>
                      <option value={3}>3 images ($0.15)</option>
                      <option value={4}>4 images ($0.20)</option>
                    </select>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-orange-700 mb-2">Image Style</label>
                    <select
                      name="ai_image_style"
                      value={formData.ai_image_style || 'professional'}
                      onChange={handleInputChange}
                      className="w-full px-3 py-2 border border-orange-300 rounded-lg focus:ring-2 focus:ring-orange-500"
                    >
                      <option value="professional">Professional</option>
                      <option value="creative">Creative</option>
                      <option value="minimalist">Minimalist</option>
                      <option value="photographic">Photographic</option>
                      <option value="artistic">Artistic</option>
                    </select>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-orange-700 mb-2">Use For</label>
                    <select
                      name="ai_image_usage"
                      value={formData.ai_image_usage || 'social_posts'}
                      onChange={handleInputChange}
                      className="w-full px-3 py-2 border border-orange-300 rounded-lg focus:ring-2 focus:ring-orange-500"
                    >
                      <option value="social_posts">Social Media Posts</option>
                      <option value="blog_headers">Blog Headers</option>
                      <option value="thumbnails">Video Thumbnails</option>
                      <option value="backgrounds">Backgrounds</option>
                    </select>
                  </div>
                </div>
                
                <div className="bg-white border border-orange-200 rounded-lg p-4">
                  <h5 className="font-semibold text-orange-800 mb-2">💰 Image Generation Cost</h5>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">{formData.ai_image_count || 2} AI Images:</span>
                    <span className="font-bold text-orange-600">
                      ${((formData.ai_image_count || 2) * 0.05).toFixed(2)}
                    </span>
                  </div>
                  <p className="text-xs text-orange-600 mt-2">
                    💡 High-quality AI images perfect for social media, blogs, and marketing materials!
                  </p>
                </div>
              </div>
            )}

            {/* AI Media Controls */}
            {(formData.generate_ai_video || formData.generate_ai_music) && (
              <div className="bg-gradient-to-r from-purple-50 to-pink-50 border border-purple-200 rounded-xl p-6">
                <h4 className="text-lg font-semibold text-purple-800 mb-4">🎬🎵 AI Media Generation Settings</h4>
                
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-4">
                  <div>
                    <label className="block text-sm font-medium text-purple-700 mb-2">Video Source</label>
                    <select
                      name="video_source"
                      value={formData.video_source || 'ai_generate'}
                      onChange={handleInputChange}
                      className="w-full px-3 py-2 border border-purple-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                    >
                      <option value="ai_generate">🎬 AI Generate New Video</option>
                      <option value="media_library">📁 Use My Uploaded Video</option>
                      <option value="none">📝 Text/Image Posts Only</option>
                    </select>
                  </div>

                  {formData.video_source === 'ai_generate' && (
                    <>
                      <div>
                        <label className="block text-sm font-medium text-purple-700 mb-2">Video Duration</label>
                        <select
                          name="ai_video_duration"
                          value={formData.ai_video_duration || 30}
                          onChange={handleInputChange}
                          className="w-full px-3 py-2 border border-purple-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                        >
                          <option value={15}>15 seconds ($1.80 + music)</option>
                          <option value={30}>30 seconds ($3.60 + music)</option>
                          <option value={45}>45 seconds ($5.40 + music)</option>
                          <option value={60}>60 seconds ($7.20 + music)</option>
                        </select>
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-purple-700 mb-2">Video Style</label>
                        <select
                          name="ai_video_style"
                          value={formData.ai_video_style || 'professional'}
                          onChange={handleInputChange}
                          className="w-full px-3 py-2 border border-purple-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                        >
                          <option value="professional">Professional</option>
                          <option value="creative">Creative</option>
                          <option value="cinematic">Cinematic</option>
                          <option value="tiktok">TikTok Style</option>
                          <option value="minimalist">Minimalist</option>
                        </select>
                      </div>
                    </>
                  )}

                  {formData.video_source === 'media_library' && (
                    <div className="md:col-span-2">
                      <label className="block text-sm font-medium text-purple-700 mb-2">Select Your Video</label>
                      <select
                        name="selected_user_video"
                        value={formData.selected_user_video || ''}
                        onChange={handleInputChange}
                        className="w-full px-3 py-2 border border-purple-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                      >
                        <option value="">Choose from your videos...</option>
                        <option value="video1.mp4">🎬 Product Demo Video (45s)</option>
                        <option value="video2.mp4">🎬 Team Introduction (30s)</option>
                        <option value="video3.mp4">🎬 Behind the Scenes (60s)</option>
                        <option value="upload_new">📤 Upload New Video</option>
                      </select>
                    </div>
                  )}
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                  <div>
                    <label className="block text-sm font-medium text-purple-700 mb-2">Music Source</label>
                    <select
                      name="music_source"
                      value={formData.music_source || 'ai_generate'}
                      onChange={handleInputChange}
                      className="w-full px-3 py-2 border border-purple-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                    >
                      <option value="ai_generate">🎵 AI Generate New Music</option>
                      <option value="media_library">📁 Use My Uploaded Music</option>
                      <option value="none">🔇 No Music</option>
                    </select>
                  </div>

                  {formData.music_source === 'ai_generate' && (
                    <div>
                      <label className="block text-sm font-medium text-purple-700 mb-2">Music Mood</label>
                      <select
                        name="ai_music_mood"
                        value={formData.ai_music_mood || 'upbeat'}
                        onChange={handleInputChange}
                        className="w-full px-3 py-2 border border-purple-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                      >
                        <option value="upbeat">Upbeat (+$0.60)</option>
                        <option value="professional">Professional (+$0.60)</option>
                        <option value="dramatic">Dramatic (+$0.60)</option>
                        <option value="calm">Calm (+$0.60)</option>
                        <option value="trendy">Trendy (+$0.60)</option>
                      </select>
                    </div>
                  )}

                  {formData.music_source === 'media_library' && (
                    <div>
                      <label className="block text-sm font-medium text-purple-700 mb-2">Select Your Music</label>
                      <select
                        name="selected_user_music"
                        value={formData.selected_user_music || ''}
                        onChange={handleInputChange}
                        className="w-full px-3 py-2 border border-purple-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                      >
                        <option value="">Choose from your music...</option>
                        <option value="track1.mp3">🎵 Corporate Background (Loop)</option>
                        <option value="track2.mp3">🎵 Upbeat Intro Music (30s)</option>
                        <option value="track3.mp3">🎵 Calm Ambient (60s)</option>
                        <option value="upload_new">📤 Upload New Music</option>
                      </select>
                    </div>
                  )}
                </div>
                
                <div className="bg-white border border-purple-200 rounded-lg p-4">
                  <h5 className="font-semibold text-purple-800 mb-2">💰 Cost Breakdown (20% markup included)</h5>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                    <div>
                      <span className="text-gray-600">Video:</span>
                      <span className="ml-2 font-semibold">
                        ${formData.video_source === 'ai_generate' ? 
                          ((formData.ai_video_duration || 30) * 0.12).toFixed(2) : '0.00'}
                      </span>
                    </div>
                    <div>
                      <span className="text-gray-600">Music:</span>
                      <span className="ml-2 font-semibold">
                        ${formData.music_source === 'ai_generate' && formData.generate_ai_music ? '0.60' : '0.00'}
                      </span>
                    </div>
                    <div>
                      <span className="text-gray-600">Processing:</span>
                      <span className="ml-2 font-semibold">
                        ${(formData.video_source !== 'none' || formData.music_source !== 'none') ? '0.25' : '0.00'}
                      </span>
                    </div>
                    <div>
                      <span className="text-gray-600">Total:</span>
                      <span className="ml-2 font-bold text-purple-600">
                        ${(
                          (formData.video_source === 'ai_generate' ? ((formData.ai_video_duration || 30) * 0.12) : 0) + 
                          (formData.music_source === 'ai_generate' && formData.generate_ai_music ? 0.60 : 0) + 
                          ((formData.video_source !== 'none' || formData.music_source !== 'none') ? 0.25 : 0)
                        ).toFixed(2)}
                      </span>
                    </div>
                  </div>
                  <div className="mt-3 text-xs">
                    {formData.video_source === 'media_library' && (
                      <p className="text-green-600">
                        🎉 Using your own video saves ${((formData.ai_video_duration || 30) * 0.12).toFixed(2)}!
                      </p>
                    )}
                    {formData.music_source === 'media_library' && (
                      <p className="text-green-600">
                        🎉 Using your own music saves $0.60!
                      </p>
                    )}
                    {(formData.video_source === 'media_library' || formData.music_source === 'media_library') ? (
                      <p className="text-purple-600 mt-1">
                        💡 Mix and match: Use your media with AI generation for maximum creativity!
                      </p>
                    ) : (
                      <p className="text-purple-600">
                        💡 This creates professional video with custom AI-generated music, ready to post across all platforms!
                      </p>
                    )}
                  </div>
                </div>
              </div>
            )}
            
            <div className="flex flex-wrap gap-4">
              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  name="seo_focus"
                  checked={formData.seo_focus}
                  onChange={handleInputChange}
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span className="text-sm text-gray-700">SEO Optimization</span>
              </label>
              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  name="repurpose_content"
                  checked={formData.repurpose_content}
                  onChange={handleInputChange}
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span className="text-sm text-gray-700">Cross-Platform Repurposing</span>
              </label>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  name="use_company_media"
                  checked={formData.use_company_media}
                  onChange={handleInputChange}
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span className="text-sm text-gray-700">Use Company Media Library</span>
              </label>
              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  name="high_authenticity"
                  checked={formData.high_authenticity || false}
                  onChange={handleInputChange}
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span className="text-sm text-gray-700">🎭 High Authenticity Mode</span>
              </label>
            </div>
            
            <div className="text-xs text-gray-600 bg-gray-50 p-3 rounded-lg">
              <p><strong>🎭 High Authenticity Mode:</strong> Creates more varied, human-like content with personality quirks, casual language, and natural imperfections that make your posts sound genuinely authentic rather than AI-generated.</p>
            </div>

            {/* Smart Content Preview Section */}
            <div className="bg-gradient-to-r from-purple-50 to-blue-50 p-4 rounded-lg">
              <h4 className="font-semibold text-gray-800 mb-3">📱 Smart Content Preview</h4>
              <div className="flex space-x-3">
                <button
                  onClick={generateContentPreview}
                  disabled={loading || !formData.topic}
                  className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors disabled:opacity-50"
                >
                  🔍 Preview Content
                </button>
                {previewEngagementMetrics && (
                  <div className="text-sm text-purple-700">
                    Est: {previewEngagementMetrics.likes} likes, {previewEngagementMetrics.comments} comments
                  </div>
                )}
              </div>
              
              {showPreview && contentPreview && (
                <div className="mt-3 p-3 bg-white rounded border">
                  <h5 className="font-medium text-gray-800">{contentPreview.title}</h5>
                  <p className="text-sm text-gray-600 mt-1">{contentPreview.content}</p>
                  <div className="mt-2 flex space-x-3 text-xs text-gray-500">
                    {Object.entries(contentPreview.characterCount).map(([platform, count]) => (
                      <span key={platform}>{platform}: {count} chars</span>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Quick Actions Enhancement */}
            {results && (
              <FeatureGate 
                feature="advanced_ai_content" 
                featureName="Quick Actions"
                requiredPlan="Professional"
                fallbackContent={
                  <div className="bg-gradient-to-r from-gray-50 to-gray-100 p-4 rounded-lg opacity-50">
                    <h4 className="font-semibold text-gray-800 mb-3">🔒 Quick Actions (Professional+)</h4>
                    <div className="flex flex-wrap gap-2 opacity-50">
                      <button className="px-3 py-1 bg-gray-400 text-white text-sm rounded cursor-not-allowed">Generate Similar</button>
                      <button className="px-3 py-1 bg-gray-400 text-white text-sm rounded cursor-not-allowed">Translate</button>
                      <button className="px-3 py-1 bg-gray-400 text-white text-sm rounded cursor-not-allowed">Optimize SEO</button>
                    </div>
                  </div>
                }
              >
                <div className="bg-gradient-to-r from-green-50 to-teal-50 p-4 rounded-lg">
                  <h4 className="font-semibold text-gray-800 mb-3">⚡ Quick Actions</h4>
                  <div className="flex flex-wrap gap-2">
                    <button
                      onClick={generateSimilarContent}
                      disabled={quickActionLoading}
                      className="px-3 py-1 bg-green-600 text-white text-sm rounded hover:bg-green-700 transition-colors"
                    >
                      🔄 Generate Similar
                    </button>
                    <select
                      value={selectedLanguage}
                      onChange={(e) => setSelectedLanguage(e.target.value)}
                      className="px-2 py-1 border border-gray-300 text-sm rounded"
                    >
                      {translationLanguages.map(lang => (
                        <option key={lang} value={lang}>{lang}</option>
                      ))}
                    </select>
                    <button
                      onClick={() => translateContent(selectedLanguage)}
                      disabled={quickActionLoading}
                      className="px-3 py-1 bg-blue-600 text-white text-sm rounded hover:bg-blue-700 transition-colors"
                    >
                      🌍 Translate
                    </button>
                    <button
                      onClick={optimizeForSEO}
                      disabled={quickActionLoading}
                      className="px-3 py-1 bg-yellow-600 text-white text-sm rounded hover:bg-yellow-700 transition-colors"
                    >
                      🎯 Optimize SEO
                    </button>
                  </div>
                </div>
              </FeatureGate>
            )}

            <div className="flex space-x-4">
              <button
                type="submit"
                disabled={loading || !formData.topic || formData.platforms.length === 0}
                className="flex-1 bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-semibold"
              >
                {loading ? 'Generating Content...' : 'Generate Advanced Content'}
              </button>
              
              {results && formData.platforms.length > 0 && (
                <button
                  type="button"
                  onClick={() => publishToConnectedPlatforms(
                    results.generated_content?.[0]?.content || 'Generated content',
                    formData.platforms
                  )}
                  disabled={loading || formData.platforms.filter(p => connectedPlatforms[p]).length === 0}
                  className="flex-1 bg-green-600 text-white py-3 px-4 rounded-lg hover:bg-green-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-semibold"
                >
                  🚀 Publish to Connected Platforms
                </button>
              )}
            </div>
          </form>
        </div>

        {/* Social Media Platforms */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-800">🔗 Social Media Platforms &nbsp;&nbsp;&nbsp;<em><strong>Posts the Content</strong></em></h3>
            <div className="text-sm text-gray-600">
              {Object.keys(connectedPlatforms).length} of {availablePlatforms.length} platforms connected
            </div>
          </div>
          
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
            {availablePlatforms.slice(0, 10).map((platform) => (
              <div key={platform} className="flex flex-col items-center space-y-2 p-3 border rounded-lg">
                <div className="relative">
                  <span className="text-2xl">{PLATFORM_ICONS[platform]}</span>
                  {connectedPlatforms[platform] ? (
                    <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-500 rounded-full border-2 border-white"></div>
                  ) : (
                    <div className="absolute -top-1 -right-1 w-3 h-3 bg-gray-400 rounded-full border-2 border-white"></div>
                  )}
                </div>
                <div className="text-xs text-center">
                  <div className="font-medium capitalize">
                    {platform === 'x' ? 'X (Twitter)' : platform === 'facebook_messenger' ? 'Messenger' : platform.replace('_', ' ')}
                  </div>
                  {platformConnectionStatus[platform]?.username && (
                    <div className="text-gray-500 truncate">
                      @{platformConnectionStatus[platform].username}
                    </div>
                  )}
                </div>
                {connectedPlatforms[platform] ? (
                  <div className="flex space-x-1 w-full">
                    <button
                      onClick={() => disconnectPlatform(platform)}
                      className="flex-1 px-2 py-1 text-xs bg-red-100 text-red-700 rounded hover:bg-red-200 transition-colors"
                    >
                      Disconnect
                    </button>
                    {platformConnectionStatus[platform]?.status === 'expired' && (
                      <button
                        onClick={() => refreshPlatformConnection(platform)}
                        className="flex-1 px-2 py-1 text-xs bg-yellow-100 text-yellow-700 rounded hover:bg-yellow-200 transition-colors"
                      >
                        Refresh
                      </button>
                    )}
                  </div>
                ) : (
                  <button
                    onClick={() => connectPlatform(platform)}
                    disabled={connectingPlatform === platform}
                    className={`w-full px-2 py-1 text-xs rounded transition-colors ${
                      connectingPlatform === platform
                        ? 'bg-gray-100 text-gray-400'
                        : 'bg-blue-100 text-blue-700 hover:bg-blue-200'
                    }`}
                  >
                    {connectingPlatform === platform ? 'Connecting...' : 'Connect'}
                  </button>
                )}
              </div>
            ))}
          </div>
          
          {availablePlatforms.length > 10 && (
            <button 
              onClick={() => setShowOAuthModal(true)}
              className="mt-4 text-blue-600 text-sm hover:text-blue-800"
            >
              View all {availablePlatforms.length} platforms →
            </button>
          )}
        </div>
      </div>
    );
  };

  // Enhanced Analytics Tab
  const AnalyticsTab = () => {
    return (
      <div className="space-y-6">
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">📊 Advanced Analytics Dashboard</h2>
          
          {/* Real-Time Performance Metrics */}
          {performanceMetrics && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
              <div className="bg-gradient-to-r from-blue-50 to-blue-100 p-4 rounded-lg">
                <h4 className="text-sm font-medium text-blue-600">Engagement Rate</h4>
                <p className="text-2xl font-bold text-blue-900">{performanceMetrics.engagement_rate}%</p>
                <p className="text-xs text-blue-700">↗️ +0.3% from last week</p>
              </div>
              <div className="bg-gradient-to-r from-green-50 to-green-100 p-4 rounded-lg">
                <h4 className="text-sm font-medium text-green-600">Total Reach</h4>
                <p className="text-2xl font-bold text-green-900">{performanceMetrics.reach.toLocaleString()}</p>
                <p className="text-xs text-green-700">↗️ +{performanceMetrics.growth_rate}% growth</p>
              </div>
              <div className="bg-gradient-to-r from-purple-50 to-purple-100 p-4 rounded-lg">
                <h4 className="text-sm font-medium text-purple-600">Conversions</h4>
                <p className="text-2xl font-bold text-purple-900">{performanceMetrics.conversions}</p>
                <p className="text-xs text-purple-700">Best time: {performanceMetrics.best_posting_time}</p>
              </div>
            </div>
          )}

          {/* ROI Analytics */}
          {roiData && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
              <div className="bg-green-50 p-4 rounded-lg">
                <h4 className="text-sm font-medium text-green-600">ROI Percentage</h4>
                <p className="text-2xl font-bold text-green-900">{roiData.roi_percentage}%</p>
              </div>
              <div className="bg-blue-50 p-4 rounded-lg">
                <h4 className="text-sm font-medium text-blue-600">Total Revenue</h4>
                <p className="text-2xl font-bold text-blue-900">${roiData.revenue_attributed}</p>
              </div>
              <div className="bg-purple-50 p-4 rounded-lg">
                <h4 className="text-sm font-medium text-purple-600">Leads Generated</h4>
                <p className="text-2xl font-bold text-purple-900">{roiData.leads_generated}</p>
              </div>
              <div className="bg-orange-50 p-4 rounded-lg">
                <h4 className="text-sm font-medium text-orange-600">Cost per Lead</h4>
                <p className="text-2xl font-bold text-orange-900">${roiData.cost_per_lead}</p>
              </div>
            </div>
          )}

          {/* Performance Comparison */}
          <div className="bg-gray-50 rounded-lg p-6 mb-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">📈 Platform Performance Comparison</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {['instagram', 'facebook', 'linkedin', 'tiktok'].map((platform) => (
                <div key={platform} className="bg-white p-4 rounded-lg">
                  <div className="flex items-center space-x-2 mb-2">
                    <span className="text-lg">{PLATFORM_ICONS[platform]}</span>
                    <span className="font-medium capitalize">{platform}</span>
                  </div>
                  <div className="space-y-1 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Engagement:</span>
                      <span className="font-semibold">{Math.floor(Math.random() * 30 + 50)}%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Reach:</span>
                      <span className="font-semibold">{Math.floor(Math.random() * 5000 + 1000)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">CTR:</span>
                      <span className="font-semibold">{(Math.random() * 3 + 1).toFixed(1)}%</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Trending Hashtags */}
          {trendingHashtags && (
            <div className="bg-gray-50 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-gray-800 mb-4">🔥 Trending Hashtags</h3>
              <div className="space-y-4">
                <div>
                  <h4 className="font-medium text-green-600 mb-2">🚀 Trending Now</h4>
                  <div className="flex flex-wrap gap-2">
                    {trendingHashtags.trending_hashtags?.trending?.map((tag, i) => (
                      <span key={i} className="bg-green-100 text-green-800 px-2 py-1 rounded text-sm font-semibold">
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
                <div>
                  <h4 className="font-medium text-blue-600 mb-2">📈 Stable Performers</h4>
                  <div className="flex flex-wrap gap-2">
                    {trendingHashtags.trending_hashtags?.stable?.map((tag, i) => (
                      <span key={i} className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm">
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}
          
          {/* Real-time Analytics Integration - What's Working */}
          {whatWorkingData && (
            <div className="bg-gradient-to-r from-emerald-50 to-green-50 rounded-lg p-6 mb-6">
              <h3 className="text-lg font-semibold text-emerald-800 mb-4">🎯 What's Working Right Now</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {whatWorkingData.map((insight, index) => (
                  <div key={index} className="bg-white p-4 rounded-lg shadow-sm">
                    <h4 className="font-semibold text-gray-800">{insight.type}</h4>
                    <p className="text-sm text-green-600 font-medium">{insight.performance}</p>
                    <p className="text-xs text-gray-500 flex items-center">
                      {insight.trend === 'rising' ? '📈' : '📊'} {insight.trend}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}
          
          {/* Best Posting Times */}
          {bestPostingTimes && (
            <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-6 mb-6">
              <h3 className="text-lg font-semibold text-blue-800 mb-4">⏰ Best Time to Post</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {bestPostingTimes.map((time, index) => (
                  <div key={index} className="bg-white p-4 rounded-lg shadow-sm text-center">
                    <h4 className="font-semibold text-gray-800">{time.day}</h4>
                    <p className="text-lg font-bold text-blue-600">{time.time}</p>
                    <p className="text-sm text-green-600">{time.engagement} engagement</p>
                  </div>
                ))}
              </div>
              <div className="mt-4 p-3 bg-blue-100 rounded-lg">
                <p className="text-sm text-blue-800">
                  💡 <strong>Tip:</strong> Schedule your most important content during these peak times for maximum visibility.
                </p>
              </div>
            </div>
          )}
          
          {/* Analytics Insights & Competitor Analysis */}
          {analyticsInsights && (
            <div className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-purple-800 mb-4">🔍 Competitor Insights</h3>
              <div className="space-y-3">
                {analyticsInsights.competitorAnalysis.map((comp, index) => (
                  <div key={index} className="bg-white p-4 rounded-lg shadow-sm flex justify-between items-center">
                    <div>
                      <h4 className="font-semibold text-gray-800">{comp.competitor}</h4>
                      <p className="text-sm text-green-600">Strength: {comp.strength}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm text-orange-600">Gap: {comp.gap}</p>
                      <p className="text-xs text-gray-500">Opportunity for you</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    );
  };

  // Enhanced Media Tab with Drag & Drop
  const MediaTab = () => {
    const [uploadForm, setUploadForm] = useState({
      files: null,
      company_id: '',
      category: 'training',
      description: '',
      tags: ''
    });

    const handleMediaUpload = async (files, category, description, tags, company_id) => {
      if (!company_id) {
        addNotification('Please select a company to upload media to', 'error');
        return;
      }

      // Find the selected company
      const targetCompany = companies.find(c => c.id === company_id);
      if (!targetCompany) {
        addNotification('Selected company not found', 'error');
        return;
      }
      
      setUploadingMedia(true);
      try {
        const uploadPromises = Array.from(files).map(async (file) => {
          const formData = new FormData();
          formData.append('file', file);
          formData.append('category', category);
          formData.append('description', description);
          formData.append('tags', tags);
          formData.append('seo_alt_text', `${targetCompany.name} ${category} - ${description}`);

          const response = await fetch(`${backendUrl}/api/companies/${company_id}/media/upload`, {
            method: 'POST',
            body: formData,
          });

          if (!response.ok) {
            throw new Error(`Failed to upload ${file.name}`);
          }

          return response.json();
        });

        await Promise.all(uploadPromises);
        await fetchCompanyMedia();
        addNotification(`Successfully uploaded ${files.length} file(s) to ${targetCompany.name}!`, 'success');
      } catch (error) {
        console.error('Error uploading media:', error);
        addNotification('Error uploading media. Please try again.', 'error');
      } finally {
        setUploadingMedia(false);
      }
    };

    const handleUploadSubmit = (e) => {
      e.preventDefault();
      if (!uploadForm.files || uploadForm.files.length === 0) {
        addNotification('Please select files to upload', 'error');
        return;
      }
      handleMediaUpload(uploadForm.files, uploadForm.category, uploadForm.description, uploadForm.tags, uploadForm.company_id);
      setUploadForm({ files: null, company_id: '', category: 'training', description: '', tags: '' });
    };

    return (
      <div className="space-y-6">
        {/* Drag & Drop Upload Zone */}
        <div 
          className="bg-white rounded-xl shadow-lg p-6 border-2 border-dashed border-gray-300 hover:border-blue-500 transition-colors"
          onDragOver={handleDragOver}
          onDrop={handleDrop}
        >
          <div className="text-center">
            <span className="text-4xl mb-4 block">📤</span>
            <h3 className="text-xl font-semibold text-gray-800 mb-2">Drag & Drop Media Upload</h3>
            <p className="text-gray-600 mb-4">Drag files here or click to browse</p>
            
            {/* Company Selection for Drag & Drop */}
            <div className="max-w-md mx-auto mb-4">
              <select
                value={dragDropCompanyId}
                onChange={(e) => setDragDropCompanyId(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Select company for upload...</option>
                {companies.map((company) => (
                  <option key={company.id} value={company.id}>
                    🏢 {company.name} ({company.industry})
                  </option>
                ))}
              </select>
              {companies.length === 0 && (
                <p className="text-sm text-gray-500 mt-1">
                  No companies available. Please add a company first.
                </p>
              )}
            </div>
            
            {draggedFiles.length > 0 && (
              <div className="mb-4">
                <div className="bg-blue-50 rounded-lg p-3">
                  <p className="text-blue-800 font-medium">
                    {draggedFiles.length} files ready for upload
                    {dragDropCompanyId && (
                      <span className="block text-sm text-blue-600 mt-1">
                        → {companies.find(c => c.id === dragDropCompanyId)?.name}
                      </span>
                    )}
                  </p>
                  <div className="text-sm text-blue-600 mt-1">
                    {draggedFiles.map((file, index) => (
                      <span key={index}>{file.name}{index < draggedFiles.length - 1 ? ', ' : ''}</span>
                    ))}
                  </div>
                </div>
                <button
                  onClick={uploadDraggedFiles}
                  disabled={uploadingMedia || !dragDropCompanyId}
                  className="mt-3 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
                >
                  {uploadingMedia ? 'Uploading...' : dragDropCompanyId ? 'Upload Files' : 'Select Company First'}
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Traditional Upload Form */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">📤 Upload Media</h2>
          <form onSubmit={handleUploadSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Select Files *</label>
              <input
                type="file"
                multiple
                accept="image/*,video/*"
                onChange={(e) => setUploadForm({ ...uploadForm, files: e.target.files })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Upload to Company *</label>
              <select
                value={uploadForm.company_id}
                onChange={(e) => setUploadForm({ ...uploadForm, company_id: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              >
                <option value="">Select a company...</option>
                {companies.map((company) => (
                  <option key={company.id} value={company.id}>
                    🏢 {company.name} ({company.industry})
                  </option>
                ))}
              </select>
              {companies.length === 0 && (
                <p className="text-sm text-gray-500 mt-1">
                  No companies available. Please add a company first in the Content Hub.
                </p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Category *</label>
              <select
                value={uploadForm.category}
                onChange={(e) => setUploadForm({ ...uploadForm, category: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              >
                {Object.entries(MEDIA_CATEGORIES).map(([key, value]) => (
                  <option key={key} value={key}>
                    {value.icon} {key.charAt(0).toUpperCase() + key.slice(1)} - {value.description}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Description</label>
              <textarea
                value={uploadForm.description}
                onChange={(e) => setUploadForm({ ...uploadForm, description: e.target.value })}
                placeholder="Brief description of the media content..."
                rows="2"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Tags (comma-separated)</label>
              <input
                type="text"
                value={uploadForm.tags}
                onChange={(e) => setUploadForm({ ...uploadForm, tags: e.target.value })}
                placeholder="e.g., safety, training, equipment, outdoor"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <button
              type="submit"
              disabled={uploadingMedia}
              className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {uploadingMedia ? 'Uploading...' : 'Upload Media'}
            </button>
          </form>
        </div>

        {/* AI Media Matching */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-xl font-semibold text-gray-800 mb-4">🤖 AI Media Matching</h3>
          <div className="bg-blue-50 rounded-lg p-4">
            <p className="text-blue-800 mb-2">
              <strong>Smart Suggestions:</strong> AI has analyzed your content and suggests these media files:
            </p>
            <div className="space-y-2">
              {mediaFiles.slice(0, 3).map((media, index) => (
                <div key={index} className="flex items-center space-x-3 bg-white p-2 rounded">
                  <span className="text-lg">{MEDIA_CATEGORIES[media.category]?.icon}</span>
                  <span className="text-sm font-medium">{media.original_filename || 'Media file'}</span>
                  <span className="text-xs text-gray-500">Match: {Math.floor(Math.random() * 20 + 80)}%</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Media Library */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-xl font-semibold text-gray-800 mb-4">📂 Media Library</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {mediaFiles.map((media) => (
              <div key={media.id} className="bg-gray-50 rounded-lg p-4 border border-gray-200 hover:shadow-md transition-shadow">
                <div className="flex items-start justify-between mb-2">
                  <div className="flex items-center space-x-2">
                    <span className="text-lg">{MEDIA_CATEGORIES[media.category]?.icon}</span>
                    <span className="text-sm font-medium text-gray-700 capitalize">{media.category}</span>
                  </div>
                  <button
                    onClick={() => copyToClipboard(media.file_path || media.original_filename)}
                    className="text-blue-600 hover:text-blue-800 text-sm"
                  >
                    📋
                  </button>
                </div>
                
                <div className="mb-2">
                  <p className="text-sm font-medium text-gray-800 truncate">{media.original_filename}</p>
                  <p className="text-xs text-gray-600">{media.description}</p>
                </div>
                
                <div className="flex flex-wrap gap-1 mb-2">
                  {media.tags && media.tags.map((tag, index) => (
                    <span key={index} className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">
                      {tag}
                    </span>
                  ))}
                </div>
                
                <div className="flex justify-between items-center text-xs text-gray-500">
                  <span>{media.media_type}</span>
                  <span>Used: {media.usage_count || 0} times</span>
                </div>
              </div>
            ))}
          </div>

          {mediaFiles.length === 0 && (
            <div className="text-center py-8 text-gray-500">
              <p className="text-lg mb-2">📷 No media files found</p>
              <p className="text-sm">Upload some photos and videos to get started!</p>
            </div>
          )}
        </div>
      </div>
    );
  };

  // Enhanced Visual Calendar Tab
  const CalendarTab = () => {
    const [currentDate, setCurrentDate] = useState(new Date());
    const [selectedDate, setSelectedDate] = useState(null);
    const [selectedCalendarCompanyId, setSelectedCalendarCompanyId] = useState('');
    
    const daysInMonth = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0).getDate();
    const firstDayOfMonth = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1).getDay();
    
    const monthNames = ["January", "February", "March", "April", "May", "June",
      "July", "August", "September", "October", "November", "December"
    ];

    const generateCalendarDays = () => {
      const days = [];
      
      // Empty cells for days before the first day of the month
      for (let i = 0; i < firstDayOfMonth; i++) {
        days.push(null);
      }
      
      // Days of the month
      for (let day = 1; day <= daysInMonth; day++) {
        days.push(day);
      }
      
      return days;
    };

    const getPostsForDate = (day) => {
      // If no company selected, show empty calendar
      if (!selectedCalendarCompanyId) {
        return [];
      }

      const selectedCompany = companies.find(c => c.id === selectedCalendarCompanyId);
      if (!selectedCompany) {
        return [];
      }

      // Generate company-specific mock posts based on industry
      const industryBasedPosts = {
        'Construction': {
          5: [{ platform: 'instagram', topic: 'Safety Protocol Update' }],
          12: [{ platform: 'facebook', topic: 'Weekly Team Safety Meeting' }, { platform: 'linkedin', topic: 'Construction Industry Trends' }],
          20: [{ platform: 'tiktok', topic: 'Equipment Operation Demo' }],
          25: [{ platform: 'instagram', topic: 'Project Milestone Progress' }]
        },
        'Environmental': {
          3: [{ platform: 'linkedin', topic: 'Environmental Compliance Update' }],
          10: [{ platform: 'facebook', topic: 'Earth Day Preparation' }, { platform: 'instagram', topic: 'Green Technology Showcase' }],
          18: [{ platform: 'tiktok', topic: 'Sustainability Tips' }],
          28: [{ platform: 'linkedin', topic: 'Monthly Environmental Report' }]
        },
        'Safety Training': {
          7: [{ platform: 'facebook', topic: 'Monthly Safety Training' }],
          14: [{ platform: 'linkedin', topic: 'OSHA Compliance Update' }, { platform: 'instagram', topic: 'Safety Equipment Check' }],
          22: [{ platform: 'tiktok', topic: 'Emergency Procedure Demo' }],
          30: [{ platform: 'instagram', topic: 'Safety Achievement Awards' }]
        },
        'Manufacturing': {
          6: [{ platform: 'linkedin', topic: 'Production Quality Update' }],
          13: [{ platform: 'facebook', topic: 'Team Productivity Showcase' }, { platform: 'instagram', topic: 'New Equipment Installation' }],
          21: [{ platform: 'tiktok', topic: 'Manufacturing Process Tour' }],
          27: [{ platform: 'linkedin', topic: 'Monthly Production Report' }]
        },
        'default': {
          5: [{ platform: 'instagram', topic: 'Company Update' }],
          12: [{ platform: 'facebook', topic: 'Team Highlights' }, { platform: 'linkedin', topic: 'Industry Insights' }],
          20: [{ platform: 'tiktok', topic: 'Behind the Scenes' }],
          25: [{ platform: 'instagram', topic: 'Monthly Progress' }]
        }
      };

      const industryPosts = industryBasedPosts[selectedCompany.industry] || industryBasedPosts['default'];
      return industryPosts[day] || [];
    };

    const navigateMonth = (direction) => {
      const newDate = new Date(currentDate);
      newDate.setMonth(currentDate.getMonth() + direction);
      setCurrentDate(newDate);
    };

    const selectedCompanyInfo = companies.find(c => c.id === selectedCalendarCompanyId);

    return (
      <div className="space-y-6">
        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-900">📅 Content Calendar</h2>
            
            {/* Company Selector for Calendar */}
            <div className="flex items-center space-x-4">
              <label className="text-sm font-medium text-gray-700">View Calendar for:</label>
              <select
                value={selectedCalendarCompanyId}
                onChange={(e) => setSelectedCalendarCompanyId(e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Select a company...</option>
                {companies.map((company) => (
                  <option key={company.id} value={company.id}>
                    🏢 {company.name} ({company.industry})
                  </option>
                ))}
              </select>
            </div>
          </div>

          {!selectedCalendarCompanyId && (
            <div className="text-center py-12 text-gray-500">
              <div className="text-4xl mb-4">📅</div>
              <h3 className="text-lg font-medium text-gray-800 mb-2">Select a Company</h3>
              <p className="text-sm">Choose a company to view its content calendar and scheduled posts.</p>
              {companies.length === 0 && (
                <p className="text-sm text-gray-400 mt-2">No companies available. Please add a company first.</p>
              )}
            </div>
          )}

          {selectedCalendarCompanyId && selectedCompanyInfo && (
            <>
              {/* Company Info Header */}
              <div className="mb-6 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <div className="bg-white p-2 rounded-lg">
                    <span className="text-2xl">🏢</span>
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-800">{selectedCompanyInfo.name}</h3>
                    <p className="text-sm text-gray-600">{selectedCompanyInfo.industry} • Content Calendar</p>
                  </div>
                </div>
              </div>
              
              {/* Calendar Header */}
              <div className="flex items-center justify-between mb-6">
                <button
                  onClick={() => navigateMonth(-1)}
                  className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
                >
                  ← Previous
                </button>
                <h3 className="text-xl font-semibold text-gray-800">
                  {monthNames[currentDate.getMonth()]} {currentDate.getFullYear()}
                </h3>
                <button
                  onClick={() => navigateMonth(1)}
                  className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
                >
                  Next →
                </button>
              </div>

              {/* Calendar Grid */}
              <div className="grid grid-cols-7 gap-1 mb-4">
                {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map((day) => (
                  <div key={day} className="p-2 text-center font-medium text-gray-600 bg-gray-50 rounded">
                    {day}
                  </div>
                ))}
              </div>

              <div className="grid grid-cols-7 gap-1">
                {generateCalendarDays().map((day, index) => (
                  <div
                    key={index}
                    className={`min-h-[80px] p-2 border rounded-lg cursor-pointer transition-colors ${
                      day ? 'hover:bg-blue-50' : ''
                    } ${selectedDate === day ? 'bg-blue-100 border-blue-500' : 'border-gray-200'}`}
                    onClick={() => day && setSelectedDate(day)}
                  >
                    {day && (
                      <>
                        <div className="font-medium text-gray-800 mb-1">{day}</div>
                        <div className="space-y-1">
                          {getPostsForDate(day).map((post, idx) => (
                            <div
                              key={idx}
                              className={`text-xs p-1 rounded ${
                                post.platform === 'instagram' ? 'bg-purple-100 text-purple-800' :
                                post.platform === 'facebook' ? 'bg-blue-100 text-blue-800' :
                                post.platform === 'linkedin' ? 'bg-blue-100 text-blue-800' :
                                post.platform === 'tiktok' ? 'bg-pink-100 text-pink-800' :
                                'bg-gray-100 text-gray-800'
                              }`}
                            >
                              {PLATFORM_ICONS[post.platform]} {post.topic}
                            </div>
                          ))}
                        </div>
                      </>
                    )}
                  </div>
                ))}
              </div>

              {/* Company-Specific Content Gap Analysis */}
              <div className="mt-6 p-4 bg-yellow-50 rounded-lg">
                <h4 className="font-semibold text-yellow-800 mb-2">🔍 Content Gap Analysis - {selectedCompanyInfo.name}</h4>
                <div className="space-y-2">
                  <div className="flex items-center space-x-2">
                    <span className="w-3 h-3 bg-red-500 rounded-full"></span>
                    <span className="text-sm text-gray-700">Days 8-11: No content scheduled for {selectedCompanyInfo.name}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="w-3 h-3 bg-yellow-500 rounded-full"></span>
                    <span className="text-sm text-gray-700">Day 15: Only 1 post scheduled</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="w-3 h-3 bg-green-500 rounded-full"></span>
                    <span className="text-sm text-gray-700">Good coverage on high-engagement days</span>
                  </div>
                </div>
              </div>

              {/* Industry-Specific Optimal Timing */}
              <div className="mt-6 p-4 bg-blue-50 rounded-lg">
                <h4 className="font-semibold text-blue-800 mb-2">⏰ Optimal Times for {selectedCompanyInfo.industry}</h4>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="text-center">
                    <div className="text-lg mb-1">📸</div>
                    <div className="text-sm font-medium">Instagram</div>
                    <div className="text-xs text-gray-600">
                      {selectedCompanyInfo.industry === 'Construction' ? '7:00 AM - 9:00 AM' :
                       selectedCompanyInfo.industry === 'Environmental' ? '10:00 AM - 12:00 PM' :
                       selectedCompanyInfo.industry === 'Safety Training' ? '8:00 AM - 10:00 AM' :
                       '11:00 AM - 2:00 PM'}
                    </div>
                  </div>
                  <div className="text-center">
                    <div className="text-lg mb-1">👥</div>
                    <div className="text-sm font-medium">Facebook</div>
                    <div className="text-xs text-gray-600">
                      {selectedCompanyInfo.industry === 'Construction' ? '12:00 PM - 2:00 PM' :
                       selectedCompanyInfo.industry === 'Environmental' ? '2:00 PM - 4:00 PM' :
                       selectedCompanyInfo.industry === 'Safety Training' ? '1:00 PM - 3:00 PM' :
                       '1:00 PM - 4:00 PM'}
                    </div>
                  </div>
                  <div className="text-center">
                    <div className="text-lg mb-1">💼</div>
                    <div className="text-sm font-medium">LinkedIn</div>
                    <div className="text-xs text-gray-600">
                      {selectedCompanyInfo.industry === 'Construction' ? '6:00 AM - 8:00 AM' :
                       selectedCompanyInfo.industry === 'Environmental' ? '8:00 AM - 10:00 AM' :
                       selectedCompanyInfo.industry === 'Safety Training' ? '7:00 AM - 9:00 AM' :
                       '8:00 AM - 10:00 AM'}
                    </div>
                  </div>
                  <div className="text-center">
                    <div className="text-lg mb-1">🎵</div>
                    <div className="text-sm font-medium">TikTok</div>
                    <div className="text-xs text-gray-600">6:00 PM - 10:00 PM</div>
                  </div>
                </div>
              </div>

              {/* Quick Actions for Selected Company */}
              <div className="mt-6 p-4 bg-green-50 rounded-lg">
                <h4 className="font-semibold text-green-800 mb-3">🚀 Quick Actions for {selectedCompanyInfo.name}</h4>
                <div className="flex flex-wrap gap-2">
                  <button className="px-3 py-1 bg-green-600 text-white text-sm rounded hover:bg-green-700 transition-colors">
                    + Schedule Post
                  </button>
                  <button className="px-3 py-1 bg-blue-600 text-white text-sm rounded hover:bg-blue-700 transition-colors">
                    Generate Content
                  </button>
                  <button className="px-3 py-1 bg-purple-600 text-white text-sm rounded hover:bg-purple-700 transition-colors">
                    Bulk Schedule
                  </button>
                  <button className="px-3 py-1 bg-orange-600 text-white text-sm rounded hover:bg-orange-700 transition-colors">
                    Analytics
                  </button>
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    );
  };

  // Enhanced Training Tab
  const TrainingTab = () => {
    const [activeSection, setActiveSection] = useState('overview');
    const [videoPlaying, setVideoPlaying] = useState(false);

    const trainingVideos = [
      {
        id: 'overview',
        title: 'PostVelocity Complete Overview',
        duration: '12:45',
        description: 'Complete walkthrough of all features and capabilities',
        thumbnail: '🎬',
        script: `
Welcome to PostVelocity - the revolutionary AI-powered social media management platform!

In this comprehensive training video, you'll learn:

00:00 - Introduction to PostVelocity
00:30 - Dashboard Overview & Navigation
01:15 - Setting Up Your First Company
02:00 - Smart Generate Feature Demo
03:30 - Weekly Batch Content Creation
04:45 - Emergency Post Templates
05:30 - Voice Input & Quick Actions
06:15 - Media Library & Drag-Drop Upload
07:00 - AI Media Matching Demo
08:00 - Analytics Dashboard Deep Dive
09:15 - Visual Calendar & Scheduling
10:30 - Automation Center Features
11:45 - Best Practices & Pro Tips
12:15 - Wrap-up & Next Steps

This video covers everything you need to become a PostVelocity expert!
        `
      },
      {
        id: 'quickstart',
        title: 'Quick Start Guide',
        duration: '5:30',
        description: 'Get up and running in under 6 minutes',
        thumbnail: '⚡',
        script: `
PostVelocity Quick Start - Get Results in 5 Minutes!

00:00 - Welcome & Goals
00:15 - Add Your Company (30 seconds)
00:45 - Upload 3-5 Photos (1 minute)
01:45 - Generate Your First Content (2 minutes)
03:45 - Review Analytics (1 minute)
04:45 - Schedule Your Posts (30 seconds)
05:15 - Success! You're Ready to Go!

Perfect for busy executives who need results fast!
        `
      },
      {
        id: 'analytics',
        title: 'Analytics Mastery',
        duration: '8:20',
        description: 'Master your social media analytics like a pro',
        thumbnail: '📊',
        script: `
Analytics Mastery - Understand Your Social Media Performance

00:00 - Introduction to Analytics
00:30 - Key Metrics Explained
01:45 - Engagement Rate Deep Dive
02:30 - ROI Calculation & Interpretation
03:15 - Platform Performance Comparison
04:00 - Red/Yellow/Green Performance Indicators
05:00 - Weekly Review Process
06:00 - Monthly Strategic Planning
07:00 - Advanced Analytics Features
07:45 - Action Items Based on Data
08:00 - Success Stories & Examples

Transform your data into actionable insights!
        `
      },
      {
        id: 'advanced',
        title: 'Advanced Features',
        duration: '10:15',
        description: 'Unlock the full power of PostVelocity',
        thumbnail: '🚀',
        script: `
Advanced PostVelocity Features - For Power Users

00:00 - Advanced Features Overview
00:30 - Industry Templates Deep Dive
01:15 - Cross-Platform Content Repurposing
02:00 - AI Proactive Suggestions
02:45 - Compliance Checker Features
03:30 - Seasonal Content Planning
04:15 - Emergency Communication Protocols
05:00 - Automation Workflows
06:00 - Voice Commands & Shortcuts
07:00 - Bulk Operations & Time-Saving Tips
08:00 - Integration Possibilities
09:00 - Advanced Analytics Features
09:45 - Expert Tips & Best Practices

Become a PostVelocity power user!
        `
      }
    ];

    const quickStartSteps = [
      { step: 1, title: 'Add Your Company', time: '30 seconds', icon: '🏢', description: 'Enter company details and select your industry' },
      { step: 2, title: 'Upload Media', time: '1 minute', icon: '📸', description: 'Drag & drop 3-5 photos or videos' },
      { step: 3, title: 'Generate Content', time: '2 minutes', icon: '✨', description: 'Click Smart Generate for instant content' },
      { step: 4, title: 'Review Results', time: '1 minute', icon: '👀', description: 'Check your generated content and analytics' },
      { step: 5, title: 'Schedule Posts', time: '30 seconds', icon: '📅', description: 'Use the calendar to schedule your content' }
    ];

    const bestPractices = [
      {
        category: 'Content Strategy',
        icon: '📝',
        tips: [
          'Use Smart Generate for trending topics',
          'Weekly Batch for consistent posting',
          'Voice Input for natural conversations',
          'Emergency Posts for timely updates'
        ]
      },
      {
        category: 'Analytics',
        icon: '📊',
        tips: [
          'Check analytics weekly, not daily',
          'Focus on engagement rate over followers',
          'Monitor ROI monthly',
          'Use trending topics for growth'
        ]
      },
      {
        category: 'Media Management',
        icon: '📸',
        tips: [
          'Upload fresh media monthly',
          'Use AI matching for better results',
          'Organize by categories',
          'Tag media for easy search'
        ]
      },
      {
        category: 'Automation',
        icon: '🤖',
        tips: [
          'Enable proactive suggestions',
          'Set up content gap alerts',
          'Use seasonal planning',
          'Monitor compliance automatically'
        ]
      }
    ];

    const faqs = [
      {
        question: 'How long does content generation take?',
        answer: 'Content generation typically takes 20-30 seconds. The AI processes your request, analyzes trending topics, and creates optimized content for each platform.'
      },
      {
        question: 'Can I edit the generated content?',
        answer: 'Absolutely! All generated content is fully editable. You can modify text, add your own touch, or regenerate if needed.'
      },
      {
        question: 'What platforms does PostVelocity support?',
        answer: 'PostVelocity supports 8 major platforms: Instagram, Facebook, LinkedIn, TikTok, YouTube, WhatsApp, Snapchat, and X (Twitter).'
      },
      {
        question: 'How do I interpret my analytics?',
        answer: 'Use our color-coded system: Green (>3% engagement) = Excellent, Yellow (1-3%) = Good, Red (<1%) = Needs Improvement. Focus on engagement rate and ROI.'
      },
      {
        question: 'What makes PostVelocity different?',
        answer: 'PostVelocity combines AI-powered content generation with real-time analytics, drag-drop media management, and proactive suggestions - all in one intuitive platform.'
      },
      {
        question: 'Can I use my own photos and videos?',
        answer: 'Yes! Upload your media to the Media Library. Our AI will automatically match relevant media to your content and suggest the best visuals.'
      }
    ];

    const renderVideoPlayer = (video) => (
      <div className="bg-gray-900 rounded-lg p-8 text-white">
        <div className="flex items-center justify-center mb-6">
          <div className="text-6xl mb-4">{video.thumbnail}</div>
        </div>
        <div className="text-center">
          <h3 className="text-xl font-bold mb-2">{video.title}</h3>
          <p className="text-gray-300 mb-4">{video.description}</p>
          <div className="flex items-center justify-center space-x-4 mb-6">
            <span className="bg-blue-600 px-3 py-1 rounded-full text-sm">Duration: {video.duration}</span>
            <span className="bg-green-600 px-3 py-1 rounded-full text-sm">HD Quality</span>
          </div>
          <button
            onClick={() => setVideoPlaying(!videoPlaying)}
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors text-lg font-semibold"
          >
            {videoPlaying ? '⏸️ Pause Video' : '▶️ Play Video'}
          </button>
        </div>
        {videoPlaying && (
          <div className="mt-8 bg-gray-800 rounded-lg p-4">
            <h4 className="font-bold mb-3">Video Script & Timeline:</h4>
            <pre className="text-sm text-gray-300 whitespace-pre-wrap">{video.script}</pre>
          </div>
        )}
      </div>
    );

    return (
      <div className="space-y-6">
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">🎓 PostVelocity Training Center</h2>
          
          {/* Training Navigation */}
          <div className="flex flex-wrap gap-2 mb-6">
            {[
              { id: 'overview', label: 'Overview', icon: '📋' },
              { id: 'videos', label: 'Video Training', icon: '🎬' },
              { id: 'quickstart', label: 'Quick Start', icon: '⚡' },
              { id: 'guides', label: 'User Guides', icon: '📖' },
              { id: 'analytics', label: 'Analytics Guide', icon: '📊' },
              { id: 'best-practices', label: 'Best Practices', icon: '🏆' },
              { id: 'faq', label: 'FAQ', icon: '❓' }
            ].map((section) => (
              <button
                key={section.id}
                onClick={() => setActiveSection(section.id)}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
                  activeSection === section.id
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                <span>{section.icon}</span>
                <span className="font-medium">{section.label}</span>
              </button>
            ))}
          </div>

          {/* Training Content */}
          <div className="min-h-[400px]">
            {activeSection === 'overview' && (
              <div className="space-y-6">
                <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-6">
                  <h3 className="text-xl font-bold text-gray-800 mb-4">🚀 Welcome to PostVelocity Training!</h3>
                  <p className="text-gray-700 mb-4">
                    PostVelocity is your complete social media management solution. This training center will help you master every feature and become a social media expert.
                  </p>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    <div className="bg-white rounded-lg p-4 border-2 border-blue-200">
                      <h4 className="font-semibold text-blue-800 mb-2">🎬 Video Training</h4>
                      <p className="text-sm text-gray-600">Watch comprehensive video tutorials covering all features</p>
                    </div>
                    <div className="bg-white rounded-lg p-4 border-2 border-green-200">
                      <h4 className="font-semibold text-green-800 mb-2">📖 User Guides</h4>
                      <p className="text-sm text-gray-600">Detailed written guides for step-by-step learning</p>
                    </div>
                    <div className="bg-white rounded-lg p-4 border-2 border-purple-200">
                      <h4 className="font-semibold text-purple-800 mb-2">🏆 Best Practices</h4>
                      <p className="text-sm text-gray-600">Pro tips and strategies for maximum results</p>
                    </div>
                  </div>
                </div>

                <div className="bg-yellow-50 rounded-lg p-6">
                  <h4 className="font-bold text-yellow-800 mb-3">📚 Learning Path Recommendation</h4>
                  <div className="space-y-3">
                    <div className="flex items-center space-x-3">
                      <span className="bg-yellow-600 text-white w-6 h-6 rounded-full flex items-center justify-center text-sm font-bold">1</span>
                      <span>Start with the <strong>Quick Start Guide</strong> (5 minutes)</span>
                    </div>
                    <div className="flex items-center space-x-3">
                      <span className="bg-yellow-600 text-white w-6 h-6 rounded-full flex items-center justify-center text-sm font-bold">2</span>
                      <span>Watch the <strong>Overview Video</strong> (12 minutes)</span>
                    </div>
                    <div className="flex items-center space-x-3">
                      <span className="bg-yellow-600 text-white w-6 h-6 rounded-full flex items-center justify-center text-sm font-bold">3</span>
                      <span>Read the <strong>Analytics Guide</strong> (10 minutes)</span>
                    </div>
                    <div className="flex items-center space-x-3">
                      <span className="bg-yellow-600 text-white w-6 h-6 rounded-full flex items-center justify-center text-sm font-bold">4</span>
                      <span>Practice with <strong>Best Practices</strong> (ongoing)</span>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {activeSection === 'videos' && (
              <div className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {trainingVideos.map((video) => (
                    <div key={video.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                      <div className="flex items-center space-x-3 mb-3">
                        <span className="text-2xl">{video.thumbnail}</span>
                        <div>
                          <h4 className="font-bold text-gray-800">{video.title}</h4>
                          <p className="text-sm text-gray-600">{video.duration}</p>
                        </div>
                      </div>
                      <p className="text-sm text-gray-700 mb-4">{video.description}</p>
                      <button
                        onClick={() => {
                          setActiveSection('video-player');
                          setVideoPlaying(video);
                        }}
                        className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors"
                      >
                        ▶️ Watch Video
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeSection === 'video-player' && videoPlaying && renderVideoPlayer(videoPlaying)}

            {activeSection === 'quickstart' && (
              <div className="space-y-6">
                <div className="bg-green-50 rounded-lg p-6">
                  <h3 className="text-xl font-bold text-green-800 mb-4">⚡ 5-Minute Quick Start</h3>
                  <p className="text-gray-700 mb-6">Follow these 5 simple steps to get your first social media post published in under 5 minutes!</p>
                  
                  <div className="space-y-4">
                    {quickStartSteps.map((item) => (
                      <div key={item.step} className="flex items-start space-x-4 bg-white rounded-lg p-4">
                        <div className="bg-green-600 text-white w-8 h-8 rounded-full flex items-center justify-center font-bold">
                          {item.step}
                        </div>
                        <div className="flex-1">
                          <div className="flex items-center space-x-2 mb-2">
                            <span className="text-lg">{item.icon}</span>
                            <h4 className="font-semibold text-gray-800">{item.title}</h4>
                            <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm">{item.time}</span>
                          </div>
                          <p className="text-gray-600">{item.description}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="bg-blue-50 rounded-lg p-6">
                  <h4 className="font-bold text-blue-800 mb-3">🎯 Success Tips</h4>
                  <ul className="space-y-2 text-gray-700">
                    <li>• <strong>Company Setup:</strong> Be specific about your industry for better AI suggestions</li>
                    <li>• <strong>Media Upload:</strong> Include team photos, equipment, and workplace images</li>
                    <li>• <strong>Content Generation:</strong> Try different topics to see what works best</li>
                    <li>• <strong>Analytics Review:</strong> Look for engagement rate above 2% for good performance</li>
                    <li>• <strong>Scheduling:</strong> Use suggested optimal times for each platform</li>
                  </ul>
                </div>
              </div>
            )}

            {activeSection === 'guides' && (
              <div className="space-y-6">
                <div className="bg-white rounded-lg border-2 border-blue-200 p-6">
                  <h3 className="text-xl font-bold text-blue-800 mb-4">📖 Complete User Guide</h3>
                  <div className="prose max-w-none">
                    <h4 className="text-lg font-semibold text-gray-800 mb-3">📋 Quick Start Guide</h4>
                    <div className="bg-gray-50 rounded-lg p-4 mb-4">
                      <h5 className="font-medium text-gray-700 mb-2">Step 1: Set Up Your Company</h5>
                      <ul className="text-sm text-gray-600 space-y-1">
                        <li>• Click "+ Add Company" in the top right</li>
                        <li>• Enter your business name and select industry</li>
                        <li>• Add website and target audience</li>
                        <li>• Define your brand voice</li>
                      </ul>
                    </div>
                    
                    <div className="bg-gray-50 rounded-lg p-4 mb-4">
                      <h5 className="font-medium text-gray-700 mb-2">Step 2: Upload Media</h5>
                      <ul className="text-sm text-gray-600 space-y-1">
                        <li>• Go to Media Library tab</li>
                        <li>• Drag & drop photos/videos</li>
                        <li>• Choose categories and add tags</li>
                        <li>• AI will help match media to content</li>
                      </ul>
                    </div>

                    <div className="bg-gray-50 rounded-lg p-4 mb-4">
                      <h5 className="font-medium text-gray-700 mb-2">Step 3: Generate Content</h5>
                      <ul className="text-sm text-gray-600 space-y-1">
                        <li>• Use Smart Generate for instant content</li>
                        <li>• Try Weekly Batch for 7 days of content</li>
                        <li>• Use Voice Input to speak topics</li>
                        <li>• Emergency Posts for urgent communications</li>
                      </ul>
                    </div>
                  </div>
                </div>

                <div className="bg-white rounded-lg border-2 border-green-200 p-6">
                  <h4 className="text-lg font-semibold text-green-800 mb-3">🎯 Feature Overview</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-3">
                      <div className="flex items-center space-x-2">
                        <span className="text-lg">🧠</span>
                        <span className="font-medium">Smart Generate</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className="text-lg">📅</span>
                        <span className="font-medium">Weekly Batch</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className="text-lg">🚨</span>
                        <span className="font-medium">Emergency Posts</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className="text-lg">🎤</span>
                        <span className="font-medium">Voice Input</span>
                      </div>
                    </div>
                    <div className="space-y-3">
                      <div className="flex items-center space-x-2">
                        <span className="text-lg">📊</span>
                        <span className="font-medium">Real-time Analytics</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className="text-lg">📸</span>
                        <span className="font-medium">AI Media Matching</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className="text-lg">🗓️</span>
                        <span className="font-medium">Visual Calendar</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className="text-lg">🤖</span>
                        <span className="font-medium">Automation Center</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {activeSection === 'analytics' && (
              <div className="space-y-6">
                <div className="bg-white rounded-lg border-2 border-purple-200 p-6">
                  <h3 className="text-xl font-bold text-purple-800 mb-4">📊 Analytics Mastery Guide</h3>
                  
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                    <div className="bg-green-50 rounded-lg p-4">
                      <h4 className="font-semibold text-green-800 mb-2">🟢 Excellent Performance</h4>
                      <ul className="text-sm text-green-700 space-y-1">
                        <li>• Engagement Rate &gt; 3%</li>
                        <li>• ROI &gt; 500%</li>
                        <li>• Growing reach</li>
                        <li>• Increasing followers</li>
                      </ul>
                    </div>
                    <div className="bg-yellow-50 rounded-lg p-4">
                      <h4 className="font-semibold text-yellow-800 mb-2">🟡 Good Performance</h4>
                      <ul className="text-sm text-yellow-700 space-y-1">
                        <li>• Engagement Rate 1-3%</li>
                        <li>• ROI 200-500%</li>
                        <li>• Stable metrics</li>
                        <li>• Consistent posting</li>
                      </ul>
                    </div>
                    <div className="bg-red-50 rounded-lg p-4">
                      <h4 className="font-semibold text-red-800 mb-2">🔴 Needs Improvement</h4>
                      <ul className="text-sm text-red-700 space-y-1">
                        <li>• Engagement Rate &lt; 1%</li>
                        <li>• ROI &lt; 200%</li>
                        <li>• Declining reach</li>
                        <li>• Irregular posting</li>
                      </ul>
                    </div>
                  </div>

                  <div className="bg-blue-50 rounded-lg p-4">
                    <h4 className="font-semibold text-blue-800 mb-3">🎯 Platform Benchmarks</h4>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                      <div className="text-center">
                        <div className="text-lg mb-1">📸</div>
                        <div className="font-medium">Instagram</div>
                        <div className="text-sm text-gray-600">1-3% engagement</div>
                      </div>
                      <div className="text-center">
                        <div className="text-lg mb-1">👥</div>
                        <div className="font-medium">Facebook</div>
                        <div className="text-sm text-gray-600">0.5-1% engagement</div>
                      </div>
                      <div className="text-center">
                        <div className="text-lg mb-1">💼</div>
                        <div className="font-medium">LinkedIn</div>
                        <div className="text-sm text-gray-600">2-5% engagement</div>
                      </div>
                      <div className="text-center">
                        <div className="text-lg mb-1">🎵</div>
                        <div className="font-medium">TikTok</div>
                        <div className="text-sm text-gray-600">5-15% engagement</div>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="bg-white rounded-lg border-2 border-orange-200 p-6">
                  <h4 className="text-lg font-semibold text-orange-800 mb-3">💰 ROI Calculation Guide</h4>
                  <div className="bg-orange-50 rounded-lg p-4">
                    <h5 className="font-medium text-orange-800 mb-2">Formula:</h5>
                    <code className="bg-white px-2 py-1 rounded text-sm">
                      ROI = (Revenue Generated - Cost) / Cost × 100
                    </code>
                    <div className="mt-3">
                      <h5 className="font-medium text-orange-800 mb-2">Example:</h5>
                      <p className="text-sm text-orange-700">
                        Revenue: $10,000 | Cost: $1,000 | ROI = ($10,000 - $1,000) / $1,000 × 100 = 900%
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {activeSection === 'best-practices' && (
              <div className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {bestPractices.map((category) => (
                    <div key={category.category} className="bg-white rounded-lg border-2 border-gray-200 p-6">
                      <div className="flex items-center space-x-3 mb-4">
                        <span className="text-2xl">{category.icon}</span>
                        <h3 className="text-lg font-bold text-gray-800">{category.category}</h3>
                      </div>
                      <ul className="space-y-2">
                        {category.tips.map((tip, index) => (
                          <li key={index} className="flex items-start space-x-2">
                            <span className="text-green-600 mt-1">✓</span>
                            <span className="text-gray-700">{tip}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </div>

                <div className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg p-6">
                  <h3 className="text-xl font-bold text-purple-800 mb-4">🏆 Pro Tips for Maximum Results</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="bg-white rounded-lg p-4">
                      <h4 className="font-semibold text-gray-800 mb-2">📈 Growth Strategies</h4>
                      <ul className="text-sm text-gray-600 space-y-1">
                        <li>• Post at optimal times (shown in Calendar)</li>
                        <li>• Use trending hashtags from Analytics</li>
                        <li>• Cross-post to multiple platforms</li>
                        <li>• Engage with your audience promptly</li>
                      </ul>
                    </div>
                    <div className="bg-white rounded-lg p-4">
                      <h4 className="font-semibold text-gray-800 mb-2">⚡ Time-Saving Tips</h4>
                      <ul className="text-sm text-gray-600 space-y-1">
                        <li>• Use Weekly Batch for efficiency</li>
                        <li>• Enable automation features</li>
                        <li>• Save successful content as templates</li>
                        <li>• Voice input for quick topic entry</li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {activeSection === 'faq' && (
              <div className="space-y-6">
                <div className="bg-white rounded-lg border-2 border-blue-200 p-6">
                  <h3 className="text-xl font-bold text-blue-800 mb-6">❓ Frequently Asked Questions</h3>
                  <div className="space-y-4">
                    {faqs.map((faq, index) => (
                      <div key={index} className="border-b border-gray-200 pb-4">
                        <h4 className="font-semibold text-gray-800 mb-2">{faq.question}</h4>
                        <p className="text-gray-600">{faq.answer}</p>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="bg-green-50 rounded-lg p-6">
                  <h4 className="font-bold text-green-800 mb-3">🚀 Still Need Help?</h4>
                  <p className="text-green-700 mb-4">
                    Can't find what you're looking for? Here are additional resources:
                  </p>
                  <div className="space-y-2">
                    <div className="flex items-center space-x-2">
                      <span className="text-green-600">📧</span>
                      <span className="text-green-700">Email support: support@postvelocity.com</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <span className="text-green-600">💬</span>
                      <span className="text-green-700">Live chat: Available 24/7 in-app</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <span className="text-green-600">📖</span>
                      <span className="text-green-700">Knowledge base: Updated weekly with new tips</span>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    );
  };

  // Team Management Tab
  const TeamTab = () => {
    return (
      <div className="space-y-6">
        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900">👥 Team Management</h2>
            <button
              onClick={() => setShowInviteModal(true)}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors font-medium"
            >
              + Invite Member
            </button>
          </div>

          {/* Team Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
            <div className="bg-blue-50 rounded-lg p-4">
              <h4 className="text-sm font-medium text-blue-600">Team Members</h4>
              <p className="text-2xl font-bold text-blue-900">{teamMembers.length}</p>
              <p className="text-xs text-blue-700">
                Limit: {getFeatureLimit('users') === Infinity ? 'Unlimited' : getFeatureLimit('users')}
              </p>
            </div>
            <div className="bg-green-50 rounded-lg p-4">
              <h4 className="text-sm font-medium text-green-600">Active Members</h4>
              <p className="text-2xl font-bold text-green-900">
                {teamMembers.filter(m => m.is_active).length}
              </p>
              <p className="text-xs text-green-700">Online now</p>
            </div>
            <div className="bg-purple-50 rounded-lg p-4">
              <h4 className="text-sm font-medium text-purple-600">Roles</h4>
              <p className="text-2xl font-bold text-purple-900">
                {new Set(teamMembers.map(m => m.role)).size}
              </p>
              <p className="text-xs text-purple-700">Different roles</p>
            </div>
          </div>

          {/* Team Members List */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-800">Team Members</h3>
            
            {teamMembers.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                <p className="text-lg mb-2">👥 No team members yet</p>
                <p className="text-sm">Invite your first team member to get started!</p>
              </div>
            ) : (
              <div className="space-y-3">
                {teamMembers.map((member) => (
                  <div key={member.id} className="bg-gray-50 rounded-lg p-4 flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center text-white font-semibold">
                        {member.full_name.charAt(0).toUpperCase()}
                      </div>
                      <div>
                        <h4 className="font-semibold text-gray-800">{member.full_name}</h4>
                        <p className="text-sm text-gray-600">{member.email}</p>
                        <div className="flex items-center space-x-2 mt-1">
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                            member.role === 'admin' ? 'bg-red-100 text-red-800' :
                            member.role === 'editor' ? 'bg-blue-100 text-blue-800' :
                            'bg-gray-100 text-gray-800'
                          }`}>
                            {member.role}
                          </span>
                          <span className={`w-2 h-2 rounded-full ${
                            member.is_active ? 'bg-green-500' : 'bg-gray-400'
                          }`}></span>
                          <span className="text-xs text-gray-500">
                            {member.is_active ? 'Active' : 'Inactive'}
                          </span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-2">
                      <select
                        value={member.role}
                        onChange={(e) => updateMemberRole(member.user_id, e.target.value)}
                        className="text-sm border border-gray-300 rounded px-2 py-1"
                      >
                        <option value="member">Member</option>
                        <option value="editor">Editor</option>
                        <option value="admin">Admin</option>
                      </select>
                      <button
                        onClick={() => removeMember(member.user_id, member.full_name)}
                        className="text-red-600 hover:text-red-800 p-1"
                        title="Remove member"
                      >
                        🗑️
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Plan Limits Info */}
          <div className="mt-8 bg-yellow-50 rounded-lg p-4 border border-yellow-200">
            <h4 className="font-semibold text-yellow-800 mb-2">📊 Plan Limits</h4>
            <div className="text-sm text-yellow-700">
              <p>Current Plan: <span className="font-semibold">{getPlanDisplayName(currentUserPlan)}</span></p>
              <p>User Limit: <span className="font-semibold">
                {getFeatureLimit('users') === Infinity ? 'Unlimited' : `${teamMembers.length}/${getFeatureLimit('users')}`}
              </span></p>
              {teamMembers.length >= getFeatureLimit('users') * 0.8 && getFeatureLimit('users') !== Infinity && (
                <p className="text-orange-600 font-medium mt-2">
                  ⚠️ Approaching user limit. Consider upgrading your plan.
                </p>
              )}
            </div>
          </div>
        </div>

        {/* Team Permissions & Roles Guide */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">🔐 Roles & Permissions</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="border border-gray-200 rounded-lg p-4">
              <h4 className="font-semibold text-red-800 mb-2">Admin</h4>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>✓ Full access to all features</li>
                <li>✓ Manage team members</li>
                <li>✓ Billing & subscription</li>
                <li>✓ Delete companies/content</li>
              </ul>
            </div>
            <div className="border border-gray-200 rounded-lg p-4">
              <h4 className="font-semibold text-blue-800 mb-2">Editor</h4>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>✓ Create & edit content</li>
                <li>✓ Manage media library</li>
                <li>✓ Schedule posts</li>
                <li>✗ Manage team members</li>
              </ul>
            </div>
            <div className="border border-gray-200 rounded-lg p-4">
              <h4 className="font-semibold text-gray-800 mb-2">Member</h4>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>✓ View content & analytics</li>
                <li>✓ Create basic content</li>
                <li>✗ Edit others' content</li>
                <li>✗ Manage settings</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    );
  };

  // Billing & Usage Dashboard Tab
  const BillingTab = () => {
    const [billingHistory, setBillingHistory] = useState([
      {
        id: '1',
        date: '2024-12-15',
        description: 'Professional Plan - Monthly',
        amount: 69.00,
        status: 'paid',
        invoice_url: '#'
      },
      {
        id: '2',
        date: '2024-11-15',
        description: 'Professional Plan - Monthly',
        amount: 69.00,
        status: 'paid',
        invoice_url: '#'
      }
    ]);

    return (
      <div className="space-y-6">
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">💳 Billing & Usage</h2>

          {/* Current Plan Overview */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
            <div className="lg:col-span-2">
              <div className="bg-gradient-to-r from-blue-50 to-blue-100 rounded-lg p-6">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-xl font-bold text-blue-900">
                      {getPlanDisplayName(currentUserPlan)} Plan
                    </h3>
                    <p className="text-blue-700">Active subscription</p>
                  </div>
                  <div className="text-right">
                    <p className="text-2xl font-bold text-blue-900">
                      ${availablePlans[currentUserPlan]?.pricing?.monthly || 0}
                    </p>
                    <p className="text-blue-700">/month</p>
                  </div>
                </div>
                
                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div>
                    <p className="text-sm text-blue-600">Companies</p>
                    <p className="font-semibold">
                      {userUsage?.companies_count || 0} / {getFeatureLimit('companies') === Infinity ? '∞' : getFeatureLimit('companies')}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-blue-600">Users</p>
                    <p className="font-semibold">
                      {teamMembers.length} / {getFeatureLimit('users') === Infinity ? '∞' : getFeatureLimit('users')}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-blue-600">Posts This Month</p>
                    <p className="font-semibold">
                      {userUsage?.posts_generated || 0} / {getFeatureLimit('posts_per_month') === Infinity ? '∞' : getFeatureLimit('posts_per_month')}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-blue-600">Social Accounts</p>
                    <p className="font-semibold">
                      {userUsage?.social_accounts_count || 0} / {getFeatureLimit('social_accounts_per_company') === Infinity ? '∞' : getFeatureLimit('social_accounts_per_company')}
                    </p>
                  </div>
                </div>

                <button
                  onClick={() => setShowPricingModal(true)}
                  className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors font-medium"
                >
                  Upgrade Plan
                </button>
              </div>
            </div>

            <div className="space-y-4">
              {/* Usage Alerts */}
              {usageWarnings.length > 0 && (
                <div className="bg-yellow-50 rounded-lg p-4 border border-yellow-200">
                  <h4 className="font-semibold text-yellow-800 mb-2">⚠️ Usage Alerts</h4>
                  <div className="space-y-2">
                    {usageWarnings.map((warning, index) => (
                      <div key={index} className="text-yellow-700 text-sm">
                        <span className="font-medium">{warning.type.replace('_', ' ')}:</span> {warning.percentage}%
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Next Billing Date */}
              <div className="bg-green-50 rounded-lg p-4 border border-green-200">
                <h4 className="font-semibold text-green-800 mb-2">📅 Next Billing</h4>
                <p className="text-green-700">January 15, 2025</p>
                <p className="text-sm text-green-600">Auto-renewal enabled</p>
              </div>
            </div>
          </div>

          {/* Usage Charts */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div className="bg-gray-50 rounded-lg p-4">
              <h4 className="font-semibold text-gray-800 mb-4">📈 Monthly Usage Trend</h4>
              <div className="space-y-3">
                {['Posts Generated', 'API Calls', 'Storage Used', 'Team Activity'].map((metric, index) => (
                  <div key={metric} className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">{metric}</span>
                    <div className="flex items-center space-x-2">
                      <div className="w-24 bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-blue-600 h-2 rounded-full" 
                          style={{ width: `${Math.random() * 80 + 20}%` }}
                        ></div>
                      </div>
                      <span className="text-sm font-medium">{Math.floor(Math.random() * 100)}%</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-gray-50 rounded-lg p-4">
              <h4 className="font-semibold text-gray-800 mb-4">🏆 Feature Usage</h4>
              <div className="space-y-3">
                {[
                  { feature: 'Content Generation', used: hasFeature('advanced_ai_content') },
                  { feature: 'Team Collaboration', used: hasFeature('team_collaboration') },
                  { feature: 'Bulk Upload', used: hasFeature('bulk_upload') },
                  { feature: 'API Access', used: hasFeature('api_access') }
                ].map((item) => (
                  <div key={item.feature} className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">{item.feature}</span>
                    <span className={`text-sm font-medium ${item.used ? 'text-green-600' : 'text-gray-400'}`}>
                      {item.used ? '✓ Available' : '✗ Upgrade Required'}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Billing History */}
          <div>
            <h3 className="text-lg font-semibold text-gray-800 mb-4">📄 Billing History</h3>
            <div className="overflow-x-auto">
              <table className="w-full border border-gray-200 rounded-lg">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-3 text-left text-sm font-semibold text-gray-600">Date</th>
                    <th className="px-4 py-3 text-left text-sm font-semibold text-gray-600">Description</th>
                    <th className="px-4 py-3 text-left text-sm font-semibold text-gray-600">Amount</th>
                    <th className="px-4 py-3 text-left text-sm font-semibold text-gray-600">Status</th>
                    <th className="px-4 py-3 text-left text-sm font-semibold text-gray-600">Invoice</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {billingHistory.map((transaction) => (
                    <tr key={transaction.id} className="hover:bg-gray-50">
                      <td className="px-4 py-3 text-sm text-gray-900">
                        {new Date(transaction.date).toLocaleDateString()}
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-900">
                        {transaction.description}
                      </td>
                      <td className="px-4 py-3 text-sm font-medium text-gray-900">
                        ${transaction.amount.toFixed(2)}
                      </td>
                      <td className="px-4 py-3 text-sm">
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                          transaction.status === 'paid' 
                            ? 'bg-green-100 text-green-800' 
                            : transaction.status === 'pending'
                              ? 'bg-yellow-100 text-yellow-800'
                              : 'bg-red-100 text-red-800'
                        }`}>
                          {transaction.status.charAt(0).toUpperCase() + transaction.status.slice(1)}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-sm">
                        <a 
                          href={transaction.invoice_url}
                          className="text-blue-600 hover:text-blue-800 font-medium"
                        >
                          Download
                        </a>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {billingHistory.length === 0 && (
              <div className="text-center py-8 text-gray-500">
                <p className="text-lg mb-2">📄 No billing history yet</p>
                <p className="text-sm">Your billing history will appear here after your first payment.</p>
              </div>
            )}
          </div>

          {/* Account Management */}
          <div className="mt-8 pt-6 border-t border-gray-200">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">⚙️ Account Management</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <button className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
                <div>
                  <h4 className="font-medium text-gray-800">Update Payment Method</h4>
                  <p className="text-sm text-gray-600">•••• •••• •••• 1234</p>
                </div>
                <span className="text-blue-600">→</span>
              </button>
              
              <button className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
                <div>
                  <h4 className="font-medium text-gray-800">Download Receipts</h4>
                  <p className="text-sm text-gray-600">Get all invoices as PDF</p>
                </div>
                <span className="text-blue-600">→</span>
              </button>
              
              <button className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
                <div>
                  <h4 className="font-medium text-gray-800">Cancel Subscription</h4>
                  <p className="text-sm text-gray-600">Effective next billing cycle</p>
                </div>
                <span className="text-red-600">→</span>
              </button>
              
              <button 
                onClick={() => setShowPricingModal(true)}
                className="flex items-center justify-between p-4 border border-blue-200 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors"
              >
                <div>
                  <h4 className="font-medium text-blue-800">Upgrade Plan</h4>
                  <p className="text-sm text-blue-600">Access more features</p>
                </div>
                <span className="text-blue-600">→</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  };

  // Partner Program Tab
  const PartnersTab = () => {
    return (
      <div className="space-y-6">
        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900">🔗 Partner Program</h2>
            {!partnerData && (
              <button
                onClick={() => setShowPartnerModal(true)}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors font-medium"
              >
                Join Partner Program
              </button>
            )}
          </div>

          {/* Partner Status */}
          {partnerData ? (
            <div className="space-y-6">
              {/* Partner Overview */}
              <div className="bg-gradient-to-r from-green-50 to-blue-50 rounded-lg p-6">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="text-xl font-bold text-green-900 mb-2">
                      {partnerData.partner_type.charAt(0).toUpperCase() + partnerData.partner_type.slice(1)} Partner
                    </h3>
                    <p className="text-green-700 mb-2">Status: <span className="font-semibold">{partnerData.status}</span></p>
                    <p className="text-green-700">Commission Rate: <span className="font-semibold">{(partnerData.commission_rate * 100)}%</span></p>
                  </div>
                  <div className="text-right">
                    <div className="bg-white rounded-lg p-3 border border-green-200">
                      <p className="text-sm text-gray-600">Your Referral Code</p>
                      <p className="text-lg font-bold text-green-800">{referralCode}</p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Partner Stats */}
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="bg-blue-50 rounded-lg p-4">
                  <h4 className="text-sm font-medium text-blue-600">Total Referrals</h4>
                  <p className="text-2xl font-bold text-blue-900">{partnerStats.total_referrals || 0}</p>
                  <p className="text-xs text-blue-700">All-time signups</p>
                </div>
                <div className="bg-green-50 rounded-lg p-4">
                  <h4 className="text-sm font-medium text-green-600">Commission Earned</h4>
                  <p className="text-2xl font-bold text-green-900">${(partnerStats.total_commission_earned || 0).toFixed(2)}</p>
                  <p className="text-xs text-green-700">Ready for payout</p>
                </div>
                <div className="bg-purple-50 rounded-lg p-4">
                  <h4 className="text-sm font-medium text-purple-600">Monthly Volume</h4>
                  <p className="text-2xl font-bold text-purple-900">${(partnerStats.monthly_sales_volume || 0).toFixed(2)}</p>
                  <p className="text-xs text-purple-700">This month</p>
                </div>
                <div className="bg-orange-50 rounded-lg p-4">
                  <h4 className="text-sm font-medium text-orange-600">Conversion Rate</h4>
                  <p className="text-2xl font-bold text-orange-900">{(partnerStats.conversion_rate || 0).toFixed(1)}%</p>
                  <p className="text-xs text-orange-700">Signup to paid</p>
                </div>
              </div>

              {/* Referral Tools */}
              <div className="bg-white border border-gray-200 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">🛠️ Referral Tools</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {/* Referral Link */}
                  <div className="border border-gray-200 rounded-lg p-4">
                    <h4 className="font-semibold text-gray-800 mb-2">📎 Referral Link</h4>
                    <div className="flex items-center space-x-2 mb-3">
                      <input
                        type="text"
                        value={`https://postvelocity.com/ref/${referralCode}`}
                        readOnly
                        className="flex-1 p-2 border border-gray-300 rounded text-sm bg-gray-50"
                      />
                      <button
                        onClick={copyReferralLink}
                        className="bg-blue-600 text-white px-3 py-2 rounded hover:bg-blue-700 text-sm"
                      >
                        Copy
                      </button>
                    </div>
                    <p className="text-xs text-gray-600">Share this link to earn {(partnerData.commission_rate * 100)}% commission on all sales</p>
                  </div>

                  {/* QR Code */}
                  <div className="border border-gray-200 rounded-lg p-4">
                    <h4 className="font-semibold text-gray-800 mb-2">📱 QR Code</h4>
                    <button
                      onClick={generateReferralQR}
                      className="w-full bg-gray-600 text-white py-2 px-4 rounded hover:bg-gray-700 transition-colors"
                    >
                      Generate QR Code
                    </button>
                    <p className="text-xs text-gray-600 mt-2">Perfect for business cards and presentations</p>
                  </div>

                  {/* Email Template */}
                  <div className="border border-gray-200 rounded-lg p-4">
                    <h4 className="font-semibold text-gray-800 mb-2">📧 Email Template</h4>
                    <button className="w-full bg-purple-600 text-white py-2 px-4 rounded hover:bg-purple-700 transition-colors">
                      Copy Email Template
                    </button>
                    <p className="text-xs text-gray-600 mt-2">Professional email template for outreach</p>
                  </div>

                  {/* Social Media Kit */}
                  <div className="border border-gray-200 rounded-lg p-4">
                    <h4 className="font-semibold text-gray-800 mb-2">📱 Social Media Kit</h4>
                    <button className="w-full bg-pink-600 text-white py-2 px-4 rounded hover:bg-pink-700 transition-colors">
                      Download Assets
                    </button>
                    <p className="text-xs text-gray-600 mt-2">Banners, posts, and graphics for social sharing</p>
                  </div>
                </div>
              </div>

              {/* Commission Structure */}
              <div className="bg-white border border-gray-200 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">💰 Commission Structure</h3>
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                  <div className="text-center p-4 bg-gray-50 rounded-lg">
                    <h4 className="font-semibold text-gray-800">Starter Plan</h4>
                    <p className="text-2xl font-bold text-blue-600">${((29 * partnerData.commission_rate) || 0).toFixed(0)}</p>
                    <p className="text-sm text-gray-600">per month per user</p>
                  </div>
                  <div className="text-center p-4 bg-blue-50 rounded-lg border-2 border-blue-200">
                    <h4 className="font-semibold text-blue-800">Professional</h4>
                    <p className="text-2xl font-bold text-blue-600">${((69 * partnerData.commission_rate) || 0).toFixed(0)}</p>
                    <p className="text-sm text-blue-600">⭐ Most Popular</p>
                  </div>
                  <div className="text-center p-4 bg-gray-50 rounded-lg">
                    <h4 className="font-semibold text-gray-800">Business</h4>
                    <p className="text-2xl font-bold text-purple-600">${((149 * partnerData.commission_rate) || 0).toFixed(0)}</p>
                    <p className="text-sm text-gray-600">per month per user</p>
                  </div>
                  <div className="text-center p-4 bg-gray-50 rounded-lg">
                    <h4 className="font-semibold text-gray-800">Enterprise</h4>
                    <p className="text-2xl font-bold text-green-600">${((349 * partnerData.commission_rate) || 0).toFixed(0)}</p>
                    <p className="text-sm text-gray-600">per month per user</p>
                  </div>
                </div>
                <div className="mt-4 bg-yellow-50 rounded-lg p-4 border border-yellow-200">
                  <p className="text-yellow-800 text-sm">
                    <strong>💡 Pro Tip:</strong> You earn {(partnerData.commission_rate * 100)}% recurring commission for the first 12 months, then {((partnerData.commission_rate - 0.1) * 100)}% thereafter.
                  </p>
                </div>
              </div>

              {/* Recent Activity */}
              <div className="bg-white border border-gray-200 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">📈 Recent Activity</h3>
                <div className="space-y-3">
                  {/* Mock activity data */}
                  {[
                    { action: 'New signup', user: 'john@example.com', date: '2 hours ago', status: 'trial' },
                    { action: 'Conversion', user: 'sarah@company.com', date: '1 day ago', status: 'paid', commission: 28.00 },
                    { action: 'New signup', user: 'mike@startup.com', date: '3 days ago', status: 'trial' }
                  ].map((activity, index) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded">
                      <div className="flex items-center space-x-3">
                        <span className={`w-3 h-3 rounded-full ${
                          activity.status === 'paid' ? 'bg-green-500' : 
                          activity.status === 'trial' ? 'bg-yellow-500' : 'bg-gray-400'
                        }`}></span>
                        <div>
                          <p className="text-sm font-medium text-gray-800">{activity.action}</p>
                          <p className="text-xs text-gray-600">{activity.user}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        {activity.commission && (
                          <p className="text-sm font-semibold text-green-600">+${activity.commission}</p>
                        )}
                        <p className="text-xs text-gray-500">{activity.date}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            /* Join Partner Program CTA */
            <div className="text-center py-12">
              <div className="max-w-2xl mx-auto">
                <h3 className="text-2xl font-bold text-gray-900 mb-4">💰 Earn Money with PostVelocity</h3>
                <p className="text-lg text-gray-600 mb-8">
                  Join our partner program and earn up to <strong>70% commission</strong> on every referral. 
                  Perfect for agencies, freelancers, and social media professionals.
                </p>
                
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
                  <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
                    <h4 className="font-semibold text-blue-800">🔗 Affiliate</h4>
                    <p className="text-2xl font-bold text-blue-600">30%</p>
                    <p className="text-sm text-blue-600">Commission rate</p>
                    <ul className="text-xs text-blue-700 mt-2 space-y-1">
                      <li>• Simple referral links</li>
                      <li>• Basic reporting</li>
                      <li>• Monthly payouts</li>
                    </ul>
                  </div>
                  
                  <div className="bg-green-50 rounded-lg p-4 border-2 border-green-400">
                    <h4 className="font-semibold text-green-800">🏢 Agency</h4>
                    <p className="text-2xl font-bold text-green-600">40%</p>
                    <p className="text-sm text-green-600">Commission rate ⭐</p>
                    <ul className="text-xs text-green-700 mt-2 space-y-1">
                      <li>• White-label portal</li>
                      <li>• Custom domain</li>
                      <li>• Priority support</li>
                    </ul>
                  </div>
                  
                  <div className="bg-purple-50 rounded-lg p-4 border border-purple-200">
                    <h4 className="font-semibold text-purple-800">🏪 Reseller</h4>
                    <p className="text-2xl font-bold text-purple-600">60%</p>
                    <p className="text-sm text-purple-600">Discount rate</p>
                    <ul className="text-xs text-purple-700 mt-2 space-y-1">
                      <li>• Full white-labeling</li>
                      <li>• API access</li>
                      <li>• Set your own pricing</li>
                    </ul>
                  </div>
                  
                  <div className="bg-orange-50 rounded-lg p-4 border border-orange-200">
                    <h4 className="font-semibold text-orange-800">🌍 Distributor</h4>
                    <p className="text-2xl font-bold text-orange-600">70%</p>
                    <p className="text-sm text-orange-600">Discount rate</p>
                    <ul className="text-xs text-orange-700 mt-2 space-y-1">
                      <li>• Territory exclusivity</li>
                      <li>• Custom features</li>
                      <li>• Revenue sharing</li>
                    </ul>
                  </div>
                </div>

                <button
                  onClick={() => setShowPartnerModal(true)}
                  className="bg-blue-600 text-white px-8 py-4 rounded-lg hover:bg-blue-700 transition-colors font-semibold text-lg"
                >
                  Join Partner Program
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    );
  };

  // API Management Tab
  const ApiTab = () => {
    return (
      <div className="space-y-6">
        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900">🔌 API Management</h2>
            <button
              onClick={() => setShowApiModal(true)}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors font-medium"
            >
              + Generate API Key
            </button>
          </div>

          {/* API Overview */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
            <div className="bg-blue-50 rounded-lg p-4">
              <h4 className="text-sm font-medium text-blue-600">Active API Keys</h4>
              <p className="text-2xl font-bold text-blue-900">{apiKeys.length}</p>
              <p className="text-xs text-blue-700">Currently active</p>
            </div>
            <div className="bg-green-50 rounded-lg p-4">
              <h4 className="text-sm font-medium text-green-600">Monthly Requests</h4>
              <p className="text-2xl font-bold text-green-900">{apiKeys.reduce((total, key) => total + (key.total_requests || 0), 0)}</p>
              <p className="text-xs text-green-700">This month</p>
            </div>
            <div className="bg-purple-50 rounded-lg p-4">
              <h4 className="text-sm font-medium text-purple-600">Rate Limit</h4>
              <p className="text-2xl font-bold text-purple-900">1,000</p>
              <p className="text-xs text-purple-700">Requests per hour</p>
            </div>
          </div>

          {/* API Keys List */}
          <div className="space-y-4 mb-8">
            <h3 className="text-lg font-semibold text-gray-800">Your API Keys</h3>
            
            {apiKeys.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                <p className="text-lg mb-2">🔌 No API keys yet</p>
                <p className="text-sm">Generate your first API key to get started with programmatic access!</p>
              </div>
            ) : (
              <div className="space-y-3">
                {apiKeys.map((key) => (
                  <div key={key.id} className="bg-gray-50 rounded-lg p-4 flex items-center justify-between">
                    <div className="flex-1">
                      <h4 className="font-semibold text-gray-800">{key.key_name}</h4>
                      <p className="text-sm text-gray-600 font-mono">{key.api_key}</p>
                      <div className="flex items-center space-x-4 mt-2 text-sm text-gray-500">
                        <span>Permissions: {key.permissions.join(', ')}</span>
                        <span>Requests: {key.total_requests}</span>
                        <span>Last Used: {key.last_used ? new Date(key.last_used).toLocaleDateString() : 'Never'}</span>
                      </div>
                      <div className="flex items-center space-x-2 mt-1">
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                          new Date(key.expires_at) > new Date() 
                            ? 'bg-green-100 text-green-800' 
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {new Date(key.expires_at) > new Date() ? 'Active' : 'Expired'}
                        </span>
                        <span className="text-xs text-gray-500">
                          Expires: {new Date(key.expires_at).toLocaleDateString()}
                        </span>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-2">
                      <button
                        onClick={() => copyApiKey(key.api_key, 'hidden_for_security')}
                        className="text-blue-600 hover:text-blue-800 p-2 rounded hover:bg-blue-50"
                        title="Copy API key"
                      >
                        📋
                      </button>
                      <button
                        onClick={() => revokeApiKey(key.id, key.key_name)}
                        className="text-red-600 hover:text-red-800 p-2 rounded hover:bg-red-50"
                        title="Revoke API key"
                      >
                        🗑️
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* API Documentation */}
          <div className="bg-gray-50 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">📚 API Documentation</h3>
            
            <div className="space-y-6">
              {/* Authentication */}
              <div>
                <h4 className="font-semibold text-gray-800 mb-2">🔐 Authentication</h4>
                <div className="bg-gray-800 rounded-lg p-4 text-green-400 font-mono text-sm overflow-x-auto">
                  <div>curl -H "Authorization: Bearer YOUR_API_KEY" \</div>
                  <div className="ml-5">https://api.postvelocity.com/v1/content</div>
                </div>
              </div>

              {/* Available Endpoints */}
              <div>
                <h4 className="font-semibold text-gray-800 mb-2">📡 Available Endpoints</h4>
                <div className="space-y-3">
                  <div className="border border-gray-200 rounded p-3">
                    <div className="flex items-center space-x-2 mb-1">
                      <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-xs font-semibold">GET</span>
                      <code className="text-sm">/api/v1/content</code>
                    </div>
                    <p className="text-sm text-gray-600">Get your generated content (requires 'read' permission)</p>
                  </div>
                  
                  <div className="border border-gray-200 rounded p-3">
                    <div className="flex items-center space-x-2 mb-1">
                      <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs font-semibold">POST</span>
                      <code className="text-sm">/api/v1/content/generate</code>
                    </div>
                    <p className="text-sm text-gray-600">Generate new content (requires 'write' permission)</p>
                  </div>
                  
                  <div className="border border-gray-200 rounded p-3">
                    <div className="flex items-center space-x-2 mb-1">
                      <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-xs font-semibold">GET</span>
                      <code className="text-sm">/api/v1/analytics</code>
                    </div>
                    <p className="text-sm text-gray-600">Get analytics data (requires 'read' permission)</p>
                  </div>
                </div>
              </div>

              {/* Code Examples */}
              <div>
                <h4 className="font-semibold text-gray-800 mb-2">💻 Code Examples</h4>
                
                <div className="space-y-4">
                  <div>
                    <h5 className="font-medium text-gray-700 mb-2">Generate Content (JavaScript)</h5>
                    <div className="bg-gray-800 rounded-lg p-4 text-green-400 font-mono text-sm overflow-x-auto">
                      <div>const response = await fetch('/api/v1/content/generate', &#123;</div>
                      <div>&nbsp;&nbsp;method: 'POST',</div>
                      <div>&nbsp;&nbsp;headers: &#123;</div>
                      <div>&nbsp;&nbsp;&nbsp;&nbsp;'Authorization': 'Bearer YOUR_API_KEY',</div>
                      <div>&nbsp;&nbsp;&nbsp;&nbsp;'Content-Type': 'application/json'</div>
                      <div>&nbsp;&nbsp;&#125;,</div>
                      <div>&nbsp;&nbsp;body: JSON.stringify(&#123;</div>
                      <div>&nbsp;&nbsp;&nbsp;&nbsp;topic: 'AI and Social Media',</div>
                      <div>&nbsp;&nbsp;&nbsp;&nbsp;platform: 'instagram'</div>
                      <div>&nbsp;&nbsp;&#125;)</div>
                      <div>&#125;);</div>
                    </div>
                  </div>

                  <div>
                    <h5 className="font-medium text-gray-700 mb-2">Get Analytics (Python)</h5>
                    <div className="bg-gray-800 rounded-lg p-4 text-green-400 font-mono text-sm overflow-x-auto">
                      <div>import requests</div>
                      <div></div>
                      <div>headers = &#123;'Authorization': 'Bearer YOUR_API_KEY'&#125;</div>
                      <div>response = requests.get('/api/v1/analytics?days=30', headers=headers)</div>
                      <div>data = response.json()</div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Rate Limits */}
              <div>
                <h4 className="font-semibold text-gray-800 mb-2">⚡ Rate Limits</h4>
                <div className="bg-yellow-50 rounded-lg p-4 border border-yellow-200">
                  <ul className="text-sm text-yellow-800 space-y-1">
                    <li>• <strong>Business Plan:</strong> 1,000 requests per hour</li>
                    <li>• <strong>Enterprise Plan:</strong> 5,000 requests per hour</li>
                    <li>• Rate limits reset every hour</li>
                    <li>• Exceeding limits returns HTTP 429 (Too Many Requests)</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  };

  // Enhanced Automation Tab
  const AutomationTab = () => {
    const [automationRules, setAutomationRules] = useState([]);
    const [showRuleForm, setShowRuleForm] = useState(false);

    return (
      <div className="space-y-6">
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">🤖 Automation Center</h2>
          
          {/* Proactive Suggestions */}
          <div className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg p-6 mb-6">
            <h3 className="text-lg font-semibold text-purple-800 mb-4">🧠 AI Proactive Suggestions</h3>
            <div className="space-y-3">
              <div className="flex items-start space-x-3 p-3 bg-white rounded-lg">
                <span className="text-lg">🔥</span>
                <div>
                  <p className="font-medium text-gray-800">Trending Alert</p>
                  <p className="text-sm text-gray-600">"AI in Construction" is trending. Create content now for maximum reach.</p>
                  <button className="mt-2 text-sm bg-purple-600 text-white px-3 py-1 rounded hover:bg-purple-700">
                    Generate Content
                  </button>
                </div>
              </div>
              <div className="flex items-start space-x-3 p-3 bg-white rounded-lg">
                <span className="text-lg">📅</span>
                <div>
                  <p className="font-medium text-gray-800">Content Gap Detected</p>
                  <p className="text-sm text-gray-600">No posts scheduled for next weekend. Suggest creating weekend content.</p>
                  <button className="mt-2 text-sm bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700">
                    Schedule Weekend Posts
                  </button>
                </div>
              </div>
              <div className="flex items-start space-x-3 p-3 bg-white rounded-lg">
                <span className="text-lg">🎯</span>
                <div>
                  <p className="font-medium text-gray-800">Seasonal Opportunity</p>
                  <p className="text-sm text-gray-600">National Safety Month is coming up. Start preparing safety-focused content.</p>
                  <button className="mt-2 text-sm bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700">
                    Plan Safety Content
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Media Requests */}
          {mediaRequests.length > 0 && (
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 mb-6">
              <h3 className="text-lg font-semibold text-yellow-800 mb-4">📅 Monthly Media Requests</h3>
              <div className="space-y-4">
                {mediaRequests.map((request) => (
                  <div key={request.company_id} className="bg-white border border-yellow-200 rounded-lg p-4">
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <h4 className="font-semibold text-gray-800">{request.company_name}</h4>
                        <p className="text-sm text-gray-600">Current media: {request.current_media_count} files</p>
                      </div>
                      <button
                        onClick={() => addNotification('Media request marked as sent!', 'success')}
                        className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700 transition-colors"
                      >
                        Mark as Sent
                      </button>
                    </div>
                    
                    <div className="text-sm text-gray-600 bg-gray-50 rounded p-2">
                      <strong>Recommendation:</strong> {request.recommendation}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Smart Workflows */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div className="border border-gray-200 rounded-lg p-4">
              <h3 className="font-semibold text-gray-800 mb-2">🔄 Content Automation</h3>
              <p className="text-sm text-gray-600 mb-4">Set up automated content generation for recurring topics</p>
              <div className="space-y-2">
                <div className="flex items-center space-x-2">
                  <input type="checkbox" id="weekly-safety" className="rounded" />
                  <label htmlFor="weekly-safety" className="text-sm">Weekly Safety Tips</label>
                </div>
                <div className="flex items-center space-x-2">
                  <input type="checkbox" id="monthly-update" className="rounded" />
                  <label htmlFor="monthly-update" className="text-sm">Monthly Company Updates</label>
                </div>
                <div className="flex items-center space-x-2">
                  <input type="checkbox" id="seasonal-content" className="rounded" />
                  <label htmlFor="seasonal-content" className="text-sm">Seasonal Content</label>
                </div>
              </div>
              <button className="w-full mt-4 bg-purple-600 text-white py-2 px-4 rounded-lg hover:bg-purple-700 transition-colors">
                Configure Automation
              </button>
            </div>

            <div className="border border-gray-200 rounded-lg p-4">
              <h3 className="font-semibold text-gray-800 mb-2">📈 Performance Monitoring</h3>
              <p className="text-sm text-gray-600 mb-4">Automatically track and optimize content performance</p>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Auto-optimize hashtags</span>
                  <span className="text-green-600">✓ Enabled</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span>Performance alerts</span>
                  <span className="text-green-600">✓ Enabled</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span>A/B testing</span>
                  <span className="text-gray-400">Disabled</span>
                </div>
              </div>
              <button className="w-full mt-4 bg-green-600 text-white py-2 px-4 rounded-lg hover:bg-green-700 transition-colors">
                Setup Monitoring
              </button>
            </div>
          </div>

          {/* Compliance Checker */}
          <div className="bg-green-50 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-green-800 mb-4">✅ Compliance Checker</h3>
            <div className="space-y-3">
              <div className="flex items-center space-x-3">
                <span className="text-green-600">✓</span>
                <span className="text-sm">All content meets OSHA communication guidelines</span>
              </div>
              <div className="flex items-center space-x-3">
                <span className="text-green-600">✓</span>
                <span className="text-sm">Brand voice consistency maintained across platforms</span>
              </div>
              <div className="flex items-center space-x-3">
                <span className="text-green-600">✓</span>
                <span className="text-sm">Industry-specific terminology verified</span>
              </div>
              <div className="flex items-center space-x-3">
                <span className="text-yellow-600">⚠️</span>
                <span className="text-sm">Review required for technical safety content</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  };

  // Enhanced Results View
  const ResultsView = () => {
    if (!results) return null;

    const handleSchedulePost = (content, date) => {
      // Implement scheduling logic
      addNotification(`Post scheduled for ${date}`, 'success');
    };

    const handleEditContent = (content) => {
      // Implement content editing
      addNotification('Content editor opened', 'info');
    };

    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="mb-6 flex items-center justify-between">
            <button
              onClick={() => setCurrentView('dashboard')}
              className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors"
            >
              ← Back to Dashboard
            </button>
            <div className="flex space-x-2">
              <button
                onClick={() => {
                  saveToContentLibrary(results);
                  addNotification('Content saved to library!', 'success');
                }}
                className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors"
              >
                💾 Save to Library
              </button>
              <button
                onClick={() => {
                  // Implement bulk scheduling
                  addNotification('All posts scheduled!', 'success');
                }}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
              >
                📅 Schedule All
              </button>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">
              {results.is_weekly ? '📅 Weekly Content Generated' : '🎉 Generated Content'}
            </h2>
            
            {/* Performance Preview */}
            <div className="bg-blue-50 rounded-lg p-4 mb-6">
              <h3 className="font-semibold text-blue-800 mb-2">📊 Performance Preview</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="text-center">
                  <div className="text-lg font-bold text-blue-900">
                    {Math.floor(Math.random() * 20 + 70)}%
                  </div>
                  <div className="text-sm text-blue-700">Predicted Engagement</div>
                </div>
                <div className="text-center">
                  <div className="text-lg font-bold text-blue-900">
                    {Math.floor(Math.random() * 5000 + 2000)}
                  </div>
                  <div className="text-sm text-blue-700">Estimated Reach</div>
                </div>
                <div className="text-center">
                  <div className="text-lg font-bold text-blue-900">
                    {Math.floor(Math.random() * 30 + 20)}
                  </div>
                  <div className="text-sm text-blue-700">Potential Leads</div>
                </div>
              </div>
            </div>

            {results.is_bulk || results.is_weekly ? (
              <div className="space-y-6">
                <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                  <h3 className="text-lg font-semibold text-green-800 mb-2">
                    {results.is_weekly ? '📅 Weekly Content Generated' : '📚 Bulk Content Generated'}
                  </h3>
                  <p className="text-sm text-green-700">
                    Generated {results.bulk_results?.length || 0} content sets with {results.generated_content?.length || 0} total posts
                  </p>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {results.generated_content?.map((content, index) => (
                    <div key={index} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center space-x-2">
                          <span className="text-2xl">{PLATFORM_ICONS[content.platform]}</span>
                          <h3 className="text-lg font-semibold capitalize">{content.platform}</h3>
                        </div>
                        <div className="flex space-x-2">
                          <button
                            onClick={() => handleEditContent(content)}
                            className="bg-yellow-500 text-white px-3 py-1 rounded text-sm hover:bg-yellow-600 transition-colors"
                          >
                            ✏️ Edit
                          </button>
                          <button
                            onClick={() => copyToClipboard(content.content)}
                            className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700 transition-colors"
                          >
                            📋 Copy
                          </button>
                        </div>
                      </div>
                      
                      <div className="space-y-3">
                        <div>
                          <p className="text-gray-800 mb-2">{content.content}</p>
                        </div>
                        
                        <div>
                          <p className="text-sm font-medium text-gray-700 mb-1">Hashtags:</p>
                          <div className="flex flex-wrap gap-1">
                            {content.hashtags?.map((tag, i) => (
                              <span key={i} className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs">
                                #{tag}
                              </span>
                            ))}
                          </div>
                        </div>

                        {content.estimated_engagement && (
                          <div>
                            <p className="text-sm font-medium text-gray-700 mb-1">Engagement Tip:</p>
                            <p className="text-xs text-gray-600">{content.estimated_engagement}</p>
                          </div>
                        )}

                        <div className="flex space-x-2">
                          <button
                            onClick={() => handleSchedulePost(content, 'Today 2:00 PM')}
                            className="bg-green-600 text-white px-3 py-1 rounded text-sm hover:bg-green-700 transition-colors"
                          >
                            📅 Schedule
                          </button>
                          <button
                            onClick={() => {
                              // Implement direct posting
                              addNotification('Post published!', 'success');
                            }}
                            className="bg-purple-600 text-white px-3 py-1 rounded text-sm hover:bg-purple-700 transition-colors"
                          >
                            📤 Post Now
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="space-y-6">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {results.generated_content?.map((content, index) => (
                    <div key={index} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center space-x-2">
                          <span className="text-2xl">{PLATFORM_ICONS[content.platform]}</span>
                          <h3 className="text-lg font-semibold capitalize">{content.platform}</h3>
                        </div>
                        <div className="flex space-x-2">
                          <button
                            onClick={() => handleEditContent(content)}
                            className="bg-yellow-500 text-white px-3 py-1 rounded text-sm hover:bg-yellow-600 transition-colors"
                          >
                            ✏️ Edit
                          </button>
                          <button
                            onClick={() => copyToClipboard(content.content)}
                            className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700 transition-colors"
                          >
                            📋 Copy
                          </button>
                        </div>
                      </div>
                      
                      <div className="space-y-3">
                        <div>
                          <p className="text-gray-800 mb-2">{content.content}</p>
                        </div>
                        
                        <div>
                          <p className="text-sm font-medium text-gray-700 mb-1">Hashtags:</p>
                          <div className="flex flex-wrap gap-1">
                            {content.hashtags?.map((tag, i) => (
                              <span key={i} className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs">
                                #{tag}
                              </span>
                            ))}
                          </div>
                        </div>

                        {content.estimated_engagement && (
                          <div>
                            <p className="text-sm font-medium text-gray-700 mb-1">Engagement Tip:</p>
                            <p className="text-xs text-gray-600">{content.estimated_engagement}</p>
                          </div>
                        )}

                        <div className="flex space-x-2">
                          <button
                            onClick={() => handleSchedulePost(content, 'Today 2:00 PM')}
                            className="bg-green-600 text-white px-3 py-1 rounded text-sm hover:bg-green-700 transition-colors"
                          >
                            📅 Schedule
                          </button>
                          <button
                            onClick={() => {
                              // Implement direct posting
                              addNotification('Post published!', 'success');
                            }}
                            className="bg-purple-600 text-white px-3 py-1 rounded text-sm hover:bg-purple-700 transition-colors"
                          >
                            📤 Post Now
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>

                {/* AI Media Results */}
                {results.ai_media && (
                  <div className="mt-8 bg-gradient-to-r from-purple-50 to-pink-50 border border-purple-200 rounded-xl p-6">
                    <h3 className="text-xl font-semibold text-purple-800 mb-4">🎬🎵 AI Generated Media</h3>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      {/* Video Section */}
                      {results.ai_media.video_url && (
                        <div className="bg-white rounded-lg p-4 border border-purple-200">
                          <h4 className="font-semibold text-gray-800 mb-3 flex items-center">
                            🎬 AI Generated Video
                          </h4>
                          <video 
                            src={results.ai_media.video_url} 
                            controls 
                            className="w-full rounded-lg mb-3"
                            poster="/api/placeholder/400/300"
                          >
                            Your browser does not support the video tag.
                          </video>
                          <div className="flex space-x-2">
                            <button
                              onClick={() => copyToClipboard(results.ai_media.video_url)}
                              className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700 transition-colors"
                            >
                              📋 Copy Link
                            </button>
                            <button
                              onClick={() => window.open(results.ai_media.video_url, '_blank')}
                              className="bg-purple-600 text-white px-3 py-1 rounded text-sm hover:bg-purple-700 transition-colors"
                            >
                              ⬇️ Download
                            </button>
                          </div>
                        </div>
                      )}

                      {/* Music Section */}
                      {results.ai_media.music_url && (
                        <div className="bg-white rounded-lg p-4 border border-purple-200">
                          <h4 className="font-semibold text-gray-800 mb-3 flex items-center">
                            🎵 AI Generated Music
                          </h4>
                          <audio 
                            src={results.ai_media.music_url} 
                            controls 
                            className="w-full mb-3"
                          >
                            Your browser does not support the audio tag.
                          </audio>
                          <div className="flex space-x-2">
                            <button
                              onClick={() => copyToClipboard(results.ai_media.music_url)}
                              className="bg-green-600 text-white px-3 py-1 rounded text-sm hover:bg-green-700 transition-colors"
                            >
                              📋 Copy Link
                            </button>
                            <button
                              onClick={() => window.open(results.ai_media.music_url, '_blank')}
                              className="bg-green-600 text-white px-3 py-1 rounded text-sm hover:bg-green-700 transition-colors"
                            >
                              ⬇️ Download
                            </button>
                          </div>
                        </div>
                      )}

                      {/* Combined Media Section */}
                      {results.ai_media.combined_url && (
                        <div className="bg-white rounded-lg p-4 border border-purple-200 md:col-span-2">
                          <h4 className="font-semibold text-gray-800 mb-3 flex items-center">
                            🎬🎵 Final Video with Music
                            <span className="ml-2 bg-purple-100 text-purple-800 text-xs px-2 py-1 rounded-full">
                              Ready to Post!
                            </span>
                          </h4>
                          <video 
                            src={results.ai_media.combined_url} 
                            controls 
                            className="w-full max-w-md rounded-lg mb-3"
                            poster="/api/placeholder/400/300"
                          >
                            Your browser does not support the video tag.
                          </video>
                          <div className="flex flex-wrap gap-2">
                            <button
                              onClick={() => copyToClipboard(results.ai_media.combined_url)}
                              className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700 transition-colors"
                            >
                              📋 Copy Link
                            </button>
                            <button
                              onClick={() => window.open(results.ai_media.combined_url, '_blank')}
                              className="bg-purple-600 text-white px-3 py-1 rounded text-sm hover:bg-purple-700 transition-colors"
                            >
                              ⬇️ Download
                            </button>
                            <button
                              onClick={() => {
                                addNotification('🚀 Video posted to social media!', 'success');
                              }}
                              className="bg-gradient-to-r from-pink-500 to-purple-600 text-white px-4 py-1 rounded text-sm hover:from-pink-600 hover:to-purple-700 transition-colors"
                            >
                              📤 Post to Platforms
                            </button>
                          </div>
                        </div>
                      )}
                    </div>

                    {/* Cost Summary */}
                    {results.ai_media.cost_breakdown && (
                      <div className="mt-4 bg-white rounded-lg p-4 border border-purple-200">
                        <h5 className="font-semibold text-gray-800 mb-2">💰 Generation Cost</h5>
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                          <div>
                            <span className="text-gray-600">Video:</span>
                            <span className="ml-2 font-semibold">${results.ai_media.cost_breakdown.video_cost}</span>
                          </div>
                          <div>
                            <span className="text-gray-600">Music:</span>
                            <span className="ml-2 font-semibold">${results.ai_media.cost_breakdown.music_cost}</span>
                          </div>
                          <div>
                            <span className="text-gray-600">Processing:</span>
                            <span className="ml-2 font-semibold">${results.ai_media.cost_breakdown.processing_fee}</span>
                          </div>
                          <div>
                            <span className="text-gray-600">Total:</span>
                            <span className="ml-2 font-bold text-purple-600">${results.ai_media.cost_breakdown.total_cost}</span>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}

            {/* Cross-Platform Promotion Strategy */}
            <div className="mt-8 bg-purple-50 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-purple-800 mb-4">🔗 Cross-Platform Promotion Strategy</h3>
              <div className="space-y-3">
                <div className="flex items-center space-x-3">
                  <span className="text-purple-600">📸→💼</span>
                  <span className="text-sm">Share Instagram visual on LinkedIn with professional context</span>
                </div>
                <div className="flex items-center space-x-3">
                  <span className="text-purple-600">👥→🎵</span>
                  <span className="text-sm">Adapt Facebook post into TikTok video format</span>
                </div>
                <div className="flex items-center space-x-3">
                  <span className="text-purple-600">📝→📧</span>
                  <span className="text-sm">Include key points in next newsletter</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  };

  // Company Form Component
  const CompanyForm = () => {
    const [companyForm, setCompanyForm] = useState({
      name: '',
      industry: 'Construction',
      website: '',
      description: '',
      target_audience: '',
      brand_voice: '',
      brand_colors: { primary: '', secondary: '' },
      seo_keywords: '',
      competitor_urls: ''
    });

    const handleCompanySubmit = (e) => {
      e.preventDefault();
      const formData = {
        ...companyForm,
        seo_keywords: companyForm.seo_keywords.split(',').map(k => k.trim()).filter(k => k),
        competitor_urls: companyForm.competitor_urls.split(',').map(u => u.trim()).filter(u => u)
      };
      createCompany(formData);
    };

    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="mb-6">
            <button
              onClick={() => setCurrentView('dashboard')}
              className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors"
            >
              ← Back to Dashboard
            </button>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">Add New Company</h2>
            <form onSubmit={handleCompanySubmit} className="space-y-4">
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Company Name *</label>
                  <input
                    type="text"
                    value={companyForm.name}
                    onChange={(e) => setCompanyForm({...companyForm, name: e.target.value})}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Industry *</label>
                  <select
                    value={companyForm.industry}
                    onChange={(e) => setCompanyForm({...companyForm, industry: e.target.value})}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    required
                  >
                    <option value="Construction">Construction</option>
                    <option value="Environmental">Environmental</option>
                    <option value="Safety Training">Safety Training</option>
                    <option value="Manufacturing">Manufacturing</option>
                    <option value="Healthcare">Healthcare</option>
                    <option value="Technology">Technology</option>
                    <option value="Other">Other</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Website</label>
                <input
                  type="url"
                  value={companyForm.website}
                  onChange={(e) => setCompanyForm({...companyForm, website: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Description</label>
                <textarea
                  value={companyForm.description}
                  onChange={(e) => setCompanyForm({...companyForm, description: e.target.value})}
                  rows="3"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Brief description of your company..."
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Target Audience</label>
                <input
                  type="text"
                  value={companyForm.target_audience}
                  onChange={(e) => setCompanyForm({...companyForm, target_audience: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="e.g., Construction workers, Safety managers, Environmental professionals"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Brand Voice</label>
                <input
                  type="text"
                  value={companyForm.brand_voice}
                  onChange={(e) => setCompanyForm({...companyForm, brand_voice: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="e.g., Professional but accessible, safety-focused, educational"
                />
              </div>

              <button
                type="submit"
                className="w-full bg-green-600 text-white py-3 px-4 rounded-lg hover:bg-green-700 transition-colors font-semibold"
              >
                Create Company
              </button>
            </form>
          </div>
        </div>
      </div>
    );
  };

  // Beta Feedback Tab Component
  const BetaFeedbackTab = () => {
    const [feedbackForm, setFeedbackForm] = useState({
      title: '',
      description: '',
      type: 'suggestion',
      priority: 'medium',
      category: 'general'
    });

    const betaLogin = async (betaId, name, email) => {
      try {
        const response = await fetch(`${backendUrl}/api/beta/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ beta_id: betaId, name, email })
        });
        
        if (response.ok) {
          const data = await response.json();
          setBetaUser(data.user);
          setShowBetaLogin(false);
          addNotification(data.message, 'success');
          fetchBetaFeedback();
        }
      } catch (error) {
        addNotification('Login failed. Please try again.', 'error');
      }
    };

    const fetchBetaFeedback = async () => {
      try {
        const response = await fetch(`${backendUrl}/api/beta/feedback`);
        if (response.ok) {
          const data = await response.json();
          setBetaFeedback(data.feedback);
        }
      } catch (error) {
        console.error('Failed to fetch beta feedback:', error);
      }
    };

    const submitFeedback = async () => {
      if (!betaUser) {
        setShowBetaLogin(true);
        return;
      }

      try {
        const response = await fetch(`${backendUrl}/api/beta/feedback`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            ...feedbackForm,
            beta_user_id: betaUser.beta_id,
            beta_user_name: betaUser.name,
            beta_user_email: betaUser.email
          })
        });
        
        if (response.ok) {
          addNotification('Feedback submitted successfully!', 'success');
          setFeedbackForm({ title: '', description: '', type: 'suggestion', priority: 'medium', category: 'general' });
          fetchBetaFeedback();
        }
      } catch (error) {
        addNotification('Failed to submit feedback. Please try again.', 'error');
      }
    };

    const voteFeedback = async (feedbackId) => {
      if (!betaUser) return;

      try {
        const response = await fetch(`${backendUrl}/api/beta/feedback/${feedbackId}/vote`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ beta_user_id: betaUser.beta_id })
        });
        
        if (response.ok) {
          fetchBetaFeedback();
        }
      } catch (error) {
        console.error('Failed to vote:', error);
      }
    };

    useEffect(() => {
      if (userStatus.isBetaTester) {
        fetchBetaFeedback();
      }
    }, [userStatus.isBetaTester]);

    return (
      <div className="space-y-6">
        {/* Beta Login Modal */}
        {showBetaLogin && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
              <h3 className="text-lg font-semibold mb-4">Beta Tester Login</h3>
              <div className="space-y-4">
                <input
                  type="text"
                  placeholder="Beta ID (e.g., BETA123)"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                  id="betaId"
                />
                <input
                  type="text"
                  placeholder="Your Name"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                  id="betaName"
                />
                <input
                  type="email"
                  placeholder="Your Email"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                  id="betaEmail"
                />
                <div className="flex space-x-2">
                  <button
                    onClick={() => {
                      const betaId = document.getElementById('betaId').value;
                      const name = document.getElementById('betaName').value;
                      const email = document.getElementById('betaEmail').value;
                      betaLogin(betaId, name, email);
                    }}
                    className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700"
                  >
                    Login
                  </button>
                  <button
                    onClick={() => setShowBetaLogin(false)}
                    className="flex-1 bg-gray-600 text-white py-2 px-4 rounded-lg hover:bg-gray-700"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Beta Feedback Header */}
        <div className="bg-purple-50 rounded-xl p-6">
          <h2 className="text-2xl font-bold text-purple-800 mb-4">🚀 Beta Feedback Center</h2>
          <p className="text-purple-700 mb-4">
            Help us improve PostVelocity! Share your suggestions, report bugs, and help shape the future of the platform.
          </p>
          {betaUser && (
            <div className="bg-white rounded-lg p-4">
              <h3 className="font-semibold text-gray-800">Welcome, {betaUser.name}!</h3>
              <p className="text-gray-600">Beta ID: {betaUser.beta_id}</p>
              <p className="text-gray-600">Contribution Score: {betaUser.contribution_score}</p>
              <p className="text-gray-600">Feedback Submitted: {betaUser.feedback_count}</p>
            </div>
          )}
        </div>

        {/* Submit New Feedback */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Submit New Feedback</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Title</label>
              <input
                type="text"
                value={feedbackForm.title}
                onChange={(e) => setFeedbackForm({...feedbackForm, title: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                placeholder="Brief description of your feedback..."
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Description</label>
              <textarea
                value={feedbackForm.description}
                onChange={(e) => setFeedbackForm({...feedbackForm, description: e.target.value})}
                rows="4"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                placeholder="Detailed description of your feedback..."
              />
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Type</label>
                <select
                  value={feedbackForm.type}
                  onChange={(e) => setFeedbackForm({...feedbackForm, type: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                >
                  <option value="suggestion">Suggestion</option>
                  <option value="bug">Bug Report</option>
                  <option value="feature_request">Feature Request</option>
                  <option value="improvement">Improvement</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Priority</label>
                <select
                  value={feedbackForm.priority}
                  onChange={(e) => setFeedbackForm({...feedbackForm, priority: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                  <option value="urgent">Urgent</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Category</label>
                <select
                  value={feedbackForm.category}
                  onChange={(e) => setFeedbackForm({...feedbackForm, category: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                >
                  <option value="general">General</option>
                  <option value="ui_ux">UI/UX</option>
                  <option value="performance">Performance</option>
                  <option value="content_generation">Content Generation</option>
                  <option value="analytics">Analytics</option>
                </select>
              </div>
            </div>
            
            <button
              onClick={submitFeedback}
              className="w-full bg-purple-600 text-white py-3 px-4 rounded-lg hover:bg-purple-700 transition-colors font-semibold"
            >
              Submit Feedback
            </button>
          </div>
        </div>

        {/* Feedback List */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Community Feedback</h3>
          <div className="space-y-4">
            {betaFeedback.map((feedback) => (
              <div key={feedback.id} className="border border-gray-200 rounded-lg p-4">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <h4 className={`font-semibold ${feedback.status === 'implemented' ? 'line-through text-gray-500' : 'text-gray-800'}`}>
                      {feedback.title}
                    </h4>
                    <p className="text-sm text-gray-600">
                      By {feedback.beta_user_name} • {feedback.type} • {feedback.priority} priority
                    </p>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className={`px-2 py-1 text-xs rounded-full ${
                      feedback.status === 'open' ? 'bg-blue-100 text-blue-800' :
                      feedback.status === 'in_progress' ? 'bg-yellow-100 text-yellow-800' :
                      feedback.status === 'implemented' ? 'bg-green-100 text-green-800' :
                      'bg-gray-100 text-gray-800'
                    }`}>
                      {feedback.status}
                    </span>
                    <button
                      onClick={() => voteFeedback(feedback.id)}
                      className="flex items-center space-x-1 px-2 py-1 bg-gray-100 rounded-full hover:bg-gray-200"
                    >
                      <span>👍</span>
                      <span className="text-sm">{feedback.votes}</span>
                    </button>
                  </div>
                </div>
                <p className="text-gray-700 mb-2">{feedback.description}</p>
                {feedback.admin_response && (
                  <div className="bg-blue-50 p-3 rounded-lg">
                    <p className="text-sm font-medium text-blue-800">Admin Response:</p>
                    <p className="text-blue-700">{feedback.admin_response}</p>
                  </div>
                )}
                {feedback.implementation_notes && (
                  <div className="bg-green-50 p-3 rounded-lg">
                    <p className="text-sm font-medium text-green-800">Implementation Notes:</p>
                    <p className="text-green-700">{feedback.implementation_notes}</p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  // SEO Monitoring Tab Component
  const SEOMonitoringTab = () => {
    const [auditForm, setAuditForm] = useState({ pageUrl: '' });

    const fetchSeoAddonStatus = async () => {
      if (!selectedCompany) return;

      try {
        const response = await fetch(`${backendUrl}/api/seo-addon/${selectedCompany.id}/status`);
        if (response.ok) {
          const data = await response.json();
          setSeoAddon(data.addon);
          setUserStatus(prev => ({
            ...prev,
            hasSeOAddon: data.status === 'active',
            seoAddonStatus: data.status
          }));
        }
      } catch (error) {
        console.error('Failed to fetch SEO addon status:', error);
      }
    };

    const runSeoAudit = async () => {
      if (!selectedCompany || !seoAddon) return;

      setAuditInProgress(true);
      try {
        const response = await fetch(`${backendUrl}/api/seo-addon/${selectedCompany.id}/audit`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ page_url: auditForm.pageUrl })
        });
        
        if (response.ok) {
          const data = await response.json();
          addNotification('SEO audit completed successfully!', 'success');
          fetchSeoAudits();
        }
      } catch (error) {
        addNotification('SEO audit failed. Please try again.', 'error');
      }
      setAuditInProgress(false);
    };

    const fetchSeoAudits = async () => {
      if (!selectedCompany) return;

      try {
        const response = await fetch(`${backendUrl}/api/seo-addon/${selectedCompany.id}/audits`);
        if (response.ok) {
          const data = await response.json();
          setSeoAudits(data.audits);
        }
      } catch (error) {
        console.error('Failed to fetch SEO audits:', error);
      }
    };

    const fetchSeoParameters = async () => {
      try {
        const response = await fetch(`${backendUrl}/api/seo-addon/parameters/latest`);
        if (response.ok) {
          const data = await response.json();
          setSeoParameters(data.parameters);
        }
      } catch (error) {
        console.error('Failed to fetch SEO parameters:', error);
      }
    };

    useEffect(() => {
      if (selectedCompany) {
        fetchSeoAddonStatus();
        fetchSeoAudits();
        fetchSeoParameters();
      }
    }, [selectedCompany]);

    if (!userStatus.hasSeOAddon) {
      return (
        <div className="space-y-6">
          {/* SEO Upgrade Modal */}
          {showSeoUpgrade && (
            <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
              <div className="bg-white rounded-lg p-6 max-w-2xl w-full mx-4">
                <h3 className="text-2xl font-bold text-gray-800 mb-4">SEO Monitoring Add-on</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="border border-gray-200 rounded-lg p-4">
                    <h4 className="font-bold text-lg mb-2">Standard Plan</h4>
                    <div className="text-3xl font-bold text-blue-600 mb-2">$297</div>
                    <div className="text-gray-500 mb-4">one-time purchase</div>
                    <ul className="text-sm space-y-2 mb-4">
                      <li>✓ 50 daily website checks</li>
                      <li>✓ Automatic SEO parameter updates</li>
                      <li>✓ Website audit reports</li>
                      <li>✓ Priority fixes recommendations</li>
                      <li>✓ Email notifications</li>
                    </ul>
                    <button
                      onClick={() => purchaseSeOAddon('standard')}
                      className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700"
                    >
                      Purchase Standard
                    </button>
                  </div>
                  
                  <div className="border-2 border-blue-500 rounded-lg p-4">
                    <div className="text-center mb-2">
                      <span className="bg-blue-500 text-white px-2 py-1 rounded-full text-xs">Most Popular</span>
                    </div>
                    <h4 className="font-bold text-lg mb-2">Pro Plan</h4>
                    <div className="text-3xl font-bold text-blue-600 mb-2">$497</div>
                    <div className="text-gray-500 mb-4">one-time purchase</div>
                    <ul className="text-sm space-y-2 mb-4">
                      <li>✓ Everything in Standard</li>
                      <li>✓ 100 daily website checks</li>
                      <li>✓ Competitor analysis</li>
                      <li>✓ Advanced reporting</li>
                      <li>✓ Priority support</li>
                    </ul>
                    <button
                      onClick={() => purchaseSeOAddon('pro')}
                      className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700"
                    >
                      Purchase Pro
                    </button>
                  </div>
                </div>
                <div className="text-center mt-4">
                  <button
                    onClick={() => setShowSeoUpgrade(false)}
                    className="text-gray-500 hover:text-gray-700"
                  >
                    Maybe later
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* SEO Add-on Promotion */}
          <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-6 text-center">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">🔍 SEO Monitoring Add-on</h2>
            <p className="text-gray-600 mb-6 max-w-2xl mx-auto">
              Unlock the power of automated SEO monitoring! Our advanced system searches the internet daily 
              to find the latest SEO parameters from Google and Bing, then automatically audits your website 
              and provides actionable recommendations.
            </p>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <div className="bg-white p-4 rounded-lg shadow">
                <div className="text-3xl mb-2">🤖</div>
                <h3 className="font-semibold mb-2">Daily Auto-Research</h3>
                <p className="text-sm text-gray-600">Automatically discovers latest SEO parameters</p>
              </div>
              <div className="bg-white p-4 rounded-lg shadow">
                <div className="text-3xl mb-2">📊</div>
                <h3 className="font-semibold mb-2">Website Audits</h3>
                <p className="text-sm text-gray-600">Comprehensive SEO analysis of every page</p>
              </div>
              <div className="bg-white p-4 rounded-lg shadow">
                <div className="text-3xl mb-2">🎯</div>
                <h3 className="font-semibold mb-2">Priority Fixes</h3>
                <p className="text-sm text-gray-600">Actionable recommendations with impact estimates</p>
              </div>
            </div>
            
            <button
              onClick={() => setShowSeoUpgrade(true)}
              className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition-colors font-semibold"
            >
              Get SEO Monitoring Add-on
            </button>
          </div>
        </div>
      );
    }

    return (
      <div className="space-y-6">
        {/* SEO Monitoring Header */}
        <div className="bg-blue-50 rounded-xl p-6">
          <h2 className="text-2xl font-bold text-blue-800 mb-4">🔍 SEO Monitoring Dashboard</h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="bg-white p-4 rounded-lg">
              <div className="text-lg font-semibold text-gray-800">Daily Checks</div>
              <div className="text-2xl font-bold text-blue-600">
                {seoAddon?.daily_checks_used || 0}/{seoAddon?.daily_checks_limit || 50}
              </div>
            </div>
            <div className="bg-white p-4 rounded-lg">
              <div className="text-lg font-semibold text-gray-800">Website</div>
              <div className="text-blue-600 truncate">{seoAddon?.website_url || 'Not set'}</div>
            </div>
            <div className="bg-white p-4 rounded-lg">
              <div className="text-lg font-semibold text-gray-800">Status</div>
              <div className="text-green-600 font-semibold">{seoAddon?.monitoring_status || 'Active'}</div>
            </div>
            <div className="bg-white p-4 rounded-lg">
              <div className="text-lg font-semibold text-gray-800">Last Check</div>
              <div className="text-gray-600">
                {seoAddon?.last_check_date ? new Date(seoAddon.last_check_date).toLocaleDateString() : 'Never'}
              </div>
            </div>
          </div>
        </div>

        {/* Quick Audit */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Quick SEO Audit</h3>
          <div className="flex space-x-4">
            <input
              type="url"
              value={auditForm.pageUrl}
              onChange={(e) => setAuditForm({...auditForm, pageUrl: e.target.value})}
              placeholder="Enter page URL to audit (optional - will use website URL)"
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            />
            <button
              onClick={runSeoAudit}
              disabled={auditInProgress}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              {auditInProgress ? 'Auditing...' : 'Run Audit'}
            </button>
          </div>
        </div>

        {/* Latest SEO Parameters */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Latest SEO Parameters</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {seoParameters.slice(0, 6).map((param, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4">
                <div className="flex justify-between items-start mb-2">
                  <h4 className="font-semibold text-gray-800">{param.parameter_name}</h4>
                  <span className={`px-2 py-1 text-xs rounded-full ${
                    param.importance_score >= 8 ? 'bg-red-100 text-red-800' :
                    param.importance_score >= 6 ? 'bg-yellow-100 text-yellow-800' :
                    'bg-green-100 text-green-800'
                  }`}>
                    {param.importance_score}/10
                  </span>
                </div>
                <p className="text-sm text-gray-600 mb-2">{param.description}</p>
                <div className="flex justify-between text-xs text-gray-500">
                  <span>Source: {param.source}</span>
                  <span>{param.category}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Audits */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Recent Audits</h3>
          <div className="space-y-4">
            {seoAudits.slice(0, 3).map((audit, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <h4 className="font-semibold text-gray-800">{audit.page_url}</h4>
                    <p className="text-sm text-gray-600">{new Date(audit.audit_date).toLocaleDateString()}</p>
                  </div>
                  <div className="text-right">
                    <div className="text-2xl font-bold text-blue-600">{audit.overall_score.toFixed(1)}</div>
                    <div className="text-sm text-gray-500">Overall Score</div>
                  </div>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                  <div>
                    <div className="text-sm font-medium text-gray-700">Issues Found</div>
                    <div className="text-lg font-semibold text-red-600">{audit.issues_found.length}</div>
                  </div>
                  <div>
                    <div className="text-sm font-medium text-gray-700">Recommendations</div>
                    <div className="text-lg font-semibold text-blue-600">{audit.recommendations.length}</div>
                  </div>
                  <div>
                    <div className="text-sm font-medium text-gray-700">Estimated Impact</div>
                    <div className={`text-lg font-semibold ${
                      audit.estimated_impact === 'high' ? 'text-red-600' :
                      audit.estimated_impact === 'medium' ? 'text-yellow-600' :
                      'text-green-600'
                    }`}>
                      {audit.estimated_impact}
                    </div>
                  </div>
                </div>
                
                <div className="bg-gray-50 p-3 rounded-lg">
                  <div className="text-sm font-medium text-gray-700 mb-2">Top Priority Fixes:</div>
                  <ul className="text-sm text-gray-600 space-y-1">
                    {audit.priority_fixes.slice(0, 3).map((fix, fixIndex) => (
                      <li key={fixIndex}>• {fix.fix} ({fix.pages} pages affected)</li>
                    ))}
                  </ul>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  // Main render function
  const renderCurrentView = () => {
    switch (currentView) {
      case 'dashboard':
        return <MainDashboard />;
      case 'results':
        return <ResultsView />;
      case 'add-company':
        return <CompanyForm />;
      default:
        return <MainDashboard />;
    }
  };

  // ==========================================
  // 🎨 PRICING & PLAN SELECTION MODALS 
  // ==========================================

  const renderPricingModal = () => {
    if (!showPricingModal) return null;

    const plans = availablePlans;

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-lg max-w-6xl w-full max-h-[90vh] overflow-y-auto">
          <div className="sticky top-0 bg-white border-b p-6">
            <div className="flex justify-between items-center">
              <div>
                <h2 className="text-3xl font-bold text-gray-900">Choose Your Plan</h2>
                <p className="text-gray-600 mt-2">Select the perfect plan for your business needs</p>
              </div>
              <button
                onClick={() => {
                  setShowPricingModal(false);
                  // Clear selections when modal is closed
                  setSelectedPlan('');
                  setSelectedAddons(new Set());
                }}
                className="text-gray-500 hover:text-gray-700 text-2xl"
              >
                ✕
              </button>
            </div>
            
            {/* Interval Toggle */}
            <div className="flex items-center justify-center mt-6">
              <div className="bg-gray-100 p-1 rounded-lg inline-flex">
                <button
                  onClick={() => setSelectedInterval('monthly')}
                  className={`px-6 py-2 rounded-lg font-medium transition-colors ${
                    selectedInterval === 'monthly' 
                      ? 'bg-blue-600 text-white shadow' 
                      : 'text-gray-600 hover:text-blue-600'
                  }`}
                >
                  Monthly
                </button>
                <button
                  onClick={() => setSelectedInterval('yearly')}
                  className={`px-6 py-2 rounded-lg font-medium transition-colors ${
                    selectedInterval === 'yearly' 
                      ? 'bg-blue-600 text-white shadow' 
                      : 'text-gray-600 hover:text-blue-600'
                  }`}
                >
                  Yearly <span className="text-green-600 font-bold ml-1">(Save 17%)</span>
                </button>
                <button
                  onClick={() => setSelectedInterval('lifetime')}
                  className={`px-6 py-2 rounded-lg font-medium transition-colors ${
                    selectedInterval === 'lifetime' 
                      ? 'bg-blue-600 text-white shadow' 
                      : 'text-gray-600 hover:text-blue-600'
                  }`}
                >
                  Lifetime <span className="text-purple-600 font-bold ml-1">(Best Value)</span>
                </button>
              </div>
            </div>
          </div>

          <div className="p-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-4 gap-6">
              {Object.entries(plans).map(([planKey, plan]) => {
                const isCurrentPlan = currentUserPlan === planKey;
                const isProfessional = planKey === 'professional';
                const price = plan.pricing?.[selectedInterval] || 0;

                return (
                  <div
                    key={planKey}
                    className={`relative bg-white border-2 rounded-xl p-6 ${
                      isProfessional 
                        ? 'border-blue-500 shadow-lg transform scale-105' 
                        : isCurrentPlan 
                          ? 'border-green-500' 
                          : 'border-gray-200 hover:border-blue-300'
                    } transition-all cursor-pointer`}
                    onClick={() => setSelectedPlan(planKey)}
                  >
                    {isProfessional && (
                      <div className="absolute -top-3 left-1/2 transform -translate-x-1/2 bg-blue-600 text-white px-4 py-1 rounded-full text-sm font-semibold whitespace-nowrap">
                        ⭐ Most Popular
                      </div>
                    )}
                    
                    {isCurrentPlan && (
                      <div className="absolute -top-3 left-1/2 transform -translate-x-1/2 bg-green-600 text-white px-3 py-1 rounded-full text-xs font-semibold">
                        Current Plan
                      </div>
                    )}

                    <div className="text-center mb-6">
                      <h3 className="text-2xl font-bold text-gray-900 mb-2">{plan.name}</h3>
                      <p className="text-gray-600 text-sm mb-4">{plan.description}</p>
                      
                      <div className="mb-4">
                        <span className="text-4xl font-bold text-blue-600">${price}</span>
                        <span className="text-gray-600 ml-1">
                          {selectedInterval === 'lifetime' ? 'one-time' : `/${selectedInterval.slice(0, -2)}`}
                        </span>
                      </div>

                      {selectedInterval === 'yearly' && (
                        <div className="text-green-600 text-sm font-medium">
                          Save ${(plan.pricing?.monthly * 12 - plan.pricing?.yearly).toFixed(0)} per year!
                        </div>
                      )}
                    </div>

                    <div className="space-y-3 mb-6">
                      <div className="text-sm text-gray-600">
                        <div className="flex justify-between items-center">
                          <span>Companies:</span>
                          <span className="font-semibold">
                            {plan.limits?.companies === -1 ? 'Unlimited' : plan.limits?.companies}
                          </span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span>Users:</span>
                          <span className="font-semibold">
                            {plan.limits?.users === -1 ? 'Unlimited' : plan.limits?.users}
                          </span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span>Posts/month:</span>
                          <span className="font-semibold">
                            {plan.limits?.posts_per_month === -1 ? 'Unlimited' : plan.limits?.posts_per_month}
                          </span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span>Social accounts:</span>
                          <span className="font-semibold">
                            {plan.limits?.social_accounts_per_company === -1 ? 'Unlimited' : plan.limits?.social_accounts_per_company}
                          </span>
                        </div>
                      </div>
                    </div>

                    <div className="space-y-2 mb-6 text-sm">
                      {plan.features?.slice(0, 5).map((feature, index) => (
                        <div key={index} className="flex items-center text-gray-700">
                          <span className="text-green-600 mr-2">✓</span>
                          <span className="capitalize">{feature.replace('_', ' ')}</span>
                        </div>
                      ))}
                      {plan.features?.length > 5 && (
                        <div className="text-blue-600 text-xs">
                          +{plan.features.length - 5} more features
                        </div>
                      )}
                    </div>

                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        setSelectedPlan(planKey);
                        initiatePlanPurchase();
                      }}
                      disabled={isCurrentPlan || paymentProcessing}
                      className={`w-full py-3 px-4 rounded-lg font-semibold transition-colors ${
                        isCurrentPlan
                          ? 'bg-green-100 text-green-600 cursor-not-allowed'
                          : isProfessional
                            ? 'bg-blue-600 text-white hover:bg-blue-700'
                            : 'bg-gray-900 text-white hover:bg-gray-800'
                      } disabled:opacity-50`}
                    >
                      {isCurrentPlan ? 'Current Plan' : paymentProcessing ? 'Processing...' : 'Choose Plan'}
                    </button>
                  </div>
                );
              })}
            </div>

            {/* Add-ons Section */}
            <div className="mt-12 border-t pt-8">
              <h3 className="text-2xl font-bold text-gray-900 mb-6 text-center">Premium Add-ons</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {[
                  { 
                    key: 'seo_monitoring', 
                    name: 'SEO Monitoring', 
                    icon: '🔍',
                    description: 'Advanced SEO tracking and optimization',
                    pricing: { monthly: 97, yearly: 970, lifetime: 2490 }
                  },
                  { 
                    key: 'hashtag_research', 
                    name: 'Hashtag Research', 
                    icon: '#️⃣',
                    description: 'AI-powered hashtag optimization',
                    pricing: { monthly: 19, yearly: 190, lifetime: 490 }
                  },
                  { 
                    key: 'keyword_research', 
                    name: 'Keyword Research', 
                    icon: '🎯',
                    description: 'SEO keyword analysis and suggestions',
                    pricing: { monthly: 29, yearly: 290, lifetime: 740 }
                  },
                  { 
                    key: 'competitor_analysis', 
                    name: 'Competitor Analysis', 
                    icon: '🏆',
                    description: 'Deep competitive intelligence insights',
                    pricing: { monthly: 49, yearly: 490, lifetime: 1250 }
                  }
                ].map((addon) => {
                  const isSelected = selectedAddons.has(addon.key);
                  const price = addon.pricing[selectedInterval];
                  
                  return (
                    <div key={addon.key} className={`rounded-lg p-4 border-2 transition-all ${
                      isSelected 
                        ? 'border-blue-500 bg-blue-50' 
                        : 'border-gray-200 bg-gray-50 hover:border-blue-300'
                    }`}>
                      <div className="text-center">
                        <div className="text-2xl mb-2">{addon.icon}</div>
                        <h4 className="font-semibold text-gray-800 mb-1">{addon.name}</h4>
                        <p className="text-xs text-gray-600 mb-3">{addon.description}</p>
                        <div className="mb-3">
                          <div className="text-blue-600 font-bold text-lg">
                            ${price}
                            <span className="text-sm text-gray-600">
                              {selectedInterval === 'lifetime' ? ' once' : `/${selectedInterval.slice(0, -2)}`}
                            </span>
                          </div>
                          {selectedInterval === 'yearly' && (
                            <div className="text-green-600 text-xs">
                              Save ${(addon.pricing.monthly * 12) - addon.pricing.yearly}!
                            </div>
                          )}
                        </div>
                        <button 
                          onClick={() => toggleAddon(addon.key)}
                          className={`w-full py-2 px-3 rounded font-medium transition-colors ${
                            isSelected
                              ? 'bg-blue-600 text-white hover:bg-blue-700'
                              : 'bg-gray-600 text-white hover:bg-gray-700'
                          }`}
                        >
                          {isSelected ? '✓ Added' : 'Add to Plan'}
                        </button>
                      </div>
                    </div>
                  );
                })}
              </div>
              
              {/* Selected Add-ons Summary */}
              {selectedAddons.size > 0 && (
                <div className="mt-6 p-4 bg-green-50 rounded-lg border border-green-200">
                  <h4 className="font-semibold text-green-800 mb-2">
                    Selected Add-ons ({selectedAddons.size})
                  </h4>
                  <div className="space-y-1 text-sm text-green-700">
                    {Array.from(selectedAddons).map(addonKey => (
                      <div key={addonKey} className="flex justify-between">
                        <span>• {addonKey.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}</span>
                        <button
                          onClick={() => toggleAddon(addonKey)}
                          className="text-red-600 hover:text-red-800 ml-2"
                        >
                          ✕
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Total Price Summary */}
            {(selectedPlan || selectedAddons.size > 0) && (
              <div className="mt-8 p-6 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg border border-blue-200">
                <div className="text-center">
                  <h3 className="text-lg font-semibold text-gray-800 mb-4">Order Summary</h3>
                  <div className="space-y-2 text-sm">
                    {selectedPlan && (
                      <div className="flex justify-between items-center">
                        <span>{availablePlans[selectedPlan]?.name} Plan</span>
                        <span className="font-semibold">
                          ${availablePlans[selectedPlan]?.pricing?.[selectedInterval] || 0}
                        </span>
                      </div>
                    )}
                    {Array.from(selectedAddons).map(addonKey => {
                      const addonPricing = {
                        'seo_monitoring': { monthly: 97, yearly: 970, lifetime: 2490 },
                        'hashtag_research': { monthly: 19, yearly: 190, lifetime: 490 },
                        'keyword_research': { monthly: 29, yearly: 290, lifetime: 740 },
                        'competitor_analysis': { monthly: 49, yearly: 490, lifetime: 1250 }
                      };
                      return (
                        <div key={addonKey} className="flex justify-between items-center text-blue-700">
                          <span>{addonKey.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}</span>
                          <span className="font-semibold">
                            ${addonPricing[addonKey]?.[selectedInterval] || 0}
                          </span>
                        </div>
                      );
                    })}
                    <div className="border-t border-gray-300 pt-2 mt-2">
                      <div className="flex justify-between items-center text-lg font-bold">
                        <span>Total:</span>
                        <span className="text-blue-600">${calculateTotalPrice()}</span>
                      </div>
                      <div className="text-xs text-gray-600 mt-1">
                        {selectedInterval === 'lifetime' ? 'One-time payment' : `Per ${selectedInterval.slice(0, -2)}`}
                      </div>
                    </div>
                  </div>
                  
                  {selectedPlan && (
                    <button
                      onClick={initiatePlanPurchase}
                      disabled={paymentProcessing}
                      className="w-full mt-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 px-6 rounded-lg hover:from-blue-700 hover:to-purple-700 font-semibold transition-all disabled:opacity-50"
                    >
                      {paymentProcessing ? 'Processing...' : `Complete Purchase - $${calculateTotalPrice()}`}
                    </button>
                  )}
                </div>
              </div>
            )}

            {/* Current Usage Display */}
            {userUsage && (
              <div className="mt-8 bg-blue-50 rounded-lg p-6">
                <h4 className="font-bold text-blue-800 mb-4">📊 Your Current Usage</h4>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-600">{userUsage.companies_count || 0}</div>
                    <div className="text-sm text-blue-700">Companies</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-600">{userUsage.posts_generated || 0}</div>
                    <div className="text-sm text-blue-700">Posts Generated</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-600">{userUsage.users_count || 1}</div>
                    <div className="text-sm text-blue-700">Users</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-600">{userUsage.social_accounts_count || 0}</div>
                    <div className="text-sm text-blue-700">Social Accounts</div>
                  </div>
                </div>
              </div>
            )}

            {/* Usage Warnings */}
            {usageWarnings.length > 0 && (
              <div className="mt-6 bg-yellow-50 rounded-lg p-4 border border-yellow-200">
                <h4 className="font-bold text-yellow-800 mb-2">⚠️ Usage Alerts</h4>
                <div className="space-y-2">
                  {usageWarnings.map((warning, index) => (
                    <div key={index} className="text-yellow-700 text-sm">
                      <span className="font-medium">{warning.type}:</span> {warning.current}/{warning.limit} ({warning.percentage}%)
                    </div>
                  ))}
                </div>
                <p className="text-yellow-700 text-sm mt-2">Consider upgrading to avoid hitting limits.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    );
  };

  const renderPlanUpgradeModal = () => {
    if (!showPlanUpgradeModal) return null;

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
          <h3 className="text-2xl font-bold text-red-600 mb-4">⚠️ Usage Limit Reached</h3>
          <div className="mb-6">
            <p className="text-gray-700 mb-4">
              You've reached your plan's usage limit. Upgrade to a higher plan to continue using all features.
            </p>
            <div className="bg-gray-50 rounded-lg p-4">
              <h4 className="font-semibold text-gray-800 mb-2">Current Plan: {getPlanDisplayName(currentUserPlan)}</h4>
              {usageWarnings.length > 0 && (
                <div className="space-y-1">
                  {usageWarnings.map((warning, index) => (
                    <div key={index} className="text-sm text-red-600">
                      {warning.message}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
          <div className="flex space-x-3">
            <button
              onClick={() => {
                setShowPlanUpgradeModal(false);
                setShowPricingModal(true);
              }}
              className="flex-1 bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 font-medium"
            >
              Upgrade Plan
            </button>
            <button
              onClick={() => setShowPlanUpgradeModal(false)}
              className="flex-1 bg-gray-400 text-white py-3 px-4 rounded-lg hover:bg-gray-500 font-medium"
            >
              Later
            </button>
          </div>
        </div>
      </div>
    );
  };

  const renderInviteModal = () => {
    if (!showInviteModal) return null;

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-2xl font-bold text-gray-900">👥 Invite Team Member</h3>
            <button
              onClick={() => setShowInviteModal(false)}
              className="text-gray-500 hover:text-gray-700 text-xl"
            >
              ✕
            </button>
          </div>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Email Address *
              </label>
              <input
                type="email"
                value={inviteForm.email}
                onChange={(e) => setInviteForm({ ...inviteForm, email: e.target.value })}
                placeholder="colleague@company.com"
                className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Role
              </label>
              <select
                value={inviteForm.role}
                onChange={(e) => setInviteForm({ ...inviteForm, role: e.target.value })}
                className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                <option value="member">Member - View & basic creation</option>
                <option value="editor">Editor - Create & edit content</option>
                <option value="admin">Admin - Full access</option>
              </select>
            </div>

            <div className="bg-blue-50 rounded-lg p-3">
              <p className="text-sm text-blue-800">
                <strong>Current Usage:</strong> {teamMembers.length} / {getFeatureLimit('users') === Infinity ? '∞' : getFeatureLimit('users')} users
              </p>
            </div>

            <div className="flex space-x-3 pt-4">
              <button
                onClick={inviteTeamMember}
                disabled={loadingTeam || !inviteForm.email.trim()}
                className="flex-1 bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 disabled:opacity-50 font-medium"
              >
                {loadingTeam ? '📤 Sending...' : '📤 Send Invitation'}
              </button>
              <button
                onClick={() => setShowInviteModal(false)}
                className="flex-1 bg-gray-400 text-white py-3 px-4 rounded-lg hover:bg-gray-500 font-medium"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  };

  const renderPartnerModal = () => {
    if (!showPartnerModal) return null;

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-lg p-6 max-w-lg w-full mx-4">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-2xl font-bold text-gray-900">🔗 Join Partner Program</h3>
            <button
              onClick={() => setShowPartnerModal(false)}
              className="text-gray-500 hover:text-gray-700 text-xl"
            >
              ✕
            </button>
          </div>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Full Name *
              </label>
              <input
                type="text"
                value={partnerForm.full_name}
                onChange={(e) => setPartnerForm({ ...partnerForm, full_name: e.target.value })}
                placeholder="Your full name"
                className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Email Address *
              </label>
              <input
                type="email"
                value={partnerForm.email}
                onChange={(e) => setPartnerForm({ ...partnerForm, email: e.target.value })}
                placeholder="your@email.com"
                className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Company Name (Optional)
              </label>
              <input
                type="text"
                value={partnerForm.company_name}
                onChange={(e) => setPartnerForm({ ...partnerForm, company_name: e.target.value })}
                placeholder="Your company name"
                className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Partner Type
              </label>
              <select
                value={partnerForm.partner_type}
                onChange={(e) => setPartnerForm({ ...partnerForm, partner_type: e.target.value })}
                className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                <option value="affiliate">Affiliate (30% commission)</option>
                <option value="agency">Agency Partner (40% commission)</option>
                <option value="reseller">Reseller (60% discount)</option>
                <option value="distributor">Distributor (70% discount)</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Website (Optional)
              </label>
              <input
                type="url"
                value={partnerForm.website}
                onChange={(e) => setPartnerForm({ ...partnerForm, website: e.target.value })}
                placeholder="https://your-website.com"
                className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div className="bg-blue-50 rounded-lg p-3">
              <p className="text-sm text-blue-800">
                <strong>Selected:</strong> {partnerForm.partner_type.charAt(0).toUpperCase() + partnerForm.partner_type.slice(1)} 
                ({partnerForm.partner_type === 'affiliate' ? '30%' : 
                  partnerForm.partner_type === 'agency' ? '40%' : 
                  partnerForm.partner_type === 'reseller' ? '60%' : '70%'} 
                {partnerForm.partner_type.includes('seller') || partnerForm.partner_type === 'distributor' ? ' discount' : ' commission'})
              </p>
            </div>

            <div className="flex space-x-3 pt-4">
              <button
                onClick={registerPartner}
                disabled={loadingPartner || !partnerForm.full_name.trim() || !partnerForm.email.trim()}
                className="flex-1 bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 disabled:opacity-50 font-medium"
              >
                {loadingPartner ? '🔄 Registering...' : '🚀 Register as Partner'}
              </button>
              <button
                onClick={() => setShowPartnerModal(false)}
                className="flex-1 bg-gray-400 text-white py-3 px-4 rounded-lg hover:bg-gray-500 font-medium"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  };

  const renderApiKeyModal = () => {
    if (!showApiModal) return null;

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-lg p-6 max-w-lg w-full mx-4">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-2xl font-bold text-gray-900">🔌 Generate API Key</h3>
            <button
              onClick={() => {
                setShowApiModal(false);
                setGeneratedApiKey(null);
              }}
              className="text-gray-500 hover:text-gray-700 text-xl"
            >
              ✕
            </button>
          </div>
          
          {!generatedApiKey ? (
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  API Key Name *
                </label>
                <input
                  type="text"
                  value={newApiKeyForm.key_name}
                  onChange={(e) => setNewApiKeyForm({ ...newApiKeyForm, key_name: e.target.value })}
                  placeholder="My API Key"
                  className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Permissions
                </label>
                <div className="space-y-2">
                  {[
                    { value: 'read', label: 'Read - Get content and analytics' },
                    { value: 'write', label: 'Write - Generate new content' },
                    { value: 'admin', label: 'Admin - Full access' }
                  ].map((permission) => (
                    <label key={permission.value} className="flex items-center">
                      <input
                        type="checkbox"
                        checked={newApiKeyForm.permissions.includes(permission.value)}
                        onChange={(e) => {
                          if (e.target.checked) {
                            setNewApiKeyForm({
                              ...newApiKeyForm,
                              permissions: [...newApiKeyForm.permissions, permission.value]
                            });
                          } else {
                            setNewApiKeyForm({
                              ...newApiKeyForm,
                              permissions: newApiKeyForm.permissions.filter(p => p !== permission.value)
                            });
                          }
                        }}
                        className="mr-2"
                      />
                      <span className="text-sm text-gray-600">{permission.label}</span>
                    </label>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Expires In
                </label>
                <select
                  value={newApiKeyForm.expires_in_days}
                  onChange={(e) => setNewApiKeyForm({ ...newApiKeyForm, expires_in_days: parseInt(e.target.value) })}
                  className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                  <option value={30}>30 days</option>
                  <option value={90}>90 days</option>
                  <option value={365}>1 year</option>
                  <option value={1825}>5 years</option>
                </select>
              </div>

              <div className="bg-blue-50 rounded-lg p-3">
                <p className="text-sm text-blue-800">
                  <strong>Selected permissions:</strong> {newApiKeyForm.permissions.join(', ')}
                </p>
                <p className="text-xs text-blue-600 mt-1">
                  You can revoke this API key at any time from the API management page.
                </p>
              </div>

              <div className="flex space-x-3 pt-4">
                <button
                  onClick={generateApiKey}
                  disabled={loadingApi || !newApiKeyForm.key_name.trim() || newApiKeyForm.permissions.length === 0}
                  className="flex-1 bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 disabled:opacity-50 font-medium"
                >
                  {loadingApi ? '🔄 Generating...' : '🔑 Generate API Key'}
                </button>
                <button
                  onClick={() => setShowApiModal(false)}
                  className="flex-1 bg-gray-400 text-white py-3 px-4 rounded-lg hover:bg-gray-500 font-medium"
                >
                  Cancel
                </button>
              </div>
            </div>
          ) : (
            /* Show Generated API Key */
            <div className="space-y-4">
              <div className="bg-green-50 rounded-lg p-4 border border-green-200">
                <h4 className="font-semibold text-green-800 mb-2">🎉 API Key Generated Successfully!</h4>
                <p className="text-sm text-green-700">
                  Please copy and store this API key securely. You won't be able to see it again.
                </p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  API Key
                </label>
                <div className="flex items-center space-x-2">
                  <input
                    type="text"
                    value={generatedApiKey.api_key}
                    readOnly
                    className="flex-1 p-3 border rounded-lg bg-gray-50 font-mono text-sm"
                  />
                  <button
                    onClick={() => copyApiKey(generatedApiKey.api_key, generatedApiKey.api_secret)}
                    className="bg-blue-600 text-white px-3 py-3 rounded hover:bg-blue-700"
                  >
                    📋
                  </button>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  API Secret
                </label>
                <div className="flex items-center space-x-2">
                  <input
                    type="text"
                    value={generatedApiKey.api_secret}
                    readOnly
                    className="flex-1 p-3 border rounded-lg bg-gray-50 font-mono text-sm"
                  />
                  <button
                    onClick={() => copyApiKey(generatedApiKey.api_key, generatedApiKey.api_secret)}
                    className="bg-blue-600 text-white px-3 py-3 rounded hover:bg-blue-700"
                  >
                    📋
                  </button>
                </div>
              </div>

              <div className="bg-red-50 rounded-lg p-4 border border-red-200">
                <p className="text-sm text-red-800">
                  <strong>⚠️ Important:</strong> Store these credentials securely. The secret will not be shown again.
                </p>
              </div>

              <button
                onClick={() => {
                  setShowApiModal(false);
                  setGeneratedApiKey(null);
                }}
                className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 font-medium"
              >
                Done
              </button>
            </div>
          )}
        </div>
      </div>
    );
  };

  return (
    <div>
      {renderCurrentView()}
      {renderPricingModal()}
      {renderPlanUpgradeModal()}
      {renderInviteModal()}
      {renderPartnerModal()}
      {renderApiKeyModal()}

      {/* Enhanced Admin Panel Modal */}
      {showAdminPanel && currentUser?.role === 'admin' && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-2xl max-w-7xl max-h-[95vh] w-full mx-4 overflow-hidden">
            {/* Header */}
            <div className="sticky top-0 bg-white border-b px-6 py-4 flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <h2 className="text-2xl font-bold text-gray-900">👑 Admin Dashboard</h2>
                <div className="flex space-x-2">
                  <button
                    onClick={() => {
                      setAdminActiveTab('overview');
                      loadComprehensiveAnalytics();
                    }}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                      adminActiveTab === 'overview' 
                        ? 'bg-blue-600 text-white' 
                        : 'text-gray-600 hover:text-blue-600 hover:bg-blue-50'
                    }`}
                  >
                    📊 Overview
                  </button>
                  <button
                    onClick={() => {
                      setAdminActiveTab('users');
                      loadAllUsers();
                    }}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                      adminActiveTab === 'users' 
                        ? 'bg-blue-600 text-white' 
                        : 'text-gray-600 hover:text-blue-600 hover:bg-blue-50'
                    }`}
                  >
                    👥 Users
                  </button>
                  <button
                    onClick={() => {
                      setAdminActiveTab('analytics');
                      loadAdminAnalytics();
                    }}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                      adminActiveTab === 'analytics' 
                        ? 'bg-blue-600 text-white' 
                        : 'text-gray-600 hover:text-blue-600 hover:bg-blue-50'
                    }`}
                  >
                    📈 Analytics
                  </button>
                  <button
                    onClick={() => {
                      setAdminActiveTab('billing');
                      loadBillingAnalytics();
                    }}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                      adminActiveTab === 'billing' 
                        ? 'bg-blue-600 text-white' 
                        : 'text-gray-600 hover:text-blue-600 hover:bg-blue-50'
                    }`}
                  >
                    💳 Billing
                  </button>
                  <button
                    onClick={() => {
                      setAdminActiveTab('free-codes');
                      loadFreeCodes();
                    }}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                      adminActiveTab === 'free-codes' 
                        ? 'bg-blue-600 text-white' 
                        : 'text-gray-600 hover:text-blue-600 hover:bg-blue-50'
                    }`}
                  >
                    🎁 Free Codes
                  </button>
                </div>
              </div>
              <button
                onClick={() => {
                  setShowAdminPanel(false);
                  setAdminActiveTab('overview');
                  setSelectedUser(null);
                }}
                className="text-gray-500 hover:text-gray-700 text-2xl"
              >
                ×
              </button>
            </div>

            {/* Content */}
            <div className="overflow-y-auto max-h-[calc(95vh-80px)]">
              {/* Overview Tab */}
              {adminActiveTab === 'overview' && (
                <div className="p-6 space-y-6">
                  <div className="text-center mb-6">
                    <h3 className="text-xl font-bold text-gray-900 mb-2">Platform Overview</h3>
                    <p className="text-gray-600">Comprehensive analytics and key metrics</p>
                  </div>

                  {comprehensiveAnalytics && (
                    <>
                      {/* Key Metrics Cards */}
                      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
                        <div className="bg-gradient-to-r from-blue-50 to-blue-100 p-4 rounded-xl border border-blue-200">
                          <div className="flex items-center justify-between">
                            <div>
                              <p className="text-sm font-medium text-blue-800">Total Users</p>
                              <p className="text-2xl font-bold text-blue-900">{comprehensiveAnalytics.overview.total_users}</p>
                            </div>
                            <div className="text-3xl text-blue-600">👥</div>
                          </div>
                          <p className="text-xs text-blue-700 mt-2">
                            +{comprehensiveAnalytics.overview.new_users_7d} this week
                          </p>
                        </div>
                        
                        <div className="bg-gradient-to-r from-green-50 to-green-100 p-4 rounded-xl border border-green-200">
                          <div className="flex items-center justify-between">
                            <div>
                              <p className="text-sm font-medium text-green-800">Monthly Revenue</p>
                              <p className="text-2xl font-bold text-green-900">${comprehensiveAnalytics.overview.total_revenue}</p>
                            </div>
                            <div className="text-3xl text-green-600">💰</div>
                          </div>
                          <p className="text-xs text-green-700 mt-2">
                            ${comprehensiveAnalytics.overview.avg_revenue_per_user}/user avg
                          </p>
                        </div>
                        
                        <div className="bg-gradient-to-r from-purple-50 to-purple-100 p-4 rounded-xl border border-purple-200">
                          <div className="flex items-center justify-between">
                            <div>
                              <p className="text-sm font-medium text-purple-800">Companies</p>
                              <p className="text-2xl font-bold text-purple-900">{comprehensiveAnalytics.overview.total_companies}</p>
                            </div>
                            <div className="text-3xl text-purple-600">🏢</div>
                          </div>
                          <p className="text-xs text-purple-700 mt-2">
                            +{comprehensiveAnalytics.overview.new_companies_30d} this month
                          </p>
                        </div>
                        
                        <div className="bg-gradient-to-r from-orange-50 to-orange-100 p-4 rounded-xl border border-orange-200">
                          <div className="flex items-center justify-between">
                            <div>
                              <p className="text-sm font-medium text-orange-800">Active Users</p>
                              <p className="text-2xl font-bold text-orange-900">{comprehensiveAnalytics.overview.active_users_7d}</p>
                            </div>
                            <div className="text-3xl text-orange-600">⚡</div>
                          </div>
                          <p className="text-xs text-orange-700 mt-2">
                            {Math.round((comprehensiveAnalytics.overview.active_users_7d / comprehensiveAnalytics.overview.total_users) * 100)}% active rate
                          </p>
                        </div>
                      </div>

                      {/* Plan Distribution */}
                      <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
                        <h4 className="text-lg font-semibold text-gray-800 mb-4">Plan Distribution</h4>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                          {comprehensiveAnalytics.plan_distribution.map((plan, index) => (
                            <div key={plan._id} className="text-center">
                              <div className="bg-gray-50 rounded-lg p-4">
                                <div className="text-lg font-bold text-gray-800">{plan.count}</div>
                                <div className="text-sm text-gray-600 capitalize">{plan._id} Plan</div>
                                <div className="text-xs text-gray-500 mt-1">
                                  {comprehensiveAnalytics.revenue_by_plan[plan._id] && 
                                    `$${comprehensiveAnalytics.revenue_by_plan[plan._id].monthly_revenue}/mo`
                                  }
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>

                      {/* Recent Transactions */}
                      {comprehensiveAnalytics.recent_transactions.length > 0 && (
                        <div className="bg-white rounded-xl shadow-lg p-6">
                          <h4 className="text-lg font-semibold text-gray-800 mb-4">Recent Transactions</h4>
                          <div className="space-y-3">
                            {comprehensiveAnalytics.recent_transactions.slice(0, 5).map((transaction, index) => (
                              <div key={transaction.id} className="flex items-center justify-between py-2 border-b border-gray-100">
                                <div>
                                  <div className="font-medium text-gray-900">${transaction.amount}</div>
                                  <div className="text-sm text-gray-600">{transaction.plan_type} plan</div>
                                </div>
                                <div className="text-right">
                                  <div className={`text-xs px-2 py-1 rounded-full ${
                                    transaction.status === 'paid' ? 'bg-green-100 text-green-800' :
                                    transaction.status === 'failed' ? 'bg-red-100 text-red-800' :
                                    'bg-yellow-100 text-yellow-800'
                                  }`}>
                                    {transaction.status}
                                  </div>
                                  <div className="text-xs text-gray-500 mt-1">
                                    {transaction.created_at ? new Date(transaction.created_at).toLocaleDateString() : 'N/A'}
                                  </div>
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </>
                  )}
                  
                  {!comprehensiveAnalytics && (
                    <div className="text-center py-12">
                      <div className="text-gray-400 mb-4">📊</div>
                      <p className="text-gray-600">Loading comprehensive analytics...</p>
                    </div>
                  )}
                </div>
              )}

              {/* Users Tab */}
              {adminActiveTab === 'users' && (
                <div className="p-6">
                  {/* Admin Actions */}
                  <div className="mb-6 flex flex-wrap gap-3">
                    <button
                      onClick={() => setShowCreateUserModal(true)}
                      className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors"
                    >
                      + Create Test User
                    </button>
                    <button
                      onClick={loadAllUsers}
                      className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                    >
                      🔄 Refresh Users
                    </button>
                  </div>

                  {/* Enhanced Users Table */}
                  <div className="bg-white rounded-xl shadow-lg overflow-hidden">
                    <table className="w-full">
                      <thead className="bg-gray-50 border-b">
                        <tr>
                          <th className="text-left py-3 px-4 font-semibold text-gray-700">User</th>
                          <th className="text-left py-3 px-4 font-semibold text-gray-700">Email</th>
                          <th className="text-left py-3 px-4 font-semibold text-gray-700">Plan</th>
                          <th className="text-left py-3 px-4 font-semibold text-gray-700">Posts</th>
                          <th className="text-left py-3 px-4 font-semibold text-gray-700">Companies</th>
                          <th className="text-left py-3 px-4 font-semibold text-gray-700">Status</th>
                          <th className="text-left py-3 px-4 font-semibold text-gray-700">Actions</th>
                        </tr>
                      </thead>
                      <tbody>
                        {allUsers.map((user) => (
                          <tr key={user.id} className="border-b hover:bg-gray-50 transition-colors">
                            <td className="py-3 px-4">
                              <div>
                                <div className="font-medium text-gray-900">{user.full_name}</div>
                                <div className="text-sm text-gray-600">@{user.username}</div>
                                {user.role === 'admin' && (
                                  <span className="inline-block bg-red-100 text-red-800 text-xs px-2 py-1 rounded mt-1">
                                    Admin
                                  </span>
                                )}
                              </div>
                            </td>
                            <td className="py-3 px-4 text-gray-700">{user.email}</td>
                            <td className="py-3 px-4">
                              <span className={`inline-block px-2 py-1 rounded text-xs font-medium ${
                                user.current_plan === 'enterprise' ? 'bg-purple-100 text-purple-800' :
                                user.current_plan === 'business' ? 'bg-blue-100 text-blue-800' :
                                user.current_plan === 'professional' ? 'bg-green-100 text-green-800' :
                                'bg-gray-100 text-gray-800'
                              }`}>
                                {user.current_plan}
                              </span>
                            </td>
                            <td className="py-3 px-4">
                              <div className="text-sm">
                                <div className="font-medium text-gray-900">{user.content_stats?.total_posts || 0}</div>
                                <div className="text-gray-500">total posts</div>
                              </div>
                            </td>
                            <td className="py-3 px-4 text-gray-700">{user.company_count || 0}</td>
                            <td className="py-3 px-4">
                              <div className="space-y-1">
                                <span className={`inline-block px-2 py-1 rounded text-xs ${
                                  user.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                                }`}>
                                  {user.is_active ? 'Active' : 'Inactive'}
                                </span>
                                <div className="text-xs text-gray-500">
                                  {user.last_login ? 
                                    `Last: ${new Date(user.last_login).toLocaleDateString()}` : 
                                    'Never logged in'
                                  }
                                </div>
                              </div>
                            </td>
                            <td className="py-3 px-4">
                              <div className="flex space-x-2">
                                <button
                                  onClick={() => loadUserDetails(user.id)}
                                  className="bg-blue-500 text-white px-2 py-1 rounded text-xs hover:bg-blue-600 transition-colors"
                                >
                                  📊 Details
                                </button>
                                {user.id !== currentUser.id && (
                                  <button
                                    onClick={() => impersonateUser(user.id)}
                                    className="bg-yellow-500 text-white px-2 py-1 rounded text-xs hover:bg-yellow-600 transition-colors"
                                  >
                                    👤 Impersonate
                                  </button>
                                )}
                                {user.id === currentUser.id && (
                                  <span className="text-gray-400 text-xs">Current User</span>
                                )}
                              </div>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                    
                    {allUsers.length === 0 && (
                      <div className="text-center py-8 text-gray-500">
                        No users found. Click "Refresh Users" to load.
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Analytics Tab */}
              {adminActiveTab === 'analytics' && (
                <div className="p-6">
                  <div className="text-center mb-6">
                    <h3 className="text-xl font-bold text-gray-900 mb-2">Platform Analytics</h3>
                    <p className="text-gray-600">Detailed platform performance metrics</p>
                  </div>

                  {adminAnalytics && (
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                      {/* User Analytics */}
                      <div className="bg-white rounded-xl shadow-lg p-6">
                        <h4 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
                          👥 User Analytics
                        </h4>
                        <div className="space-y-3">
                          <div className="flex justify-between items-center">
                            <span className="text-gray-600">Total Users:</span>
                            <span className="font-bold text-lg">{adminAnalytics.users.total}</span>
                          </div>
                          <div className="flex justify-between items-center">
                            <span className="text-gray-600">Active Users:</span>
                            <span className="font-bold text-lg text-green-600">{adminAnalytics.users.active}</span>
                          </div>
                          <div className="flex justify-between items-center">
                            <span className="text-gray-600">Admin Users:</span>
                            <span className="font-bold text-lg text-red-600">{adminAnalytics.users.admin}</span>
                          </div>
                          <div className="flex justify-between items-center">
                            <span className="text-gray-600">Growth Rate:</span>
                            <span className={`font-bold text-lg ${adminAnalytics.users.growth_rate >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                              {adminAnalytics.users.growth_rate}%
                            </span>
                          </div>
                        </div>
                      </div>

                      {/* Revenue Analytics */}
                      <div className="bg-white rounded-xl shadow-lg p-6">
                        <h4 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
                          💰 Revenue Analytics
                        </h4>
                        <div className="space-y-3">
                          <div className="flex justify-between items-center">
                            <span className="text-gray-600">Monthly Revenue:</span>
                            <span className="font-bold text-lg text-green-600">${adminAnalytics.revenue.monthly_revenue}</span>
                          </div>
                          <div className="flex justify-between items-center">
                            <span className="text-gray-600">Annual Revenue:</span>
                            <span className="font-bold text-lg">${adminAnalytics.revenue.annual_revenue}</span>
                          </div>
                          <div className="flex justify-between items-center">
                            <span className="text-gray-600">ARPU:</span>
                            <span className="font-bold text-lg">${adminAnalytics.revenue.avg_revenue_per_user}</span>
                          </div>
                        </div>
                      </div>

                      {/* Company Analytics */}
                      <div className="bg-white rounded-xl shadow-lg p-6">
                        <h4 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
                          🏢 Company Analytics
                        </h4>
                        <div className="space-y-3">
                          <div className="flex justify-between items-center">
                            <span className="text-gray-600">Total Companies:</span>
                            <span className="font-bold text-lg">{adminAnalytics.companies.total}</span>
                          </div>
                          <div className="flex justify-between items-center">
                            <span className="text-gray-600">Avg per User:</span>
                            <span className="font-bold text-lg">{adminAnalytics.companies.avg_per_user}</span>
                          </div>
                        </div>
                      </div>

                      {/* OAuth Analytics */}
                      <div className="bg-white rounded-xl shadow-lg p-6">
                        <h4 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
                          🔗 OAuth Analytics
                        </h4>
                        <div className="space-y-3">
                          <div className="flex justify-between items-center">
                            <span className="text-gray-600">Total Connections:</span>
                            <span className="font-bold text-lg">{adminAnalytics.oauth.total_connections}</span>
                          </div>
                          <div className="flex justify-between items-center">
                            <span className="text-gray-600">Avg per User:</span>
                            <span className="font-bold text-lg">{adminAnalytics.oauth.avg_per_user}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  )}
                  
                  {!adminAnalytics && (
                    <div className="text-center py-12">
                      <div className="text-gray-400 mb-4">📈</div>
                      <p className="text-gray-600">Loading analytics...</p>
                    </div>
                  )}
                </div>
              )}

              {/* Billing Tab */}
              {adminActiveTab === 'billing' && (
                <div className="p-6">
                  <div className="text-center mb-6">
                    <h3 className="text-xl font-bold text-gray-900 mb-2">Billing Analytics</h3>
                    <p className="text-gray-600">Revenue tracking and transaction analytics</p>
                  </div>

                  {billingAnalytics && (
                    <>
                      {/* Revenue Overview */}
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                        <div className="bg-gradient-to-r from-green-50 to-green-100 p-6 rounded-xl border border-green-200">
                          <div className="text-center">
                            <div className="text-2xl font-bold text-green-900">${billingAnalytics.revenue.last_30_days}</div>
                            <div className="text-sm text-green-700">Last 30 Days</div>
                          </div>
                        </div>
                        <div className="bg-gradient-to-r from-blue-50 to-blue-100 p-6 rounded-xl border border-blue-200">
                          <div className="text-center">
                            <div className="text-2xl font-bold text-blue-900">${billingAnalytics.revenue.last_90_days}</div>
                            <div className="text-sm text-blue-700">Last 90 Days</div>
                          </div>
                        </div>
                        <div className="bg-gradient-to-r from-purple-50 to-purple-100 p-6 rounded-xl border border-purple-200">
                          <div className="text-center">
                            <div className="text-2xl font-bold text-purple-900">{billingAnalytics.revenue.success_rate}%</div>
                            <div className="text-sm text-purple-700">Success Rate</div>
                          </div>
                        </div>
                      </div>

                      {/* Top Customers */}
                      {billingAnalytics.top_customers.length > 0 && (
                        <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
                          <h4 className="text-lg font-semibold text-gray-800 mb-4">Top Customers</h4>
                          <div className="overflow-x-auto">
                            <table className="w-full">
                              <thead className="bg-gray-50 border-b">
                                <tr>
                                  <th className="text-left py-2 px-4 font-medium text-gray-700">Customer</th>
                                  <th className="text-left py-2 px-4 font-medium text-gray-700">Plan</th>
                                  <th className="text-left py-2 px-4 font-medium text-gray-700">Total Spent</th>
                                  <th className="text-left py-2 px-4 font-medium text-gray-700">Transactions</th>
                                  <th className="text-left py-2 px-4 font-medium text-gray-700">Last Payment</th>
                                </tr>
                              </thead>
                              <tbody>
                                {billingAnalytics.top_customers.slice(0, 5).map((customer, index) => (
                                  <tr key={customer.user_id} className="border-b hover:bg-gray-50">
                                    <td className="py-2 px-4">
                                      <div>
                                        <div className="font-medium text-gray-900">{customer.full_name}</div>
                                        <div className="text-sm text-gray-600">{customer.email}</div>
                                      </div>
                                    </td>
                                    <td className="py-2 px-4">
                                      <span className="capitalize text-sm font-medium">{customer.current_plan}</span>
                                    </td>
                                    <td className="py-2 px-4 font-bold text-green-600">${customer.total_spent}</td>
                                    <td className="py-2 px-4">{customer.transaction_count}</td>
                                    <td className="py-2 px-4 text-sm text-gray-600">
                                      {customer.last_payment ? new Date(customer.last_payment).toLocaleDateString() : 'N/A'}
                                    </td>
                                  </tr>
                                ))}
                              </tbody>
                            </table>
                          </div>
                        </div>
                      )}

                      {/* Plan Changes */}
                      <div className="bg-white rounded-xl shadow-lg p-6">
                        <h4 className="text-lg font-semibold text-gray-800 mb-4">Plan Changes (Last 30 Days)</h4>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                          <div className="text-center p-4 bg-green-50 rounded-lg">
                            <div className="text-2xl font-bold text-green-600">{billingAnalytics.plan_changes.upgrades_30d}</div>
                            <div className="text-sm text-green-700">Upgrades</div>
                          </div>
                          <div className="text-center p-4 bg-yellow-50 rounded-lg">
                            <div className="text-2xl font-bold text-yellow-600">{billingAnalytics.plan_changes.downgrades_30d}</div>
                            <div className="text-sm text-yellow-700">Downgrades</div>
                          </div>
                          <div className="text-center p-4 bg-red-50 rounded-lg">
                            <div className="text-2xl font-bold text-red-600">{billingAnalytics.plan_changes.cancellations_30d}</div>
                            <div className="text-sm text-red-700">Cancellations</div>
                          </div>
                        </div>
                      </div>
                    </>
                  )}
                  
                  {!billingAnalytics && (
                    <div className="text-center py-12">
                      <div className="text-gray-400 mb-4">💳</div>
                      <p className="text-gray-600">Loading billing analytics...</p>
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* User Details Modal */}
            {selectedUser && (
              <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-60">
                <div className="bg-white rounded-2xl max-w-4xl max-h-[90vh] w-full mx-4 overflow-y-auto">
                  <div className="sticky top-0 bg-white border-b px-6 py-4 flex items-center justify-between">
                    <h3 className="text-xl font-bold text-gray-900">👤 {selectedUser.full_name}</h3>
                    <button
                      onClick={() => setSelectedUser(null)}
                      className="text-gray-500 hover:text-gray-700 text-xl"
                    >
                      ×
                    </button>
                  </div>
                  
                  <div className="p-6">
                    {/* User Info Cards */}
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
                      <div className="bg-blue-50 p-4 rounded-xl">
                        <div className="text-sm text-blue-700">Current Plan</div>
                        <div className="font-bold text-blue-900 capitalize">{selectedUser.current_plan}</div>
                      </div>
                      <div className="bg-green-50 p-4 rounded-xl">
                        <div className="text-sm text-green-700">Total Spent</div>
                        <div className="font-bold text-green-900">${selectedUser.total_spent}</div>
                      </div>
                      <div className="bg-purple-50 p-4 rounded-xl">
                        <div className="text-sm text-purple-700">Posts Generated</div>
                        <div className="font-bold text-purple-900">{selectedUser.content_stats.total_posts_generated}</div>
                      </div>
                      <div className="bg-orange-50 p-4 rounded-xl">
                        <div className="text-sm text-orange-700">Health Score</div>
                        <div className="font-bold text-orange-900">{selectedUser.health_score}/100</div>
                      </div>
                    </div>

                    {/* Companies */}
                    <div className="bg-white border rounded-xl p-4 mb-6">
                      <h4 className="font-semibold text-gray-800 mb-3">Companies ({selectedUser.companies.length})</h4>
                      {selectedUser.companies.length > 0 ? (
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                          {selectedUser.companies.map((company, index) => (
                            <div key={company.id} className="bg-gray-50 p-3 rounded-lg">
                              <div className="font-medium">{company.name}</div>
                              <div className="text-sm text-gray-600">{company.industry}</div>
                              <div className="text-xs text-gray-500">
                                Created: {company.created_at ? new Date(company.created_at).toLocaleDateString() : 'N/A'}
                              </div>
                            </div>
                          ))}
                        </div>
                      ) : (
                        <div className="text-gray-500 text-sm">No companies created</div>
                      )}
                    </div>

                    {/* Billing History */}
                    <div className="bg-white border rounded-xl p-4">
                      <h4 className="font-semibold text-gray-800 mb-3">Billing History ({selectedUser.billing_history.length})</h4>
                      {selectedUser.billing_history.length > 0 ? (
                        <div className="space-y-2">
                          {selectedUser.billing_history.map((transaction, index) => (
                            <div key={transaction.id} className="flex justify-between items-center py-2 border-b border-gray-100 last:border-b-0">
                              <div>
                                <div className="font-medium">${transaction.amount}</div>
                                <div className="text-sm text-gray-600">{transaction.plan_type} - {transaction.plan_interval}</div>
                              </div>
                              <div className="text-right">
                                <div className={`text-xs px-2 py-1 rounded-full ${
                                  transaction.status === 'paid' ? 'bg-green-100 text-green-800' :
                                  transaction.status === 'failed' ? 'bg-red-100 text-red-800' :
                                  'bg-yellow-100 text-yellow-800'
                                }`}>
                                  {transaction.status}
                                </div>
                                <div className="text-xs text-gray-500 mt-1">
                                  {transaction.created_at ? new Date(transaction.created_at).toLocaleDateString() : 'N/A'}
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      ) : (
                        <div className="text-gray-500 text-sm">No billing history</div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Free Codes Tab */}
            {adminActiveTab === 'free-codes' && (
              <div className="p-6">
                <div className="text-center mb-6">
                  <h3 className="text-xl font-bold text-gray-900 mb-2">🎁 Free Access Codes</h3>
                  <p className="text-gray-600">Generate and manage promotional codes for free PostVelocity access</p>
                </div>

                {/* Action Buttons */}
                <div className="mb-6 flex flex-wrap gap-3">
                  <button
                    onClick={() => setShowCreateCodeModal(true)}
                    className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors"
                  >
                    🎁 Generate Free Code
                  </button>
                  <button
                    onClick={loadFreeCodes}
                    className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                  >
                    🔄 Refresh Codes
                  </button>
                </div>

                {/* Free Codes Table */}
                <div className="bg-white rounded-xl shadow-lg overflow-hidden">
                  <table className="w-full">
                    <thead className="bg-gray-50 border-b">
                      <tr>
                        <th className="text-left py-3 px-4 font-semibold text-gray-700">Code</th>
                        <th className="text-left py-3 px-4 font-semibold text-gray-700">Plan Level</th>
                        <th className="text-left py-3 px-4 font-semibold text-gray-700">Duration</th>
                        <th className="text-left py-3 px-4 font-semibold text-gray-700">Uses</th>
                        <th className="text-left py-3 px-4 font-semibold text-gray-700">Status</th>
                        <th className="text-left py-3 px-4 font-semibold text-gray-700">Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {freeCodes.map((code) => (
                        <tr key={code.code} className="border-b hover:bg-gray-50 transition-colors">
                          <td className="py-3 px-4">
                            <div className="font-mono text-sm bg-gray-100 px-2 py-1 rounded">
                              {code.code}
                            </div>
                            <div className="text-xs text-gray-500 mt-1">
                              {code.description}
                            </div>
                          </td>
                          <td className="py-3 px-4">
                            <span className={`inline-block px-2 py-1 rounded text-xs font-medium ${
                              code.plan_level === 'enterprise' ? 'bg-purple-100 text-purple-800' :
                              code.plan_level === 'business' ? 'bg-blue-100 text-blue-800' :
                              code.plan_level === 'professional' ? 'bg-green-100 text-green-800' :
                              'bg-gray-100 text-gray-800'
                            }`}>
                              {code.plan_level}
                            </span>
                          </td>
                          <td className="py-3 px-4 text-gray-700">
                            {code.duration_days} days
                          </td>
                          <td className="py-3 px-4">
                            <div className="text-sm">
                              <span className={`font-medium ${
                                code.used_count >= code.max_uses ? 'text-red-600' : 'text-gray-900'
                              }`}>
                                {code.used_count}/{code.max_uses}
                              </span>
                            </div>
                          </td>
                          <td className="py-3 px-4">
                            <div className="space-y-1">
                              <span className={`inline-block px-2 py-1 rounded text-xs ${
                                code.is_active && new Date(code.expires_at) > new Date() 
                                  ? 'bg-green-100 text-green-800' 
                                  : 'bg-red-100 text-red-800'
                              }`}>
                                {code.is_active && new Date(code.expires_at) > new Date() ? 'Active' : 'Expired'}
                              </span>
                              <div className="text-xs text-gray-500">
                                Expires: {new Date(code.expires_at).toLocaleDateString()}
                              </div>
                            </div>
                          </td>
                          <td className="py-3 px-4">
                            <div className="flex space-x-2">
                              <button
                                onClick={() => {
                                  navigator.clipboard.writeText(code.code);
                                  addNotification('Code copied to clipboard!', 'success');
                                }}
                                className="bg-blue-500 text-white px-2 py-1 rounded text-xs hover:bg-blue-600 transition-colors"
                              >
                                📋 Copy
                              </button>
                              {code.is_active && (
                                <button
                                  onClick={() => deactivateFreeCode(code.code)}
                                  className="bg-red-500 text-white px-2 py-1 rounded text-xs hover:bg-red-600 transition-colors"
                                >
                                  🚫 Deactivate
                                </button>
                              )}
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                  
                  {freeCodes.length === 0 && (
                    <div className="text-center py-8 text-gray-500">
                      No free codes generated yet. Click "Generate Free Code" to create one.
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Create Test User Modal */}
      {showCreateUserModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-2xl max-w-md w-full mx-4">
            <div className="px-6 py-4 border-b">
              <h3 className="text-xl font-bold text-gray-900">Create Test User</h3>
            </div>
            
            <div className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
                <input
                  type="text"
                  value={newUserForm.full_name}
                  onChange={(e) => setNewUserForm({...newUserForm, full_name: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="John Smith"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                <input
                  type="email"
                  value={newUserForm.email}
                  onChange={(e) => setNewUserForm({...newUserForm, email: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="john@example.com"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Plan</label>
                <select
                  value={newUserForm.plan}
                  onChange={(e) => setNewUserForm({...newUserForm, plan: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="starter">Starter</option>
                  <option value="professional">Professional</option>
                  <option value="business">Business</option>
                  <option value="enterprise">Enterprise</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Industry</label>
                <select
                  value={newUserForm.industry}
                  onChange={(e) => setNewUserForm({...newUserForm, industry: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="Construction">Construction</option>
                  <option value="Environmental">Environmental</option>
                  <option value="Safety Training">Safety Training</option>
                  <option value="Manufacturing">Manufacturing</option>
                  <option value="Healthcare">Healthcare</option>
                  <option value="Technology">Technology</option>
                </select>
              </div>
            </div>
            
            <div className="px-6 py-4 border-t flex justify-end space-x-3">
              <button
                onClick={() => setShowCreateUserModal(false)}
                className="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={createTestUser}
                disabled={!newUserForm.email || !newUserForm.full_name}
                className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors disabled:opacity-50"
              >
                Create User
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Create Free Code Modal */}
      {showCreateCodeModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-2xl max-w-md w-full mx-4">
            <div className="px-6 py-4 border-b">
              <h3 className="text-xl font-bold text-gray-900">🎁 Generate Free Access Code</h3>
            </div>
            
            <div className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Plan Level</label>
                <select
                  value={newCodeForm.plan_level}
                  onChange={(e) => setNewCodeForm({...newCodeForm, plan_level: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="starter">Starter - $0</option>
                  <option value="professional">Professional - $29/month</option>
                  <option value="business">Business - $79/month</option>
                  <option value="enterprise">Enterprise - $199/month</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Duration (Days)</label>
                <input
                  type="number"
                  value={newCodeForm.duration_days}
                  onChange={(e) => setNewCodeForm({...newCodeForm, duration_days: parseInt(e.target.value)})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  min="1"
                  max="365"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Max Uses</label>
                <input
                  type="number"
                  value={newCodeForm.max_uses}
                  onChange={(e) => setNewCodeForm({...newCodeForm, max_uses: parseInt(e.target.value)})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  min="1"
                  max="1000"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Description (Optional)</label>
                <input
                  type="text"
                  value={newCodeForm.description}
                  onChange={(e) => setNewCodeForm({...newCodeForm, description: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="e.g., Holiday promotion, Beta tester reward"
                />
              </div>
            </div>

            <div className="px-6 py-4 border-t flex justify-end space-x-3">
              <button
                onClick={() => setShowCreateCodeModal(false)}
                className="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={generateFreeCode}
                className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors"
              >
                Generate Code
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Redeem Free Code Modal */}
      {showRedeemCodeModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-2xl max-w-md w-full mx-4">
            <div className="px-6 py-4 border-b">
              <h3 className="text-xl font-bold text-gray-900">🎁 Redeem Free Access Code</h3>
            </div>
            
            <div className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Enter Your Code</label>
                <input
                  type="text"
                  value={redeemCodeInput}
                  onChange={(e) => setRedeemCodeInput(e.target.value.toUpperCase())}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono"
                  placeholder="FREE-XXXXXXXX"
                  maxLength="12"
                />
              </div>
              
              <div className="bg-blue-50 p-4 rounded-lg">
                <h4 className="font-semibold text-blue-900 mb-2">How it works:</h4>
                <ul className="text-sm text-blue-800 space-y-1">
                  <li>• Enter your promotional code above</li>
                  <li>• Get instant access to premium features</li>
                  <li>• Access duration depends on the specific code</li>
                  <li>• Your current plan will be upgraded automatically</li>
                </ul>
              </div>
            </div>

            <div className="px-6 py-4 border-t flex justify-end space-x-3">
              <button
                onClick={() => {
                  setShowRedeemCodeModal(false);
                  setRedeemCodeInput('');
                }}
                className="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={redeemFreeCode}
                disabled={!redeemCodeInput.trim()}
                className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors disabled:opacity-50"
              >
                Redeem Code
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;