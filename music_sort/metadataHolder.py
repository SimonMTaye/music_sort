# Template class for holding metadata
from dataclasses import dataclass


@dataclass()
class MetadataHolder:
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

def __eq__(self, other: MetadataHolder):
    return (self.title,
        self.album,
        self.albumartist,
        self.artist,
        self.genre,
        self.bitrate,
        self.track,
        self.year,
        self.path,
        self.name,
        self.extension ==
        other.title,
        other.album,
        other.albumartist,
        other.artist,
        other.genre,
        other.bitrate,
        other.track,
        other.year,
        other.path,
        other.name,
        other.extension )
        
