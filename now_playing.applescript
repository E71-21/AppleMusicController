if application "Music" is running then
	tell application "Music"
		if player state is playing then
			set trackName to name of current track
			set artistName to artist of current track
			set albumName to album of current track
			set playlistName to name of current playlist
			return "title=\"" & trackName & "\" artist=\"" & artistName & "\" album=\"" & albumName & "\" playlist=\"" & playlistName & "\""
		else if player state is paused then
			set trackName to name of current track
			set artistName to artist of current track
			set albumName to album of current track
			set playlistName to name of current playlist
			return "title=\"" & trackName & "\" artist=\"" & artistName & "\" album=\"" & albumName & "\" playlist=\"" & playlistName & "\""
		else if player state is stopped then
			return "No Music Playing"
		end if
	end tell
else
	return "No Music Playing"
end if