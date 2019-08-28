import shutil, os
import multiprocessing, pickle
from fuzzywuzzy import fuzz

## If audio fingerprinting is ever implemented, use that for comparisons
## TODO fix multiprocessing implementation
class duplicateManager:

    def __init__(self, songList, currentDir, useMultiProcessing):
        self.songList = songList
        self.checkedSongList = []
        self.duplicateSongList = []
        self.currentDir = currentDir
        self.duplicateIndices = []
        self.removeList = []
        self.usingMultiProcessing = useMultiProcessing
        self.duplicatesDir = os.path.join(currentDir, 'duplicates')
        os.makedirs(self.duplicatesDir, exist_ok=True)

    def checkForDuplicates(self):
        if not self.usingMultiProcessing:
            for uncheckedSong in self.songList:
                self.isDuplicate(uncheckedSong)
        elif self.usingMultiProcessing:
            pool = multiprocessing.Pool(multiprocessing.cpu_count())
            serializedSongList = pool.map(pickle.dumps, self.songList)
            pool.map(self.isDuplicateSerialiaztionHandler, serializedSongList)
                        
                
    def isDuplicate(self, uncheckedSong):
        duplicate = False
        if len(self.checkedSongList) == 0:
            self.checkedSongList.append(uncheckedSong)
        else:
            for index, song in enumerate(self.checkedSongList):
                titleSimilarity = fuzz.token_set_ratio(uncheckedSong.title, song.title)
                artistSimilarity = fuzz.token_set_ratio(uncheckedSong.artist, song.artist)
                similarityIndex = artistSimilarity + titleSimilarity
                similarityIndex = similarityIndex / 2
                if(similarityIndex > 93 ):
                    self.duplicateIndices.append({'uncheckedSongIndex': self.songList.index(uncheckedSong), 'originalSongIndex': index})
                    duplicate = True
            if not duplicate:
                    self.checkedSongList.append(uncheckedSong)

    def isDuplicateSerialiaztionHandler(self, serializedSong):
        uncheckedSong = pickle.Unpickler(serializedSong)
        self.isDuplicate(uncheckedSong)

    def handleDuplicates (self):
        for indices in self.duplicateIndices:
            originalSong = self.checkedSongList[indices['originalSongIndex']]
            duplicateSong = self.songList[indices['uncheckedSongIndex']]
            if(originalSong.bitrate != 320 and originalSong.bitrate < duplicateSong.bitrate ):
                self.duplicateSongList.append(originalSong)
                self.removeList.append(indices['originalSongIndex'])
            else:
                self.duplicateSongList.append(duplicateSong)                
        self.removeList.sort(reverse=True)
        for item in self.removeList:
            del self.checkedSongList[item]
        self.sortDuplicates()

    def sortDuplicates(self):
        for duplicate in self.duplicateSongList:
            try:
                shutil.move(duplicate.path, self.duplicatesDir)           
            except:
                print('Error handling: ' + duplicate.path)    

    def skipDuplicateChecking(self):
        self.checkedSongList = self.songList