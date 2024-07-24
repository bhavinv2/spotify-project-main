import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Container, Typography, Box } from '@mui/material';

export default function Welcome() {
  const navigate = useNavigate();

  const handleSpotifySignup = (answer) => {
    if (answer === 'no') {
      window.location.href = 'https://www.spotify.com/us/signup?forward_url=https%3A%2F%2Fopen.spotify.com%2F';
    } else {
      navigate('/vibesync-check');
    }
  };

  return (
    <Container component="main" maxWidth="xs">
      <Box
        sx={{
          marginTop: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Typography component="h1" variant="h5">
          Are you signed up for Spotify?
        </Typography>
        <Button
          variant="contained"
          onClick={() => handleSpotifySignup('yes')}
          sx={{ mt: 3, mb: 2 }}
        >
          Yes
        </Button>
        <Button
          variant="contained"
          onClick={() => handleSpotifySignup('no')}
          sx={{ mt: 3, mb: 2 }}
        >
          No
        </Button>
      </Box>
    </Container>
  );
}