import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import NavigationTabs from './components/NavigationTabs/NavigationTabs';
import HomePage from './pages/HomePage/HomePage';
import Chatbot from './pages/Chatbot/Chatbot';
import MoodPlaylist from './pages/MoodPlaylist/MoodPlaylist';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
      <NavigationTabs />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/chatbot" element={<Chatbot />} />
          <Route path="/mood-playlist" element={<MoodPlaylist />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;