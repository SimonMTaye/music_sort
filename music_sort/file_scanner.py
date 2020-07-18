import os

def scan_folder(dir: str, wantedFileTypes: list, recursive: bool, *, files=[]):
    files_in_dir = os.scandir(dir)
    for file in files_in_dir:
        if file.is_file() and correct_file_type(file.name, wantedFileTypes):
            files.append(file.path)
        elif file.is_dir() and recursive and file.name != "Duplicates" and file.name != "Sorted":
            scan_folder(file.path, wantedFileTypes, recursive, files=files)
    return files


def correct_file_type(fileName: str, wantedFileTypes: list):
    for fileType in wantedFileTypes:
        if fileName.endswith(fileType):
            return True
    return False
