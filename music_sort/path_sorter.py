import os
import shutil

from . import errors


class PathSorter:
    def __init__(self, sorting_properties: tuple, root_dir: str, keep_file_name: bool):
        self.sorting_properties = sorting_properties
        self.root_dir = root_dir
        self.keep_file_name = keep_file_name

    def move_songs(self, filtered_songs, duplicate_songs):
        for filtered_songs in filtered_songs:
            dir_properties = self.parse_dir(filtered_songs)
            destination_dir = os.path.join(self.root_dir, "Sorted", dir_properties["dir"])
            destination_file = os.path.join(destination_dir, dir_properties["name"])
            try:
                os.makedirs(destination_dir, exist_ok=True)
                shutil.move(filtered_songs.path, destination_file)
            except (OSError, ValueError) as e:
                print(r"Error moving: %s" %filtered_songs.path)
                print(e)
        for duplicate_songs in duplicate_songs:
            dir_properties = self.parse_dir(duplicate_songs)
            destination_dir = os.path.join(self.root_dir, "Duplicates", dir_properties["dir"])
            destination_file = os.path.join(destination_dir, dir_properties["name"])
            try:
                os.makedirs(destination_dir, exist_ok=True)
                shutil.copy2(duplicate_songs.path, destination_file)
                os.remove(duplicate_songs.path)
            except Exception as e:
                print("Error handling: " + duplicate_songs.path)
                print(e)

    def parse_dir(self, song_metadata):
        song_directory = ""
        for property in self.sorting_properties:
            attribute_value = str(getattr(song_metadata, property))
            attribute_value = self.legalize_path(attribute_value)
            song_directory = os.path.join(song_directory, attribute_value)
        song_directory = os.path.normpath(song_directory)
        if self.keep_file_name:
            title = str(song_metadata.title)
            file_name = str(title + song_metadata.extension)
        else:
            file_name = str(song_metadata.name)
        file_name = self.legalize_path(file_name)
        return {"dir": song_directory, "name": file_name}

    def legalize_path(self, path_name: str):
        forbiddenCharacterList = [":", "*", "?", '"', ">", "<", "|", "/"]
        forbiddenNameList = [
            "CON",
            "PRN",
            "AUX",
            "NUL",
            "COM1",
            "COM2",
            "COM3",
            "COM4",
            "COM5",
            "COM6",
            "COM7",
            "COM8",
            "COM9",
            "LPT1",
            "LPT2",
            "LPT3",
            "LPT4",
            "LPT5",
            "LPT6",
            "LPT7",
            "LPT8",
            "LPT9",
        ]
        for character in forbiddenCharacterList:
            path_name = path_name.replace(character, "")
        name_without_ext = os.path.splitext(path_name)[0]
        ext = os.path.splitext(path_name)[1]
        if name_without_ext in forbiddenNameList:
            raise errors.IllegalFileNameError()
        if name_without_ext.endswith("."):
            path_name = name_without_ext.strip(".") + ext
        elif ext == ".":
            path_name = name_without_ext
        path_name = str(path_name).strip()
        return path_name

    def move_song(self, song_path: str, newDir: str):
        try:
            shutil.move(song_path, newDir)
        except OSError as e:
            print("Error moving: " + song_path)
            print(e)
