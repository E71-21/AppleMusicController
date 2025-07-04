tell application "Music"
    if player state is playing or player state is paused then
        set currentTrack to current track
        set artworkList to artworks of currentTrack
        if artworkList is not {} then
            set art to item 1 of artworkList
            set artData to data of art
            
            -- Build the file path inside Documents/Github/AppleMusicController
            set baseFolder to (path to documents folder as text)
            set folderPath to baseFolder & "Github:AppleMusicController:"
            set filePath to folderPath & "CurrentSongArtwork.jpg"
            
            -- Save the artwork
            set outFile to open for access file filePath with write permission
            try
                set eof outFile to 0
                write artData to outFile
            end try
            close access outFile
        end if
    end if
end tell