import React, { useState, useEffect } from 'react';
import './CuratedRecommendations.css';

const CuratedRecommendations = () => {
  const [recommendations, setRecommendations] = useState([]);

  useEffect(() => {
    fetch('/api/recommendations')
      .then(response => response.json())
      .then(data => {
        console.log('Fetched recommendations:', data); // Debugging log
        if (data.error) {
          console.error('Error:', data.error);
        } else {
          setRecommendations(data);
        }
      })
      .catch(error => console.error('Error fetching recommendations:', error));
  }, []);

  return (
    <div className="curated-recommendations">
      <h2>Curated Recommendations</h2>
      <ul>
        {recommendations.length > 0 ? (
          recommendations.map((track, index) => (
            <li key={index}>{track.name} by {track.artist}</li>
          ))
        ) : (
          <li>No recommendations available</li>
        )}
      </ul>
    </div>
  );
};

export default CuratedRecommendations;
