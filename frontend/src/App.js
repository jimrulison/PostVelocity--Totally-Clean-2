import React, { useState, useEffect } from 'react';
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

  const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

  useEffect(() => {
    fetchCompanies();
    fetchPlatforms();
    fetchMonthlyMediaRequests();
  }, []);

  useEffect(() => {
    if (selectedCompany) {
      fetchCompanyMedia();
      fetchRoiData();
      fetchTrendingHashtags();
    }
  }, [selectedCompany]);

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
      alert('Please fill in company, topic, and select at least one platform');
      return;
    }

    setLoading(true);
    try {
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
      setCurrentView('results');
    } catch (error) {
      console.error('Error generating content:', error);
      alert('Error generating content. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Quick Action Functions
  const generateQuickContent = async (topic, platforms) => {
    setQuickActionLoading(true);
    try {
      const quickRequest = {
        ...formData,
        topic,
        platforms: platforms || ['instagram', 'facebook', 'linkedin']
      };
      
      const response = await fetch(`${backendUrl}/api/generate-content`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(quickRequest),
      });

      if (!response.ok) {
        throw new Error('Failed to generate quick content');
      }

      const data = await response.json();
      setResults(data);
      setCurrentView('results');
      setActiveTab('content-hub');
    } catch (error) {
      console.error('Error generating quick content:', error);
      alert('Error generating quick content. Please try again.');
    } finally {
      setQuickActionLoading(false);
    }
  };

  const generateBulkContent = async (topics) => {
    setBulkContentLoading(true);
    try {
      const bulkResults = [];
      
      for (const topic of topics) {
        const response = await fetch(`${backendUrl}/api/generate-content`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            ...formData,
            topic,
            platforms: ['instagram', 'facebook', 'linkedin', 'tiktok']
          }),
        });

        if (response.ok) {
          const data = await response.json();
          bulkResults.push(data);
        }
      }
      
      setResults({
        bulk_results: bulkResults,
        is_bulk: true,
        generated_content: bulkResults.flatMap(r => r.generated_content || [])
      });
      setCurrentView('results');
      setActiveTab('content-hub');
    } catch (error) {
      console.error('Error generating bulk content:', error);
      alert('Error generating bulk content. Please try again.');
    } finally {
      setBulkContentLoading(false);
    }
  };

  const scheduleAllContent = async () => {
    if (!results?.generated_content) return;
    
    const now = new Date();
    const schedulePromises = results.generated_content.map((content, index) => {
      const scheduledTime = new Date(now);
      scheduledTime.setHours(now.getHours() + index * 2);
      
      return schedulePost(content.platform, content.content, content.hashtags, scheduledTime);
    });
    
    try {
      await Promise.all(schedulePromises);
      alert('All content scheduled successfully!');
    } catch (error) {
      console.error('Error scheduling bulk content:', error);
      alert('Error scheduling some content. Please try again.');
    }
  };

  const schedulePost = async (platform, content, hashtags, scheduledTime) => {
    try {
      const response = await fetch(`${backendUrl}/api/schedule-post`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          company_id: selectedCompany.id,
          platform,
          content,
          hashtags,
          scheduled_time: scheduledTime,
          topic: formData.topic,
          media_files: []
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to schedule post');
      }

      return true;
    } catch (error) {
      console.error('Error scheduling post:', error);
      throw error;
    }
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
      alert('Company created successfully!');
      setCurrentView('dashboard');
    } catch (error) {
      console.error('Error creating company:', error);
      alert('Error creating company. Please try again.');
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    alert('Content copied to clipboard!');
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
                  <h1 className="text-2xl font-bold text-gray-900">AI Social Media Manager</h1>
                </div>
                {selectedCompany && (
                  <div className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium">
                    {selectedCompany.name}
                  </div>
                )}
              </div>
              <div className="flex items-center space-x-4">
                <button
                  onClick={() => setCurrentView('add-company')}
                  className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors"
                >
                  + Add Company
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
                { id: 'automation', label: 'Automation', icon: '🤖' }
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
        </main>
      </div>
    );
  };

  // Content Hub Tab - The main content generation area
  const ContentHubTab = () => {
    const [quickTopic, setQuickTopic] = useState('');
    const [showBulkForm, setShowBulkForm] = useState(false);
    const [bulkTopics, setBulkTopics] = useState('');

    const quickTopicSuggestions = [
      'Weekly Safety Tips',
      'Equipment Maintenance',
      'Team Achievement',
      'Industry News Update',
      'Training Session Highlights'
    ];

    return (
      <div className="space-y-6">
        {/* Quick Actions */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">⚡ Quick Actions</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <h3 className="font-semibold text-gray-800 mb-2">🎯 Generate Content</h3>
              <div className="space-y-3">
                <input
                  type="text"
                  value={quickTopic}
                  onChange={(e) => setQuickTopic(e.target.value)}
                  placeholder="Enter your topic..."
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <button
                  onClick={() => generateQuickContent(quickTopic)}
                  disabled={!quickTopic || quickActionLoading}
                  className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
                >
                  {quickActionLoading ? 'Generating...' : 'Generate Now'}
                </button>
              </div>
            </div>

            <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <h3 className="font-semibold text-gray-800 mb-2">📚 Bulk Content</h3>
              <div className="space-y-3">
                <button
                  onClick={() => setShowBulkForm(!showBulkForm)}
                  className="w-full bg-purple-600 text-white py-2 px-4 rounded-lg hover:bg-purple-700 transition-colors"
                >
                  Create Multiple Posts
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
                      onClick={() => generateBulkContent(bulkTopics.split('\n').filter(t => t.trim()))}
                      disabled={!bulkTopics || bulkContentLoading}
                      className="w-full bg-purple-600 text-white py-2 px-4 rounded-lg hover:bg-purple-700 transition-colors disabled:opacity-50"
                    >
                      {bulkContentLoading ? 'Generating...' : 'Generate All'}
                    </button>
                  </div>
                )}
              </div>
            </div>

            <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <h3 className="font-semibold text-gray-800 mb-2">📅 Auto Schedule</h3>
              <div className="space-y-3">
                <p className="text-sm text-gray-600">Schedule all generated content automatically</p>
                <button
                  onClick={scheduleAllContent}
                  disabled={!results?.generated_content}
                  className="w-full bg-green-600 text-white py-2 px-4 rounded-lg hover:bg-green-700 transition-colors disabled:opacity-50"
                >
                  Schedule All Posts
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Quick Topic Suggestions */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">💡 Topic Suggestions</h3>
          <div className="flex flex-wrap gap-2">
            {quickTopicSuggestions.map((topic) => (
              <button
                key={topic}
                onClick={() => generateQuickContent(topic)}
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

  // Analytics Tab
  const AnalyticsTab = () => {
    return (
      <div className="space-y-6">
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">📊 Analytics Dashboard</h2>
          
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

  // Media Tab
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
        alert(`Successfully uploaded ${files.length} file(s)!`);
      } catch (error) {
        console.error('Error uploading media:', error);
        alert('Error uploading media. Please try again.');
      } finally {
        setUploadingMedia(false);
      }
    };

    const handleUploadSubmit = (e) => {
      e.preventDefault();
      if (!uploadForm.files || uploadForm.files.length === 0) {
        alert('Please select files to upload');
        return;
      }
      handleMediaUpload(uploadForm.files, uploadForm.category, uploadForm.description, uploadForm.tags);
      setUploadForm({ files: null, category: 'training', description: '', tags: '' });
    };

    return (
      <div className="space-y-6">
        {/* Upload Form */}
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

        {/* Media Library */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-xl font-semibold text-gray-800 mb-4">📂 Media Library</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {mediaFiles.map((media) => (
              <div key={media.id} className="bg-gray-50 rounded-lg p-4 border border-gray-200">
                <div className="flex items-start justify-between mb-2">
                  <div className="flex items-center space-x-2">
                    <span className="text-lg">{MEDIA_CATEGORIES[media.category]?.icon}</span>
                    <span className="text-sm font-medium text-gray-700 capitalize">{media.category}</span>
                  </div>
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

  // Calendar Tab
  const CalendarTab = () => {
    return (
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">📅 Content Calendar</h2>
        <div className="text-center py-8 text-gray-500">
          <p className="text-lg mb-2">📅 Calendar Coming Soon</p>
          <p className="text-sm">Schedule and manage your content calendar</p>
        </div>
      </div>
    );
  };

  // Automation Tab
  const AutomationTab = () => {
    return (
      <div className="space-y-6">
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">🤖 Automation Center</h2>
          
          {/* Media Requests */}
          {mediaRequests.length > 0 && (
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
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
                        onClick={() => {
                          // Mark as sent functionality
                          alert('Media request marked as sent!');
                        }}
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

          {/* Automation Tools */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="border border-gray-200 rounded-lg p-4">
              <h3 className="font-semibold text-gray-800 mb-2">🔄 Content Automation</h3>
              <p className="text-sm text-gray-600 mb-4">Set up automated content generation for recurring topics</p>
              <button className="w-full bg-purple-600 text-white py-2 px-4 rounded-lg hover:bg-purple-700 transition-colors">
                Configure Automation
              </button>
            </div>

            <div className="border border-gray-200 rounded-lg p-4">
              <h3 className="font-semibold text-gray-800 mb-2">📈 Performance Monitoring</h3>
              <p className="text-sm text-gray-600 mb-4">Automatically track and optimize content performance</p>
              <button className="w-full bg-green-600 text-white py-2 px-4 rounded-lg hover:bg-green-700 transition-colors">
                Setup Monitoring
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  };

  // Results View Component
  const ResultsView = () => {
    if (!results) return null;

    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="mb-6">
            <button
              onClick={() => setCurrentView('dashboard')}
              className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors"
            >
              ← Back to Dashboard
            </button>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">🎉 Generated Content</h2>
            
            {results.is_bulk ? (
              <div className="space-y-6">
                <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                  <h3 className="text-lg font-semibold text-green-800 mb-2">
                    📚 Bulk Content Generated
                  </h3>
                  <p className="text-sm text-green-700">
                    Generated {results.bulk_results?.length || 0} content sets with {results.generated_content?.length || 0} total posts
                  </p>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {results.generated_content?.map((content, index) => (
                    <div key={index} className="border border-gray-200 rounded-lg p-4">
                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center space-x-2">
                          <span className="text-2xl">{PLATFORM_ICONS[content.platform]}</span>
                          <h3 className="text-lg font-semibold capitalize">{content.platform}</h3>
                        </div>
                        <button
                          onClick={() => copyToClipboard(content.content)}
                          className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700 transition-colors"
                        >
                          Copy
                        </button>
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
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="space-y-6">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {results.generated_content?.map((content, index) => (
                    <div key={index} className="border border-gray-200 rounded-lg p-4">
                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center space-x-2">
                          <span className="text-2xl">{PLATFORM_ICONS[content.platform]}</span>
                          <h3 className="text-lg font-semibold capitalize">{content.platform}</h3>
                        </div>
                        <button
                          onClick={() => copyToClipboard(content.content)}
                          className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700 transition-colors"
                        >
                          Copy
                        </button>
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
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
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