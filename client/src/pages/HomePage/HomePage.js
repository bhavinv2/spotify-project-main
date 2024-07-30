import React, { useEffect, useState } from 'react';
import CuratedRecommendations from './CuratedRecommendations/CuratedRecommendations';
import TopArtists from './TopArtists/TopArtists';
import TopGenres from './TopGenres/TopGenres';
import TopTracks from './TopTracks/TopTracks';
import './HomePage.css';

function HomePage() {
  const [topArtists, setTopArtists] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTopArtists = async () => {
      const token = localStorage.getItem('spotifyAuthToken');
      if (token) {
        try {
          const response = await fetch('https://api.spotify.com/v1/me/top/artists', {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json',
            },
          });

          if (response.ok) {
            const data = await response.json();
            setTopArtists(data.items);
          } else {
            const errorText = await response.text();
            console.error('Failed to fetch top artists:', response.statusText, errorText);
            setError(`Failed to fetch top artists: ${response.statusText}. ${errorText}`);
          }
        } catch (error) {
          console.error('Error fetching top artists:', error);
          setError(`Error fetching top artists: ${error.message}`);
        }
      } else {
        setError('No token found.');
      }
      setLoading(false);
    };

    fetchTopArtists();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

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
          <TopArtists artists={topArtists} />
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
