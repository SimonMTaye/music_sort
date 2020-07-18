from os import cpu_count
from multiprocessing import Pool
from typing import List, Dict, Tuple
from .metadata_holder import MetadataHolder


# Returns song with higher bitrate. If they have the same bitrate, returns the first song
def is_worsequality(firstsong: MetadataHolder, secondsong: MetadataHolder):
    if secondsong.bitrate > firstsong.bitrate:
        return True
    else:
        return False


def sort_songs(song_list: List[MetadataHolder]) -> Dict[str, List[MetadataHolder]]:
    """
    Returns a dictionary with every artist as a key and a list of songs by that artist as a value 
    :param song_list: The list of songs
    :return: Sorted dictionary 
        
    """
    parsed_dict = {}
    for song in song_list:
        if parsed_dict.get(song.albumartist):
            parsed_dict.get(song.albumartist).append(song)
        else:
            parsed_dict[song.albumartist] = [song]
    return parsed_dict


def deep_filter(song_list: List[MetadataHolder]) -> Tuple[List[MetadataHolder], List[MetadataHolder]]:
    """ Looks through a list of songs and removes duplicates
    If a duplicate is found, the one with higher bitrate is chosen.

    Args:
        song_list(list or List): the song list to be checked

    Returns:
        sortedSongListDict(dict): a dict containing two lists, the filtered_list and the duplicate_list
    """
    filtered_list = []
    duplicate_list = []
    for song in song_list:
        for i, checked_song in enumerate(filtered_list):
            if song == checked_song:
                if is_worsequality(checked_song, song):
                    filtered_list[i] = song
                    duplicate_list.append(checked_song)
                else:
                    duplicate_list.append(song)
                break
        else:
            filtered_list.append(song)
    return (
        filtered_list,
        duplicate_list,
    )


def shallow_filter(song_list: List[MetadataHolder], multiprocessing: bool = False):
    song_dict = sort_songs(song_list)
    filtered_list = []
    duplicate_list = []
    if multiprocessing:
        with Pool(cpu_count()) as p:
            results = p.imap_unordered(deep_filter, song_dict.values())
            for result in results:
                duplicate_list.extend(result[1])
                filtered_list.extend(result[0])
    else:
        for artist_list in song_dict.values():
            sorted_dict = deep_filter(artist_list)
            filtered_list.extend(sorted_dict[0])
            duplicate_list.extend(sorted_dict[1])
    return (
        filtered_list,
        duplicate_list
    )
