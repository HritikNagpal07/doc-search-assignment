import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css'; // This imports our styling
import App from './App'; // This imports the main App component above

// This finds the <div id="root"> in our HTML file and puts our React app inside it
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
