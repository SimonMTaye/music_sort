# Template class for holding metadata
from dataclasses import dataclass


@dataclass(init=False)
class metadataHolder:
    title: str
    album: str
    albumartist: str
    artist: str
    genre: str
    bitrate: float
    track: str
    year: str
    path: str
    name: str
    extension: str
