import spotipy
import spotipy.util as util
import random


#Defining users and authorization codes

username = '1167152572'
username_j = 'joselusko'

scope = 'user-library-read user-top-read playlist-modify-public user-follow-read playlist-read-private playlist-modify-private'
token = util.prompt_for_user_token(username, scope)
token_j = util.prompt_for_user_token(username_j, scope)

sp = spotipy.Spotify(auth=token)
sp_j = spotipy.Spotify(auth=token_j)

#I already created a playlist so to avoid to create a new one all the time I will rewrite on this one

playlist_id = '3Uvw17LxK0xgJUiiGEebZE'
playlist_url = 'https://open.spotify.com/playlist/3Uvw17LxK0xgJUiiGEebZE'



#Finding top artists 100, mine and Jose's

#short term range means 4 weeks, medium is 6 months and long-term is of all time

def my_top_artists(sp):
    print('Give me a second..')
    top_artists_name_c = []
    top_artists_uri_c = []

    ranges = ['short_term', 'medium_term']
    for r in ranges:
        all_top_artists = sp.current_user_top_artists(limit=100, time_range= r)
        top_artists_data = all_top_artists['items']
        for artist_data in top_artists_data:
            if artist_data['name'] not in top_artists_name_c:
                top_artists_name_c.append(artist_data['name'])
                top_artists_uri_c.append(artist_data['uri'])

    return top_artists_uri_c

def j_top_artists(sp_j):
    print('Give me another second..')
    top_artists_name_j = []
    top_artists_uri_j = []

    ranges = ['short_term', 'medium_term']
    for r in ranges:
        all_top_artists = sp_j.current_user_top_artists(limit=100, time_range= r)
        top_artists_data = all_top_artists['items']
        for artist_data in top_artists_data:
            if artist_data['name'] not in top_artists_name_j:
                top_artists_name_j.append(artist_data['name'])
                top_artists_uri_j.append(artist_data['uri'])

    return top_artists_uri_j


#Now I'm getting the top 10 songs for each of these artists selected

def my_top_artists_top_10songs(sp, top_artists_uri_c):
    print('..I\'m looking into CinCin\'s songs')
    top_10tracks_uri_c = []
    for artist in top_artists_uri_c:
        top_tracks_all = sp.artist_top_tracks(artist)
        top_tracks = top_tracks_all['tracks']
        for track_data in top_tracks:
            top_10tracks_uri_c.append(track_data['uri'])
    return top_10tracks_uri_c

def j_top_artists_top_10songs(sp_j, top_artists_uri_j):
    print('..I\'m looking into Jose\'s songs')
    top_10tracks_uri_j = []
    for artist in top_artists_uri_j:
        top_tracks_all = sp_j.artist_top_tracks(artist)
        top_tracks = top_tracks_all['tracks']
        for track_data in top_tracks:
            top_10tracks_uri_j.append(track_data['uri'])
    return top_10tracks_uri_j


#Now I am calling the functions and shuffling the results

top_artists_uri_c = my_top_artists(sp)

top_10tracks_uri_c = my_top_artists_top_10songs(sp, top_artists_uri_c)


top_artists_uri_j = j_top_artists(sp_j)

top_10tracks_uri_j = j_top_artists_top_10songs(sp_j, top_artists_uri_j)


random.shuffle(top_10tracks_uri_c)
random.shuffle(top_10tracks_uri_j)

#getting 3 random tracks from Cin and 3 from Jose to use as seeds to create the final playlist

random_selected_c = random.sample(top_10tracks_uri_c, 2)
random_selected_j = random.sample(top_10tracks_uri_j, 2)


top_10tracks_uri = random_selected_c + random_selected_j
random.shuffle(top_10tracks_uri)

random_seeds_tracks = top_10tracks_uri

#These 6 tracks will be seeds to find new tracks, and based on the mood I will select specific parameters for the tracks

track_ids = []

mood = input('I\'m ready! How do you feel today? Sloth, Quokka, Cheetah or just curious?')
print('Okay! Picking your tracks...')

if mood.lower() not in ['sloth', 'quokka', 'cheetah']:
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
        ene_min, ene_max = 0.4, 0.6
        tem_min, tem_max = 100, 170
        tem_target = 140

    elif mood.lower() == 'cheetah':
        val_min, val_max = 0.7, 1.0
        ene_min, ene_max = 0.7, 1.0
        tem_min, tem_max = 160, 230
        tem_target = 180


find_new_songs = sp.recommendations(
    seed_tracks= random_seeds_tracks,
    limit=[30],
    min_valence=val_min,
    max_valence=val_max,
    min_energy=ene_min,
    max_energy=ene_max,
    target_tempo = tem_target,
    # max_popularity = [20]
    )


# Here I am printing the name of the songs that will appear in the playlist and the audio features to check that the parameters have been followed correctly

for i, j in enumerate(find_new_songs['tracks']):
    track_ids.append(j['id'])
    print('{})\"{}\" by \"{}\"'.format(i + 1, j['name'], j['artists'][0]['name']))

audio_f = sp.audio_features(track_ids)
print(audio_f)

# in this way I am rewriting on the already made playlist
add_songs = sp.user_playlist_replace_tracks(username, playlist_id, track_ids)


#If I want to create a new playlist I can use these again:

#playlist_name = 'Embrace your mood and dance with it! - Family edition'
#playlist_new = sp.user_playlist_create(username, playlist_name, public=True)
#add_songs= sp.user_playlist_add_tracks(username, playlist_new['id'], track_ids)
#url = playlist_new['external_urls']['spotify']



print('Your playlist is ready at {}'.format(playlist_url))