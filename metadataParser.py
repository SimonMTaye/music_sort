from tinytag import TinyTag
from os.path import basename

class metadataParser:

    def parseSong(self, songPath: str):
        metadata = TinyTag.get(songPath)
        metadata.path = songPath
        metadata.name = basename(songPath)
        return metadata