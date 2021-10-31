import random

MOOOODY_PLAYLIST_NAME = 'Embrace your mood and dance with it!'


def generate_playlist(sp, top_tracks, val_min, val_max, ene_min, ene_max, tem_target):
    # top_tracks = get_top_10songs_from_artists(sp, get_top_artists(sp))
    random.shuffle(top_tracks)
    random_seed_tracks = random.sample(top_tracks, 2)

    # Now based on the mood I will select specific parameters for the tracks of my new playlist
    track_ids = []
    recommended_songs = sp.recommendations(
        seed_tracks=random_seed_tracks,
        limit=[20],
        min_valence=val_min,
        max_valence=val_max,
        min_energy=ene_min,
        max_energy=ene_max,
        target_tempo=tem_target,
    )

    track_ids = [i['id'] for i in recommended_songs['tracks']]
    user_playlists = sp.user_playlists(sp.me()['id'])

    # if user already has playlist, update it
    playlist_replaced = False
    for i in range(len(user_playlists['items'])):
        if user_playlists['items'][i]['name'] == MOOOODY_PLAYLIST_NAME:
            sp.playlist_replace_items(user_playlists['items'][i]['id'], track_ids)
            playlist_url = user_playlists['items'][i]['external_urls']['spotify']
            playlist_replaced = True
            break

    # if playlist not found, create it
    if not playlist_replaced:
        playlist = sp.user_playlist_create(sp.me()['id'], MOOOODY_PLAYLIST_NAME, public=True)
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

    artists_short = sp_auth.current_user_top_artists(limit=100, time_range='short_term')['items']
    artists_medium = sp_auth.current_user_top_artists(limit=100, time_range='medium_term')['items']

    artists_short_uris = [i['uri'] for i in artists_short]
    artists_medium_uris = [i['uri'] for i in artists_medium]
    top_artists_uris = artists_short_uris + artists_medium_uris
    top_artists_uris = list(dict.fromkeys(top_artists_uris)) # Remove duplicates

    return top_artists_uris


def get_top_10songs_from_artists(sp_auth, artists_uri):
    """
    Gets 10 top songs given artist uris
    :param sp_auth: spotipy.Spotify
    :param artists_uri: list
    :return: list
    """

    top_10tracks_uri = []
    for artist in artists_uri:
        top_tracks_all = sp_auth.artist_top_tracks(artist)
        top_tracks = top_tracks_all['tracks']
        for track_data in top_tracks:
            top_10tracks_uri.append(track_data['uri'])
    return top_10tracks_uri
