from flask import Flask, redirect, request, session, render_template
import uuid
from os import makedirs, path, remove

from playlist_utils import MoooodyPlaylist
from data_utils import session_cache_path, UserData
from credentials import SECRET_KEY


app = Flask(__name__)
app.secret_key = SECRET_KEY

CACHES_FOLDER = './.spotify_caches/'
MOOOODY_PLAYLIST_NAME = 'Embrace your mood and dance with it!'

if not path.exists(CACHES_FOLDER):
    makedirs(CACHES_FOLDER)


def clear_all_data():
    try:
        remove(session_cache_path())
    except OSError:
        pass
    session.clear()


@app.route("/sign_in")
def sign_in():
    user_data = UserData()
    auth_url = user_data.get_authorize_url()
    return redirect(auth_url)


@app.route('/sign_out')
def sign_out():
    clear_all_data()
    return redirect('/')


@app.route("/callback")
def api_callback():
    code = request.args.get('code')

    if code:
        user_data = UserData()
        user_data.set_token_from_code(code)
        return redirect("start")

    else:
        return redirect("/")


@app.route('/generate/<title>/')
def generate(title):

    if session.get('uuid') is None:
        redirect('start')

    user_data = UserData()
    user_data.get_cached_token()
    user_data.authenticate()

    playlist = MoooodyPlaylist()
    playlist.set_sp(user_data.sp)

    valid_process = playlist.preprocess_top_artists()

    # Deny access if no artists are found (Freemium users)
    if not valid_process:
        clear_all_data()
        return render_template('denied.html')

    playlist.search_for_playlist()

    if not playlist.ready_to_generate():
        return redirect("/")

    playlist.generate_playlist(title)

    if title == 'sloth':
        color = ["#0288d1", "#1a237e"]

    elif title == 'quokka':
        color = ["#ffd54f", "#ff9800"]

    elif title == 'cheetah':
        color = ["#cc0000", "#c51162"]

    elif title == 'curious':
        color = ["#ab47bc", "#00c853"]

    else:
        raise ValueError('Invalid title')

    return render_template('gotolink.html', title=title.capitalize(),
                            url=playlist.url, color=color)


@app.route("/start")
def start():
    if session.get('uuid') is None:
        session['uuid'] = str(uuid.uuid4())

    user_data = UserData()
    user_data.get_cached_token()
    if user_data.token is None:
        return redirect('sign_in')

    return render_template('moodpage.html')


@app.route("/index", methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route("/")
def entry():
    return redirect('index')


if __name__ == "__main__":
    app.run(debug=True)
