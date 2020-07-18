import fire
import os

from . import duplicate_manager
from . import metadata_parser
from . import file_scanner
from . import path_sorter

# TODO:  add multiprocessing

PROPERTIES_TUPLE = tuple(["artist", "genre", "album", "bitrate", "albumartist", "year"])
SUPPORTED_FILE_TYPES = tuple(["mp3", "m4a", "flac", "ogg", "wav"])


def verify_sorting_properties(user_properties):
    """ Verify that given sorting properties are appropirate, raise ValueError if not"""
    for attribute in user_properties:
        if attribute not in PROPERTIES_TUPLE:
            raise ValueError(
                "Unsupported value "
                + attribute
                + ' used as sorting property. Use: "artist", "genre", "album", "bitrate", "albumartist" or "year"'
            )


def verify_file_types(userFileTypes):
    """ Verify that given file types are appropirate, raise ValueError if not"""
    for file_type in userFileTypes:
        if file_type not in SUPPORTED_FILE_TYPES:
            raise ValueError(
                "Unsupported music file type "
                + file_type
                + ". Use: mp3, m4a, flac, ogg or wav"
            )


def sortMusic(
        root_dir=os.getcwd(),
        recursive=True,
        sorting_properties=tuple(["albumartist", "album"]),
        keep_file_name=True,
        music_file_types=tuple(["mp3", "m4a", "flac"]),
        check_for_duplicates=True,
        do_deep_duplicate_search=False,
        multiprocessing: bool = False
):
    # Verify that given parameters are appropirate, raise ValueError if not
    verify_sorting_properties(sorting_properties)
    verify_file_types(music_file_types)

    print("Scanning for music...")
    scanned_files = file_scanner.scan_folder(root_dir, music_file_types, recursive)
    print("Parsing scanned music..")
    parsed_songs = metadata_parser.parse_song_list(scanned_files)

    if check_for_duplicates:
        print("Checking for duplicates...")
        if do_deep_duplicate_search:
            checked_songs = duplicate_manager.deep_filter(parsed_songs)
        else:
            checked_songs = duplicate_manager.shallow_filter(parsed_songs, multiprocessing)
        filtered_songs = checked_songs[0]
        duplicate_songs = checked_songs[1]
    else:
        filtered_songs = parsed_songs
        duplicate_songs = []
    print("Moving songs to new directories")
    path_man = path_sorter.PathSorter(sorting_properties, root_dir, keep_file_name)
    path_man.move_songs(filtered_songs, duplicate_songs)


if __name__ == "__main__":
    fire.Fire(sortMusic)
