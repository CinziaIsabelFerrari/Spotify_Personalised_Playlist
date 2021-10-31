import csv
from os.path import isfile, join, dirname, realpath

SCOPE = 'user-library-read user-top-read playlist-modify-public user-follow-read playlist-read-private playlist-modify-private'
PLAYLIST_FILE_FILENAME = 'generated_playlist_info.csv'
PLAYLIST_FILE_PATH = join(dirname(realpath(__file__)), PLAYLIST_FILE_FILENAME)
MOOOODY_PLAYLIST_NAME = 'Embrace your mood and dance with it!'

def get_top_artists(sp_auth):
    """
    Gets top artists

    :param sp_auth: spotipy.Spotify
    :return: list
    """

    top_artists_name = []
    top_artists_uri = []

    ranges = ['short_term',
              'medium_term']  # short term range means 4 weeks, medium is 6 months and long-term is of all time
    for r in ranges:
        all_top_artists = sp_auth.current_user_top_artists(limit=100, time_range=r)
        top_artists_data = all_top_artists['items']
        for artist_data in top_artists_data:
            if artist_data['name'] not in top_artists_name:
                top_artists_name.append(artist_data['name'])
                top_artists_uri.append(artist_data['uri'])
        return top_artists_uri


def get_top_10songs_from_top_artists(sp_auth, top_artists_uri):
    """
    Gets 10 top songs given artist uris

    :param sp_auth: spotipy.Spotify
    :param top_artists_uri: list
    :return: list
    """

    top_10tracks_uri = []
    for artist in top_artists_uri:
        top_tracks_all = sp_auth.artist_top_tracks(artist)
        top_tracks = top_tracks_all['tracks']
        for track_data in top_tracks:
            top_10tracks_uri.append(track_data['uri'])
    return top_10tracks_uri


def create_playlist_file(id, url, file_path=PLAYLIST_FILE_PATH):
    """
    Creates a playlist id and url info file

    :param id: str
    :param url: str
    :param file_path: str
    """

    if isfile(file_path):
        raise ValueError('Trying to create new playlist info file but file already exists')
    else:
        playlist_info = [id, url]
        print('Saving playlist info to {}'.format(file_path))
        with open(file_path, 'w', newline='') as f:
            wr = csv.writer(f, quoting=csv.QUOTE_ALL)
            wr.writerow(playlist_info)


def read_playlist_file(file_path=PLAYLIST_FILE_PATH):
    """
    Reads an existing playlist info file to retrieve id and url

    :param file_path: str
    :return: str, str
    """

    if not isfile(file_path):
        raise ValueError('Trying to update playlist info file but file {} does not exist'.format(file_path))
    else:
        print('Reading existing playlist info from {}'.format(file_path))
        with open(file_path, newline='') as f:
            reader = csv.reader(f)
            playlist_info = list(reader)

        id, url = playlist_info[0][0], playlist_info[0][1]
        return id, url
