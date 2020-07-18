# Template class for holding metadata
from dataclasses import dataclass
from fuzzywuzzy import fuzz

DUPLICATE_THRESHOLD = 95


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

    def __eq__(self, other: "MetadataHolder"):
        return is_duplicate(self, other)


def is_duplicate(firstSong: MetadataHolder, secondSong: MetadataHolder):
    if is_remix(firstSong.title, secondSong.title):
        return False

    titleSimilarity = get_similarity(firstSong.title, secondSong.title)
    if titleSimilarity > 95:
        artistSimilarity = get_similarity(
            firstSong.artist, secondSong.artist
        )
        similarityIndex = (artistSimilarity + titleSimilarity) / 2
        if similarityIndex > DUPLICATE_THRESHOLD:
            return True
    else:
        return False


def get_similarity(first_string: str, second_string: str):
    return fuzz.token_set_ratio(first_string, second_string)


# Checks if the song is remix
def is_remix(first_song_title: str, second_song_title: str):
    remixDenoters = ["remix", "acoustic", "instrumental"]
    for denoter in remixDenoters:
        if denoter in first_song_title.lower() or denoter in second_song_title.lower():
            return True
    return False
