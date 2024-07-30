import React from 'react';
import './SignIn.css';

const CLIENT_ID = 'e6326c4c4d7c436bb8aa5cbb18c311dc';
const REDIRECT_URI = 'http://localhost:3000/callback';

const SignIn = () => {
  const handleSignIn = () => {
    const scope = 'user-top-read'; // Define your scopes
    window.location = `https://accounts.spotify.com/authorize?client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&scope=${scope}&response_type=token&show_dialog=true`;
  };

  return (
    <div className="signin-page">
      <h1>Welcome to VibeSync</h1>
      <button onClick={handleSignIn}>Sign in with Spotify</button>
    </div>
  );
};

export default SignIn;
