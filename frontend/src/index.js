import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import "./index.css";
import App from "./App";

// Simple routing wrapper
function AppWithRouter() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<App loginType="user" />} />
        <Route path="/admin-login" element={<App loginType="admin" />} />
        <Route path="*" element={<App loginType="auto" />} />
      </Routes>
    </Router>
  );
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <AppWithRouter />
  </React.StrictMode>,
);
