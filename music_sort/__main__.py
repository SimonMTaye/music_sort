import fire
import time

from . import duplicateManager
from . import metadataParser
from . import fileScanner
from . import pathSorter


# TODO:  add multiprocessing

PROPERTIES_TUPLE = tuple(['artist', 'genre', 'album', 'bitrate', 'albumartist', 'year'])
SUPPORTED_FILE_TYPES = tuple(['mp3', 'm4a', 'flac', 'ogg', 'wav'])

def sortMusic(dir, recursive=True, sortingProperties=tuple(['albumartist', 'album']), useTrackTitle=False, musicFileTypes=['mp3', 'm4a', 'flac'], checkForDuplicates=True):
    # Verify that given parameters are appropirate, raise ValueError if not
    verifySortingProperties(sortingProperties)
    verifyFileTypes(musicFileTypes)
    if recursive:
        start = time.time()
        print("Scanning Files...")
        scannedFiles = fileScanner.scanFolderRecursively(dir, musicFileTypes)
        end = time.time()
        print("File scanning took: " + str(end - start))
    elif not recursive:
        scannedFiles = fileScanner.scanFolder(dir, musicFileTypes)
    start = time.time()
    parsedSongs = metadataParser.parseSongList(scannedFiles)
    end = time.time()
    print("Parsing songs took: " + str(end - start))
    duplicateMan = duplicateManager.DuplicateManager(parsedSongs, dir)
    if(checkForDuplicates):
        start = time.time()
        checkedSongs = duplicateMan.filterDuplicates(tuple(parsedSongs))
        filteredSongs = checkedSongs['filteredList']
        duplicateSongs = checkedSongs['duplicateList']        
        end = time.time()
        print("Duplicate sorting took: " + str(end - start))
        start = time.time()
        pathMan = pathSorter.PathSorter(sortingProperties, dir, useTrackTitle)
        pathMan.moveSongs(filteredSongs, duplicateSongs)
        end = time.time()
        print("Moving songs took: " + str(end - start))
    else:
        start = time.time()
        pathMan = pathSorter.PathSorter(sortingProperties, dir, useTrackTitle)
        pathMan.moveSongs(parsedSongs, [])
        end = time.time()
        print("Moving songs took: " + str(end - start))


def verifySortingProperties(userProperties):
    """ Verify that given sorting properties are appropirate, raise ValueError if not"""
    for property in userProperties:
        if property not in PROPERTIES_TUPLE:
            raise ValueError(
                'Unsupported value ' + property + ' used as sorting property. Use: "artist", "genre", "album", "bitrate", "albumartist" or "year"'
                )
def verifyFileTypes(userFileTypes):
    """ Verify that given file types are appropirate, raise ValueError if not"""
    for type in userFileTypes:
        if type not in SUPPORTED_FILE_TYPES:
            raise ValueError(
                'Unsupported music file type ' + property + '. Use: mp3, m4a, flac, ogg or wav'
                )

if __name__ == '__main__':
    fire.Fire(sortMusic)
