from tinytag import TinyTag
from os.path import basename

def parseSong(songPath: str):
    metadata = TinyTag.get(songPath)
    metadata.path = songPath
    metadata.name = basename(songPath)
    return metadata