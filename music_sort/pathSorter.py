import os, shutil

class pathSorter:


    ## Choose which properties will be used to Sort Songs (read throuh python parameters for better opitons but use tuples for now)
    def __init__(self, sortUsing: tuple, songMetadata, initialDir):
        self.chosenAttributes = sortUsing
        for attribute in self.chosenAttributes:
            if(attribute not in ['album', 'artist', 'genre', 'bitrate','albumartist']):
                del self.chosenAttributes[attribute]
        self.selectedSong = songMetadata
        self.initialDir = initialDir
    
    def createDir(self):
        self.newDir = os.path.join(self.initialDir, 'Sorted')
        for property in self.chosenAttributes:
            self.newDir = os.path.join(self.newDir, str(getattr(self.selectedSong, property)))
        self.newDir = os.path.normpath(self.newDir)    
        os.makedirs(self.newDir, exist_ok=True)
        
    
    def moveSong(self):
        if(not os.path.exists(os.path.join(self.newDir, self.selectedSong.name))):
            shutil.move(self.selectedSong.path, self.newDir)