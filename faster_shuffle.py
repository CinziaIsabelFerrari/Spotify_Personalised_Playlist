import spotipy
import spotipy.util as util
import random


username = '1167152572'
scope = 'user-library-read user-top-read playlist-modify-public user-follow-read playlist-read-private playlist-modify-private'
playlist_id = '1o4dtzeLcupqgKpjqLZyvm'
playlist_url = 'https://open.spotify.com/playlist/1o4dtzeLcupqgKpjqLZyvm'

token = util.prompt_for_user_token(username, scope)

sp = spotipy.Spotify(auth=token)



#Finding my top artists 100

#short term range means 4 weeks, medium is 6 months and long-term is of all time

def my_top_artists(sp):
    print('Give me a second..')
    top_artists_name = []
    top_artists_uri = []

    ranges = ['short_term', 'medium_term','long_term']
    for r in ranges:
        all_top_artists = sp.current_user_top_artists(limit=150, time_range= r)
        top_artists_data = all_top_artists['items']
        for artist_data in top_artists_data:
            if artist_data['name'] not in top_artists_name:
                top_artists_name.append(artist_data['name'])
                top_artists_uri.append(artist_data['uri'])

    return top_artists_uri


#Now I'm getting the top 10 songs

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

# Maybe I can also add these --> current_user_recently_played(limit=50, after=None, before=None)

#Now from these top tracks, I get some random to use as seed

random.shuffle(top_10tracks_uri)

random_seeds_tracks = random.sample(top_10tracks_uri, 5)

#Using these as seed I will get a playlist based on the mood

track_ids = []

mood = input('I\'m ready! How do you feel today? Sloth, Quokka, Cheetah or just curious?')
print('Okay! Picking your tracks...')

if mood.lower() not in ['sloth', 'quokka', 'cheetah']:
    tracks_subset = random.sample(top_10tracks_uri, 20)
    for tracks in tracks_subset:
        track_data = sp.audio_features(tracks)[0]
        track_ids.append(track_data['uri'])

    else:
        val_min, val_max = 0, 1.0
        ene_min, ene_max = 0, 1.0
        tem_target = None

else:

    if mood.lower() == 'sloth':
        val_min, val_max = 0, 0.3
        ene_min, ene_max = 0, 0.3
        tem_min, tem_max = 0, 140
        tem_target = 100

    elif mood.lower() == 'quokka':
        val_min, val_max = 0.4, 0.7
        ene_min, ene_max = 0.4, 0.7
        tem_min, tem_max = 100, 170
        tem_target = 140

    elif mood.lower() == 'cheetah':
        val_min, val_max = 0.7, 1.0
        ene_min, ene_max = 0.7, 1.0
        tem_min, tem_max = 160, 230
        tem_target = 180

find_new_songs = sp.recommendations(
    seed_tracks= random_seeds_tracks,
    limit=[20],
    min_valence=val_min,
    max_valence=val_max,
    min_energy=ene_min,
    max_energy=ene_max,
    target_tempo = tem_target,
    # max_popularity = [20]
    )

for i, j in enumerate(find_new_songs['tracks']):
    track_ids.append(j['id'])
    print('{})\"{}\" by \"{}\"'.format(i + 1, j['name'], j['artists'][0]['name']))

audio_f = sp.audio_features(track_ids)
print(audio_f)


#playlist_name = 'Embrace your mood and dance with it!'

#playlist_new = sp.user_playlist_create(username, playlist_name, public=True, description='save at least one new song!')


#add_songs = sp.user_playlist_add_tracks(username, playlist_new['id'], track_ids)

# in this way I am rewriting on the already made playlist
add_songs = sp.user_playlist_replace_tracks(username, playlist_id, track_ids)

#url = playlist_new['external_urls']['spotify']

print('Your playlist is ready at {}'.format(playlist_url))
