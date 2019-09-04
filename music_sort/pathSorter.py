import os
import shutil


class pathSorter:

    def __init__(self, sortUsing: tuple, songMetadata, initialDir, useTrackTitle):
        self.chosenAttributes = sortUsing
        for attribute in self.chosenAttributes:
            if(attribute not in ['album', 'artist', 'genre', 'bitrate', 'albumartist']):
                raise ValueError(
                    "Argument chosen is incorrect or not supported")
        self.selectedSong = songMetadata
        self.newDir = 'Sorted'
        for property in self.chosenAttributes:
            attributeValue = str(getattr(self.selectedSong, property))
            attributeValue = self.legalizePathName(attributeValue)
            self.newDir = os.path.join(self.newDir, attributeValue)
        self.newDir = os.path.normpath(self.newDir)
        self.newDir = os.path.join(initialDir, self.newDir)
        try:
            os.makedirs(self.newDir, exist_ok=True)
        except Exception as e:
            self.newDir = os.path.join(initialDir, 'Sorted', 'Unknown')
            os.makedirs(self.newDir, exist_ok=True)
            print("Error creating directory for: " + self.selectedSong.path)
            print(e)
            pass
        if(useTrackTitle):
            title = str(self.selectedSong.title)
            fileName = str(title + self.selectedSong.extension)
            fileName = self.legalizePathName(fileName)
            self.newDir = os.path.join(self.newDir, title)
            self.newDir = os.path.normpath(self.newDir)
        else:
            fileName = str(self.selectedSong.name)
            fileName = self.legalizePathName(fileName)
            self.newDir = os.path.join(self.newDir, fileName)
            self.newDir = os.path.normpath(self.newDir)
        try:
            shutil.move(self.selectedSong.path, self.newDir)
        except OSError as e:
            print("Error sorting: " + self.selectedSong.path)
            print(e)
            pass

    def legalizePathName(self, pathName: str):
        forbiddenCharacterList = [':', '*', '?', '"', '>', '<', '|', '/']
        forbiddenNameList = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3',
                             'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
                             'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6',
                             'LPT7', 'LPT8', 'LPT9']
        for character in forbiddenCharacterList:
            pathName = pathName.replace(character, '')
        pathName = str(pathName).strip('\x00')
        nameWithoutExt = os.path.splitext(pathName)[0]
        ext = os.path.splitext(pathName)[1]
        if nameWithoutExt in forbiddenNameList:
            raise IllegalFileNameError('Illegal file name: ' + pathName)
        if nameWithoutExt.endswith('.'):
            pathName = nameWithoutExt.strip('.') + ext
        elif ext == '.':
            pathName = nameWithoutExt
        pathName = str(pathName).strip()
        verifiedPath = pathName
        return verifiedPath


class IllegalFileNameError (Exception):
    pass
