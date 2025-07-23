import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('content');
  const [contentTopic, setContentTopic] = useState('');
  const [selectedPlatforms, setSelectedPlatforms] = useState([]);
  const [generatedContent, setGeneratedContent] = useState({});
  const [isGenerating, setIsGenerating] = useState(false);
  const [userStatus, setUserStatus] = useState({ type: 'free', generationsUsed: 0, generationsLimit: 10 });

  // Smart Quick Actions (from your original app)
  const quickActions = [
    { id: 'smart_generate', name: '🤖 Smart Generate', description: 'AI-powered content for all platforms' },
    { id: 'weekly_batch', name: '📅 Weekly Batch', description: 'Generate a week of content' },
    { id: 'emergency_post', name: '🚨 Emergency Post', description: 'Quick crisis response' },
    { id: 'voice_input', name: '🎤 Voice Input', description: 'Speak your content ideas' }
  ];

  // Trending Topics (from your original app)
  const trendingTopics = [
    { topic: 'AI in Construction', engagement: '2.3M', trend: '+15%' },
    { topic: 'Green Building', engagement: '1.8M', trend: '+22%' },
    { topic: 'Remote Work Safety', engagement: '1.2M', trend: '+8%' },
    { topic: 'Equipment Innovation', engagement: '945K', trend: '+18%' }
  ];

  // Industry Templates (from your original app)
  const industryTemplates = [
    { name: 'Safety Reminder', template: 'Safety first! Remember to [SAFETY_TIP] when [ACTIVITY]. #SafetyFirst' },
    { name: 'Equipment Showcase', template: 'Check out our latest [EQUIPMENT] in action! Perfect for [PROJECT_TYPE]. #Innovation' },
    { name: 'Team Achievement', template: 'Proud of our team for [ACHIEVEMENT]! Great work on [PROJECT]. #TeamWork' },
    { name: 'Project Update', template: 'Progress update on [PROJECT_NAME]: [MILESTONE_ACHIEVED]. On track for [COMPLETION_DATE]!' }
  ];

  // Topic Suggestions (from your original app)
  const topicSuggestions = [
    'Construction safety tips', 'Equipment maintenance', 'Team achievements', 
    'Project milestones', 'Industry innovations', 'Weather preparations'
  ];

  // Premium Content Enhancers (from your original app)
  const premiumEnhancers = [
    { name: 'Hashtags Generator', description: 'AI-powered hashtag suggestions', premium: true },
    { name: 'SEO Keywords', description: 'Optimize for search engines', premium: true },
    { name: 'Competitor Analysis', description: 'See what competitors are posting', premium: true }
  ];

  const platforms = [
    { id: 'instagram', name: 'Instagram', icon: '📸' },
    { id: 'tiktok', name: 'TikTok', icon: '🎵' },
    { id: 'facebook', name: 'Facebook', icon: '👥' },
    { id: 'youtube', name: 'YouTube', icon: '📺' },
    { id: 'linkedin', name: 'LinkedIn', icon: '💼' },
    { id: 'x', name: 'X (Twitter)', icon: '🐦' }
  ];

  const generateContent = async () => {
    if (!contentTopic.trim() || selectedPlatforms.length === 0) return;
    
    setIsGenerating(true);
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/generate-content`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic: contentTopic, platforms: selectedPlatforms })
      });
      
      if (response.ok) {
        const data = await response.json();
        setGeneratedContent(data.content || {});
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-blue-600">🚀 PostVelocity</h1>
            <div className="flex items-center space-x-4">
              <span className="bg-gray-100 px-3 py-1 rounded-full text-sm">Free User</span>
              <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
                ⚡ Upgrade
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Smart Quick Actions */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold mb-4">⚡ Smart Quick Actions</h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {quickActions.map(action => (
              <div key={action.id} className="bg-white p-4 rounded-lg shadow-sm border hover:shadow-md transition-shadow cursor-pointer">
                <h3 className="font-medium text-gray-900">{action.name}</h3>
                <p className="text-sm text-gray-600 mt-1">{action.description}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Trending Topics */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold mb-4">📈 Trending Topics</h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {trendingTopics.map((topic, index) => (
              <div key={index} className="bg-white p-4 rounded-lg shadow-sm border">
                <h3 className="font-medium text-gray-900">{topic.topic}</h3>
                <div className="flex justify-between items-center mt-2">
                  <span className="text-sm text-gray-600">{topic.engagement}</span>
                  <span className="text-sm text-green-600 font-medium">{topic.trend}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Content Generation */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
          <h2 className="text-xl font-semibold mb-6">🤖 AI Content Generation</h2>
          
          {/* Topic Input */}
          <div className="mb-6">
            <label className="block text-sm font-medium mb-2">Content Topic</label>
            <input
              type="text"
              value={contentTopic}
              onChange={(e) => setContentTopic(e.target.value)}
              placeholder="Enter your content topic..."
              className="w-full border rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {/* Topic Suggestions */}
          <div className="mb-6">
            <label className="block text-sm font-medium mb-2">💡 Topic Suggestions</label>
            <div className="flex flex-wrap gap-2">
              {topicSuggestions.map((suggestion, index) => (
                <button
                  key={index}
                  onClick={() => setContentTopic(suggestion)}
                  className="bg-gray-100 hover:bg-gray-200 px-3 py-1 rounded-full text-sm transition-colors"
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>

          {/* Platform Selection */}
          <div className="mb-6">
            <label className="block text-sm font-medium mb-3">Select Platforms</label>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {platforms.map(platform => (
                <label key={platform.id} className={`flex items-center p-3 border rounded-lg cursor-pointer ${
                  selectedPlatforms.includes(platform.id) ? 'border-blue-500 bg-blue-50' : 'border-gray-200'
                }`}>
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
            className="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white py-3 px-6 rounded-lg font-medium hover:from-blue-600 hover:to-purple-700 disabled:opacity-50 transition-all"
          >
            {isGenerating ? '🔄 Generating Content...' : '✨ Generate Content'}
          </button>
        </div>

        {/* Industry Templates */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold mb-4">📋 Industry Templates</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {industryTemplates.map((template, index) => (
              <div key={index} className="bg-white p-4 rounded-lg shadow-sm border">
                <h3 className="font-medium text-gray-900 mb-2">{template.name}</h3>
                <p className="text-sm text-gray-600">{template.template}</p>
                <button className="mt-2 text-blue-600 text-sm hover:underline">Use Template</button>
              </div>
            ))}
          </div>
        </div>

        {/* Premium Content Enhancers */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold mb-4">⭐ Premium Content Enhancers</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {premiumEnhancers.map((enhancer, index) => (
              <div key={index} className="bg-white p-4 rounded-lg shadow-sm border">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-medium text-gray-900">{enhancer.name}</h3>
                  <span className="bg-yellow-100 text-yellow-800 px-2 py-1 rounded text-xs">PRO</span>
                </div>
                <p className="text-sm text-gray-600">{enhancer.description}</p>
              </div>
            ))}
          </div>
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
    </div>
  );
}

export default App;