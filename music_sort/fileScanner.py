import os

wantedFiles = []


def scanFolder(dir: str, wantedFileTypes: list):
    filesInDir = os.scandir(dir)
    for file in filesInDir:
        if(file.is_file and correctFileType(file.name, wantedFileTypes)):
            wantedFiles.append(file.path)
    return wantedFiles


def scanFolderRecursively(dir: str, wantedFileTypes: list):
    try:
        stuffInDir = os.scandir(dir)
    except (FileNotFoundError, NotADirectoryError) as e:
        stuffInDir = []
        print(e)
        pass
    for thing in stuffInDir:
        if(thing.is_file and correctFileType(thing.name, wantedFileTypes)):
            wantedFiles.append(thing.path)
        elif(thing.is_dir and thing.name != 'duplicates' and thing.name != 'Sorted'):
            scanFolderRecursively(thing.path, wantedFileTypes)
    return wantedFiles


def correctFileType(fileName: str, wantedFileTypes: list):
    for fileType in wantedFileTypes:
        if(fileName.endswith(fileType)):
            return True
    return False
