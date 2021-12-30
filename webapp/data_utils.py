from flask import session
from os import path, remove
import spotipy

from credentials import CLI_ID, CLI_SEC, REDIRECT_URI

CACHES_FOLDER = './.spotify_caches/'
SCOPE = 'playlist-modify-public,user-top-read'

def session_cache_path():
    return CACHES_FOLDER + session.get('uuid')


class UserData():
    def __init__(self):
        self.token = None
        self.sp_oauth = None
        self.sp = None

    def get_cached_token(self):
        if path.exists(session_cache_path()):
            cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
            sp_oauth = spotipy.oauth2.SpotifyOAuth(CLI_ID, CLI_SEC, REDIRECT_URI,
                        scope=SCOPE,
                        cache_handler=cache_handler,
                        show_dialog=True)
            if not sp_oauth.validate_token(cache_handler.get_cached_token()):
                remove(session_cache_path())
            else:
                self.token = cache_handler.get_cached_token()['access_token']

    def get_sp_oauth(self):
        cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
        if self.sp_oauth is None:
            self.sp_oauth = spotipy.oauth2.SpotifyOAuth(CLI_ID, CLI_SEC, REDIRECT_URI,
                    scope=SCOPE,
                    cache_handler=cache_handler,
                    show_dialog=True)

        return self.sp_oauth

    def set_token_from_code(self, code):
        sp_auth = self.get_sp_oauth()
        self.token = sp_auth.get_access_token(code)['access_token']

    def authenticate(self):
        self.sp = spotipy.Spotify(auth=self.token)

    def get_authorize_url(self):
        sp_oauth = self.get_sp_oauth()
        return sp_oauth.get_authorize_url()

    def clear(self):
        self.token = None
        self.sp_oauth = None
        self.sp = None
