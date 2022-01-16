import logging
import random

logger = logging.getLogger(__name__)
MOOOODY_PLAYLIST_NAME = 'Embrace your mood and dance with it!'


class MoooodyPlaylist():
    def __init__(self):
        self.sp = None
        self.top_artists = None
        self.id = None
        self.url = None

    def set_sp(self, sp):
        self.sp = sp

    def preprocess_top_artists(self):
        if not self.sp:
            raise ValueError()

        artists_short = self.sp.current_user_top_artists(
            limit=100, time_range='short_term')['items']
        artists_medium = self.sp.current_user_top_artists(
            limit=100, time_range='medium_term')['items']
        artists = artists_short + artists_medium
        artists_uris = [i['uri'] for i in artists]
        artists_uris = list(dict.fromkeys(artists_uris))  # Remove duplicates
        self.top_artists = artists_uris

        if not self.top_artists:
            return False
        else:
            return True

    def search_for_playlist(self):
        if not self.sp:
            raise ValueError()

        all_playlists = self.sp.user_playlists(self.sp.me()['id'])

        # check if user already has playlist
        for p in all_playlists['items']:
            if p['name'] == MOOOODY_PLAYLIST_NAME:
                self.id = p['id']
                self.url = p['external_urls']['spotify']
                break

    def get_random_seed_tracks(self):
        """
        Gets single random track per artist
        :param sp_auth: spotipy.Spotify
        :param artists_uris: list
        :return: list
        """
        artists_uris = random.sample(self.top_artists, 2)

        track_uris = []
        for artist in artists_uris:
            top_tracks = self.sp.artist_top_tracks(artist)['tracks']
            random_track = random.sample(top_tracks, 1)[0]
            track_uris.append(random_track['uri'])

        return track_uris

    def create_new_playlist(self):
        p = self.sp.user_playlist_create(self.sp.me()['id'],
                                         MOOOODY_PLAYLIST_NAME,
                                         public=True)
        self.id = p['id']
        self.url = p['external_urls']['spotify']

    def get_playlist_id(self):
        if self.id is None:
            self.create_new_playlist()

        return self.id

    def generate_playlist(self, title):

        if title == 'sloth':
            val = [0.0, 0.3]
            ene = [0.0, 0.3]
            tem = 100

        if title == 'quokka':
            val = [0.4, 0.7]
            ene = [0.4, 0.6]
            tem = 140

        if title == 'cheetah':
            val = [0.7, 1.0]
            ene = [0.7, 1.0]
            tem = 180

        if title == 'curious':
            val = [0.0, 1.0]
            ene = [0.0, 1.0]
            tem = None

        logger.info('Seeking seed tracks')
        seed_tracks = self.get_random_seed_tracks()

        logger.info('Requesting recommendations')
        track_ids = []
        recommended_songs = self.sp.recommendations(
            seed_tracks=seed_tracks,
            min_valence=val[0],
            max_valence=val[1],
            min_energy=ene[0],
            max_energy=ene[1],
            target_tempo=tem,
        )

        logger.info('Updating playlist')
        track_ids = [i['id'] for i in recommended_songs['tracks']]
        self.sp.playlist_replace_items(self.get_playlist_id(), track_ids)
        self.sp.playlist_change_details(
            self.get_playlist_id(),
            description=f"A {title.capitalize()} playlist created by CiPi at https://moooody.pythonanywhere.com/")

        logger.info('Playlist generation done')

    def ready_to_generate(self):
        if self.sp is None or self.top_artists is None:
            return False
        else:
            return True
