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



#Finding my top artists 100

#short term range means 4 weeks, medium is 6 months and long-term is of all time

def my_top_artists(sp):
    print('..finding top artist')
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
    print('..getting their top tracks')
    top_10tracks_uri = []
    for artist in top_artists_uri:
        top_tracks_all = sp.artist_top_tracks(artist)
        top_tracks = top_tracks_all['tracks']
        for track_data in top_tracks:
            top_10tracks_uri.append(track_data['uri'])
    return top_10tracks_uri


