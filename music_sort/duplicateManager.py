import fuzzywuzzy, shutil

## If audio fingerprinting is ever implemented, use that for comparisons

class duplicateManager:

    def __init__(self, songList):
        self.songList = songList
        self.checkedSongList = []
        self.duplicateSongList = []

    def checkForDuplicates(self):
        for uncheckedSong in self.songList:
            for index, song in enumerate(self.checkedSongList):
                titleSimilarity = fuzzywuzzy.fuzz.token_set_ratio(uncheckedSong.title, song.title)
                artistSimilarity = fuzzywuzzy.fuzz.token_set_ratio(uncheckedSong.artist, song.artist)
                if((artistSimilarity + titleSimilarity) / 2 > 0.85 ):
                    self.handleDuplicate(uncheckedSong, index)

    def handleDuplicate (self, duplicateSong, originalSongIndex):
        originalSong = self.checkedSongList[originalSongIndex]
        if(originalSong.bitrate == 320 or originalSong.bitrate >= duplicateSong.bitrate ):
            self.duplicateSongList.append(duplicateSong)
        else:
            self.duplicateSongList.append(originalSong)
            del self.checkedSongList[originalSongIndex]

    def sortDuplicates(self):
        for duplicate in self.duplicateSongList:
            shutil.move(duplicate.path, 'duplicates')           