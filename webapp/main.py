from flask import Flask, redirect, request, session, render_template
import uuid
from os import makedirs, path, remove

from playlist_utils import MoooodyPlaylist
from data_utils import session_cache_path, UserData, CACHES_FOLDER
from credentials import SECRET_KEY


app = Flask(__name__)
app.secret_key = SECRET_KEY

MOOOODY_PLAYLIST_NAME = 'Embrace your mood and dance with it!'

if not path.exists(CACHES_FOLDER):
    makedirs(CACHES_FOLDER)

user_data = UserData()
playlist = MoooodyPlaylist()


def clear_all_data():
    try:
        remove(session_cache_path())
        session.clear()
        user_data.clear()
        playlist.clear()
    except OSError as e:
        print(f'Error: {e.filename} - {e.strerror}.')

@app.route("/sign_in")
def sign_in():
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
        user_data.set_token_from_code(code)
        return redirect("start")

    else:
        return redirect("/")


@app.route('/generate/<title>/')
def generate(title):

    if not playlist.ready_to_generate():
        return redirect("/")

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

    playlist.generate_playlist(val, ene, tem, title)
    return render_template('gotolink.html', title=title.capitalize(), url=playlist.url,
                           color=color)


@app.route("/start")
def start():

    if not session.get('uuid'):
        session['uuid'] = str(uuid.uuid4())

    user_data.get_cached_token()

    if user_data.token is None:
        return redirect('sign_in')

    user_data.authenticate()

    playlist.set_sp(user_data.sp)
    valid_process = playlist.preprocess_top_artists()
    if not valid_process:
        clear_all_data()
        return render_template('moodpage.html')

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
