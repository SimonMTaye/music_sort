import shutil
import os
import multiprocessing
import pickle
from fuzzywuzzy import fuzz


# If audio fingerprinting is ever implemented, use that for comparisons
# TODO: fix multiprocessing implementation
class duplicateManager:

    def __init__(self, songList, currentDir):
        self.songList = songList
        self.checkedSongList = []
        self.duplicateSongList = []
        self.currentDir = currentDir
        self.duplicateIndices = []
        self.removeList = []
        self.duplicatesDir = os.path.join(currentDir, 'duplicates')
        os.makedirs(self.duplicatesDir, exist_ok=True)

    def checkForDuplicates(self):
        for uncheckedSong in self.songList:
            self.isDuplicate(uncheckedSong)
       

    def isDuplicate(self, uncheckedSong):
        duplicate = False
        if len(self.checkedSongList) == 0:
            self.checkedSongList.append(uncheckedSong)
        else:
            for index, song in enumerate(self.checkedSongList):
                titleSimilarity = fuzz.token_set_ratio(
                    uncheckedSong.title, song.title)
                artistSimilarity = fuzz.token_set_ratio(
                    uncheckedSong.artist, song.artist)
                similarityIndex = artistSimilarity + titleSimilarity
                similarityIndex = similarityIndex / 2
                if(similarityIndex > 93):
                    if not self.isRemix(uncheckedSong.title, song.title):
                        self.duplicateIndices.append({'uncheckedSongIndex': self.songList.index(
                            uncheckedSong), 'originalSongIndex': index})
                        duplicate = True
            if not duplicate:
                self.checkedSongList.append(uncheckedSong)

    def isRemix(self, uncheckedSongTitle: str, songTitle: str):
        isRemix = False
        remixDenoters = ['remix', 'acoustic', 'instrumental']
        for denoter in remixDenoters:
            if denoter in uncheckedSongTitle.lower():
                isRemix = True
            elif denoter in songTitle.lower():
                isRemix = True
        return isRemix

    def handleDuplicates(self):
        for indices in self.duplicateIndices:
            originalSong = self.checkedSongList[indices['originalSongIndex']]
            duplicateSong = self.songList[indices['uncheckedSongIndex']]
            if(originalSong.bitrate != 320 and originalSong.bitrate < duplicateSong.bitrate):
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
                shutil.copy2(duplicate.path, self.duplicatesDir)
                os.remove(duplicate.path)
            except Exception as e:
                print('Error handling: ' + duplicate.path)
                print(e)

    def skipDuplicateChecking(self):
        self.checkedSongList = self.songList
