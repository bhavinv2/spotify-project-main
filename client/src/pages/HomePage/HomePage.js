import React from 'react';
import CuratedRecommendations from './CuratedRecommendations/CuratedRecommendations';
import TopArtists from './TopArtists/TopArtists';
import TopGenres from './TopGenres/TopGenres';
import TopTracks from './TopTracks/TopTracks';
import './HomePage.css';

function HomePage() {
  return (
    <div className="homepage">
      <div className="welcome-section">
        <h1>Welcome to VibeSync</h1>
      </div>
      <div className="content-section">
        <div className="feature-box">
          <CuratedRecommendations />
        </div>
        <div className="feature-box">
          <TopArtists />
        </div>
        <div className="feature-box">
          <TopGenres />
        </div>
        <div className="feature-box">
          <TopTracks />
        </div>
      </div>
    </div>
  );
}

export default HomePage;