import React, { useState, useEffect } from 'react';
import './TopTracks.css';

const TopTracks = () => {
  const [tracks, setTracks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTopTracks = async () => {
      const token = localStorage.getItem('spotifyAuthToken');
      if (token) {
        try {
          const response = await fetch('http://localhost:5000/api/top_tracks', {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json',
            },
          });

          if (response.ok) {
            const data = await response.json();
            setTracks(data);
          } else {
            const errorText = await response.text();
            console.error('Failed to fetch top tracks:', response.statusText, errorText);
            setError(`Failed to fetch top tracks: ${response.statusText}. ${errorText}`);
          }
        } catch (error) {
          console.error('Error fetching top tracks:', error);
          setError(`Error fetching top tracks: ${error.message}`);
        }
      } else {
        setError('No token found.');
      }
      setLoading(false);
    };

    fetchTopTracks();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div className="top-tracks">
      <h2>Top Tracks</h2>
      <ul>
        {tracks.map((track, index) => (
          <li key={index}>{track.name} by {track.artist}</li>
        ))}
      </ul>
    </div>
  );
};

export default TopTracks;
