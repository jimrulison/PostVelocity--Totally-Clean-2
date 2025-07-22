import React, { useState, useEffect } from 'react';

// Simple URL-based authentication router
function AuthRouter({ children }) {
  const [authView, setAuthView] = useState('login');

  useEffect(() => {
    // Check URL path to determine auth view
    const path = window.location.pathname;
    if (path === '/admin-login') {
      setAuthView('admin-login');
    } else if (path === '/login') {
      setAuthView('login');
    } else {
      setAuthView('auto');
    }

    // Listen for URL changes
    const handlePopState = () => {
      const path = window.location.pathname;
      if (path === '/admin-login') {
        setAuthView('admin-login');
      } else if (path === '/login') {
        setAuthView('login');
      } else {
        setAuthView('auto');
      }
    };

    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, []);

  // Helper function to navigate between login types
  const navigateToAuth = (type) => {
    const url = type === 'admin-login' ? '/admin-login' : '/login';
    window.history.pushState(null, '', url);
    setAuthView(type);
  };

  return React.cloneElement(children, { authView, navigateToAuth });
}

export default AuthRouter;