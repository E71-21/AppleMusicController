from flask import Flask, jsonify, send_from_directory
import subprocess
import json

app = Flask(__name__)


def get_song_data(data_bytes):
    # 1. Decode bytes to string
    data = data_bytes.decode('utf-8').strip()

    result = {}
    i = 0
    n = len(data)

    while i < n:
        # Skip spaces
        while i < n and data[i] == ' ':
            i += 1

        # Extract key
        key_start = i
        while i < n and data[i] != '=' and data[i] != ' ':
            i += 1
        key = data[key_start:i].strip()

        # Skip spaces before '='
        while i < n and data[i] == ' ':
            i += 1

        if i < n and data[i] == '=':
            i += 1

        # Skip spaces after '='
        while i < n and data[i] == ' ':
            i += 1

        # Expect opening quote
        if i < n and data[i] == '"':
            i += 1
            value_start = i
            while i < n and data[i] != '"':
                if data[i] == '\\' and i + 1 < n:
                    i += 2  # skip escaped character
                else:
                    i += 1
            value = data[value_start:i].replace('\\"', '"')
            i += 1  # skip closing quote

            result[key] = value

    return json.dumps(result)

def run_script(filename):
    """Runs AppleScript in this folder and returns stdout."""
    result = subprocess.run(
        ['osascript', str("Mac/Apple Scripts/"+filename)],
        capture_output=True
    )
    return result.stdout

@app.route('/nowplaying')
def now_playing():
    # Assumes your get_now_playing.applescript returns a dict-like string
    output = run_script('now_playing.applescript')
    formatted_output = get_song_data(output)
    return jsonify(eval(formatted_output))  # Or parse to JSON if needed

@app.route('/playpause')
def playpause():
    run_script('play_pause.applescript')
    return "OK"

@app.route('/next')
def next_track():
    run_script('next_track.applescript')
    return "OK"

@app.route('/previous')
def previous_track():
    run_script('previous_track.applescript')
    return "OK"

@app.route('/artwork')
def get_artwork():
    subprocess.run(
        ['osascript', 'Mac/Apple Scripts/song_artwork.applescript']
    )
    return send_from_directory("Song Art", "CurrentSongArtwork.jpg")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)