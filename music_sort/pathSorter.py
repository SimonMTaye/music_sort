import os, shutil

class pathSorter:


    ## Choose which properties will be used to Sort Songs (read throuh python parameters for better opitons but use tuples for now)
    def _inti_(self, sortUsing: tuple, songMetadata):
        self.chosenAttributes = sortUsing
        for attribute in self.chosenAttributes:
            if(attribute not in ['title', 'album', 'artist', 'genre', 'bitrate','albumartist']):
                del self.chosenAttributes[attribute]
        self.selectedSong = songMetadata
    
    def createDir(self):
        self.newDir = ""
        for property in self.chosenAttributes:
            self.newDir = self.newDir + '/' + str(self.selectedSong[property])
        self.newDir = os.path.normpath(self.newDir)    
        os.makedirs(self.newDir, exist_ok=True)
        
    
    def moveSong(self):
        if(not os.path.exists(self.newDir)):
            shutil.move(self.selectedSong.path, self.newDir)