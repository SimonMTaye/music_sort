from tinytag import TinyTag, TinyTagException
from os import path

from typing import List, Dict
from .metadata_holder import MetadataHolder

DEFAULT_ATTRIBUTE_VALUE = "Unknown"
DEFAULT_BITRATE_VALUE = float(0.00)


def parse_song_list(song_list: List[str]) -> List[MetadataHolder]:
    parsed_list = list()
    for song in song_list:
        try:
            metadata = parse_song(song)
            parsed_list.append(metadata)
        except (PermissionError, TinyTagException) as e:
            print(song)
            print(e)
            continue
    return parsed_list


def parse_song(song_path: str):
    song_info = TinyTag.get(song_path)
    metadata = MetadataHolder(
        song_info.title,
        song_info.album,
        song_info.albumartist,
        song_info.artist,
        song_info.genre,
        song_info.bitrate,
        song_info.track,
        song_info.year,
        song_path,
        path.basename(song_path),
        path.splitext(song_path)[1],
    )
    clean_metadata(metadata)
    return metadata


def clean_metadata(metadata):
    critical_properties = [
        "title",
        "album",
        "albumartist",
        "artist",
        "genre",
        "track",
        "year",
    ]
    for property in critical_properties:
        if type(getattr(metadata, property, DEFAULT_ATTRIBUTE_VALUE)) != str:
            setattr(metadata, property, DEFAULT_ATTRIBUTE_VALUE)
    if type(getattr(metadata, "bitrate", DEFAULT_ATTRIBUTE_VALUE)) != float:
        setattr(metadata, "bitrate", DEFAULT_BITRATE_VALUE)
