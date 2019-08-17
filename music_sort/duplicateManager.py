import fuzzywuzzy, shutil

## If audio fingerprinting is ever implemented, use that for comparisons

class duplicateManager:

    def __init__(self, songList):
        self.songList = songList
        self.duplicateSongList = []

    def checkIfDuplicate(self, newSong):
        for index, oldSong in enumerate(self.songList):
            titleSimilarity = fuzzywuzzy.fuzz.token_set_ratio(oldSong.title, newSong.title)
            artistSimilarity = fuzzywuzzy.fuzz.token_set_ratio(oldSong.artist, newSong.artist)
            if((artistSimilarity + titleSimilarity) / 2 > 0.85 ):
                self.handleDuplicate(newSong, index)
        ## -1 Duplicate value shows song doesn't exist in list        
        return ({'isDuplicate': False, 'index': -1})

    def handleDuplicate (self, duplicateSong, originalSongIndex):
        originalSong = self.songList[originalSongIndex]
        if(originalSong.bitrate == 320 or originalSong.bitrate >= duplicateSong.bitrate ):
            self.duplicateSongList.append(duplicateSong)
        else:
            self.duplicateSongList.append(originalSong)
            del self.songList[originalSongIndex]

    def sortDuplicates(self):
        for duplicate in self.duplicateSongList:
            shutil.move(duplicate.path, 'duplicates')           