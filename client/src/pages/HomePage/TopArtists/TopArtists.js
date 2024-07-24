import React, { useState, useEffect } from 'react';
import './TopArtists.css';

const TopArtists = () => {
  const [artists, setArtists] = useState([]);

  useEffect(() => {
    // Placeholder for API call to get top artists
    setArtists([
      'Artist 1',
      'Artist 2',
      'Artist 3',
      'Artist 4',
      'Artist 5',
      'Artist 6',
      'Artist 7',
      'Artist 8',
      'Artist 9',
      'Artist 10',
    ]);
  }, []);

  return (
    <div className="top-artists">
      <h2>Top Artists</h2>
      <ul>
        {artists.map((artist, index) => (
          <li key={index}>{artist}</li>
        ))}
      </ul>
    </div>
  );
};

export default TopArtists;