from pydantic import BaseModel


class TrackTitleList(BaseModel):
    titles: list[str]


class TrackURIList(BaseModel):
    track_uris: list[str]


class Artist(BaseModel):
    name: str
    id: str
    uri: str
    href: str
    external_urls: dict[str, str]


class Track(BaseModel):
    title: str
    track_uri: str
    artists: list[Artist]
    duration_ms: int
    explicit: bool


class TracksResponse(BaseModel):
    tracks: list[Track]
