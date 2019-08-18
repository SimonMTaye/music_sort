import os

wantedFiles = []

def scanFolder (dir: str, wantedFileTypes: list):
    filesInDir = os.scandir(dir)
    for file in filesInDir:
        if(file.is_file and correctFileType(file.name, wantedFileTypes)):
            wantedFiles.append(file.path)
    return wantedFiles        

def scanFolderRecursively (dir: str, wantedFileTypes: list):
    stuffInDir = os.scandir(dir)
    for thing in stuffInDir:
        if(thing.is_file and correctFileType(thing.name, wantedFileTypes)):
            wantedFiles.append(thing.path)
        elif(thing.is_dir):
            scanFolderRecursively(thing.path, wantedFileTypes)    
    return wantedFiles             


def correctFileType(fileName: str, wantedFileTypes: list):
    for fileType in wantedFileTypes:
        if(fileName.endswith(fileType)):
            return True
    return False  