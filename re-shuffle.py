import sys
import requests
import spotipy
import spotipy.util as util
import json
import random
from time import gmtime, strftime
# from re import group


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

    ranges = ['short_term', 'medium_term','long_term'] #(you can add also long_term)
    for r in ranges:
        all_top_artists = sp.current_user_top_artists(limit=150, time_range= r)
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



top_artists_uri = my_top_artists(sp)

top_10tracks_uri = my_top_artists_top_10songs(sp, top_artists_uri)

#Now from these top tracks, we select the ones we want based on the mood


#def choose_tracks(sp, top_10tracks_uri):

mood = input('I\'m ready! How do you feel today? Sloth, Quokka, Cheetah or just curious?')
print('Okay! Picking your tracks...')

selected_tracks_uri = []

random.shuffle(top_10tracks_uri)

if mood.lower() not in ['sloth', 'quokka', 'cheetah']:
    tracks_subset = random.sample(top_10tracks_uri, 100)
    for tracks in tracks_subset:
        track_data = sp.audio_features(tracks)[0]
        selected_tracks_uri.append(track_data['uri'])

else:

    if mood.lower() == 'sloth':
        val_min, val_max = 0, 0.3
        ene_min, ene_max = 0, 0.3
        tem_min, tem_max = 0, 140
        tem_target = 100

    elif mood.lower() == 'quokka':
        val_min, val_max = 0.4, 0.7
        ene_min, ene_max = 0.4, 0.6
        tem_min, tem_max = 110, 170
        tem_target = 140

    elif mood.lower() == 'cheetah':
        val_min, val_max = 0.7, 1.0
        ene_min, ene_max = 0.7, 1.0
        tem_min, tem_max = 160, 230
        tem_target = 180

    for tracks in top_10tracks_uri: #group(top_10tracks_uri,50) check this
        track_data = sp.audio_features(tracks)[0]

        if (val_min <= track_data['valence'] <= val_max
            and ene_min <= track_data['energy'] <= ene_max
            and tem_min <= track_data['tempo'] <= tem_max):
            selected_tracks_uri.append(track_data['uri'])



        # if mood.lower() == 'sloth':
        #     if (0 <= track_data['valence'] <= 0.3
        #             # and track_data['danceability'] <= 0.2
        #             and track_data['energy'] <= 0.3
        #             and track_data['tempo'] <= 140):
        #         selected_tracks_uri.append(track_data['uri'])
        # elif mood.lower() == 'quokka':
        #     if (0.4 <= track_data['valence'] <= 0.7
        #             # and 0.4 <= track_data['danceability'] <= 0.6
        #             and 0.4 <= track_data['energy'] <= 0.6
        #             and 100 <= track_data['tempo'] <= 170):
        #         selected_tracks_uri.append(track_data['uri'])
        # elif mood.lower() == 'cheetah':
        #     if (0.7 <= track_data['valence'] <= 1
        #             # and track_data['danceability'] >= 0.
        #             and track_data['energy'] >= 0.7
        #             and track_data['tempo'] >= 140):
        #         selected_tracks_uri.append(track_data['uri'])

print('I found {} tracks out of {} for you!'.format(len(selected_tracks_uri), len(top_10tracks_uri)))

random_seeds_tracks = random.sample(selected_tracks_uri, 2)

find_new_songs = sp.recommendations(
    seed_tracks= random_seeds_tracks,
    limit=[20],
    #target_danceability=[0.8],
    min_valence=val_min,
    max_valence=val_max,
    #target_energy=[energy],
    target_tempo = tem_target,
    # max_popularity = [20]
    )

track_ids = []
for i, j in enumerate(find_new_songs['tracks']):
    track_ids.append(j['id'])
    print('{})\"{}\" by \"{}\"'.format(i + 1, j['name'], j['artists'][0]['name']))

audio_f = sp.audio_features(track_ids)
print(audio_f)

# for i, j in enumerate(selected_tracks_name):
#     print('{})\"{}\" by \"{}\"'.format(i + 1, j['name'], j['artists'][0]['name']))
#     #return selected_tracks_uri

#def create_playlist(sp, selected_tracks_uri):
#    playlist_name = 'Today\'s mood'
#
#    playlist_new = sp.user_playlist_create(username, playlist_name, public=True)
#    playlist_id = playlist_new['id']
#
#    random.shuffle(selected_tracks_uri)
#    sp.user_playlist_add_tracks(username, playlist_id, selected_tracks_uri[1:20])



#selected_tracks_uri = choose_tracks(sp, top_10tracks_uri)


playlist_name = 'Today\'s mood!'

playlist_new = sp.user_playlist_create(username, playlist_name, public=True, description='Enjoy!')

print(selected_tracks_uri)

add_songs = sp.user_playlist_add_tracks(username, playlist_new['id'], track_ids)

url = playlist_new['external_urls']['spotify']

print('Your playlist is ready at {}'.format(url))