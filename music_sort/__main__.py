import fire, time

import duplicateManager, metadataParser, pathSorter, fileScanner

##Potentially add multiprocessing

def sortMusic(dir=r'C:\Users\smtsi\Code\Test', recursive=True, sortingProperties=('artist', 'album'), musicFileTypes=['mp3','m4a','flac'], checkForDuplicate=True):
    for property in sortingProperties:
        if property not in ['artist', 'genre','album', 'bitrate', 'albumartist']:
            raise ValueError('Unsupported value used as sorting property. Use: "artist", "genre", "album", "bitrate" or "albumartist"')
    for type in musicFileTypes:
        if type not in ['mp3', 'm4a', 'flac','ogg','wav']:
            raise ValueError('Unsupported music file type. Use: mp3, m4a, flac, ogg or wav')  
    if recursive:
        start = time.time()
        scannedFiles = fileScanner.scanFolderRecursively(dir, musicFileTypes)
        end = time.time()
        print("File scanning took: " + str(end - start))
    elif not recursive:
        scannedFiles = fileScanner.scanFolder(dir, musicFileTypes)
    parsedSongs = []
    start = time.time()        
    for file in scannedFiles:
        metadata = metadataParser.parseSong(file)
        parsedSongs.append(metadata)
    end = time.time()
    print("Parsing songs took: " + str(end - start))    
    duplicateMan = duplicateManager.duplicateManager(parsedSongs, dir)
    if(checkForDuplicate):
        start = time.time()
        duplicateMan.checkForDuplicates()
        end = time.time()
        print("Duplicate sorting took: " + str(end - start))
    else:
        duplicateMan.skipDuplicateChecking()    
    duplicateMan.handleDuplicates()
    parsedSongs = duplicateMan.checkedSongList
    start = time.time()
    for song in parsedSongs:
        pathMan = pathSorter.pathSorter(sortingProperties, song, dir)
        pathMan.createDir()
        pathMan.moveSong()
    end = time.time()
    print("Moving songs took: " + str(end - start))
if __name__ == '__main__':
    fire.Fire(sortMusic)        