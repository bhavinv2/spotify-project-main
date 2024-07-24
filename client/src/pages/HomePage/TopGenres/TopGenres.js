import React, { useState, useEffect } from 'react';
import './TopGenres.css';

const TopGenres = () => {
  const [genres, setGenres] = useState([]);

  useEffect(() => {
    // Placeholder for API call to get top genres
    setGenres([
      'Genre 1',
      'Genre 2',
      'Genre 3',
      'Genre 4',
      'Genre 5',
    ]);
  }, []);

  return (
    <div className="top-genres">
      <h2>Top Genres</h2>
      <ul>
        {genres.map((genre, index) => (
          <li key={index}>{genre}</li>
        ))}
      </ul>
    </div>
  );
};

export default TopGenres;