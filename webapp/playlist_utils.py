import random

MOOOODY_PLAYLIST_NAME = 'Embrace your mood and dance with it!'

def get_playlist(sp, val_min, val_max, ene_min, ene_max, tem_target):
    print('getting playlist')
    # Finding my top artists 100 and their top 10 songs:
    top_artists_uri_c = get_top_artists(sp)

    # Get top tracks and shuffle
    top_10tracks_uri_c = get_top_10songs_from_top_artists(sp, top_artists_uri_c)
    random.shuffle(top_10tracks_uri_c)

    # Get 2 random tracks to use as seeds
    random_seed_tracks = random.sample(top_10tracks_uri_c, 2)

    # Now based on the mood I will select specific parameters for the tracks of my new playlist
    track_ids = []
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

    # if user has playlist with the same name, overwrite it
    user_playlists = sp.user_playlists(sp.me()['id'])
    for i in range(len(user_playlists['items'])):
        if user_playlists['items'][i]['name'] == MOOOODY_PLAYLIST_NAME:
            print('Unfollowing playlist with name {}'.format(user_playlists['items'][i]['name']))
            sp.user_playlist_unfollow(sp.me()['id'], user_playlists['items'][i]['id'])

    # Creating new playlist
    playlist_name = MOOOODY_PLAYLIST_NAME
    playlist = sp.user_playlist_create(sp.me()['id'], playlist_name, public=True)
    playlist_id, playlist_url = playlist['id'], playlist['external_urls']['spotify']

    sp.playlist_add_items(playlist_id, track_ids)

    return f'Enjoy your playlist!' \
            f'<a href="{playlist_url}" target="_blank">LINK</a>'

def get_top_artists(sp_auth):
    """
    Gets top artists
    :param sp_auth: spotipy.Spotify
    :return: list
    """

    top_artists_name = []
    top_artists_uri = []

    ranges = ['short_term',
              'medium_term']  # short term range means 4 weeks, medium is 6 months and long-term is of all time
    for r in ranges:
        all_top_artists = sp_auth.current_user_top_artists(limit=100, time_range=r)
        top_artists_data = all_top_artists['items']
        for artist_data in top_artists_data:
            if artist_data['name'] not in top_artists_name:
                top_artists_name.append(artist_data['name'])
                top_artists_uri.append(artist_data['uri'])
        return top_artists_uri


def get_top_10songs_from_top_artists(sp_auth, top_artists_uri):
    """
    Gets 10 top songs given artist uris
    :param sp_auth: spotipy.Spotify
    :param top_artists_uri: list
    :return: list
    """

    top_10tracks_uri = []
    for artist in top_artists_uri:
        top_tracks_all = sp_auth.artist_top_tracks(artist)
        top_tracks = top_tracks_all['tracks']
        for track_data in top_tracks:
            top_10tracks_uri.append(track_data['uri'])
    return top_10tracks_uri
