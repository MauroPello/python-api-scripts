import subprocess
import psutil
import spotipy
import os
from secret import *
from spotipy.oauth2 import SpotifyOAuth


def check_running_process(process_name):
    # Check if there is any running process that contains the given name processName.
    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if process_name.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


# opens spotify if not already open
# sets up the spotify API
def spotify_api_setup():
    global spotify
    os.environ["SPOTIPY_CLIENT_ID"] = SPOTIPY_CLIENT_ID
    os.environ["SPOTIPY_CLIENT_SECRET"] = SPOTIPY_CLIENT_SECRET
    os.environ["SPOTIPY_REDIRECT_URI"] = SPOTIPY_REDIRECT_URI
    spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(username=SPOTIPY_USERNAME,
                                                        scope="streaming user-modify-playback-state playlist-read-private"))


# checks if I already have a playlist for that artist
# search through: https://developer.spotify.com/console/get-current-user-playlists
# gets URI of saved playlist with desired artist
def check_playlist(artist):
    playlists = spotify.current_user_playlists(limit=50)
    for playlist in enumerate(playlists['items']):
        if playlist[1]['name'].__contains__(artist):
            return playlist[1]['uri']
    return None


# plays my playlist for that artist randomly
def play_my_playlist(playlist_uri):
    spotify.start_playback(context_uri=playlist_uri)
    spotify.shuffle(True)


# plays randomly the default playlist "This Is *Artist*"
# get URI of "This Is *Artist*" playlist: https://developer.spotify.com/console/get-search-item
# play playlist
def play_this_is_playlist(artist):
    this_is_playlist = spotify.search(q='This Is ' + artist, type='playlist', limit=1)
    spotify.start_playback(context_uri=this_is_playlist['playlists']['items'][0]['uri'])
    spotify.shuffle(True)


if __name__ == '__main__':
    # input desired artist
    # if not len(sys.argv) == 1:
    #     sys.exit()
    # artist = sys.argv[1]
    artist = input("Enter Desired Artist: ")
    spotify_api_setup()
    playlist_uri = check_playlist(artist)
    if playlist_uri is not None:
        play_my_playlist(playlist_uri)
    else:
        play_this_is_playlist(artist)
    if not check_running_process('spotify'):
        subprocess.call('spotify')
