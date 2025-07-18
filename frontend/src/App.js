import React, { useState, useEffect } from 'react';
import './App.css';

const PLATFORM_ICONS = {
  instagram: '📸',
  tiktok: '🎵',
  facebook: '👥',
  youtube: '📺',
  whatsapp: '💬',
  snapchat: '👻',
  x: '✖️'
};

const PLATFORM_COLORS = {
  instagram: 'bg-gradient-to-r from-purple-500 to-pink-500',
  tiktok: 'bg-gradient-to-r from-black to-gray-800',
  facebook: 'bg-blue-600',
  youtube: 'bg-red-600',
  whatsapp: 'bg-green-500',
  snapchat: 'bg-yellow-400',
  x: 'bg-gray-900'
};

function App() {
  const [formData, setFormData] = useState({
    company_name: '',
    topic: '',
    platforms: [],
    audience_level: 'general',
    additional_context: ''
  });
  
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [examples, setExamples] = useState(null);
  const [availablePlatforms, setAvailablePlatforms] = useState([]);

  const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

  useEffect(() => {
    fetchExamples();
    fetchPlatforms();
  }, []);

  const fetchExamples = async () => {
    try {
      const response = await fetch(`${backendUrl}/api/content-examples`);
      const data = await response.json();
      setExamples(data);
    } catch (error) {
      console.error('Error fetching examples:', error);
    }
  };

  const fetchPlatforms = async () => {
    try {
      const response = await fetch(`${backendUrl}/api/platforms`);
      const data = await response.json();
      setAvailablePlatforms(data.platforms);
    } catch (error) {
      console.error('Error fetching platforms:', error);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
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
    if (!formData.company_name || !formData.topic || formData.platforms.length === 0) {
      alert('Please fill in company name, topic, and select at least one platform');
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
    } catch (error) {
      console.error('Error generating content:', error);
      alert('Error generating content. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    alert('Content copied to clipboard!');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            🏗️ Social Media Content Generator
          </h1>
          <p className="text-gray-600 text-lg">
            AI-powered content creation for construction & environmental training companies
          </p>
        </div>

        {/* Main Content */}
        <div className="max-w-7xl mx-auto">
          {!results ? (
            /* Input Form */
            <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
              <form onSubmit={handleSubmit} className="space-y-6">
                {/* Company Name */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Company Name *
                  </label>
                  <input
                    type="text"
                    name="company_name"
                    value={formData.company_name}
                    onChange={handleInputChange}
                    placeholder="e.g., SafetyFirst Environmental Training"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    required
                  />
                </div>

                {/* Topic */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Topic *
                  </label>
                  <input
                    type="text"
                    name="topic"
                    value={formData.topic}
                    onChange={handleInputChange}
                    placeholder="e.g., OSHA Fall Protection Standards"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    required
                  />
                  {examples && (
                    <div className="mt-2">
                      <p className="text-sm text-gray-500 mb-2">Example topics:</p>
                      <div className="flex flex-wrap gap-2">
                        {examples.topics.slice(0, 5).map(topic => (
                          <button
                            key={topic}
                            type="button"
                            onClick={() => setFormData(prev => ({ ...prev, topic }))}
                            className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full hover:bg-blue-200 transition-colors"
                          >
                            {topic}
                          </button>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                {/* Platforms */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Select Platforms *
                  </label>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                    {availablePlatforms.map(platform => (
                      <button
                        key={platform}
                        type="button"
                        onClick={() => handlePlatformToggle(platform)}
                        className={`p-3 rounded-lg border-2 transition-all ${
                          formData.platforms.includes(platform)
                            ? `${PLATFORM_COLORS[platform]} text-white border-transparent`
                            : 'bg-white border-gray-300 hover:border-gray-400'
                        }`}
                      >
                        <div className="text-2xl mb-1">{PLATFORM_ICONS[platform]}</div>
                        <div className="text-sm font-medium capitalize">{platform}</div>
                      </button>
                    ))}
                  </div>
                </div>

                {/* Audience Level */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Audience Level
                  </label>
                  <select
                    name="audience_level"
                    value={formData.audience_level}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="general">General</option>
                    <option value="beginner">Beginner</option>
                    <option value="intermediate">Intermediate</option>
                    <option value="advanced">Advanced</option>
                    <option value="management">Management</option>
                  </select>
                </div>

                {/* Additional Context */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Additional Context (Optional)
                  </label>
                  <textarea
                    name="additional_context"
                    value={formData.additional_context}
                    onChange={handleInputChange}
                    placeholder="Any specific requirements, recent news, or context..."
                    rows="3"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                {/* Submit Button */}
                <button
                  type="submit"
                  disabled={loading}
                  className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? (
                    <div className="flex items-center justify-center">
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                      Generating Content...
                    </div>
                  ) : (
                    'Generate Content'
                  )}
                </button>
              </form>
            </div>
          ) : (
            /* Results Display */
            <div className="space-y-6">
              {/* Header with Back Button */}
              <div className="flex justify-between items-center bg-white rounded-lg shadow-lg p-6">
                <div>
                  <h2 className="text-2xl font-bold text-gray-800">
                    Content for {results.company_name}
                  </h2>
                  <p className="text-gray-600">Topic: {results.topic}</p>
                </div>
                <button
                  onClick={() => setResults(null)}
                  className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors"
                >
                  Generate New Content
                </button>
              </div>

              {/* Platform Content */}
              <div className="grid gap-6">
                {results.generated_content.map((content, index) => (
                  <div key={index} className="bg-white rounded-lg shadow-lg overflow-hidden">
                    <div className={`${PLATFORM_COLORS[content.platform]} p-4 text-white`}>
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                          <span className="text-2xl">{PLATFORM_ICONS[content.platform]}</span>
                          <h3 className="text-lg font-semibold capitalize">{content.platform}</h3>
                        </div>
                        <button
                          onClick={() => copyToClipboard(content.content)}
                          className="bg-white bg-opacity-20 hover:bg-opacity-30 px-3 py-1 rounded text-sm transition-colors"
                        >
                          Copy
                        </button>
                      </div>
                    </div>
                    
                    <div className="p-6">
                      <div className="mb-4">
                        <h4 className="font-medium text-gray-700 mb-2">Content:</h4>
                        <p className="text-gray-800 leading-relaxed whitespace-pre-wrap">
                          {content.content}
                        </p>
                      </div>
                      
                      {content.hashtags.length > 0 && (
                        <div className="mb-4">
                          <h4 className="font-medium text-gray-700 mb-2">Hashtags:</h4>
                          <div className="flex flex-wrap gap-2">
                            {content.hashtags.map((tag, i) => (
                              <span key={i} className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm">
                                #{tag}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                      
                      <div className="grid md:grid-cols-2 gap-4 text-sm">
                        <div>
                          <h4 className="font-medium text-gray-700 mb-1">Engagement Tip:</h4>
                          <p className="text-gray-600">{content.estimated_engagement}</p>
                        </div>
                        <div>
                          <h4 className="font-medium text-gray-700 mb-1">Posting Tip:</h4>
                          <p className="text-gray-600">{content.posting_tips}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {/* Blog Post */}
              {results.blog_post && (
                <div className="bg-white rounded-lg shadow-lg p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-xl font-semibold text-gray-800">📝 Blog Post</h3>
                    <button
                      onClick={() => copyToClipboard(results.blog_post)}
                      className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors"
                    >
                      Copy Blog Post
                    </button>
                  </div>
                  <div className="prose max-w-none">
                    <pre className="whitespace-pre-wrap text-gray-800 leading-relaxed">
                      {results.blog_post}
                    </pre>
                  </div>
                </div>
              )}

              {/* Newsletter Article */}
              {results.newsletter_article && (
                <div className="bg-white rounded-lg shadow-lg p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-xl font-semibold text-gray-800">📧 Newsletter Article</h3>
                    <button
                      onClick={() => copyToClipboard(results.newsletter_article)}
                      className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 transition-colors"
                    >
                      Copy Newsletter
                    </button>
                  </div>
                  <div className="prose max-w-none">
                    <pre className="whitespace-pre-wrap text-gray-800 leading-relaxed">
                      {results.newsletter_article}
                    </pre>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;