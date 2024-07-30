import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import NavigationTabs from './components/NavigationTabs/NavigationTabs';
import HomePage from './pages/HomePage/HomePage';
import Chatbot from './pages/Chatbot/Chatbot';
import MoodPlaylist from './pages/MoodPlaylist/MoodPlaylist';
import SignIn from './pages/SignIn/SignIn';
import Callback from './pages/Callback/Callback';
import './App.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [accessToken, setAccessToken] = useState('');

  useEffect(() => {
    const token = localStorage.getItem('spotifyAuthToken');
    if (token) {
      setIsAuthenticated(true);
      setAccessToken(token);
    }
  }, []);

  return (
    <Router>
      <div className="App">
        {isAuthenticated && <NavigationTabs />}
        <Routes>
          <Route path="/" element={isAuthenticated ? <HomePage /> : <SignIn />} />
          <Route path="/chatbot" element={<Chatbot accessToken={accessToken} />} />
          <Route path="/mood-playlist" element={<MoodPlaylist />} />
          <Route path="/signin" element={<SignIn />} />
          <Route
            path="/callback"
            element={<Callback setIsAuthenticated={setIsAuthenticated} setAccessToken={setAccessToken} />}
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;