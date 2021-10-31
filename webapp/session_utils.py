from os import path, makedirs
from time import time

from flask import session
import spotipy

from credentials import CLI_ID, CLI_SEC, REDIRECT_URI

SCOPE = 'playlist-modify-private,playlist-modify-public,user-top-read'


caches_folder = './.spotify_caches/'
if not path.exists(caches_folder):
    makedirs(caches_folder)


def session_cache_path():
    return caches_folder + session.get('uuid')


def get_sp_oauth():
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    sp_oauth = spotipy.oauth2.SpotifyOAuth(CLI_ID, CLI_SEC, REDIRECT_URI,
        scope=SCOPE,
        cache_handler=cache_handler,
        show_dialog=True)
    return sp_oauth


# Checks to see if token is valid and gets a new token if not
def get_token_from_session(session):
    token_valid = False
    token_info = session.get("token_info", {})

    # Checking if the session already has a token stored
    if not (session.get('token_info', False)):
        token_valid = False
        return token_info, token_valid

    # Checking if token has expired
    now = int(time())
    is_token_expired = session.get('token_info').get('expires_at') - now < 60

    # Refreshing token if it has expired
    if (is_token_expired):
        sp_oauth = get_sp_oauth()
        token_info = sp_oauth.refresh_access_token(session.get('token_info').get('refresh_token'))

    token_valid = True
    return token_info, token_valid
