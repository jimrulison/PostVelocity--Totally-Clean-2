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
  linkedin: '💼'
};

const PLATFORM_COLORS = {
  instagram: 'bg-gradient-to-r from-purple-500 to-pink-500',
  tiktok: 'bg-gradient-to-r from-black to-gray-800',
  facebook: 'bg-blue-600',
  youtube: 'bg-red-600',
  whatsapp: 'bg-green-500',
  snapchat: 'bg-yellow-400',
  x: 'bg-gray-900',
  linkedin: 'bg-blue-700'
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
    { name: 'Equipment Feature', template: 'Spotlight on [EQUIPMENT]: [BENEFITS]. Perfect for [USE_CASE]. #Equipment #Construction' }
  ],
  safety: [
    { name: 'Training Reminder', template: 'Don\'t forget: [TRAINING_TOPIC] training is scheduled for [DATE]. Safety first! #SafetyTraining' },
    { name: 'Compliance Update', template: 'New [REGULATION] requirements: [DETAILS]. Stay compliant! #Compliance #Safety' },
    { name: 'Safety Tip', template: 'Pro tip: [SAFETY_TIP]. Small actions, big impact! #SafetyTips #Prevention' }
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
    generate_blog: false,
    generate_newsletter: false,
    generate_video_script: false,
    use_company_media: true,
    seo_focus: true,
    target_keywords: [],
    repurpose_content: false
  });
  
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
  
  // New state for payment/trial system
  const [userStatus, setUserStatus] = useState({
    isTrialUser: false,
    trialStartDate: null,
    trialDaysRemaining: 0,
    isPaidUser: false,
    subscriptionType: null,
    usageCount: 0,
    trialUsageLimit: 50
  });
  const [showPaymentModal, setShowPaymentModal] = useState(false);
  const [showTrialModal, setShowTrialModal] = useState(false);
  
  // New state for enhanced features
  const [progressStatus, setProgressStatus] = useState(null);
  const [contentLibrary, setContentLibrary] = useState([]);
  const [notifications, setNotifications] = useState([]);
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
  };

  const startFreeTrial = () => {
    const trialStatus = {
      isTrialUser: true,
      trialStartDate: new Date().toISOString(),
      trialDaysRemaining: 7,
      isPaidUser: false,
      subscriptionType: null,
      usageCount: 0,
      trialUsageLimit: 50
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
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      const paidStatus = {
        isTrialUser: false,
        trialStartDate: null,
        trialDaysRemaining: 0,
        isPaidUser: true,
        subscriptionType: plan,
        usageCount: 0,
        trialUsageLimit: 0
      };
      
      setUserStatus(paidStatus);
      localStorage.setItem('userStatus', JSON.stringify(paidStatus));
      setShowPaymentModal(false);
      
      addNotification(`🎉 Welcome to PostVelocity ${plan}! You now have unlimited access.`, 'success');
    } catch (error) {
      addNotification('Payment processing failed. Please try again.', 'error');
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
      const response = await fetch(`${backendUrl}/api/platforms`);
      const data = await response.json();
      setAvailablePlatforms(data.platforms || []);
    } catch (error) {
      console.error('Error fetching platforms:', error);
      setAvailablePlatforms([]);
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

  // Voice Input Feature
  const startVoiceRecording = () => {
    if (!('webkitSpeechRecognition' in window)) {
      addNotification('Voice input not supported in this browser', 'error');
      return;
    }

    const recognition = new window.webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    setIsVoiceRecording(true);

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setFormData(prev => ({ ...prev, topic: transcript }));
      addNotification(`Voice input captured: "${transcript}"`, 'success');
    };

    recognition.onerror = (event) => {
      console.error('Speech recognition error:', event.error);
      addNotification('Voice input failed. Please try again.', 'error');
    };

    recognition.onend = () => {
      setIsVoiceRecording(false);
    };

    recognition.start();
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
    if (!draggedFiles.length || !selectedCompany) return;

    setUploadingMedia(true);
    try {
      const uploadPromises = draggedFiles.map(async (file) => {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('category', 'workplace');
        formData.append('description', `Uploaded via drag and drop: ${file.name}`);
        formData.append('tags', 'drag-drop, auto-upload');
        formData.append('seo_alt_text', `${selectedCompany.name} media - ${file.name}`);

        const response = await fetch(`${backendUrl}/api/companies/${selectedCompany.id}/media/upload`, {
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
              Start your 7-day free trial and experience the power of AI-driven social media management.
            </p>
            <div className="space-y-4">
              <div className="bg-blue-50 rounded-lg p-4">
                <h4 className="font-semibold text-blue-800 mb-2">Free Trial Includes:</h4>
                <ul className="text-sm text-blue-700 space-y-1">
                  <li>• Up to 50 content generations</li>
                  <li>• All AI features unlocked</li>
                  <li>• 8+ platform support</li>
                  <li>• Advanced analytics</li>
                  <li>• No credit card required</li>
                </ul>
              </div>
              <div className="flex space-x-3">
                <button
                  onClick={startFreeTrial}
                  className="flex-1 bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 transition-colors font-semibold"
                >
                  Start Free Trial
                </button>
                <button
                  onClick={() => setShowTrialModal(false)}
                  className="flex-1 bg-gray-200 text-gray-800 py-3 px-4 rounded-lg hover:bg-gray-300 transition-colors"
                >
                  Maybe Later
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  };

  // Payment Modal Component
  const PaymentModal = () => {
    if (!showPaymentModal) return null;

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-xl p-8 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
          <div className="text-center mb-8">
            <div className="text-4xl mb-4">💳</div>
            <h3 className="text-2xl font-bold text-gray-900 mb-2">Upgrade to Continue</h3>
            <p className="text-gray-600">
              {userStatus.isTrialUser ? 'Your trial has expired.' : 'You have reached your trial limit.'} 
              Choose a plan to continue using PostVelocity.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            {/* Pro Plan */}
            <div className="border-2 border-blue-500 rounded-lg p-6 relative">
              <div className="absolute top-0 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
                <div className="bg-blue-500 text-white px-3 py-1 rounded-full text-sm font-bold">
                  MOST POPULAR
                </div>
              </div>
              <div className="text-center">
                <h4 className="text-xl font-bold text-gray-900 mb-2">Pro Plan</h4>
                <div className="text-3xl font-bold text-blue-600 mb-1">$49</div>
                <div className="text-gray-500 mb-4">per month</div>
                <ul className="text-sm text-gray-600 space-y-2 mb-6">
                  <li>✓ Unlimited content generation</li>
                  <li>✓ All AI features</li>
                  <li>✓ 8+ platform support</li>
                  <li>✓ Advanced analytics</li>
                  <li>✓ Up to 5 companies</li>
                  <li>✓ Priority support</li>
                </ul>
                <button
                  onClick={() => processPayment('Pro')}
                  className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition-colors font-semibold"
                >
                  Choose Pro Plan
                </button>
              </div>
            </div>

            {/* Enterprise Plan */}
            <div className="border-2 border-gray-200 rounded-lg p-6">
              <div className="text-center">
                <h4 className="text-xl font-bold text-gray-900 mb-2">Enterprise</h4>
                <div className="text-3xl font-bold text-gray-900 mb-1">$149</div>
                <div className="text-gray-500 mb-4">per month</div>
                <ul className="text-sm text-gray-600 space-y-2 mb-6">
                  <li>✓ Everything in Pro</li>
                  <li>✓ Unlimited companies</li>
                  <li>✓ Custom integrations</li>
                  <li>✓ White-label options</li>
                  <li>✓ Dedicated support</li>
                  <li>✓ Custom training</li>
                </ul>
                <button
                  onClick={() => processPayment('Enterprise')}
                  className="w-full bg-gray-600 text-white py-3 rounded-lg hover:bg-gray-700 transition-colors font-semibold"
                >
                  Choose Enterprise
                </button>
              </div>
            </div>
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

  // Usage Status Component
  const UsageStatus = () => {
    if (userStatus.isPaidUser) {
      return (
        <div className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium">
          {userStatus.subscriptionType} Plan - Unlimited
        </div>
      );
    }
    
    if (userStatus.isTrialUser) {
      return (
        <div className="bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-sm font-medium">
          Trial: {userStatus.trialDaysRemaining} days, {userStatus.trialUsageLimit - userStatus.usageCount} uses left
        </div>
      );
    }
    
    return (
      <div className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium">
        Free User
      </div>
    );
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
        {/* Header */}
        <header className="bg-white shadow-lg border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center py-6">
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2">
                  <span className="text-3xl">🚀</span>
                  <h1 className="text-2xl font-bold text-gray-900">PostVelocity</h1>
                </div>
                {selectedCompany && (
                  <div className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium">
                    {selectedCompany.name}
                  </div>
                )}
                {isOffline && (
                  <div className="bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm font-medium">
                    Offline Mode
                  </div>
                )}
              </div>
              <div className="flex items-center space-x-4">
                <NotificationCenter />
                <button
                  onClick={() => setCurrentView('add-company')}
                  className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors"
                >
                  + Add Company
                </button>
                <button
                  onClick={() => {
                    if (window.confirm('Are you sure you want to clear all companies? This action cannot be undone.')) {
                      clearAllCompanies();
                    }
                  }}
                  className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors"
                >
                  Clear All
                </button>
                <select
                  value={selectedCompany?.id || ''}
                  onChange={(e) => {
                    const company = companies.find(c => c.id === e.target.value);
                    setSelectedCompany(company);
                    setFormData(prev => ({ ...prev, company_id: e.target.value }));
                  }}
                  className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">Select Company</option>
                  {companies.map((company) => (
                    <option key={company.id} value={company.id}>{company.name}</option>
                  ))}
                </select>
              </div>
            </div>
          </div>
        </header>

        {/* Navigation Tabs */}
        <nav className="bg-white border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex space-x-8">
              {[
                { id: 'content-hub', label: 'Content Hub', icon: '📝' },
                { id: 'analytics', label: 'Analytics', icon: '📊' },
                { id: 'media', label: 'Media Library', icon: '📸' },
                { id: 'calendar', label: 'Calendar', icon: '📅' },
                { id: 'automation', label: 'Automation', icon: '🤖' },
                { id: 'training', label: 'Training', icon: '🎓' }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center space-x-2 py-4 px-2 border-b-2 font-medium text-sm ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <span className="text-lg">{tab.icon}</span>
                  <span>{tab.label}</span>
                </button>
              ))}
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
        </main>

        {/* Progress Indicator */}
        <ProgressIndicator status={progressStatus} />

        {/* Success Animation */}
        <SuccessAnimation show={showSuccessAnimation} />
      </div>
    );
  };

  // Content Hub Tab - Enhanced with all new features
  const ContentHubTab = () => {
    const [quickTopic, setQuickTopic] = useState('');
    const [showBulkForm, setShowBulkForm] = useState(false);
    const [bulkTopics, setBulkTopics] = useState('');
    const [showEmergencyForm, setShowEmergencyForm] = useState(false);
    const [showTemplates, setShowTemplates] = useState(false);

    return (
      <div className="space-y-6">
        {/* Smart Quick Actions */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">⚡ Smart Quick Actions</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
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
              <p className="text-sm text-gray-600 mb-3">Speak your topic instead of typing</p>
              <button
                onClick={startVoiceRecording}
                disabled={isVoiceRecording}
                className={`w-full py-2 px-4 rounded-lg transition-colors ${
                  isVoiceRecording 
                    ? 'bg-red-500 text-white animate-pulse' 
                    : 'bg-blue-600 text-white hover:bg-blue-700'
                }`}
              >
                {isVoiceRecording ? 'Recording...' : 'Voice Input'}
              </button>
            </div>
          </div>
        </div>

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
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
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
              <button
                onClick={() => setShowBulkForm(!showBulkForm)}
                className="w-full bg-purple-600 text-white py-2 px-4 rounded-lg hover:bg-purple-700 transition-colors"
              >
                📚 Bulk Content
              </button>
              {showBulkForm && (
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

        {/* Advanced Content Generation */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">🎨 Advanced Content Generation</h3>
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
              <label className="block text-sm font-medium text-gray-700 mb-2">Select Platforms</label>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                {availablePlatforms.map((platform) => (
                  <button
                    key={platform}
                    type="button"
                    onClick={() => handlePlatformToggle(platform)}
                    className={`flex items-center space-x-2 px-4 py-2 rounded-lg border transition-colors ${
                      formData.platforms.includes(platform)
                        ? `${PLATFORM_COLORS[platform]} text-white`
                        : 'border-gray-300 text-gray-700 hover:bg-gray-50'
                    }`}
                  >
                    <span className="text-lg">{PLATFORM_ICONS[platform]}</span>
                    <span className="capitalize">{platform}</span>
                  </button>
                ))}
              </div>
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

            <button
              type="submit"
              disabled={loading || !formData.topic || formData.platforms.length === 0}
              className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-semibold"
            >
              {loading ? 'Generating Content...' : 'Generate Advanced Content'}
            </button>
          </form>
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
        </div>
      </div>
    );
  };

  // Enhanced Media Tab with Drag & Drop
  const MediaTab = () => {
    const [uploadForm, setUploadForm] = useState({
      files: null,
      category: 'training',
      description: '',
      tags: ''
    });

    const handleMediaUpload = async (files, category, description, tags) => {
      if (!selectedCompany) return;
      
      setUploadingMedia(true);
      try {
        const uploadPromises = Array.from(files).map(async (file) => {
          const formData = new FormData();
          formData.append('file', file);
          formData.append('category', category);
          formData.append('description', description);
          formData.append('tags', tags);
          formData.append('seo_alt_text', `${selectedCompany.name} ${category} - ${description}`);

          const response = await fetch(`${backendUrl}/api/companies/${selectedCompany.id}/media/upload`, {
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
        addNotification(`Successfully uploaded ${files.length} file(s)!`, 'success');
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
      handleMediaUpload(uploadForm.files, uploadForm.category, uploadForm.description, uploadForm.tags);
      setUploadForm({ files: null, category: 'training', description: '', tags: '' });
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
            
            {draggedFiles.length > 0 && (
              <div className="mb-4">
                <div className="bg-blue-50 rounded-lg p-3">
                  <p className="text-blue-800 font-medium">
                    {draggedFiles.length} files ready for upload
                  </p>
                  <div className="text-sm text-blue-600 mt-1">
                    {draggedFiles.map((file, index) => (
                      <span key={index}>{file.name}{index < draggedFiles.length - 1 ? ', ' : ''}</span>
                    ))}
                  </div>
                </div>
                <button
                  onClick={uploadDraggedFiles}
                  disabled={uploadingMedia}
                  className="mt-3 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
                >
                  {uploadingMedia ? 'Uploading...' : 'Upload Files'}
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
      // Simulate posts for certain dates
      const mockPosts = {
        5: [{ platform: 'instagram', topic: 'Safety Tips' }],
        12: [{ platform: 'facebook', topic: 'Team Update' }, { platform: 'linkedin', topic: 'Industry News' }],
        20: [{ platform: 'tiktok', topic: 'Equipment Demo' }],
        25: [{ platform: 'instagram', topic: 'Project Progress' }]
      };
      return mockPosts[day] || [];
    };

    const navigateMonth = (direction) => {
      const newDate = new Date(currentDate);
      newDate.setMonth(currentDate.getMonth() + direction);
      setCurrentDate(newDate);
    };

    return (
      <div className="space-y-6">
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">📅 Visual Content Calendar</h2>
          
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

          {/* Content Gap Detection */}
          <div className="mt-6 p-4 bg-yellow-50 rounded-lg">
            <h4 className="font-semibold text-yellow-800 mb-2">🔍 Content Gap Analysis</h4>
            <div className="space-y-2">
              <div className="flex items-center space-x-2">
                <span className="w-3 h-3 bg-red-500 rounded-full"></span>
                <span className="text-sm text-gray-700">Days 8-11: No content scheduled</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="w-3 h-3 bg-yellow-500 rounded-full"></span>
                <span className="text-sm text-gray-700">Day 15: Only 1 post scheduled</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="w-3 h-3 bg-orange-500 rounded-full"></span>
                <span className="text-sm text-gray-700">Weekend posts needed</span>
              </div>
            </div>
          </div>

          {/* Auto-Optimal Timing */}
          <div className="mt-6 p-4 bg-blue-50 rounded-lg">
            <h4 className="font-semibold text-blue-800 mb-2">⏰ Optimal Posting Times</h4>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center">
                <div className="text-lg mb-1">📸</div>
                <div className="text-sm font-medium">Instagram</div>
                <div className="text-xs text-gray-600">11:00 AM - 2:00 PM</div>
              </div>
              <div className="text-center">
                <div className="text-lg mb-1">👥</div>
                <div className="text-sm font-medium">Facebook</div>
                <div className="text-xs text-gray-600">1:00 PM - 4:00 PM</div>
              </div>
              <div className="text-center">
                <div className="text-lg mb-1">💼</div>
                <div className="text-sm font-medium">LinkedIn</div>
                <div className="text-xs text-gray-600">8:00 AM - 10:00 AM</div>
              </div>
              <div className="text-center">
                <div className="text-lg mb-1">🎵</div>
                <div className="text-sm font-medium">TikTok</div>
                <div className="text-xs text-gray-600">6:00 PM - 10:00 PM</div>
              </div>
            </div>
          </div>
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

  return renderCurrentView();
}

export default App;