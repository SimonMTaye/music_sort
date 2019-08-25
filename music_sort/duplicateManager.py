import shutil, os
import multiprocessing
from fuzzywuzzy import fuzz

## If audio fingerprinting is ever implemented, use that for comparisons
class duplicateManager:

    def __init__(self, songList, currentDir):
        self.songList = songList
        self.checkedSongList = []
        self.duplicateSongList = []
        self.currentDir = currentDir
        self.duplicatesDir = os.path.join(currentDir, 'duplicates')
        self.duplicateIndices = []
        self.removeList = []
        ##self.usingMultiProcessing = useMultiProcessing
        os.makedirs(self.duplicatesDir, exist_ok=True)

    def checkForDuplicates(self):
        ##if not self.usingMultiProcessing:
        for uncheckedSong in self.songList:
            self.isDuplicate(uncheckedSong)
        ##elif self.usingMultiProcessing:
        ##    pool = multiprocessing.Pool(multiprocessing.cpu_count())
        ##    pool.map(self.isDuplicate, self.songList)
                        
                
    def isDuplicate(self, uncheckedSong):
        for index, song in enumerate(self.checkedSongList):
            titleSimilarity = fuzz.token_set_ratio(uncheckedSong.title, song.title)
            artistSimilarity = fuzz.token_set_ratio(uncheckedSong.artist, song.artist)
            similarityIndex = artistSimilarity + titleSimilarity
            similarityIndex = similarityIndex / 2
            if(similarityIndex > 93 ):
                self.duplicateIndices.append({'uncheckedSongIndex': self.songList.index(uncheckedSong), 'originalSongIndex': index})
        self.checkedSongList.append(uncheckedSong)

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