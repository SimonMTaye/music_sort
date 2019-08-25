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
        self.newDir = os.path.join(self.initialDir,'Sorted')
        for property in self.chosenAttributes:
            self.newDir = os.path.join(self.newDir, str(getattr(self.selectedSong, property)))
        self.newDir = os.path.normpath(self.newDir)
        self.checkPathValidity()
        try:    
            os.makedirs(self.newDir, exist_ok=True)
        except:
            print('Error Processing: ' + self.selectedSong.name)    
            pass    

    def checkPathValidity (self):
        forbiddenCharacterList = [  ':' , '*' , '?' , '"' , '>' , '<' , '|']  
        forbiddenNameList = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 
        'COM4','COM5','COM6','COM7','COM8','COM9', 
        'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 
        'LPT7', 'LPT8', 'LPT9']
        for character in forbiddenCharacterList:
          self.newDir = self.newDir.replace(character, '') 
        name = os.path.basename(self.newDir)
        nameWithoutExt = os.path.splitext(name)[0]
        ext = os.path.splitext(name)[1]
        if name in forbiddenNameList:
            raise IllegalFileNameError('Illegal file name: ' + name)
        if nameWithoutExt.endswith('.'):
            name = nameWithoutExt[:len(nameWithoutExt) - 1] + ext

    
    
    def moveSong(self):
##        if(not os.path.exists(os.path.join(self.newDir, self.selectedSong.name))):
        try:
            shutil.move(self.selectedSong.path, self.newDir)
        except:
            print('Error moving: ' + self.selectedSong.name) 
            pass   

## Add function to make sure path is valid windows path
    ## \/ : * ? " < > |

class IllegalFileNameError (Exception):
    pass