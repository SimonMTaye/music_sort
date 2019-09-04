from tinytag import TinyTag
from os import path


def parseSong(songPath: str):
    metadata = TinyTag.get(songPath)
    metadata.path = songPath
    metadata.name = path.basename(songPath)
    metadata.extension = path.splitext(songPath)[1]
    cleanMetadata(metadata)
    return metadata


# TODO: check issue with bitrate cleaning
def cleanMetadata(metadata):
    criticalProperties = ['artist', 'genre', 'album', 'albumartist']
    for property in criticalProperties:
        if type(getattr(metadata, property, 'Unknown')) != str:
            setattr(metadata, property, 'Unknown')
    if type(getattr(metadata, 'bitrate')) != float and type(getattr(metadata, 'bitrate')) != int:
        setattr(metadata, 'bitrate', 'Unknown')
