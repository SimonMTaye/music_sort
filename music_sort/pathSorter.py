import os
import shutil

import __main__
import errors

class PathSorter:

    def __init__(self, sortUsing: tuple, initialDir: str, useTrackTitle: bool):
        self.chosenAttributes = sortUsing
        self.initialDir = initialDir
        self.useTrackTitle = useTrackTitle
        self.verifySortingArguments(self.chosenAttributes)

    def sortSongs(self, songMetadataList):
        for songMetadata in songMetadataList:
            newDir = self.parseDir(songMetadata, self.chosenAttributes)
            self.createDir(newDir, songMetadata)
            self.moveSong(songMetadata.path, newDir)
            pass

    def verifySortingArguments(self, sortingAttributes):
        for attribute in sortingAttributes:
            if attribute not in __main__.PROPERTIES_TUPLE:
                raise ValueError(
                    "Argument chosen is incorrect or not supported")

    def parseDir(self, songMetadata, chosenAttributes):
        songDirectory = 'Sorted'
        for property in chosenAttributes:
            attributeValue = str(getattr(songMetadata, property))
            attributeValue = self.legalizePathName(attributeValue)
            songDirectory = os.path.join(songDirectory, attributeValue)
        songDirectory = os.path.normpath(songDirectory)
        songDirectory = os.path.join(self.initialDir, songDirectory)
        if(self.useTrackTitle):
            title = str(songMetadata.title)
            fileName = str(title + songMetadata.extension)
            fileName = self.legalizePathName(fileName)
            songDirectory = os.path.join(songDirectory, fileName)
            songDirectory = os.path.normpath(songDirectory)
        else:
            fileName = str(songMetadata.name)
            fileName = self.legalizePathName(fileName)
            songDirectory = os.path.join(songDirectory, fileName)
            songDirectory = os.path.normpath(songDirectory)
        return songDirectory        

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
            raise errors.IllegalFileNameError('Illegal file name: ' + pathName)
        if nameWithoutExt.endswith('.'):
            pathName = nameWithoutExt.strip('.') + ext
        elif ext == '.':
            pathName = nameWithoutExt
        pathName = str(pathName).strip()
        verifiedPath = pathName
        return verifiedPath

    def createDir(self, newDir, songMetadata):
        try:
            os.makedirs(newDir, exist_ok=True)
        except Exception as e:
            newDir = os.path.join(self.initialDir, 'Sorted', 'Unknown')
            os.makedirs(newDir, exist_ok=True)
            print("Error creating directory " + newDir)
            print(e)
            pass    

    def moveSong(self, songPath: str, newDir: str):
        try:
            shutil.move(songPath, newDir)
        except OSError as e:
            print("Error sorting: " + songPath)
            print(e)


