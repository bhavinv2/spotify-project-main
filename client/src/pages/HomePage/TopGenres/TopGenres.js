import React, { useState, useEffect } from 'react';
import './TopGenres.css';

const TopGenres = () => {
  const [genres, setGenres] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchTopGenres = async () => {
      const token = localStorage.getItem('spotifyAuthToken'); // Ensure token key matches
      console.log('Token from local storage:', token); // Debugging log

      if (token) {
        try {
          const response = await fetch('http://localhost:5000/api/top_genres', {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json',
            },
          });

          if (response.ok) {
            const data = await response.json();
            setGenres(data);
          } else {
            const errorText = await response.text();
            console.error('Failed to fetch top genres:', response.statusText, errorText);
            setError(`Failed to fetch top genres: ${response.statusText}. ${errorText}`);
          }
        } catch (error) {
          console.error('Error fetching top genres:', error);
          setError(`Error fetching top genres: ${error.message}`);
        }
      } else {
        setError('No token found.');
      }
      setLoading(false);
    };

    fetchTopGenres();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div className="top-genres">
      <h2>Top Genres</h2>
      <ul>
        {genres.length > 0 ? (
          genres.map((genre, index) => (
            <li key={index}>
              {genre.genre} ({genre.count})
            </li>
          ))
        ) : (
          <li>No genres available</li>
        )}
      </ul>
    </div>
  );
};

export default TopGenres;
