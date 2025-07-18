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

const SEO_SCORE_COLORS = {
  excellent: 'text-green-600 bg-green-100',
  good: 'text-blue-600 bg-blue-100',
  fair: 'text-yellow-600 bg-yellow-100',
  poor: 'text-red-600 bg-red-100'
};

const PERFORMANCE_COLORS = {
  high: 'text-green-600 bg-green-100',
  medium: 'text-yellow-600 bg-yellow-100',
  low: 'text-red-600 bg-red-100'
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
  const [examples, setExamples] = useState(null);
  const [availablePlatforms, setAvailablePlatforms] = useState([]);
  const [calendar, setCalendar] = useState([]);
  const [analytics, setAnalytics] = useState([]);
  const [monthlyReport, setMonthlyReport] = useState(null);
  const [mediaFiles, setMediaFiles] = useState([]);
  const [mediaRequests, setMediaRequests] = useState([]);
  const [uploadingMedia, setUploadingMedia] = useState(false);
  const [seoAnalysis, setSeoAnalysis] = useState(null);
  const [hashtagAnalysis, setHashtagAnalysis] = useState(null);
  const [performancePrediction, setPerformancePrediction] = useState(null);
  const [roiData, setRoiData] = useState(null);
  const [trendingHashtags, setTrendingHashtags] = useState(null);

  const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

  useEffect(() => {
    fetchCompanies();
    fetchExamples();
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

  const fetchCalendar = async (month, year) => {
    if (!selectedCompany) return;
    try {
      const response = await fetch(`${backendUrl}/api/calendar/${selectedCompany.id}?month=${month}&year=${year}`);
      const data = await response.json();
      setCalendar(data || []);
    } catch (error) {
      console.error('Error fetching calendar:', error);
      setCalendar([]);
    }
  };

  const fetchAnalytics = async (days = 30) => {
    if (!selectedCompany) return;
    try {
      const response = await fetch(`${backendUrl}/api/analytics/${selectedCompany.id}?days=${days}`);
      const data = await response.json();
      setAnalytics(data || []);
    } catch (error) {
      console.error('Error fetching analytics:', error);
      setAnalytics([]);
    }
  };

  const fetchMonthlyReport = async (month, year) => {
    if (!selectedCompany) return;
    try {
      const response = await fetch(`${backendUrl}/api/reports/monthly/${selectedCompany.id}?month=${month}&year=${year}`);
      const data = await response.json();
      setMonthlyReport(data);
    } catch (error) {
      console.error('Error fetching monthly report:', error);
    }
  };

  const analyzeSEO = async (content, keywords) => {
    try {
      const response = await fetch(`${backendUrl}/api/seo/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content,
          target_keywords: keywords
        }),
      });
      const data = await response.json();
      setSeoAnalysis(data);
      return data;
    } catch (error) {
      console.error('Error analyzing SEO:', error);
      return null;
    }
  };

  const analyzeHashtags = async (hashtags) => {
    try {
      const response = await fetch(`${backendUrl}/api/hashtags/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          hashtags,
          industry: selectedCompany?.industry?.toLowerCase() || 'construction'
        }),
      });
      const data = await response.json();
      setHashtagAnalysis(data);
      return data;
    } catch (error) {
      console.error('Error analyzing hashtags:', error);
      return null;
    }
  };

  const predictPerformance = async (content, platform, hashtags) => {
    try {
      const response = await fetch(`${backendUrl}/api/predict/performance`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content,
          platform,
          hashtags,
          company_id: selectedCompany?.id
        }),
      });
      const data = await response.json();
      setPerformancePrediction(data);
      return data;
    } catch (error) {
      console.error('Error predicting performance:', error);
      return null;
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

  const handleTargetKeywordsChange = (e) => {
    const keywords = e.target.value.split(',').map(k => k.trim()).filter(k => k);
    setFormData(prev => ({
      ...prev,
      target_keywords: keywords
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

  const handleDeleteMedia = async (mediaId) => {
    try {
      const response = await fetch(`${backendUrl}/api/media/${mediaId}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        throw new Error('Failed to delete media');
      }

      await fetchCompanyMedia();
      alert('Media deleted successfully!');
    } catch (error) {
      console.error('Error deleting media:', error);
      alert('Error deleting media. Please try again.');
    }
  };

  const markMediaRequestSent = async (companyId) => {
    try {
      const response = await fetch(`${backendUrl}/api/companies/${companyId}/media/request/sent`, {
        method: 'POST',
      });

      if (!response.ok) {
        throw new Error('Failed to mark media request as sent');
      }

      await fetchMonthlyMediaRequests();
      alert('Media request marked as sent!');
    } catch (error) {
      console.error('Error marking media request:', error);
      alert('Error marking media request. Please try again.');
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

      alert('Post scheduled successfully!');
    } catch (error) {
      console.error('Error scheduling post:', error);
      alert('Error scheduling post. Please try again.');
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    alert('Content copied to clipboard!');
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
    } catch (error) {
      console.error('Error creating company:', error);
      alert('Error creating company. Please try again.');
    }
  };

  const getSeoScoreColor = (score) => {
    if (score >= 80) return SEO_SCORE_COLORS.excellent;
    if (score >= 60) return SEO_SCORE_COLORS.good;
    if (score >= 40) return SEO_SCORE_COLORS.fair;
    return SEO_SCORE_COLORS.poor;
  };

  const getPerformanceColor = (score) => {
    if (score >= 70) return PERFORMANCE_COLORS.high;
    if (score >= 50) return PERFORMANCE_COLORS.medium;
    return PERFORMANCE_COLORS.low;
  };

  const SEOAnalysisPanel = ({ analysis }) => {
    if (!analysis) return null;

    return (
      <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
        <h3 className="text-xl font-semibold text-gray-800 mb-4">🔍 SEO Analysis</h3>
        <div className="grid md:grid-cols-2 gap-4">
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-gray-700">SEO Score:</span>
              <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getSeoScoreColor(analysis.seo_score)}`}>
                {analysis.seo_score}/100
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-700">Readability:</span>
              <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getSeoScoreColor(analysis.readability_score)}`}>
                {analysis.readability_score}/100
              </span>
            </div>
            <div>
              <span className="text-gray-700 block mb-2">Target Keywords:</span>
              <div className="flex flex-wrap gap-2">
                {analysis.target_keywords && analysis.target_keywords.map((keyword, i) => (
                  <span key={i} className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm">
                    {keyword}
                  </span>
                ))}
              </div>
            </div>
          </div>
          <div>
            <span className="text-gray-700 block mb-2">SEO Recommendations:</span>
            <ul className="space-y-1 text-sm">
              {analysis.recommendations && analysis.recommendations.map((rec, i) => (
                <li key={i} className="text-gray-600">• {rec}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    );
  };

  const HashtagAnalysisPanel = ({ analysis }) => {
    if (!analysis || !analysis.hashtag_analysis) return null;

    return (
      <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
        <h3 className="text-xl font-semibold text-gray-800 mb-4">🏷️ Hashtag Analysis</h3>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {analysis.hashtag_analysis.map((hashtag, i) => (
            <div key={i} className="bg-gray-50 rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="font-semibold text-gray-800">#{hashtag.hashtag}</span>
                <span className={`px-2 py-1 rounded text-xs ${
                  hashtag.trend_direction === 'trending' ? 'bg-green-100 text-green-800' :
                  hashtag.trend_direction === 'stable' ? 'bg-blue-100 text-blue-800' :
                  'bg-red-100 text-red-800'
                }`}>
                  {hashtag.trend_direction}
                </span>
              </div>
              <div className="space-y-1 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">Popularity:</span>
                  <span className="font-semibold">{hashtag.popularity_score}/100</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Engagement:</span>
                  <span className="font-semibold">{(hashtag.engagement_rate * 100).toFixed(2)}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Reach:</span>
                  <span className="font-semibold">{hashtag.estimated_reach}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Competition:</span>
                  <span className="font-semibold">{hashtag.competition_level}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  const PerformancePredictionPanel = ({ prediction }) => {
    if (!prediction) return null;

    return (
      <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
        <h3 className="text-xl font-semibold text-gray-800 mb-4">📊 Performance Prediction</h3>
        <div className="grid md:grid-cols-2 gap-4">
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-gray-700">Predicted Performance:</span>
              <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getPerformanceColor(prediction.predicted_performance)}`}>
                {prediction.predicted_performance}%
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-700">Confidence Level:</span>
              <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                prediction.confidence_level === 'High' ? 'bg-green-100 text-green-800' :
                prediction.confidence_level === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                'bg-red-100 text-red-800'
              }`}>
                {prediction.confidence_level}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-700">Platform:</span>
              <span className="font-semibold capitalize">{prediction.platform}</span>
            </div>
          </div>
          <div>
            <span className="text-gray-700 block mb-2">Recommendations:</span>
            <ul className="space-y-1 text-sm">
              {prediction.recommendations && prediction.recommendations.map((rec, i) => (
                <li key={i} className="text-gray-600">• {rec}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    );
  };

  const TrendingHashtagsPanel = ({ hashtags }) => {
    if (!hashtags || !hashtags.trending_hashtags) return null;

    return (
      <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
        <h3 className="text-xl font-semibold text-gray-800 mb-4">🔥 Trending Hashtags</h3>
        <div className="space-y-4">
          <div>
            <h4 className="font-medium text-green-600 mb-2">🚀 Trending Now</h4>
            <div className="flex flex-wrap gap-2">
              {hashtags.trending_hashtags.trending && hashtags.trending_hashtags.trending.map((tag, i) => (
                <span key={i} className="bg-green-100 text-green-800 px-2 py-1 rounded text-sm font-semibold">
                  {tag}
                </span>
              ))}
            </div>
          </div>
          <div>
            <h4 className="font-medium text-blue-600 mb-2">📈 Stable Performers</h4>
            <div className="flex flex-wrap gap-2">
              {hashtags.trending_hashtags.stable && hashtags.trending_hashtags.stable.map((tag, i) => (
                <span key={i} className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm">
                  {tag}
                </span>
              ))}
            </div>
          </div>
          <div>
            <h4 className="font-medium text-red-600 mb-2">📉 Declining</h4>
            <div className="flex flex-wrap gap-2">
              {hashtags.trending_hashtags.declining && hashtags.trending_hashtags.declining.map((tag, i) => (
                <span key={i} className="bg-red-100 text-red-800 px-2 py-1 rounded text-sm">
                  {tag}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  };

  const ROIAnalyticsPanel = ({ roi }) => {
    if (!roi) return null;

    return (
      <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
        <h3 className="text-xl font-semibold text-gray-800 mb-4">💰 ROI Analytics</h3>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-green-50 p-4 rounded-lg">
            <h4 className="text-sm font-medium text-green-600">ROI Percentage</h4>
            <p className="text-2xl font-bold text-green-900">{roi.roi_percentage}%</p>
          </div>
          <div className="bg-blue-50 p-4 rounded-lg">
            <h4 className="text-sm font-medium text-blue-600">Total Revenue</h4>
            <p className="text-2xl font-bold text-blue-900">${roi.revenue_attributed}</p>
          </div>
          <div className="bg-purple-50 p-4 rounded-lg">
            <h4 className="text-sm font-medium text-purple-600">Leads Generated</h4>
            <p className="text-2xl font-bold text-purple-900">{roi.leads_generated}</p>
          </div>
          <div className="bg-orange-50 p-4 rounded-lg">
            <h4 className="text-sm font-medium text-orange-600">Cost per Lead</h4>
            <p className="text-2xl font-bold text-orange-900">${roi.cost_per_lead}</p>
          </div>
        </div>
        
        <div className="mt-6">
          <h4 className="font-medium text-gray-700 mb-4">Platform Performance</h4>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
            {roi.platform_breakdown && Object.entries(roi.platform_breakdown).map(([platform, data]) => (
              <div key={platform} className="bg-gray-50 p-4 rounded-lg">
                <div className="flex items-center space-x-2 mb-2">
                  <span className="text-lg">{PLATFORM_ICONS[platform]}</span>
                  <span className="font-medium capitalize">{platform}</span>
                </div>
                <div className="space-y-1 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Investment:</span>
                    <span className="font-semibold">${data.investment}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Revenue:</span>
                    <span className="font-semibold">${data.revenue}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">ROI:</span>
                    <span className="font-semibold">{data.roi}%</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  const MediaUploadForm = () => {
    const [uploadForm, setUploadForm] = useState({
      files: null,
      category: 'training',
      description: '',
      tags: ''
    });

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
      <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
        <h3 className="text-xl font-semibold text-gray-800 mb-4">📤 Upload Media</h3>
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
            <p className="text-sm text-gray-500 mt-1">Supported formats: Images (JPG, PNG, GIF) and Videos (MP4, MOV, AVI)</p>
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
            {uploadingMedia ? (
              <div className="flex items-center justify-center">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                Uploading...
              </div>
            ) : (
              'Upload Media'
            )}
          </button>
        </form>
      </div>
    );
  };

  const MediaLibrary = () => {
    const [selectedCategory, setSelectedCategory] = useState('all');

    const filteredMedia = selectedCategory === 'all' 
      ? mediaFiles 
      : mediaFiles.filter(media => media.category === selectedCategory);

    return (
      <div className="space-y-6">
        <div className="bg-white rounded-lg shadow-lg p-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-xl font-semibold text-gray-800">📂 Media Library</h3>
            <div className="flex space-x-4">
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="all">All Categories ({mediaFiles.length})</option>
                {Object.entries(MEDIA_CATEGORIES).map(([key, value]) => (
                  <option key={key} value={key}>
                    {value.icon} {key.charAt(0).toUpperCase() + key.slice(1)} ({mediaFiles.filter(m => m.category === key).length})
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredMedia.map((media) => (
              <div key={media.id} className="bg-gray-50 rounded-lg p-4 border border-gray-200">
                <div className="flex items-start justify-between mb-2">
                  <div className="flex items-center space-x-2">
                    <span className="text-lg">{MEDIA_CATEGORIES[media.category]?.icon}</span>
                    <span className="text-sm font-medium text-gray-700 capitalize">{media.category}</span>
                  </div>
                  <button
                    onClick={() => handleDeleteMedia(media.id)}
                    className="text-red-600 hover:text-red-800 text-sm"
                  >
                    🗑️
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
                
                <div className="text-xs text-gray-400 mt-1">
                  Uploaded: {new Date(media.upload_date).toLocaleDateString()}
                </div>
              </div>
            ))}
          </div>

          {filteredMedia.length === 0 && (
            <div className="text-center py-8 text-gray-500">
              <p className="text-lg mb-2">📷 No media files found</p>
              <p className="text-sm">Upload some photos and videos to get started!</p>
            </div>
          )}
        </div>
      </div>
    );
  };

  const MediaRequestsPanel = () => {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
        <h3 className="text-xl font-semibold text-gray-800 mb-4">📅 Monthly Media Requests</h3>
        
        {mediaRequests.length === 0 ? (
          <p className="text-gray-600">All companies have uploaded media recently! 🎉</p>
        ) : (
          <div className="space-y-4">
            {mediaRequests.map((request) => (
              <div key={request.company_id} className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <h4 className="font-semibold text-gray-800">{request.company_name}</h4>
                    <p className="text-sm text-gray-600">Current media: {request.current_media_count} files</p>
                  </div>
                  <button
                    onClick={() => markMediaRequestSent(request.company_id)}
                    className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700 transition-colors"
                  >
                    Mark as Sent
                  </button>
                </div>
                
                <div className="mb-2">
                  <p className="text-sm font-medium text-gray-700">Suggested Categories:</p>
                  <div className="flex flex-wrap gap-1 mt-1">
                    {request.suggested_categories && request.suggested_categories.map((category) => (
                      <span key={category} className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">
                        {MEDIA_CATEGORIES[category]?.icon} {category}
                      </span>
                    ))}
                  </div>
                </div>
                
                <div className="text-sm text-gray-600 bg-white rounded p-2">
                  <strong>Recommendation:</strong> {request.recommendation}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    );
  };

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
      setCurrentView('dashboard');
    };

    return (
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-lg shadow-lg p-6">
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
                <label className="block text-sm font-medium text-gray-700 mb-2">Industry</label>
                <select
                  value={companyForm.industry}
                  onChange={(e) => setCompanyForm({...companyForm, industry: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="Construction">Construction</option>
                  <option value="Environmental Training">Environmental Training</option>
                  <option value="Manufacturing">Manufacturing</option>
                  <option value="Healthcare">Healthcare</option>
                  <option value="Education">Education</option>
                  <option value="Oil & Gas">Oil & Gas</option>
                  <option value="Mining">Mining</option>
                  <option value="Transportation">Transportation</option>
                  <option value="Utilities">Utilities</option>
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
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Target Audience</label>
              <input
                type="text"
                value={companyForm.target_audience}
                onChange={(e) => setCompanyForm({...companyForm, target_audience: e.target.value})}
                placeholder="e.g., Construction workers, safety managers"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Brand Voice</label>
              <input
                type="text"
                value={companyForm.brand_voice}
                onChange={(e) => setCompanyForm({...companyForm, brand_voice: e.target.value})}
                placeholder="e.g., Professional but accessible, safety-focused"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Primary Brand Color</label>
                <input
                  type="color"
                  value={companyForm.brand_colors.primary}
                  onChange={(e) => setCompanyForm({...companyForm, brand_colors: {...companyForm.brand_colors, primary: e.target.value}})}
                  className="w-full h-10 px-1 py-1 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Secondary Brand Color</label>
                <input
                  type="color"
                  value={companyForm.brand_colors.secondary}
                  onChange={(e) => setCompanyForm({...companyForm, brand_colors: {...companyForm.brand_colors, secondary: e.target.value}})}
                  className="w-full h-10 px-1 py-1 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">SEO Keywords (comma-separated)</label>
              <input
                type="text"
                value={companyForm.seo_keywords}
                onChange={(e) => setCompanyForm({...companyForm, seo_keywords: e.target.value})}
                placeholder="e.g., construction safety, OSHA training, workplace protection"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Competitor URLs (comma-separated)</label>
              <input
                type="text"
                value={companyForm.competitor_urls}
                onChange={(e) => setCompanyForm({...companyForm, competitor_urls: e.target.value})}
                placeholder="e.g., https://competitor1.com, https://competitor2.com"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            
            <div className="flex space-x-4">
              <button
                type="submit"
                className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
              >
                Create Company
              </button>
              <button
                type="button"
                onClick={() => setCurrentView('dashboard')}
                className="bg-gray-600 text-white px-6 py-2 rounded-lg hover:bg-gray-700 transition-colors"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  };

  const Dashboard = () => (
    <div className="space-y-6">
      {/* Monthly Media Requests */}
      <MediaRequestsPanel />

      {/* SEO Tools */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-xl font-semibold text-gray-800 mb-4">🔍 SEO & Analytics Tools</h3>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
          <button
            onClick={() => {
              const content = "Sample content for SEO analysis";
              analyzeSEO(content, ["safety", "training", "OSHA"]);
            }}
            className="bg-blue-50 border border-blue-200 rounded-lg p-4 hover:bg-blue-100 transition-colors"
          >
            <h4 className="font-semibold text-blue-800">SEO Analysis</h4>
            <p className="text-sm text-blue-600">Analyze content SEO</p>
          </button>
          <button
            onClick={() => {
              const hashtags = ["SafetyFirst", "OSHA", "WorkplaceSafety"];
              analyzeHashtags(hashtags);
            }}
            className="bg-green-50 border border-green-200 rounded-lg p-4 hover:bg-green-100 transition-colors"
          >
            <h4 className="font-semibold text-green-800">Hashtag Analysis</h4>
            <p className="text-sm text-green-600">Analyze hashtag trends</p>
          </button>
          <button
            onClick={() => {
              const content = "Safety training content";
              predictPerformance(content, "instagram", ["SafetyFirst"]);
            }}
            className="bg-purple-50 border border-purple-200 rounded-lg p-4 hover:bg-purple-100 transition-colors"
          >
            <h4 className="font-semibold text-purple-800">Performance Prediction</h4>
            <p className="text-sm text-purple-600">Predict content performance</p>
          </button>
          <button
            onClick={() => fetchTrendingHashtags()}
            className="bg-orange-50 border border-orange-200 rounded-lg p-4 hover:bg-orange-100 transition-colors"
          >
            <h4 className="font-semibold text-orange-800">Trending Hashtags</h4>
            <p className="text-sm text-orange-600">View trending hashtags</p>
          </button>
        </div>
      </div>

      {/* Analysis Results */}
      <SEOAnalysisPanel analysis={seoAnalysis} />
      <HashtagAnalysisPanel analysis={hashtagAnalysis} />
      <PerformancePredictionPanel prediction={performancePrediction} />
      <TrendingHashtagsPanel hashtags={trendingHashtags} />
      <ROIAnalyticsPanel roi={roiData} />

      {/* Company Selection */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold text-gray-800">Select Company</h2>
          <button
            onClick={() => setCurrentView('add-company')}
            className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors"
          >
            + Add Company
          </button>
        </div>
        
        <div className="grid md:grid-cols-3 gap-4">
          {companies.map(company => (
            <div
              key={company.id}
              onClick={() => {
                setSelectedCompany(company);
                setFormData(prev => ({ ...prev, company_id: company.id }));
              }}
              className={`p-4 border-2 rounded-lg cursor-pointer transition-all ${
                selectedCompany?.id === company.id
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-300 hover:border-gray-400'
              }`}
            >
              <h3 className="font-semibold text-gray-800">{company.name}</h3>
              <p className="text-gray-600 text-sm">{company.industry}</p>
              <p className="text-gray-500 text-xs mt-2">{company.target_audience}</p>
              <div className="flex items-center justify-between mt-2">
                <span className="text-xs text-gray-500">
                  📁 {company.media_library_size || 0} media files
                </span>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    setSelectedCompany(company);
                    setFormData(prev => ({ ...prev, company_id: company.id }));
                    setCurrentView('media');
                  }}
                  className="text-blue-600 hover:text-blue-800 text-xs"
                >
                  Manage Media
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Enhanced Content Generation */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-xl font-bold text-gray-800 mb-4">🚀 AI-Powered Content Generation</h2>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Topic *</label>
            <input
              type="text"
              name="topic"
              value={formData.topic}
              onChange={handleInputChange}
              placeholder="e.g., Advanced PPE Safety Training"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
            {examples && (
              <div className="mt-2">
                <p className="text-sm text-gray-500 mb-2">Example topics:</p>
                <div className="flex flex-wrap gap-2">
                  {examples.topics && examples.topics.slice(0, 6).map(topic => (
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

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Select Platforms *</label>
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

          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Audience Level</label>
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
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Content Options</label>
              <div className="space-y-2">
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    name="generate_blog"
                    checked={formData.generate_blog}
                    onChange={handleInputChange}
                    className="mr-2"
                  />
                  <span className="text-sm">Generate Blog Post</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    name="generate_newsletter"
                    checked={formData.generate_newsletter}
                    onChange={handleInputChange}
                    className="mr-2"
                  />
                  <span className="text-sm">Generate Newsletter</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    name="generate_video_script"
                    checked={formData.generate_video_script}
                    onChange={handleInputChange}
                    className="mr-2"
                  />
                  <span className="text-sm">Generate Video Scripts</span>
                </label>
              </div>
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">SEO & Analytics</label>
              <div className="space-y-2">
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    name="use_company_media"
                    checked={formData.use_company_media}
                    onChange={handleInputChange}
                    className="mr-2"
                  />
                  <span className="text-sm">Use Company Media ({mediaFiles.length} files)</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    name="seo_focus"
                    checked={formData.seo_focus}
                    onChange={handleInputChange}
                    className="mr-2"
                  />
                  <span className="text-sm">SEO Optimization</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    name="repurpose_content"
                    checked={formData.repurpose_content}
                    onChange={handleInputChange}
                    className="mr-2"
                  />
                  <span className="text-sm">Cross-Platform Repurposing</span>
                </label>
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Target Keywords (comma-separated)</label>
              <input
                type="text"
                onChange={handleTargetKeywordsChange}
                placeholder="e.g., safety training, PPE, workplace protection"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Additional Context</label>
            <textarea
              name="additional_context"
              value={formData.additional_context}
              onChange={handleInputChange}
              placeholder="Any specific requirements, recent news, or context..."
              rows="3"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <div className="flex items-center justify-center">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                Generating AI-Powered Content...
              </div>
            ) : (
              '🚀 Generate AI-Powered Content'
            )}
          </button>
        </form>
      </div>
    </div>
  );

  const MediaManagement = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-800">
          Media Management - {selectedCompany?.name}
        </h2>
        <button
          onClick={() => setCurrentView('dashboard')}
          className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors"
        >
          Back to Dashboard
        </button>
      </div>

      <MediaUploadForm />
      <MediaLibrary />
    </div>
  );

  const Results = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center bg-white rounded-lg shadow-lg p-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-800">
            🎯 AI-Generated Content for {selectedCompany?.name}
          </h2>
          <p className="text-gray-600">Topic: {results.topic}</p>
          {results.media_used && results.media_used.length > 0 && (
            <p className="text-sm text-green-600 mt-1">
              ✅ Used {results.media_used.length} company media files
            </p>
          )}
        </div>
        <div className="flex space-x-4">
          <button
            onClick={() => setCurrentView('calendar')}
            className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors"
          >
            Schedule Posts
          </button>
          <button
            onClick={() => setCurrentView('dashboard')}
            className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors"
          >
            Generate New Content
          </button>
        </div>
      </div>

      {/* SEO Recommendations */}
      {results.seo_recommendations && results.seo_recommendations.length > 0 && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-blue-800 mb-4">🔍 SEO Recommendations</h3>
          <div className="space-y-2">
            {results.seo_recommendations.map((rec, index) => (
              <div key={index} className="flex items-start space-x-2">
                <span className="text-blue-600 mt-1">•</span>
                <p className="text-sm text-blue-800">{rec}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Hashtag Strategy */}
      {results.hashtag_strategy && Object.keys(results.hashtag_strategy).length > 0 && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-green-800 mb-4">🏷️ Hashtag Strategy</h3>
          <div className="space-y-4">
            {Object.entries(results.hashtag_strategy).map(([platform, strategy]) => (
              <div key={platform} className="bg-white rounded-lg p-4">
                <h4 className="font-semibold text-gray-800 mb-2 capitalize flex items-center">
                  <span className="text-lg mr-2">{PLATFORM_ICONS[platform]}</span>
                  {platform}
                </h4>
                <p className="text-sm text-gray-600 mb-2">{strategy.recommended_mix}</p>
                <div className="flex flex-wrap gap-2">
                  {strategy.trending && strategy.trending.map((tag, i) => (
                    <span key={i} className="bg-green-100 text-green-800 px-2 py-1 rounded text-sm">
                      #{tag}
                    </span>
                  ))}
                  {strategy.stable && strategy.stable.map((tag, i) => (
                    <span key={i} className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm">
                      #{tag}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Performance Forecast */}
      {results.performance_forecast && Object.keys(results.performance_forecast).length > 0 && (
        <div className="bg-purple-50 border border-purple-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-purple-800 mb-4">📊 Performance Forecast</h3>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
            {Object.entries(results.performance_forecast).map(([platform, forecast]) => (
              <div key={platform} className="bg-white rounded-lg p-4">
                <h4 className="font-semibold text-gray-800 mb-2 capitalize flex items-center">
                  <span className="text-lg mr-2">{PLATFORM_ICONS[platform]}</span>
                  {platform}
                </h4>
                <div className="space-y-1 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Engagement:</span>
                    <span className={`font-semibold ${getPerformanceColor(forecast.engagement_rate)}`}>
                      {forecast.engagement_rate}%
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Est. Reach:</span>
                    <span className="font-semibold">{forecast.estimated_reach}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Confidence:</span>
                    <span className="font-semibold">{forecast.confidence_level}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Media Usage Summary */}
      {results.media_used && results.media_used.length > 0 && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">📁 Media Files Used</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {results.media_used.map((media, index) => (
              <div key={index} className="bg-gray-50 rounded-lg p-3 border border-gray-200">
                <div className="flex items-center space-x-2 mb-2">
                  <span className="text-sm">{MEDIA_CATEGORIES[media.category]?.icon}</span>
                  <span className="text-sm font-medium text-gray-700 capitalize">{media.category}</span>
                </div>
                <p className="text-sm text-gray-800 truncate">{media.filename}</p>
                <p className="text-xs text-gray-600">{media.description}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Media Suggestions */}
      {results.media_suggestions && results.media_suggestions.length > 0 && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-yellow-800 mb-4">💡 Media Suggestions</h3>
          <div className="space-y-2">
            {results.media_suggestions.map((suggestion, index) => (
              <div key={index} className="flex items-start space-x-2">
                <span className="text-yellow-600 mt-1">•</span>
                <p className="text-sm text-yellow-800">{suggestion}</p>
              </div>
            ))}
          </div>
          <button
            onClick={() => setCurrentView('media')}
            className="mt-4 bg-yellow-600 text-white px-4 py-2 rounded-lg hover:bg-yellow-700 transition-colors"
          >
            Upload Media Now
          </button>
        </div>
      )}

      {/* Platform Content */}
      <div className="grid gap-6">
        {results.generated_content && results.generated_content.map((content, index) => (
          <div key={index} className="bg-white rounded-lg shadow-lg overflow-hidden">
            <div className={`${PLATFORM_COLORS[content.platform]} p-4 text-white`}>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <span className="text-2xl">{PLATFORM_ICONS[content.platform]}</span>
                  <h3 className="text-lg font-semibold capitalize">{content.platform}</h3>
                  {content.performance_prediction && (
                    <span className="bg-white bg-opacity-20 px-2 py-1 rounded text-sm">
                      {content.performance_prediction}% predicted
                    </span>
                  )}
                </div>
                <div className="flex space-x-2">
                  <button
                    onClick={() => copyToClipboard(content.content)}
                    className="bg-white bg-opacity-20 hover:bg-opacity-30 px-3 py-1 rounded text-sm transition-colors"
                  >
                    Copy
                  </button>
                  <button
                    onClick={() => {
                      const scheduledTime = new Date();
                      scheduledTime.setHours(scheduledTime.getHours() + 1);
                      schedulePost(content.platform, content.content, content.hashtags, scheduledTime);
                    }}
                    className="bg-white bg-opacity-20 hover:bg-opacity-30 px-3 py-1 rounded text-sm transition-colors"
                  >
                    Schedule
                  </button>
                </div>
              </div>
            </div>
            
            <div className="p-6">
              <div className="mb-4">
                <h4 className="font-medium text-gray-700 mb-2">Content:</h4>
                <p className="text-gray-800 leading-relaxed whitespace-pre-wrap">
                  {content.content}
                </p>
              </div>
              
              {content.hashtags && content.hashtags.length > 0 && (
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

              {/* SEO Analysis for this content */}
              {content.seo_analysis && (
                <div className="mb-4">
                  <h4 className="font-medium text-gray-700 mb-2">SEO Analysis:</h4>
                  <div className="bg-gray-50 rounded-lg p-3">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm text-gray-600">SEO Score:</span>
                      <span className={`px-2 py-1 rounded text-xs ${getSeoScoreColor(content.seo_analysis.seo_score)}`}>
                        {content.seo_analysis.seo_score}/100
                      </span>
                    </div>
                    <div className="text-xs text-gray-600">
                      <p className="mb-1">Keywords: {Object.keys(content.seo_analysis.keyword_density || {}).join(', ')}</p>
                      <p>Recommendations: {content.seo_analysis.recommendations && content.seo_analysis.recommendations.length} items</p>
                    </div>
                  </div>
                </div>
              )}

              {/* Hashtag Analysis */}
              {content.hashtag_analysis && content.hashtag_analysis.length > 0 && (
                <div className="mb-4">
                  <h4 className="font-medium text-gray-700 mb-2">Hashtag Performance:</h4>
                  <div className="bg-gray-50 rounded-lg p-3">
                    <div className="grid grid-cols-2 gap-2 text-xs">
                      <div>Avg. Popularity: {(content.hashtag_analysis.reduce((sum, h) => sum + h.popularity_score, 0) / content.hashtag_analysis.length).toFixed(1)}</div>
                      <div>Avg. Engagement: {(content.hashtag_analysis.reduce((sum, h) => sum + h.engagement_rate, 0) / content.hashtag_analysis.length * 100).toFixed(2)}%</div>
                    </div>
                  </div>
                </div>
              )}
              
              {content.suggested_media && content.suggested_media.length > 0 && (
                <div className="mb-4">
                  <h4 className="font-medium text-gray-700 mb-2">Suggested Media:</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                    {content.suggested_media.map((media, i) => (
                      <div key={i} className="bg-green-50 border border-green-200 rounded p-2">
                        <div className="flex items-center space-x-2">
                          <span className="text-sm">{MEDIA_CATEGORIES[media.category]?.icon}</span>
                          <span className="text-sm font-medium text-green-800">{media.filename}</span>
                        </div>
                        <p className="text-xs text-green-600">{media.description}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              
              {content.media_placement && (
                <div className="mb-4">
                  <h4 className="font-medium text-gray-700 mb-2">Media Placement Guide:</h4>
                  <p className="text-sm text-gray-600 bg-gray-50 p-2 rounded">{content.media_placement}</p>
                </div>
              )}
              
              {content.video_suggestions && content.video_suggestions !== 'Not applicable' && (
                <div className="mb-4">
                  <h4 className="font-medium text-gray-700 mb-2">Video Suggestion:</h4>
                  <p className="text-gray-600">{content.video_suggestions}</p>
                </div>
              )}
              
              {/* Repurposed Versions */}
              {content.repurposed_versions && Object.keys(content.repurposed_versions).length > 0 && (
                <div className="mb-4">
                  <h4 className="font-medium text-gray-700 mb-2">Cross-Platform Versions:</h4>
                  <div className="space-y-2">
                    {Object.entries(content.repurposed_versions).map(([platform, repurposedContent]) => (
                      <div key={platform} className="bg-gray-50 rounded p-2">
                        <div className="flex items-center space-x-2 mb-1">
                          <span className="text-sm">{PLATFORM_ICONS[platform]}</span>
                          <span className="text-sm font-medium capitalize">{platform}</span>
                        </div>
                        <p className="text-xs text-gray-600 truncate">{repurposedContent}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              
              <div className="grid md:grid-cols-3 gap-4 text-sm">
                <div>
                  <h4 className="font-medium text-gray-700 mb-1">Engagement Tip:</h4>
                  <p className="text-gray-600">{content.estimated_engagement}</p>
                </div>
                <div>
                  <h4 className="font-medium text-gray-700 mb-1">Posting Tip:</h4>
                  <p className="text-gray-600">{content.posting_tips}</p>
                </div>
                <div>
                  <h4 className="font-medium text-gray-700 mb-1">Optimal Times:</h4>
                  <p className="text-gray-600">{content.optimal_posting_times && content.optimal_posting_times.join(', ')}</p>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Enhanced Blog Post */}
      {results.blog_post && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-semibold text-gray-800">📝 SEO-Optimized Blog Post</h3>
            <button
              onClick={() => copyToClipboard(results.blog_post.content)}
              className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors"
            >
              Copy Blog Post
            </button>
          </div>
          
          {/* SEO Analysis for Blog */}
          {results.blog_post.seo_analysis && (
            <div className="mb-4">
              <h4 className="font-medium text-gray-700 mb-2">SEO Analysis:</h4>
              <div className="bg-blue-50 rounded-lg p-4">
                <div className="grid md:grid-cols-3 gap-4 text-sm">
                  <div>
                    <span className="text-gray-600">SEO Score:</span>
                    <span className={`ml-2 px-2 py-1 rounded text-xs ${getSeoScoreColor(results.blog_post.seo_analysis.seo_score)}`}>
                      {results.blog_post.seo_analysis.seo_score}/100
                    </span>
                  </div>
                  <div>
                    <span className="text-gray-600">Readability:</span>
                    <span className={`ml-2 px-2 py-1 rounded text-xs ${getSeoScoreColor(results.blog_post.seo_analysis.readability_score)}`}>
                      {results.blog_post.seo_analysis.readability_score}/100
                    </span>
                  </div>
                  <div>
                    <span className="text-gray-600">Read Time:</span>
                    <span className="ml-2 font-semibold">{results.blog_post.estimated_read_time}</span>
                  </div>
                </div>
              </div>
            </div>
          )}
          
          <div className="space-y-4">
            <div>
              <h4 className="font-bold text-lg text-gray-800">{results.blog_post.title}</h4>
              <p className="text-gray-600 italic">{results.blog_post.excerpt}</p>
              {results.blog_post.meta_description && (
                <p className="text-sm text-gray-500 mt-1">Meta: {results.blog_post.meta_description}</p>
              )}
            </div>
            
            {results.blog_post.suggested_media && results.blog_post.suggested_media.length > 0 && (
              <div>
                <h4 className="font-medium text-gray-700 mb-2">Suggested Media for Blog:</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                  {results.blog_post.suggested_media.map((media, i) => (
                    <div key={i} className="bg-green-50 border border-green-200 rounded p-2">
                      <div className="flex items-center space-x-2">
                        <span className="text-sm">{MEDIA_CATEGORIES[media.category]?.icon}</span>
                        <span className="text-sm font-medium text-green-800">{media.filename}</span>
                      </div>
                      <p className="text-xs text-green-600">{media.description}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
            
            {results.blog_post.media_placement_guide && (
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <h4 className="font-medium text-blue-800 mb-2">Media Placement Guide:</h4>
                <p className="text-sm text-blue-700">{results.blog_post.media_placement_guide}</p>
              </div>
            )}
            
            <div className="prose max-w-none">
              <pre className="whitespace-pre-wrap text-gray-800 leading-relaxed">
                {results.blog_post.content}
              </pre>
            </div>
            
            <div>
              <h4 className="font-medium text-gray-700 mb-2">SEO Keywords:</h4>
              <div className="flex flex-wrap gap-2">
                {results.blog_post.seo_keywords && results.blog_post.seo_keywords.map((keyword, i) => (
                  <span key={i} className="bg-green-100 text-green-800 px-2 py-1 rounded text-sm">
                    {keyword}
                  </span>
                ))}
              </div>
            </div>

            {/* Schema Markup */}
            {results.blog_post.schema_markup && (
              <div>
                <h4 className="font-medium text-gray-700 mb-2">Schema Markup:</h4>
                <div className="bg-gray-50 rounded-lg p-3">
                  <pre className="text-xs text-gray-600 whitespace-pre-wrap">
                    {JSON.stringify(results.blog_post.schema_markup, null, 2)}
                  </pre>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Continue with newsletter, video scripts, etc. */}
      {/* ... rest of the existing Results component code ... */}
    </div>
  );

  const Calendar = () => {
    const [currentDate, setCurrentDate] = useState(new Date());
    
    useEffect(() => {
      if (selectedCompany) {
        fetchCalendar(currentDate.getMonth() + 1, currentDate.getFullYear());
      }
    }, [selectedCompany, currentDate]);

    return (
      <div className="space-y-6">
        <div className="bg-white rounded-lg shadow-lg p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-800">📅 Smart Content Calendar</h2>
            <div className="flex space-x-4">
              <button
                onClick={() => setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() - 1))}
                className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors"
              >
                Previous
              </button>
              <span className="px-4 py-2 bg-gray-100 rounded-lg">
                {currentDate.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })}
              </span>
              <button
                onClick={() => setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() + 1))}
                className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors"
              >
                Next
              </button>
            </div>
          </div>
          
          <div className="grid gap-4">
            {calendar.map((entry, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4">
                <h3 className="font-semibold text-gray-800 mb-2">
                  {new Date(entry.date).toLocaleDateString('en-US', { 
                    weekday: 'long', 
                    year: 'numeric', 
                    month: 'long', 
                    day: 'numeric' 
                  })}
                </h3>
                <p className="text-sm text-gray-600 mb-3">{entry.total_posts} posts scheduled</p>
                <div className="space-y-2">
                  {entry.posts && entry.posts.map((post, postIndex) => (
                    <div key={postIndex} className="flex items-center justify-between bg-gray-50 p-3 rounded">
                      <div className="flex items-center space-x-3">
                        <span className="text-lg">{PLATFORM_ICONS[post.platform]}</span>
                        <div>
                          <p className="font-medium text-gray-800">{post.platform}</p>
                          <p className="text-sm text-gray-600">{post.topic}</p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className={`px-2 py-1 rounded text-xs ${
                          post.status === 'published' ? 'bg-green-100 text-green-800' :
                          post.status === 'scheduled' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-gray-100 text-gray-800'
                        }`}>
                          {post.status}
                        </span>
                        <span className="text-sm text-gray-500">
                          {new Date(post.scheduled_time).toLocaleTimeString('en-US', { 
                            hour: '2-digit', 
                            minute: '2-digit' 
                          })}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  const Analytics = () => {
    useEffect(() => {
      if (selectedCompany) {
        fetchAnalytics();
        fetchMonthlyReport(new Date().getMonth() + 1, new Date().getFullYear());
      }
    }, [selectedCompany]);

    return (
      <div className="space-y-6">
        {/* ROI Analytics */}
        <ROIAnalyticsPanel roi={roiData} />
        
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">📊 Advanced Analytics Dashboard</h2>
          
          {/* Quick Stats */}
          <div className="grid md:grid-cols-4 gap-4 mb-6">
            <div className="bg-blue-50 p-4 rounded-lg">
              <h3 className="text-sm font-medium text-blue-600">Total Posts</h3>
              <p className="text-2xl font-bold text-blue-900">{analytics.length}</p>
            </div>
            <div className="bg-green-50 p-4 rounded-lg">
              <h3 className="text-sm font-medium text-green-600">Total Engagement</h3>
              <p className="text-2xl font-bold text-green-900">
                {analytics.reduce((sum, record) => sum + (record.likes || 0) + (record.shares || 0) + (record.comments || 0), 0)}
              </p>
            </div>
            <div className="bg-purple-50 p-4 rounded-lg">
              <h3 className="text-sm font-medium text-purple-600">Avg. Engagement Rate</h3>
              <p className="text-2xl font-bold text-purple-900">
                {analytics.length > 0 ? 
                  (analytics.reduce((sum, record) => sum + (record.engagement_rate || 0), 0) / analytics.length * 100).toFixed(1) : 0
                }%
              </p>
            </div>
            <div className="bg-orange-50 p-4 rounded-lg">
              <h3 className="text-sm font-medium text-orange-600">Media Library</h3>
              <p className="text-2xl font-bold text-orange-900">{mediaFiles.length}</p>
            </div>
          </div>
          
          {/* Recent Posts Performance */}
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Recent Posts Performance</h3>
            <div className="space-y-3">
              {analytics.slice(0, 5).map((record, index) => (
                <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                  <div className="flex items-center space-x-3">
                    <span className="text-lg">{PLATFORM_ICONS[record.platform]}</span>
                    <div>
                      <p className="font-medium text-gray-800">{record.platform}</p>
                      <p className="text-sm text-gray-600">
                        {new Date(record.recorded_at).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                  <div className="flex space-x-4 text-sm">
                    <span className="text-gray-600">👍 {record.likes || 0}</span>
                    <span className="text-gray-600">💬 {record.comments || 0}</span>
                    <span className="text-gray-600">📤 {record.shares || 0}</span>
                    <span className="text-gray-600">📊 {((record.engagement_rate || 0) * 100).toFixed(1)}%</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
          
          {/* Enhanced Monthly Report */}
          {monthlyReport && (
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-4">📈 Monthly Report</h3>
              <div className="bg-gray-50 rounded-lg p-4">
                <div className="mb-4">
                  <h4 className="font-medium text-gray-700 mb-2">Content Recommendations:</h4>
                  <ul className="space-y-1">
                    {monthlyReport.recommendations && monthlyReport.recommendations.map((rec, index) => (
                      <li key={index} className="text-sm text-gray-600">• {rec}</li>
                    ))}
                  </ul>
                </div>
                
                {monthlyReport.media_recommendations && monthlyReport.media_recommendations.length > 0 && (
                  <div className="mb-4">
                    <h4 className="font-medium text-gray-700 mb-2">Media Recommendations:</h4>
                    <ul className="space-y-1">
                      {monthlyReport.media_recommendations.map((rec, index) => (
                        <li key={index} className="text-sm text-gray-600">📷 {rec}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Enhanced Analytics */}
                {monthlyReport.seo_insights && (
                  <div className="mb-4">
                    <h4 className="font-medium text-gray-700 mb-2">SEO Insights:</h4>
                    <div className="bg-white p-3 rounded">
                      <div className="grid md:grid-cols-2 gap-4 text-sm">
                        <div>Average SEO Score: {monthlyReport.seo_insights.avg_seo_score}</div>
                        <div>Content Optimization: {monthlyReport.seo_insights.content_optimization}</div>
                      </div>
                    </div>
                  </div>
                )}

                {monthlyReport.hashtag_performance && (
                  <div className="mb-4">
                    <h4 className="font-medium text-gray-700 mb-2">Hashtag Performance:</h4>
                    <div className="bg-white p-3 rounded">
                      <div className="grid md:grid-cols-2 gap-4 text-sm">
                        <div>Trending Usage: {monthlyReport.hashtag_performance.trending_usage}</div>
                        <div>Avg. Engagement: {monthlyReport.hashtag_performance.avg_hashtag_engagement}</div>
                      </div>
                    </div>
                  </div>
                )}
                
                <div className="mb-4">
                  <h4 className="font-medium text-gray-700 mb-2">Platform Performance:</h4>
                  <div className="grid md:grid-cols-2 gap-3">
                    {monthlyReport.platform_performance && Object.entries(monthlyReport.platform_performance).map(([platform, data]) => (
                      <div key={platform} className="bg-white p-3 rounded">
                        <div className="flex items-center space-x-2 mb-1">
                          <span>{PLATFORM_ICONS[platform]}</span>
                          <span className="font-medium capitalize">{platform}</span>
                        </div>
                        <p className="text-sm text-gray-600">
                          {data.total_posts} posts, {data.total_engagement} engagement
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
                
                {monthlyReport.media_performance && Object.keys(monthlyReport.media_performance).length > 0 && (
                  <div className="mb-4">
                    <h4 className="font-medium text-gray-700 mb-2">Media Performance:</h4>
                    <div className="grid md:grid-cols-2 gap-3">
                      {Object.entries(monthlyReport.media_performance).map(([category, usage]) => (
                        <div key={category} className="bg-white p-3 rounded">
                          <div className="flex items-center space-x-2 mb-1">
                            <span>{MEDIA_CATEGORIES[category]?.icon}</span>
                            <span className="font-medium capitalize">{category}</span>
                          </div>
                          <p className="text-sm text-gray-600">Used {usage} times</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
                
                {monthlyReport.viral_potential_posts && monthlyReport.viral_potential_posts.length > 0 && (
                  <div>
                    <h4 className="font-medium text-gray-700 mb-2">Viral Potential Posts:</h4>
                    <p className="text-sm text-gray-600">
                      {monthlyReport.viral_potential_posts.length} posts showing high engagement potential
                    </p>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    );
  };

  const Navigation = () => (
    <nav className="bg-white shadow-lg mb-6">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-8">
            <h1 className="text-xl font-bold text-gray-800">
              🚀 AI Social Media Manager
            </h1>
            <div className="flex space-x-4">
              <button
                onClick={() => setCurrentView('dashboard')}
                className={`px-4 py-2 rounded-lg transition-colors ${
                  currentView === 'dashboard' ? 'bg-blue-600 text-white' : 'text-gray-600 hover:text-gray-800'
                }`}
              >
                Dashboard
              </button>
              <button
                onClick={() => setCurrentView('media')}
                className={`px-4 py-2 rounded-lg transition-colors ${
                  currentView === 'media' ? 'bg-blue-600 text-white' : 'text-gray-600 hover:text-gray-800'
                }`}
              >
                Media
              </button>
              <button
                onClick={() => setCurrentView('calendar')}
                className={`px-4 py-2 rounded-lg transition-colors ${
                  currentView === 'calendar' ? 'bg-blue-600 text-white' : 'text-gray-600 hover:text-gray-800'
                }`}
              >
                Calendar
              </button>
              <button
                onClick={() => setCurrentView('analytics')}
                className={`px-4 py-2 rounded-lg transition-colors ${
                  currentView === 'analytics' ? 'bg-blue-600 text-white' : 'text-gray-600 hover:text-gray-800'
                }`}
              >
                Analytics
              </button>
            </div>
          </div>
          
          {selectedCompany && (
            <div className="text-right">
              <p className="text-sm text-gray-600">Selected Company:</p>
              <p className="font-medium text-gray-800">{selectedCompany.name}</p>
              <p className="text-xs text-gray-500">📁 {mediaFiles.length} media files</p>
            </div>
          )}
        </div>
      </div>
    </nav>
  );

  const renderCurrentView = () => {
    switch (currentView) {
      case 'dashboard':
        return <Dashboard />;
      case 'add-company':
        return <CompanyForm />;
      case 'results':
        return <Results />;
      case 'media':
        return <MediaManagement />;
      case 'calendar':
        return <Calendar />;
      case 'analytics':
        return <Analytics />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <Navigation />
      <div className="container mx-auto px-4 py-8">
        {renderCurrentView()}
      </div>
    </div>
  );
}

export default App;