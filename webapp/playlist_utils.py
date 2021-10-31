import random

MOOOODY_PLAYLIST_NAME = 'Embrace your mood and dance with it!'


def generate_playlist(sp, seed_tracks, val_min, val_max, ene_min, ene_max, tem_target):
    track_ids = []
    recommended_songs = sp.recommendations(
        seed_tracks=seed_tracks,
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

def get_random_top_artists(sp_auth, artists_per_range=2):
    """
    Gets random top artists in short and medium term ranges
    :param sp_auth: spotipy.Spotify
    :return: list
    """

    artists_short = sp_auth.current_user_top_artists(limit=100, time_range='short_term')['items']
    artists_medium = sp_auth.current_user_top_artists(limit=100, time_range='medium_term')['items']
    artists = artists_short + artists_medium

    artists_uris = [i['uri'] for i in artists]
    artists_uris = list(dict.fromkeys(artists_uris)) # Remove duplicates

    random_artists_uris = random.sample(artists_uris, 2)
    
    return random_artists_uris

def get_random_tracks_from_artists(sp_auth, artists_uri):
    """
    Gets single random track per artist
    :param sp_auth: spotipy.Spotify
    :param artists_uri: list
    :return: list
    """
    track_uris = []

    for artist in artists_uri:
        top_tracks = sp_auth.artist_top_tracks(artist)['tracks']
        random_track = random.sample(top_tracks, 1)[0]
        track_uris.append(random_track['uri'])

    return track_uris
