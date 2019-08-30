import os, shutil

class pathSorter:

    def __init__(self, sortUsing: tuple, songMetadata, initialDir, useTrackTitle):
        self.chosenAttributes = sortUsing
        for attribute in self.chosenAttributes:
            if(attribute not in ['album', 'artist', 'genre', 'bitrate','albumartist']):
                del self.chosenAttributes[attribute]
        self.selectedSong = songMetadata
        self.newDir = 'Sorted'
        for property in self.chosenAttributes:
            self.newDir = os.path.join(self.newDir, str(getattr(self.selectedSong, property)))
            self.checkPathValidity()
        self.newDir = os.path.normpath(self.newDir)
        self.newDir = os.path.join(initialDir, self.newDir)
        try:
            self.checkPathValidity()
            os.makedirs(self.newDir, exist_ok=True)
        except Exception as e:
            self.newDir = os.path.join(initialDir, 'Sorted', 'Unknown')
            os.makedirs(self.newDir, exist_ok=True)
            print("Error creating directory for: " + self.selectedSong.path)
            print(e)
            pass
        if(useTrackTitle):
            self.newDir = os.path.join(self.newDir, self.selectedSong.title)
            self.newDir = os.path.normpath(self.newDir)
            self.checkPathValidity()
        else:
            self.newDir = os.path.join(self.newDir, self.selectedSong.name)
            self.newDir = os.path.normpath(self.newDir)
            self.checkPathValidity()
        try:
            shutil.move(self.selectedSong.path, self.newDir)
        except OSError as e:
            print("Error sorting: " + self.selectedSong.path)
            print(e)
            pass



    def checkPathValidity(self):
        forbiddenCharacterList = [':', '*', '?', '"', '>', '<', '|']
        forbiddenNameList = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3',
        'COM4','COM5','COM6','COM7','COM8','COM9',
        'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6',
        'LPT7', 'LPT8', 'LPT9']
        for character in forbiddenCharacterList:
            self.newDir = self.newDir.replace(character, '')
        self.newDir = self.newDir.replace('\\x00', '')
        self.newDir = self.newDir.strip()
        name = os.path.basename(self.newDir)
        nameWithoutExt = os.path.splitext(name)[0]
        ext = os.path.splitext(name)[1]
        if name in forbiddenNameList:
            raise IllegalFileNameError('Illegal file name: ' + name)
        if nameWithoutExt.endswith('.'):
            name = nameWithoutExt[:len(nameWithoutExt) - 1] + ext
            name = name.strip()
            rootDir = os.path.split(self.newDir)[0].strip()
            self.newDir = os.path.join(rootDir, name)
        elif ext == '.':
            name = nameWithoutExt
            name = name.strip()
            rootDir = os.path.split(self.newDir)[0].strip()
            self.newDir = os.path.join(rootDir, name)



class IllegalFileNameError (Exception):
    pass
