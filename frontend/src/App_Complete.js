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

  // Smart Quick Actions (enhanced from your screenshot)
  const quickActions = [
    { 
      id: 'smart_generate', 
      name: 'Smart Generate', 
      description: 'AI-powered content for all platforms',
      icon: '🤖',
      color: 'bg-blue-500'
    },
    { 
      id: 'weekly_batch', 
      name: 'Weekly Batch', 
      description: 'Generate a week of content',
      icon: '📅',
      color: 'bg-green-500'
    },
    { 
      id: 'emergency_post', 
      name: 'Emergency Post', 
      description: 'Quick crisis response',
      icon: '🚨',
      color: 'bg-red-500'
    },
    { 
      id: 'voice_input', 
      name: 'Voice Input', 
      description: 'Speak your content ideas',
      icon: '🎤',
      color: 'bg-purple-500'
    },
    { 
      id: 'competitor_analysis', 
      name: 'Competitor Analysis', 
      description: 'Analyze competitor content',
      icon: '🔍',
      color: 'bg-yellow-500'
    },
    { 
      id: 'trend_optimizer', 
      name: 'Trend Optimizer', 
      description: 'Optimize for trending topics',
      icon: '📈',
      color: 'bg-indigo-500'
    },
    { 
      id: 'hashtag_generator', 
      name: 'Hashtag Generator', 
      description: 'AI-powered hashtag suggestions',
      icon: '#️⃣',
      color: 'bg-pink-500'
    },
    { 
      id: 'content_repurpose', 
      name: 'Content Repurpose', 
      description: 'Transform content across platforms',
      icon: '♻️',
      color: 'bg-teal-500'
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

  // Premium Content Enhancers
  const premiumEnhancers = [
    { 
      name: 'AI Video Generator', 
      description: 'Create professional videos from text',
      icon: '🎥',
      premium: true,
      popular: true
    },
    { 
      name: 'Advanced Analytics', 
      description: 'Deep performance insights',
      icon: '📊',
      premium: true
    },
    { 
      name: 'Automated Scheduling', 
      description: 'Smart posting optimization',
      icon: '⏰',
      premium: true
    },
    { 
      name: 'Brand Voice Training', 
      description: 'Custom AI voice matching',
      icon: '🎯',
      premium: true,
      popular: true
    },
    { 
      name: 'Competitor Monitoring', 
      description: 'Track industry leaders',
      icon: '👁️',
      premium: true
    },
    { 
      name: 'ROI Tracking', 
      description: 'Measure content performance',
      icon: '💰',
      premium: true
    }
  ];

  // Platforms (comprehensive list with icons)
  const platforms = [
    { id: 'instagram', name: 'Instagram', icon: '📸', color: 'bg-pink-500' },
    { id: 'tiktok', name: 'TikTok', icon: '🎵', color: 'bg-black' },
    { id: 'facebook', name: 'Facebook', icon: '👥', color: 'bg-blue-600' },
    { id: 'youtube', name: 'YouTube', icon: '📺', color: 'bg-red-600' },
    { id: 'linkedin', name: 'LinkedIn', icon: '💼', color: 'bg-blue-700' },
    { id: 'x', name: 'X (Twitter)', icon: '🐦', color: 'bg-gray-900' },
    { id: 'pinterest', name: 'Pinterest', icon: '📌', color: 'bg-red-500' },
    { id: 'snapchat', name: 'Snapchat', icon: '👻', color: 'bg-yellow-400' }
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
    alert(`${quickActions.find(a => a.id === actionId)?.name} feature coming soon!`);
  };

  const showAdminLogin = window.location.pathname === '/admin-login';

  // Login UI (unchanged)
  if (!isAuthenticated) {
    if (showAdminLogin) {
      return (
        <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black flex items-center justify-center px-4">
          <div className="max-w-md w-full bg-gray-800 rounded-2xl shadow-2xl p-8 border border-gray-700">
            <div className="text-center mb-8">
              <div className="text-4xl font-bold text-white mb-2">🔐 Admin Portal</div>
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
              <div className="text-4xl font-bold text-blue-600 mb-2">🚀 PostVelocity</div>
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
              <div className="text-2xl font-bold text-blue-600">🚀 PostVelocity</div>
              
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
                    onClick={() => handleQuickAction(action.id)}
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

        {/* Other Tabs - Placeholder Content */}
        {activeTab !== 'content' && (
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
    </div>
  );
}

export default App;