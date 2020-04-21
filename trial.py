import sys
import requests
import spotipy
import spotipy.util as util
import json
import random
from time import gmtime, strftime


username = '1167152572'
scope = 'playlist-modify-public'
token = util.prompt_for_user_token(username, scope)


sp = spotipy.Spotify(auth=token)


#define_language = sp.featured_playlists(
#    locale=['es_ES'],
#    country=['ES'],
#    limit=[1],
#    offset=[40]
#)


#recommendation_genre_seeds()
#target_instrumentalness=[0.95], #if want instrumental
#max_speechiness=[0.03], #if want instrumental

#optional - make a loop to repeat this process and try to get more random tracks? Offset somehow?

date = strftime("%d of %B", gmtime())
genre_choice = input ('Which kind of music would you like to listen to?')
speediness = input ('Do you feel energetic, slow or mixed today?')

if speediness == 'energetic':
    tempo = 190
    valence = 1.0
    energy = 1.0
elif speediness == 'slow':
    tempo = 70
    valence = 0.05
    energy = 0.05
else:
    tempo = random.randint(100,200)
    valence = random.uniform(0.5,1.0)
    energy = random.uniform(0.5,1.0)


find_songs = sp.recommendations(
    seed_genres= [genre_choice],
    limit=[20],
    target_danceability=[0.8],
    target_valence=[valence],
    target_energy=[energy],
    target_tempo = [tempo],
    max_popularity = [20]
    )


track_ids = []
for i, j in enumerate(find_songs['tracks']):
    track_ids.append(j['id'])
    print('{})\"{}\" by \"{}\"'.format(i + 1, j['name'], j['artists'][0]['name']))


playlist_name = 'Your {} {} {} playlist!'.format(date,speediness,genre_choice)

playlist = sp.user_playlist_create(username, playlist_name, public=True, description='Enjoy your day!')
add_songs = sp.user_playlist_add_tracks(username, playlist['id'], track_ids, position=None)

audio_f = sp.audio_features(track_ids)
print(audio_f)

url = playlist['external_urls']['spotify']

print('Your playlist is ready at {}'.format(url))