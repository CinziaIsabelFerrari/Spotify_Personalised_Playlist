from flask import Flask, redirect, request, session, render_template
import uuid
from os import makedirs, path, remove

import spotipy

from credentials import SECRET_KEY, CLI_ID, CLI_SEC, REDIRECT_URI
from playlist_utils import MoooodyPlaylist, SLOTH_VALUES, QUOKKA_VALUES, CURIOUS_VALUES, CHEETAH_VALUES

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


@app.route('/generate/<float:val_min>/<float:val_max>/<float:ene_min>/<float:ene_max>/<tem_target>')
def generate(val_min, val_max, ene_min, ene_max, tem_target):
    if tem_target == "null":
        tem_target = None

    val = [val_min, val_max]
    ene = [ene_min, ene_max]

    playlist.generate_playlist(val, ene, tem_target)
    return f'Enjoy your playlist!' \
        f'<a href="{playlist.url}" target="_blank">LINK</a>'


@app.route("/start")
def start():

    if not session.get('uuid'):
        session['uuid'] = str(uuid.uuid4())

    if user_data.token is None:
        return redirect('sign_in')

    user_data.authenticate()

    playlist.set_sp(user_data.sp)
    playlist.preprocess_top_artists()
    playlist.search_for_playlist()

    return f'<h2>Hi {user_data.sp.me()["display_name"]}, how do you feel today? ' \
        f'<small><a href="/sign_out">[sign out]<a/></small></h2>' \
        f'<a href="/generate/{SLOTH_VALUES}">SLOTH</a> | ' \
        f'<a href="/generate/{QUOKKA_VALUES}">QUOKKA</a> | ' \
        f'<a href="/generate/{CHEETAH_VALUES}">CHEETAH</a> | ' \
        f'<a href="/generate/{CURIOUS_VALUES}">CURIOUS</a>' \


@app.route("/index", methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route("/")
def entry():
    return redirect('index')


if __name__ == "__main__":
    app.run(debug=True)
