##authmain:
from flask import Flask, request, url_for, session, redirect, jsonify
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
from flask_cors import CORS
from requests import get
import os
from dotenv import load_dotenv
from collections import Counter
import requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SESSION_COOKIE_NAME'] = 'SpotifySession'
app.secret_key = 'your_secret_key_here'  # Replace with a strong, random secret key
TOKEN_INFO = 'token_info'

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=url_for('redirect_page', _external=True),
        scope='user-library-read playlist-modify-public playlist-modify-private user-top-read user-follow-read playlist-read-private'
    )


@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route('/redirect')
def redirect_page():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('home', _external=True))


@app.route('/home')
def home():
    try:
        token_info = get_token()
    except:
        print("User not logged in")
        return redirect('/')

    return "✅✅✅✅OAuth successful. You can now use the API endpoints."


def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        return None

    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if is_expired:
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        session[TOKEN_INFO] = token_info

    return token_info


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def get_user_top_artists(token):
    url = "https://api.spotify.com/v1/me/top/artists"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    if result.status_code == 200:
        return result.json().get("items", [])
    else:
        print(f"Failed to get top artists: {result.status_code}")
        return []


@app.route('/api/top_artists', methods=['GET'])
def api_top_artists():
    try:
        token = request.headers.get('Authorization').split('Bearer ')[-1]
        if not token:
            return jsonify({'error': 'User not authenticated'}), 401

        top_artists = get_user_top_artists(token)
        if top_artists:
            artists_data = [{'name': artist['name']} for artist in top_artists]
            return jsonify(artists_data)
        else:
            return jsonify({'error': 'No top artists found'}), 404
    except Exception as e:
        print(f"Exception in api_top_artists: {str(e)}")
        return jsonify({'error': 'Failed to fetch top artists', 'details': str(e)}), 500


def get_user_top_tracks(token):
    url = "https://api.spotify.com/v1/me/top/tracks"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    if result.status_code == 200:
        return result.json().get("items", [])
    else:
        print(f"Failed to get top tracks: {result.status_code}")
        return None


@app.route('/api/top_tracks', methods=['GET'])
def api_top_tracks():
    try:
        token = request.headers.get('Authorization').split('Bearer ')[-1]
        if not token:
            return jsonify({'error': 'User not authenticated'}), 401

        user_top_tracks = get_user_top_tracks(token)
        if user_top_tracks:
            tracks_data = [{'name': track['name'], 'artist': track['artists'][0]['name']} for track in user_top_tracks]
            return jsonify(tracks_data)
        else:
            return jsonify({'error': 'No top tracks found'}), 404
    except Exception as e:
        print(f"Error fetching top tracks: {e}")
        return jsonify({'error': 'Failed to fetch top tracks', 'details': str(e)}), 500





def get_recommendations(token, seed_artists=None, seed_genres=None, seed_tracks=None):
    url = "https://api.spotify.com/v1/recommendations"
    headers = get_auth_header(token)

    params = {
        "limit": 10,
        "seed_artists": ','.join(seed_artists) if seed_artists else None,
        "seed_genres": ','.join(seed_genres) if seed_genres else None,
        "seed_tracks": ','.join(seed_tracks) if seed_tracks else None,
    }

    result = get(url, headers=headers, params=params)
    if result.status_code == 200:
        json_result = result.json().get("tracks", [])
        return json_result
    else:
        print(f"Failed to get recommendations: {result.status_code}")
        print(result.content)
        return None

@app.route('/api/recommendations', methods=['GET'])
def api_recommendations():
    try:
        token_info = get_token()
        token = token_info['access_token']

        # Get top tracks and artists for seeding recommendations
        top_tracks = get_user_top_tracks(token)
        top_artists = get_user_top_artists(token)

        # Prepare seed data
        seed_tracks = [track['id'] for track in top_tracks[:5]] if top_tracks else []
        seed_artists = [artist['id'] for artist in top_artists[:5]] if top_artists else []

        recommendations = get_recommendations(token, seed_artists=seed_artists, seed_tracks=seed_tracks)
        if recommendations:
            recommendations_data = [{'name': track['name'], 'artist': track['artists'][0]['name']} for track in recommendations]
            return jsonify(recommendations_data)
        else:
            return jsonify({'error': 'No recommendations found'}), 404
    except Exception as e:
        print(f"Error fetching recommendations: {e}")
        return jsonify({'error': 'Failed to fetch recommendations', 'details': str(e)}), 500

def view_top_genres(token):
    top_artists = get_user_top_artists(token)
    if top_artists:
        genre_counter = Counter()
        for artist in top_artists:
            genres = artist.get('genres', [])
            genre_counter.update(genres)

        top_genres = genre_counter.most_common()
        return top_genres
    else:
        return []

@app.route('/api/top_genres', methods=['GET'])
def api_top_genres():
    try:
        token = request.headers.get('Authorization').split('Bearer ')[-1]
        if not token:
            return jsonify({'error': 'User not authenticated'}), 401

        top_genres = view_top_genres(token)
        if top_genres:
            genre_data = [{'genre': genre, 'count': count} for genre, count in top_genres]
            return jsonify(genre_data)
        else:
            return jsonify({'error': 'No top genres found'}), 404
    except Exception as e:
        print(f"Exception in api_top_genres: {str(e)}")
        return jsonify({'error': 'Failed to fetch top genres', 'details': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def api_chat():
    try:
        data = request.get_json()
        user_input = data.get('query', '')

        # Use Vertex AI Gemini model to get a response
        response = chat.send_message(
            [user_input],
            generation_config=generation_config,
            safety_settings=safety_settings
        )

        chatbot_response = response.candidates[0].content.parts[0].text

        return jsonify({'response': chatbot_response})
    except Exception as e:
        print(f"Error in /api/chat: {e}")
        return jsonify({'error': 'Failed to process chat request'}), 500

if __name__ == '__main__':
    app.run(debug=True)


#chatbot js:

// Chatbot.js
import React, { useState } from 'react';
import './Chatbot.css';

function Chatbot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const handleSend = async () => {
    if (input.trim()) {
      const newMessages = [...messages, { text: input, user: true }];
      setMessages(newMessages);
      setInput('');

      try {
        const response = await fetch('http://localhost:5000/api/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ query: input }),
        });

        const data = await response.json();
        setMessages([...newMessages, { text: data.response, user: false }]);
      } catch (error) {
        console.error('Error fetching chatbot response:', error);
        setMessages([...newMessages, { text: 'Sorry, something went wrong.', user: false }]);
      }
    }
  };

  return (
    <div className="chatbot">
      <h2>Chat with Your Stats</h2>
      <div className="chat-window">
        {messages.map((msg, index) => (
          <div key={index} className={`chat-message ${msg.user ? 'user' : 'bot'}`}>
            {msg.text}
          </div>
        ))}
      </div>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && handleSend()}
        placeholder="Type a message..."
      />
      <button onClick={handleSend}>Send</button>
    </div>
  );
}

export default Chatbot;
;