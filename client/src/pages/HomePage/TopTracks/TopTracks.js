import React, { useState, useEffect } from 'react';
import './TopTracks.css';

const TopTracks = () => {
  const [tracks, setTracks] = useState([]);

  useEffect(() => {
    // Placeholder for API call to get top tracks
    setTracks([
      'Track 1',
      'Track 2',
      'Track 3',
      'Track 4',
      'Track 5',
      'Track 6',
      'Track 7',
      'Track 8',
      'Track 9',
      'Track 10',
    ]);
  }, []);

  return (
    <div className="top-tracks">
      <h2>Top Tracks</h2>
      <ul>
        {tracks.map((track, index) => (
          <li key={index}>{track}</li>
        ))}
      </ul>
    </div>
  );
};

export default TopTracks;