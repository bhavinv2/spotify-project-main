import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Callback.css';

const Callback = ({ setIsAuthenticated }) => {
  const navigate = useNavigate();

  useEffect(() => {
    const hash = window.location.hash;
    const token = new URLSearchParams(hash.replace('#', '?')).get('access_token');

    if (token) {
      localStorage.setItem('spotifyAuthToken', token);
      setIsAuthenticated(true);
      navigate('/');
    } else {
      navigate('/signin');
    }
  }, [navigate, setIsAuthenticated]);

  return (
    <div className="callback-page">
      <h1>Authenticating...</h1>
    </div>
  );
};

export default Callback;
