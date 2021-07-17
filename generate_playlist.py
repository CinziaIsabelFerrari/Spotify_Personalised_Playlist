"""
Moooody Spotify Playlist generator

Created by: Cinzia Ferrari
"""

import random
import spotipy

from spotipy.oauth2 import SpotifyOAuth
from utils import *

if __name__ == "__main__":
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE))

    # Finding my top artists 100 and their top 10 songs:
    print("Wait a minute, I'm looking into your top artists..")
    top_artists_uri_c = get_top_artists(sp)

    # Get top tracks and shuffle
    print("..getting their top tracks..")
    top_10tracks_uri_c = get_top_10songs_from_top_artists(sp, top_artists_uri_c)
    random.shuffle(top_10tracks_uri_c)

    # Get 2 random tracks to use as seeds
    random_seed_tracks = random.sample(top_10tracks_uri_c, 2)

    # Now based on the mood I will select specific parameters for the tracks of my new playlist
    track_ids = []
    mood = input('I\'m ready! How do you feel today? Sloth, Quokka, Cheetah or curious?')
    print('Okay! Picking your tracks...')

    if mood.lower() == 'sloth':
        val_min, val_max = 0, 0.3
        ene_min, ene_max = 0, 0.3
        tem_target = 100

    elif mood.lower() == 'quokka':
        val_min, val_max = 0.4, 0.7
        ene_min, ene_max = 0.4, 0.6
        tem_target = 140

    elif mood.lower() == 'cheetah':
        val_min, val_max = 0.7, 1.0
        ene_min, ene_max = 0.7, 1.0
        tem_target = 180

    else:
        val_min, val_max = 0, 1.0
        ene_min, ene_max = 0, 1.0
        tem_target = None

    find_new_songs = sp.recommendations(
        seed_tracks=random_seed_tracks,
        limit=[20],
        min_valence=val_min,
        max_valence=val_max,
        min_energy=ene_min,
        max_energy=ene_max,
        target_tempo=tem_target,
    )

    # Prints the selected songs
    for i, j in enumerate(find_new_songs['tracks']):
        track_ids.append(j['id'])
        print('{})\"{}\" by \"{}\"'.format(i + 1, j['name'], j['artists'][0]['name']))

    if isfile(PLAYLIST_FILE_PATH):
        # Updating existing playlist
        playlist_id, playlist_url = read_playlist_file()
        add_songs = sp.playlist_replace_items(playlist_id, track_ids)
    else:
        # Creating new playlist
        playlist_name = 'Embrace your mood and dance with it!'
        playlist = sp.user_playlist_create(sp.me()['id'], playlist_name, public=True)
        playlist_id, playlist_url = playlist['id'], playlist['external_urls']['spotify']

        add_songs = sp.playlist_add_items(playlist_id, track_ids)
        create_playlist_file(playlist_id, playlist_url)

    print('You''ve created a playlist with {} brand new song. Enjoy it!'.format(len(track_ids)))
    print('Your playlist is ready at {}'.format(playlist_url))
