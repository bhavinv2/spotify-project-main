import React from 'react';
import './TopArtists.css';

const TopArtists = ({ artists }) => {
  return (
    <div className="top-artists">
      <h2>Top Artists</h2>
      <ul>
        {artists.map((artist, index) => (
          <li key={index}>{artist.name}</li>
        ))}
      </ul>
    </div>
  );
};

export default TopArtists;
