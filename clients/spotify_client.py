import requests

class SpotifyClient:
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = 'https://api.spotify.com/v1'

    def _auth_headers(self):
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

    def get_spotify_user_id(self, access_token: str):
        response = requests.get(
            f'{self.base_url}/me', headers=self._auth_headers())

        if response.status_code == 200:
            user_data = response.json()
            return user_data['id']
        else:
            print(f'Error: {response.status_code}')
            return None

    def create_playlist(self, user_id: str, name: str):
        data = {
            'name': name
        }
        response = requests.post(
            f'{self.base_url}/users/{user_id}/playlists', headers=self._auth_headers(), json=data)
        response.raise_for_status()

        return response.json()['id']

    def add_songs_to_playlist(self, playlist_id: str, song_uris: list[str]):
        data = {
            'uris': song_uris
        }
        response = requests.post(
            f'{self.base_url}/playlists/{playlist_id}/tracks', headers=self._auth_headers(), json=data)
        response.raise_for_status()

    def search_track(self, query: str, limit=10):
        params = {
            'q': query,
            'type': 'track',
            'limit': limit
        }
        response = requests.get(
            '{self.base_url}/search', headers=self._auth_headers(), params=params)
        response.raise_for_status()
        return response.json()['tracks']['items']
