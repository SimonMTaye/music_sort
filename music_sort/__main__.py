import fire

import duplicateManager, metadataParser, pathSorter, fileScanner

def sortMusic(dir=r'C:\Users\smtsi\Code\Test', recursive=True, sortingProperties=('artist', 'album'), musicFileTypes=['mp3','m4a','flac']):
    for property in sortingProperties:
        if property not in ['artist', 'genre','album', 'bitrate', 'albumartist']:
            raise ValueError('Unsupported value used as sorting property. Use: "artist", "genre", "album", "bitrate" or "albumartist"')
    for type in musicFileTypes:
        if type not in ['mp3', 'm4a', 'flac','ogg','wav']:
            raise ValueError('Unsupported music file type. Use: mp3, m4a, flac, ogg or wav')  
    if recursive:
        scannedFiles = fileScanner.scanFolderRecursively(dir, musicFileTypes)
    elif not recursive:
        scannedFiles = fileScanner.scanFolder(dir, musicFileTypes)
    parsedSongs = []    
    for file in scannedFiles:
        metadata = metadataParser.parseSong(file)
        parsedSongs.append(metadata)
    duplicateMan = duplicateManager.duplicateManager(parsedSongs, dir)
    duplicateMan.checkForDuplicates()
    duplicateMan.handleDuplicates()
    duplicateMan.sortDuplicates()
    parsedSongs = duplicateMan.checkedSongList
    for song in parsedSongs:
        pathMan = pathSorter.pathSorter(sortingProperties, song, dir)
        pathMan.createDir()
        pathMan.moveSong()

if __name__ == '__main__':
    fire.Fire(sortMusic)        