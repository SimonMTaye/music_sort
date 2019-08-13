import os
class fileScanner:

    def __init__(self, wantedFileTypes: list):
        self.wantedFileTypes = wantedFileTypes

    def scanFolder (self, dir: str):
        wantedFiles = []
        filesInDir = os.scandir(dir)
        for file in filesInDir:
            if(file.is_file and self.correctFileType(file.name)):
                wantedFiles.append(file.path)
        return wantedFiles        
    
    def scanFolderRecursively (self, dir: str):
        watnedFiles = []
        stuffInDir = os.scandir(dir)
        for thing in stuffInDir:
            if(thing.is_file and self.correctFileType(thing.name)):
                watnedFiles.append(thing.path)
            elif(thing.is_dir):
                self.scanFolderRecursively(thing.path)    
        return watnedFiles
                


    def correctFileType(self, fileName: str):
        for fileType in self.wantedFileTypes:
            if(fileName.endswith(fileType)):
                return True
        return False  