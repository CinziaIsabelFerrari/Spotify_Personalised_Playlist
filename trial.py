import spotipy
import spotipy.util as util
from time import gmtime, strftime


username = '1167152572'
scope = 'playlist-modify-public'
token = util.prompt_for_user_token(username, scope)


sp = spotipy.Spotify(auth=token)

date = strftime("%d of %B", gmtime())
genre_choice = input ('Which kind of music would you like to listen to?')
speediness = input ('Do you feel energetic, slow or mixed today?')

if speediness.lower() not in ['energetic', 'slow']:
    val_min, val_max = 0, 1.0
    ene_min, ene_max = 0, 1.0
    tem_target = None

else:

    if speediness.lower() == 'slow':
        val_min, val_max = 0, 0.3
        ene_min, ene_max = 0, 0.3
        tem_target = 100

    elif speediness.lower() == 'energetic':
        val_min, val_max = 0.5, 0.8
        ene_min, ene_max = 0.5, 0.8
        tem_target = 150



find_songs = sp.recommendations(
    seed_genres= [genre_choice],
    limit=[20],
    min_valence=val_min,
    max_valence=val_max,
    min_energy=ene_min,
    max_energy=ene_max,
    target_tempo = tem_target,
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