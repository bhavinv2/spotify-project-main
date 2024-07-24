import React, { useState } from 'react';
import './MoodPlaylist.css';

function MoodPlaylist() {
  const [mood, setMood] = useState('');
  const [playlist, setPlaylist] = useState([]);

  const handleGeneratePlaylist = () => {
    // Placeholder for generating playlist based on mood
    setPlaylist(['Song 1', 'Song 2', 'Song 3', 'Song 4', 'Song 5', 'Song 6', 'Song 7', 'Song 8', 'Song 9', 'Song 10' ]);
  };

  const handleSavePlaylist = () => {
    // Placeholder for saving the playlist
    alert('Playlist saved!');
  };

  return (
    <div className="mood-playlist">
      <h2>Create a Playlist Based on Your Mood</h2>
      <input
        type="text"
        value={mood}
        onChange={(e) => setMood(e.target.value)}
        placeholder="Enter your mood..."
      />
      <button onClick={handleGeneratePlaylist}>Generate Playlist</button>
      <div className="playlist">
        {playlist.map((song, index) => (
          <div key={index} className="playlist-item">
            {song}
          </div>
        ))}
      </div>
      <button onClick={handleSavePlaylist}>Save Playlist</button>
    </div>
  );
}

export default MoodPlaylist;