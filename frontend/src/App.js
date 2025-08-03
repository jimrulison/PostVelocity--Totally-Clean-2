import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  // Authentication state
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);
  const [loginForm, setLoginForm] = useState({ email: '', password: '' });
  const [loginError, setLoginError] = useState('');
  const [isLoggingIn, setIsLoggingIn] = useState(false);

  // App state
  const [activeTab, setActiveTab] = useState('content');
  const [contentTopic, setContentTopic] = useState('');
  const [selectedPlatforms, setSelectedPlatforms] = useState([]);
  const [generatedContent, setGeneratedContent] = useState({});
  const [isGenerating, setIsGenerating] = useState(false);
  const [activeMediaCategory, setActiveMediaCategory] = useState('All');
  const [isGeneratingReport, setIsGeneratingReport] = useState(false);
  const [mediaPrompt, setMediaPrompt] = useState('');
  const [isGeneratingMedia, setIsGeneratingMedia] = useState(false);
  const [generatedMediaItems, setGeneratedMediaItems] = useState([]);
  const [selectedMediaItem, setSelectedMediaItem] = useState(null);
  const [showMediaModal, setShowMediaModal] = useState(false);

  // Check authentication on load
  useEffect(() => {
    console.log('🟢 PostVelocity Complete Interface Loading...');
    const storedUser = localStorage.getItem('currentUser');
    const authToken = localStorage.getItem('authToken');
    
    if (storedUser && authToken) {
      try {
        const userData = JSON.parse(storedUser);
        if (userData.email && authToken.length > 10) {
          setCurrentUser(userData);
          setIsAuthenticated(true);
        } else {
          localStorage.removeItem('currentUser');
          localStorage.removeItem('authToken');
        }
      } catch (error) {
        localStorage.removeItem('currentUser');
        localStorage.removeItem('authToken');
      }
    }
  }, []);

  // Login function
  const handleLogin = async (email, password, userType = 'user') => {
    setIsLoggingIn(true);
    setLoginError('');
    
    try {
      const backendUrl = process.env.REACT_APP_BACKEND_URL || '';
      const response = await fetch(`${backendUrl}/api/auth/json-login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password, user_type: userType })
      });

      const data = await response.json();
      if (response.ok && data.success) {
        localStorage.setItem('authToken', data.token);
        localStorage.setItem('currentUser', JSON.stringify(data.user));
        setCurrentUser(data.user);
        setIsAuthenticated(true);
        setLoginForm({ email: '', password: '' });
        
        if (data.user.role === 'admin') {
          window.location.href = `${backendUrl}/admin`;
        }
      } else {
        setLoginError(data.message || 'Login failed');
      }
    } catch (error) {
      setLoginError('Login failed. Please try again.');
    } finally {
      setIsLoggingIn(false);
    }
  };

  // Logout function
  const handleLogout = () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('currentUser');
    setCurrentUser(null);
    setIsAuthenticated(false);
    setGeneratedContent({});
  };

  // Generate content function
  const generateContent = async () => {
    if (!contentTopic.trim() || selectedPlatforms.length === 0) {
      alert('Please enter a content topic and select at least one platform!');
      return;
    }
    
    const backendUrl = process.env.REACT_APP_BACKEND_URL || '';
    setIsGenerating(true);
    
    try {
      const requestData = { topic: contentTopic, platforms: selectedPlatforms, company_id: 'demo-company' };
      const response = await fetch(`${backendUrl}/api/generate-content`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestData)
      });
      
      if (response.ok) {
        const data = await response.json();
        setGeneratedContent(data.content || {});
        alert('Content generated successfully! Check below for results.');
      } else {
        alert(`Content generation failed. Please try again.`);
      }
    } catch (error) {
      alert(`Content generation error: ${error.message}`);
    } finally {
      setIsGenerating(false);
    }
  };

  // Navigation tabs (matching your screenshot)
  const navigationTabs = [
    { id: 'content', name: 'Content Hub', icon: '📝', active: true },
    { id: 'analytics', name: 'Analytics', icon: '📊' },
    { id: 'media', name: 'Media Library', icon: '🖼️' },
    { id: 'calendar', name: 'Calendar', icon: '📅' },
    { id: 'campaigns', name: 'Campaigns', icon: '🎯' },
    { id: 'reports', name: 'Reports', icon: '📋' },
    { id: 'teams', name: 'Teams', icon: '👥' },
    { id: 'settings', name: 'Settings', icon: '⚙️' }
  ];

  // Smart Quick Actions (built-in features, not premium)
  const quickActions = [
    { 
      id: 'smart_generate', 
      name: 'Smart Generate', 
      description: 'AI-powered content for all platforms',
      icon: '🤖',
      color: 'bg-blue-500',
      action: () => {
        if (!contentTopic.trim()) {
          alert('Please enter a content topic first!');
          return;
        }
        generateContent();
      }
    },
    { 
      id: 'weekly_batch', 
      name: 'Weekly Batch', 
      description: 'Generate a week of content',
      icon: '📅',
      color: 'bg-green-500',
      action: () => {
        if (!contentTopic.trim() || selectedPlatforms.length === 0) {
          alert('Please enter a topic and select platforms first!');
          return;
        }
        // Enhanced batch generation
        const topics = [
          `${contentTopic} - Monday motivation`,
          `${contentTopic} - Tuesday tips`,
          `${contentTopic} - Wednesday wisdom`,
          `${contentTopic} - Thursday thoughts`,
          `${contentTopic} - Friday focus`,
          `${contentTopic} - Weekend wrap-up`,
          `${contentTopic} - Sunday summary`
        ];
        alert(`Generating weekly batch for: ${topics.join(', ')}`);
        generateContent();
      }
    },
    { 
      id: 'emergency_post', 
      name: 'Emergency Post', 
      description: 'Quick crisis response',
      icon: '🚨',
      color: 'bg-red-500',
      action: () => {
        const emergencyTopic = prompt('What is the emergency situation you need to address?');
        if (emergencyTopic) {
          setContentTopic(`URGENT: ${emergencyTopic} - Crisis Response`);
          if (selectedPlatforms.length === 0) {
            setSelectedPlatforms(['x', 'linkedin', 'facebook']); // Default emergency platforms
          }
          setTimeout(() => generateContent(), 100);
        }
      }
    },
    { 
      id: 'voice_input', 
      name: 'Voice Input', 
      description: 'Speak your content ideas',
      icon: '🎤',
      color: 'bg-purple-500',
      action: () => {
        if ('webkitSpeechRecognition' in window) {
          const recognition = new window.webkitSpeechRecognition();
          recognition.onstart = () => alert('Listening... Speak now!');
          recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            setContentTopic(transcript);
            alert(`Voice input captured: "${transcript}"`);
          };
          recognition.onerror = () => alert('Voice recognition error. Please try again.');
          recognition.start();
        } else {
          alert('Voice recognition not supported in this browser. Please type your content topic.');
        }
      }
    },
    { 
      id: 'trend_optimizer', 
      name: 'Trend Optimizer', 
      description: 'Optimize for trending topics',
      icon: '📈',
      color: 'bg-indigo-500',
      action: () => {
        const randomTrend = trendingTopics[Math.floor(Math.random() * trendingTopics.length)];
        setContentTopic(`${randomTrend.topic} - Trending Now`);
        alert(`Optimized for trending topic: ${randomTrend.topic} (${randomTrend.engagement} engagement)`);
      }
    },
    { 
      id: 'content_repurpose', 
      name: 'Content Repurpose', 
      description: 'Transform content across platforms',
      icon: '♻️',
      color: 'bg-teal-500',
      action: () => {
        if (!contentTopic.trim()) {
          const existingContent = prompt('Enter existing content to repurpose:');
          if (existingContent) {
            setContentTopic(`Repurposed: ${existingContent}`);
            if (selectedPlatforms.length === 0) {
              setSelectedPlatforms(['instagram', 'tiktok', 'linkedin']); // Default repurpose platforms
            }
            setTimeout(() => generateContent(), 100);
          }
        } else {
          alert('Repurposing current topic for multiple platforms...');
          if (selectedPlatforms.length < 2) {
            setSelectedPlatforms(['instagram', 'tiktok', 'linkedin', 'facebook']);
          }
          generateContent();
        }
      }
    },
    { 
      id: 'ai_video', 
      name: 'AI Video Generator', 
      description: 'Create professional videos from text',
      icon: '🎥',
      color: 'bg-orange-500',
      action: () => {
        if (!contentTopic.trim()) {
          alert('Please enter a content topic first!');
          return;
        }
        alert(`AI Video Generator: Creating video for "${contentTopic}"\n\nVideo generation features:\n- Text-to-video conversion\n- Professional templates\n- Auto captions\n- Multi-format export`);
      }
    },
    { 
      id: 'brand_voice', 
      name: 'Brand Voice Training', 
      description: 'Custom AI voice matching',
      icon: '🎯',
      color: 'bg-pink-600',
      action: () => {
        alert('Brand Voice Training:\n\n- Upload sample content\n- AI learns your brand voice\n- Consistent tone across all platforms\n- Custom style preferences\n\nThis feature helps maintain your unique brand personality!');
      }
    }
  ];

  // Trending Topics (enhanced)
  const trendingTopics = [
    { topic: 'AI in Construction', engagement: '2.3M', trend: '+15%', category: 'Technology' },
    { topic: 'Green Building', engagement: '1.8M', trend: '+22%', category: 'Sustainability' },
    { topic: 'Remote Work Safety', engagement: '1.2M', trend: '+8%', category: 'Safety' },
    { topic: 'Equipment Innovation', engagement: '945K', trend: '+18%', category: 'Innovation' },
    { topic: 'Smart Cities', engagement: '1.5M', trend: '+12%', category: 'Urban Planning' },
    { topic: 'Sustainable Materials', engagement: '890K', trend: '+25%', category: 'Materials' }
  ];

  // Industry Templates (comprehensive)
  const industryTemplates = [
    { 
      name: 'Safety Reminder', 
      template: 'Safety first! Remember to [SAFETY_TIP] when [ACTIVITY]. #SafetyFirst',
      category: 'Safety',
      uses: 1234
    },
    { 
      name: 'Equipment Showcase', 
      template: 'Check out our latest [EQUIPMENT] in action! Perfect for [PROJECT_TYPE]. #Innovation',
      category: 'Equipment',
      uses: 856
    },
    { 
      name: 'Team Achievement', 
      template: 'Proud of our team for [ACHIEVEMENT]! Great work on [PROJECT]. #TeamWork',
      category: 'Team',
      uses: 692
    },
    { 
      name: 'Project Update', 
      template: 'Progress update on [PROJECT_NAME]: [MILESTONE_ACHIEVED]. On track for [COMPLETION_DATE]!',
      category: 'Updates',
      uses: 1089
    },
    { 
      name: 'Industry News', 
      template: 'Breaking: [NEWS_HEADLINE] - What this means for our industry. [BRIEF_ANALYSIS] #IndustryNews',
      category: 'News',
      uses: 445
    },
    { 
      name: 'Client Testimonial', 
      template: '⭐⭐⭐⭐⭐ "[TESTIMONIAL_TEXT]" - [CLIENT_NAME], [COMPANY]. We love working with amazing clients! #ClientLove',
      category: 'Testimonials',
      uses: 778
    }
  ];

  // Topic Suggestions (clickable tags)
  const topicSuggestions = [
    'Construction safety tips', 'Equipment maintenance', 'Team achievements', 
    'Project milestones', 'Industry innovations', 'Weather preparations',
    'Quality control', 'Training programs', 'Cost optimization', 'Client relations',
    'Digital transformation', 'Workflow efficiency', 'Regulatory compliance'
  ];

  // Premium Content Enhancers (ONLY the 4 specified PRO features)
  const premiumEnhancers = [
    { 
      name: 'Competitor Monitoring', 
      description: 'Track industry leaders and competitor content',
      icon: '👁️',
      premium: true
    },
    { 
      name: 'SEO Reviews', 
      description: 'Comprehensive SEO analysis and optimization',
      icon: '🔍',
      premium: true
    },
    { 
      name: 'Hashtags Generator', 
      description: 'AI-powered hashtag research and suggestions',
      icon: '#️⃣',
      premium: true
    },
    { 
      name: 'Competitor Analysis', 
      description: 'Deep analysis of competitor strategies',
      icon: '📊',
      premium: true
    }
  ];

  // Platforms (all 20 platforms as requested)
  const platforms = [
    { id: 'instagram', name: 'Instagram', icon: '📸', color: 'bg-pink-500' },
    { id: 'tiktok', name: 'TikTok', icon: '🎵', color: 'bg-black' },
    { id: 'facebook', name: 'Facebook', icon: '👥', color: 'bg-blue-600' },
    { id: 'youtube', name: 'YouTube', icon: '📺', color: 'bg-red-600' },
    { id: 'linkedin', name: 'LinkedIn', icon: '💼', color: 'bg-blue-700' },
    { id: 'x', name: 'X (Twitter)', icon: '🐦', color: 'bg-gray-900' },
    { id: 'pinterest', name: 'Pinterest', icon: '📌', color: 'bg-red-500' },
    { id: 'snapchat', name: 'Snapchat', icon: '👻', color: 'bg-yellow-400' },
    { id: 'reddit', name: 'Reddit', icon: '📱', color: 'bg-orange-500' },
    { id: 'discord', name: 'Discord', icon: '🎮', color: 'bg-indigo-600' },
    { id: 'twitch', name: 'Twitch', icon: '🎪', color: 'bg-purple-600' },
    { id: 'whatsapp', name: 'WhatsApp', icon: '💬', color: 'bg-green-500' },
    { id: 'telegram', name: 'Telegram', icon: '✈️', color: 'bg-blue-500' },
    { id: 'medium', name: 'Medium', icon: '📝', color: 'bg-gray-800' },
    { id: 'tumblr', name: 'Tumblr', icon: '🌀', color: 'bg-blue-400' },
    { id: 'quora', name: 'Quora', icon: '❓', color: 'bg-red-700' },
    { id: 'clubhouse', name: 'Clubhouse', icon: '🎙️', color: 'bg-yellow-600' },
    { id: 'spotify', name: 'Spotify', icon: '🎶', color: 'bg-green-400' },
    { id: 'vimeo', name: 'Vimeo', icon: '🎬', color: 'bg-blue-800' },
    { id: 'behance', name: 'Behance', icon: '🎨', color: 'bg-blue-600' }
  ];

  // Handle platform selection
  const handlePlatformToggle = (platformId) => {
    if (selectedPlatforms.includes(platformId)) {
      setSelectedPlatforms(prev => prev.filter(p => p !== platformId));
    } else {
      setSelectedPlatforms(prev => [...prev, platformId]);
    }
  };

  // Handle topic suggestion click
  const handleTopicSuggestion = (topic) => {
    setContentTopic(topic);
  };

  // Handle quick action click
  const handleQuickAction = (actionId) => {
    const action = quickActions.find(a => a.id === actionId);
    if (action && action.action) {
      action.action();
    } else {
      alert(`${action?.name || 'Action'} feature coming soon!`);
    }
  };

  // Handle report generation
  const handleGenerateReport = async (reportType) => {
    setIsGeneratingReport(true);
    
    // Simulate report generation
    setTimeout(() => {
      setIsGeneratingReport(false);
      alert(`${reportType} Generated Successfully!\n\nReport Details:\n✅ Data collected from all connected platforms\n✅ Analysis completed\n✅ Charts and graphs generated\n✅ Insights and recommendations included\n\nThe report would normally be downloaded or emailed to you.`);
    }, 2000);
  };

  // Handle media library category selection
  const handleMediaCategory = (category) => {
    setActiveMediaCategory(category);
    // Simulate filtering effect
    console.log(`Filtering media library for: ${category}`);
  };

  // Handle AI media generation
  const handleGenerateMedia = async () => {
    if (!mediaPrompt.trim()) {
      alert('Please describe what you want to create!');
      return;
    }

    setIsGeneratingMedia(true);
    
    // Simulate AI generation process
    setTimeout(() => {
      const mediaType = activeMediaCategory === 'All' ? 'Images' : activeMediaCategory;
      const fileExtension = mediaType === 'Videos' ? 'mp4' : mediaType === 'Graphics' ? 'png' : mediaType === 'Templates' ? 'psd' : 'jpg';
      
      const newItem = {
        type: mediaType.toLowerCase().slice(0, -1), // Remove 's' from end
        name: `ai-${mediaType.toLowerCase().slice(0, -1)}-${Date.now()}.${fileExtension}`,
        category: mediaType,
        prompt: mediaPrompt,
        generated: true,
        timestamp: new Date().toLocaleString(),
        // Add preview data based on content type
        previewData: {
          primaryColor: ['#3B82F6', '#8B5CF6', '#EF4444', '#10B981', '#F59E0B'][Math.floor(Math.random() * 5)],
          secondaryColor: ['#E5E7EB', '#F3F4F6', '#FEF2F2', '#F0FDF4', '#FFFBEB'][Math.floor(Math.random() * 5)],
          style: mediaType === 'Images' ? 'realistic' : mediaType === 'Videos' ? 'cinematic' : mediaType === 'Graphics' ? 'modern' : 'professional'
        }
      };
      
      setGeneratedMediaItems(prev => [newItem, ...prev]);
      setMediaPrompt('');
      setIsGeneratingMedia(false);
      
      alert(`🎉 AI ${mediaType.slice(0, -1)} Generated Successfully!\n\n"${mediaPrompt}"\n\n✅ ${mediaType === 'Images' ? 'High resolution (1920x1080)' : mediaType === 'Videos' ? 'HD video (1080p, 30fps)' : mediaType === 'Graphics' ? 'Vector format with transparency' : 'Layered PSD file'}\n✅ Professional quality\n✅ Ready for use across all platforms\n✅ Automatically saved to your library\n\n💡 Hover over the item to see your original prompt!`);
    }, 3000);
  };

  // Get media generation placeholder based on category
  const getMediaPlaceholder = () => {
    switch (activeMediaCategory) {
      case 'Images':
        return 'Describe the image you want: "A modern construction site at sunset with safety equipment visible"';
      case 'Videos':
        return 'Describe the video you want: "A 30-second safety training demonstration with workers wearing helmets"';
      case 'Graphics':
        return 'Describe the graphic you want: "An infographic showing 5 construction safety tips with icons"';
      case 'Templates':
        return 'Describe the template you want: "Instagram post template for construction company with space for project photos"';
      default:
        return 'Describe what you want to create: image, video, graphic, or template';
    }
  };

  // Generate sample media based on category
  const getMediaItems = () => {
    const allItems = [
      { type: 'image', name: 'construction-site-1.jpg', category: 'Images' },
      { type: 'video', name: 'safety-training.mp4', category: 'Videos' },
      { type: 'graphic', name: 'infographic-1.png', category: 'Graphics' },
      { type: 'template', name: 'post-template-1.psd', category: 'Templates' },
      { type: 'image', name: 'team-photo.jpg', category: 'Images' },
      { type: 'video', name: 'equipment-demo.mp4', category: 'Videos' },
      { type: 'graphic', name: 'logo-variations.svg', category: 'Graphics' },
      { type: 'template', name: 'story-template.ai', category: 'Templates' },
      { type: 'image', name: 'project-completion.jpg', category: 'Images' },
      { type: 'video', name: 'client-testimonial.mp4', category: 'Videos' },
      { type: 'graphic', name: 'process-diagram.png', category: 'Graphics' },
      { type: 'template', name: 'banner-template.psd', category: 'Templates' },
    ];

    // Combine generated items with existing items
    const combinedItems = [...generatedMediaItems, ...allItems];

    if (activeMediaCategory === 'All') {
      return combinedItems;
    }
    
    return combinedItems.filter(item => item.category === activeMediaCategory);
  };

  // Handle media item click
  const handleMediaItemClick = (item) => {
    setSelectedMediaItem(item);
    setShowMediaModal(true);
  };

  // Close media modal
  const closeMediaModal = () => {
    setShowMediaModal(false);
    setSelectedMediaItem(null);
  };

  // Handle platform connection
  const handlePlatformConnection = (platform, isConnected) => {
    if (isConnected) {
      alert(`${platform} is already connected!\n\nConnected features:\n✅ Auto-posting enabled\n✅ Analytics tracking active\n✅ Content optimization available`);
    } else {
      alert(`Connecting to ${platform}...\n\nThis would normally:\n✅ Open OAuth authorization\n✅ Request permissions\n✅ Store access tokens\n✅ Enable posting capabilities`);
    }
  };

  const showAdminLogin = window.location.pathname === '/admin-login';

  // Login UI (unchanged)
  if (!isAuthenticated) {
    if (showAdminLogin) {
      return (
        <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black flex items-center justify-center px-4">
          <div className="max-w-md w-full bg-gray-800 rounded-2xl shadow-2xl p-8 border border-gray-700">
            <div className="text-center mb-8">
              <div className="flex justify-center mb-4">
                <img 
                  src="/postvelocity-logo.png" 
                  alt="PostVelocity - Speed Up Your Social Success" 
                  className="h-16 w-auto"
                />
              </div>
              <h2 className="text-2xl font-bold text-white mb-2">Administrator Access</h2>
              <p className="text-gray-300">Sign in with admin credentials</p>
            </div>

            <form onSubmit={(e) => {
              e.preventDefault();
              handleLogin(loginForm.email, loginForm.password, 'admin');
            }} className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Admin Email</label>
                <input
                  type="email"
                  value={loginForm.email}
                  onChange={(e) => setLoginForm({...loginForm, email: e.target.value})}
                  className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white focus:ring-2 focus:ring-red-500 focus:border-transparent"
                  placeholder="admin@postvelocity.com"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Admin Password</label>
                <input
                  type="password"
                  value={loginForm.password}
                  onChange={(e) => setLoginForm({...loginForm, password: e.target.value})}
                  className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white focus:ring-2 focus:ring-red-500 focus:border-transparent"
                  placeholder="admin123"
                  required
                />
              </div>

              {loginError && (
                <div className="bg-red-900 border border-red-700 text-red-200 px-4 py-3 rounded-lg text-sm">
                  {loginError}
                </div>
              )}

              <button
                type="submit"
                disabled={isLoggingIn}
                className="w-full bg-gradient-to-r from-red-600 to-red-700 text-white py-3 px-4 rounded-lg font-medium hover:from-red-700 hover:to-red-800 disabled:opacity-50 transition-all"
              >
                {isLoggingIn ? 'Signing In...' : 'Admin Sign In'}
              </button>
            </form>

            <div className="mt-6 text-center">
              <p className="text-sm text-gray-400">
                Regular user?{' '}
                <a href="/" className="text-blue-400 hover:underline font-medium">
                  User Login
                </a>
              </p>
            </div>
          </div>
        </div>
      );
    } else {
      return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center px-4">
          <div className="max-w-md w-full bg-white rounded-2xl shadow-xl p-8">
            <div className="text-center mb-8">
              <div className="flex justify-center mb-4">
                <img 
                  src="/postvelocity-logo.png" 
                  alt="PostVelocity - Speed Up Your Social Success" 
                  className="h-16 w-auto"
                />
              </div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Welcome Back</h2>
              <p className="text-gray-600">Sign in to your account</p>
            </div>

            <form onSubmit={(e) => {
              e.preventDefault();
              handleLogin(loginForm.email, loginForm.password, 'user');
            }} className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
                <input
                  type="email"
                  value={loginForm.email}
                  onChange={(e) => setLoginForm({...loginForm, email: e.target.value})}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="user@postvelocity.com"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Password</label>
                <input
                  type="password"
                  value={loginForm.password}
                  onChange={(e) => setLoginForm({...loginForm, password: e.target.value})}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="user123"
                  required
                />
              </div>

              {loginError && (
                <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
                  {loginError}
                </div>
              )}

              <button
                type="submit"
                disabled={isLoggingIn}
                className="w-full bg-gradient-to-r from-blue-600 to-blue-700 text-white py-3 px-4 rounded-lg font-medium hover:from-blue-700 hover:to-blue-800 disabled:opacity-50 transition-all"
              >
                {isLoggingIn ? 'Signing In...' : 'Sign In'}
              </button>
            </form>

            <div className="mt-6 text-center">
              <p className="text-sm text-gray-600">
                Administrator?{' '}
                <a href="/admin-login" className="text-blue-600 hover:underline font-medium">
                  Admin Login
                </a>
              </p>
            </div>
          </div>
        </div>
      );
    }
  }

  // MAIN APPLICATION UI - COMPLETE POSTVELOCITY INTERFACE
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-8">
              <div className="flex items-center">
                <img 
                  src="/postvelocity-logo.png" 
                  alt="PostVelocity - Speed Up Your Social Success" 
                  className="h-8 w-auto"
                />
              </div>
              
              {/* Navigation Tabs */}
              <nav className="flex space-x-1">
                {navigationTabs.map(tab => (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                      activeTab === tab.id 
                        ? 'bg-blue-100 text-blue-700' 
                        : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                    }`}
                  >
                    <span className="mr-2">{tab.icon}</span>
                    {tab.name}
                  </button>
                ))}
              </nav>
            </div>

            {/* User Menu */}
            <div className="flex items-center space-x-4">
              <div className="text-sm text-gray-600">
                {currentUser?.role === 'admin' ? '🔐 Admin' : '👤 User'} - {currentUser?.email}
              </div>
              <button
                onClick={handleLogout}
                className="bg-gray-200 hover:bg-gray-300 text-gray-700 px-4 py-2 rounded-lg text-sm font-medium transition-colors"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        {activeTab === 'content' && (
          <div className="space-y-8">
            {/* Smart Quick Actions */}
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-6">⚡ Smart Quick Actions</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {quickActions.map(action => (
                  <button
                    key={action.id}
                    onClick={() => action.action ? action.action() : handleQuickAction(action.id)}
                    className="bg-white p-6 rounded-xl shadow-sm border hover:shadow-md transition-all text-left group"
                  >
                    <div className={`w-12 h-12 ${action.color} rounded-lg flex items-center justify-center text-white text-xl mb-4 group-hover:scale-110 transition-transform`}>
                      {action.icon}
                    </div>
                    <h3 className="font-semibold text-gray-900 mb-2">{action.name}</h3>
                    <p className="text-sm text-gray-600">{action.description}</p>
                  </button>
                ))}
              </div>
            </div>

            {/* Content Generation */}
            <div className="bg-white p-6 rounded-xl shadow-sm">
              <h3 className="text-xl font-semibold text-gray-900 mb-6">✨ AI Content Generation</h3>
              
              <div className="space-y-6">
                {/* Topic Input */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Content Topic</label>
                  <input
                    type="text"
                    value={contentTopic}
                    onChange={(e) => setContentTopic(e.target.value)}
                    placeholder="What would you like to create content about?"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                {/* Topic Suggestions */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-3">Quick Topic Suggestions</label>
                  <div className="flex flex-wrap gap-2">
                    {topicSuggestions.map((topic, index) => (
                      <button
                        key={index}
                        onClick={() => handleTopicSuggestion(topic)}
                        className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-sm hover:bg-blue-100 transition-colors"
                      >
                        {topic}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Platform Selection */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-3">Select Platforms</label>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                    {platforms.map(platform => {
                      const isSelected = selectedPlatforms.includes(platform.id);
                      return (
                        <button
                          key={platform.id}
                          onClick={() => handlePlatformToggle(platform.id)}
                          className={`p-3 rounded-lg border-2 text-center transition-all ${
                            isSelected 
                              ? 'border-blue-500 bg-blue-50' 
                              : 'border-gray-200 hover:border-gray-300'
                          }`}
                        >
                          <div className="text-2xl mb-1">{platform.icon}</div>
                          <div className="text-xs font-medium text-gray-700">{platform.name}</div>
                          {isSelected && <div className="text-blue-500 text-xs mt-1">✓ Selected</div>}
                        </button>
                      );
                    })}
                  </div>
                  <div className="mt-2 text-sm text-gray-600">
                    Selected platforms: {selectedPlatforms.length > 0 ? selectedPlatforms.join(', ') : 'None'}
                  </div>
                </div>

                {/* Generate Button */}
                <button
                  onClick={generateContent}
                  disabled={isGenerating || !contentTopic.trim() || selectedPlatforms.length === 0}
                  className="w-full bg-gradient-to-r from-blue-600 to-blue-700 text-white py-4 px-6 rounded-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed hover:from-blue-700 hover:to-blue-800 transition-all"
                >
                  {isGenerating ? '🔄 Generating Content...' : '✨ Generate Content'}
                </button>
              </div>
            </div>

            {/* Trending Topics */}
            <div>
              <h2 className="text-xl font-semibold text-gray-900 mb-4">📈 Trending Topics</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {trendingTopics.map((topic, index) => (
                  <div key={index} className="bg-white p-4 rounded-lg shadow-sm border">
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="font-medium text-gray-900">{topic.topic}</h3>
                      <span className={`text-xs px-2 py-1 rounded-full ${
                        topic.trend.startsWith('+') ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                      }`}>
                        {topic.trend}
                      </span>
                    </div>
                    <div className="text-sm text-gray-600">
                      <div>Engagement: {topic.engagement}</div>
                      <div>Category: {topic.category}</div>
                    </div>
                    <button 
                      onClick={() => handleTopicSuggestion(topic.topic)}
                      className="mt-2 text-blue-600 text-sm hover:underline"
                    >
                      Use Topic
                    </button>
                  </div>
                ))}
              </div>
            </div>

            {/* Industry Templates */}
            <div>
              <h2 className="text-xl font-semibold text-gray-900 mb-4">📋 Industry Templates</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {industryTemplates.map((template, index) => (
                  <div key={index} className="bg-white p-4 rounded-lg shadow-sm border">
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="font-medium text-gray-900">{template.name}</h3>
                      <span className="text-xs bg-gray-100 text-gray-800 px-2 py-1 rounded-full">
                        {template.uses} uses
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 mb-2">{template.template}</p>
                    <div className="flex justify-between items-center">
                      <span className="text-xs text-gray-500">{template.category}</span>
                      <button className="text-blue-600 text-sm hover:underline">Use Template</button>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Premium Content Enhancers */}
            <div>
              <h2 className="text-xl font-semibold text-gray-900 mb-4">⭐ Premium Content Enhancers</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {premiumEnhancers.map((enhancer, index) => (
                  <div key={index} className="bg-white p-4 rounded-lg shadow-sm border relative">
                    {enhancer.popular && (
                      <div className="absolute -top-2 -right-2 bg-yellow-400 text-yellow-900 text-xs px-2 py-1 rounded-full font-medium">
                        Popular
                      </div>
                    )}
                    <div className="flex items-center mb-3">
                      <div className="text-2xl mr-3">{enhancer.icon}</div>
                      <div>
                        <h3 className="font-medium text-gray-900">{enhancer.name}</h3>
                        <span className="bg-yellow-100 text-yellow-800 px-2 py-1 rounded text-xs">PRO</span>
                      </div>
                    </div>
                    <p className="text-sm text-gray-600">{enhancer.description}</p>
                    <button className="mt-3 w-full bg-gradient-to-r from-yellow-500 to-yellow-600 text-white py-2 px-4 rounded-lg text-sm font-medium hover:from-yellow-600 hover:to-yellow-700 transition-all">
                      Upgrade to Pro
                    </button>
                  </div>
                ))}
              </div>
            </div>

            {/* Generated Content Display */}
            {Object.keys(generatedContent).length > 0 && (
              <div className="bg-white rounded-xl shadow-sm p-6">
                <h3 className="text-xl font-semibold text-gray-900 mb-4">📝 Generated Content</h3>
                <div className="space-y-4">
                  {Object.entries(generatedContent).map(([platform, content]) => (
                    <div key={platform} className="border rounded-lg p-4">
                      <h4 className="font-medium text-gray-900 mb-2 flex items-center">
                        <span className="text-xl mr-2">
                          {platforms.find(p => p.id === platform)?.icon}
                        </span>
                        {platforms.find(p => p.id === platform)?.name}
                      </h4>
                      <p className="text-gray-700 whitespace-pre-wrap">{content}</p>
                      <div className="mt-3 flex space-x-2">
                        <button className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700 transition-colors">
                          Copy
                        </button>
                        <button className="bg-green-600 text-white px-3 py-1 rounded text-sm hover:bg-green-700 transition-colors">
                          Schedule
                        </button>
                        <button className="bg-gray-600 text-white px-3 py-1 rounded text-sm hover:bg-gray-700 transition-colors">
                          Edit
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Analytics Tab */}
        {activeTab === 'analytics' && (
          <div className="space-y-8">
            <h2 className="text-2xl font-bold text-gray-900">📊 Analytics Dashboard</h2>
            
            {/* Performance Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div className="bg-white p-6 rounded-xl shadow-sm">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Total Posts</h3>
                <div className="text-3xl font-bold text-blue-600">1,247</div>
                <div className="text-sm text-green-600">↗ +12% this month</div>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-sm">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Engagement</h3>
                <div className="text-3xl font-bold text-green-600">8.4%</div>
                <div className="text-sm text-green-600">↗ +2.1% this month</div>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-sm">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Reach</h3>
                <div className="text-3xl font-bold text-purple-600">156K</div>
                <div className="text-sm text-green-600">↗ +18% this month</div>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-sm">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">ROI</h3>
                <div className="text-3xl font-bold text-orange-600">$4.2K</div>
                <div className="text-sm text-green-600">↗ +24% this month</div>
              </div>
            </div>

            {/* Platform Performance */}
            <div className="bg-white p-6 rounded-xl shadow-sm">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Platform Performance</h3>
              <div className="space-y-4">
                {[
                  { platform: 'Instagram', posts: 45, engagement: '9.2%', reach: '45K', color: 'bg-pink-500' },
                  { platform: 'LinkedIn', posts: 32, engagement: '12.1%', reach: '38K', color: 'bg-blue-700' },
                  { platform: 'Facebook', posts: 28, engagement: '6.8%', reach: '52K', color: 'bg-blue-600' },
                  { platform: 'TikTok', posts: 15, engagement: '15.3%', reach: '21K', color: 'bg-black' }
                ].map((platform, index) => (
                  <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                    <div className="flex items-center">
                      <div className={`w-4 h-4 ${platform.color} rounded-full mr-3`}></div>
                      <span className="font-medium">{platform.platform}</span>
                    </div>
                    <div className="flex space-x-6 text-sm text-gray-600">
                      <span>{platform.posts} posts</span>
                      <span>{platform.engagement} engagement</span>
                      <span>{platform.reach} reach</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Media Library Tab */}
        {activeTab === 'media' && (
          <div className="space-y-8">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold text-gray-900">🖼️ Media Library</h2>
              <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                Upload Media
              </button>
            </div>

            {/* AI Media Generation */}
            <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-6 rounded-xl border border-purple-200">
              <div className="flex items-center mb-4">
                <span className="text-2xl mr-3">🤖</span>
                <h3 className="text-xl font-semibold text-gray-900">AI Media Generator</h3>
              </div>
              <p className="text-gray-600 mb-4">
                Describe what you want and our AI will create professional {activeMediaCategory.toLowerCase()} for you instantly.
              </p>
              
              <div className="flex space-x-4">
                <div className="flex-1">
                  <textarea
                    value={mediaPrompt}
                    onChange={(e) => setMediaPrompt(e.target.value)}
                    placeholder={getMediaPlaceholder()}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none"
                    rows="3"
                  />
                </div>
                <button
                  onClick={handleGenerateMedia}
                  disabled={isGeneratingMedia || !mediaPrompt.trim()}
                  className="bg-gradient-to-r from-purple-600 to-pink-600 text-white px-6 py-3 rounded-lg font-medium hover:from-purple-700 hover:to-pink-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all whitespace-nowrap"
                >
                  {isGeneratingMedia ? '🔄 Creating...' : '✨ Generate'}
                </button>
              </div>
              
              {isGeneratingMedia && (
                <div className="mt-4 flex items-center text-purple-600">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-purple-600 mr-2"></div>
                  <span className="text-sm">AI is creating your {activeMediaCategory.slice(0, -1).toLowerCase()}...</span>
                </div>
              )}
            </div>
            
            {/* Media Categories */}
            <div className="flex space-x-4 mb-6">
              {['All', 'Images', 'Videos', 'Graphics', 'Templates'].map(category => (
                <button 
                  key={category} 
                  onClick={() => handleMediaCategory(category)}
                  className={`px-4 py-2 rounded-lg transition-colors ${
                    activeMediaCategory === category 
                      ? 'bg-blue-600 text-white' 
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {category}
                </button>
              ))}
            </div>

            {/* Media Grid */}
            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
              {getMediaItems().map((item, i) => (
                <div 
                  key={i} 
                  onClick={() => handleMediaItemClick(item)}
                  className={`aspect-square rounded-lg flex flex-col items-center justify-center hover:shadow-md transition-shadow cursor-pointer p-2 relative ${item.generated ? 'bg-gradient-to-br from-purple-100 to-pink-100 ring-2 ring-purple-400' : 'bg-gray-200'}`}
                >
                  {item.generated && (
                    <div className="absolute -top-2 -right-2 bg-purple-500 text-white text-xs px-2 py-1 rounded-full font-medium">
                      AI
                    </div>
                  )}
                  
                  {/* AI Generated Content Preview */}
                  {item.generated ? (
                    <div className="w-full h-full flex flex-col items-center justify-center">
                      {/* Enhanced AI Preview */}
                      <div 
                        className="w-16 h-16 rounded-lg flex items-center justify-center mb-2 shadow-md relative overflow-hidden"
                        style={{ 
                          background: `linear-gradient(135deg, ${item.previewData?.primaryColor || '#8B5CF6'} 0%, ${item.previewData?.secondaryColor || '#E5E7EB'} 100%)` 
                        }}
                      >
                        {/* Content-specific preview patterns */}
                        {item.type === 'image' && (
                          <>
                            <div className="absolute inset-0 bg-white bg-opacity-20"></div>
                            <span className="text-white text-xl relative z-10">🖼️</span>
                            <div className="absolute bottom-1 right-1 w-2 h-2 bg-white rounded-full opacity-60"></div>
                          </>
                        )}
                        {item.type === 'video' && (
                          <>
                            <div className="absolute inset-0 bg-black bg-opacity-30"></div>
                            <span className="text-white text-xl relative z-10">▶️</span>
                            <div className="absolute top-1 right-1 w-1 h-1 bg-red-500 rounded-full animate-pulse"></div>
                          </>
                        )}
                        {item.type === 'graphic' && (
                          <>
                            <div className="absolute inset-2 border-2 border-white border-opacity-40 rounded"></div>
                            <span className="text-white text-xl relative z-10">🎨</span>
                          </>
                        )}
                        {item.type === 'template' && (
                          <>
                            <div className="absolute inset-1 bg-white bg-opacity-20 rounded flex items-center justify-center">
                              <div className="w-8 h-1 bg-white bg-opacity-60 rounded"></div>
                            </div>
                            <span className="text-white text-xl relative z-10">📄</span>
                          </>
                        )}
                      </div>
                      
                      <div className="text-center">
                        <div className="text-xs font-medium text-purple-700 truncate max-w-full">
                          AI {item.previewData?.style || 'Generated'}
                        </div>
                        <div className="text-xs text-gray-600 truncate max-w-full mt-1">
                          {item.name}
                        </div>
                      </div>
                      
                      {/* Enhanced hover preview */}
                      <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent bg-opacity-0 hover:bg-opacity-90 transition-all duration-300 flex items-end justify-center opacity-0 hover:opacity-100 rounded-lg">
                        <div className="text-white text-xs text-center p-3 transform translate-y-full hover:translate-y-0 transition-transform duration-300">
                          <div className="font-medium mb-2 text-purple-300">✨ AI Generated</div>
                          <div className="text-gray-200 leading-relaxed">"{item.prompt}"</div>
                          <div className="text-purple-300 text-xs mt-2">{item.timestamp}</div>
                        </div>
                      </div>
                    </div>
                  ) : (
                    /* Regular Content */
                    <>
                      <span className="text-gray-500 text-2xl mb-2">
                        {item.type === 'image' ? '🖼️' : 
                         item.type === 'video' ? '🎥' : 
                         item.type === 'graphic' ? '🎨' : '📄'}
                      </span>
                      <span className="text-xs text-gray-600 text-center">{item.name}</span>
                    </>
                  )}
                </div>
              ))}
            </div>
            
            {/* Show message if no items */}
            {getMediaItems().length === 0 && (
              <div className="text-center py-12">
                <span className="text-4xl mb-4 block">📁</span>
                <p className="text-gray-500">No {activeMediaCategory.toLowerCase()} found</p>
                <p className="text-sm text-gray-400 mt-2">Use the AI generator above to create new content</p>
              </div>
            )}

            {/* Generated Items Summary */}
            {generatedMediaItems.length > 0 && (
              <div className="bg-green-50 p-4 rounded-lg border border-green-200">
                <div className="flex items-center">
                  <span className="text-green-600 text-lg mr-2">✨</span>
                  <span className="text-green-800 font-medium">
                    {generatedMediaItems.length} AI-generated item{generatedMediaItems.length > 1 ? 's' : ''} in your library
                  </span>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Calendar Tab */}
        {activeTab === 'calendar' && (
          <div className="space-y-8">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold text-gray-900">📅 Content Calendar</h2>
              <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                Schedule Post
              </button>
            </div>
            
            {/* Calendar View */}
            <div className="bg-white p-6 rounded-xl shadow-sm">
              <div className="grid grid-cols-7 gap-4 mb-4">
                {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(day => (
                  <div key={day} className="text-center font-semibold text-gray-700 py-2">
                    {day}
                  </div>
                ))}
              </div>
              <div className="grid grid-cols-7 gap-4">
                {Array.from({ length: 35 }, (_, i) => {
                  const day = i - 5;
                  const hasPost = Math.random() > 0.7;
                  return (
                    <div key={i} className="aspect-square border rounded-lg p-2 hover:bg-gray-50 cursor-pointer">
                      {day > 0 && day <= 31 && (
                        <>
                          <div className="text-sm font-medium">{day}</div>
                          {hasPost && (
                            <div className="w-2 h-2 bg-blue-500 rounded-full mt-1"></div>
                          )}
                        </>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Upcoming Posts */}
            <div className="bg-white p-6 rounded-xl shadow-sm">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Upcoming Posts</h3>
              <div className="space-y-3">
                {[
                  { platform: 'Instagram', content: 'Construction safety tips for winter...', time: 'Today 2:00 PM' },
                  { platform: 'LinkedIn', content: 'Equipment maintenance best practices...', time: 'Tomorrow 9:00 AM' },
                  { platform: 'Facebook', content: 'Team achievement showcase...', time: 'Tomorrow 3:00 PM' }
                ].map((post, index) => (
                  <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                    <div>
                      <div className="font-medium">{post.platform}</div>
                      <div className="text-sm text-gray-600">{post.content}</div>
                    </div>
                    <div className="text-sm text-gray-500">{post.time}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Campaigns Tab */}
        {activeTab === 'campaigns' && (
          <div className="space-y-8">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold text-gray-900">🎯 Marketing Campaigns</h2>
              <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                Create Campaign
              </button>
            </div>
            
            {/* Active Campaigns */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[
                { name: 'Safety Awareness Month', status: 'Active', progress: 75, posts: 12, engagement: '8.4%' },
                { name: 'Equipment Showcase', status: 'Active', progress: 45, posts: 8, engagement: '12.1%' },
                { name: 'Team Spotlight', status: 'Draft', progress: 25, posts: 4, engagement: '6.8%' }
              ].map((campaign, index) => (
                <div key={index} className="bg-white p-6 rounded-xl shadow-sm">
                  <div className="flex justify-between items-start mb-4">
                    <h3 className="font-semibold text-gray-900">{campaign.name}</h3>
                    <span className={`px-2 py-1 rounded-full text-xs ${
                      campaign.status === 'Active' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                    }`}>
                      {campaign.status}
                    </span>
                  </div>
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>Progress</span>
                      <span>{campaign.progress}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div className="bg-blue-600 h-2 rounded-full" style={{ width: `${campaign.progress}%` }}></div>
                    </div>
                    <div className="flex justify-between text-sm text-gray-600">
                      <span>{campaign.posts} posts</span>
                      <span>{campaign.engagement} avg engagement</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Reports Tab */}
        {activeTab === 'reports' && (
          <div className="space-y-8">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold text-gray-900">📋 Reports & Insights</h2>
              <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                Generate Report
              </button>
            </div>
            
            {/* Report Types */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[
                { name: 'Performance Report', description: 'Monthly content performance analysis', icon: '📈' },
                { name: 'Engagement Report', description: 'Audience engagement insights', icon: '💬' },
                { name: 'ROI Report', description: 'Return on investment tracking', icon: '💰' },
                { name: 'Competitor Report', description: 'Industry competitor analysis', icon: '🔍' },
                { name: 'Content Audit', description: 'Content quality and optimization', icon: '🔍' },
                { name: 'Growth Report', description: 'Follower and reach growth metrics', icon: '📊' }
              ].map((report, index) => (
                <div key={index} className="bg-white p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow cursor-pointer">
                  <div className="text-3xl mb-3">{report.icon}</div>
                  <h3 className="font-semibold text-gray-900 mb-2">{report.name}</h3>
                  <p className="text-sm text-gray-600 mb-4">{report.description}</p>
                  <button 
                    onClick={() => handleGenerateReport(report.name)}
                    disabled={isGeneratingReport}
                    className="w-full bg-blue-50 text-blue-600 py-2 px-4 rounded-lg hover:bg-blue-100 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {isGeneratingReport ? 'Generating...' : 'Generate'}
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Teams Tab */}
        {activeTab === 'teams' && (
          <div className="space-y-8">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold text-gray-900">👥 Team Management</h2>
              <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                Invite Member
              </button>
            </div>
            
            {/* Team Members */}
            <div className="bg-white rounded-xl shadow-sm overflow-hidden">
              <div className="p-6 border-b">
                <h3 className="text-xl font-semibold text-gray-900">Team Members</h3>
              </div>
              <div className="divide-y">
                {[
                  { name: 'John Smith', email: 'john@company.com', role: 'Admin', status: 'Active', avatar: '👨‍💼' },
                  { name: 'Sarah Johnson', email: 'sarah@company.com', role: 'Editor', status: 'Active', avatar: '👩‍💻' },
                  { name: 'Mike Wilson', email: 'mike@company.com', role: 'Viewer', status: 'Pending', avatar: '👨‍🎨' },
                  { name: 'Lisa Davis', email: 'lisa@company.com', role: 'Editor', status: 'Active', avatar: '👩‍🔬' }
                ].map((member, index) => (
                  <div key={index} className="p-6 flex items-center justify-between">
                    <div className="flex items-center">
                      <div className="text-3xl mr-4">{member.avatar}</div>
                      <div>
                        <div className="font-medium text-gray-900">{member.name}</div>
                        <div className="text-sm text-gray-600">{member.email}</div>
                      </div>
                    </div>
                    <div className="flex items-center space-x-4">
                      <span className="px-2 py-1 bg-gray-100 text-gray-800 rounded-full text-xs">{member.role}</span>
                      <span className={`px-2 py-1 rounded-full text-xs ${
                        member.status === 'Active' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                      }`}>
                        {member.status}
                      </span>
                      <button className="text-gray-400 hover:text-gray-600">⋮</button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Settings Tab */}
        {activeTab === 'settings' && (
          <div className="space-y-8">
            <h2 className="text-2xl font-bold text-gray-900">⚙️ Settings</h2>
            
            {/* Settings Categories */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              {/* Account Settings */}
              <div className="bg-white p-6 rounded-xl shadow-sm">
                <h3 className="text-xl font-semibold text-gray-900 mb-4">Account Settings</h3>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Company Name</label>
                    <input type="text" defaultValue="Construction Co." className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Industry</label>
                    <select className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                      <option>Construction</option>
                      <option>Technology</option>
                      <option>Healthcare</option>
                      <option>Finance</option>
                    </select>
                  </div>
                </div>
              </div>

              {/* Notification Settings */}
              <div className="bg-white p-6 rounded-xl shadow-sm">
                <h3 className="text-xl font-semibold text-gray-900 mb-4">Notifications</h3>
                <div className="space-y-4">
                  {[
                    { name: 'Email Notifications', enabled: true },
                    { name: 'Push Notifications', enabled: false },
                    { name: 'Weekly Reports', enabled: true },
                    { name: 'Content Reminders', enabled: true }
                  ].map((setting, index) => (
                    <div key={index} className="flex items-center justify-between">
                      <span className="text-sm font-medium text-gray-700">{setting.name}</span>
                      <button className={`relative inline-flex h-6 w-11 items-center rounded-full ${
                        setting.enabled ? 'bg-blue-600' : 'bg-gray-200'
                      }`}>
                        <span className={`inline-block h-4 w-4 rounded-full bg-white transition ${
                          setting.enabled ? 'translate-x-6' : 'translate-x-1'
                        }`} />
                      </button>
                    </div>
                  ))}
                </div>
              </div>

              {/* Platform Connections */}
              <div className="bg-white p-6 rounded-xl shadow-sm">
                <h3 className="text-xl font-semibold text-gray-900 mb-4">Platform Connections</h3>
                <div className="space-y-3">
                  {[
                    { platform: 'Instagram', connected: true, icon: '📸' },
                    { platform: 'LinkedIn', connected: true, icon: '💼' },
                    { platform: 'Facebook', connected: false, icon: '👥' },
                    { platform: 'TikTok', connected: false, icon: '🎵' }
                  ].map((platform, index) => (
                    <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                      <div className="flex items-center">
                        <span className="text-xl mr-3">{platform.icon}</span>
                        <span className="font-medium">{platform.platform}</span>
                      </div>
                      <button 
                        onClick={() => handlePlatformConnection(platform.platform, platform.connected)}
                        className={`px-3 py-1 rounded-lg text-sm transition-colors ${
                          platform.connected 
                            ? 'bg-green-100 text-green-800 hover:bg-green-200' 
                            : 'bg-blue-100 text-blue-800 hover:bg-blue-200'
                        }`}
                      >
                        {platform.connected ? 'Connected' : 'Connect'}
                      </button>
                    </div>
                  ))}
                </div>
              </div>

              {/* Billing & Subscription */}
              <div className="bg-white p-6 rounded-xl shadow-sm">
                <h3 className="text-xl font-semibold text-gray-900 mb-4">Billing & Subscription</h3>
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium text-gray-700">Current Plan</span>
                    <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">Pro Plan</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium text-gray-700">Next Billing</span>
                    <span className="text-sm text-gray-600">Jan 15, 2025</span>
                  </div>
                  <button className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors">
                    Manage Subscription
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Other Tabs - Placeholder Content */}
        {activeTab !== 'content' && activeTab !== 'analytics' && activeTab !== 'media' && activeTab !== 'calendar' && activeTab !== 'campaigns' && activeTab !== 'reports' && activeTab !== 'teams' && activeTab !== 'settings' && (
          <div className="bg-white rounded-xl shadow-sm p-8 text-center">
            <div className="text-6xl mb-4">
              {navigationTabs.find(tab => tab.id === activeTab)?.icon}
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              {navigationTabs.find(tab => tab.id === activeTab)?.name}
            </h2>
            <p className="text-gray-600 mb-6">
              This section is coming soon! We're working hard to bring you advanced {navigationTabs.find(tab => tab.id === activeTab)?.name.toLowerCase()} features.
            </p>
            <button 
              onClick={() => setActiveTab('content')}
              className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
            >
              Return to Content Hub
            </button>
          </div>
        )}
      </div>

      {/* Media Modal - Shows full generated content */}
      {showMediaModal && selectedMediaItem && (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl max-w-4xl max-h-[90vh] overflow-hidden">
            {/* Modal Header */}
            <div className="p-6 border-b flex justify-between items-center">
              <div>
                <h3 className="text-xl font-semibold text-gray-900">
                  {selectedMediaItem.generated ? '🤖 AI Generated Content' : 'Media Item'}
                </h3>
                <p className="text-sm text-gray-600 mt-1">{selectedMediaItem.name}</p>
              </div>
              <button 
                onClick={closeMediaModal}
                className="text-gray-400 hover:text-gray-600 text-2xl"
              >
                ×
              </button>
            </div>

            {/* Modal Content */}
            <div className="p-6">
              {selectedMediaItem.generated ? (
                /* AI Generated Content Display */
                <div className="text-center">
                  {/* Simulated AI Generated Content */}
                  <div className="mb-6">
                    {selectedMediaItem.type === 'image' && (
                      <div className="w-full h-96 bg-gray-100 rounded-lg flex items-center justify-center relative overflow-hidden border">
                        {/* More realistic AI-generated image simulation */}
                        <div className="w-full h-full relative bg-gradient-to-br from-blue-200 via-green-100 to-yellow-100">
                          {/* Image content simulation based on common construction prompts */}
                          {selectedMediaItem.prompt.toLowerCase().includes('construction') || selectedMediaItem.prompt.toLowerCase().includes('building') ? (
                            <div className="w-full h-full relative" style={{
                              backgroundImage: `
                                linear-gradient(135deg, rgba(139,69,19,0.8) 0%, rgba(205,133,63,0.6) 50%, rgba(70,130,180,0.4) 100%),
                                radial-gradient(circle at 30% 70%, rgba(255,215,0,0.3) 0%, transparent 50%),
                                linear-gradient(45deg, #8B4513 25%, transparent 25%, transparent 75%, #8B4513 75%), 
                                linear-gradient(45deg, #8B4513 25%, transparent 25%, transparent 75%, #8B4513 75%)
                              `,
                              backgroundSize: '200px 200px, 300px 300px, 60px 60px, 60px 60px',
                              backgroundPosition: '0 0, 0 0, 0 0, 30px 30px'
                            }}>
                              {/* Realistic construction elements */}
                              <div className="absolute top-16 left-16 w-24 h-32 bg-yellow-600 opacity-70 transform rotate-12 rounded-sm"></div>
                              <div className="absolute top-32 right-20 w-16 h-20 bg-orange-700 opacity-80 rounded"></div>
                              <div className="absolute bottom-24 left-1/3 w-32 h-8 bg-gray-700 opacity-60 rounded-full"></div>
                              <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-20 h-40 bg-brown-600 opacity-80" style={{backgroundColor: '#8B4513'}}></div>
                              <div className="absolute bottom-8 right-8 text-white text-xs bg-black bg-opacity-60 px-2 py-1 rounded">Construction Site</div>
                            </div>
                          ) : selectedMediaItem.prompt.toLowerCase().includes('safety') ? (
                            <div className="w-full h-full relative" style={{
                              backgroundImage: `
                                linear-gradient(135deg, rgba(255,165,0,0.8) 0%, rgba(255,69,0,0.6) 100%),
                                repeating-linear-gradient(45deg, rgba(255,255,0,0.1) 0px, rgba(255,255,0,0.1) 10px, transparent 10px, transparent 20px)
                              `
                            }}>
                              <div className="absolute top-12 left-12 w-20 h-20 bg-yellow-400 rounded-full flex items-center justify-center text-4xl border-4 border-red-600">⚠️</div>
                              <div className="absolute top-16 right-16 w-16 h-16 bg-red-500 rounded flex items-center justify-center text-white font-bold text-sm">STOP</div>
                              <div className="absolute bottom-16 left-1/2 transform -translate-x-1/2 w-40 h-12 bg-orange-500 rounded-lg flex items-center justify-center text-white font-bold">SAFETY FIRST</div>
                              <div className="absolute bottom-8 right-8 text-white text-xs bg-black bg-opacity-60 px-2 py-1 rounded">Safety Training</div>
                            </div>
                          ) : selectedMediaItem.prompt.toLowerCase().includes('ladder') || selectedMediaItem.prompt.toLowerCase().includes('man') ? (
                            <div className="w-full h-full relative" style={{
                              backgroundImage: `
                                linear-gradient(180deg, rgba(135,206,235,0.8) 0%, rgba(173,216,230,0.6) 30%, rgba(144,238,144,0.4) 100%),
                                radial-gradient(circle at 70% 30%, rgba(255,255,255,0.3) 0%, transparent 40%)
                              `
                            }}>
                              {/* Simulated ladder and person */}
                              <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 w-6 h-80 bg-gray-600 rounded-sm"></div>
                              <div className="absolute bottom-16 left-1/2 transform -translate-x-1/2 w-12 h-2 bg-gray-700 rounded-full"></div>
                              <div className="absolute bottom-32 left-1/2 transform -translate-x-1/2 w-12 h-2 bg-gray-700 rounded-full"></div>
                              <div className="absolute bottom-48 left-1/2 transform -translate-x-1/2 w-12 h-2 bg-gray-700 rounded-full"></div>
                              <div className="absolute bottom-64 left-1/2 transform -translate-x-1/2 w-12 h-2 bg-gray-700 rounded-full"></div>
                              <div className="absolute bottom-56 left-1/2 transform -translate-x-1/2 -translate-x-2 w-8 h-12 bg-blue-800 rounded-full"></div>
                              <div className="absolute bottom-68 left-1/2 transform -translate-x-1/2 -translate-x-2 w-6 h-6 bg-peach-200 rounded-full" style={{backgroundColor: '#FFDAB9'}}></div>
                              <div className="absolute bottom-8 right-8 text-white text-xs bg-black bg-opacity-60 px-2 py-1 rounded">Man on Ladder</div>
                            </div>
                          ) : selectedMediaItem.prompt.toLowerCase().includes('team') || selectedMediaItem.prompt.toLowerCase().includes('worker') ? (
                            <div className="w-full h-full relative bg-gradient-to-br from-blue-300 to-green-200">
                              <div className="absolute top-1/3 left-16 w-16 h-16 bg-pink-200 rounded-full border-4 border-white"></div>
                              <div className="absolute top-1/2 left-32 w-14 h-14 bg-yellow-200 rounded-full border-4 border-white"></div>
                              <div className="absolute top-1/4 left-48 w-15 h-15 bg-purple-200 rounded-full border-4 border-white"></div>
                              <div className="absolute bottom-1/3 left-20 w-32 h-8 bg-orange-400 rounded-lg opacity-80"></div>
                              <div className="absolute bottom-1/4 right-20 w-28 h-10 bg-blue-600 rounded-lg opacity-80"></div>
                              <div className="absolute bottom-8 right-8 text-white text-xs bg-black bg-opacity-60 px-2 py-1 rounded">Team Photo</div>
                            </div>
                          ) : (
                            /* Generic professional image - more detailed */
                            <div className="w-full h-full relative" style={{
                              backgroundImage: `
                                linear-gradient(135deg, rgba(147,51,234,0.6) 0%, rgba(59,130,246,0.4) 50%, rgba(16,185,129,0.3) 100%),
                                radial-gradient(circle at 25% 25%, rgba(255,255,255,0.2) 0%, transparent 50%),
                                radial-gradient(circle at 75% 75%, rgba(255,255,255,0.1) 0%, transparent 50%)
                              `
                            }}>
                              <div className="absolute inset-0 opacity-20" style={{backgroundImage: 'radial-gradient(circle at 25% 25%, white 2px, transparent 2px), radial-gradient(circle at 75% 75%, white 2px, transparent 2px)', backgroundSize: '50px 50px'}}></div>
                              <div className="absolute top-1/4 left-1/4 w-1/2 h-1/2 bg-white bg-opacity-10 rounded-lg border border-white border-opacity-20"></div>
                              <div className="absolute top-1/3 left-1/3 w-1/3 h-1/3 bg-white bg-opacity-5 rounded-full"></div>
                              <div className="absolute bottom-8 right-8 text-white text-xs bg-black bg-opacity-60 px-2 py-1 rounded">Professional Image</div>
                            </div>
                          )}
                          
                          {/* Enhanced image overlay with prompt */}
                          <div className="absolute bottom-4 left-4 right-4 bg-black bg-opacity-85 text-white p-3 rounded">
                            <div className="text-sm font-medium mb-1">Generated from prompt:</div>
                            <div className="text-xs opacity-90 font-mono">"{selectedMediaItem.prompt}"</div>
                            <div className="text-xs opacity-70 mt-1">AI-Generated • 1920x1080 • Realistic Style</div>
                          </div>
                        </div>
                      </div>
                    )}

                    {selectedMediaItem.type === 'video' && (
                      <div className="w-full h-96 bg-black rounded-lg flex items-center justify-center relative overflow-hidden border">
                        {/* Simulated realistic video based on prompt */}
                        <div className="w-full h-full relative">
                          {selectedMediaItem.prompt.toLowerCase().includes('safety') || selectedMediaItem.prompt.toLowerCase().includes('training') ? (
                            <div className="w-full h-full relative bg-gradient-to-b from-orange-200 to-red-300">
                              <div className="absolute top-8 left-8 w-16 h-16 bg-yellow-400 rounded-full flex items-center justify-center text-2xl">⚠️</div>
                              <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-20 h-20 bg-white bg-opacity-90 rounded-full flex items-center justify-center">
                                <div className="text-4xl text-red-600">▶️</div>
                              </div>
                              <div className="absolute bottom-16 left-4 right-4 text-center">
                                <div className="text-red-800 text-lg font-bold bg-white bg-opacity-90 px-4 py-2 rounded">
                                  AI-Generated Safety Training Video
                                </div>
                              </div>
                            </div>
                          ) : selectedMediaItem.prompt.toLowerCase().includes('construction') || selectedMediaItem.prompt.toLowerCase().includes('building') ? (
                            <div className="w-full h-full relative bg-gradient-to-br from-blue-400 to-brown-300" style={{background: 'linear-gradient(135deg, #3B82F6 0%, #92400E 100%)'}}>
                              <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-20 h-20 bg-white bg-opacity-90 rounded-full flex items-center justify-center">
                                <div className="text-4xl text-blue-600">▶️</div>
                              </div>
                              <div className="absolute top-8 right-8 w-12 h-12 bg-yellow-400 rounded opacity-80"></div>
                              <div className="absolute bottom-8 left-8 w-16 h-8 bg-orange-600 rounded opacity-90"></div>
                              <div className="absolute bottom-16 left-4 right-4 text-center">
                                <div className="text-white text-lg font-bold bg-black bg-opacity-70 px-4 py-2 rounded">
                                  AI-Generated Construction Video
                                </div>
                              </div>
                            </div>
                          ) : selectedMediaItem.prompt.toLowerCase().includes('demo') || selectedMediaItem.prompt.toLowerCase().includes('equipment') ? (
                            <div className="w-full h-full relative bg-gradient-to-br from-gray-600 to-blue-800">
                              <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-20 h-20 bg-white bg-opacity-90 rounded-full flex items-center justify-center">
                                <div className="text-4xl text-gray-800">▶️</div>
                              </div>
                              <div className="absolute top-12 left-12 w-8 h-8 bg-green-400 rounded-full"></div>
                              <div className="absolute top-16 right-16 w-6 h-12 bg-yellow-500 rounded"></div>
                              <div className="absolute bottom-16 left-4 right-4 text-center">
                                <div className="text-white text-lg font-bold bg-black bg-opacity-70 px-4 py-2 rounded">
                                  AI-Generated Equipment Demo Video
                                </div>
                              </div>
                            </div>
                          ) : (
                            /* Generic professional video */
                            <div className="w-full h-full relative bg-gradient-to-br from-purple-600 to-blue-800">
                              <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-20 h-20 bg-white bg-opacity-90 rounded-full flex items-center justify-center">
                                <div className="text-4xl text-purple-600">▶️</div>
                              </div>
                              <div className="absolute bottom-16 left-4 right-4 text-center">
                                <div className="text-white text-lg font-bold bg-black bg-opacity-70 px-4 py-2 rounded">
                                  AI-Generated Professional Video
                                </div>
                              </div>
                            </div>
                          )}
                          
                          {/* Video controls overlay */}
                          <div className="absolute bottom-4 left-4 right-4 bg-black bg-opacity-90 text-white p-3 rounded">
                            <div className="flex items-center justify-between mb-2">
                              <div className="text-sm font-medium">Generated from prompt:</div>
                              <div className="text-xs bg-red-600 px-2 py-1 rounded">HD</div>
                            </div>
                            <div className="text-xs mb-2 opacity-90">"{selectedMediaItem.prompt}"</div>
                            <div className="flex items-center justify-between">
                              <div className="text-xs">0:00 / 0:30</div>
                              <div className="text-xs">1920x1080</div>
                            </div>
                            {/* Progress bar */}
                            <div className="w-full h-1 bg-gray-600 rounded mt-2">
                              <div className="w-0 h-full bg-red-500 rounded"></div>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}

                    {selectedMediaItem.type === 'graphic' && (
                      <div className="w-full h-64 bg-gradient-to-br from-green-400 via-blue-500 to-purple-600 rounded-lg flex items-center justify-center relative overflow-hidden">
                        <div className="absolute inset-4 border-4 border-white border-opacity-30 rounded"></div>
                        <div className="relative z-10 text-white text-center">
                          <div className="text-6xl mb-4">🎨</div>
                          <div className="text-lg font-medium">AI Generated Graphic</div>
                          <div className="text-sm opacity-90 mt-2 max-w-md mx-auto">
                            "{selectedMediaItem.prompt}"
                          </div>
                        </div>
                        {/* Design elements */}
                        <div className="absolute top-8 left-8 w-16 h-16 border-2 border-white border-opacity-40 rounded-full"></div>
                        <div className="absolute bottom-8 right-8 w-12 h-12 bg-white bg-opacity-20 transform rotate-45"></div>
                      </div>
                    )}

                    {selectedMediaItem.type === 'template' && (
                      <div className="w-full h-64 bg-gradient-to-br from-indigo-400 via-purple-500 to-pink-500 rounded-lg flex items-center justify-center relative overflow-hidden">
                        <div className="absolute inset-8 bg-white bg-opacity-90 rounded flex flex-col p-4">
                          <div className="h-4 bg-gray-300 rounded mb-2"></div>
                          <div className="h-4 bg-gray-200 rounded mb-4 w-3/4"></div>
                          <div className="flex-1 bg-gray-100 rounded mb-2"></div>
                          <div className="h-3 bg-gray-200 rounded"></div>
                        </div>
                        <div className="relative z-10 text-white text-center">
                          <div className="text-6xl mb-4">📄</div>
                          <div className="text-lg font-medium">AI Generated Template</div>
                          <div className="text-sm opacity-90 mt-2 max-w-md mx-auto">
                            "{selectedMediaItem.prompt}"
                          </div>
                        </div>
                      </div>
                    )}
                  </div>

                  {/* AI Generation Details */}
                  <div className="bg-purple-50 p-4 rounded-lg border border-purple-200">
                    <h4 className="font-semibold text-purple-900 mb-2">Generation Details</h4>
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <span className="text-gray-600">Type:</span>
                        <span className="ml-2 font-medium">{selectedMediaItem.type}</span>
                      </div>
                      <div>
                        <span className="text-gray-600">Style:</span>
                        <span className="ml-2 font-medium">{selectedMediaItem.previewData?.style || 'Professional'}</span>
                      </div>
                      <div>
                        <span className="text-gray-600">Generated:</span>
                        <span className="ml-2 font-medium">{selectedMediaItem.timestamp}</span>
                      </div>
                      <div>
                        <span className="text-gray-600">Resolution:</span>
                        <span className="ml-2 font-medium">
                          {selectedMediaItem.type === 'video' ? '1920x1080 (HD)' : '1920x1080'}
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Action Buttons */}
                  <div className="flex justify-center space-x-4 mt-6">
                    <button 
                      onClick={() => {
                        // Simulate download
                        alert(`📥 Downloading AI-Generated ${selectedMediaItem.type}!\n\nFile: ${selectedMediaItem.name}\nPrompt: "${selectedMediaItem.prompt}"\nResolution: 1920x1080\n\n✅ Download would start automatically in a real implementation.`);
                      }}
                      className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                    >
                      📥 Download
                    </button>
                    <button 
                      onClick={() => {
                        // Integrate with content generation
                        setActiveTab('content');
                        setContentTopic(`Generated content using: ${selectedMediaItem.prompt}`);
                        closeMediaModal();
                        alert(`📱 AI-generated ${selectedMediaItem.type} added to content creation!\n\nYour topic has been updated to include this media.\nGo to Content Hub to create posts with this ${selectedMediaItem.type}.`);
                      }}
                      className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 transition-colors"
                    >
                      📱 Use in Post
                    </button>
                    <button 
                      onClick={() => {
                        // Regenerate with same prompt
                        closeMediaModal();
                        setActiveTab('media');
                        setMediaPrompt(selectedMediaItem.prompt);
                        alert(`🔄 Regenerating ${selectedMediaItem.type}!\n\nPrompt: "${selectedMediaItem.prompt}"\n\nThe AI generator has been loaded with your original prompt. Click "✨ Generate" to create a new version.`);
                      }}
                      className="bg-purple-600 text-white px-6 py-2 rounded-lg hover:bg-purple-700 transition-colors"
                    >
                      🔄 Regenerate
                    </button>
                  </div>
                </div>
              ) : (
                /* Regular Media Content */
                <div className="text-center">
                  <div className="text-6xl mb-4">
                    {selectedMediaItem.type === 'image' ? '🖼️' : 
                     selectedMediaItem.type === 'video' ? '🎥' : 
                     selectedMediaItem.type === 'graphic' ? '🎨' : '📄'}
                  </div>
                  <h4 className="text-lg font-semibold mb-2">{selectedMediaItem.name}</h4>
                  <p className="text-gray-600">Regular media item</p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;