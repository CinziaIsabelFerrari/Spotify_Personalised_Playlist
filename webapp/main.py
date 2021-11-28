from flask import Flask, redirect, request, session, render_template
import uuid
from os import makedirs, path, remove

import spotipy
from playlist_utils import get_random_tracks_from_random_artists, get_top_artists, generate_playlist
from credentials import SECRET_KEY, CLI_ID, CLI_SEC, REDIRECT_URI

SCOPE = 'playlist-modify-private,playlist-modify-public,user-top-read'

app = Flask(__name__)
app.secret_key = SECRET_KEY


caches_folder = './.spotify_caches/'
if not path.exists(caches_folder):
    makedirs(caches_folder)


def session_cache_path():
    return caches_folder + session.get('uuid')


class UserData():
    def __init__(self):
        self.token = None
        self.top_artists = None
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
        self.token = self.sp_oauth.get_access_token(code)['access_token']

    def preprocess_top_artists(self):
        self.top_artists = get_top_artists(self.sp)

    def get_random_seed_tracks(self):
        return get_random_tracks_from_random_artists(self.sp, self.top_artists)

    def authenticate(self):
        self.sp = spotipy.Spotify(auth=user_data.token)


user_data = UserData()


@app.route("/sign_in")
def sign_in():
    sp_oauth = user_data.get_sp_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route('/sign_out')
def sign_out():
    try:
        remove(session_cache_path())
        session.clear()
    except OSError as e:
        print (f'Error: {e.filename} - {e.strerror}.')
    return redirect('/')


@app.route("/callback")
def api_callback():
    code = request.args.get('code')
    sp_oauth = user_data.get_sp_oauth()
    user_data.set_token_from_code(code)
    return redirect("start")


@app.route('/sloth')
def sloth():
    val_min, val_max = 0, 0.3
    ene_min, ene_max = 0, 0.3
    tem_target = 100

    seed_tracks = user_data.get_random_seed_tracks()
    return generate_playlist(user_data.sp, seed_tracks, val_min, val_max, ene_min, ene_max, tem_target)


@app.route('/cheetah')
def cheetah():
    val_min, val_max = 0.7, 1.0
    ene_min, ene_max = 0.7, 1.0
    tem_target = 180

    seed_tracks = user_data.get_random_seed_tracks()
    return generate_playlist(user_data.sp, seed_tracks, val_min, val_max, ene_min, ene_max, tem_target)


@app.route('/quokka')
def quokka():
    val_min, val_max = 0.4, 0.7
    ene_min, ene_max = 0.4, 0.6
    tem_target = 140

    seed_tracks = user_data.get_random_seed_tracks()
    return generate_playlist(user_data.sp, seed_tracks, val_min, val_max, ene_min, ene_max, tem_target)


@app.route('/curious')
def curious():
    val_min, val_max = 0, 1.0
    ene_min, ene_max = 0, 1.0
    tem_target = None

    seed_tracks = user_data.get_random_seed_tracks()
    return generate_playlist(user_data.sp, seed_tracks, val_min, val_max, ene_min, ene_max, tem_target)


@app.route("/start")
def start():

    if not session.get('uuid'):
        session['uuid'] = str(uuid.uuid4())

    if user_data.token is None:
        return redirect('sign_in')

    user_data.authenticate()
    user_data.preprocess_top_artists()

    return f'<h2>Hi {user_data.sp.me()["display_name"]}, how do you feel today? ' \
        f'<small><a href="/sign_out">[sign out]<a/></small></h2>' \
        f'<a href="/sloth">SLOTH</a> | ' \
        f'<a href="/quokka">QUOKKA</a> | ' \
        f'<a href="/cheetah">CHEETAH</a> | ' \
        f'<a href="/curious">CURIOUS</a>' \


@app.route("/index", methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route("/")
def entry():
    return redirect('index')


if __name__ == "__main__":
    app.run(debug=True)
