from os import remove

from flask import Flask, redirect, request, session, render_template
import spotipy
import uuid

from playlist_utils import get_top_artists, get_top_10songs_from_artists, generate_playlist
from session_utils import get_sp_oauth, get_token_from_session, session_cache_path
from credentials import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY

TOP_TRACKS = []
SP = []


@app.route("/sign_in")
def sign_in():
    sp_oauth = get_sp_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route('/sign_out')
def sign_out():
    try:
        # Remove the CACHE file (.cache-test) so that a new user can authorize.
        remove(session_cache_path())
        session.clear()
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))
    return redirect('/')


@app.route('/sloth')
def sloth():
    global TOP_TRACKS
    global SP

    val_min, val_max = 0, 0.3
    ene_min, ene_max = 0, 0.3
    tem_target = 100

    return generate_playlist(SP, TOP_TRACKS, val_min, val_max, ene_min, ene_max, tem_target)


@app.route('/cheetah')
def cheetah():
    global TOP_TRACKS
    global SP

    val_min, val_max = 0.7, 1.0
    ene_min, ene_max = 0.7, 1.0
    tem_target = 180

    return generate_playlist(SP, TOP_TRACKS, val_min, val_max, ene_min, ene_max, tem_target)


@app.route('/quokka')
def quokka():
    global TOP_TRACKS
    global SP

    val_min, val_max = 0.4, 0.7
    ene_min, ene_max = 0.4, 0.6
    tem_target = 140

    return generate_playlist(SP, TOP_TRACKS, val_min, val_max, ene_min, ene_max, tem_target)


@app.route('/curious')
def curious():
    global TOP_TRACKS
    global SP

    val_min, val_max = 0, 1.0
    ene_min, ene_max = 0, 1.0
    tem_target = None

    return generate_playlist(SP, TOP_TRACKS, val_min, val_max, ene_min, ene_max, tem_target)


@app.route("/callback")
def api_callback():
    sp_oauth = get_sp_oauth()

    code = request.args.get('code')
    session["token_info"] = sp_oauth.get_access_token(code)

    return redirect("start")


@app.route("/start")
def start():
    if not session.get('uuid'):
        session['uuid'] = str(uuid.uuid4()) # random ID for unknown user

    session['token_info'], authorized = get_token_from_session(session)
    session.modified = True
    if not authorized:
        return redirect('sign_in')

    global SP
    SP = spotipy.Spotify(auth=session.get('token_info').get('access_token'))

    # This takes too long - can run in background?
    global TOP_TRACKS
    TOP_TRACKS = get_top_10songs_from_artists(SP, get_top_artists(SP))

    return f'<h2>Hi {SP.me()["display_name"]}, how do you feel today? ' \
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
    app.run(debug=False)
