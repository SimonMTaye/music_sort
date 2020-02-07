import os
import shutil

from . import __main__
from . import errors

class PathSorter:

    def __init__(self, sortUsing: tuple, initialDir: str, useTrackTitle: bool):
        self.chosenAttributes = sortUsing
        self.initialDir = initialDir
        self.useTrackTitle = useTrackTitle

    def moveSongs(self, filteredSongList, duplicateSongList):
        self.verifySortingArguments(self.chosenAttributes)
        for i, filteredSongMetadata in enumerate(filteredSongList):
            print('Moving song ' + str(i + 1) + ' of ' + str(len(filteredSongList)), end='\r')
            customDir = self.parseCustomDir(filteredSongMetadata)
            targetDir = customDir['targetDir']
            fileName = customDir['fileName']
            destinationDir = os.path.join(self.initialDir, 'Sorted', targetDir)
            destinationFilePath = os.path.join(destinationDir, fileName)
            try:
                os.makedirs(destinationDir, exist_ok=True)
                shutil.move(filteredSongMetadata.path, destinationFilePath)
            except OSError as e:
                print("Error moving: " + filteredSongMetadata.path)
                print(e)
        for j, duplicateSongMetadata in enumerate(duplicateSongList):
            print('Moving duplicate song ' + str(j + 1) + ' of ' + str(len(duplicateSongList)), end='\r')
            customDir = self.parseCustomDir(duplicateSongMetadata)
            targetDir = customDir['targetDir']
            fileName = customDir['fileName']
            destinationDir = os.path.join(self.initialDir, 'Duplicates', targetDir)
            destinationFilePath = os.path.join(destinationDir, fileName)
            try:
                os.makedirs(destinationDir, exist_ok=True)
                shutil.copy2(duplicateSongMetadata.path, destinationFilePath)
                os.remove(duplicateSongMetadata.path)
            except Exception as e:
                print('Error handling: ' + duplicateSongMetadata.path)
                print(e)

    def verifySortingArguments(self, sortingAttributes):
        for attribute in sortingAttributes:
            if attribute not in __main__.PROPERTIES_TUPLE:
                raise ValueError(
                    "Argument chosen is incorrect or not supported")

    def parseCustomDir(self, songMetadata):
        songDirectory = ''
        for property in self.chosenAttributes:
            attributeValue = str(getattr(songMetadata, property))
            attributeValue = self.legalizePathName(attributeValue)
            songDirectory = os.path.join(songDirectory, attributeValue)
        songDirectory = os.path.normpath(songDirectory)
        if(self.useTrackTitle):
            title = str(songMetadata.title)
            fileName = str(title + songMetadata.extension)
            fileName = self.legalizePathName(fileName)
        else:
            fileName = str(songMetadata.name)
            fileName = self.legalizePathName(fileName)
        return {'targetDir': songDirectory , 'fileName': fileName}

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
            raise errors.IllegalFileNameError()
        if nameWithoutExt.endswith('.'):
            pathName = nameWithoutExt.strip('.') + ext
        elif ext == '.':
            pathName = nameWithoutExt
        pathName = str(pathName).strip()
        verifiedPath = pathName
        return verifiedPath

    def moveSong(self, songPath: str, newDir: str):
        try:
            shutil.move(songPath, newDir)
        except OSError as e:
            print("Error moving: " + songPath)
            print(e)


