import shutil
import os
from fuzzywuzzy import fuzz

from .metadataHolder import MetadataHolder


# TODO: fix multiprocessing implementation
class DuplicateManager:

    DUPLICATE_THRESHOLD = 95
    NOT_DUPLICATE = -1
    FIRST_SONG = 100
    SECOND_SONG = 200  

    def __init__(self, songTuple: tuple, currentDir: str):
        self.songTuple = songTuple
        self.currentDir = currentDir              
        self.duplicatesDir = os.path.join(currentDir, 'duplicates')

    # Wrapper function. Runs the filterDuplicate function and stores the resulting duplicate and filtered lists 
    # Runs moveDuplicate on the duplicate list and returns the filtered list
    def handleDuplicates(self):
        sortedSongListDict = self.filterDuplicates(self.songTuple)
        checkedList = sortedSongListDict['filteredList']
        duplicateList = sortedSongListDict['duplicateList']
        self.moveDuplicates(duplicateList, self.duplicatesDir)
        return checkedList

    # Travereses through a list and identifies duplicate songs. Pass a dict object containing a clean list and a duplicate list
    def filterDuplicates(self, songList: tuple):
        """ Looks through a list of songs and removes duplicates

        Looks through a list of songs and separtes the duplicates and filtered songs into separate lists.
        Each song in the list received as a parameter is checked against the filteredList
        If a duplicate is found, the one with higher bitrate is chosen. 
        If the filtered list is empty (first song being checked), then the song is automatically added to the list.
        
        Args:
            songList(list or tuple): the song list to be checked

        Returns:
            sortedSongListDict(dict): a dict containing two lists, the filteredList and the duplicateList
        """
        filteredList = []
        duplicateList = []
        print('Checking for duplicates')
        for uncheckedSongIndex, uncheckedSong in enumerate(songList):
            print('Checking song ' + str(uncheckedSongIndex + 1) + ' of ' + str(len(songList)), end='\r')
            if len(filteredList) == 0:
                filteredList.append(uncheckedSong)
                continue
            for checkedSongIndex, checkedSong in enumerate(filteredList):
                if not self.isDuplicate(uncheckedSong, checkedSong):
                    isLastSongInFilteredList = checkedSongIndex == len(filteredList)- 1
                    if isLastSongInFilteredList:
                        filteredList.append(uncheckedSong)
                        break
                else:
                    if self.pickBetterQuality(uncheckedSong, checkedSong) == self.FIRST_SONG:
                        del filteredList[checkedSongIndex]
                        filteredList.append(uncheckedSong)
                        duplicateList.append(checkedSong)
                    elif self.pickBetterQuality(uncheckedSong, checkedSong) == self.SECOND_SONG:
                        duplicateList.append(uncheckedSong)
                    break
        sortedSongListsDict = {"filteredList" : filteredList, "duplicateList" : duplicateList}             
        return sortedSongListsDict

    # Gets the similarity of the title and artist of two songs and determines if they are duplicates
    # They are identified as duplicates if the similarity is above the threshold
    def isDuplicate(self, firstSong: MetadataHolder, secondSong: MetadataHolder):
        titleSimilarity = self.getSimilarityRating(firstSong.title, secondSong.title)
        artistSimilarity = self.getSimilarityRating(firstSong.artist, secondSong.artist)
        similarityIndex = (artistSimilarity + titleSimilarity) / 2
        if(similarityIndex > self.DUPLICATE_THRESHOLD):
            if not self.isRemix(firstSong.title, secondSong.title):
                return True
        return False

    # Does a fuzzy string comparision
    def getSimilarityRating(self, firstString: str, secondString: str):
        return fuzz.token_set_ratio(firstString, secondString)

    # Checks if the song is remix       
    def isRemix(self, firstSongTitle: str, secondSongTitle: str):
        remixDenoters = ['remix', 'acoustic', 'instrumental']
        for denoter in remixDenoters:
            if denoter in firstSongTitle.lower() or denoter in secondSongTitle.lower():
                return True
        return False

    # Returns song with higher bitrate. If they have the same bitrate, returns the first song
    def pickBetterQuality(self, firstSong: MetadataHolder, secondSong: MetadataHolder):
        if secondSong.bitrate > firstSong.bitrate:
            return self.SECOND_SONG
        else:
            return self.FIRST_SONG

    # Move songs in the duplicate list to the designated directory         
    def moveDuplicates(self, duplicateSongList: list, duplicatesDir: str):
        os.makedirs(duplicatesDir, exist_ok=True)
        for duplicate in duplicateSongList:
            try:
                shutil.copy2(duplicate.path, self.duplicatesDir)
                os.remove(duplicate.path)
            except Exception as e:
                print('Error handling: ' + duplicate.path)
                print(e)
