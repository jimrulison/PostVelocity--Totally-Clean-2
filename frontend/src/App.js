import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={
            <div className="min-h-screen bg-gray-100 flex items-center justify-center">
              <div className="max-w-md w-full bg-white rounded-lg shadow-lg p-8">
                <div className="text-center">
                  <h1 className="text-3xl font-bold text-gray-900 mb-4">PostVelocity</h1>
                  <p className="text-gray-600 mb-8">AI-Powered Social Media Management</p>
                  
                  {!isLoggedIn ? (
                    <div>
                      <h2 className="text-xl font-semibold mb-4">Welcome!</h2>
                      <p className="text-gray-600 mb-6">
                        Please use the login pages to access your dashboard:
                      </p>
                      <div className="space-y-3">
                        <a 
                          href="/api/login" 
                          className="block w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition"
                        >
                          User Login
                        </a>
                        <a 
                          href="/api/admin-login" 
                          className="block w-full bg-gray-600 text-white py-2 px-4 rounded hover:bg-gray-700 transition"
                        >
                          Admin Login
                        </a>
                      </div>
                    </div>
                  ) : (
                    <div>
                      <h2 className="text-xl font-semibold mb-4">Dashboard</h2>
                      <p className="text-gray-600">Welcome to your PostVelocity dashboard!</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          } />
          <Route path="*" element={
            <div className="min-h-screen bg-gray-100 flex items-center justify-center">
              <div className="text-center">
                <h1 className="text-4xl font-bold text-gray-800 mb-4">404</h1>
                <p className="text-gray-600 mb-4">Page not found</p>
                <a href="/" className="text-blue-600 hover:underline">Go back home</a>
              </div>
            </div>
          } />
        </Routes>
      </div>
    </Router>
  );
}

export default App;