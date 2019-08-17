from tinytag import TinyTag
from os.path import basename

def parseSong(songPath: str):
    metadata = TinyTag.get(songPath)
    metadata.path = songPath
    metadata.name = basename(songPath)
    return metadata

##def cleanMetadata(metadata):
    ## For everyattribute, check if type is list, str or number. If not set to unknown
    ## If value is a list, extract into single string for easy dir creation