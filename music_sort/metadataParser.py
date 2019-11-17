from tinytag import TinyTag
from os import path

from . import metadataHolder

def parseSongArray(songArray):
    parsedSongs = []
    for song in songArray:
        metadata = parseSong(song)
        parsedSongs.append(metadata)
    return parsedSongs

def parseSong(songPath: str):
    songInfo = TinyTag.get(songPath)
    metadata = metadataHolder.MetadataHolder()
    metadata.title = songInfo.title
    metadata.album = songInfo.album
    metadata.albumartist = songInfo.albumartist
    metadata.artist = songInfo.artist
    metadata.genre = songInfo.genre
    metadata.bitrate = songInfo.bitrate
    metadata.track = songInfo.track
    metadata.year = songInfo.year
    metadata.path = songPath
    metadata.name = path.basename(songPath)
    metadata.extension = path.splitext(songPath)[1]
    cleanMetadata(metadata)
    return metadata

def cleanMetadata(metadata):
    criticalProperties = ['title', 'album',
                          'albumartist', 'artist', 'genre', 'track', 'year']
    for property in criticalProperties:
        if type(getattr(metadata, property, 'Unknown')) != str:
            setattr(metadata, property, 'Unknown')
    if type(getattr(metadata, 'bitrate')) != float:
        setattr(metadata, 'bitrate', 'Unknown')
