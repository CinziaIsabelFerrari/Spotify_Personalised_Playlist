import sys
import requests
import spotipy
import spotipy.util as util
import json
import random
from time import gmtime, strftime



username = '1167152572'
scope = 'user-library-read user-top-read playlist-modify-public user-follow-read'
token = util.prompt_for_user_token(username, scope)

sp = spotipy.Spotify(auth=token)

#Here I am getting my top artists and creating playlists based on how I feel on the day.
#A new option could be getting my top songs and creating the same with seed, or using seed with my top artists to get similar stuff.

#TOO MANY OPTIONS TO CHOOSE FROM

#Maybe I can get my top 10 artists of the last 4 weeks or 6 months and with seed making a new playlist

#Maybe I can get random artist to put on seed + random track to put on seed and create a playlist

#Finding my top artists 100

#short term range means 4 weeks, medium is 6 months and long-term is of all time

def my_top_artists(sp):
    print('Give me a second..')
    top_artists_name = []
    top_artists_uri = []

    ranges = ['short_term', 'medium_term'] #(you can add also long_term)
    for r in ranges:
        all_top_artists = sp.current_user_top_artists(limit=100, time_range= r)
        top_artists_data = all_top_artists['items']
        for artist_data in top_artists_data:
            if artist_data['name'] not in top_artists_name:
                top_artists_name.append(artist_data['name'])
                top_artists_uri.append(artist_data['uri'])

    return top_artists_uri

#Now we are finding these artists top 10 songs

def my_top_artists_top_10songs(sp, top_artists_uri):
    print('..I\'m looking into your songs')
    top_10tracks_uri = []
    for artist in top_artists_uri:
        top_tracks_all = sp.artist_top_tracks(artist)
        top_tracks = top_tracks_all['tracks']
        for track_data in top_tracks:
            top_10tracks_uri.append(track_data['uri'])
    return top_10tracks_uri


#Now from these top tracks, we select the ones we want based on the mood


def choose_tracks(sp, top_10tracks_uri):
    mood = input('I\'m ready! How do you feel today? Sloth, Quokka, Cheetaah or just curious?')
    print('Okay! Picking your tracks...')
    selected_tracks_uri = []
    selected_tracks_name = []

    random.shuffle(top_10tracks_uri)

    for tracks in list(top_10tracks_uri): #group(top_10tracks_uri,50) check this
        selected_tracks_data = sp.audio_features(tracks)
        for track_data in selected_tracks_data:
            try:
                if mood == 'sloth':
                    if  (0 <= track_data['valence'] <= 0.2
                    and track_data['danceability'] <= 0.2
                    and track_data['energy'] <= 0.2
                    and track_data['tempo'] <= 70):
                        selected_tracks_uri.append(track_data['uri'])
                        selected_tracks_name.append(track_data['tracks'])
                elif mood == 'quokka':
                    if  (0.4 <= track_data['valence'] <= 0.6
                    and 0.4 <= track_data['danceability'] <= 0.6
                    and 0.4 <= track_data['energy'] <= 0.6
                    and 100<= track_data['tempo'] <= 150):
                        selected_tracks_uri.append(track_data['uri'])
                        selected_tracks_name.append(track_data['tracks'])
                elif mood == 'cheetaah':
                    if (0.9 <= track_data['valence'] <= 1
                    and track_data['danceability'] >= 0.9
                    and track_data['energy'] >= 0.9
                    and track_data['tempo'] >= 170):
                        selected_tracks_uri.append(track_data['uri'])
                        selected_tracks_name.append(track_data['tracks'])
                else:
                    if  (track_data['tempo'] == random.randint(100, 200)
                    and track_data['valence'] == random.uniform(0.2, 1.0)
                    and track_data['energy'] == random.uniform(0.2, 1.0)
                    and track_data['danceability'] == random.uniform(0.2, 1.0)):
                        selected_tracks_uri.append(track_data['uri'])
                        selected_tracks_name.append(track_data['tracks'])
            except TypeError as te:
                continue
    return selected_tracks_uri
    return selected_tracks_name

#def create_playlist(sp, selected_tracks_uri):
#    playlist_name = 'Today\'s mood'
#
#    playlist_new = sp.user_playlist_create(username, playlist_name, public=True)
#    playlist_id = playlist_new['id']
#
#    random.shuffle(selected_tracks_uri)
#    sp.user_playlist_add_tracks(username, playlist_id, selected_tracks_uri[1:20])
#
#   return playlist_new['external_urls']['spotify']






top_artists_uri = my_top_artists(sp)

top_10tracks_uri = my_top_artists_top_10songs(sp, top_artists_uri)

selected_tracks_uri = choose_tracks(sp, top_10tracks_uri)

playlist_name = 'Today\'s mood!'

playlist_new = sp.user_playlist_create(username, playlist_name, public=True, description='Enjoy!')
add_songs = sp.user_playlist_add_tracks(username, playlist_new['id'], selected_tracks_uri, position=None)

url = playlist_new['external_urls']['spotify']

print('Your playlist is ready at {}'.format(url))