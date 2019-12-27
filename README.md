# music_sort
Look through a directory for audio files and sort them using the specified properties (eg. /exampleArtist/exampleAlbum/exaplmeTrack.mp3) 

## Usage

*python music_sort (dir) [-argument]

Arguments
  + *dir* (**str**)   -   The root directory to be scanned for audio files
  + *recursive* (**bool**)  -   Determines if the root directory should be recursively scanned (default = **True**)
  + *sortingProperties* (**tuple**) - Determines which properties (from arist, genre, album, bitrate, albumartist, year) are used to create directories for each audio file (default = ['artist', 'album'] )
  + *useTrackTile* (**bool**) -  Determines whether file should be renamed to the track title or keep original file name (default = **False**)
  + *musicFileTypes* (**list**) - Audio file extensions to search for (default = ['mp3', 'm4a', 'flac'] )
  + *checkForDuplicates* (**bool**) - Check for duplicate songs using fuzzy string comparison of track titles and artist (default = **True** )
    * Could consume time on large amount of music files. Is CPU intensive
  
## Dependencies
  + *fuzzywuzzy* - used for fuzzy string matching
  + *Python Fire* - used for the CLI
  + *tinytag* - parse music file metadata
 
