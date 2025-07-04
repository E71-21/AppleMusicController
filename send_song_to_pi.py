import subprocess


def get_song_data(data):
    result = {}
    i = 0
    n = len(data)

    while i < n:
        # Skip any spaces
        while i < n and data[i] == ' ':
            i += 1

        # Extract key
        key_start = i
        while i < n and data[i] != '=':
            i += 1
        key = data[key_start:i].strip()

        if i < n and data[i] == '=':
            i += 1  # skip '='

        # Expect opening quote
        if i < n and data[i] == '"':
            i += 1  # skip opening quote
            value_start = i
            # Look for closing quote
            while i < n and data[i] != '"':
                i += 1
            value = data[value_start:i]
            i += 1  # skip closing quote

            result[key] = value

    return result


now_playing_result = subprocess.run(
    ['osascript', 'now_playing.applescript'],
    capture_output=True,
    text=True
)

if __name__ == "__main__":
    if not now_playing_result.stdout == "" and now_playing_result.stderr == "":
        print(now_playing_result.stdout)
    else:
        print(now_playing_result.stderr)
    song_data = get_song_data(now_playing_result.stdout)
    print(song_data)