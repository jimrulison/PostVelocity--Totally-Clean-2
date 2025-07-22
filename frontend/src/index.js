import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
import AuthRouter from "./AuthRouter";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <AuthRouter>
      <App />
    </AuthRouter>
  </React.StrictMode>,
);
