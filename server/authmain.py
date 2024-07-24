import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
from flask import Flask, request, url_for, session, redirect
from requests import get, post
import json
import os
import csv
from dotenv import load_dotenv
import threading
from collections import Counter

app = Flask(__name__)

app.config['SESSION_COOKIE_NAME'] = 'SpotifySession'
app.secret_key = 'your_secret_key_here'  # Replace with a secure secret key
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
    auth_url = create_spotify_oauth().get_authorize_url()
    return redirect(auth_url)


@app.route('/redirect')
def redirect_page():
    code = request.args.get('code')
    token_info = create_spotify_oauth().get_access_token(code)
    session[TOKEN_INFO] = token_info

    token = token_info['access_token']
    headers = get_auth_header(token)
    user_profile_response = get("https://api.spotify.com/v1/me", headers=headers)
    user_profile = json.loads(user_profile_response.content)
    session['user_id'] = user_profile['id']

    # Store user ID in CSV
    store_user_id_csv(user_profile['id'])

    return redirect(url_for('home', _external=True))


@app.route('/home')
def home():
    try:
        token_info = get_token()
    except:
        print("User not logged in")
        return redirect('/')

    token = token_info['access_token']

    # Start the terminal menu in a separate thread
    threading.Thread(target=main_menu, args=(token,)).start()

    return "✅✅✅✅OAuth successful. Check terminal for menu."


def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        return redirect(url_for('login', _external=False))

    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if is_expired:
        spotify_oauth = create_spotify_oauth()
        token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])
        session[TOKEN_INFO] = token_info

    return token_info


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def store_user_id_csv(user_id):
    file_exists = os.path.isfile('.venv/user_ids.csv')
    with open('.venv/user_ids.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['User ID'])
        writer.writerow([user_id])


def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content).get("artists", {}).get("items", [])
    if len(json_result) == 0:
        print("No artist with this name exists...")
        return None

    return json_result[0]


def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content).get("tracks", [])
    return json_result


def get_user_top_tracks(token):
    url = "https://api.spotify.com/v1/me/top/tracks"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    if result.status_code == 200:
        json_result = json.loads(result.content).get("items", [])
        return json_result
    else:
        print(f"Failed to get top tracks: {result.status_code}")
        print(result.content)
        return None


def get_saved_tracks(token):
    url = "https://api.spotify.com/v1/me/tracks"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    if result.status_code == 200:
        json_result = json.loads(result.content).get("items", [])
        return json_result
    else:
        print(f"Failed to get saved tracks: {result.status_code}")
        print(result.content)
        return None


def get_followed_artists(token):
    url = "https://api.spotify.com/v1/me/following?type=artist"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    if result.status_code == 200:
        json_result = json.loads(result.content).get("artists", {}).get("items", [])
        return json_result
    else:
        print(f"Failed to get followed artists: {result.status_code}")
        print(result.content)
        return None


def get_user_playlists(token):
    url = "https://api.spotify.com/v1/me/playlists"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    if result.status_code == 200:
        json_result = json.loads(result.content).get("items", [])
        return json_result
    else:
        print(f"Failed to get user playlists: {result.status_code}")
        print(result.content)
        return None


def get_playlist_tracks(token, playlist_id):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    if result.status_code == 200:
        json_result = json.loads(result.content).get("items", [])
        return json_result
    else:
        print(f"Failed to get playlist tracks: {result.status_code}")
        print(result.content)
        return None


def get_user_top_artists(token):
    url = "https://api.spotify.com/v1/me/top/artists?limit=10"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    if result.status_code == 200:
        json_result = json.loads(result.content).get("items", [])
        return json_result
    else:
        print(f"Failed to get top artists: {result.status_code}")
        print(result.content)
        return None


def add_song_to_playlist(token, playlist_id, track_uri):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = get_auth_header(token)
    headers["Content-Type"] = "application/json"
    data = json.dumps({"uris": [track_uri]})

    result = post(url, headers=headers, data=data)

    if result.status_code == 201:
        print(f"Successfully added track to playlist {playlist_id}.")
    else:
        print(f"Failed to add track to playlist: {result.status_code}")
        print(result.content)


def view_top_songs(token):
    artist_name = input("Enter the artist name: ")
    result = search_for_artist(token, artist_name)
    if result:
        artist_id = result["id"]
        songs = get_songs_by_artist(token, artist_id)
        print(f"\nTop 10 songs by {artist_name}:\n")
        for idx, song in enumerate(songs):
            print(f"{idx + 1}. {song['name']}")

        add_choice = input("Enter the number of the song to add to a playlist, or '0' to go back: ")
        if add_choice.isdigit() and 1 <= int(add_choice) <= len(songs):
            track_uri = songs[int(add_choice) - 1]['uri']
            playlists = get_user_playlists(token)

            if playlists:
                print("\nYour Playlists:\n")
                for idx, playlist in enumerate(playlists):
                    print(f"{idx + 1}. {playlist['name']} (ID: {playlist['id']})")

                playlist_choice = input("Enter the number of the playlist to add the song to, or '0' to go back: ")
                if playlist_choice.isdigit() and 1 <= int(playlist_choice) <= len(playlists):
                    selected_playlist_id = playlists[int(playlist_choice) - 1]['id']
                    add_song_to_playlist(token, selected_playlist_id, track_uri)
                else:
                    print("Invalid choice. Returning to the main menu.")
            else:
                print("No playlists found.")
        else:
            print("Invalid choice. Returning to the main menu.")
    else:
        print(f"No information found for artist: {artist_name}")


def view_saved_tracks(token):
    saved_tracks = get_saved_tracks(token)
    if saved_tracks:
        print("\nYour Liked Tracks (Recent 20):\n")
        for idx, item in enumerate(saved_tracks):
            track = item['track']
            print(f"{idx + 1}. {track['name']} by {track['artists'][0]['name']}")
    else:
        print("No liked tracks found.")


def view_top_tracks(token):
    user_top_tracks = get_user_top_tracks(token)
    if user_top_tracks is not None:
        print("User's Top Tracks:")
        for idx, track in enumerate(user_top_tracks):
            print(f"{idx + 1}. {track['name']} by {track['artists'][0]['name']}")
    else:
        print("Failed to retrieve user's top tracks.")


def view_followed_artists(token):
    followed_artists = get_followed_artists(token)
    if followed_artists is not None:
        print("User's Followed Artists:")
        for idx, artist in enumerate(followed_artists):
            print(f"{idx + 1}. {artist['name']}")
    else:
        print("Failed to retrieve followed artists.")


def view_user_playlists(token):
    user_playlists = get_user_playlists(token)
    if user_playlists is not None:
        print("User's Playlists:")
        for idx, playlist in enumerate(user_playlists):
            print(f"{idx + 1}. {playlist['name']}")
    else:
        print("Failed to retrieve user's playlists.")


def view_top_artists(token):
    top_artists = get_user_top_artists(token)
    if top_artists:
        print("\nYour Top Artists:\n")
        for idx, artist in enumerate(top_artists):
            print(f"{idx + 1}. {artist['name']}")
    else:
        print("No top artists found.")


def get_top_genres(token):
    top_artists = get_user_top_artists(token)
    if top_artists:
        genres = []
        for artist in top_artists:
            genres.extend(artist.get('genres', []))
        genre_counts = Counter(genres)
        top_genres = genre_counts.most_common(5)
        return top_genres
    else:
        print("No top artists found.")
        return None


def view_top_genres(token):
    top_genres = get_top_genres(token)
    if top_genres:
        print("\nYour Top Genres:\n")
        for idx, (genre, count) in enumerate(top_genres):
            print(f"{idx + 1}. {genre} ({count} artists)")
    else:
        print("No top genres found.")


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
        json_result = json.loads(result.content).get("tracks", [])
        return json_result
    else:
        print(f"Failed to get recommendations: {result.status_code}")
        print(result.content)
        return None


def view_recommendations(token):
    top_tracks = get_user_top_tracks(token)
    top_artists = get_user_top_artists(token)

    seed_tracks = [track['id'] for track in top_tracks[:5]] if top_tracks else []
    seed_artists = [artist['id'] for artist in top_artists[:5]] if top_artists else []

    recommendations = get_recommendations(token, seed_artists=seed_artists, seed_tracks=seed_tracks)
    if recommendations:
        print("\nTop 10 Curated Recommended Songs:\n")
        for idx, track in enumerate(recommendations):
            print(f"{idx + 1}. {track['name']} by {track['artists'][0]['name']}")
    else:
        print("No recommendations found.")


def main_menu(token):
    while True:
        print("\nMenu:")
        print("1. View top songs by artist")
        print("2. View liked tracks")
        print("3. View top tracks")
        print("4. View followed artists")
        print("5. View user playlists")
        print("6. View top artists")
        print("7. View top genres")
        print("8. View top 10 curated recommended songs")
        print("9. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            view_top_songs(token)
        elif choice == "2":
            view_saved_tracks(token)
        elif choice == "3":
            view_top_tracks(token)
        elif choice == "4":
            view_followed_artists(token)
        elif choice == "5":
            view_user_playlists(token)
        elif choice == "6":
            view_top_artists(token)
        elif choice == "7":
            view_top_genres(token)
        elif choice == "8":
            view_recommendations(token)
        elif choice == "9":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    app.run(debug=True)