from __future__ import unicode_literals
from time import sleep
from spotipy.oauth2 import SpotifyOAuth
from youtubesearchpython import VideosSearch
import os
from glob import glob
import spotipy
import shutil
import youtube_dl

USERPROFILE = os.getenv("USERPROFILE")
download_location = fr"{USERPROFILE}\\Downloads\\GetSpotify-Downloads\\"

class GetSpotify:
    def __init__(self, download_bitrate, download_location):
        self.bitrate = download_bitrate
        self.download_location = download_location

    def create_query(self, song_name, artist_list):
        query = song_name
        for artist_name in artist_list:
            query += ' ' + artist_name # first + goes between song end and artist name. second + replaces spaces in artist name

        return query


    def get_spotify_playlist_data(self, playlist_link):

        CLIENT_ID = "your-client-id"
        CLIENT_SECRET = "your-client-secret"
        REDIRECT_URI = "https://example.com/"
        scope = "playlist-modify-public"

        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI))
        result = sp.playlist(playlist_id=playlist_link, fields="name, id, tracks.items(track.artists(name), track.name)")
        search_data = result['tracks']['items']

        playlist_data = dict()
        for item in search_data:
            song_name = item['track']['name']
            artist_name = list()
            for artist in item['track']['artists']:
                artist_name.append(artist['name'])
            playlist_data.update({song_name: artist_name})

        return playlist_data

    # print(help(youtube_dl))
    def download_mp3_from_youtube(self, song_name, song_link):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': self.bitrate,
            }],
            'outtmpl': download_location + f'/{song_name}.mp3',
            'quiet': True,
            'no_warnings': True
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([song_link])

    def get_song_link(self, song_name, artist_list):
        preexisting_songs = [os.path.basename(f) for f in glob(fr"{self.download_location}\*.mp3")]
        if f"{song_name}.mp3" in preexisting_songs:
            return (True, None)
        else:
            search_result = VideosSearch(self.create_query(song_name, artist_list), limit=1)
            song_link = search_result.result()['result'][0]['link']
            return (False, song_link)


    def download(self, playlist_link):
        '''song_data should be a dict with song_name as key and list of artists as value
           ie: {'Baby': ['Justin Bieber', 'artist2'], 'Hate Me': ['Ellei Goulding', 'Juice Wrld']} this dict contains 2 song data'''

        playlist_data = self.get_spotify_playlist_data(playlist_link)

        for ind, (song_name, artist_list) in enumerate(playlist_data.items()):
            is_preexist, song_link = self.get_song_link(song_name, artist_list)

            # Printing Progress
            header = f"---------------------------------{ind+1} of {len(playlist_data)}--------------------------------"
            header_len = len(header)
            empty_line = (header_len-1)*' ' + '|\n'
            print(header)
            print(song_name + (header_len - len(song_name) - 1)*' ' + '|')

            if is_preexist:
                print((header_len - len("Already Downloaded|"))*' ' + "Already Downloaded|")
            else:
                try:
                    self.download_mp3_from_youtube(song_name, song_link)
                    print((header_len - len("Downloaded|"))*' ' + "Downloaded|")
                except (youtube_dl.utils.ExtractorError, youtube_dl.utils.DownloadError) as err:
                    print((header_len - len("Song Skipped|"))*' ' + "Song Skipped|")
            print(empty_line + empty_line, end='')

            if os.path.exists(f"{USERPROFILE}\.cache\youtube-dl"):
                shutil.rmtree(f"{USERPROFILE}\.cache\youtube-dl")
            sleep(1)



playlist_to_download = "https://open.spotify.com/playlist/40in8rjeVLr6NWYCZEqAp4?si=23bc45d16e464344"  # input("Enter spotify playlist link: ")
get_spotify = GetSpotify('256', download_location)
get_spotify.download(playlist_to_download)
