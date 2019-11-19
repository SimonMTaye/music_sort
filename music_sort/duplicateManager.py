import shutil
import os
import multiprocessing
import pickle
from fuzzywuzzy import fuzz

from metadataHolder import MetadataHolder


# If audio fingerprinting is ever implemented, use that for comparisons
# TODO: fix multiprocessing implementation
class DuplicateManager:

    def __init__(self, songList: list, currentDir: str):
        self.songList = songList
        self.currentDir = currentDir
        self.NOT_DUPLICATE = -1
        self.FIRST_SONG = 100
        self.SECOND_SONG = 200        
        self.duplicatesDir = os.path.join(currentDir, 'duplicates')

    def handleDuplicates(self):
        sortedSongListDict = self.filterDuplicates(self.songList)
        checkedList = sortedSongListDict['filteredList']
        duplicateList = sortedSongListDict['duplicateList']
        self.moveDuplicates(duplicateList, self.duplicatesDir)
        return checkedList

    def filterDuplicates(self, songList: list):
        filteredList = []
        duplicateList = []
        for uncheckedSong in songList:
            if filteredList.__len__ == 0:
                filteredList.append(uncheckedSong)
                continue
            duplicateIndex = self.isDuplicate(uncheckedSong, filteredList)
            if duplicateIndex == self.NOT_DUPLICATE:
                filteredList.append(uncheckedSong)
            elif not duplicateIndex == self.NOT_DUPLICATE:
                duplicateSong = songList[duplicateIndex]
                if self.pickBetterQuality(uncheckedSong, duplicateSong) == self.FIRST_SONG:
                    filteredList.append(uncheckedSong)
                    duplicateList.append(duplicateSong)
                elif self.pickBetterQuality(uncheckedSong, duplicateSong) == self.SECOND_SONG:
                    filteredList.append(duplicateSong)
                    duplicateList.append(uncheckedSong)
        sortedSongListsDict = {"filteredList" : filteredList, "duplicateList" : duplicateList}             
        return sortedSongListsDict

    def isDuplicate(self, uncheckedSong: MetadataHolder, songList: list):
        for index, song in enumerate(songList):
            titleSimilarity = fuzz.token_set_ratio(
                uncheckedSong.title, song.title)
            artistSimilarity = fuzz.token_set_ratio(
                uncheckedSong.artist, song.artist)
            similarityIndex = artistSimilarity + titleSimilarity
            similarityIndex = similarityIndex / 2
            if(similarityIndex > 93):
                if not self.isRemix(uncheckedSong.title, song.title):
                    return index
        return self.NOT_DUPLICATE
           
    def isRemix(self, firstSongTitle: str, secondSongTitle: str):
        remixDenoters = ['remix', 'acoustic', 'instrumental']
        for denoter in remixDenoters:
            if denoter in firstSongTitle.lower() or denoter in secondSongTitle.lower():
                return True
        return False

    def pickBetterQuality(self, firstSong: MetadataHolder, secondSong: MetadataHolder):
        if secondSong.bitrate > firstSong.bitrate:
            return self.SECOND_SONG
        else:
            return self.FIRST_SONG
            
    def moveDuplicates(self, duplicateSongList: list, duplicatesDir: str):
        os.makedirs(duplicatesDir, exist_ok=True)
        for duplicate in duplicateSongList:
            try:
                shutil.copy2(duplicate.path, self.duplicatesDir)
                os.remove(duplicate.path)
            except Exception as e:
                print('Error handling: ' + duplicate.path)
                print(e)
