from fastapi import FastAPI, Header
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import requests

from pydantic import BaseModel

from clients.spotify_client import SpotifyClient


class PlayList(BaseModel):
    name: str
    titles: list[str]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")


@app.get("/.well-known/ai-plugin.json")
def read_plugin_config():
    return FileResponse("static/ai-plugin.json")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/create-playlist")
def create_playlist(playlist: PlayList, authorization: str = Header(None)):
    if authorization:
        access_token = authorization.split(" ")[1]
    else:
        return JSONResponse(status_code=403, content={"error": "Authorization header not found"})

    spotify = SpotifyClient(access_token)

    try:
        user_id = spotify.get_spotify_user_id(access_token)
        playlist_id = spotify.create_playlist(user_id, playlist.name)
    except requests.HTTPError as e:
        if e.response.status_code in [401, 403]:
            print(f"Authorization has expired: {e}")
            # Give ChatGPT explanation and a chance to refresh the token.
            return JSONResponse(status_code=403, content={"error": "Authorization has expired"})
        else:
            raise e

    song_uris = []
    for title in playlist.titles:
        tracks = spotify.search_track(title, limit=10)
        if len(tracks) > 0:
            song_uris.append(tracks[0]['uri'])
        else:
            print(f'No tracks found for {title}')

    spotify.add_songs_to_playlist(playlist_id, song_uris)
    return {'playlist_id': playlist_id, 'song_uris': song_uris}
