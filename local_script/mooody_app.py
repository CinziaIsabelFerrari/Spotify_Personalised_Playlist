"""
Prerequisites

    pip3 install spotipy Flask Flask-Session

    // from your [app settings](https://developer.spotify.com/dashboard/applications)
    export SPOTIPY_CLIENT_ID=client_id_here
    export SPOTIPY_CLIENT_SECRET=client_secret_here
    export SPOTIPY_REDIRECT_URI='http://127.0.0.1:8080' // must contain a port
    // SPOTIPY_REDIRECT_URI must be added to your [app settings](https://developer.spotify.com/dashboard/applications)
    OPTIONAL
    // in development environment for debug output
    export FLASK_ENV=development
    // so that you can invoke the app outside of the file's directory include
    export FLASK_APP=/path/to/spotipy/examples/app.py

    // on Windows, use `SET` instead of `export`

Run app.py

    python3 app.py OR python3 -m flask run
    NOTE: If receiving "port already in use" error, try other ports: 5000, 8090, 8888, etc...
        (will need to be updated in your Spotify app and SPOTIPY_REDIRECT_URI variable)
"""

import os
import random
import webbrowser

from flask import Flask, session, request, redirect
from flask_session import Session
import spotipy
import uuid

from utils import *

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)

caches_folder = './.spotify_caches/'
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)

def session_cache_path():
    return caches_folder + session.get('uuid')

def validate_token_from_cache():
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    sp = spotipy.Spotify(auth_manager=auth_manager)
    return sp


def get_playlist(sp, val_min, val_max, ene_min, ene_max, tem_target):
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

    webbrowser.open(playlist_url)

    return 'Enjoy your playlist!'


@app.route('/')
def index():
    if not session.get('uuid'):
        # Step 1. Visitor is unknown, give random ID
        session['uuid'] = str(uuid.uuid4())

    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope=SCOPE,
                                               cache_handler=cache_handler,
                                               show_dialog=True)

    if request.args.get("code"):
        # Step 3. Being redirected from Spotify auth page
        auth_manager.get_access_token(request.args.get("code"))
        return redirect('/')

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 2. Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
        return f'<h2><a href="{auth_url}">Sign in</a></h2>'

    # Step 4. Signed in, display data
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return f'<h2>Hi {spotify.me()["display_name"]}, how do you feel today? ' \
           f'<small><a href="/sign_out">[sign out]<a/></small></h2>' \
           f'<a href="/sloth">SLOTH</a> | ' \
           f'<a href="/quokka">QUOKKA</a> | ' \
		   f'<a href="/cheetah">CHEETAH</a> | ' \
           f'<a href="/curious">CURIOUS</a>' \


@app.route('/sign_out')
def sign_out():
    try:
        # Remove the CACHE file (.cache-test) so that a new user can authorize.
        os.remove(session_cache_path())
        session.clear()
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))
    return redirect('/')


@app.route('/sloth')
def sloth():
    sp = validate_token_from_cache()

    val_min, val_max = 0, 0.3
    ene_min, ene_max = 0, 0.3
    tem_target = 100

    return get_playlist(sp, val_min, val_max, ene_min, ene_max, tem_target)


@app.route('/cheetah')
def cheetah():
    sp = validate_token_from_cache()

    val_min, val_max = 0.7, 1.0
    ene_min, ene_max = 0.7, 1.0
    tem_target = 180

    return get_playlist(sp, val_min, val_max, ene_min, ene_max, tem_target)


@app.route('/quokka')
def quokka():
    sp = validate_token_from_cache()

    val_min, val_max = 0.4, 0.7
    ene_min, ene_max = 0.4, 0.6
    tem_target = 140

    return get_playlist(sp, val_min, val_max, ene_min, ene_max, tem_target)


@app.route('/curious')
def curious():
    sp = validate_token_from_cache()

    val_min, val_max = 0, 1.0
    ene_min, ene_max = 0, 1.0
    tem_target = None

    return get_playlist(sp, val_min, val_max, ene_min, ene_max, tem_target)


'''
Following lines allow application to be run more conveniently with
`python app.py` (Make sure you're using python3)
(Also includes directive to leverage pythons threading capacity.)
'''
if __name__ == '__main__':
    app.run(threaded=True, port=int(os.environ.get("PORT",
                                                   os.environ.get("SPOTIPY_REDIRECT_URI", 8080).split(":")[-1])))