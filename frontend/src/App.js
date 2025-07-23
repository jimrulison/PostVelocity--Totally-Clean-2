import React, { useState, useEffect, useRef } from 'react';
import './App.css';

function App() {
  // Core application state
  const [activeTab, setActiveTab] = useState('content');
  const [companies, setCompanies] = useState([]);
  const [selectedCompany, setSelectedCompany] = useState('');
  const [userStatus, setUserStatus] = useState({
    type: 'free',
    generationsUsed: 0,
    generationsLimit: 10,
    trialDaysLeft: 0,
    isPaidUser: false,
    isBetaTester: false,
    hasSeOAddon: false,
    seoAddonStatus: 'inactive'
  });

  // Content generation state
  const [contentTopic, setContentTopic] = useState('');
  const [selectedPlatforms, setSelectedPlatforms] = useState([]);
  const [generatedContent, setGeneratedContent] = useState({});
  const [isGenerating, setIsGenerating] = useState(false);

  // Modal states
  const [showPaymentModal, setShowPaymentModal] = useState(false);
  const [showTrialModal, setShowTrialModal] = useState(false);
  const [showBetaModal, setShowBetaModal] = useState(false);
  const [showAdminPanel, setShowAdminPanel] = useState(false);
  const [showSeOUpgradeModal, setShowSeOUpgradeModal] = useState(false);

  // Voice input state
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const recognitionRef = useRef(null);

  // Authentication check
  useEffect(() => {
    checkAuthenticationStatus();
    loadCompanies();
    checkTrialParams();
  }, []);

  const checkAuthenticationStatus = () => {
    const currentUser = JSON.parse(localStorage.getItem('currentUser') || '{}');
    const authToken = localStorage.getItem('authToken');
    
    if (!currentUser.email && !authToken) {
      // Redirect to appropriate login page
      window.location.href = '/user-login';
      return;
    }
    
    // Set initial user status based on stored data
    const storedStatus = JSON.parse(localStorage.getItem('userStatus') || '{}');
    setUserStatus(prev => ({
      ...prev,
      ...storedStatus,
      isPaidUser: currentUser.role === 'admin' || storedStatus.isPaidUser || false,
      isBetaTester: storedStatus.isBetaTester || false
    }));
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

  const loadCompanies = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/companies`);
      if (response.ok) {
        const data = await response.json();
        setCompanies(data.companies || []);
        if (data.companies && data.companies.length > 0) {
          setSelectedCompany(data.companies[0].id);
        }
      }
    } catch (error) {
      console.error('Error loading companies:', error);
    }
  };

  // Platform configurations
  const platforms = [
    { id: 'instagram', name: 'Instagram', color: '#E4405F', icon: '📷' },
    { id: 'tiktok', name: 'TikTok', color: '#000000', icon: '🎵' },
    { id: 'facebook', name: 'Facebook', color: '#1877F2', icon: '👥' },
    { id: 'youtube', name: 'YouTube', color: '#FF0000', icon: '📺' },
    { id: 'linkedin', name: 'LinkedIn', color: '#0A66C2', icon: '💼' },
    { id: 'x', name: 'X (Twitter)', color: '#000000', icon: '🐦' },
    { id: 'whatsapp', name: 'WhatsApp', color: '#25D366', icon: '💬' },
    { id: 'snapchat', name: 'Snapchat', color: '#FFFC00', icon: '👻' }
  ];

  // Tab configuration
  const tabs = [
    { id: 'content', name: '📝 Content Hub', show: true },
    { id: 'analytics', name: '📊 Analytics', show: true },
    { id: 'media', name: '📸 Media Library', show: true },
    { id: 'calendar', name: '📅 Calendar', show: true },
    { id: 'automation', name: '🤖 Automation', show: true },
    { id: 'training', name: '🎓 Training', show: true },
    { id: 'beta-feedback', name: '💬 Beta Feedback', show: userStatus.isBetaTester },
    { id: 'seo-monitor', name: '🔍 SEO Monitor', show: userStatus.isPaidUser && userStatus.hasSeOAddon }
  ];

  const visibleTabs = tabs.filter(tab => tab.show);

  // Content generation function
  const generateContent = async () => {
    if (!contentTopic.trim() || selectedPlatforms.length === 0) {
      alert('Please enter a topic and select at least one platform');
      return;
    }

    // Check usage limits
    if (userStatus.type === 'free' && userStatus.generationsUsed >= userStatus.generationsLimit) {
      setShowPaymentModal(true);
      return;
    }

    setIsGenerating(true);
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/generate-content`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          topic: contentTopic,
          platforms: selectedPlatforms,
          company_id: selectedCompany || 'demo-company'
        })
      });

      if (response.ok) {
        const data = await response.json();
        setGeneratedContent(data.content || {});
        
        // Update usage count
        setUserStatus(prev => ({
          ...prev,
          generationsUsed: prev.generationsUsed + 1
        }));
      } else {
        alert('Error generating content. Please try again.');
      }
    } catch (error) {
      console.error('Content generation error:', error);
      alert('Error generating content. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  // Voice input functions
  const startListening = () => {
    if ('webkitSpeechRecognition' in window) {
      const recognition = new window.webkitSpeechRecognition();
      recognitionRef.current = recognition;
      
      recognition.continuous = false;
      recognition.interimResults = true;
      recognition.lang = 'en-US';
      
      recognition.onstart = () => setIsListening(true);
      recognition.onend = () => setIsListening(false);
      
      recognition.onresult = (event) => {
        const result = event.results[0][0].transcript;
        setTranscript(result);
        setContentTopic(result);
      };
      
      recognition.start();
    } else {
      alert('Speech recognition not supported in this browser');
    }
  };

  const stopListening = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
    }
  };

  // Payment and upgrade functions
  const startFreeTrial = () => {
    setUserStatus(prev => ({
      ...prev,
      type: 'trial',
      trialDaysLeft: 7,
      generationsLimit: 50
    }));
    setShowTrialModal(false);
    localStorage.setItem('userStatus', JSON.stringify({
      ...userStatus,
      type: 'trial',
      trialDaysLeft: 7,
      generationsLimit: 50
    }));
  };

  const purchasePlan = (planType) => {
    setUserStatus(prev => ({
      ...prev,
      type: 'paid',
      isPaidUser: true,
      generationsLimit: -1
    }));
    setShowPaymentModal(false);
    localStorage.setItem('userStatus', JSON.stringify({
      ...userStatus,
      type: 'paid',
      isPaidUser: true,
      generationsLimit: -1
    }));
    alert(`${planType} plan activated! Welcome to PostVelocity Pro!`);
  };

  const joinBetaProgram = () => {
    setUserStatus(prev => ({
      ...prev,
      isBetaTester: true,
      generationsLimit: 200
    }));
    setShowBetaModal(false);
    localStorage.setItem('userStatus', JSON.stringify({
      ...userStatus,
      isBetaTester: true,
      generationsLimit: 200
    }));
  };

  const purchaseSeOAddon = (plan) => {
    console.log(`SEO ${plan} button clicked`);
    console.log(`purchaseSeOAddon called with plan: ${plan}`);
    
    // Simulate successful purchase
    const updatedStatus = {
      ...userStatus,
      hasSeOAddon: true,
      seoAddonStatus: 'active'
    };
    
    setUserStatus(updatedStatus);
    localStorage.setItem('userStatus', JSON.stringify(updatedStatus));
    setShowSeOUpgradeModal(false);
    
    alert('SEO Monitoring Add-on activated!');
  };

  const renderUsageStatus = () => {
    const currentUser = JSON.parse(localStorage.getItem('currentUser') || '{}');
    
    if (userStatus.isPaidUser) {
      if (userStatus.isBetaTester) {
        return (
          <div className="bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-sm font-medium">
            🎉 Beta VIP - Unlimited
          </div>
        );
      }
      return (
        <div className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium">
          💎 Lifetime - Unlimited
        </div>
      );
    }
    
    if (userStatus.isBetaTester) {
      const remaining = userStatus.generationsLimit - userStatus.generationsUsed;
      return (
        <div className="bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-sm font-medium">
          🚀 Beta Tester - {remaining} uses left
        </div>
      );
    }
    
    if (userStatus.type === 'trial') {
      const remaining = userStatus.generationsLimit - userStatus.generationsUsed;
      return (
        <div className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium">
          ⏰ Trial: {userStatus.trialDaysLeft} days, {remaining} uses left
        </div>
      );
    }
    
    return (
      <div className="bg-gray-100 text-gray-800 px-3 py-1 rounded-full text-sm font-medium">
        👋 Free User - Join Beta
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <div className="flex items-center">
              <div className="text-2xl font-bold text-blue-600">🚀 PostVelocity</div>
            </div>
            
            {/* Company Selection */}
            <div className="flex items-center space-x-4">
              <select 
                value={selectedCompany} 
                onChange={(e) => setSelectedCompany(e.target.value)}
                className="border rounded-lg px-3 py-2 text-sm"
              >
                <option value="">Select Company</option>
                {companies.map(company => (
                  <option key={company.id} value={company.id}>
                    {company.name}
                  </option>
                ))}
              </select>
            </div>
            
            {/* User Status and Actions */}
            <div className="flex items-center space-x-3">
              {renderUsageStatus()}
              
              {!userStatus.isPaidUser && (
                <button
                  onClick={() => setShowPaymentModal(true)}
                  className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:from-blue-600 hover:to-purple-700 transition-all"
                >
                  ⚡ Upgrade
                </button>
              )}
              
              {userStatus.isPaidUser && !userStatus.hasSeOAddon && (
                <button
                  onClick={() => setShowSeOUpgradeModal(true)}
                  className="bg-gradient-to-r from-green-500 to-teal-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:from-green-600 hover:to-teal-700 transition-all"
                >
                  🔍 SEO Addon
                </button>
              )}
              
              {JSON.parse(localStorage.getItem('currentUser') || '{}').role === 'admin' && (
                <button
                  onClick={() => setShowAdminPanel(true)}
                  className="bg-red-500 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-red-600 transition-all"
                >
                  🔐 Admin
                </button>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Tab Navigation */}
        <div className="mb-8">
          <nav className="flex space-x-8 border-b">
            {visibleTabs.map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab.name}
              </button>
            ))}
          </nav>
        </div>

        {/* Tab Content */}
        {activeTab === 'content' && (
          <div className="space-y-8">
            {/* Content Generation Section */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h2 className="text-xl font-semibold mb-6">🤖 AI Content Generation</h2>
              
              {/* Content Topic Input */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Content Topic
                </label>
                <div className="flex space-x-2">
                  <input
                    type="text"
                    value={contentTopic}
                    onChange={(e) => setContentTopic(e.target.value)}
                    placeholder="Enter your content topic (e.g., 'Construction safety tips for winter')"
                    className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                  <button
                    onClick={isListening ? stopListening : startListening}
                    className={`px-4 py-2 rounded-lg font-medium ${
                      isListening 
                        ? 'bg-red-500 text-white hover:bg-red-600' 
                        : 'bg-green-500 text-white hover:bg-green-600'
                    }`}
                  >
                    {isListening ? '🛑 Stop' : '🎤 Voice'}
                  </button>
                </div>
                {isListening && (
                  <div className="mt-2 text-sm text-gray-600">
                    🎙️ Listening... Speak your content topic
                  </div>
                )}
                {transcript && (
                  <div className="mt-2 text-sm text-green-600">
                    Transcript: {transcript}
                  </div>
                )}
              </div>

              {/* Platform Selection */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-3">
                  Select Platforms
                </label>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  {platforms.map(platform => (
                    <label
                      key={platform.id}
                      className={`flex items-center p-3 border rounded-lg cursor-pointer transition-all ${
                        selectedPlatforms.includes(platform.id)
                          ? 'border-blue-500 bg-blue-50'
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                    >
                      <input
                        type="checkbox"
                        checked={selectedPlatforms.includes(platform.id)}
                        onChange={(e) => {
                          if (e.target.checked) {
                            setSelectedPlatforms([...selectedPlatforms, platform.id]);
                          } else {
                            setSelectedPlatforms(selectedPlatforms.filter(p => p !== platform.id));
                          }
                        }}
                        className="sr-only"
                      />
                      <span className="text-lg mr-2">{platform.icon}</span>
                      <span className="text-sm font-medium">{platform.name}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* Generate Button */}
              <button
                onClick={generateContent}
                disabled={isGenerating || !contentTopic.trim() || selectedPlatforms.length === 0}
                className="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white py-3 px-6 rounded-lg font-medium hover:from-blue-600 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
              >
                {isGenerating ? '🔄 Generating Content...' : '✨ Generate Content'}
              </button>
            </div>

            {/* Generated Content Display */}
            {Object.keys(generatedContent).length > 0 && (
              <div className="bg-white rounded-lg shadow-sm p-6">
                <h3 className="text-lg font-semibold mb-4">📝 Generated Content</h3>
                <div className="space-y-4">
                  {Object.entries(generatedContent).map(([platform, content]) => (
                    <div key={platform} className="border rounded-lg p-4">
                      <h4 className="font-medium text-gray-900 mb-2">
                        {platforms.find(p => p.id === platform)?.icon} {platforms.find(p => p.id === platform)?.name}
                      </h4>
                      <p className="text-gray-700 whitespace-pre-wrap">{content}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Other tabs placeholder content */}
        {activeTab !== 'content' && (
          <div className="bg-white rounded-lg shadow-sm p-8 text-center">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">
              {tabs.find(t => t.id === activeTab)?.name}
            </h2>
            <p className="text-gray-600">
              This section is being rebuilt with all your original features. Coming soon!
            </p>
          </div>
        )}
      </div>

      {/* Modals */}
      {/* Payment Modal */}
      {showPaymentModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-8 max-w-md w-full mx-4">
            <h3 className="text-xl font-semibold mb-4">⚡ Upgrade to Pro</h3>
            <p className="text-gray-600 mb-6">
              You've reached your free limit. Upgrade for unlimited content generation!
            </p>
            <div className="space-y-3">
              <button
                onClick={() => purchasePlan('Professional')}
                className="w-full bg-blue-500 text-white py-3 px-4 rounded-lg font-medium hover:bg-blue-600"
              >
                Professional - $49/month
              </button>
              <button
                onClick={() => purchasePlan('Enterprise')}
                className="w-full bg-purple-500 text-white py-3 px-4 rounded-lg font-medium hover:bg-purple-600"
              >
                Enterprise - $149/month
              </button>
            </div>
            <button
              onClick={() => setShowPaymentModal(false)}
              className="w-full mt-4 text-gray-500 hover:text-gray-700"
            >
              Maybe Later
            </button>
          </div>
        </div>
      )}

      {/* Trial Modal */}
      {showTrialModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-8 max-w-md w-full mx-4">
            <h3 className="text-xl font-semibold mb-4">🎉 Start Your Free Trial</h3>
            <p className="text-gray-600 mb-6">
              Get 7 days free access with 50 content generations and all AI features!
            </p>
            <div className="space-y-3">
              <button
                onClick={startFreeTrial}
                className="w-full bg-green-500 text-white py-3 px-4 rounded-lg font-medium hover:bg-green-600"
              >
                Start Free Trial
              </button>
              <button
                onClick={() => setShowTrialModal(false)}
                className="w-full text-gray-500 hover:text-gray-700"
              >
                Maybe Later
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Beta Modal */}
      {showBetaModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-8 max-w-md w-full mx-4">
            <h3 className="text-xl font-semibold mb-4">🚀 Join Beta Program</h3>
            <p className="text-gray-600 mb-6">
              Get early access to new features with 200 generations and beta feedback access!
            </p>
            <div className="space-y-3">
              <button
                onClick={joinBetaProgram}
                className="w-full bg-purple-500 text-white py-3 px-4 rounded-lg font-medium hover:bg-purple-600"
              >
                Join Beta Program
              </button>
              <button
                onClick={() => setShowBetaModal(false)}
                className="w-full text-gray-500 hover:text-gray-700"
              >
                Maybe Later
              </button>
            </div>
          </div>
        </div>
      )}

      {/* SEO Upgrade Modal */}
      {showSeOUpgradeModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-8 max-w-md w-full mx-4">
            <h3 className="text-xl font-semibold mb-4">🔍 SEO Monitoring Add-on</h3>
            <p className="text-gray-600 mb-6">
              Add comprehensive SEO monitoring and keyword analysis to your account.
            </p>
            <div className="space-y-3">
              <button
                onClick={() => purchaseSeOAddon('standard')}
                className="w-full bg-green-500 text-white py-3 px-4 rounded-lg font-medium hover:bg-green-600"
              >
                Purchase Standard - $297
              </button>
              <button
                onClick={() => purchaseSeOAddon('pro')}
                className="w-full bg-blue-500 text-white py-3 px-4 rounded-lg font-medium hover:bg-blue-600"
              >
                Purchase Pro - $497
              </button>
            </div>
            <button
              onClick={() => setShowSeOUpgradeModal(false)}
              className="w-full mt-4 text-gray-500 hover:text-gray-700"
            >
              Maybe Later
            </button>
          </div>
        </div>
      )}

      {/* Admin Panel Modal */}
      {showAdminPanel && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-8 max-w-2xl w-full mx-4 max-h-96 overflow-y-auto">
            <h3 className="text-xl font-semibold mb-4">🔐 Admin Panel</h3>
            <p className="text-gray-600 mb-4">Quick admin access - for full panel visit /admin</p>
            <div className="space-y-2">
              <a href="/admin" target="_blank" className="block w-full bg-red-500 text-white py-2 px-4 rounded text-center hover:bg-red-600">
                Open Full Admin Panel
              </a>
              <button
                onClick={() => setShowAdminPanel(false)}
                className="w-full text-gray-500 hover:text-gray-700 py-2"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;