from flask import Flask, redirect, request, session, render_template
import uuid
from os import makedirs, path, remove
from os.path import exists

import spotipy

from credentials import SECRET_KEY, CLI_ID, CLI_SEC, REDIRECT_URI
from playlist_utils import MoooodyPlaylist

SCOPE = 'playlist-modify-private,playlist-modify-public,user-top-read'

app = Flask(__name__)
app.secret_key = SECRET_KEY

MOOOODY_PLAYLIST_NAME = 'Embrace your mood and dance with it!'
CACHES_FOLDER = './.spotify_caches/'

if not path.exists(CACHES_FOLDER):
        makedirs(CACHES_FOLDER)

def session_cache_path():
    return CACHES_FOLDER + session.get('uuid')


class UserData():
    def __init__(self):
        self.token = None
        self.sp_oauth = None
        self.sp = None

    def get_cached_token(self):
        if exists(session_cache_path()):
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
        self.sp = spotipy.Spotify(auth=user_data.token)

    def get_authorize_url(self):
        sp_oauth = user_data.get_sp_oauth()
        return sp_oauth.get_authorize_url()

    def clear(self):
        self.token = None
        self.sp_oauth = None
        self.sp = None


user_data = UserData()
playlist = MoooodyPlaylist()


@app.route("/sign_in")
def sign_in():
    auth_url = user_data.get_authorize_url()
    return redirect(auth_url)


@app.route('/sign_out')
def sign_out():
    try:
        remove(session_cache_path())
        session.clear()
        user_data.clear()
        playlist.clear()
    except OSError as e:
        print(f'Error: {e.filename} - {e.strerror}.')
    return redirect('/')


@app.route("/callback")
def api_callback():
    code = request.args.get('code')
    user_data.set_token_from_code(code)
    return redirect("start")


@app.route('/generate/<title>/')
def generate(title):

    if title == 'sloth':
        val = [0.0, 0.3]
        ene = [0.0, 0.3]
        tem = 100
        color = ["#0288d1", "#1a237e"]

    if title == 'quokka':
        val = [0.4, 0.7]
        ene = [0.4, 0.6]
        tem = 140
        color = ["#ffd54f", "#ff9800"]

    if title == 'cheetah':
        val = [0.7, 1.0]
        ene = [0.7, 1.0]
        tem = 180
        color = ["#cc0000", "#c51162"]

    if title == 'curious':
        val = [0.0, 1.0]
        ene = [0.0, 1.0]
        tem = None
        color = ["#ab47bc", "#00c853"]

    playlist.generate_playlist(val, ene, tem)
    return render_template('gotolink.html', title = title.capitalize(), url = playlist.url,
                            color = color)


@app.route("/start")
def start():

    if not session.get('uuid'):
        session['uuid'] = str(uuid.uuid4())

    user_data.get_cached_token()

    if user_data.token is None:
        return redirect('sign_in')

    user_data.authenticate()

    playlist.set_sp(user_data.sp)
    playlist.preprocess_top_artists()
    playlist.search_for_playlist()

    return render_template('moodpage.html')


@app.route("/index", methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route("/")
def entry():
    return redirect('index')


if __name__ == "__main__":
    app.run(debug=True)
