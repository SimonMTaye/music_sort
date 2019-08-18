import shutil, os
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
        os.makedirs(self.duplicatesDir, exist_ok=True)

    def checkForDuplicates(self):
        for index, uncheckedSong in enumerate(self.songList):
            if not self.isDuplicate(uncheckedSong, index):
                self.checkedSongList.append(uncheckedSong)
            
    def isDuplicate(self, uncheckedSong, uncheckedSongIndex):
        isDuplicate = False
        for index, song in enumerate(self.checkedSongList):
            titleSimilarity = fuzz.token_set_ratio(uncheckedSong.title, song.title)
            artistSimilarity = fuzz.token_set_ratio(uncheckedSong.artist, song.artist)
            similarityIndex = artistSimilarity + titleSimilarity
            similarityIndex = similarityIndex / 2
            if(similarityIndex > 85 ):
                self.duplicateIndices.append({'uncheckedSongIndex': uncheckedSongIndex, 'originalSongIndex': index})
                isDuplicate = True
                break
        return isDuplicate        

    def handleDuplicates (self):
        for indices in self.duplicateIndices:
            originalSong = self.checkedSongList[indices['originalSongIndex']]
            duplicateSong = self.songList[indices['uncheckedSongIndex']]
            if(originalSong.bitrate == 320 or originalSong.bitrate >= duplicateSong.bitrate ):
                self.duplicateSongList.append(duplicateSong)
            else:
                self.duplicateSongList.append(originalSong)
                self.checkedSongList.remove(originalSong)

    def sortDuplicates(self):
        for duplicate in self.duplicateSongList:
            shutil.move(duplicate.path, self.duplicatesDir)           
            